---
title: "Decentralized Compute"
slug: decentralized-compute
type: explainer
pillars: ["compute"]
description: "Permissionless markets for CPU and GPU time: how decentralized compute networks work, how they handle trust, and where capacity is real or token-driven."
dek: "Permissionless markets for CPU, GPU, and (increasingly) confidential-GPU time. The supply side of an internet where you can rent computation without a cloud account, and — when combined with TEEs — without trusting the node operator."
updated: 2026-06-16
created: 2026-04-17
origin: vault
source: "04-Decentralized-Compute/Overview - Decentralized Compute.md"
aliases: ["DePIN Compute", "P2P Compute"]
tags: ["decentralized-compute", "akash", "golem", "render", "phala", "bacalhau", "confidential-inference", "aethir", "nosana", "gensyn"]
---

## Why decentralize compute

- No account gatekeeping. Sanctioned, under-banked, or pseudonymous users can pay in crypto and get compute.
- Provider diversity. Side-steps concentration risk (three hyperscalers run most of the world's inference).
- Price discovery. Idle GPUs from gamers, universities, and miners can be priced at marginal cost, beating hyperscaler margins for some workloads.
- Confidential by default. Combining decentralized compute with TEEs and attestation means the node operator can't read prompts and can't steal the model — a trust model no centralized cloud offers.

## Major networks

| Network | Focus | Tech | Confidential |
|---|---|---|---|
| [Akash](/kb/akash/) | General K8s workloads | Cosmos SDK; reverse-auction; GPU support 2024+ | AEP-65 (TEE) live May 2026 |
| [Golem](/kb/golem/) | Task-based CPU compute | Long-running; generic tasks; GLM on ETH/Polygon | No |
| [Render Network](/kb/render-network/) | GPU rendering / ML | RENDER on Solana; OctaneRender; Dispersed AI compute 2025+ | No |
| [io.net](/kb/io-net/) | GPU aggregation for ML | Solana; aggregates Render/Filecoin/consumer GPUs | No |
| Fluence | Serverless WASM compute | Rust/Aqua; IPC Arbitrum Orbit L2; USDC payments; FLT staking | TEE roadmap 2026 |
| [Bacalhau and Compute-over-Data](/kb/bacalhau/) | Compute-over-data orchestration | Go single binary; Docker/WASM; IPFS/S3/HTTP/local sources |
| [Phala and 0G](/kb/phala-and-0g/) | TEE marketplace / AI OS | TDX + H100 CC; on-chain attestation; Ethereum L2 (Nov 2025) | Yes (native) |
| Marlin Oyster | CVM marketplace | Nitro + TDX + H100 CC | Yes |
| Nosana | AI inference | Solana-based GPU grid; production workload focus in 2025 |
| [Decentralized Training](/kb/decentralized-training/) | Gensyn / Prime Intellect | Proofs of training work; DiLoCo / asynchronous RL |
| [Bittensor](/kb/bittensor/) | Token-incentivized AI subnets | Validator scoring and Yuma consensus |
| [Aethir](/kb/aethir/) | Enterprise GPU cloud | ATH token; Strategic Compute Reserve |

## Patterns

### Raw compute (non-confidential)

Akash, Golem, Render. Suitable for open workloads (rendering, public model inference, batch jobs) where the provider seeing the data doesn't matter.

Akash 2025-2026 changes:

- Homenode Early Access (May 2026): average users with RTX 4090/5090 can now participate as providers.
- **$5M monthly compute spend** crossed in Q1 2026.
- BME (Burn-Mint Equilibrium) went live March 23, 2026 — every compute transaction burns AKT.
- AkashML processing **1.7B tokens/day** on OpenRouter (November 2025 launch).
- NVIDIA H200 nodes added to the GPU waitlist.
- AEP-65: Confidential Computing with TEE (target July 2026).
- AEP-29: Hardware Verification using Trusted Execution — providers prove CPU/GPU specs via attestation (live).
- Lease-to-lease networking: dynamic IP address management between tenant workloads.
- Akash Agents: one-click AI agent deployments on decentralized compute.

### Confidential compute

Phala, Marlin, Oasis ROFL, Automata, and Fluence run workloads inside TEEs on community-operated nodes. On-chain smart contracts verify attestation quotes before a job is considered valid and paid. This is how you get:

- Private inference on open-weights LLMs without trusting any cloud (Tinfoil sits adjacent; Phala is the canonical on-chain version).
- Verifiable off-chain computation for smart contracts (oracles).
- Private DeFi strategies, private order matching.

2025-2026 TEE confidential AI work:

- Phala: **10,004 total users, 398 paid, 2,529 CVMs, 3.05B tokens/day peak** (end-2025 report).
- OLLM + Phala: confidential AI gateway launched December 2025; drop-in OpenAI-compatible API with verifiable TEE attestation.
- Phala + 0G: Phala's TEE SDK integrated into 0G's decentralized AI Operating System for confidential inference.
- Phala + Venice AI: end-to-end encrypted AI inference mode launched — prompts encrypted on device, stay encrypted in transit, decrypted only inside the TEE.
- Phala + ai16z: TEE technology integrated into the Eliza AI Agent framework (Q4 2024).
- Phala + NeurochainAI: partnership supplying GPU TEE compute infrastructure.
- Akash AEP-65: Confidential Computing with TEE (target: July 2026).
- Akash AEP-29: Hardware Verification using Trusted Execution for provider attestation (live).
- NVIDIA H100 CC now production-grade on Phala.

See [Confidential-AI-Inference](/kb/confidential-ai-inference/) and [NVIDIA-GPU-TEE](/kb/nvidia-gpu-tee/).

### Verifiable compute without TEEs

Gensyn, RISC Zero, and Succinct use cryptographic proofs (ZK or optimistic challenges) to prove compute was performed correctly without TEEs. Slower, but no hardware trust required.

2025-2026 Gensyn work:

- ICLR 2026 workshop hosted on open problems in decentralized training.
- Testnet dashboard showing contributor stats.
- On-chain identity tracking node progress.
- Collaborative foundation models via local assistants.

### Compute-over-data

Bacalhau moves the job to the data rather than moving the data to the job. This is a different axis from raw GPU rental: it is most useful when the scarce resource is not H100 time but bandwidth, egress budget, locality, or data-sovereignty constraints. Bacalhau's current stack is a Go single-binary orchestrator with Docker/WASM execution and IPFS/S3/HTTP/local data sources; the strongest deployments are controlled distributed fleets, Filecoin/IPFS jobs, edge analytics, and DuckDB-style partitioned queries. Natural fit for ZK, FHE, or TEE privacy layers. See [Bacalhau and Compute-over-Data](/kb/bacalhau/).

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

## Recent developments (2025-2026)

### Akash — Confidential Computing Live, BME, Homenode, 500K AKT Burned

- **AEP-65 Confidential Computing: Live May 19, 2026.** Provider operators cannot read tenant workloads inside TEE. AEP-29 (Hardware Verification) already live. This eliminates the primary trust gap separating Akash (trust the provider) from Phala/Marlin (TEE-attested).
- **BME (Burn-Mint Equilibrium)**: Live March 23, 2026. Every compute lease burns AKT, producing ACT stablecoin for providers. Crossed **$5M monthly compute spend** in Q1 2026. As of May 26, 2026: **500,000 AKT burned** via BME — direct on-chain evidence of real compute usage translating to token deflation.
- **Homenode Early Access**: Live May 2026. Average users with RTX 4090/5090 can now participate as providers.
- **Akash Agents Platform**: One-click AI agent deployments on decentralized compute. Built by community member Sandeep Narahari, powered by AkashML inference (OpenAI-compatible API).
- **AkashML**: Processing **1.7 billion tokens/day** on OpenRouter (November 2025 launch).
- **Mainnet 18 (June 11, 2026)**: Resource Reclamation (AEP-82) — graceful lease exit with on-chain escrow; Oracle v2 — wall-clock timestamps for deterministic staleness detection and TWAP.
- **Razer $0.01/image**: Partnership demonstrating Akash's cost advantage in image generation workloads.

### Phala — Ethereum L2 Migration (November 2025), TEE Confidential AI

- **Polkadot → Ethereum L2**: Community-approved migration completed November 19, 2025. PHA → vPHA (ERC-20, 1:1). Phala L2 = execution layer for GPU/TDX confidential compute; Ethereum L1 = staking and governance.
- **Ethereum ecosystem integration**: Access to the largest smart contract ecosystem, tooling, and enterprise integrations.
- **2025 metrics**: 10,004 total users, 398 paid, 2,529 CVMs, 3.05B tokens/day peak (end-2025).
- **dstack SDK**: Docker-compose-style TDX confidential VMs with on-chain attestation.

### Aethir — $260M Enterprise Deal, 2,304 B300 GPUs

- **Largest decentralized GPU contract in history**: Axe Compute (NASDAQ: AGPU) signed a **$260 million multi-year enterprise contract** centered on a **2,304-GPU NVIDIA B300 Blackwell cluster** powered by Aethir's decentralized GPU cloud.
- Qualitatively different from prior enterprise adoption: a public NASDAQ-listed company committing $260M to decentralized infrastructure for AI workloads — not a pilot or DePIN-native company.
- **ATH Strategic Compute Reserve** model continues to attract institutional interest (Predictive Oncology was first public-company treasury participant).
- **Aethir AI Compute Panel** on June 2, 2026 brought together Nosana, Akash, Aethir, and io.net for a live discussion on centralized vs. decentralized AI compute.

### io.net — Dell Technologies Partnership, 30,000+ GPUs

- **Dell Technologies Authorized Partner and Cloud Service Provider** — the partnership merges io.net's decentralized GPU network with Dell's hardware and enterprise sales channel.
- **Additional partnerships**: Creator.Bid (image model scaling), Alpha Network (secure decentralized AI/Web3 environment), Mira Network (strategic AI landscape partnership).
- **Production metrics**: Wondera ($2.48M savings vs AWS, 552,000 GPU hours, 96 GPUs including 64 H100s + 32 H200s); Leonardo.Ai (scaled from 14K to 19M users, 50%+ cost reduction vs AWS).
- Platform claim: **30,000+ GPUs** available, up to 70% lower cost than AWS.

### Fluence — Instant GPU Access Live, FLT Grid League

- **GPU Containers/VMs now instant-access** (June 2026): No waitlist, direct access via Fluence Console for GPU Containers, VMs, and Bare Metal deployments. USDC pricing on Arbitrum Orbit L2.
- **GPU Auction**: New price discovery mechanism for compute capacity, demonstrated at SuperAI Conference (Singapore, June 2026).
- **FLT Grid League**: Trading competition on Gate.io with 3,000 USDC prize pool — tying FLT liquidity to speculative volume.
- **DAO governance migrated** to native Token App (flt.fluence.network/governance) from Tally.
- SuperAI Conference (June 2026): booth showcasing GPU cluster availability alongside io.net.

### Render Network — Dispersed AI Compute Subnet (Breakpoint 2025)

- **Dispersed.com** launched at Solana Breakpoint 2025 as the AI compute subnet. GPU marketplace grew 87% YoY; rendering compute power grew 40%.
- **RenderCon 2026**: New governance proposal for additional compute subnet, Dispersed node architecture.
- **Token rebrand**: RNDR → RENDER (Solana SPL token).
- **AI narrative tailwind**: Among primary beneficiaries of 2025-2026 AI crypto sector rotation alongside AKT's 72% YTD surge.

### Decentralized Compute Market Context (2026)

- DePIN combined market cap: ~$19-20B across ~250 projects (CoinGecko, 2026).
- On-chain revenue: ~$150M/month across leading DePIN networks (January 2026).
- DePIN GPU compute crossed **$200M+ annualized protocol revenue** in early 2026.
- Hyperscaler GPU cost pressure: H100 at $7.90+/hour on AWS vs. decentralized alternatives at significant discounts.
- xAI Colossus: 555,000 GPUs as of January 2026, roadmap to 1M — single largest AI compute concentration, illustrating why decentralized GPU markets remain structurally relevant.
- **Greg Osuri's energy constraint argument**: Northern Virginia projected to fall out of electricity reliability standards by June 2027; agents consume 10–40x more tokens than human-to-AI interaction; local energy + peer-to-peer compute on home meshes is the path that doesn't require building new power plants.

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

## Attack surface

- Malicious node operator. The whole reason to use TEEs and attestation. Without them, the operator is fully trusted.
- Sybil attacks on reputation systems.
- Stake-grinding and free-rider attacks on proof-of-compute schemes.
- Oracle compromises. If off-chain data feeding on-chain payments is wrong, the whole market distorts.
- Network splits. Partitioned verifiers may accept inconsistent attestation collateral.

## Primary sources

- Akash — `akash.network/docs` | [2026 Roadmap](https://akash.network/roadmap/2026/)
- Bacalhau — [Docs](https://bacalhau.org/docs/) | [GitHub](https://github.com/bacalhau-project/bacalhau) | [IPFS CoD docs](https://docs.ipfs.tech/concepts/cod/)
- Phala Cloud / dstack — `phala.network` | [0G Partnership](https://www.bitget.com/news/detail/12560604458724)
- Marlin Oyster — `docs.marlin.org`
- Oasis ROFL — `docs.oasis.io/build/rofl`
- Gensyn — [gensyn.ai](https://www.gensyn.ai) | [Contribute](https://www.gensyn.ai/contribute) | [ICLR 2026](https://x.com/gensynai/highlights)
- Nosana — `nosana.com` | [Blog](https://nosana.com/blog/)
- Aethir — `aethir.com` | [Strategic Roadmap](https://ecosystem.aethir.com/blog-posts/aethirs-12-month-strategic-roadmap-supercharging-enterprise-ai-compute-growth)
- 0G — `0g.ai`
- Render Network — `rendernetwork.com`
- io.net — `io.net`

Continue with [Compare decentralized compute platforms](/kb/compare-decentralized-compute/).
