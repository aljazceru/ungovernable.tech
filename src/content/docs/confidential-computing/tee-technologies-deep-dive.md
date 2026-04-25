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
sidebar: {"label":"TEE Technologies Deep Dive"}
---
*Detailed technical analysis of Trusted Execution Environment architectures*

---

## Executive Summary

Confidential Computing protects data **while it is being processed** — the final gap in the data lifecycle. At its core is the **Trusted Execution Environment (TEE)**, a secure hardware enclave that isolates sensitive computations from the rest of the system (OS, hypervisor, cloud provider).

This document provides deep technical analysis of major TEE technologies.

---

## 1. The Problem: Data in Use

Traditional encryption protects data in two states:
- **At rest**: Storage encryption (AES-256, LUKS, TDE)
- **In transit**: TLS/SSL for network communication

The gap: **Data in use** — while being processed by CPU instructions — has historically been plaintext in RAM. This exposes sensitive workloads to:
- Malicious cloud providers or hypervisors
- Row hammer, cold boot attacks
- Malicious insiders with physical access
- Software vulnerabilities in the host OS

Confidential Computing addresses this by creating hardware-protected enclaves where data decrypts only for authorized code executing within the TEE.

---

## 2. Intel Software Guard Extensions (SGX)

### Overview
Intel SGX is the **original** modern confidential computing technology, introduced in 2015 with 6th Generation Core processors (Skylake). It provides **fine-grained enclave protection** at the application level.

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

### Key Components

| Component | Description |
|-----------|-------------|
| **EPC (Enclave Page Cache)** | Specialized memory region in DRAM for encrypted enclave pages |
| **EPCM (EPC Map)** | Metadata table inside CPU tracking enclave pages |
| **MEE (Memory Encryption Engine)** | Hardware block that encrypts/decrypts EPC contents |
| **Enclave Mode** | CPU execution mode granting special memory access semantics |
| **MRENCLAVE** | Measurement hash identifying enclave code + data |
| **REPORT Key** | Key for generating attestation reports |
| **SEAL Key** | Key for encrypting data to persist outside enclave |

### New CPU Instructions

- **EINIT**: Initialize and launch an enclave
- **EENTER**: Transfer control into the enclave
- **EEXIT**: Exit the enclave
- **EADD**: Add pages to an enclave
- **EEXTEND**: Extend enclave measurement (256-byte chunks)
- **EREMOVE**: Remove pages from enclave
- **EGETKEY**: Derive sealing/attestation keys
- **EREPORT**: Create attestation report for another enclave

### Security Properties

- **Memory encryption**: EPC contents encrypted by MEE using keys burned into CPU
- **Access control**: CPU blocks all memory access to EPC except from enclave in enclave mode
- **Isolation**: Even privileged software (OS, hypervisor, SMM) cannot read enclave memory
- **Attestation**: Remote parties can verify the enclave's identity via signed reports

### Limitations

- **Small enclave size**: EPC limited to ~256MB on most CPUs (128MB max)
- **No virtualization**: SGX doesn't support running a full OS; application-level only
- **Page swap limitations**: EPC pages can be swapped but require special handling
- **Attack surface**: Smaller attack surface than VM-level solutions, but fewer features
- **Side-channel vulnerabilities**: Spectre, L1TF, Foreshadow attacks

### Use Cases

- Cryptographic key management
- Secure authentication
- Database query processing on sensitive data
- AI model inference on private data
- Blockchain privacy (transaction validation)

---

## 3. AMD Secure Encrypted Virtualization (SEV)

### Evolution

AMD's confidential computing evolved through three generations:

| Generation | Year | Feature |
|-------------|------|---------|
| **SEV** | 2016 | Memory encryption for VMs |
| **SEV-ES** | 2017 | Encrypted register state |
| **SEV-SNP** | 2021 | Secure Nested Paging (integrity protection) |
| **SEV-SNP ME** | 2024 | Memory Encryption (guest management) |

### SEV Architecture

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

### SEV-SNP Security Properties

1. **Confidentiality**: Each VM has a unique encryption key; hypervisor cannot read VM memory
2. **Integrity**: RAPL (Reverse Address Physical Lookaside) prevents memory remapping attacks
3. **Attestation**: SNP provides hardware-attested launch certificates
4. **Migration**: Supports secure live migration between hosts

### Advantages over SGX

- **Full VM isolation**: Can run entire operating systems
- **Larger workloads**: No enclave size limits
- **Standard virtualization**: Works with KVM, VMware, Hyper-V
- **Multi-vCPU support**: Scales across multiple cores

### Limitations

- **AMD-only**: Only available on EPYC processors (Zen 2+)
- **Hypervisor trust**: Assumes hypervisor cooperation (though SNP mitigates)
- **Performance overhead**: ~1-5% latency for encrypted memory operations
- **Live migration**: More complex than non-confidential VMs

---

## 4. Intel Trust Domain Extensions (TDX)

### Overview
Intel TDX is the successor to SGX, introduced in 2022 to provide VM-level confidential computing. It's designed for cloud environments requiring full OS isolation.

### Key Features

- **Confidential VMs**: Full virtual machines with encrypted memory
- **TDX Module**: New CPU mode for managing confidential VMs
- **TD-Shield**: Memory encryption and isolation
- **Flexibility**: Supports both enumerated and flex-attestation

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

Arm CCA, introduced with Armv9-A architecture (2021), builds on TrustZone while enabling **Realm** execution — a new security world for confidential computing.

### TrustZone -> CCA Evolution

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

### Key Components

| Component | Description |
|-----------|-------------|
| **Realm** | Secure execution environment for confidential VMs |
| **RME (Realm Management Extension)** | Hardware extensions enabling CCA |
| **RMM (Realm Management Monitor)** | Firmware managing Realm lifecycle |
| **Realm(world)** | New physical address space inaccessible to NS/Secure worlds |
| **GPA (Granule Protection Analog)** | Hardware mechanism protecting Realm memory |

### Security Model

- **Realm Management Monitor (RMM)**: Small TCB firmware that mediates all Realm operations
- **Hyp switch**: Hypervisor requests become RMM calls rather than direct hardware access
- **Dynamic allocation**: Realms can grow/shrink memory dynamically
- **Attestation**: RMM provides secure attestation of Realm state

### Advantages

- **Full VM support**: Runs entire OSes in Realms
- **Hardware-verified monitor**: RMM in verified ARM assembly
- **Performance**: Uses VHE (Virtualization Host Extension) for minimal overhead
- **Ecosystem leverage**: Builds on TrustZone ecosystem

---

## 6. Comprehensive Comparison Matrix

| Feature | Intel SGX | AMD SEV-SNP | Intel TDX | Arm CCA |
|---------|-----------|------------|-----------|--------|
| **Isolation Level** | Application | VM | VM | VM |
| **Granularity** | Enclave | Full VM | Confidential VM | Realm |
| **Max Memory** | ~256MB | No limit | No limit | No limit |
| **Multi-tenancy** | Multiple enclaves | Multiple VMs | Multiple VMs | Multiple Realms |
| **Full OS Support** | No | Yes | Yes | Yes |
| **Encryption Key** | Per-enclave | Per-VM | Per-VM | Per-Realm |
| **Integrity Protection** | MEE | RAPL | Yes | GPA |
| **Attestation** | Local/Remote | SNP reports | Remote | RMM attestation |
| **Processor** | Intel (6th gen+) | AMD EPYC (Zen 2+) | Intel (4th gen+) | Armv9 (C1+) |
| **Performance Overhead** | 1-10% | 1-5% | 1-5% | 1-3% |
| **Cloud Support** | Azure, GCP | AWS, Azure, GCP | GCP, Azure | Coming |

### When to Use Each

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

## 7. Cloud Provider Offerings

### AWS Nitro Enclaves

- Uses Nitro hypervisor (custom)
- Provides isolated execution environments
- VPC-attached encrypted containers
- No dedicated hardware TEE; relies on Nitro security model

### Azure Confidential Computing

- **Intel SGX**: DCsv2, DCdsv2 VMs
- **AMD SEV-SNP**: DCasv5, DCadsv5 VMs
- **Intel TDX**: DCasv5 series
- **Attestation**: Azure Attestation service

### Google Cloud Confidential VMs

- **AMD SEV-SNP**: C2D VMs
- **Intel TDX**: C2D VMs (confidential)
- **Confidential Space**: Container-based enclaves
- **Privacy-based encryption**: Customer-managed keys

### Comparison Matrix

| Provider | SGX | SEV-SNP | TDX | Arm CCA |
|----------|-----|--------|--------|-------|
| **AWS** | Nitro Enclaves | ✓ (EC2) | — | — |
| **Azure** | ✓ | ✓ | ✓ | ✓ (preview) |
| **Google** | — | ✓ | ✓ | — |

---

## 8. Attack Surface & Mitigations

### Known Attacks

| Attack | Target | Mitigation |
|--------|--------|------------|
| **Speculative execution** (Spectre) | SGX | Microcode updates, side-channel resistant code |
| **Side channels** (timing) | All TEEs | Constant-time implementations |
| **Row hammer** | SGX | EPC page swapping, refresh rates |
| **L1TF** (Foreshadow) | SGX | BIOS updates, hypervisor patches |
| **Malicious hypervisor** | SEV | SEV-SNP integrity protection |
| **Cold boot attacks** | All | Memory encryption at rest |
| **Firmware attacks** | All | TCB verification, measured boot |

### Defense Layers

1. **Hardware root of trust**: Keys burned into CPU
2. **Secure boot chain**: Verify firmware before execution
3. **Attestation**: Prove TCB state to remote parties
4. **Encryption**: All data at rest inside TEE
5. **Isolation**: No direct hardware access from untrusted software

### Best Practices

- Use latest TEE generation (SEV-SNP > TDX > SGX)
- Keep TCB updated
- Use multiple TEE generations together (defense in depth)
- Implement constant-time code to prevent timing attacks

---

## 9. Implementation Considerations

### For Developers

1. **Choose your TEE**: SGX for fine-grained, SEV/TDX/CCA for full VMs
2. **Minimize TCB**: Only put sensitive code in enclave
3. **Design for attestation**: Plan how to verify enclave identity
4. **Handle secrets carefully**: Never log or expose secrets
5. **Test side-channel resistance**: Use constant-time patterns
6. **Use library OS**: Gramine, Occlum for running unmodified apps

### For Infrastructure

1. **Hardware selection**: Ensure CPU supports required TEE
2. **Firmware updates**: Keep CPU microcode current
3. **Secure boot**: Enable measured/verified boot
4. **Key management**: Use hardware-backed key storage
5. **Monitoring**: Log TEE operations for audit
6. **Attestation service**: Set up RA service for verification

### Recommended Frameworks

- **Gramine**: Library OS for running unmodified apps in SGX
- **Occlum**: Memory-safe OS for SGX enclaves
- **Kata Containers**: VM-based containers with TEE
- **Confidential Containers (CoCo)**: Kubernetes integration
- **Marblerun**: CoCo orchestrator for Kubernetes

---

## 10. Further Reading

- [Confidential Computing Consortium](https://confidentialcomputing.io)
- [Intel SGX Developer Guide](https://software.intel.com/sgx)
- [AMD SEV-SNP Specification](https://www.amd.com/sev-snp)
- [Arm CCA Architecture](https://developer.arm.com/cca)
- [Cloud Security Alliance - Confidential Computing](https://cloudsecurityalliance.org/research/topics/confidential-computing)
- [Gramine Project](https://gramineproject.io/)
- [Occlum](https://occlum.io/)

---

*Part of the Ungovernable.tech knowledge base. Last updated: April 2026*

