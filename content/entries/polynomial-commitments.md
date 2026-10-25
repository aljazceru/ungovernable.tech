---
title: "Polynomial Commitments"
slug: polynomial-commitments
type: explainer
pillars: ["zk", "cryptography"]
readiness: usable
description: "Polynomial commitment schemes such as KZG, FRI and IPA sit underneath every modern proof system. What they are and how they trade off."
dek: "Underneath every modern proof system is a polynomial commitment scheme (PCS). The PCS lets a prover commit to a polynomial and later open it at a verifier-chosen point with a short proof. Most of the trade-offs that distinguish SNARKs from STARKs — proof size, prover time, trusted setup, post-quantum security — actually come from the PCS layer, not from the polynomial IOP on top. Pick the PCS and the proof system's properties largely follow."
updated: 2026-10-25
created: 2026-04-26
origin: vault
source: "09-Zero-Knowledge/Polynomial Commitments.md"
aliases: ["PCS", "KZG", "FRI", "IPA"]
tags: ["zk", "polynomial-commitments", "kzg", "fri", "ipa", "brakedown", "deep-dive", "cryptography"]
---

## What a PCS does

A polynomial commitment scheme is a tuple `(Commit, Open, Verify)`:

- `Commit(p) → C`. Compress a polynomial `p` of degree `d` into a short commitment `C`.
- `Open(p, z) → (y, π)`. Given the polynomial, the verifier-chosen evaluation point `z`, produce the claimed evaluation `y = p(z)` and a proof `π`.
- `Verify(C, z, y, π) → {accept, reject}`. Check that `C` was a commitment to *some* polynomial `p` and that `p(z) = y`, without seeing `p`.

Required security properties:

- **Binding.** A prover can't produce two valid openings of the same `C` to different `y` values for the same `z`.
- **Hiding (optional).** `C` reveals nothing about `p` beyond what the openings reveal.
- **Succinctness.** `|C|` and `|π|` should be much smaller than `|p|`. Verifier time should be much less than `O(d)`.

Almost all modern proof systems compile a polynomial Interactive Oracle Proof (PIOP) into a non-interactive argument by replacing the PIOP's polynomial-oracle queries with PCS commitments and openings. The choice of PCS dictates the resulting proof system's properties.

## KZG (Kate-Zaverucha-Goldberg, 2010)

Kate, Zaverucha, Goldberg, *Constant-Size Commitments to Polynomials and Their Applications*, ASIACRYPT 2010.

### Construction

KZG is pairing-based. The setup produces a Structured Reference String (SRS) consisting of `(g, gᵗ, gᵗ², ..., gᵗᵈ)` for a secret `t` (which must be discarded — this is the trusted setup). Commitments are `C = g^p(t)` — a single group element.

To open at point `z`, the prover computes the quotient `q(x) = (p(x) - p(z)) / (x - z)` and outputs the proof `π = g^q(t)` — also a single group element. The verifier checks `e(C - g^y, h) = e(π, h^t - h^z)` using a pairing.

### Properties

- **Proof size:** O(1) — one group element. Smallest possible.
- **Verifier time:** O(1) — one pairing.
- **Prover time:** O(d) field operations + group exponentiations.
- **Setup:** trusted. The secret `t` must be destroyed; if not, the scheme is broken.
- **Post-quantum:** No. Pairings are vulnerable to Shor.

### Used by

- Groth16 (variant for R1CS).
- PLONK (Plonkish PIOP + KZG).
- Most pairing-based [SNARKs](/kb/snarks/).
- Ethereum's blob commitments (EIP-4844 / proto-danksharding) use KZG over BLS12-381.

KZG dominates the "smallest proofs on Ethereum" niche because of pairing precompiles in the EVM (BN254 pairings are cheap; BLS12-381 pairings are added via EIP precompiles).

## FRI (Fast Reed-Solomon Interactive Oracle Proof)

Ben-Sasson, Bentov, Horesh, Riabzev, *Fast Reed-Solomon Interactive Oracle Proofs of Proximity*, ICALP 2018.

### Construction

FRI is hash-based and transparent. The prover commits to a polynomial `p` by encoding it as a Reed-Solomon codeword (evaluations on a coset of the multiplicative group of size `ρ⁻¹·d`, where `ρ < 1` is the rate) and Merkle-hashes the evaluations.

To prove that a committed evaluation table is close to a low-degree polynomial, FRI runs an interactive folding protocol:

1. Split `p(x) = pₑ(x²) + x·pₒ(x²)`.
2. Verifier sends a random `α`; prover commits to `p'(y) = pₑ(y) + α·pₒ(y)` of half degree.
3. Repeat until the polynomial is constant.
4. Verifier checks Merkle paths at random sampled points and checks consistency between adjacent rounds.

The interactive protocol is made non-interactive via Fiat-Shamir.

### Properties

- **Proof size:** O(log² d). Tens to hundreds of kilobytes typical.
- **Verifier time:** O(log² d) hashes plus a constant number of Merkle path checks.
- **Prover time:** O(d log d) — fast.
- **Setup:** none. Fully transparent.
- **Post-quantum:** Yes (relies only on hash collision resistance).

### Used by

- StarkWare's STARK provers, Cairo, StarkNet.
- Plonky2 / Plonky3 (Plonkish PIOP + FRI).
- Risc Zero, SP1 zkVMs.
- Boojum (zkSync Era's prover).

FRI dominates "transparent, post-quantum, fast prover" — the [STARKs](/kb/starks/) family.

## Inner Product Argument (IPA)

Bootle, Cerulli, Chaidos, Groth, Petit, *Efficient Zero-Knowledge Arguments for Arithmetic Circuits in the Discrete Log Setting*, EUROCRYPT 2016.

### Construction

IPA commits to a polynomial via a Pedersen-vector commitment to its coefficients: `C = ∑ aᵢ·Gᵢ + r·H` for a vector of basis points `Gᵢ` and a randomness `r·H`.

To open at `z`, the prover proves an inner product equality: `<a, (1, z, z², ..., zᵈ)> = y`. The proof uses a recursive halving: in each round, the prover sends two group elements, the verifier sends a random scalar, and the inner product is folded to half size. After `log d` rounds, the proof concludes with a single scalar.

### Properties

- **Proof size:** O(log d) group elements. Around a few KB at typical sizes.
- **Verifier time:** O(d) group exponentiations (linear in degree). This is the IPA verifier's main cost.
- **Prover time:** O(d log d) group operations.
- **Setup:** transparent. The basis points `Gᵢ` are derivable from a hash function (no secret).
- **Post-quantum:** No (relies on discrete log).

### Used by

- Bulletproofs (Bünz et al., 2018) — IPA-based range proofs.
- Halo / Halo2 (Bowe-Grigg-Hopwood, 2019) — recursive composition without trusted setup.
- Pickles (Mina Protocol).

IPA's role is "transparent, recursive-friendly SNARK without pairings." The price is linear verifier time.

## PCS comparison

| PCS | Assumption | Proof size | Verifier time | Prover time | Setup | Post-quantum |
|-----|------------|-----------|---------------|-------------|-------|--------------|
| **KZG** | q-SDH (pairings) | O(1) | O(1) | O(d) | Trusted (per-degree) | No |
| **FRI** | Hash CR + RS proximity | O(log² d) | O(log² d) | O(d log d) | None | Yes |
| **IPA** | Discrete log | O(log d) | O(d) | O(d log d) | None | No |
| **Bulletproofs (IPA)** | Discrete log | O(log d) | O(d) | O(d log d) | None | No |
| **Brakedown** | Hash CR + linear codes | O(√d) | O(√d) | O(d) | None | Yes |
| **Orion** | Hash CR + linear codes | O(log² d) | O(log² d) | O(d) | None | Yes |
| **Basefold** | Hash CR + RS / FRI-like | O(log² d) | O(log² d) | O(d log d) | None | Yes |
| **Hyrax** | Discrete log | O(√d) | O(√d) | O(d) | None | No |

(d = polynomial degree; "verifier time" excludes O(1) constants; multilinear PCS row entries are for n-variate polynomials with 2ⁿ terms.)

## Why PCS choice dominates proof-system trade-offs

A proof system is roughly: PIOP + PCS. Most PIOPs (Plonkish, R1CS, AIR, sumcheck) can be paired with several PCSes. The system's external properties — proof size, verifier cost, setup, PQ status — track the PCS, not the PIOP.

Examples:

- **Plonkish PIOP + KZG = PLONK.** Tiny proof (~5 KB), fast on-chain verifier, trusted setup.
- **Plonkish PIOP + IPA = Halo2.** No trusted setup, recursive-friendly, slower verifier.
- **Plonkish PIOP + FRI = Plonky2.** No trusted setup, post-quantum, larger proof.
- **AIR PIOP + FRI = STARK.** No trusted setup, post-quantum, large proof.
- **R1CS PIOP + KZG = Marlin.** Universal trusted setup, small proof.
- **R1CS PIOP + IPA = Bulletproofs-style.** No trusted setup, log-size proof, linear verifier.

Proof-system designers pick a PIOP that matches their constraint system, then pick a PCS based on what they want externally. The PCS choice is usually the more consequential one for users.

## Multilinear PCS — newer family

For sumcheck-based provers (Spartan, HyperPlonk, STIR), multilinear polynomials over the boolean hypercube are a natural representation. Multilinear PCS designs:

### Brakedown

Golovnev, Lee, Setty, Thaler, Wahby, *Brakedown: Linear-Time and Field-Agnostic SNARKs for R1CS*, CRYPTO 2023.

- Hash-based, transparent.
- Linear-time prover.
- Square-root proof size: O(√d).
- Field-agnostic — works over any field, including small fields favored by hardware acceleration.

### Orion

Xie, Zhang, Song, *Orion: Zero-Knowledge Proof with Linear Prover Time*, CRYPTO 2022.

- Builds on Brakedown's code-based ideas with smaller proofs (poly-log).
- Hash-based, transparent.
- Linear-time prover.

### Basefold

Zeilberger, Chen, Fisch, *Basefold: Efficient Field-Agnostic Polynomial Commitment Schemes from Foldable Codes*, CRYPTO 2024.

- FRI-style folding generalized to a wider class of codes.
- Field-agnostic; unifies FRI and Brakedown-style approaches.
- Hash-based; transparent; PQ-secure.

### Hyrax

Wahby, Tzialla, Shelat, Thaler, Walfish, *Doubly-Efficient zkSNARKs Without Trusted Setup*, IEEE S&P 2018.

- IPA-based; multilinear; square-root proof size.
- No trusted setup.

These multilinear PCS designs are increasingly the choice for newer zkVMs and SNARK frameworks because the linear-time prover and field-agnostic structure match modern hardware better than pairing-based systems.

## Field choice and PCS

PCS choice constrains which fields are usable:

- **KZG** requires a pairing-friendly elliptic curve (BN254, BLS12-381). The scalar field is fixed by the curve.
- **FRI** prefers fields with large smooth (multiplicative) subgroups for FFT efficiency. Mersenne primes (`2⁶¹ - 1`, `2³¹ - 1`) and Goldilocks (`2⁶⁴ - 2³² + 1`) are popular for STARK provers.
- **IPA** works over any group with hard discrete log; in practice paired with `secp256k1`, `pasta`, or similar non-pairing curves.
- **Brakedown / Orion / Basefold** are field-agnostic — usable over small fields, which dramatically speeds up proving on commodity hardware.

The trend in 2024-2026 is toward small fields and hash-based PCS for prover throughput. Pairing-based systems are increasingly used only at the *final wrapping* layer to produce small on-chain proofs.

## Wrapping: combining PCSes

Modern stacks compose multiple proof systems:

1. **Inner prover** uses FRI or Brakedown over a small field for prover throughput.
2. **Outer wrapper** verifies the inner proof inside a SNARK that uses KZG over BN254 — producing a small proof verifiable cheaply on Ethereum.

This pattern (Plonky2 → Groth16, STARK → Boojum → Groth16, etc.) is now standard in production rollups. The PCS structure shifts twice: throughput-optimized inside, size-optimized outside.

See [ZK Rollups](/kb/zk-rollups/) for how this composition shows up in production proving stacks.

## Cross-cutting concerns

### Trusted setup

KZG requires per-degree trusted setup. Universal setup ceremonies (Ethereum's KZG ceremony, Aleo's setup) make a single setup reusable for any circuit up to a degree cap. FRI, IPA-without-trapdoor, and the multilinear hash-based schemes have no trusted setup.

### Post-quantum security

Hash-based PCSes (FRI, Brakedown, Orion, Basefold) survive Shor's algorithm. Pairing- and discrete-log-based PCSes (KZG, IPA) do not. As [Overview - Post-Quantum Cryptography](/kb/post-quantum-cryptography/) discusses, new ZK deployments increasingly weight PQ security.

### Verifier cost on chain

For Ethereum-deployed verifiers:

- KZG: ~250-500k gas (one or two pairings + minor group ops). Cheapest.
- IPA: verification can require linear work even though the proof has logarithmic size; on-chain cost depends on the implementation.
- FRI: log² verifier, but practical implementations are still ~1-3M gas. Usable but not cheap.
- Brakedown / Orion: similar order to FRI in current implementations.

This cost is why the "wrap with Groth16 / KZG for final on-chain verification" pattern is universal.

## Trade-offs summary

| If you need… | Pick |
|--------------|------|
| Smallest on-chain proof (Ethereum) | KZG (Groth16, PLONK) |
| No trusted setup ever | FRI, IPA, or hash-based multilinear |
| Post-quantum security | FRI, Brakedown, Orion, Basefold |
| Linear-time prover | Brakedown, Orion |
| Recursive composition without overhead | Halo2 (IPA) or accumulation schemes |
| Field-agnostic prover (small-field hardware) | Brakedown / Basefold |
| Highest prover throughput on big circuits | FRI over Goldilocks (Plonky3-style) |

## Primary sources

- [Efficient Zero-Knowledge Arguments for Arithmetic Circuits in the Discrete Log Setting](https://eprint.iacr.org/2016/263)
- [Bulletproofs: Short Proofs for Confidential Transactions and More](https://eprint.iacr.org/2017/1066)
- [Recursive Proof Composition without a Trusted Setup](https://eprint.iacr.org/2019/1021)
- [Doubly-efficient zkSNARKs without trusted setup](https://eprint.iacr.org/2017/1132)
- [Brakedown: Linear-time and field-agnostic SNARKs for R1CS](https://eprint.iacr.org/2021/1043)
- [Orion: Zero Knowledge Proof with Linear Prover Time](https://eprint.iacr.org/2022/1010)
- [BaseFold: Efficient Field-Agnostic Polynomial Commitment Schemes from Foldable Codes](https://eprint.iacr.org/2023/1705)
- [Spartan: Efficient and general-purpose zkSNARKs without trusted setup](https://eprint.iacr.org/2019/550)
- [Halo2 design documentation](https://zcash.github.io/halo2/)
- [Kate, Zaverucha and Goldberg: Polynomial Commitments](https://cacr.uwaterloo.ca/techreports/2010/cacr2010-10.pdf)
- [Fast Reed-Solomon Interactive Oracle Proofs of Proximity](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2018.14)
