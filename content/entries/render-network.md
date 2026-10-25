---
title: "Render Network"
slug: render-network
type: deep-dive
pillars: ["compute"]
readiness: usable
description: "Render Network, a decentralized GPU rental market that grew from 3D rendering into AI compute: how jobs, nodes and payments work."
dek: "The oldest decentralized GPU compute network. A Solana-based GPU rental market (RNDR token) that started as a rendering farm and expanded to AI/ML compute. Founded 2017, the original decentralized GPU primitive."
updated: 2026-06-09
created: 2026-04-28
origin: vault
source: "04-Decentralized-Compute/Render Network.md"
aliases: ["Render Network", "RNDR", "OctaneRender"]
tags: ["render", "rndr", "gpu", "decentralized-compute", "depin", "deep-dive"]
---

## Position

Render Network occupies a specific niche in this library's decentralized compute coverage:

- **Founded 2017** — alongside Golem, the oldest decentralized compute project.
- **Solana-based** — RNDR is an SPL token on Solana.
- **GPU-first**: built for GPU workloads (rendering, ML, AI inference), not generic compute.
- **Specialization over generalization**: compared to Akash (generic K8s), Render is optimized for GPU compute.

Compared to other networks:

- **vs. Akash**: Akash is generic compute with container model; Render is GPU-specific but with a dedicated rendering pipeline.
- **vs. Phala**: Phala is TEE-confidential; Render has no TEE component.
- **vs. Golem**: Golem is generic CPU/GPU batch; Render is GPU-specialized.
- **vs. io.net**: Both GPU-focused; Render is older with a stronger rendering legacy; io.net is newer, more ML-focused, and aggregates multiple sources.

## Architecture

### Core components

- **RENDER token**: SPL token on Solana. (RNDR was rebranded to RENDER in 2025; older references still use RNDR.)
- **GPU Providers**: operators running GPUs (typically professional render farms, idle data center GPUs, increasingly AI GPU clusters).
- **OctaneRender integration**: The original killer app — Render's integration with OTOY's OctaneRender bootstrapped the network. Studios submit Blender/3ds Max/Maya scenes; they render on the network.
- **Dispersed AI Compute Subnet**: Dedicated AI compute subnet launched at Solana Breakpoint 2025. The customer-facing brand is Dispersed.com. Targets generative AI model training and inference workloads — the network's pivot from "rendering-only" to "rendering + AI compute."

### Multi-GPU and scaling

Render's architecture allows:

- Multi-GPU node scaling for large renders.
- Real-time rendering for interactive sessions.
- Batch jobs for offline renders.
- ML job types expanded since Dispersed launched in 2025.

### 2025-2026 developments

The network has been expanding beyond rendering:

- **Dispersed launched**: At Solana Breakpoint 2025, the dedicated AI compute subnet went live as Dispersed.com. GPU marketplace grew 87% year-over-year; rendering compute power increased 40%.
- **Governance proposal**: New compute subnet proposal approved at RenderCon 2026.
- **Solana integration**: Aiming to be a "core decentralized compute layer" for the Solana ecosystem.
- **AI alignment**: As AI infrastructure narratives grew in 2025-2026, RENDER benefited from capital rotating into AI-linked crypto assets.

## RNDR token

- **Blockchain**: Solana (SPL token)
- **Supply**: Fixed.burnable
- **Utility**: Payment for GPU compute; provider rewards; governance (via proposals)
- **Market**: Listed on major exchanges; one of the few DePIN tokens with sustained liquidity since 2017.

## Use cases

### 3D rendering (the original use case)

The canonical Render use case: studios render scenes without owning GPU farms.

- **Workflow**: Upload scene → pay in RNDR → distributed to GPU providers → download render.
- **Cost**: Often cheaper than on-prem or cloud farms for episodic work.
- **Quality**: Verified outputs; providers stake RNDR as reputation.

### AI inference and training

Growing but not the primary focus:

- LLM inference on decentralized GPUs.
- Fine-tuning workloads.
- Model serving.

### Cloud gaming (adjacent)

Render is well-suited for cloud gaming streams — low-latency GPU rendering to endpoints. Aethir has stronger cloud gaming focus, but Render's GPU inventory is complementary.

## Comparison

| Dimension | Render | Akash | Phala/dstack | Golem | io.net |
|-----------|--------|-------|--------------|-------|-------|
| Founded | 2017 | 2020 | 2022 | 2017 | 2023 |
| Token | RNDR (Solana) | AKT (Cosmos) | PHA (Substrate) | GLM (ETH) | IO (Solana) |
| Blockchain | Solana | Cosmos | Substrate | Ethereum | Solana |
| Focus | GPU rendering | K8s containers | TEE compute | Generic batch | GPU ML |
| GPU class | Mixed | Mixed | TDX+H100 CC | Limited | Mixed |
| TEE | No | 2026 | Yes | No | No |
| Mainnet | 2017 | 2020 | 2022 | 2017 | 2023 |
| Token age | Oldest | Mid | New | Oldest | New |

## Trade-offs

### Strengths

- **Longest track record** (9+ years) in decentralized GPU compute.
- **Specialization**: GPU rendering is battle-tested, with studios as real customers.
- **Solana ecosystem**: Integration with the broader Solana DePIN narrative.
- **AI alignment**: As AI crypto narratives grew (2024-2026), Render benefited.
- **RNDR liquidity**: One of the few DePIN tokens with sustained exchange listing and volume.

### Limitations

- **No confidential computing**: Provider sees all data. Not suitable for AI prompts requiring privacy.
- **Rendering-specific**: The network is optimized for visual rendering; generic compute is secondary.
- **Centralization risk**: Large render farms dominate supply.
- **No TEE story**: Unlike Phala, no path to confidential AI inference.
- **Solana dependency**: If Solana has issues, Render has issues.

## Attack surface

| Attack | Mitigation |
|--------|------------|
| Provider reads data | No mitigation — full trust. Don't send sensitive data. |
| Provider submits fake renders | Verification; stakeholder reputation. Staking. |
| Sybil providers | Proof-of-work and Proof-of-Time-Lock verifications. |
| Oracle manipulation | Off-chain pricing. Multi-source. |
| Solana congestion | Fee smoothing. |
| Token manipulation | Governance via proposals. |

## Recent developments (2025-2026)

### Dispersed — Dedicated AI Compute Subnet (Breakpoint 2025)

Render's most significant product expansion since OctaneRender integration:

- **Dispersed.com** launched at Solana Breakpoint 2025 as the customer-facing brand for the compute subnet.
- GPU marketplace grew **87%** year-over-year; rendering compute power grew **40%**.
- Targets generative AI model training and inference — the network's explicit pivot from "rendering-only" to "rendering + AI compute."
- At RenderCon 2026 (March 2026): new governance proposal for additional compute subnet, Dispersed node architecture announced.

### RenderCon 2026

March 2026, the RenderCon 2026 full speaker lineup was announced alongside a new governance proposal for a dedicated compute subnet and the Dispersed node architecture.

### RNDR → RENDER Rebranding

The token was rebranded from RNDR to RENDER (SPL token on Solana). Both names appear in wild; this library uses both.

### AI Crypto Narrative Revaluation

As AI infrastructure narratives rotated back into crypto in 2025-2026, RENDER was among the primary beneficiaries among DePIN compute tokens — alongside AKT's 72% YTD surge and Render's own AI-driven revenue growth.

### June 2, 2026 AI Compute Panel

Render joined Nosana, Akash, and Aethir on the "Centralized vs. Decentralized AI Compute" panel on June 2, 2026, reinforcing decentralized GPU compute as a coherent sector.

## Primary sources

- Render Network — [rendernetwork.com](https://rendernetwork.com)
- Documentation — [docs.rendernetwork.com](https://docs.rendernetwork.com)
- GitHub — [github.com/rendernetwork](https://github.com/rendernetwork)
- Blog — [rendernetwork.medium.com](https://rendernetwork.medium.com)
- RNDR token — [coingecko.com/en/coin/render](https://coingecko.com/en/coin/render)
- RenderCon 2025 — [rendernetwork.medium.com/gpu-markets-and-compute-at-rendercon-2025](https://rendernetwork.medium.com/gpu-markets-and-compute-at-rendercon-2025)
- Messari report — [messari.io/report/understanding-io-net-a-comprehensive-overview](https://messari.io/report/understanding-io-net-a-comprehensive-overview)
