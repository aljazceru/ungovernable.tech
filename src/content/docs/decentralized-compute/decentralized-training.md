---
title: "Decentralized Training"
tags:
  - "gensyn"
  - "prime-intellect"
  - "diloco"
  - "decentralized-training"
  - "deep-dive"
  - "ai"
---
*Training large models across geographically distributed, heterogeneous hardware. The hard problem: getting a 70B-parameter model trained without 10,000 GPUs in one datacenter. Two production-direction projects (Gensyn and Prime Intellect) and the algorithmic primitives that make it possible.*

---

## The bandwidth wall

The fundamental tension: training large models requires synchronizing gradients across many GPUs. Naive data-parallel training synchronizes after every step, which needs datacenter-class interconnect (NVLink at terabytes per second). Two GPUs in different cities can communicate at internet bandwidth — orders of magnitude slower.

For a long time this killed decentralized training. The breakthrough has been algorithms that **synchronize less often** without hurting model quality.

---

## DiLoCo and friends

**DiLoCo** (Distributed Low-Communication training, Google DeepMind 2024): instead of synchronizing every step, each worker performs many local optimizer steps and only communicates aggregated weight deltas every `N` steps. The communication-to-compute ratio drops by orders of magnitude.

The insight: with appropriate optimizer choices (Nesterov momentum across the outer loop, AdamW inner) the convergence cost of less-frequent synchronization is small for many model classes.

Variants and follow-ups:

- OpenDiLoCo (Prime Intellect, 2024): open-source DiLoCo implementation.
- INTELLECT-1 (Prime Intellect, 2024): first 10B-parameter model trained across continents using DiLoCo.
- INTELLECT-2 (2025): 32B-parameter follow-up.
- Lo-FI / SWARM-style federated approaches.

These make decentralized training plausible for model sizes that previously required hyperscaler-only infrastructure.

---

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

---

## Gensyn

Position: a decentralized network for ML training where participants get paid for verifiable contributions.

Architecture:

- Solver / verifier model. Solvers train; verifiers spot-check via cryptographic proofs of work.
- Proof of training work. A verifiable claim that a particular update came from a particular dataset and model weights.
- Substrate-based chain for coordination.
- Heterogeneous hardware. Consumer GPUs welcome.

The cryptographic proof-of-training story is what differentiates Gensyn: rather than trusting solver claims about gradients, the protocol can verify them at much lower cost than redoing the training.

Status (2026): Gensyn has been moving from research and testnets toward production. Smaller-scale demonstrations have shipped; frontier-scale runs remain ahead.

---

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

---

## Comparison

| Dimension | Gensyn | Prime Intellect | Hyperscaler training |
|-----------|--------|-----------------|----------------------|
| Verification | Cryptographic proof of work | TEE + optimistic + reputation | Trust the operator |
| Algorithm | Generic; not tied to one optimizer | DiLoCo-family | All-reduce / allgather |
| Scale (2026) | Smaller deployments | INTELLECT-2 (32B) | Hundreds of billions |
| Hardware | Consumer + datacenter | Mostly datacenter-class | Datacenter-only |
| Open weights | Per-contract | Always | Often closed |
| Token model | Yes | Yes | No |

---

## Use cases

### Open-weights frontier model training

Communities pool GPU contributions to train and release open-weights models that beat or match hyperscaler closed models. Prime Intellect's INTELLECT runs are the prototype.

### Sovereign training

A consortium (academic, civic, sovereign-state) wants to train a model without depending on US or Chinese hyperscalers. Decentralized training plus TEE attestation lets them distribute trust across their members.

### Federated learning at internet scale

Privacy-preserving training where each participant's data stays local; only model updates are shared. DiLoCo-class algorithms make this scale; TEE / MPC / FHE add privacy guarantees on top.

### Continual or community fine-tuning

An open-weights base model is fine-tuned by a community on specialized data, with each contributor verifiably credited and rewarded.

---

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

---

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Malicious worker submits fake gradients | Cryptographic proofs, TEE attestation, optimistic challenges |
| Sybil flooding | Stake-weighted contribution; reputation |
| Data-poisoning attacks | Robust aggregation; outlier detection |
| Model exfiltration | Confidential training (TEE / FHE) |
| Token-incentive hacks | Slashing, capped rewards, reputation cooldowns |
| Network-level censorship | Multi-relay coordination; Tor/mixnet underneath |

---

## Recent developments (2024-2026)

- DiLoCo (Google, 2024) provided the algorithmic foundation.
- OpenDiLoCo (Prime Intellect, 2024) gave the open-source implementation.
- INTELLECT-1 (Oct 2024): 10B-parameter model trained decentrally.
- INTELLECT-2 (2025): 32B follow-up.
- Gensyn moves from testnet toward production verifiable training.
- TEE-attested training experiments composing with Phala / Marlin.
- Federated continual learning is a deployed pattern in some industry consortiums.

---

## Related files

- [Overview - Decentralized Compute](/decentralized-compute)
- [Akash](/decentralized-compute/akash)
- [Phala and 0G](/decentralized-compute/phala-and-0g)
- [Bittensor](/decentralized-compute/bittensor)
- [Aethir](/decentralized-compute/aethir)
- [Confidential-AI-Inference](/confidential-computing/confidential-ai-inference)

---

## Primary sources

- Douillard et al., *DiLoCo: Distributed Low-Communication Training of Language Models*, Google DeepMind, 2024.
- Prime Intellect, *INTELLECT-1 Technical Report*, 2024.
- Prime Intellect, *INTELLECT-2 Report*, 2025. [primeintellect.ai](https://primeintellect.ai).
- OpenDiLoCo — [github.com/PrimeIntellect-ai/OpenDiLoCo](https://github.com/PrimeIntellect-ai/OpenDiLoCo).
- Gensyn — [gensyn.ai](https://gensyn.ai); [docs.gensyn.ai](https://docs.gensyn.ai).
- DiLoCo follow-up papers (Lo-FI, SWARM) on arXiv.
- *Federated Learning at Scale*, McMahan et al., 2017.

