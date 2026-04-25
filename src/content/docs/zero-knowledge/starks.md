---
title: "STARKs"
tags:
  - "zk"
  - "starks"
  - "fri"
  - "plonky2"
  - "plonky3"
  - "deep-dive"
  - "post-quantum"
---
*Hash-based, transparent (no trusted setup), post-quantum-secure proofs. Larger than SNARKs but with operational virtues that make them the dominant choice for new high-throughput proving systems.*

---

## How STARKs differ

Compared to SNARKs ([SNARKs](/zero-knowledge/snarks)):

| Property | SNARK (typical) | STARK |
|----------|-----------------|-------|
| Trusted setup | Often yes | **Never** |
| Proof size | 100 B - 10 KB | 50-200 KB |
| Verifier time | constant | log² of computation |
| Prover speed | varies | typically faster |
| Cryptographic basis | pairings, IPA, KZG | hashes only |
| Post-quantum safe | Mostly no (pairings) | **Yes** (hash-based) |

The trade-off is proof size for transparency, post-quantum security, and prover speed. For systems where the prover is run repeatedly (rollups, zkVMs), STARK proving speed wins; the larger on-chain verifier cost is amortized or wrapped.

---

## How STARKs work (conceptually)

A STARK proves an arithmetic execution trace satisfies an algebraic constraint system. Build:

1. **AIR** (Algebraic Intermediate Representation): execution trace as a polynomial.
2. **Reed-Solomon encoding** of the trace.
3. **FRI** (Fast Reed-Solomon Interactive Oracle Proof): proves the encoded polynomial has low degree.
4. **Fiat-Shamir**: make it non-interactive by hashing.

Soundness comes from: low-degree polynomial agreement is very unlikely between two distinct codewords; sampled positions catch cheating with high probability.

The math is simpler in spirit than pairing-based SNARKs. Fewer exotic structures, more standard hash and interpolation primitives.

---

## FRI (Fast Reed-Solomon IOP)

The polynomial commitment scheme at the heart of STARKs (and modern transparent SNARKs).

- **Commit**: hash a Merkle tree over a Reed-Solomon evaluation of the polynomial.
- **Open**: reveal sampled points plus Merkle paths.
- **Soundness**: relies on Reed-Solomon distance and folding consistency.

Commitment is hash-based (typically SHA-3, BLAKE3, or Poseidon for in-circuit use). The hash assumption is the only cryptographic hardness, which is the entire post-quantum story.

---

## STARK implementations

### StarkWare's Cairo / StarkNet

The original production STARK system. Cairo is a STARK-friendly programming language; StarkNet is an Ethereum L2 powered by StarkWare's prover.

### Plonky2 / Plonky3

Polygon's Plonky family combines Plonkish arithmetization with FRI (instead of KZG). Compared to pure STARKs:

- Smaller proofs.
- Faster prover.
- Same transparency, no trusted setup.
- Custom gates from Plonkish baseline.

Plonky3 (2024) is the modular successor; designed for composition with other systems.

### Boojum / Risc0

zkSync's Boojum is a STARK-based prover; Risc0 is a STARK-based zkVM proving RISC-V execution.

### Stwo / S2 / Circle STARK

StarkWare's next-generation prover using Mersenne-prime fields and Circle group arithmetic. Major prover-speed improvements; rolling out 2025-2026.

### SP1 / Jolt / other zkVMs

Modern zkVMs combine STARK proving (or STARK-ish proving) for the bulk of execution with SNARK wrapping for final on-chain verification. **SP1** (Succinct Labs) and **Jolt** (a16z) are the most-discussed in 2025-2026.

---

## STARKs vs Plonky2 vs Plonky3

The boundary between "pure STARK" and "Plonkish-with-FRI" blurs. The de facto situation:

- **Pure STARKs** (Cairo, original StarkWare prover): AIR → FRI.
- **Plonky2/3**: Plonkish circuits → FRI commitment. Best of both worlds — Plonkish flexibility plus FRI transparency.
- **Hybrid systems** (Nova-on-FRI, etc.): research-stage.

Most new production systems pick a Plonkish-style frontend with a FRI / hash-based commitment scheme rather than pure traditional STARKs. The terminology is messy, but the engineering is converging.

---

## Performance snapshot (early 2026)

| System | Throughput | Proof size | Verifier (on-chain) |
|--------|-----------|-----------|---------------------|
| Cairo + StarkWare prover | High (StarkNet block proving) | ~50-150 KB | ~1M gas |
| Plonky2 | Very fast prover | ~50-100 KB | ~500K-1M gas |
| Plonky3 | Faster than 2 | similar | similar |
| Boojum | Production-grade for zkSync | ~100-200 KB | ~1M gas |
| Risc0 (RISC-V STARK) | Moderate | Wrapped Groth16 final ~200 B | low |

The "wrapped Groth16 final" pattern is common: prove with a fast STARK, then wrap into a tiny Groth16 for cheap on-chain verification.

---

## Where STARKs show up

- **StarkNet, zkSync (Boojum), Polygon Miden**: L2s using STARK-style proving.
- **Risc0**: RISC-V STARK-based zkVM, wrapped with Groth16 for on-chain.
- **Filecoin**: Proof-of-Spacetime uses STARK-derived constructions.
- PQ-secure ZK identity systems experimenting with STARK proofs.
- Privacy on stake / consensus: some experimental L1s.

---

## Trade-offs

### Strengths

- No trusted setup, ever.
- Hash-only assumptions. Post-quantum-friendly.
- Fast prover for large computations.
- Mature production deployments (StarkNet since 2020).
- Composable with SNARKs via wrapping.

### Limitations

- Larger proofs. Mitigated by SNARK wrapping for on-chain.
- Verifier on Ethereum is more expensive than Groth16 (mitigated by wrapping).
- Field constraints. Reed-Solomon over specific fields; arithmetization can be awkward.
- Less mature lookup-argument literature than the SNARK side (catching up).
- Tooling is fragmented. Cairo, Plonky3, Risc0, SP1 all have different DSLs.

---

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Hash function break | Choose hashes with margin (SHA-3, BLAKE3); migrate ahead of breaks |
| FRI soundness via low-distance forging | Conservative parameter choice; field size selection |
| Implementation bugs in prover/verifier | Formal verification, audit, fuzzing |
| Quantum (future) | STARKs are resistant. Grover halves preimage security but margins survive |
| Field-specific attacks | Standard cryptanalytic vigilance |

---

## Recent developments (2024-2026)

- Plonky3 released, modular successor to Plonky2.
- Stwo / Circle STARK: Mersenne-prime field, faster proving.
- SP1 (Succinct Labs): RISC-V zkVM, rapid adoption.
- Jolt (a16z): Lasso-based zkVM, alternative architecture.
- GPU / FPGA STARK provers from Ingonyama, Cysic.
- Risc0 production. Used by some applications for verifiable AI inference and bridges.
- STARK-based bridges between L1s.

---

## Related files

- [Overview - Zero-Knowledge Proofs](/zero-knowledge)
- [SNARKs](/zero-knowledge/snarks)
- [Folding Schemes](/zero-knowledge/folding-schemes)
- [ZK Rollups](/zero-knowledge/zk-rollups)
- [ZKML](/zero-knowledge/zkml)
- [Overview - Post-Quantum Cryptography](/post-quantum) — STARK PQ relevance
- [Glossary](/meta/glossary) — STARK, FRI, AIR, Plonky2, Plonky3

---

## Primary sources

- Ben-Sasson, Bentov, Horesh, Riabzev, *Scalable, transparent, and post-quantum secure computational integrity*, IACR 2018/046.
- Ben-Sasson et al., *DEEP-FRI: Sampling Outside the Box Improves Soundness*, 2019.
- Polygon Labs, *Plonky2*. [github.com/0xPolygonZero/plonky2](https://github.com/0xPolygonZero/plonky2).
- Plonky3 — [github.com/Plonky3/Plonky3](https://github.com/Plonky3/Plonky3).
- StarkWare resources — [starkware.co/docs](https://starkware.co/docs).
- Cairo book — [cairo-book.github.io](https://cairo-book.github.io).
- Risc0 — [risczero.com](https://risczero.com).
- SP1 — [github.com/succinctlabs/sp1](https://github.com/succinctlabs/sp1).

