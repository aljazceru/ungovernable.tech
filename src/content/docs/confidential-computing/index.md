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
## Overview

**Confidential Computing** — powered by Trusted Execution Environments (TEEs) — enables a fundamental shift: data remains encrypted not just at rest and in transit, but **during computation**. Traditional encryption protects data at rest (full-disk encryption) and in transit (TLS), but leaves data exposed in memory where it's processed. TEEs solve this by creating isolated enclaves within the CPU that even the operating system, hypervisor, and cloud provider cannot access.

The primary use cases include:
- **Privacy-preserving cloud AI** — running inference on encrypted model inputs
- **Multi-party computation** — parties can contribute data without seeing each other's inputs
- **Blockchain oracles** — attested off-chain computation for smart contracts
- **Securing keys** — private keys never leave the hardware enclave

---

## Historical Context

### Early Enclaves (2006-2015)

The concept of hardware-backed security enclaves began with:
- **Intel SGX (Software Guard Extensions)** — introduced in 2015 with Skylake processors, allowed applications to create secure enclaves within user space
- **ARM TrustZone** — earlier TEE technology focused on mobile devices

### Cloud Confidential Computing (2017-Present)

The cloud providers began offering enclave services:
- **AWS Nitro Enclaves** (2019) — Nitro-based isolated environments
- **Azure Confidential Computing** (2017) — SGX-based VMs
- **GCP Confidential VMs** (2020) — AMD SEV-based VMs

### Modern Era (2020-Present)

- **AMD SEV-SNP** (2020) — Secure Nested Paging for stronger isolation
- **Intel TDX** (2022) — Trust Domain Extensions for virtualization
- **NVIDIA Confidential Computing** (2023) — GPU enclaves
- **Cloud Native Confidential Computing (CoCo)** — Kubernetes integration

---

## How TEEs Work

### The Trust Model

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

Key properties:
- **Isolation** — Enclave memory is encrypted and isolated from all other software
- **Attestation** — Remote parties can verify the enclave's identity and code hash
- **Sealing** — Data can be sealed (encrypted) so only the same enclave can decrypt it

### Attestation Process

1. **Local Attestation** — Enclave proves its identity to another enclave on the same platform
2. **Remote Attestation** — Enclave proves its identity to a remote party via quotes signed by the hardware

The quote contains:
- Measurement (hash) of the enclave code
- Platform TCB (Trusted Computing Base) version
- Signatures from the hardware attestation key

---

## TEE Technologies Comparison

| Technology | Vendor | Launch Year | Target | Isolation Level |
|------------|--------|-------------|--------|----------------|
| **Intel SGX** | Intel | 2015 | Consumer/Cloud | Process-level |
| **AMD SEV-ES** | AMD | 2017 | Cloud | VM-level |
| **AMD SEV-SNP** | AMD | 2020 | Cloud | VM-level + migration |
| **Intel TDX** | Intel | 2022 | Cloud | VM-level |
| **ARM TrustZone** | ARM | 2009+ | Mobile | Secure world |
| **NVIDIA CC** | NVIDIA | 2023 | GPU | GPU enclaves |

---

## Major Implementations

### Intel SGX

- **Overview**: Most mature TEE, available in consumer CPUs and cloud
- **Pros**: Well-documented, multiple cloud providers support
- **Cons**: Vulnerable to side-channel attacks (Spectre, L1TF)
- **Cloud Support**: Azure DCsv2, GCP C2D, Alibaba ECS
- **Libraries**: [Occlum](https://github.com/occlum/occlum), [Graminer](https://github.com/gramineproject/gramine)

### AMD SEV-SNP

- **Overview**: VM-level TEE; stronger guarantees than SEV/SEV-ES (integrity + replay protection via the SP RMP)
- **Pros**: Mature, broad cloud availability, live migration support, no class of side-channel breaks comparable to SGX's enclave hijacks (CacheWarp and Hertzbleed notwithstanding)
- **Cons**: You still trust AMD's PSP; firmware updates rotate the TCB
- **Cloud Support**: Azure DCasv5/ECasv5, GCP Confidential VMs (N2D, C3D), AWS M7a/C7a/R7a (since 2023), OCI E5
- **Note**: AWS *Nitro Enclaves* are a separate Nitro-hypervisor isolation primitive — not a CPU TEE in the SEV/TDX sense, and cannot do remote attestation against an AMD/Intel root.
- **Reference**: [AMD SEV-SNP Overview](https://www.amd.com/system/files/TechDocs/SEV-SNP-strengthening-vm-isolation-with-integrity-protection-and-more.pdf)

### Intel TDX

- **Overview**: Virtualization-based TEE — VM-level confidential computing, complementary to (not replacing) SGX
- **Pros**: VM-level isolation with smaller per-tenant TCB than SGX, supports unmodified guest OS
- **Cons**: Newer; class of speculative-execution issues being discovered (e.g., TDXDown 2024)
- **Cloud Support**: Azure DCesv5/ECesv5, GCP Confidential VMs (C3), Alibaba g8i

### Confidential Containers (CoCo)

- **Overview**: Cloud-native framework for running containers in TEEs
- **Key Projects**:
  - [Confidential Containers](https://github.com/confidential-containers/) — Kubernetes operator
  - [Kata Containers](https://katacontainers.io/) — VM-based containers
  - [Marblerun](https://github.com/edgelesssys/marblerun) — CoCo orchestrator

### Confidential AI

- [Gramine](https://github.com/gramineproject/gramine) — Library OS for running unmodified apps in enclaves
- [Enclaive](https://github.com/enclaive) — Framework for building confidential apps
- [Phala Network](https://github.com/Phala-Network/phala-cloud) — Decentralized confidential cloud

---

## Use Cases

### 1. Private Inference

Run ML inference on encrypted inputs — the model never sees the raw data.

Example: [ Blyss Blog: Confidential AI](https://blog.blyss.dev/confidential-ai-from-gpu-enclaves)

### 2. Multi-Party Data Analysis

Multiple parties can contribute data to a joint computation without revealing their inputs to each other.

### 3. Blockchain Oracles

Attested computation for smart contracts — the oracle runs in a TEE and the result is cryptographically attested.

### 4. Key Management

Private keys never leave the hardware — signing operations happen inside the enclave.

### 5. Confidential Databases

Query encrypted databases without decrypting the data — uses enclaves combined with FHE or secure enclaves.

---

## Evidence at a Glance

| Use Case | Maturity | Evidence |
|----------|----------|----------|
| Cloud Confidential VMs | Production | Azure, AWS, GCP all offer |
| CoCo | Beta | Active CNCF project |
| Confidential AI | Emerging | Research + startups |
| Multi-party Mpc | Research | Academic papers |

---

## Trade-offs

### Strengths

- **Hardware-backed security** — Stronger than software-only solutions
- **Performance** — Near-native speed (unlike FHE which is 10,000x slower)
- **Compatibility** — Can run existing code with minimal modification
- **Verified boot chain** — From hardware root of trust

### Limitations

- **Side-channel risks** — SGX has had multiple side-channel vulnerabilities
- **Trust in CPU vendor** — You're trusting Intel/AMD/NVIDIA
- **Key escrow risk** — Vendor might have recovery keys
- **Limited secure memory** — SGX enclaves have limited EPC (Enclave Page Cache)
- **Attestation complexity** — Setting up remote attestation is non-trivial

---

## Attack Surface

### Physical Attacks

- Microprobing (hard, requires lab equipment)
- Fault injection (voltage glitching)
- EM emissions analysis

### Side-Channel Attacks

- Cache timing attacks
- Speculative execution (Spectre variants)
- Page fault attacks

### Software Attacks

- OS/kernel compromise
- Hypervisor escape
- Supply chain attacks

### Mitigation

- Use latest TEE generation (SEV-SNP > TDX > SGX)
- Keep TCB updated
- Use multiple TEE generations together (defense in depth)

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
