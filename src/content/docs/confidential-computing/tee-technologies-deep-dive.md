---
title: "TEE Technologies Deep Dive"
tags:
  - "tee"
  - "sgx"
  - "sev-snp"
  - "arm-cca"
  - "intel-tdx"
  - "confidential-computing"
  - "hardware"
---
*Detailed technical analysis of the major Trusted Execution Environment architectures.*

---

## Summary

Confidential computing protects data while it is being processed. That is the gap left after at-rest and in-transit encryption. The mechanism is the Trusted Execution Environment (TEE): a hardware enclave that isolates a computation from the rest of the system (OS, hypervisor, cloud provider).

This document walks through the major TEE designs in technical detail.

---

## 1. The problem: data in use

Traditional encryption protects data in two states:
- At rest: storage encryption (AES-256, LUKS, TDE).
- In transit: TLS/SSL on the network.

The gap is data in use. While the CPU is working on it, plaintext sits in RAM. That exposes sensitive workloads to:
- Malicious cloud providers or hypervisors.
- Row hammer and cold-boot attacks.
- Malicious insiders with physical access.
- Software vulnerabilities in the host OS.

Confidential computing addresses this by creating hardware-protected enclaves where data is decrypted only for authorized code running inside the TEE.

---

## 2. Intel Software Guard Extensions (SGX)

### Overview
Intel SGX is the first modern confidential-computing technology, introduced in 2015 with 6th-Generation Core processors (Skylake). It provides fine-grained enclave protection at the application level.

### Architecture

```
┌─────────────────────────────────────────────────────┐
│                User Space                          │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐        │
│  │Regular │    │ Enclave │    │Regular │        │
│  │ App A  │    │ (SGX)   │    │ App B  │        │
│  └─────────┘    └─────────┘    └─────────┘        │
│        │             │             │               │
│        └──────┬──────┘────────────┘               │
│               ▼                                    │
│  ┌─────────────────────────────────────────┐     │
│  │       Operating System (Untrusted)       │     │
│  └─────────────────────────────────────────┘     │
│                      │                            │
│  ┌─────────────────────────────────────────┐     │
│  │     System Firmware / BIOS (Untrusted)  │     │
│  └─────────────────────────────────────────┘     │
│                      ▼                             │
│  ┌─────────────────────────────────────────┐     │
│  │    Processor Reserved Memory (PRM)      │     │
│  │  ┌─────────────���─────────────────────┐  │     │
│  │  │    Enclave Page Cache (EPC)         │  │     │
│  │  │  Encrypted Memory Regions          │  │     │
│  │  └───────────────────────────────────┘  │     │
│  └─────────────────────────────────────────┘     │
│                      ▼                            │
│  ┌─────────────────────────────────────────┐     │
│  │         CPU (Trusted)                   │     │
│  │   Memory Encryption Engine (MEE)       │     │
│  └─────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────┘
```

### Key components

| Component | Description |
|-----------|-------------|
| **EPC (Enclave Page Cache)** | Specialized memory region in DRAM for encrypted enclave pages |
| **EPCM (EPC Map)** | Metadata table inside CPU tracking enclave pages |
| **MEE (Memory Encryption Engine)** | Hardware block that encrypts/decrypts EPC contents |
| **Enclave Mode** | CPU execution mode granting special memory access semantics |
| **MRENCLAVE** | Measurement hash identifying enclave code + data |
| **REPORT Key** | Key for generating attestation reports |
| **SEAL Key** | Key for encrypting data to persist outside enclave |

### New CPU instructions

- `EINIT`: initialize and launch an enclave.
- `EENTER`: transfer control into the enclave.
- `EEXIT`: exit the enclave.
- `EADD`: add pages to an enclave.
- `EEXTEND`: extend the enclave measurement (256-byte chunks).
- `EREMOVE`: remove pages from the enclave.
- `EGETKEY`: derive sealing or attestation keys.
- `EREPORT`: create an attestation report for another enclave.

### Security properties

- Memory encryption: EPC contents are encrypted by the MEE using keys burned into the CPU.
- Access control: the CPU blocks all memory access to EPC except from an enclave running in enclave mode.
- Isolation: even privileged software (OS, hypervisor, SMM) cannot read enclave memory.
- Attestation: remote parties can verify the enclave's identity via signed reports.

### Limitations

- Small enclave size: EPC is limited to roughly 256MB on most CPUs (128MB max).
- No virtualization: SGX cannot run a full OS; application-level only.
- Page swap limitations: EPC pages can be swapped but require special handling.
- Attack surface: smaller than VM-level solutions but with fewer features.
- Side-channel vulnerabilities: Spectre, L1TF, Foreshadow attacks.

### Use cases

- Cryptographic key management.
- Secure authentication.
- Database query processing on sensitive data.
- AI model inference on private data.
- Blockchain privacy (transaction validation).

---

## 3. AMD Secure Encrypted Virtualization (SEV)

### Evolution

AMD's confidential computing has gone through several generations:

| Generation | Year (first ship) | Feature |
|-------------|-------------------|---------|
| **SEV** | 2017 (Naples / Zen 1) | Memory encryption per VM |
| **SEV-ES** | 2019 (Rome / Zen 2) | + Encrypted register state |
| **SEV-SNP** | 2021 (Milan / Zen 3) | + Secure Nested Paging (integrity protection via RMP) |
| **SEV-SNP Ciphertext Hiding** | 2024 (Turin / Zen 5) | Hides ciphertext from hypervisor reads (defense vs CipherLeaks-style attacks) |

### SEV architecture

```
┌─────────────────────────────────────────────────────┐
│                   Hypervisor (Untrusted)                │
│  ┌─────────────────────────────���─��──────────────────┐ │
│  │           VMs with encrypted memory              │ │
│  │  ┌─────────────┐   ┌─────────────┐               │ │
│  │  │  VM 1 (SEV) │   │  VM 2 (SEV) │               │ │
│  │  │  Key: K1    │   │  Key: K2    │               │ │
│  │  └─────────────┘   └─────────────┘               │ │
│  └──────────────────────────────────────────────────┘ │
│                         │                              │
│  ┌──────────────────────────────────────────────────┐ │
│  │      System BIOS / AMD-V (Untrusted)             │ │
│  └──────────────────────────────────────────────────┘ │
│                         ▼                             │
│  ┌──────────────────────────────────────────────────┐ │
│  │      AMD EPYC CPU (Encrypted Memory Engine)     │ │
│  │   Per-VM encryption keys, isolated address spaces│ │
│  └──────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────┘
```

### SEV vs SEV-ES vs SEV-SNP

| Feature | SEV | SEV-ES | SEV-SNP |
|---------|-----|-------|---------|
| **Memory encryption** | ✓ | ✓ | ✓ |
| **Register encryption** | — | ✓ | ✓ |
| **Integrity protection** | — | — | ✓ |
| **Data replay prevention** | — | — | ✓ |
| **Malicious hypervisor** | Partial | Partial | ✓ |
| **Side-channel protection** | — | — | ✓ |

### SEV-SNP security properties

1. Confidentiality: each VM has a unique encryption key; the hypervisor cannot read VM memory.
2. Integrity: the RMP (Reverse Map Table) prevents memory remapping attacks. The hypervisor cannot remap a guest physical page to a different host page without invalidating the integrity check.
3. Attestation: SNP provides hardware-attested launch certificates.
4. Migration: supports secure live migration between hosts.

### Advantages over SGX

- Full VM isolation: can run entire operating systems.
- Larger workloads: no enclave size limits.
- Standard virtualization: works with KVM, VMware, Hyper-V.
- Multi-vCPU support: scales across multiple cores.

### Limitations

- AMD-only: only available on EPYC processors (Zen 2+).
- Hypervisor trust: assumes hypervisor cooperation (though SNP mitigates).
- Performance overhead: ~1-5% latency for encrypted memory operations.
- Live migration: more complex than non-confidential VMs.

---

## 4. Intel Trust Domain Extensions (TDX)

### Overview
Intel TDX, introduced in 2022, provides VM-level confidential computing. It is designed for cloud environments that need full OS isolation, complementing rather than replacing SGX.

### Features

- Confidential VMs: full virtual machines with encrypted memory.
- TDX Module: a new CPU mode for managing confidential VMs.
- TD-Shield: memory encryption and isolation.
- Flexibility: supports both enumerated and flex-attestation.

### Architecture

```
┌─────────────────────────────────────────────────────┐
│              Virtual Machine Monitor               │
│                    (VMM - Untrusted)               │
└��────────────────────────────────────────────────────┘
                         │
              ┌────────┴────────┐
              │   TDX Module     │
              │   (CPU mode)     │
              └────────┬────────┘
                         │
┌─────────────────────────────────────────────────────┐
│              Confidential VMs (TD)                 │
│  ┌─────────────┐   ┌─────────────┐   ┌──────────┐ │
│  │   TD 1      │   │   TD 2      │   │  TD N    │ │
│  └─────────────┘   └─────────────┘   └──────────┘ │
└─────────────────────────────────────────────────────┘
```

### Comparison with SGX

| Feature | SGX | TDX |
|---------|-----|-----|
| **Isolation Level** | Enclave (app) | VM |
| **Memory Limit** | ~256MB | No practical limit |
| **Full OS Support** | No | Yes |
| **Performance** | Good | Good |
| **Migration** | Complex | Supported |

---

## 5. Arm Confidential Compute Architecture (CCA)

### Overview

Arm CCA, introduced with the Armv9-A architecture (2021), builds on TrustZone and adds Realm execution: a new security world for confidential computing.

### TrustZone -> CCA evolution

```
TrustZone (Armv8):
┌─────────────────────────────────────┐
│     Normal World (Rich OS)          │
├─────────────────────────────────────┤
│         Secure World (TEE)         │
│    (Static, immutable partitions)  │
└─────────────────────────────────────┘

Armv9 CCA:
┌─────────────────────────────────────┐
│     Normal World (Rich OS/VM)       │
├─────────────────────────────────────┤
│         Secure World (TEE)          │
├─────────────────────────────────────┤
│      NEW: Realm World               │
│   (Dynamic, confidential VMs)     │
└─────────────────────────────────────┘
```

### Key components

| Component | Description |
|-----------|-------------|
| **Realm** | Secure execution environment for confidential VMs |
| **RME (Realm Management Extension)** | Hardware extensions enabling CCA |
| **RMM (Realm Management Monitor)** | Firmware managing Realm lifecycle |
| **Realm(world)** | New physical address space inaccessible to NS/Secure worlds |
| **GPA (Granule Protection Analog)** | Hardware mechanism protecting Realm memory |

### Security model

- Realm Management Monitor (RMM): small TCB firmware that mediates all Realm operations.
- Hyp switch: hypervisor requests become RMM calls rather than direct hardware access.
- Dynamic allocation: Realms can grow and shrink memory dynamically.
- Attestation: RMM provides secure attestation of Realm state.

### Advantages

- Full VM support: runs entire OSes in Realms.
- Hardware-verified monitor: RMM in verified ARM assembly.
- Performance: uses VHE (Virtualization Host Extension) for minimal overhead.
- Ecosystem: builds on the TrustZone ecosystem.

---

## 6. Comparison matrix

| Feature | Intel SGX | AMD SEV-SNP | Intel TDX | Arm CCA |
|---------|-----------|------------|-----------|--------|
| **Isolation Level** | Application | VM | VM | VM |
| **Granularity** | Enclave | Full VM | Confidential VM | Realm |
| **Max Memory** | ~256MB | No limit | No limit | No limit |
| **Multi-tenancy** | Multiple enclaves | Multiple VMs | Multiple VMs | Multiple Realms |
| **Full OS Support** | No | Yes | Yes | Yes |
| **Encryption Key** | Per-enclave | Per-VM | Per-VM | Per-Realm |
| **Integrity Protection** | MEE | RMP (SEV-SNP) | TD-MR (TDX) | RMM attestation |
| **Attestation** | Local/Remote | SNP reports | TD quote | RMM attestation |
| **Processor** | Intel (6th gen Skylake+; client-deprecated 11th gen) | SEV: Zen 1+ (Naples 2017); SEV-SNP: Zen 3+ (Milan 2021) | Intel 5th gen Xeon (Emerald Rapids GA) | Armv9 (C1+) |
| **Performance Overhead** | 1-10% | 1-5% | 1-5% | 1-3% |
| **Cloud Support** | Azure, GCP | AWS, Azure, GCP | GCP, Azure | Coming |

### When to use each

| Use Case | Recommended TEE |
|----------|-----------------|
| Cryptographic key handling | Intel SGX |
| Database query processing | Intel SGX or SEV-SNP |
| Full VM isolation | SEV-SNP or TDX or CCA |
| Cloud-native workloads | SEV-SNP (Azure, AWS) |
| Mobile/Edge | Arm TrustZone/CCA |
| Blockchain validators | SGX or SEV-SNP |
| AI model inference | SEV-SNP (confidential GPU) |
| Enterprise cloud | SEV-SNP or TDX |

---

## 7. Cloud provider offerings

### AWS Nitro Enclaves

- Uses the Nitro hypervisor (custom).
- Provides isolated execution environments.
- VPC-attached encrypted containers.
- No dedicated hardware TEE; relies on the Nitro security model.

### Azure Confidential Computing

- Intel SGX: DCsv2, DCsv3, DCdsv2 VMs.
- AMD SEV-SNP: DCasv5 / ECasv5 / DCadsv5 series.
- Intel TDX: DCesv5 / ECesv5 series (distinct from the SEV-SNP DCasv5).
- Attestation: Microsoft Azure Attestation (MAA).

### Google Cloud Confidential VMs

- AMD SEV (legacy): N2D, C2D.
- AMD SEV-SNP: N2D (Milan, GA June 2024) and newer.
- Intel TDX: C3 (Sapphire Rapids), preview/GA depending on region.
- NVIDIA H100 CC: A3 Confidential (preview as of late 2025).
- Confidential Space: container-based enclaves.
- Customer-managed encryption keys with Cloud KMS.

### Comparison matrix

| Provider | SGX | SEV-SNP | TDX | Arm CCA |
|----------|-----|--------|--------|-------|
| **AWS** | Nitro Enclaves | ✓ (EC2) | — | — |
| **Azure** | ✓ | ✓ | ✓ | ✓ (preview) |
| **Google** | — | ✓ | ✓ | — |

---

## 8. Attack surface and mitigations

### Known attacks

| Attack | Target | Mitigation |
|--------|--------|------------|
| **Speculative execution** (Spectre) | SGX | Microcode updates, side-channel resistant code |
| **Side channels** (timing) | All TEEs | Constant-time implementations |
| **Row hammer** | SGX | EPC page swapping, refresh rates |
| **L1TF** (Foreshadow) | SGX | BIOS updates, hypervisor patches |
| **Malicious hypervisor** | SEV | SEV-SNP integrity protection |
| **Cold boot attacks** | All | Memory encryption at rest |
| **Firmware attacks** | All | TCB verification, measured boot |

### Defense layers

1. Hardware root of trust: keys burned into the CPU.
2. Secure boot chain: verify firmware before execution.
3. Attestation: prove TCB state to remote parties.
4. Encryption: all data at rest inside the TEE.
5. Isolation: no direct hardware access from untrusted software.

### Best practices

- Use the latest TEE generation (SEV-SNP > TDX > SGX).
- Keep TCB updated.
- Combine multiple TEE generations for defense in depth.
- Use constant-time code to prevent timing attacks.

---

## 9. Implementation considerations

### For developers

1. Pick a TEE: SGX for fine-grained, SEV/TDX/CCA for full VMs.
2. Minimize TCB: only put sensitive code in the enclave.
3. Design for attestation: plan how to verify enclave identity.
4. Handle secrets carefully: never log or expose them.
5. Test side-channel resistance: use constant-time patterns.
6. Use a library OS (Gramine, Occlum) for running unmodified apps.

### For infrastructure

1. Hardware selection: ensure the CPU supports the required TEE.
2. Firmware updates: keep CPU microcode current.
3. Secure boot: enable measured/verified boot.
4. Key management: use hardware-backed key storage.
5. Monitoring: log TEE operations for audit.
6. Attestation service: set up remote-attestation services for verification.

### Recommended frameworks

- Gramine: library OS for running unmodified apps in SGX.
- Occlum: memory-safe OS for SGX enclaves.
- Kata Containers: VM-based containers with TEE.
- Confidential Containers (CoCo): Kubernetes integration.
- Marblerun: CoCo orchestrator for Kubernetes.

---

## 10. Further reading

- [Confidential Computing Consortium](https://confidentialcomputing.io)
- [Intel SGX Developer Guide](https://software.intel.com/sgx)
- [AMD SEV-SNP Specification](https://www.amd.com/sev-snp)
- [Arm CCA Architecture](https://developer.arm.com/cca)
- [Cloud Security Alliance - Confidential Computing](https://cloudsecurityalliance.org/research/topics/confidential-computing)
- [Gramine Project](https://gramineproject.io/)
- [Occlum](https://occlum.io/)

---

*Part of the Ungovernable.tech knowledge base. Last updated: April 2026*

