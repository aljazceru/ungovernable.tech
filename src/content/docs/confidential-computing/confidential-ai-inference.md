---
title: "Confidential AI Inference"
tags:
  - "confidential-computing"
  - "confidential-ai"
  - "confidential-inference"
  - "tee"
  - "gpu-tee"
  - "llm"
  - "privacy"
---
*Running machine learning inference where neither the model owner sees the inputs, nor the user sees the weights — and both can cryptographically verify the promise.*

---

## The Problem

Modern AI inference forces a three-way trust failure:

1. **User → Provider:** Users hand raw prompts, images, documents, medical records, or code to a remote GPU they don't control. The provider (and anyone with subpoena/coercion power over it) sees everything.
2. **Provider → User:** Providers must ship model weights to any host that runs the workload. Weights are stolen, leaked, or exfiltrated by customers, insiders, or compromised hypervisors.
3. **Both → Infrastructure:** Cloud operators, hypervisors, orchestration layers, and supply chains sit between user and model and can silently swap models, log prompts, or tamper with outputs.

Confidential inference closes all three gaps by running the model inside a **Trusted Execution Environment** whose identity — code hash, firmware version, GPU identity — is cryptographically attested to the counterparty *before* any prompt or weight is sent.

---

## The Ideal Trust Property

A fully confidential inference service satisfies, for every request:

| Property | Meaning |
|---|---|
| **Input secrecy** | Prompt / image / audio plaintext exists only inside the TEE |
| **Output secrecy** | Response is encrypted to the client inside the TEE |
| **Weight secrecy** | Model weights are either sealed to the TEE identity or decrypted only inside it |
| **Code integrity** | The exact binary serving the request is measured and published |
| **Binding** | The session key is bound to the attestation so MITM is impossible |
| **Non-retention** | No logs, no KV-cache persistence, no side-channel telemetry leaves the enclave |
| **Auditability** | A third party can later prove what code was running, without needing the provider's cooperation |

No production system hits 7/7 yet. The state of the art (Apple PCC, NVIDIA H100 CC + attestation, Tinfoil, Phala, Oasis, Marlin) hits 4–6 depending on threat model.

---

## Architectural Patterns

### 1. Single-TEE CPU Inference (small models)

Entire model runs inside an Intel TDX / AMD SEV-SNP confidential VM. No GPU.

- **Fits:** models <20B parameters that tolerate CPU latency, or fine-tuned small transformers (embeddings, classifiers, tool-call routers).
- **Providers:** Azure DCasv5 (TDX), GCP C3 (TDX), AWS M7a (SEV-SNP).
- **Example stacks:** Gramine + llama.cpp, Enarx, Occlum, MSFT Confidential Inferencing Containers.
- **Limitation:** no matrix-multiply accelerator — 50–200× slower than a GPU for large models.

### 2. CPU-TEE ↔ GPU-TEE (the modern pattern)

Confidential VM (TDX/SEV-SNP) pairs with a confidential GPU (NVIDIA H100 / H200 / Blackwell in CC mode). All PCIe traffic between them is AES-GCM encrypted; both endpoints attest jointly.

- **Fits:** frontier LLMs, diffusion, multimodal — anything GPU-bound.
- **Providers:** Azure NCC H100 v5, GCP A3 Confidential, Oracle OCI H100 CC, Coreweave/Lambda early access.
- **Key doc:** [NVIDIA-GPU-TEE](/confidential-computing/nvidia-gpu-tee).
- **Caveat:** ~5–15% throughput cost; first-token latency +30–120ms from attestation handshake.

### 3. Split / Federated Inference

Embedding layer runs in a CPU TEE near the user (or on-device); deep layers run on a remote GPU TEE; activations are encrypted between hops.

- **Pro:** limits blast radius if one enclave is broken.
- **Con:** activation-leakage attacks (reconstruction from hidden states) are an active research area — do not assume "activations ≈ noise."

### 4. Cryptographic Inference (FHE / MPC / ZKML)

Not TEE-based at all: homomorphic encryption, secure multi-party computation, or zero-knowledge ML circuits.

- **FHE (Zama Concrete-ML, OpenFHE):** input privacy, weight privacy — but ~10³–10⁶× overhead, only viable for tiny models today.
- **MPC (CrypTen, MP-SPDZ):** 2–3 non-colluding parties, interactive — good for specific enterprise joint-compute deals.
- **ZKML (EZKL, Giza, RISC Zero + onnx):** proves *output* was computed correctly from a committed model, not input privacy by itself. Pair with TEE for full story.

### 5. On-Device Inference

Run the model on the user's own hardware — Apple Neural Engine, Qualcomm Hexagon, local llama.cpp on M-series / 5090. No confidentiality problem because the user *is* the trusted party.

- **Gold standard for privacy** when model can fit. Always ask "can this run locally?" before reaching for a TEE.
- See [Overview - Confidential Computing](/confidential-computing) §Use Cases.

---

## Production & Near-Production Systems

### Apple Private Cloud Compute (PCC) — 2024–

The most ambitious consumer deployment. An iPhone can offload an Apple-Intelligence request to PCC servers where:

- Custom Apple Silicon server nodes run a hardened variant of iOS/Darwin with Secure Enclave + Secure Boot + sealed memory.
- Every build image is reproducibly hashed and published to a **transparency log**; clients refuse to send prompts to any node whose image hash isn't in the log.
- No persistent storage, no admin interface, no remote shell. Logging is structurally impossible, not merely policy-disabled.
- End-to-end encrypted session keyed to attestation.

**Why it matters:** first mass-market system where "the server operator genuinely cannot see your prompt" is a deployed guarantee, not marketing. Threat model writeup: `security.apple.com/blog/private-cloud-compute`.

**What it's not:** open. Only Apple builds on Apple silicon can join. No third-party audit of running instances — you trust the transparency log and Apple's signing keys.

### NVIDIA H100 / H200 / Blackwell Confidential Computing

NVIDIA's Hopper (and Blackwell) GPUs ship a hardware root of trust, encrypted PCIe (SPDM + AES-GCM), and attestable firmware. Paired with a TDX or SEV-SNP host, they form the only production GPU-TEE today. See [NVIDIA-GPU-TEE](/confidential-computing/nvidia-gpu-tee) for the full mechanism.

### Tinfoil (tinfoil.sh)

- CPU-TEE (SEV-SNP / TDX) + NVIDIA CC GPU hosting of open-weights LLMs (Llama 3.x, DeepSeek, Mistral).
- Clients verify attestation in-browser before any prompt is transmitted.
- Reproducible container builds published to Sigstore; the attestation quote commits to the exact image digest.
- Threat model: trusted = NVIDIA + AMD/Intel silicon + Tinfoil's build pipeline (transparency-logged). Untrusted = Tinfoil operators, cloud, ISPs.

### Phala Cloud / Phala Network

- Decentralized TEE marketplace (Intel SGX → TDX, with NVIDIA CC support).
- Workloads run on-chain-registered worker nodes; attestation quotes are verified by the blockchain before a job is considered valid.
- `dstack` SDK packages docker-compose workloads into TDX CVMs with deterministic attestation.

### Oasis (Sapphire / ROFL)

- Confidential EVM (Sapphire) runs smart-contract state in SGX.
- ROFL (Runtime Off-chain Logic) runs larger compute — including LLM inference — in TDX with on-chain attestation receipts.
- Good fit when you want "confidential inference as a verifiable oracle."

### Marlin (Oyster)

- CVM marketplace (AWS Nitro Enclaves + NVIDIA CC).
- Focus: serverless confidential functions; pay-per-second; attestation returned with every response.

### Edgeless Systems (Contrast, Constellation, MarbleRun)

- Enterprise Kubernetes + CoCo stack; attestation-gated secret injection into confidential pods.
- Constellation: always-encrypted K8s cluster on SEV-SNP / TDX.
- Used for private inference in regulated industries (health, finance).

### Secret Network / Fortanix / Anjuna

- Secret Network: SGX-backed confidential smart contracts, some ML-oracle experiments.
- Fortanix Confidential Computing Manager: enterprise TEE orchestration, SGX/TDX.
- Anjuna: "lift and shift" confidential VM wrapper — no code changes; auto-enables SEV-SNP/TDX + attestation gating on AWS/Azure/GCP.

---

## Attack Surface Specific to Inference

Even a perfect TEE doesn't give you a perfect confidential-inference system. Model-specific and workflow-specific leaks:

### Prompt / Activation Leakage

- **Timing side channels:** decode latency varies with token choice, KV-cache state, speculative decoding hit/miss. An observer of *response timing alone* can sometimes reconstruct which tokens were generated. Mitigations: constant-time decoding (rare), padded batches, fixed max_tokens, jittered emission.
- **Memory access patterns:** even inside an enclave, DRAM traffic is visible to the memory controller. Sparse-MoE routing has been shown to leak the active expert → the token class. Dense models are safer; MoE in TEE is an open problem.
- **Speculative decoding across tenants:** shared draft models leak cross-request information. Don't share drafts across confidentiality domains.

### Output Channels

- **Model memorization:** a confidential model may still regurgitate training-data secrets. TEEs protect *this request's* data, not the corpus the model memorized.
- **Logit leakage via streaming:** per-token streaming + timing = more side-channel surface than batched completion. Prefer batched for high-sensitivity use.
- **Tool-use side effects:** the moment the model makes an external HTTP call the enclave guarantee ends. Keep tool execution inside a second enclave or accept the leak.

### Weight Exfiltration

- **Attester-less weight delivery is a bug.** Weights must be encrypted to the enclave measurement, not to a long-lived account key the operator holds.
- **Page-swap & cold-boot:** older SGX could be coerced into paging EPC; SEV-SNP / TDX mitigate but not eliminate. Disable hibernation on confidential hosts.
- **Model stealing via queries:** unrelated to TEEs — if the API is public, adversaries can distill weights through query volume. Rate-limit and watermark.

### Attestation-Pipeline Attacks

- **Stale TCB:** an attestation can be valid *and* vulnerable. Always require a minimum TCB level and reject SEV-SNP microcode below the latest CVE-fixed version.
- **Collateral DoS:** Intel/AMD attestation services can be unavailable. Cache TCB info and verifier collateral locally; support offline verification.
- **Rogue signer:** a compromised CPU signing key ends the model. Multi-vendor deployments (TDX *and* SEV-SNP nodes with quorum) reduce systemic risk — see [Attestation-Architecture](/confidential-computing/attestation-architecture).

### Supply Chain

- **Build reproducibility:** if you can't rebuild the enclave image bit-for-bit, your attestation quote means "Trust the build server," not "Trust the code." Use SLSA L3+, sigstore, and transparency-logged image hashes.
- **Dependency creep:** every added Python package expands MRENCLAVE and shrinks auditability. Minimal runtimes (musl + static llama.cpp) beat full PyTorch stacks for high-assurance contexts.

---

## Threat Model Checklist (use before deploying)

1. **Who is in your TCB?** List every party: silicon vendor, firmware signer, BIOS, hypervisor vendor, image builder, transparency-log operator, key-release service. Anyone on that list can break you.
2. **Where does the plaintext prompt first appear?** Client TLS → TEE public key? Verify the TLS endpoint is *inside* the enclave, not a front-end proxy.
3. **How is the model key released?** KMS → enclave via attested channel? Or baked into the image (rotation nightmare)?
4. **What does "no logging" mean?** Structural (no disk, no syslog compiled in) or policy (config flag)? Only structural counts.
5. **Freshness?** Does the attestation quote include a client-supplied nonce? Otherwise replay is trivial.
6. **Revocation?** If a CVE drops today, how do you turn off every vulnerable TCB *right now*? Pre-wire the kill switch.
7. **What does the user verify?** A one-line "this is secure" UI is theater. Give them the image hash + a way to check it against the transparency log, even if 99% ignore it.

---

## Decision Matrix

| Requirement | Pick |
|---|---|
| Consumer, Apple-ecosystem only | Apple PCC (transparent, but closed) |
| Open-weights LLM, lowest friction | Tinfoil / Phala |
| Enterprise K8s, regulated data | Edgeless Constellation, Anjuna, Fortanix |
| Verifiable inference for smart contracts | Oasis ROFL, Marlin Oyster, Phala |
| Input *and* weight privacy, no hardware trust | FHE (small models only) |
| Output-correctness proof only | ZKML (no input privacy by itself) |
| Maximum privacy, small model | On-device — don't use a TEE at all |

---

## Related Files

- [Overview - Confidential Computing](/confidential-computing)
- [TEE-Technologies-Deep-Dive](/confidential-computing/tee-technologies-deep-dive)
- [NVIDIA-GPU-TEE](/confidential-computing/nvidia-gpu-tee)
- [Attestation-Architecture](/confidential-computing/attestation-architecture)
- [Private-LLM-Inference-Patterns](/confidential-computing/private-llm-inference-patterns)
- [TEE-Side-Channel-Attacks](/confidential-computing/tee-side-channel-attacks)
- [Confidential-Containers](/confidential-computing/confidential-containers)
- [Overview - Fully Homomorphic Encryption](/cryptography/overview-fully-homomorphic-encryption)

## Primary Sources

- Apple: *Private Cloud Compute Security Guide* — `security.apple.com/documentation/private-cloud-compute`
- NVIDIA: *Confidential Computing on H100 GPUs* whitepaper (2023) — `docs.nvidia.com/confidential-computing`
- Confidential Computing Consortium: *Technical Analyses* — `confidentialcomputing.io/resources`
- Microsoft Azure: *Confidential inferencing with ONNX Runtime* — `learn.microsoft.com/azure/confidential-computing`
- Costan & Devadas: *Intel SGX Explained* — IACR ePrint 2016/086
- Li et al.: *A Survey of Secure Computation Using Trusted Execution Environments* — ACM CSUR 2023

