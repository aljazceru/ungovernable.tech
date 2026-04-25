---
title: "SNARKs"
tags:
  - "zk"
  - "snarks"
  - "groth16"
  - "plonk"
  - "halo2"
  - "deep-dive"
  - "cryptography"
---
*Cryptographic proofs that are tiny (hundreds of bytes to a few kilobytes), check in milliseconds, and can prove arbitrary computation. The workhorse of ZK rollups, privacy coins, and verifiable identity systems.*

---

## What "SNARK" means

The acronym unpacks tightly:

- **Succinct**: proof size and verifier time are roughly independent of the computation's size.
- **Non-interactive**: the prover sends the verifier a single message; no back-and-forth.
- **ARgument**: soundness holds against computationally bounded provers (vs. proofs which hold against unbounded provers).
- **of Knowledge**: the prover demonstrates it *knows* a witness, not merely that one exists.

Every modern ZK system is a SNARK or STARK variant. The differences are in trusted setup requirements, proof size, prover time, verifier time, and post-quantum security.

---

## The construction pipeline

A SNARK is built from three layers:

```
1. Statement → Arithmetic Circuit (R1CS, AIR, Plonkish)
2. Circuit → Polynomial IOP (PIOP)
3. PIOP → Cryptographic compilation (KZG, FRI, IPA, Bulletproofs)
```

Different SNARK systems pick different layers. Examples:

| System | Circuit format | PIOP | Crypto compilation |
|--------|----------------|------|--------------------|
| **Groth16** | R1CS | Linear PIOP | Pairing-based (BN254/BLS12-381) |
| **PLONK** | Plonkish | Plonkish PIOP | KZG (pairing-based) |
| **Halo2** | Plonkish | Plonkish PIOP | IPA (no pairings) |
| **Marlin** | R1CS | AHP | KZG |
| **Spartan** | R1CS | Sumcheck | Pedersen / hash-based |

The "best" choice depends on what you're optimizing for: proof size, prover speed, setup requirements, or recursive composition.

---

## Groth16 (2016)

The shortest practical SNARK. Proofs are around **128-200 bytes** (3 group elements: 2 in G1, 1 in G2 over BN254 or BLS12-381). Verifier time is constant (a few pairings).

- Trusted setup: per-circuit. Each new circuit needs a fresh ceremony.
- Use cases: Zcash Sapling, Tornado Cash, Aztec Connect (legacy), Semaphore.
- Trade-off: smallest proofs, but the per-circuit setup is operationally inconvenient. Once your circuit is fixed, Groth16 is the cheapest verifier on Ethereum.

Implementation: `arkworks/groth16`, `bellman` (Zcash), `circom` + `snarkjs`.

---

## PLONK (2019)

**Permutations over Lagrange-bases for Oecumenical Non-interactive arguments of Knowledge.** Universal updatable trusted setup. One ceremony serves all circuits up to a maximum size.

- Proof size: 1-5 KB.
- Verifier time: 10-50 ms.
- Setup: universal. Circuits with up to 2ⁿ gates share the same setup.
- Custom gates: domain-specific operations baked into the arithmetization for efficiency.

The innovation that broke the per-circuit-setup bottleneck. Every modern PLONK-family system inherits this property.

Variants: Aztec Plonk, TurboPlonk, UltraPlonk, Plookup, Caulk, Lasso (lookup arguments).

---

## Halo2 (2020-2021)

Electric Coin Co.'s rewrite of Plonk for Zcash Orchard. Two big changes:

- No trusted setup. Uses Inner Product Arguments (IPA) over `secp256k1` / `pasta` curves instead of pairings. The transparent setup is hash-based.
- Recursive composition without overhead. Proofs prove proofs, enabling unbounded depth.

Halo2 is the basis for many modern systems: Filecoin's Saturn, Scroll's Plonkish prover, Anoma, Aztec Network's modern stack.

---

## STARKs (briefly, see [STARKs](/zero-knowledge/starks))

A non-SNARK alternative using FRI (Fast Reed-Solomon Interactive Oracle Proof) for polynomial commitment. Larger proofs (50-200 KB), but:

- No trusted setup ever.
- Hash-based (post-quantum-friendly).
- Fast prover for large computations.

Modern systems (Plonky2/3, Boojum) compose SNARK and STARK layers. STARK for bulk proving, SNARK for final wrapping when on-chain verification cost matters.

---

## Lookup arguments

Modern SNARK efficiency leans heavily on lookup arguments, a way to prove "this value is in this precomputed table" cheaply. Examples:

- **Plookup** (Gabizon-Williamson 2020): original.
- **Caulk** (Zapico et al. 2022): sublinear prover for huge tables.
- **Lasso** (Setty-Thaler-Wahby 2023): even more efficient for structured tables.
- **Jolt** (Arun-Setty-Thaler 2023): RISC-V zkVM built on Lasso.

Lookups dramatically reduce circuit size for operations like AES, hash functions, and arithmetic on bounded ranges.

---

## Recursive composition and folding

A SNARK that verifies SNARKs lets you compress proof chains: prove N steps, output a single succinct proof of the entire computation.

- **In-circuit verification**: express the SNARK verifier as a circuit. Pairing-based systems can't do this efficiently because pairings inside the field are expensive.
- **Cycles of curves**: Halo2 alternates between two curves so each layer's verifier is efficient in the next layer's field.
- **Folding schemes** ([Folding Schemes](/zero-knowledge/folding-schemes)): Nova / SuperNova / HyperNova accumulate proofs incrementally without per-step SNARK overhead.

Recursive composition is what makes ZK rollups scalable: prove a million transactions by folding millions of step-proofs into one.

---

## Performance snapshot (early 2026)

| System | Proof size | Verifier time | Prover time | Setup |
|--------|-----------|---------------|-------------|-------|
| Groth16 | ~128 B | <5 ms | Slow | Per-circuit |
| PLONK | 1-5 KB | 10-50 ms | Moderate | Universal |
| Halo2 | 5-10 KB | 30-80 ms | Moderate | None |
| Plonky2/3 | 50-100 KB | ~10 ms | Fast | None (hash-based) |
| STARK | 50-200 KB | ~10 ms | Fast | None |
| Spartan | ~5 KB | Linear | Fast | None |
| Nova/SuperNova (folded) | Small | Fast | Incremental | Per-circuit |

Numbers compress every year as research advances.

---

## Where SNARKs show up in this vault

- [Overview - Zero-Knowledge Proofs](/zero-knowledge) — overview.
- [ZK Rollups](/zero-knowledge/zk-rollups) — proving Ethereum execution.
- [ZKML](/zero-knowledge/zkml) — proving model inference.
- [FHE Bootstrapping and Verification](/cryptography/fhe-bootstrapping-and-verification) — vFHE composition.
- [Overview - Decentralized Identity](/identity/overview-decentralized-identity) — selective disclosure (BBS+, ZK passports).
- [Lightning Network Deep Dive](/financial-sovereignty/lightning-network-deep-dive) — PTLCs use Schnorr + ZK adaptors.
- [Overview - Identity & Pseudonymity](/identity) — proof-of-personhood (Anon Aadhaar, zkPassport, Worldcoin).

---

## Trusted setup, when it matters

A "trusted setup" generates structured reference parameters via a multi-party computation ceremony. If any single participant is honest and destroys their share of the secret, the setup is sound. Adversary needs all participants to collude.

- **Per-circuit setup** (Groth16): ceremony per use case. Operationally heavy.
- **Universal setup** (PLONK family): one ceremony for all circuits up to a size cap. Reusable.
- **Updatable setup** (Sonic, Marlin): anyone can extend the ceremony, lowering trust.
- **No setup** (STARKs, Halo2 with IPA): purely hash-based.

Production projects with trusted setups (Zcash, Filecoin, Aleo) ran ceremonies with thousands of contributors. The cryptographic case for soundness is solid; the operational case for "no setup" systems is increasingly preferred for new designs.

---

## Trade-offs

### Strengths

- Smallest proofs of any verifiable-computation system.
- Constant verifier time for many constructions.
- Mature. Production deployments since 2014 (Zcash).
- Composable with FHE, MPC, blockchain, and identity systems.
- Active research field. Every year sees major performance improvements.

### Limitations

- Prover time is the dominant cost. Proving complex computations takes minutes to hours.
- Trusted setup for some systems (Groth16, KZG-based PLONK).
- Pairing-based systems are not post-quantum safe.
- Implementation complexity. Bugs in low-level code can break soundness silently.
- Field-specific. Choosing the right field/curve is a serious engineering exercise.

---

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Trusted-setup all-collude | Multi-party ceremony with honest-1-of-n soundness |
| Prover bugs in circuit | Formal verification, audit, fuzzing |
| Soundness break in proof system | Use battle-tested systems (Groth16, PLONK have strong literature) |
| Quantum break (pairings) | Migrate to STARK / Halo2 / hash-based variants |
| Implementation timing-side-channel | Constant-time prover libraries |
| Public-input commitment confusion | Clear API for what's public vs witness |

---

## Recent developments (2024-2026)

- Lookup arguments mature into standard SNARK toolkits (Lasso, Jolt).
- Folding schemes (Nova, SuperNova, HyperNova, ProtoStar) productize.
- Hardware acceleration. FPGA / GPU SNARK provers from CysicNetwork, Ingonyama, others.
- PQ SNARKs progressing. STARKs deployed; transparent SNARK research advancing.
- zkVMs ([ZK Rollups](/zero-knowledge/zk-rollups)) compete on developer ergonomics. Risc Zero, SP1, Jolt, Cairo.

---

## Related files

- [Overview - Zero-Knowledge Proofs](/zero-knowledge)
- [STARKs](/zero-knowledge/starks)
- [Folding Schemes](/zero-knowledge/folding-schemes)
- [ZK Rollups](/zero-knowledge/zk-rollups)
- [ZKML](/zero-knowledge/zkml)
- [Overview - Post-Quantum Cryptography](/post-quantum)
- [FHE Bootstrapping and Verification](/cryptography/fhe-bootstrapping-and-verification)
- [Glossary](/meta/glossary) — Groth16, PLONK, Halo2, STARK, FRI, KZG

---

## Primary sources

- Groth, *On the Size of Pairing-Based Non-Interactive Arguments*, EUROCRYPT 2016.
- Gabizon, Williamson, Ciobotaru, *PLONK*, IACR 2019/953.
- Bowe, Grigg, Hopwood, *Recursive Proof Composition without a Trusted Setup* (Halo), 2019.
- Bowe et al., *Halo2 Book* — [zcash.github.io/halo2/](https://zcash.github.io/halo2/).
- Setty, *Spartan: Efficient and General-Purpose zkSNARKs*, CRYPTO 2020.
- Setty, Thaler, Wahby, *Unlocking the Lookup Singularity with Lasso*, 2023.
- Arun, Setty, Thaler, *Jolt: SNARKs for Virtual Machines via Lookups*, 2023.
- Kothapalli, Setty, Tzialla, *Nova: Recursive Zero-Knowledge Arguments from Folding Schemes*, 2022.

