---
title: "Confidential Computing Cloud Provider Comparison"
tags:
  - "cloud"
  - "azure"
  - "aws"
  - "gcp"
  - "oracle"
  - "confidential-computing"
  - "comparison"
---
*Which cloud does what, with which silicon, and what you actually get when the marketing page says "confidential."*

State: early 2026. This space moves quarterly — verify before committing.

---

## Capability Matrix

| Capability | Azure | AWS | GCP | Oracle OCI | IBM Cloud | Alibaba |
|---|---|---|---|---|---|---|
| **Intel SGX (app enclaves)** | DCsv3 (GA) | — (deprecated in cloud) | — | — | — | ECS ebmre6p (GA) |
| **Intel TDX (CVM)** | DCesv5 (GA) | Roadmap | C3 / C3D (GA) | — | LinuxONE-adjacent only | ECS g8i (GA) |
| **AMD SEV-SNP (CVM)** | DCasv5/DCadsv5 (GA) | M6a/M7a/C7a with Nitro+SNP (GA, evolving) | C3D (GA) | E5/E6 (GA) | Hyper Protect (GA) | ECS g7a (GA) |
| **NVIDIA H100 CC** | NCC H100 v5 (GA) | — (roadmap) | A3 Confidential (GA) | BM.GPU.H100.CC (GA) | — | — |
| **Nitro Enclaves (non-DRAM-encrypted VM isolation)** | — | GA (all Nitro instances) | — | — | — | — |
| **Attestation service** | Microsoft Azure Attestation (MAA) | KMS attestation conditions + Nitro attestation | Confidential Space attestation | OCI attestation (beta) | HPVS attestation | Alibaba-specific |
| **Key release service** | Azure Key Vault Secure Key Release | AWS KMS with attestation conditions | GCP KMS + Confidential Space | OCI Vault | HPCS | KMS |
| **Confidential Containers / CoCo support** | AKS CoCo preview | EKS via peer-pods (community) | GKE Confidential GKE Nodes (SNP) | OKE (community) | IBM HPVS | ACK |
| **Confidential GKE / AKS at scale** | AKS Confidential | EKS (partial) | GKE Confidential Nodes GA | OKE CC | — | ACK |

---

## Provider-Specific Notes

### Microsoft Azure

- Broadest SKU catalog; the only public cloud with both **SGX** and **TDX** and **SEV-SNP** and **H100 CC** simultaneously.
- **Azure Attestation (MAA)** is mature, multi-platform, and returns a JWT a relying party can verify.
- **Secure Key Release (SKR)** in Key Vault with Managed HSM — strongest KMS-gating story among majors.
- Confidential AKS integrates CoCo and Kata.
- **Caveat:** MAA is an Azure-operated verifier — for strongest assurance, verify raw quotes against Intel/AMD directly, not via MAA alone.

### AWS

- **Nitro Enclaves** are AWS's in-house solution: isolated mini-VMs carved out of a parent EC2 instance, with signed attestation documents. **Not** encrypted DRAM — the isolation is hypervisor+silicon-level via Nitro, not memory encryption. For many threat models this is sufficient because the Nitro hypervisor is smaller and more trusted than a general-purpose hypervisor, but it's a different model than SGX/TDX/SEV-SNP.
- **SEV-SNP** support rolled out on M6a/M7a/C7a generations with deep Nitro integration (VLEK signing).
- **KMS + Nitro attestation conditions** is the cleanest KMS-gated-key pattern in the industry — a single IAM policy clause can enforce "only release key to enclave with PCR0=X".
- **No GA H100 CC yet.** Watch Trainium/Inferentia; AWS is building in-house confidential accelerators.

### Google Cloud

- Pioneered public-cloud SEV-based Confidential VMs (2020).
- **Confidential Space** — a serverless-style product that packages a hardened Confidential VM, attestation, and workload identity federation to GCP APIs; good default for multi-party computation and attested workloads.
- **GKE Confidential Nodes** — SNP nodes at scale; TDX in preview.
- **A3 Confidential** is the main offering for confidential LLM inference with H100 CC.

### Oracle OCI

- Fewer SKUs, but aggressive on **H100 CC bare-metal** — notable because you own the whole node (no co-tenant side channels).
- OCI Vault + attestation is less mature than Azure/AWS; you'll do more plumbing.

### IBM Cloud

- **Hyper Protect Virtual Servers** use IBM Z Secure Execution (s390x) — a different TEE lineage from x86, with strong pedigree for regulated finance/health.
- Not relevant to NVIDIA GPU confidential inference today.

### Alibaba / Tencent / Huawei

- Alibaba ECS has SGX, TDX, and SNP offerings; attestation collateral flows through Alibaba's own services. Relevant for APAC deployments; audit the trust chain carefully — the operator's verifier is *also* the cloud operator.

### Decentralized / Specialist Operators

- **Phala, Marlin, Oasis, Secret Network, Fluence** — TEE marketplaces where nodes are community-operated, attestation is verified on-chain, and payment is usually crypto.
- **CoreWeave, Lambda, Crusoe, TensorWave** — GPU-specialist clouds; H100/H200 CC availability varies, often requires bring-your-own orchestration.
- **Tinfoil, Edgeless, Anjuna, Fortanix** — layer atop the majors with hardened images + attestation UX.

---

## Choosing a Provider

| You care about… | Go with |
|---|---|
| Fastest path to confidential LLM inference | Azure NCC H100 v5 or GCP A3 Confidential |
| Strongest KMS-gating UX | AWS KMS + Nitro Enclaves / SNP |
| Confidential Kubernetes at scale | GCP Confidential GKE or Azure Confidential AKS |
| Bare-metal, no co-tenancy | Oracle OCI or CoreWeave |
| Regulated finance/healthcare (EU/US) | Azure Confidential + Fortanix, or IBM HPVS |
| Minimum trust in cloud operator | Decentralized TEE marketplace (Phala, Marlin) + third-party verifier |
| Open-weights LLM for end users | Tinfoil, Phala, or self-host on Azure/GCP with an open verifier |

---

## The Trust-Is-Not-Free Small Print

Every cloud provider controls:
- The **BIOS / bootloader** you cannot audit remotely (though measured and attested).
- The **attestation service endpoints** (unless you bring-your-own verifier).
- **Key management infrastructure** (unless you use split-key / external KMS).
- **Network routing and egress logging** — TEEs don't hide traffic metadata.
- **Supply-chain access** to silicon — a cloud can, in principle, receive silicon the vendor isn't shipping elsewhere.

Confidential computing reduces the cloud's plaintext-access surface dramatically; it does not eliminate the cloud from your threat model. Pair with transparency logs, multi-vendor quorum, or on-chain verification if you need to actually minimize cloud trust.

---

## Related Files

- [Overview - Confidential Computing](/confidential-computing)
- [TEE-Technologies-Deep-Dive](/confidential-computing/tee-technologies-deep-dive)
- [Attestation-Architecture](/confidential-computing/attestation-architecture)
- [NVIDIA-GPU-TEE](/confidential-computing/nvidia-gpu-tee)
- [Confidential-Containers](/confidential-computing/confidential-containers)

