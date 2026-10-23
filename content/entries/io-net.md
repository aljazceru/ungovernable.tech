---
title: "io.net"
slug: io-net
type: deep-dive
pillars: ["compute"]
readiness: usable
description: "io.net aggregates GPUs from data centres and individuals into an AI compute marketplace: how it works, what it offers and how trust is handled."
dek: "The AI/ML-focused GPU aggregator. A Solana-based DePIN that aggregates GPUs from multiple sources — render farms, crypto miners, Filecoin storage providers, and independent data centers — into a unified decentralized GPU cloud optimized for AI inference and training workloads."
updated: 2026-06-09
created: 2026-04-28
origin: vault
source: "04-Decentralized-Compute/io.net.md"
aliases: ["IO Cloud", "Internet of GPUs"]
tags: ["io.net", "gpu", "depin", "decentralized-compute", "ai", "ml", "deep-dive"]
---

## Position

io.net is the newest major entrant in this library's GPU compute coverage:

- **Founded 2023** — younger than Render (2017), Golem (2017), and Akash (2020).
- **Solana-based** — IO token is an SPL token on Solana.
- **Aggregator model**: pulls GPU supply from diverse sources (Render, Filecoin, independent farms).
- **AI/ML-first**: built specifically for AI and machine learning workloads, not general compute or rendering.

Compared to other networks:

- **vs. Render**: Render is dedicated GPU rendering; io.net aggregates Render's supply plus other sources and focuses on AI/ML.
- **vs. Akash**: Akash is generic K8s containers; io.net is GPU-specific and ML-optimized.
- **vs. Phala**: Phala is TEE-confidential; io.net has no TEE component.
- **vs. Bittensor**: Bittensor is AI subnets with token incentives; io.net is raw GPU compute.

## Architecture

### Supply aggregation

io.net's innovation is aggregating GPU supply from multiple sources:

- **Render Network contributors**: Render providers can plug into io.net.
- **Filecoin storage providers**: Mining hardware with GPUs repurposed for compute.
- **Independent data centers**: Small and medium GPU clusters.
- **Cryptocurrency miners**: Ethash/Equihash miners with idle GPUs.
- **Consumer GPUs**: Individual providers contributing gaming GPUs.

This aggregator model means io.net doesn't need to bootstrap its own provider network from scratch — it taps existing GPU inventory via partnerships and integrations.

### Verification and quality

Before any workload runs:

1. **Proof-of-Work verification**: GPU actually has the claimed compute.
2. **Proof of Time-Lock**: Provider commits to a lock-up period.
3. **Staking**: Providers stake IO as a performance bond.
4. **12-hour onboarding** (first-time): GPUs, network, and system are stress-tested.

### Platform components

The io.net ecosystem:

- **IO Cloud**: The core marketplace — dynamic scaling for AI/ML applications.
- **IO Intelligence**: AI infrastructure platform — pre-trained models and AI agents.
- **IO Worker**: Interface for GPU providers to contribute resources.
- **IO Staking**: Co-staking allocations tracking.
- **IO Explorer**: Real-time monitoring of compute usage and network activity.
- **IO ID**: Provider earnings tracking and withdrawals.

### 2025-2026: Solana migration

Notable 2026 development: io.net migrated fully to Solana, citing:
- Instant GPU payments.
- Smart contract automation.
- Secure decentralized compute transactions.
- Integration with the broader Solana DePIN ecosystem.

## IO token

- **Blockchain**: Solana (SPL token)
- **Utility**: Payments, provider staking, governance
- **Staking model**: Providers stake IO as performance bond; slashing for underperformance.
- **Reward distribution**: IO tokens distributed to providers based on compute contributed.

## Use cases

### AI inference at scale

The primary io.net use case:

- LLMs serving on decentralized GPUs.
- Dynamic scaling across the aggregated network.
- Cost-competitive with hyperscalers for specific workloads.

### ML training

Distributed training workflows across heterogeneous GPUs:

- Fine-tuning open-weights models.
- Batch training on aggregated compute.
- Integration with distributed training frameworks.

### Inference via Render

io.net partners with Render to provide an inference pathway:

- Render focused on rendering.
- io.net provides AI/ML compute.
- Combined, they offer a broader GPU marketplace.

## Comparison

| Dimension | io.net | Render | Akash | Phala/dstack | Golem |
|-----------|--------|--------|-------|-------------|-------|
| Founded | 2023 | 2017 | 2020 | 2022 | 2017 |
| Token | IO (Solana) | RNDR (Solana) | AKT (Cosmos) | PHA (Substrate) | GLM (ETH) |
| Blockchain | Solana | Solana | Cosmos | Substrate | Ethereum |
| Supply model | Aggregator | Dedicated | Marketplace | Dedicated | Marketplace |
| AI/ML focus | Primary | Secondary | Generic | TEE | Generic |
| GPU rendering | Via Render | Primary | No | No | Limited |
| TEE | No | No | 2026 | Yes | No |
| Verification | PoW + PoT-Lock | Provider stake | Escrow | TEE | Escrow |

## Trade-offs

### Strengths

- **Aggregator model**: Fast supply scaling by tapping existing GPU inventory.
- **AI/ML optimization**: Purpose-built for ML inference and training.
- **Solana integration**: Fast settlement, DePIN ecosystem alignment.
- **Diverse sources**: Combines render farms, miners, and data centers.
- **2025 production proof**: Real AI workloads executed on the network.

### Limitations

- **No confidential computing**: Provider sees all data. Not suitable for prompt privacy.
- **Aggregator dependency**: Relies on Render, Filecoin, etc. for supply. If partnerships falter, supply shrinks.
- **No TEE story**: Unlike Phala, no path to confidential AI inference.
- **Newer than Render**: Less track record in production GPU compute.
- **Solana dependency**: Has a blockchain dependency risk.
- **Verification overhead**: The 12-hour onboarding and verification may limit provider onboarding speed.

## Attack surface

| Attack | Mitigation |
|--------|------------|
| Provider reads data | No TEE. Don't use for sensitive prompts. |
| Fake GPU claims | Proof-of-Work verification, Proof of Time-Lock, staking. |
| Sybil flooding | Hardware requirements, verification delays. |
| Staking manipulation | Co-staking model. |
| Oracle pricing | Multi-source; off-chain reference. |
| Solana congestion | Fee smoothing. |

## Recent developments (2024-2026)

### Dell Technologies Partnership — Authorized Partner and Cloud Service Provider (June 2026)

io.net announced a partnership joining **Dell Technologies Authorized Partner and Cloud Service Provider program**. The collaboration:

- Merges io.net's decentralized GPU network with Dell's hardware and infrastructure.
- Go-to-market: demand generation and co-marketing.
- Positioned as bridging decentralized GPU power with enterprise-grade hardware infrastructure.
- Dell's channel relationships and enterprise salesforce give io.net access to customers that wouldn't find a crypto-native project organically.

### Additional Partnerships (May-June 2026)

- **Creator.Bid**: Partnership to accelerate image model scaling using decentralized GPUs.
- **Alpha Network**: Partnership to establish a secure, decentralized environment for AI and Web3 applications.
- **Mira Network**: Strategic partnership for decentralized AI landscape.

### 2025 Production Proof — Real AI Workloads Executed

From io.net's 2025 Year in Review:

- **Wondera**: $2.48M savings vs AWS equivalent, 552,000 GPU hours, 96 GPUs (64 H100s + 32 H200s).
- **Leonardo.Ai**: Scaled from 14K to 19M users while cutting GPU costs 50%+ vs AWS.
- Platform claim: **30,000+ GPUs** available, up to 70% lower cost than AWS.

### Solana Migration (2026)

io.net migrated fully to Solana, citing:
- Instant GPU payments.
- Smart contract automation.
- Secure decentralized compute transactions.
- Integration with the broader Solana DePIN ecosystem.

### IO Intelligence

Launched AI infrastructure platform — pre-trained models and AI agents on decentralized GPU.

## Primary sources

- io.net — [io.net](https://io.net)
- Blog — [io.net/blog](https://io.net/blog)
- Documentation — [docs.io.net](https://docs.io.net)
- 2025 Year in Review — [io.net/blog/2025-io-net-year-in-review](https://io.net/blog/2025-io-net-year-in-review)
- Solana migration — [io.net/blog/io-net-on-solana-the-place-for-depin-in-2026-and-beyond](https://io.net/blog/io-net-on-solana-the-place-for-depin-in-2026-and-beyond)
- Messari report — [messari.io/report/understanding-io-net-a-comprehensive-overview](https://messari.io/report/understanding-io-net-a-comprehensive-overview)
