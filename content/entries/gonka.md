---
title: "Gonka"
slug: gonka
type: deep-dive
pillars: ["compute"]
readiness: experimental
description: "Gonka, an experimental Layer 1 that redesigns proof-of-work around transformer computation so that mining produces useful AI inference."
dek: "A Cosmos-SDK L1 that rebuilds Proof-of-Work around transformer mathematics — the competitive \"Sprint\" proof phase occupies miners ~10 minutes per cycle, then the same hardware is released for paid AI inference and training. The first credible attempt at useful-proof-of-work at inference scale, independently measured at #2 among all tracked decentralized-AI networks — and still pre-production in stability terms."
updated: 2026-08-25
created: 2026-08-25
origin: vault
source: "04-Decentralized-Compute/Gonka.md"
aliases: ["Gonka Network", "GNK"]
tags: ["gonka", "gnk", "proof-of-work", "useful-work", "inference", "decentralized-compute", "deep-dive"]
---

## Position

Gonka's thesis: Bitcoin's security model (PoW, permissionless entry, no stake required) but with the work being **useful AI computation** instead of hash lotteries. Where Bittensor pays stakers ~60% of rewards and Akash/io.net are marketplaces, Gonka directs **100% of rewards to GPU providers** for verified inference work:

| Parameter | Gonka | Bittensor |
|---|---|---|
| Model | Single inference network, vertical efficiency | 128+ subnet marketplace |
| Consensus | Sprint (PoW 2.0) | Yuma Consensus (PoS-family) |
| GPU reward share | **100%** | ~40% |
| Entry barrier | Hardware only (~$35K H100) | Hardware + $1–5M TAO stake |
| Exchanges | OTC (SafeTrade) | Coinbase, Kraken, Binance |
| Backing | ~$80M (Coatue, **Bitfury $50M**) | Public markets |

The Bitfury investment (Dec 2025) is the signal that matters: a Bitcoin-mining incumbent concluding that GPU-PoW-for-inference is the closest living relative of its own business model. CEO Val Vavilov: the model "channels hardware power directly toward productive AI workloads, which aligns perfectly with Bitfury's mission to support open, resilient, and high-impact digital infrastructure."

## Architecture

### Sprint — Proof-of-Work 2.0

- Miners ("Hosts") connect GPUs (H100, A100, Blackwell; eventually ASICs) and compete in a **~10-minute Sprint cycle** on a **2.3B-parameter transformer** — the competitive proof phase.
- Outside the Sprint window, the same hardware serves **paid workloads**: inference (Kimi K2.6, MiniMax M2.7, DeepSeek V4 Flash are the flagship models) and training.
- Verification: results checked by validators via cryptographic proofs of compute; the L1 records balances, transactions, and the cryptographic artifacts proving Hosts performed AI work correctly. All computation happens off-chain.
- Whitepaper goal: **near-100% of network compute toward training and inference** instead of consensus busywork — against >90% of GPU cycles consumed by consensus in typical PoS networks (per Bitfury's announcement framing).

### Governance — Proof-of-Compute-weighted voting

- Voting power ∝ verified compute contribution (PoC).
- 20% of PoC-derived voting weight activates automatically; the remaining 80% unlocks only by locking GNK as collateral — influence requires **real compute work + economic skin in the game**.
- Inference pricing is miner-votable on-chain: the launch rate has held flat at **$0.000314 per million tokens** (pricepertoken), an order of magnitude below mainstream API pricing. Heavy Kimi-model volume loading GPUs is expected to force the pricing vote.

### Token (GNK)

- Payments for compute, validator staking, governance.
- OTC only (SafeTrade; HeX orderbook DEX) — no tier-1 listing yet. Market cap ~$80M class (early stage).

## Measured Output — the DeAI Dashboard numbers

The reason Gonka earns a vault note now is independent measurement:

- **72.34B tokens/day across 626 GPUs** — **#2 among all tracked entities** (behind only Bittensor's Chutes at 425B), **#1 among standalone networks**, roughly matching io.net's 71.45B on a fraction of the silicon (io.net's B200 index: 402.20 vs Gonka's 626 tracked GPUs).
- Institutional backing alongside a CertiK audit; Bitfury's $50M (Dec 2025) plus Coatue.
- ~6,000 H100-equivalent GPUs aggregated in the first months post-mainnet (mainnet: August 2025).
- Dashboard readings are volatile (~10% week-over-week swings) — appropriate for a network still in rewrite.

## Trade-offs

### Strengths

- **The useful-PoW thesis, live.** Nobody else has Bitcoin-style permissionless security and measured inference output in one system. No stake-to-participate means GPU owners enter with hardware alone — the lowest-capital permissionless entry in the sector.
- **Radical price transparency.** Flat, governance-set $0.000314/M tokens is test-level pricing for production inference; pricepertoken tracks it independently.
- **Reward integrity.** 100% of rewards to compute providers (vs ~40% Bittensor) removes the staker-over-miner extraction that Bittensor critics highlight.
- **Independently measured.** Throughput claims are checkable against the DeAI Dashboard, not just marketing.

### Limitations

- **Pre-production stability.** A January 2026 flaw in the original Sprint design let Hosts **overstate hardware capacity**; the fix grew into a **ground-up rewrite that is well advanced but unfinished**. Track record is the thinnest of any top-5 tracked network (mainnet Aug 2025).
- **Dynamic pricing unbuilt.** The whitepaper's dynamic pricing model remains unimplemented; flat-rate pricing is sustainable only while test-level demand subsidizes it.
- **Liquidity and access.** OTC-only GNK; no tier-1 exchange; no US/EU retail on-ramp.
- **Verification depth.** Validator-checked cryptographic proofs of compute are weaker than optimistic-verification + fraud proofs (Gensyn) or TEE attestation (Phala) for workloads where correctness of *reasoning* (not just execution) matters.
- **Model narrowness.** A handful of flagship open models vs 128+ specialized Bittensor subnets.

## Attack surface

- **Capacity fraud** — the January class of bugs: hosts claiming hardware they don't operate. The Sprint rewrite is the systemic fix; watch its audit trail.
- **Consensus-period capture** — a coalition dominating Sprint cycles could gate paid-work allocation; PoC-weighted governance concentrates influence in large farms.
- **Underpriced inference race** — if the pricing vote keeps rates near $0.000314/M, host economics may only work for subsidization-phase actors; the network needs the dynamic-pricing mechanism to survive demand maturation.
- **Single-verification path** — no fraud-proof game or TEE redundancy yet; a validator-collusion event has no secondary check.

## Use cases

### Cheapest measured inference in the sector
Flat $0.000314/M tokens for flagship open models (Kimi K2.6-class) — for bulk, non-sensitive, throughput-bound workloads where correctness risk is tolerable.

### Useful-PoW mining
Bitcoin-familiar operators (Bitfury's lineage) repurposing GPU fleets: hardware-only entry, no token purchase required, rewards proportional to verified useful work.

### Sovereignty angle
Permissionless, stake-free GPU provision with governance set by compute contribution rather than capital — structurally the closest thing to "Bitcoin for AI compute." The censorship-resistance depends on the rewrite landing and validator decentralization actually materializing; treat as thesis-in-progress.

## Evidence at a glance

| Claim | Evidence | Date | Source |
|---|---|---|---|
| 72.34B tokens/day, #1 standalone | DeAI Dashboard measurement | Aug 2026 | [Crypto Daily/Binance](https://www.binance.com/en/square/post/355561392608274) |
| $50M Bitfury investment | VentureBeat announcement; Vavilov quote | Dec 2025 | [VentureBeat](https://venturebeat.com/business/bitfury-announces-50-million-investment-in-gonkaa-decentralized-network-for-highefficiency-ai-compute) |
| ~6,000 H100-equivalents post-launch | Network aggregation claim | 2025–2026 | [hot-labs summary](https://hot-labs.org/blog/what-is-gonka-ai-decentralized-network-for-ai-computations) |
| $0.000314/M tokens flat since launch | pricepertoken tracking | Aug 2026 | via Crypto Daily |
| Sprint capacity-overstatement flaw → rewrite | January 2026 incident; "stability short of production" | Jan–Aug 2026 | [Crypto Daily](https://www.binance.com/en/square/post/355561392608274) |
| 100% rewards to GPU providers | Protocol design vs Bittensor ~40% | 2026 | [joingonka comparison](https://joingonka.ai/en/knowledge/gonka-vs-bittensor) |

## Primary sources

- Gonka — [gonka.ai](https://gonka.ai); FAQ — [gonka.ai/docs/FAQ](https://gonka.ai/docs/FAQ).
- GitHub — [github.com/gonka-ai](https://github.com/gonka-ai).
- Bitfury investment — [VentureBeat](https://venturebeat.com/business/bitfury-announces-50-million-investment-in-gonkaa-decentralized-network-for-highefficiency-ai-compute) (Dec 2025).
- DeAI Dashboard coverage — [Crypto Daily via Binance Square](https://www.binance.com/en/square/post/355561392608274) (Aug 14, 2026).
