---
title: "Confidential Containers (CoCo)"
tags:
  - "coco"
  - "confidential-containers"
  - "kata"
  - "kubernetes"
  - "tee"
  - "trustee"
  - "kbs"
sidebar: {"label":"Confidential Containers"}
---
*The CNCF project that makes confidential VMs look like regular Kubernetes pods — and an attestation-gated secret-release service that makes them actually safe.*

Home: `github.com/confidential-containers`.

---

## Why CoCo Exists

Container ecosystems assume the *node* is the trust boundary: kubelet reads secrets, the container runtime sees plaintext, the node OS has full memory access. In a TEE world, the *pod* (or even the container) is the trust boundary; the node is untrusted. CoCo is the glue that makes K8s schedulers, CRI runtimes, image pullers, and secret injectors respect that inversion.

---

## Stack

```
┌───────────────────────────────────────────────┐
│  Kubernetes control plane (untrusted)          │
└───────────────────────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────┐
│  Worker node (untrusted OS)                    │
│  ┌─────────────────────────────────────────┐  │
│  │ containerd + CoCo shim (Kata)           │  │
│  └──────────────┬──────────────────────────┘  │
│                 │ launches                     │
│                 ▼                              │
│  ┌─────────────────────────────────────────┐  │
│  │  Confidential VM (TDX / SEV-SNP)        │  │
│  │  ┌───────────────────────────────────┐  │  │
│  │  │  Kata-agent (measured in RTMR)    │  │  │
│  │  │  + attestation-agent              │  │  │
│  │  │  + image puller + decryptor       │  │  │
│  │  └───────────────────────────────────┘  │  │
│  │  ┌───────────────────────────────────┐  │  │
│  │  │  Workload container(s)            │  │  │
│  │  └───────────────────────────────────┘  │  │
│  └─────────────────────────────────────────┘  │
└───────────────────────────────────────────────┘
                │ attested channel
                ▼
┌───────────────────────────────────────────────┐
│  Trustee (out-of-band, operator-owned or       │
│  third-party)                                  │
│    - Key Broker Service (KBS)                  │
│    - Attestation Service (AS) — Veraison       │
│    - Reference Value Provider Service (RVPS)   │
│    - Resource repository (secrets, keys)      │
└───────────────────────────────────────────────┘
```

### Core Components

| Component | Role |
|---|---|
| **Kata Containers** | VM-per-pod runtime. CoCo uses a hardened Kata variant that launches *confidential* VMs (TDX/SNP) instead of normal KVM. |
| **Kata-agent** | Tiny agent inside the CVM that talks to the host shim over a hardened vsock channel; measured into RTMR. |
| **Attestation-agent** | Client-side of RATS; collects evidence (TDX quote, SNP report, etc.) and talks to the KBS. |
| **Image puller** | Pulls OCI images *inside* the CVM (not on the untrusted host), supports encrypted images (OCIcrypt / skopeo encrypt). |
| **Trustee** | The relying-party services: KBS, Attestation Service (Veraison-based), RVPS (known-good measurements), resource store. |
| **KBS (Key Broker Service)** | Single gateway the attestation-agent talks to; returns keys, secrets, or encrypted resources only after Attestation Service approves the evidence. |
| **Peer-pods** | CoCo mode where the CVM runs on a *different* host (e.g., a managed confidential VM instance in the cloud) because the K8s worker itself may not have TDX/SNP. The shim becomes a thin broker. |

### Threat Model

Trusted: silicon + firmware vendors, the Trustee operator (or, better, a split-Trustee / transparency-logged Trustee), the build pipeline for the workload image and the CoCo guest rootfs.

Untrusted: everything else — K8s control plane, kubelet, host OS, worker-node admin, container registry (encrypted images), network.

---

## What Actually Gets Measured

On launch of a confidential pod:

1. **MRTD** (TDX) / launch digest (SNP) = hash of the initial VM image + OVMF + initial kernel.
2. **RTMR[0..3]** extended with: kernel cmdline, initrd, Kata rootfs hash, agent policy.
3. **Agent policy** (OPA-style) hashed in: decides which kubelet RPCs the agent accepts — critical, because without policy, the untrusted kubelet can call `ExecProcess` into the enclave and read everything.

The workload container image itself is typically pulled-and-verified at runtime:
- Image signed via Cosign / Notation → signature checked inside enclave.
- Optionally encrypted with OCIcrypt → decryption key released by KBS only after attestation.

---

## Agent Policy (the detail that makes or breaks the security claim)

Kubernetes routinely does things the TEE's threat model says shouldn't be allowed: `kubectl exec`, `kubectl cp`, reading logs, mounting ConfigMaps the untrusted API server can rewrite. Without restrictions, the untrusted control plane can pull every secret out of the enclave.

**Agent policy** is a Rego document embedded in the guest image (and therefore measured) that whitelists exactly which kata-agent RPCs are allowed. Typical production policies deny `ExecProcess`, `ReadStreamRequest`, and `WriteStreamRequest`, and tightly constrain mount points. Every deployment must write this policy themselves; the default "allow everything" policy exists for dev only and is a footgun.

---

## Encrypted Images

Workflow:

1. Build image → encrypt with `skopeo copy --encryption-key jwe:pub.pem …` → push to registry.
2. Private key lives only in KBS.
3. At pull, image puller inside the CVM fetches ciphertext, asks attestation-agent for the decryption key, KBS verifies quote + RVPS lookup, releases key.
4. Plaintext image layers exist only in CVM memory.

Caveat: the OCI registry sees manifests, tags, and layer sizes. Traffic analysis can still reveal *which* encrypted image was pulled. If that matters, use a private registry in a TEE or pre-embed images.

---

## Related Projects

| Project | Relationship |
|---|---|
| **Edgeless Constellation** | Full K8s distribution where *all* nodes are confidential VMs; complementary to CoCo |
| **Edgeless MarbleRun** | Service mesh for confidential workloads; handles attestation-gated cert issuance |
| **Inclavare / Occlum** | Library-OS approach (SGX-centric); different trade-offs than CoCo's VM approach |
| **Gramine-SGX** | Library OS for unmodified Linux binaries in SGX; predates CoCo, still widely used for tight SGX workloads |
| **Veraison** | Open verifier used inside Trustee |
| **Keylime** | Runtime integrity verification (IMA) for confidential and non-confidential hosts; can be combined |

---

## Production Considerations

- **Cluster heterogeneity.** Not every node will have TDX or SNP. Use node taints + RuntimeClass so only confidential pods land on confidential nodes. Peer-pods mode sidesteps this by running CVMs on managed cloud confidential-VM instances.
- **Startup latency.** CVM boot + attestation + encrypted image pull typically adds 5–20s to cold start. Pre-warm pods if latency matters.
- **Secrets lifecycle.** Trustee must be operated by a party the *workload owner* (not the cluster operator) trusts. Otherwise you've recreated the trust problem you tried to escape.
- **Networking.** Service mesh mTLS is insufficient alone — the sidecar container can leak plaintext between itself and the app. Either run without a sidecar and do in-app mTLS, or use an attested-mesh (MarbleRun, Istio with confidential-aware CA).
- **GPU CC inside CoCo.** Supported on TDX-based CoCo with H100 CC via device passthrough; the GPU quote must be plumbed into the attestation evidence. Still early in 2026; expect rough edges.

---

## When Not to Use CoCo

- **Tiny, non-K8s workloads.** Direct SGX (Gramine) or a raw confidential VM is simpler.
- **Latency-critical under-1s functions.** CVM startup overhead dominates.
- **Jobs where the trust boundary is the VM, not the pod.** Then Constellation (all-confidential cluster) may be cleaner.
- **FHE / MPC workloads** where the whole point is no-hardware-trust — TEEs are the wrong tool.

---

## Related Files

- [Overview - Confidential Computing](/confidential-computing/overview-confidential-computing)
- [TEE-Technologies-Deep-Dive](/confidential-computing/tee-technologies-deep-dive)
- [Attestation-Architecture](/confidential-computing/attestation-architecture)
- [Confidential-AI-Inference](/confidential-computing/confidential-ai-inference)
- [Cloud-Provider-Comparison](/confidential-computing/cloud-provider-comparison)

## Primary Sources

- CoCo project — `github.com/confidential-containers`
- Trustee repo + docs — `github.com/confidential-containers/trustee`
- Kata Containers docs — `katacontainers.io/docs/`
- Edgeless Constellation — `docs.edgeless.systems/constellation`
- OCIcrypt spec — `github.com/containers/ocicrypt`

