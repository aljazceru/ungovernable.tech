---
title: "Verifiable Delay Functions (VDFs)"
slug: verifiable-delay-functions
type: explainer
pillars: ["cryptography"]
description: "Verifiable delay functions take a fixed amount of sequential time to compute but are quick to verify: constructions and uses in randomness beacons."
dek: "A function whose evaluation requires a prescribed amount of sequential work — no parallel speedup — but whose output is fast to verify. The point is to force the passage of real wall-clock time onto an output that everyone can check cheaply."
updated: 2026-04-26
created: 2026-04-26
origin: vault
source: "02-Cryptography/VDFs.md"
aliases: ["VDF", "Verifiable Delay Function"]
tags: ["vdf", "randomness", "sequentiality", "cryptography", "deep-dive"]
---

## What sequentiality means

A VDF is a triple `(Setup, Eval, Verify)`:

- `Setup(λ, T) → pp` — public parameters bound to a delay `T`.
- `Eval(pp, x) → (y, π)` — produces the output `y` after roughly `T` sequential steps.
- `Verify(pp, x, y, π) → {accept, reject}` — runs in `polylog(T)` time.

Two adversarial properties:

1. **Sequentiality.** No algorithm with `poly(λ)` parallel processors can produce `y` in significantly fewer than `T` sequential steps.
2. **Uniqueness / soundness.** For each `x`, only one `y` accepts under any proof.

The first property is what makes the primitive distinct from a VRF or hash chain: even an attacker with unlimited cores cannot rush ahead. The second is what makes the output committing.

Boneh, Bonneau, Bünz, Fisch, *Verifiable Delay Functions*, CRYPTO 2018.

## Why VDFs exist

Public randomness suffers from a *last-revealer* problem. If validators contribute entropy in sequence, the final contributor sees what everyone else committed and can choose to publish or withhold their share to bias the output. A VDF applied to the aggregate makes this attack expensive: by the time the last contributor knows the resulting `y`, the deadline for influencing the round has long passed.

Equivalent framing: a VDF is a slow, public hash that no one can precompute.

See [VRFs](/kb/verifiable-random-functions/) for the complementary primitive (unbiasable, but the keyholder chooses when to publish).

## Constructions

### Pietrzak (2018)

Pietrzak, *Simple Verifiable Delay Functions*, ITCS 2019 (preprint 2018). Uses repeated squaring in an RSA group with hidden order:

```
y = x^(2^T) mod N        # sequential: T squarings
```

The proof is a recursive halving where the prover commits to mid-points. Verification cost is `O(log T)` group operations. Soundness rests on the *low-order* assumption (no efficiently-findable element of low order in the group).

### Wesolowski (2018, EUROCRYPT 2019)

Wesolowski, *Efficient Verifiable Delay Functions*, EUROCRYPT 2019. Same `y = x^(2^T) mod N` form, but with a more compact proof:

```
ℓ = Hprime(x, y)         # prime challenge
q = floor(2^T / ℓ)
π = x^q mod N
verify: π^ℓ · x^(2^T mod ℓ) =? y
```

Proof is a single group element (typically ~256 bytes for a 2048-bit RSA group). Soundness rests on the *adaptive root* assumption.

Both constructions need a group whose order is not known to participants. Two options:

| Group | Setup | Trust |
|-------|-------|-------|
| RSA group `Z/NZ*` | Trusted setup picks `N = pq` | Trusted to delete factors, or MPC ceremony |
| Class groups of imaginary quadratic orders | Discriminant only, no trapdoor | Transparent setup; computation is slower per step |

Class-group VDFs (Chia) avoid the trusted setup at the cost of more expensive squarings.

### MinRoot (Ethereum, dropped)

Khovratovich, Maller, Bhat, *MinRoot: Candidate Sequential Function for Ethereum VDF*, 2022. Iterated low-degree permutation `x ← (x + c)^(1/5)` over a prime field. Designed to be ASIC-resistant by reducing the gap between general-purpose silicon and custom hardware to a small constant. Ethereum considered MinRoot for randomness post-merge but **shelved** the integration in 2023 after analysis showed:

- The expected ASIC speedup over commodity silicon was larger than initially modeled.
- The economic incentive to build a single-purpose ASIC and capture MEV from biased randomness outweighed the cost.

Status as of 2026: Ethereum continues to use RANDAO without a VDF backstop. MinRoot lives on as a research target.

### Other candidates

- **Sloth** (Lenstra, Wesolowski, 2015): pre-VDF construction, modular square-root iterations. Uniqueness only, not sequentiality in the modern sense.
- **Isogeny-based VDFs** (De Feo et al.): post-quantum candidate, large parameters.

## Applications

### Ethereum RANDAO post-merge debate

RANDAO is a commit-reveal aggregation of validator-supplied entropy. Each round's last proposer can choose to publish their reveal or skip; the latter means losing block rewards but biasing the next epoch's randomness slightly. A VDF applied to the RANDAO output would close this attack window. The MinRoot effort was the closest Ethereum came to deploying one. As of 2026, no VDF is in the production protocol; `mix_hash` continues to derive from RANDAO alone.

### Filecoin

Filecoin uses a "wall-clock proof" called WinningPoSt that combines proof-of-replication with leader election. Some early Filecoin design documents proposed a VDF for tie-breaking; the production protocol uses simpler sortition.

### Chia proof-of-time

Chia's Nakamoto-style consensus pairs proof-of-space (storage commitment) with proof-of-time (a class-group VDF). Each block requires a VDF chain of computed length determined by the prevailing space proof. The "Timelord" role runs the VDF; it's permissionless but rewards the fastest implementation. Production deployment since 2021. The fastest Timelords reach roughly 200,000–250,000 squarings/sec on optimized FPGA/ASIC builds (community reports, varying).

### League of Entropy and randomness beacons

The League of Entropy (drand) produces a publicly-verifiable threshold-BLS beacon every 30 seconds. It does not use a VDF directly but composes well with one: clients that need unpredictable-future randomness combine the beacon output with a VDF computed over their own input, ensuring no party can precompute the resulting value.

### Time-lock encryption

A ciphertext that can only be decrypted after `T` sequential operations. Drand's *timelock* feature (since 2023) uses BLS-based identity-based encryption against future beacon rounds; it relies on the beacon's liveness rather than a VDF. True VDF-based time-lock encryption is research-grade — see Malavolta and Thyagarajan, *Homomorphic Time-Lock Puzzles and Applications*, CRYPTO 2019.

## Hardware ASIC race

VDFs are interesting precisely because their security argument depends on the gap between an honest evaluator and the fastest possible attacker being small. This invites a hardware race:

- **VDF Alliance** (Ethereum Foundation, Protocol Labs, others, 2019–2022) funded ASIC research to bound the gap.
- Chia funded its own Timelord optimization community.
- Class-group VDFs are slower per step than RSA VDFs, partially offsetting ASIC gains because the irregular arithmetic is harder to pipeline.

The unsolved tension: any deployed VDF creates an incentive to build dedicated silicon. If a single party owns the fastest ASIC by a wide margin, sequentiality fails in practice even if the math holds.

## Trade-offs

### Strengths

- Bias-free: combines with any commit-reveal or beacon to remove last-revealer power.
- Public, fast verification.
- Composable: a VDF on top of a VRF or beacon stacks cleanly.

### Limitations

- Hardware sensitivity. The whole security argument depends on no attacker having a much faster evaluator than the honest one.
- Trusted setup (RSA variants) or expensive setup (class groups).
- Latency. By definition, a VDF imposes wall-clock delay; whether the application can absorb this matters.
- No post-quantum candidate is production-ready.
- Energy. Sequential squaring at scale consumes power; this is a feature (no shortcut) and a cost.

## Primary sources

- Boneh, Bonneau, Bünz, Fisch, *Verifiable Delay Functions*, CRYPTO 2018.
- Pietrzak, *Simple Verifiable Delay Functions*, ITCS 2019.
- Wesolowski, *Efficient Verifiable Delay Functions*, EUROCRYPT 2019.
- Boneh, Bünz, Fisch, *A Survey of Two Verifiable Delay Functions*, IACR ePrint 2018/712.
- Khovratovich, Maller, Bhat, *MinRoot: Candidate Sequential Function for Ethereum VDF*, 2022.
- De Feo, Masson, Petit, Sanso, *Verifiable Delay Functions from Supersingular Isogenies and Pairings*, ASIACRYPT 2019.
- Malavolta, Thyagarajan, *Homomorphic Time-Lock Puzzles and Applications*, CRYPTO 2019.
- Chia VDF reference: [github.com/Chia-Network/chiavdf](https://github.com/Chia-Network/chiavdf).
- drand: [drand.love](https://drand.love), [github.com/drand/drand](https://github.com/drand/drand).
