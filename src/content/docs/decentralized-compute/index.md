---
title: "Decentralized Compute"
tags:
  - "decentralized-compute"
  - "akash"
  - "golem"
  - "render"
  - "phala"
  - "bacalhau"
  - "confidential-inference"
  - "aethir"
  - "nosana"
  - "gensyn"
sidebar: {"label":"Overview","order":0}
---
*Permissionless markets for CPU, GPU, and (increasingly) confidential-GPU time. The supply side of an internet where you can rent computation without a cloud account, and — when combined with TEEs — without trusting the node operator.*

---

## Why decentralize compute

- No account gatekeeping. Sanctioned, under-banked, or pseudonymous users can pay in crypto and get compute.
- Provider diversity. Side-steps concentration risk (three hyperscalers run most of the world's inference).
- Price discovery. Idle GPUs from gamers, universities, and miners can be priced at marginal cost, beating hyperscaler margins for some workloads.
- Confidential by default. Combining decentralized compute with TEEs and attestation means the node operator can't read prompts and can't steal the model — a trust model no centralized cloud offers.

---

## Major networks

| Network | Focus | Tech |
|---|---|---|
| Akash | General K8s workloads | Cosmos SDK; reverse-auction; GPU support 2024+ |
| Golem | Task-based CPU compute | Long-running; generic tasks |
| Render | GPU rendering / ML | RNDR token; Octane/ML jobs |
| io.net | GPU aggregation for ML | Layer atop Render, Filecoin workers, others |
| Fluence | Serverless confidential compute | Rust-focused; TEE support |
| Bacalhau | Compute-over-data | Deterministic jobs near Filecoin/IPFS data |
| Phala Cloud | TEE marketplace | SGX → TDX + H100 CC; on-chain attestation |
| Marlin Oyster | CVM marketplace | Nitro + TDX + H100 CC |
| Nosana | AI inference | Solana-based; Google Gemini tested |
| Gensyn | Decentralized training | Proofs of training work |
| Prime Intellect | Distributed training | DiLoCo / federated |
| Aethir | Enterprise GPU cloud | ATH token; Strategic Compute Reserve |
| 0G | Decentralized AI OS | Phala TEE integration |

---

## Patterns

### Raw compute (non-confidential)

Akash, Golem, Render. Suitable for open workloads (rendering, public model inference, batch jobs) where the provider seeing the data doesn't matter.

Akash 2025-2026 changes:

- Homenode Early Access (2026): lets average users participate as providers.
- NVIDIA H200 nodes added to the GPU waitlist.
- AEP-67: Console improvements (March 2026).
- AEP-65: Confidential Computing with TEE (target July 2026).
- AEP-29: Hardware Verification using Trusted Execution — providers prove CPU/GPU specs via attestation.
- Lease-to-lease networking: dynamic IP address management between tenant workloads.
- 99%+ cost reduction from gas optimizations on L1.

### Confidential compute

Phala, Marlin, Oasis ROFL, Automata, and Fluence run workloads inside TEEs on community-operated nodes. On-chain smart contracts verify attestation quotes before a job is considered valid and paid. This is how you get:

- Private inference on open-weights LLMs without trusting any cloud (Tinfoil sits adjacent; Phala is the canonical on-chain version).
- Verifiable off-chain computation for smart contracts (oracles).
- Private DeFi strategies, private order matching.

2025-2026 TEE confidential AI work:

- Phala + 0G: Phala's TEE SDK integrated into 0G's decentralized AI Operating System for confidential inference.
- Phala + Venice AI: end-to-end encrypted AI inference mode launched — prompts encrypted on device, stay encrypted in transit, decrypted only inside the TEE.
- Phala + ai16z: TEE technology integrated into the Eliza AI Agent framework (Q4 2024).
- Phala + NeurochainAI: partnership supplying GPU TEE compute infrastructure.
- Akash AEP-65: Confidential Computing with TEE (target: July 2026).
- Akash AEP-29: Hardware Verification using Trusted Execution for provider attestation (live).

See [Confidential-AI-Inference](/confidential-computing/confidential-ai-inference) and [NVIDIA-GPU-TEE](/confidential-computing/nvidia-gpu-tee).

### Verifiable compute without TEEs

Gensyn, RISC Zero, and Succinct use cryptographic proofs (ZK or optimistic challenges) to prove compute was performed correctly without TEEs. Slower, but no hardware trust required.

2025-2026 Gensyn work:

- ICLR 2026 workshop hosted on open problems in decentralized training.
- Testnet dashboard showing contributor stats.
- On-chain identity tracking node progress.
- Collaborative foundation models via local assistants.

### Compute-over-data

Bacalhau and similar systems move the job to the data (large datasets on Filecoin / IPFS) rather than shipping data to compute. Natural fit for ZK, FHE, or TEE privacy layers.

### Solana-based GPU networks

Nosana: decentralized GPU grid on Solana, optimized for AI inference.

- 2025-2026 changes:
  - Public GPU-grid testnet for AI inference workloads.
  - Documented partnerships include Exabits, Piknik, Inferia, Sogni, Rivalz, OpenGPU.
  - Node operators earn NOS rewards.
  - Focus areas: 3D rendering, video processing, scientific simulations, AI inference.

### Enterprise GPU clouds

Aethir: enterprise-grade decentralized GPU cloud focused on enterprise customers.

- 2025-2026 changes:
  - ATH Strategic Compute Reserve with Predictive Oncology (first of its kind).
  - Enterprise case studies with AI and robotics clients.
  - Cloud Host incentive model based on GPU usage, uptime, and performance.
  - H2 2026: agentic AI booking real-time GPU inference.
  - Focus: AI-driven gaming user acquisition, enterprise AI workloads.

---

## Trade-offs

### Strengths

- Censorship resistance. No single provider can kick you off.
- Combined with TEEs, a stronger privacy story than any hyperscaler.
- Aligned economic incentives (stakers lose money for cheating).

### Limitations

- Reliability. Hyperscaler SLAs beat decentralized networks by a wide margin; workloads need retries and redundancy.
- Performance variance. Heterogeneous hardware; no guaranteed NVLink topologies for multi-GPU jobs.
- Compliance friction. Data-residency and regulatory audits are harder.
- Egress and data gravity. Moving large datasets in and out of decentralized storage is slow.
- Onboarding UX. Crypto wallets and CLI tools keep mainstream users out for now.

---

## Attack surface

- Malicious node operator. The whole reason to use TEEs and attestation. Without them, the operator is fully trusted.
- Sybil attacks on reputation systems.
- Stake-grinding and free-rider attacks on proof-of-compute schemes.
- Oracle compromises. If off-chain data feeding on-chain payments is wrong, the whole market distorts.
- Network splits. Partitioned verifiers may accept inconsistent attestation collateral.

---

## Related files

- [Confidential-AI-Inference](/confidential-computing/confidential-ai-inference)
- [NVIDIA-GPU-TEE](/confidential-computing/nvidia-gpu-tee)
- [Attestation-Architecture](/confidential-computing/attestation-architecture)
- [Confidential-Containers](/confidential-computing/confidential-containers)
- [Overview - Zero-Knowledge Proofs](/zero-knowledge)

## Primary sources

- Akash — `akash.network/docs` | [2026 Roadmap](https://akash.network/roadmap/2026/)
- Phala Cloud / dstack — `phala.network` | [0G Partnership](https://www.bitget.com/news/detail/12560604458724)
- Marlin Oyster — `docs.marlin.org`
- Oasis ROFL — `docs.oasis.io/build/rofl`
- Gensyn — [gensyn.ai](https://www.gensyn.ai) | [Contribute](https://www.gensyn.ai/contribute) | [ICLR 2026](https://x.com/gensynai/highlights)
- Nosana — `nosana.com` | [Blog](https://nosana.com/blog/)
- Aethir — `aethir.com` | [Strategic Roadmap](https://ecosystem.aethir.com/blog-posts/aethirs-12-month-strategic-roadmap-supercharging-enterprise-ai-compute-growth)
- 0G — `0g.ai`
- Render Network — `rendernetwork.com`
- io.net — `io.net`

