---
title: "Decentralized Training"
slug: decentralized-training
type: explainer
pillars: ["compute"]
readiness: experimental
description: "Training large AI models across distributed, heterogeneous hardware over the internet: the techniques, the bandwidth problem and the projects trying it."
dek: "Training large models across geographically distributed, heterogeneous hardware. The hard problem: getting a 70B-parameter model trained without 10,000 GPUs in one datacenter. Two production-direction projects (Gensyn and Prime Intellect) and the algorithmic primitives that make it possible."
updated: 2026-05-12
created: 2026-04-25
origin: vault
source: "04-Decentralized-Compute/Decentralized Training.md"
aliases: ["Gensyn", "Prime Intellect", "DiLoCo"]
tags: ["gensyn", "prime-intellect", "diloco", "decentralized-training", "deep-dive", "ai"]
---

## The bandwidth wall

The fundamental tension: training large models requires synchronizing gradients across many GPUs. Naive data-parallel training synchronizes after every step, which needs datacenter-class interconnect (NVLink at terabytes per second). Two GPUs in different cities can communicate at internet bandwidth — orders of magnitude slower.

For a long time this killed decentralized training. The breakthrough has been algorithms that **synchronize less often** without hurting model quality.

## DiLoCo and friends

**DiLoCo** (Distributed Low-Communication training, Google DeepMind 2024): instead of synchronizing every step, each worker performs many local optimizer steps and only communicates aggregated weight deltas every `N` steps. The communication-to-compute ratio drops by orders of magnitude.

The insight: with appropriate optimizer choices (Nesterov momentum across the outer loop, AdamW inner) the convergence cost of less-frequent synchronization is small for many model classes.

Variants and follow-ups:

- OpenDiLoCo (Prime Intellect, 2024): open-source DiLoCo implementation.
- INTELLECT-1 (Prime Intellect, 2024): first 10B-parameter model trained across continents using DiLoCo.
- INTELLECT-2 (2025): 32B-parameter follow-up.
- Lo-FI / SWARM-style federated approaches.

These make decentralized training plausible for model sizes that previously required hyperscaler-only infrastructure.

## Prime Intellect

Position: open-source decentralized training of frontier models, with a coordination chain and a community of GPU contributors.

Stack:

- OpenDiLoCo for the training algorithm.
- Coordination chain for tracking contributions, attestation, and reward distribution.
- GPU contributor network. Anyone with capable hardware can join.
- Attested workers. TEE attestation is being explored to handle adversarial workers.

Track record:

- INTELLECT-1 (10B params, 2024) trained across distributed contributors.
- INTELLECT-2 (32B params, 2025) scale-up.
- Push toward frontier (70B+) models for 2026.

Why it matters:

- Demonstrates that frontier model training can happen outside hyperscalers.
- Opens the supply side of model creation to communities, not just OpenAI / Anthropic / Google scale.
- Open weights end-to-end.

## Gensyn

Position: a decentralized network for ML training where participants get paid for verifiable contributions.

Architecture:

- Solver / verifier model. Solvers train; verifiers spot-check via cryptographic proofs of work.
- Proof of training work. A verifiable claim that a particular update came from a particular dataset and model weights.
- Substrate-based chain for coordination.
- Heterogeneous hardware. Consumer GPUs welcome.

The cryptographic proof-of-training story is what differentiates Gensyn: rather than trusting solver claims about gradients, the protocol can verify them at much lower cost than redoing the training.

Status (2026): Gensyn's mainnet went live April 22, 2026 on a custom Ethereum rollup (OP Stack), alongside the $AI token launch. The core verification system — **Verde** (cryptographically verifiable ML evaluation) and the **Reproducible Runtime** (bitwise-exact reproducibility across devices) — is deployed in production as **Judge**, a verifiable AI evaluation system that replaces opaque API-based evaluation (e.g., GPT-5 as judge) with open, independently verifiable judgment. The first live application is **Delphi**, an AI-settled prediction market. BlockAssist (AI Minecraft assistant for assistance learning research) was sunset. Galaxy Research published a comprehensive report on decentralized AI training highlighting Gensyn's Judge/Verde system as evidence that verifiable training and evaluation have reached production maturity. Market cap ~$57M (May 2026). Uniswap V3 deployment targeted for Q3 2026.

## The verification problem

Decentralized training has a unique attack: a malicious worker submits fake gradient updates to corrupt the model (or to claim payment without doing the work). Solutions:

### Spot-checking

Verifiers redo a small fraction of work to catch obvious cheating. Cheap but not sound against sophisticated attacks.

### Cryptographic proofs

Compute a SNARK over the training step, proving "given these weights and this data sample, the gradient is X". Pure math, but currently impractical at frontier-model scale (proving overhead too high).

### TEE attestation

A worker runs training in a TEE; attestation pins the binary; the binary is audited; therefore the gradient comes from honest training. Practical today; trades hardware-vendor trust for cryptographic verification.

### Replay-based verification

A random subset of steps is replayed by independent workers; consensus on output. Works in honest-majority models.

### Optimistic plus slashing

Workers submit gradients; a challenge period follows; another worker can challenge with proof of incorrect computation. Stake gets slashed if the challenge succeeds.

Gensyn's proof-of-training-work falls in the cryptographic / replay-based category. Prime Intellect leans optimistic plus TEE-based.

## Comparison

| Dimension | Gensyn | Prime Intellect | Hyperscaler training |
|-----------|--------|-----------------|----------------------|
| Verification | Cryptographic proof of work | TEE + optimistic + reputation | Trust the operator |
| Algorithm | Generic; not tied to one optimizer | DiLoCo-family | All-reduce / allgather |
| Scale (2026) | Smaller deployments | INTELLECT-2 (32B) | Hundreds of billions |
| Hardware | Consumer + datacenter | Mostly datacenter-class | Datacenter-only |
| Open weights | Per-contract | Always | Often closed |
| Token model | Yes | Yes | No |

## Use cases

### Open-weights frontier model training

Communities pool GPU contributions to train and release open-weights models that beat or match hyperscaler closed models. Prime Intellect's INTELLECT runs are the prototype.

### Sovereign training

A consortium (academic, civic, sovereign-state) wants to train a model without depending on US or Chinese hyperscalers. Decentralized training plus TEE attestation lets them distribute trust across their members.

### Federated learning at internet scale

Privacy-preserving training where each participant's data stays local; only model updates are shared. DiLoCo-class algorithms make this scale; TEE / MPC / FHE add privacy guarantees on top.

### Continual or community fine-tuning

An open-weights base model is fine-tuned by a community on specialized data, with each contributor verifiably credited and rewarded.

## Trade-offs

### Strengths

- Breaks the hyperscaler monopoly on frontier-model training.
- Communities can train models that align with their values rather than corporate ones.
- Algorithmic progress is real. DiLoCo-class methods cut communication 100x with small quality cost.
- Open weights by default in most projects.

### Limitations

- Still bandwidth-limited at the highest scales.
- Verification overhead in cryptographic and TEE approaches.
- Coordination complexity beats traditional cloud at small scale.
- Frontier scale is still elusive. INTELLECT-2's 32B is impressive but small compared to commercial frontiers.
- Token incentive design is hard; bad incentives produce bad-faith workers.

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Malicious worker submits fake gradients | Cryptographic proofs, TEE attestation, optimistic challenges |
| Sybil flooding | Stake-weighted contribution; reputation |
| Data-poisoning attacks | Robust aggregation; outlier detection |
| Model exfiltration | Confidential training (TEE / FHE) |
| Token-incentive hacks | Slashing, capped rewards, reputation cooldowns |
| Network-level censorship | Multi-relay coordination; Tor/mixnet underneath |

## Recent developments (2024-2026)

- DiLoCo (Google, 2024) provided the algorithmic foundation.
- OpenDiLoCo (Prime Intellect, 2024) gave the open-source implementation.
- INTELLECT-1 (Oct 2024): 10B-parameter model trained decentrally.
- INTELLECT-2 (2025): 32B follow-up; Prime Intellect's arXiv paper (`arXiv:2505.07291`) frames it as a reasoning model trained through globally decentralized reinforcement learning, with `prime-rl`, TOPLOC rollout validation, and SHARDCAST weight broadcasting.
- **Prime Intellect $130M Series A (July 8, 2026)**: Led by Intel Capital, with Founders Fund and others. Funds the "Open Superintelligence Stack."
- **Prime Agent (August 5, 2026)**: Open-sourced self-improving coding harness — 95.5% on ARC-AGI-3 (above human baseline 95.4%). Built on Recursive Language Model (RLM) abstraction with Continual Harness architecture. MIT-licensed.
- **Multi-Agent Systems in PRIME-RL (August 7, 2026)**: RL stack expanded to support arbitrary multi-agent interactions, with verifiers `0.3.0` and prime-rl `0.8.0`. Agents can communicate within "nuclear family" scope (parent/sibling/child).
- **Scaling Agentic RL (July 22, 2026)**: Demonstrated RL training at 365,000+ parallel environments across SWE, Terminal, and Search tasks.
- **verifiers v1 (July 10, 2026)**: Modular component library for RL environments and LLM agent training.
- **NVIDIA Nemotron Coalition (June 4, 2026)**: Prime Intellect joined to advance open frontier models; post-training of Nemotron 3 on the Lab platform.
- **Customer deployments**: Zapier (AutomationBench as continuous agent improvement loop); Ramp (RL beating frontier models at spreadsheet search).
- Gensyn Mainnet + $AI token launch (April 22, 2026) on Ethereum rollup (OP Stack).
- Gensyn **Judge/Verde** verifiable AI evaluation system live in production; **Delphi** AI-settled prediction market live on testnet.
- Gensyn BlockAssist (AI Minecraft assistant) sunset; RL Swarm, CodeAssist paused. Focus shifted to Judge/Delphi/Verde verification stack.
- Gensyn's `rl-swarm` remains a useful open-source artifact (GitHub API 2026-05-05: 1,691 stars, 620 forks, MIT).
- Prime Intellect's active codebases are moving quickly (GitHub API 2026-05-05: `PrimeIntellect-ai/prime-rl` 1,338 stars, pushed 2026-05-05; `PrimeIntellect-ai/prime` 193 stars, pushed 2026-05-04).
- TEE-attested training experiments composing with Phala / Marlin.
- Federated continual learning is a deployed pattern in some industry consortiums.

## Primary sources

- Douillard et al., *DiLoCo: Distributed Low-Communication Training of Language Models*, Google DeepMind, 2024.
- Prime Intellect, *INTELLECT-1 Technical Report*, 2024.
- Prime Intellect, *INTELLECT-2: A Reasoning Model Trained Through Globally Decentralized Reinforcement Learning*, 2025. [arXiv:2505.07291](https://arxiv.org/abs/2505.07291) | [Launch blog](https://www.primeintellect.ai/blog/intellect-2) | [prime-rl](https://github.com/PrimeIntellect-ai/prime-rl) | [prime](https://github.com/PrimeIntellect-ai/prime).
- OpenDiLoCo — [github.com/PrimeIntellect-ai/OpenDiLoCo](https://github.com/PrimeIntellect-ai/OpenDiLoCo).
- Gensyn — [gensyn.ai](https://gensyn.ai); [Testnet docs](https://docs.gensyn.ai/testnet); [rl-swarm](https://github.com/gensyn-ai/rl-swarm).
- DiLoCo follow-up papers (Lo-FI, SWARM) on arXiv.
- *Federated Learning at Scale*, McMahan et al., 2017.
