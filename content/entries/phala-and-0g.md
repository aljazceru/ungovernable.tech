---
title: "Phala and 0G"
slug: phala-and-0g
type: deep-dive
pillars: ["compute", "confidential"]
readiness: usable
description: "Phala and 0G, two TEE-first decentralized compute networks for confidential and AI workloads: architectures, attestation and track records."
dek: "Two TEE-first decentralized compute networks. Phala has the longer track record and the more mature TEE marketplace; 0G adds a \"decentralized AI OS\" framing with Phala as one of its compute layers. Both pin attestation reports on-chain so workloads carry verifiable trust from the silicon up."
updated: 2026-10-25
created: 2026-04-25
origin: vault
source: "04-Decentralized-Compute/Phala and 0G.md"
aliases: ["Phala Cloud", "dstack", "0G Network"]
tags: ["phala", "0g", "tee", "decentralized-compute", "attestation", "deep-dive"]
---

## Phala — position

Phala is the most-developed TEE marketplace in decentralized compute. Its evolution:

- Phase 1 (2018-2022): SGX-based confidential smart contracts.
- Phase 2 (2022-2024): Phala Cloud, a TEE marketplace running TDX, SEV-SNP, and NVIDIA H100 CC workloads.
- Phase 3 (2024-2026): `dstack`, a developer SDK that packages docker-compose-style workloads into TDX confidential VMs with on-chain attestation.

The differentiating claim is **on-chain attestation**. A Phala workload's attestation report is anchored to the Phala chain (or relayable to Ethereum or other chains), so any smart contract or off-chain client can verify "this workload runs the agreed binary in a real TDX VM" without trusting Phala itself.

## dstack — the developer story

```
Developer:
  - writes a docker-compose.yml
  - signs a manifest committing to the image hashes
  - deploys via Phala Cloud SDK

Phala:
  - allocates a TDX CVM on a participating provider
  - provider boots the docker-compose, fetches images by hash
  - TDX produces an attestation report covering the boot + image set
  - report posted on-chain

Client:
  - queries on-chain attestation
  - verifies provider's TDX certificate chain
  - obtains TLS-bound key from inside the enclave
  - establishes attested TLS to the workload
```

Effects:

- Familiar UX (docker-compose, not raw enclave SDK).
- Reproducible builds via manifest-pinned image hashes.
- On-chain verifiability so anyone can audit the trust chain.
- Multi-provider: workloads can move providers and re-attest.

This is the cleanest decentralized confidential-compute developer story in 2026.

## Phala for confidential AI

The flagship use case. A model owner ships an open-weights or proprietary LLM to a Phala dstack workload running TDX + H100 CC. End users connect over attested TLS, verify the attestation, and send prompts. Three properties hold:

- The operator can't read prompts. TDX + H100 CC encrypts everything.
- GPU memory protection depends on the hardware and mode. On H100, access controls protect HBM while CPU–GPU transfers are encrypted; HBM itself is not encrypted.
- The client can verify that the workload runs the published binary on the published model.

Used in production by partners offering "open inference" services to users who don't want to send prompts to OpenAI.

## 0G — position

0G frames itself as a "decentralized AI OS" — broader scope than just compute. Components:

- 0G Storage: decentralized object storage with verifiable retrieval.
- 0G Compute: TEE-attested compute, often using Phala as the underlying infrastructure.
- 0G DA (Data Availability): modular DA layer for rollups.
- 0G Consensus: Cosmos-style chain anchoring everything.

The thesis is that training and serving large models requires storage, compute, data availability, and verifiable attestation. 0G assembles these into one tightly integrated stack rather than relying on independent providers for each.

In practice, 0G's compute layer composes with Phala (TEE attestation) and adapts the broader Cosmos / EVM tooling around it.

## Comparison

| Dimension | Phala / dstack | 0G | [Akash](/kb/akash/) | Marlin Oyster |
|-----------|----------------|-----|-----------|---------------|
| Trust model | TDX/SEV-SNP/H100 CC + on-chain attestation | TEE attestation across stack | Trust provider | TDX/Nitro+H100 CC |
| Workload | docker-compose | LLM serving + storage | Kubernetes containers | Custom CVM images |
| Attestation | On-chain | On-chain | None native | On-chain |
| GPU CC | Yes | Yes (via Phala) | Provider-dependent | Yes |
| Persistent storage | Limited | First-class (0G Storage) | Provider option | Limited |
| Maturity | Production | Growing | High | Growing |

## Use cases

### Confidential LLM endpoint

```
Model owner ─► dstack manifest ─► Phala Cloud
                                  ─► TDX + H100 CC instance
                                  ─► attested TLS endpoint
                                  ─► users verify, send prompts
```

Replaces "trust OpenAI's privacy policy" with "verify the silicon".

### Confidential RAG over private corpus

A customer's private document corpus is stored encrypted (or held in a TEE-readable form). Phala dstack runs the retrieval and the LLM. The provider sees neither corpus nor queries.

### Cross-chain attestation

A smart contract on Ethereum needs to know that the off-chain compute for a prediction market ran in a real TEE on the published code. Phala posts the attestation to Ethereum via a bridge; the contract verifies. The pattern is used in oracle-style flows where DLCs would be unwieldy.

### Decentralized AI workflows on 0G

Train a model on 0G Compute, store weights in 0G Storage, publish attestation, serve inference on Phala. All verifiable, all on-chain anchored.

## Trade-offs

### Strengths (both)

- TEE attestation as a first-class primitive. No other large decentralized compute network does this as well.
- GPU CC support. H100 confidential mode is integrated.
- On-chain verifiability. Any client can audit.
- Developer ergonomics improving. dstack is the cleanest TEE-aware docker-compose available.

### Limitations

- TEE trust assumption. You trust Intel, AMD, or NVIDIA. (This is true for any TEE-based system.)
- Smaller provider pool than Akash; less geographic diversity.
- Chain dependency. Both Phala and 0G run their own chains; chain liveness matters for attestation availability.
- 0G is newer, with less production track record than Phala.
- Token economics introduce attack surface separate from the technical design.

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| TEE side-channel on provider | Multi-vendor diversity; TCB updates; layer with FHE for highest stakes |
| Compromised attestation chain | Multi-party signing of attestation aggregations |
| Image-supply-chain | Pin image hashes; reproducible builds; Sigstore-like transparency |
| Provider downtime | Multi-provider redundancy via dstack manifests |
| Smart-contract bugs in attestation verifier | Audited verifier circuits / contracts |
| Token-economic attacks | Slashing, stake-bounded influence |

## Operational patterns

### Phala dstack quick start

```
git clone dstack-app-template
edit docker-compose.yml + manifest.yml
phala deploy --network mainnet
# returns attestation handle + endpoint
verify attestation client-side, then connect via attested TLS
```

### Multi-provider failover

dstack manifests can list multiple providers; if one drops, another picks up. Re-attestation happens automatically on failover.

### Combine with Akash

Some users deploy dstack workloads on Akash providers. Akash for the marketplace, dstack for the TEE attestation. A hybrid stack.

## Recent developments (2024-2026)

### Ethereum L2 Migration — November 19, 2025

Phala completed its most significant architectural transition since launch: migrating from a Polkadot parachain to an Ethereum Layer 2. Key facts:

- **Community vote**: Approved decisively before the November 20, 2025 parachain slot expiry.
- **Token migration**: PHA → vPHA (ERC-20) at 1:1 ratio.
- **New architecture**: Phala L2 = execution layer for GPU/TDX confidential compute; Ethereum L1 = staking and governance.
- **Migration timeline**: November 19, 2025 — all collators and Gatekeepers manually stopped; assets frozen on old chain; claim process opened.
- **Bridge pause**: Phala-Ethereum bridge paused November 10, 2025 to ensure clean migration.
- **Rationale**: Deeper Ethereum ecosystem integration, broader tooling access, EVM alignment, better scalability for GPU compute workloads.

This is the end of Phala's four-year Polkadot chapter. The Ethereum L2 positioning gives Phala access to the largest smart contract ecosystem and its tooling, liquidity, and enterprise integrations.

### Phala 2025 Full-Stack Confidential AI — Year in Review

By end of 2025, Phala reported:

- **10,004** total users
- **398** paid users
- **2,529** CVMs deployed (813 running simultaneously)
- **3.05B LLM tokens** processed in a single day (peak)
- Crossed from TEE research into production-grade infrastructure with real enterprise customer traction.

### OLLM Partnership — Confidential AI Gateway (December 2025)

OLLM, a privacy-first AI infrastructure firm, partnered with Phala to integrate Phala's GPU TEE confidential AI cloud into the OLLM AI Gateway:

- Every request to a Phala-backed model on OLLM is processed inside a hardware-isolated TEE enclave.
- Cryptographic proof of confidentiality visible in the OLLM scanner.
- Builders can tap hardware-secured models with verifiable privacy without rewriting their stack.
- Drop-in OpenAI-compatible API: `base_url = https://api.redpill.ai/v1`.
- Users verify the attestation before sending prompts.

### NVIDIA H100 CC Mainstream

H100 confidential computing protects GPU memory through isolation and encrypts transfers through shared bounce buffers. NVIDIA explicitly states that Hopper HBM is not encrypted; do not describe H100 support as GPU memory encryption.

### dstack as the SDK Pattern

dstack is now the canonical developer experience for Phala:

- docker-compose-style workloads inside TDX confidential VMs.
- On-chain attestation verifiable by any client.
- Multi-provider failover with automatic re-attestation.

### 0G Mainnet

0G mainnet rollout of compute, storage, and DA layers — positioning as a "decentralized AI OS" with Phala as the TEE-attested compute substrate.

### Cross-chain Attestation Matured

Phala posts attestations to Ethereum via bridge, enabling smart contracts to verify off-chain TEE compute without trusting Phala itself.

### Throughput Breakout — August 2026

Confidential-inference volume steepened through August, per official @PhalaNetwork reporting:

- **Aug 9: ~5.2B billed tokens/day** (doubled from ~2.6B in late July).
- **Aug 22: 37.11B billed input+output tokens in 24 hours** — the peak reading, roughly 7x the Aug 9 figure.
- **Aug 24: 16.66B tokens/day** — 37B was a spike; the new operating band appears to be 15–25B/day.
- Model mix (Aug 24): DeepSeek V4 Flash 39.44%, GLM-5.2 26.48%, Muse Glimmer 30B 8.94% — open-weight, refusal-free models dominate confidential demand.

Enterprise posture hardened alongside: **SOC 2 Type I certified, HIPAA compliant, ISO 27001 in progress, GDPR-aligned processing, 99.9% uptime SLA**. **OPPO × Phala** published a joint paper on Kubernetes **Pod-level remote attestation** for confidential AI (arXiv:2606.03323, June 2026) — proving hardware, container image, and Pod identity before sensitive data enters the workload; the granularity confidential Kubernetes actually needs.

The paradox to track: **PHA hit its all-time low Aug 3 ($0.01922)** and trades ~$0.022 while usage multiplied ~7x in two weeks — token value capture from confidential-inference volume remains the unsolved design problem.

### DeAI Dashboard Placement (August 2026)

Per the [DeAI Dashboard coverage](/briefings/compute/2026-08-25/) (Aug 14), Phala's OpenRouter-served tokens and phala.com live chart make it one of the independently-tracked networks; its OpenRouter provider listing remains a key distribution channel — a dependency given Stripe's acquisition of OpenRouter (Aug 19, $7.5B).

### September 08, 2026 Update — 40.4B Tokens/Day Peak, dstack Repo Re-org, Audit Settled

The Sept 2–8 weekly update confirmed three structural moves that harden Phala's standing on the OpenRouter provider surface:

1. **New peak: 40.4B tokens/day on the Sept 2 home-page snapshot** (vs 28.1B at the Sept 5 server-render — the home page captures the most-recent rolling-window peak, with 10 active models, vs 7 in late August). Phala cleared the 40B/day ceiling for the first time and remains the only DePIN-native network hitting Groq-class last-week token volumes inside the Stripe-owned OpenRouter surface.
2. **dstack repo re-org is now visible on GitHub.** `Phala-Network/dstack-cloud` was archived by the owner on Jun 10, 2026 (read-only, 6★, 2,263 commits, no successor pointer). The canonical runtime is **`Dstack-TEE/dstack`** — the GitHub org rename is consistent with the `go get github.com/Dstack-TEE/dstack/sdk/go` import path now published on the dstack landing page. Auditors and CI consumers should pin to `Dstack-TEE/dstack` (not `Phala-Network/dstack-cloud`) when wiring in 2026 H2.
3. **zkSecurity audit (May–June 2026) formally announced (Aug 13)** as the first OS-level TEE platform audit; the dstack Attestation Pipeline Hardening follow-up was published Jun 16. By the time SOC 2 / HIPAA / ISO 27001 buyers come asking, the audit answer is on the public record.

See [Decentralized Compute Tuesday — September 08 2026 Weekly Update](/briefings/compute/2026-09-08/) for the full coverage including Phala's home-page token-trajectory table and the cross-cloud dstack comparison (AWS Nitro / GCP TDX / Phala native).

## Primary sources

- [NVIDIA H100 memory and transfer protections](https://developer.nvidia.com/blog/confidential-computing-on-h100-gpus-for-secure-and-trustworthy-ai/)

- Phala Network — [phala.network](https://phala.network).
- Phala Cloud — [docs.phala.network/phala-cloud](https://docs.phala.network/phala-cloud).
- dstack — [github.com/Phala-Network/dstack](https://github.com/Phala-Network/dstack).
- Phala source — [github.com/Phala-Network](https://github.com/Phala-Network).
- 0G Network — [0g.ai](https://0g.ai).
- 0G docs — [docs.0g.ai](https://docs.0g.ai).
