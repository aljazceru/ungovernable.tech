---
title: "Golem Network"
slug: golem
type: deep-dive
pillars: ["compute"]
readiness: usable
description: "Golem, one of the oldest decentralized compute markets: a two-sided marketplace for general-purpose computation and what years of operation show."
dek: "The oldest decentralized compute market. A 2017-vintage ERC-20 token and battle-tested two-sided marketplace for generic compute — essentially a peer-to-peer rental market for idle CPU and GPU cycles."
updated: 2026-06-09
created: 2026-04-28
origin: vault
source: "04-Decentralized-Compute/Golem.md"
aliases: ["Golem Network", "Yagna"]
tags: ["golem", "glm", "decentralized-compute", "depin", "deep-dive"]
---

## Position

Golem is the oldest project in this library's decentralized compute coverage:

- **Founded 2017** — predates most DePIN and decentralized compute projects by years.
- **GLM token** — utility token on Ethereum (ERC-20) and Polygon.
- **Generic compute** — not specialized to a single workload type; any embarrassingly parallel job works.
- **Architecture: provider/requestor** — the standard peer-to-peer model Golem helped pioneer.

Compared to the rest of this library's compute coverage:

- **Akash**: Kubernetes-style container deployments; Golem is more task-oriented.
- **Phala**: TEE-confidential; Golem has no TEE component.
- **Render**: GPU rendering/ML-specific; Golem is generic.
- **Bittensor**: specialized AI subnets; Golem is general-purpose.

## Architecture

### Provider / Requestor model

Golem implements the classic two-sided marketplace:

- **Providers**: operators running the `yagna` daemon and sharing CPU/GPU resources. Each provider runs inside a sandboxed VM (was Docker, evolved to unikernels).
- **Requestors**: actors who submit jobs (Golem calls them "activities") to the network and pay in GLM.
- **Yagna daemon**: the core software both providers and requestors run. Implements the Golem protocol, market, and payment settlement.

### Market and settlement

The Golem market matches provider offers to requestor demands:

1. Requestor posts a **demand** (specifies compute requirements and price).
2. Providers with matching **offers** are selected.
3. Job runs on the provider's infrastructure.
4. Provider invoices the requestor.
5. Payment settles in GLM (via Polygon or Ethereum).

### Payment platforms

Golem supports settlement on:
- **Ethereum Mainnet** — expensive but highest security.
- **Polygon** — lower fees, sufficient for most microtransactions.

### Sandbox

Golem pioneered the execution sandbox:

- Early versions: Docker-based.
- Current: Unikernel-based VMs for stronger isolation between requestor workloads.
- Each job runs in its own execution environment; providers can't access other providers' data or each other's jobs.

## GLM token

- **Standard**: ERC-20 (Ethereum)
- **Networks**: ETH Mainnet and Polygon
- **Supply**: 1,000,000,000 total (1:1 migration from legacy GNT)
- **Utility**: the sole currency for paying providers

### GNT → GLM migration

Golem's original token was GNT (2017). Migration to GLM began in late 2020 and is ongoing. 1:1 conversion ratio.

## Use cases

### Batch computation

The canonical Golem use case: embarrassingly parallel batch jobs where provider trust doesn't matter.

- **Examples**: rendering farms, video encoding, distributed computing (BOINC-style science workloads).
- **Current fit**: moderate. Golem handles this but has more competition now.

### Web2 partnership

Notable 2026 development: **Salad.com partnership** — a GPU cloud platform that partnered with Golem to test Golem's network for enterprise-grade AI and rendering workloads, with settlements in GLM.

This represents Golem's path to real-world adoption: engineering trials with established Web2 GPU cloud platforms.

### Token utility

For token-economic analysis: GLM is one of the earliest DePIN tokens with continuous mainnet operation since 2017. Longest track record of any decentralized compute token.

## Comparison

| Dimension | Golem | Akash | Phala/dstack | Render | io.net |
|-----------|-------|-------|-------------|--------|-------|
| Founded | 2017 | 2020 | 2022 | 2017 | 2023 |
| Token | GLM (ERC-20) | AKT (Cosmos) | PHA (Substrate) | RNDR (Solana) | IO |
| Focus | Generic batch | K8s containers | TEE compute | GPU rendering | GPU ML |
| GPU support | Limited | Growing | H100 CC | Strong | Strong |
| Confidential | No | No (roadmap) | Yes (TEE) | No | No |
| TEE roadmap | No | 2026 | Production | No | No |
| Status | Maintain | Active | Active | Active | Active |

## Trade-offs

### Strengths

- **Battle-tested**: 8+ years of mainnet operation. Longest track record in decentralized compute.
- **Generic model**: any parallelizable workload fits. Not constrained to containers or specific GPU architectures.
- **Simple trust model**: the provider sees the data. For non-sensitive workloads, this is fine.
- **Polygon settlement**: low fees for high-volume microtransactions.

### Limitations

- **No confidential computing**: provider is fully trusted. For AI inference where prompt privacy matters, this is a dealbreaker.
- **Smaller network**: far fewer providers than Akash or Render. Limited GPU inventory.
- **No frontier AI story**: not optimized for LLM inference or training in the way modern GPU networks are.
- **Slow evolution**: newer projects (Phala, Akash 2026 GPU, Bittensor) move faster.
- **Developer tooling**: Yagna is Rust-based; less mainstream than Kubernetes/Docker for the average cloud developer.

## Attack surface

| Attack | Mitigation |
|--------|------------|
| Provider reads requestor data | No mitigation — full trust. Don't use for sensitive workloads. |
| Provider runs malicious code | Sandbox (unikernels). Requestor verifies results. |
| Provider claims work without doing | Reputation system and scoring. |
| Payment fraud | Escrow via market smart contract. |
| Sybil providers | Identity and reputation require history. |
| Smart contract exploit | Audited contracts. Time-locked admin. |

## Primary sources

- Golem — [golem.network](https://golem.network)
- Documentation — [docs.golem.network](https://docs.golem.network)
- GitHub — [github.com/golemfactory/golem](https://github.com/golemfactory/golem)
- GitHub (yagna) — [github.com/golemfactory/yagna](https://github.com/golemfactory/yagna)
- GLM token — [golem.network/glm](https://golem.network/glm)
- Salad partnership (Jan 2026) — [blog.golem.network](https://blog.golem.network)
