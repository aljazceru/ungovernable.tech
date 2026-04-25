---
title: "01 — Confidential Computing"
tags:
  - "confidential-computing"
  - "tee"
  - "sgx"
  - "sev-snp"
  - "tdx"
  - "confidential-inference"
---
Trusted Execution Environments (TEEs), hardware security enclaves, GPU confidential computing, attestation, and confidential AI inference. The foundation of protecting data *during* computation — not just at rest or in transit.

---

## Start Here

- [Overview - Confidential Computing](/confidential-computing/overview-confidential-computing) — the big picture: what, why, how, at what cost.

## Core Technology

- [TEE-Technologies-Deep-Dive](/confidential-computing/tee-technologies-deep-dive) — SGX, SEV-SNP, TDX, Arm CCA — architectural detail.
- [NVIDIA-GPU-TEE](/confidential-computing/nvidia-gpu-tee) — Hopper / H100 / H200 / Blackwell confidential computing, encrypted PCIe.
- [Attestation-Architecture](/confidential-computing/attestation-architecture) — RATS model, DCAP, SEV-SNP reports, TDX quotes, verifiers, KMS-gating.
- [TEE-Side-Channel-Attacks](/confidential-computing/tee-side-channel-attacks) — catalog of breaks (SGAxe, Foreshadow, CacheWarp, Hertzbleed…) and mitigations.

## Infrastructure & Deployment

- [Confidential-Containers](/confidential-computing/confidential-containers) — CoCo, Kata, Trustee, KBS, peer-pods, Kubernetes integration.
- [Cloud-Provider-Comparison](/confidential-computing/cloud-provider-comparison) — Azure, AWS, GCP, Oracle, IBM, decentralized operators.

## Confidential AI / Inference (focus area)

- [Confidential-AI-Inference](/confidential-computing/confidential-ai-inference) — threat model, architectural patterns, production systems (Apple PCC, Tinfoil, Phala, Oasis…), inference-specific leaks.
- [Private-LLM-Inference-Patterns](/confidential-computing/private-llm-inference-patterns) — concrete recipes: attested-TLS, KMS-gated weights, transparency-logged builds, no-persistence enclaves, confidential RAG, attested tool use.

## Planned / Stub

*Files below are not yet written. Tracked in [CHANGELOG](/meta/changelog).*

- Multi-Party Computation — joint computation with no trusted party.
- Key Management — hardware-backed keys, HSMs vs. TEEs.

---

## Technology Map

```
Confidential Computing
├── CPU TEEs
│   ├── Intel SGX (process-level)
│   ├── Intel TDX (VM-level)
│   ├── AMD SEV / SEV-ES / SEV-SNP (VM-level)
│   ├── Arm CCA (Realm)
│   └── IBM Z Secure Execution (s390x)
├── Accelerator TEEs
│   ├── NVIDIA H100 / H200 / Blackwell CC
│   ├── (Roadmap) AMD Instinct CC
│   └── (Roadmap) AWS Trainium CC
├── Attestation
│   ├── Intel DCAP / PCS / Tiber
│   ├── AMD KDS (VCEK / VLEK)
│   ├── NVIDIA NRAS
│   ├── Azure MAA, AWS KMS, GCP Confidential Space
│   └── Open: Veraison, on-chain (Oasis, Phala)
├── Orchestration
│   ├── Confidential Containers (CoCo) + Trustee
│   ├── Kata Containers
│   ├── Gramine / Occlum (library OS, SGX)
│   ├── Edgeless Constellation / MarbleRun
│   └── Anjuna, Fortanix, Enclaive
└── Confidential AI
    ├── Apple Private Cloud Compute
    ├── Tinfoil, Phala, Marlin, Oasis ROFL
    └── Microsoft Confidential Inferencing
```

---

## Status Snapshot (early 2026)

| Technology | Status | Notes |
|------------|--------|-------|
| Intel SGX | Production, legacy | New workloads should prefer TDX |
| AMD SEV-SNP | Production | Broad cloud availability; watch microcode |
| Intel TDX | Production | Azure, GCP, Alibaba GA |
| Arm CCA | Early | Silicon shipping, software stack maturing |
| NVIDIA H100/H200 CC | Production | Azure, GCP, OCI GA; AWS roadmap |
| Blackwell CC | Rolling out | Encrypted NVLink is the big upgrade |
| Confidential Containers | GA/Beta | CoCo 0.x → 1.x; Trustee stable |
| Apple PCC | Production | Consumer; closed but transparency-logged |

---

## Quick Reference

| Use case | Recommended stack |
|---|---|
| Confidential LLM inference, open weights | TDX/SNP + H100 CC + attested TLS + transparency log |
| Enterprise regulated workload | Constellation / Anjuna / Fortanix on Azure or GCP |
| Multi-party compute | GCP Confidential Space or SNP + MPC library |
| Blockchain oracle | Oasis Sapphire, Phala, or Secret Network |
| Confidential K8s at scale | GCP Confidential GKE or Azure AKS + CoCo |
| Absolute minimum trust | On-device inference — no TEE needed |

