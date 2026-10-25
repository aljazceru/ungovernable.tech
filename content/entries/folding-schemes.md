---
title: "Folding Schemes"
slug: folding-schemes
type: explainer
pillars: ["zk"]
readiness: research
description: "Folding schemes such as Nova combine many instances of a computation into one claim, making incremental and recursive zero-knowledge proofs cheap."
dek: "A 2022-onward family of techniques that \"fold\" multiple instances of a computation into a single succinct claim, deferring expensive SNARK proving until the end. The technical innovation that makes incremental ZK proving practical at scale."
updated: 2026-10-25
created: 2026-04-25
origin: vault
source: "09-Zero-Knowledge/Folding Schemes.md"
aliases: ["Nova", "SuperNova", "HyperNova", "ProtoStar"]
tags: ["zk", "folding", "nova", "supernova", "hypernova", "protostar", "deep-dive"]
---

## What folding solves

Recursive SNARKs prove SNARKs prove SNARKs. The natural way to handle N steps of computation is: prove step 1, then prove "step 2 plus verify step 1's proof", then prove "step 3 plus verify step 2's proof", and so on. Each step pays the cost of an in-circuit verifier.

That cost is non-trivial. In-circuit verification of a SNARK is expensive; every step's prover budget is consumed proving the previous proof. For long computations this becomes prohibitive.

Folding schemes flip the structure: instead of proving each step's proof inside the next step, *fold* two instances of the same constraint system into a single combined instance. The folded instance carries the same witness obligation as the original but at half the cost. Repeat. At the end, prove a SNARK over the final folded claim.

```
Without folding:
  step 1 ──[SNARK]──► step 2 ──[SNARK with verifier]──► step 3 ──[SNARK with verifier]──► ...

With folding:
  fold(step 1, step 2) → folded_1
  fold(folded_1, step 3) → folded_2
  fold(folded_2, step 4) → folded_3
  ...
  SNARK over final folded claim
```

Effects:

- Per-step cost is low. Folding is much cheaper than in-circuit verification.
- Final SNARK is small. Only one expensive operation at the end.
- Memory bounded. Incremental, no need to keep all step witnesses around.
- Composable with virtually any SNARK / STARK base system.

## Nova (Kothapalli-Setty-Tzialla 2022)

The first practical folding scheme. Built on **R1CS** (Rank-1 Constraint System) and **relaxed R1CS** (a tweak that admits the folding operation). Operates over **cycles of curves** (Pasta) so the verifier can be expressed efficiently in the next layer's field.

Result: incremental verifiable computation (IVC) with constant-size step prover overhead. Per-step proving is dominated by elliptic-curve scalar multiplications, not in-circuit SNARK verification.

Used in: zkVM-style systems, recursive composition, encrypted state machines.

## SuperNova (Kothapalli-Setty 2022)

Generalizes Nova to **non-uniform IVC**, where each step might run a different program. Useful for zkVMs where each step is a different RISC-V opcode, an arbitrary AI model layer, or a different smart-contract function.

Effect: a zkVM doesn't need a single monolithic constraint system covering all opcodes. Each opcode has its own circuit; SuperNova folds across them efficiently.

## HyperNova (Kothapalli-Setty 2023)

Folds **Customizable Constraint Systems** (CCS), a generalization of Plonkish that includes lookups, custom gates, and high-degree constraints. Folding-friendly Plonkish.

Bridges the folding world (originally R1CS) with the modern Plonkish world.

## ProtoStar (Bünz-Chen 2024)

Folding for **Plonkish constraint systems** with arbitrary high-degree custom gates and lookups. Compatible with the existing Plonkish ecosystem (Halo2, Plonky3) without re-arithmetizing.

ProtoStar is what made folding practical for production Plonkish-based zkVMs.

## Why this matters for this library

ZK proving was historically too expensive to integrate into many sovereignty-relevant primitives. Folding changes the calculus:

- ZK rollups can scale proving to millions of transactions cheaply.
- zkML ([ZKML](/kb/zkml/)) can prove model inference layer-by-layer instead of all-at-once.
- vFHE composability becomes more tractable.
- Verifiable AI inference at production latency.
- State-machine replication (verifiable rollup-of-rollups, light-client provers).

Without folding, recursive ZK was the right idea expressed in the wrong shape. With folding, it's the right shape too.

## Comparison

| System | Constraint system | Innovation |
|--------|-------------------|-----------|
| **Nova** | Relaxed R1CS | First IVC with cheap step folding |
| **SuperNova** | Relaxed R1CS, non-uniform | Multi-program IVC |
| **HyperNova** | CCS | Plonkish-friendly folding |
| **ProtoStar** | Plonkish with high-degree gates | Plonkish accumulation/folding research |
| **Mangrove / Honk** | Plonkish | Aztec's folding direction (PG / variations) |
| **Sangria / Origami** | Variants | Research alternatives |

## Trade-offs

### Strengths

- Cheap per-step proving.
- Bounded memory.
- Composable with most SNARK / STARK frontends.
- Active research continues to optimize.

### Limitations

- Final SNARK is still required. Folding doesn't replace SNARKs, just accumulates.
- Implementation complexity. Folding-aware libraries are newer; bugs exist.
- Field-specific. Most schemes target specific fields / curve cycles.
- Verifier-on-chain cost for the final SNARK is unchanged.

## Where folding shows up

- **zkVMs** use different proof architectures. RISC Zero uses STARKs; Nova-style folding is one approach to incremental computation, not a property of every zkVM.
- **Aztec Network** uses folding (Honk variants) for recursive proof aggregation.
- **Lurk language** (Filecoin / Lurk Lab) is folding-native.
- Verifiable ML prototypes fold per-layer proofs into final-model proofs.
- Recursive bridges and light clients between L1s use folding for proof aggregation.

## Recent developments (2024-2026)

- ProtoStar publishes Plonkish folding for production.
- HyperNova extends to CCS.
- Lurk matures as a folding-native programming environment.
- zkVM comparisons must distinguish STARK recursion, lookup arguments and folding.
- Folding-friendly curves become a research target. Fields chosen for cheap folding rather than just SNARK-friendliness.

## Primary sources

- [Nova: Recursive Zero-Knowledge Arguments from Folding Schemes](https://eprint.iacr.org/2021/370)
- [SuperNova: Proving universal machine executions without universal circuits](https://eprint.iacr.org/2022/1758)
- [HyperNova: Recursive arguments for customizable constraint systems](https://eprint.iacr.org/2023/573)
- [ProtoStar: Generic Efficient Accumulation/Folding for Special Sound Protocols](https://eprint.iacr.org/2023/620)
- [Microsoft Nova implementation](https://github.com/microsoft/Nova)
- [Lurk implementation](https://github.com/lurk-lab/lurk-rs)
- [RISC Zero implementation](https://github.com/risc0/risc0)
- [SP1 implementation](https://github.com/succinctlabs/sp1)
- [Jolt implementation](https://github.com/a16z/jolt)
