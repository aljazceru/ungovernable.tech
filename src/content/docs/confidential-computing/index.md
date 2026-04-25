---
title: "Confidential Computing"
tags:
  - "confidential-computing"
  - "tee"
  - "sgx"
  - "sev-snp"
  - "tdx"
  - "cryptography"
sidebar: {"label":"Overview","order":0}
---
## Summary

Confidential computing keeps data encrypted while it is being processed, not only at rest and in transit. Disk encryption protects bytes on the platter; TLS protects bytes on the wire. Both leave plaintext sitting in DRAM where the CPU works on it. Trusted Execution Environments (TEEs) close that gap by carving out memory regions the OS, the hypervisor, and the cloud operator cannot read.

Common uses:
- Privacy-preserving cloud AI: inference on inputs the operator never sees in plaintext.
- Multi-party computation: each party contributes data without exposing it to the others.
- Blockchain oracles: attested off-chain computation feeding smart contracts.
- Key handling: private keys never leave the enclave.

---

## Historical context

### Early enclaves (2006–2015)

- Intel SGX (Software Guard Extensions) shipped with Skylake in 2015 and let user-space applications create encrypted enclaves.
- ARM TrustZone, an earlier mobile-focused TEE, predates SGX by several years.

### Cloud confidential computing (2017 onward)

The major clouds started offering enclave-backed services:
- AWS Nitro Enclaves (2019): Nitro-based isolated environments.
- Azure Confidential Computing (2017): SGX-based VMs.
- GCP Confidential VMs (2020): AMD SEV-based VMs.

### Modern era (2020 onward)

- AMD SEV-SNP (2020): Secure Nested Paging adds integrity to memory encryption.
- Intel TDX (2022): Trust Domain Extensions for VM-level confidentiality.
- NVIDIA Confidential Computing (2023): GPU enclaves.
- Cloud Native Confidential Computing (CoCo): Kubernetes integration.

---

## How TEEs work

### Trust model

```
┌─────────────────────────────────────────────────────────┐
│                    Untrusted Area                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │   OS       │  │ Hypervisor │  │ Cloud Provider │  │
│  └─────────────┘  └─────────────┘  └─────────────┘   │
└─────────────────────────────────────────────────────────┘
                          ↑
                    [Attestation]
                          │
┌─────────────────────────────────────────────────────────┐
│                    Trusted Area                        │
│  ┌─────────────────────────────────────────────────┐   │
│  │              Enclave Memory                     │   │
│  │  ┌─────────────────────────────────────────┐  │   │
│  │  │         Application Code               │  │   │
│  │  │         + Sensitive Data                │  │   │
│  │  └─────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

Three properties matter:
- Isolation: enclave memory is encrypted and walled off from all other software.
- Attestation: remote parties can verify the enclave's identity and code hash.
- Sealing: data can be encrypted so only the same enclave can decrypt it later.

### Attestation process

1. Local attestation: an enclave proves its identity to another enclave on the same platform.
2. Remote attestation: an enclave proves its identity to a remote party using quotes signed by the hardware.

A quote contains:
- A measurement (hash) of the enclave code.
- The platform TCB (Trusted Computing Base) version.
- Signatures from the hardware attestation key.

---

## TEE technologies compared

| Technology | Vendor | First ship | Target | Isolation Level |
|------------|--------|------------|--------|----------------|
| **Intel SGX** | Intel | 2015 (Skylake) | Consumer/Cloud | Process-level |
| **AMD SEV** | AMD | 2017 (Naples) | Cloud | VM-level (memory only) |
| **AMD SEV-ES** | AMD | 2019 (Rome) | Cloud | + Encrypted register state |
| **AMD SEV-SNP** | AMD | 2021 (Milan) | Cloud | + Integrity (RMP) + migration |
| **Intel TDX** | Intel | 2024 (Emerald Rapids GA; limited 4th-gen SKUs earlier) | Cloud | VM-level |
| **ARM CCA** | ARM | 2023 (Armv9 silicon shipping) | Cloud / mobile | Realm |
| **ARM TrustZone** | ARM | 2009+ | Mobile | Secure world (legacy TEE) |
| **NVIDIA H100 CC** | NVIDIA | 2023 (preview) → 2024 (GA, CUDA 12.4 / r550) | GPU | GPU TEE |

---

## Major implementations

### Intel SGX

- Process-level TEE. SGX1 since 2015 Skylake, SGX2 (DCAP / EDMM) on server-class chips. Client-class SGX was deprecated starting with 11th-gen consumer CPUs in 2021; it lives on in Xeon SP for confidential workloads.
- Pros: smallest TCB of the production TEEs, mature attestation tooling, per-process isolation.
- Cons: a long catalog of side-channel breaks (Foreshadow / L1TF, ÆPIC Leak, ZenBleed-class issues). Treat it as legacy for new VM-scale workloads; prefer TDX.
- Cloud support: Azure DCsv2/DCsv3 (GA), Alibaba Cloud ECS ebmre6p, IBM Cloud (legacy). GCP and AWS never shipped public SGX SKUs.
- Libraries: [Occlum](https://github.com/occlum/occlum), [Gramine](https://github.com/gramineproject/gramine).

### AMD SEV-SNP

- VM-level TEE with stronger guarantees than SEV/SEV-ES (integrity and replay protection via the SP RMP).
- Pros: mature, broad cloud availability, live migration support, no class of side-channel breaks comparable to SGX's enclave hijacks (CacheWarp and Hertzbleed aside).
- Cons: you still trust AMD's PSP; firmware updates rotate the TCB.
- Cloud support: Azure DCasv5/ECasv5, GCP Confidential VMs (N2D, C3D), AWS M7a/C7a/R7a (since 2023), OCI E5.
- Note: AWS Nitro Enclaves are a separate Nitro-hypervisor isolation primitive, not a CPU TEE in the SEV/TDX sense, and cannot do remote attestation against an AMD/Intel root.
- Reference: [AMD SEV-SNP Overview](https://www.amd.com/system/files/TechDocs/SEV-SNP-strengthening-vm-isolation-with-integrity-protection-and-more.pdf).

### Intel TDX

- Virtualization-based TEE. VM-level confidential computing, complementary to SGX rather than replacing it.
- Pros: VM-level isolation with a smaller per-tenant TCB than SGX, supports unmodified guest OS.
- Cons: newer; speculative-execution issues are still being found (for example TDXDown 2024).
- Cloud support: Azure DCesv5/ECesv5, GCP Confidential VMs (C3), Alibaba g8i.

### Confidential Containers (CoCo)

- Cloud-native framework for running containers in TEEs.
- Key projects:
  - [Confidential Containers](https://github.com/confidential-containers/): Kubernetes operator.
  - [Kata Containers](https://katacontainers.io/): VM-based containers.
  - [Marblerun](https://github.com/edgelesssys/marblerun): CoCo orchestrator.

### Confidential AI

- [Gramine](https://github.com/gramineproject/gramine): library OS for running unmodified apps in enclaves.
- [Enclaive](https://github.com/enclaive): framework for building confidential apps.
- [Phala Network](https://github.com/Phala-Network/phala-cloud): decentralized confidential cloud.

---

## Use cases

### 1. Private inference

Run ML inference on encrypted inputs. The model never sees the raw data.

Example: [Blyss Blog: Confidential AI](https://blog.blyss.dev/confidential-ai-from-gpu-enclaves).

### 2. Multi-party data analysis

Multiple parties contribute data to a joint computation without revealing their inputs to each other.

### 3. Blockchain oracles

Attested computation for smart contracts. The oracle runs in a TEE and the result is cryptographically attested.

### 4. Key management

Private keys never leave the hardware. Signing happens inside the enclave.

### 5. Confidential databases

Query encrypted databases without decrypting the data, using enclaves combined with FHE or secure enclaves.

---

## Evidence at a glance

| Use Case | Maturity | Evidence |
|----------|----------|----------|
| Cloud Confidential VMs | Production | Azure, AWS, GCP all offer |
| CoCo | Beta | Active CNCF project |
| Confidential AI | Emerging | Research + startups |
| Multi-party Mpc | Research | Academic papers |

---

## Trade-offs

### Strengths

- Hardware-backed: stronger than software-only isolation.
- Performance: near-native, unlike FHE which is roughly 10,000x slower.
- Compatibility: existing code can run with minimal modification.
- Verified boot chain rooted in hardware.

### Limitations

- Side-channel risk: SGX in particular has had multiple side-channel vulnerabilities.
- Vendor trust: you trust Intel, AMD, or NVIDIA.
- Key escrow risk: the vendor may have recovery keys.
- Limited secure memory: SGX enclaves have a limited Enclave Page Cache (EPC).
- Attestation complexity: setting up remote attestation is not trivial.

---

## Attack surface

### Physical attacks

- Microprobing (hard, lab equipment required).
- Fault injection (voltage glitching).
- EM emissions analysis.

### Side-channel attacks

- Cache timing attacks.
- Speculative execution (Spectre variants).
- Page fault attacks.

### Software attacks

- OS or kernel compromise.
- Hypervisor escape.
- Supply chain attacks.

### Mitigation

- Use the latest TEE generation (SEV-SNP > TDX > SGX).
- Keep TCB updated.
- Combine multiple TEE generations for defense in depth.

---

## Related Files

- [TEE-Technologies-Deep-Dive](/confidential-computing/tee-technologies-deep-dive)
- [Confidential-Containers](/confidential-computing/confidential-containers)
- [Cloud-Provider-Comparison](/confidential-computing/cloud-provider-comparison)
- [Attestation-Architecture](/confidential-computing/attestation-architecture)
- [TEE-Side-Channel-Attacks](/confidential-computing/tee-side-channel-attacks)
- [Confidential-AI-Inference](/confidential-computing/confidential-ai-inference)
- [Private-LLM-Inference-Patterns](/confidential-computing/private-llm-inference-patterns)
- [Overview - Fully Homomorphic Encryption](/cryptography/overview-fully-homomorphic-encryption) — Combines with FHE for stronger guarantees

