---
title: "NVIDIA GPU TEE (Hopper / Blackwell Confidential Computing)"
tags:
  - "gpu-tee"
  - "nvidia"
  - "h100"
  - "h200"
  - "blackwell"
  - "confidential-computing"
  - "confidential-ai"
---
*The only production GPU confidential-computing stack as of 2026. Everything "confidential LLM inference on frontier models" is built on it.*

---

## Why a GPU TEE Matters

CPU TEEs (SGX, TDX, SEV-SNP) solved "data in use" for CPU workloads. But modern inference and training are GPU-bound — if the prompt leaves the CPU enclave in plaintext across the PCIe bus to a non-confidential GPU, the whole chain is broken: a malicious hypervisor, a PCIe-snooping cloud operator, or a rogue firmware blob on the GPU can read every token.

NVIDIA Confidential Computing (first shipped on **H100 / Hopper, 2023**, expanded on **H200, 2024**, and **Blackwell B100/B200/GB200, 2024–2025**) extends the TEE boundary across the PCIe link and into the GPU itself.

---

## Architecture

```
┌─────────────────────────────────────────────┐
│           Confidential VM (TDX / SEV-SNP)   │
│  ┌───────────────────────────────────────┐  │
│  │  Guest OS + CUDA app (measured)       │  │
│  └───────────────────────────────────────┘  │
│             │  encrypted PCIe (SPDM/AES-GCM)│
│             ▼                               │
│  ┌───────────────────────────────────────┐  │
│  │   NVIDIA GPU in CC-On mode            │  │
│  │  ┌──────────────────────────────┐     │  │
│  │  │  GPU Secure Processor (GSP)  │     │  │
│  │  │  - Hardware root of trust    │     │  │
│  │  │  - Firmware measurement      │     │  │
│  │  │  - Attestation signing key   │     │  │
│  │  └──────────────────────────────┘     │  │
│  │  ┌──────────────────────────────┐     │  │
│  │  │  HBM (encrypted & integrity   │     │  │
│  │  │  protected via on-die engine)│     │  │
│  │  └──────────────────────────────┘     │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

### Components

| Component | Role |
|---|---|
| **GPU Secure Processor (GSP)** | On-die microcontroller; the GPU's root of trust. Measures firmware, holds the per-device ECDSA P-384 attestation key, produces quotes. |
| **Secure Boot** | GSP verifies signed firmware before CUDA is allowed to run; failure locks the GPU out of CC mode. |
| **Encrypted HBM** | HBM contents encrypted + integrity-protected by hardware engine at memory-controller layer (AES-256-GCM, per-GPU key). |
| **Encrypted PCIe** | SPDM 1.2 session between CPU TEE and GPU. Key exchange via ECDHE, bulk traffic AES-GCM. All CUDA H2D/D2H copies transparently encrypted. |
| **NVIDIA Remote Attestation Service (NRAS)** | Cloud service that verifies GSP-signed quotes and checks firmware versions against a known-good list; returns a JWT to the relying party. Local verification also supported. |
| **Confidential Compute Mode** | Boolean state on the GPU. Set by privileged firmware command; once on, non-CC code paths are disabled and attestation becomes required for use. |

### Modes

1. **CC-Off** — regular, non-confidential. Any mode switch wipes HBM.
2. **CC-On (protected PCIe)** — full TEE: encrypted PCIe, attested, HBM encrypted.
3. **CC-On (DevTools)** — looser mode for debugging; don't ship prod with this.
4. **Multi-GPU / NVLink CC (Blackwell)** — NVLink traffic between GPUs in the same confidential domain is also encrypted + attested; enables multi-GPU models (tensor/pipeline parallel) inside a single TEE trust domain. Hopper's NVLink is *not* encrypted — multi-GPU on H100 CC forces PCIe routing with heavy perf cost; this is a major Blackwell upgrade.

---

## The Attestation Flow (End to End)

1. **Client** opens TLS to relying service and requests attestation evidence before sending the prompt.
2. **CPU TEE** (TDX/SEV-SNP) generates its quote with a nonce supplied by the client, including the hash of the GPU attestation token it just received.
3. **GPU** produces its own quote (via GSP) over the same nonce + current firmware version + CC mode status, signed by the device-unique attestation key.
4. **Client** (or a verifier the client trusts) checks:
   - CPU quote against Intel PCS / AMD KDS collateral.
   - GPU quote against NVIDIA's device-certificate chain + NRAS revocation list.
   - Firmware version ≥ policy-defined minimum.
   - Measurement (MRTD for TDX; measurement of the OVMF + kernel + initrd + rootfs) matches the expected value for the published image.
5. **Client** derives a session key bound to both quotes; from this point the prompt is encrypted to the dual-attested TEE and no component in the cloud can decrypt it.

Replay is prevented by the client nonce; operator substitution is prevented because the GPU cert chain is rooted in NVIDIA's factory-provisioned keys — the cloud operator cannot forge a quote without a CVE-class break.

---

## Performance Cost

Rough numbers (H100 CC, 70B-class dense LLM inference, published & independently measured in 2024–2025):

| Phase | Overhead vs. non-CC |
|---|---|
| First-token latency (attestation + key exchange) | +30–120 ms once per session |
| Sustained token throughput | 5–15% lower |
| H2D / D2H copy-heavy workloads | up to 25% lower |
| Pure compute (matmul-dominated, data resident in HBM) | ~2–5% lower |

Rule of thumb: **for steady-state LLM serving, assume ~10% cost.** For training or workloads that thrash PCIe, the cost is higher and may be prohibitive until Blackwell's encrypted NVLink is the norm.

Blackwell improves this materially: encrypted NVLink, higher-throughput PCIe Gen5 crypto engines, and larger on-die attestation caches push steady-state overhead toward single digits even for multi-GPU MoE.

---

## What NVIDIA CC Does *Not* Protect Against

- **Side channels you bring yourself.** Timing leaks in your CUDA code, cache-based attacks across SMs for co-tenanted GPUs (not a concern if you own the whole GPU; MIG partitioning in CC mode is restricted).
- **Model extraction via the API.** TEE prevents *raw weight theft*; it does not prevent slow distillation via queries.
- **Driver compromise on the host.** The *host* NVIDIA driver is untrusted by design — that's the point. But a buggy *guest* driver inside your CVM can still leak. Keep the guest-side `nvidia-open` driver pinned and audited.
- **GSP firmware bugs.** CVEs in GSP firmware have dropped before (see 2023 advisories). Treat the GSP as part of your TCB and monitor NVIDIA security advisories the same way you track Intel/AMD microcode.
- **Covert channels via power / thermal.** Co-located TEE workloads can sometimes be distinguished by power draw observable to the cloud operator. Not a confidentiality break for plaintext, but a weak fingerprint channel.

---

## Clouds That Offer It

| Provider | SKU | CPU TEE | GPU | Notes |
|---|---|---|---|---|
| **Azure** | NCC H100 v5 | AMD SEV-SNP (Genoa) | H100 CC | GA; first major cloud with GPU CC |
| **GCP** | A3 Confidential | Intel TDX (Sapphire Rapids / EMR) | H100 CC | GA |
| **Oracle OCI** | BM.GPU.H100.CC | AMD SEV-SNP | H100 CC | GA |
| **AWS** | (none GA for H100 CC as of early 2026) | Nitro + SEV-SNP | H100/H200 non-CC | Nitro Enclaves *do* attest but don't extend to GPU; AWS roadmap signals Trainium/Blackwell CC future |
| **CoreWeave / Lambda / Crusoe** | Various H100/H200/B200 | TDX or SEV-SNP | CC optional | Early access / bring-your-own orchestration |
| **Phala / Marlin / Tinfoil** | Decentralized | TDX / SEV-SNP | H100 CC | On-chain-attested GPU marketplaces |

---

## Practical Deployment Checklist

1. **Enable CC mode** on the GPU (`nvidia-smi conf-compute -srs 1` — sticky across reboots; wipes HBM on transition).
2. **Pin GSP firmware** ≥ the minimum version that patches the latest advisory (track `nvidia.com/en-us/security/`).
3. **Use the NVIDIA Confidential Computing SDK / NVTrust** for attestation collection; don't roll your own quote parser.
4. **Verify both quotes**, not just the CPU one. Many early deployments verified the TDX quote and assumed the GPU was fine — it wasn't.
5. **Bind the attestation to your session.** The client nonce must appear in both quotes and in the TLS key-export.
6. **Reject CC-Off GPUs explicitly.** Default-closed: if the GPU quote says CC mode = off, drop the connection.
7. **Rotate on CVE.** When a GSP-firmware CVE drops, push a new minimum-firmware policy to your verifier. Old quotes become invalid automatically.
8. **Don't leak via logs.** The confidential guarantee is worthless if the app logs prompts to stdout and a sidecar ships them to the cloud's logging service. Build with `nvidia-container-toolkit` in no-persistence mode.

---

## Related Files

- [Confidential-AI-Inference](/confidential-computing/confidential-ai-inference)
- [Attestation-Architecture](/confidential-computing/attestation-architecture)
- [TEE-Technologies-Deep-Dive](/confidential-computing/tee-technologies-deep-dive)
- [Private-LLM-Inference-Patterns](/confidential-computing/private-llm-inference-patterns)

## Primary Sources

- NVIDIA: *Confidential Computing on NVIDIA H100 GPUs* (whitepaper, 2023)
- NVIDIA: *Blackwell Architecture Technical Brief* (2024)
- NVIDIA NVTrust repo — `github.com/NVIDIA/nvtrust`
- NRAS docs — `docs.attestation.nvidia.com`
- DMTF SPDM 1.2 spec — `dmtf.org/standards/spdm`

