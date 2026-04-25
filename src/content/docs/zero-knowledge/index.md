---
title: "Zero-Knowledge"
tags:
  - "zk"
  - "zk-snark"
  - "zk-stark"
  - "bulletproofs"
  - "zkml"
  - "cryptography"
sidebar: {"label":"Overview","order":0}
---
*Prove that a statement is true without revealing anything beyond its truth.*

---

## Core idea

A prover convinces a verifier that a statement `S` holds, such that the verifier learns nothing except `S` itself. Formally: completeness, soundness, zero-knowledge. The modern cryptographic realization uses succinct non-interactive arguments of knowledge — **SNARKs**.

The practical win: a prover does work once, produces a tiny proof (hundreds of bytes to a few KB), and the verifier checks it in milliseconds. Proof size and verifier time are near-constant regardless of the computation's complexity.

---

## Families

| Family | Size | Prover | Verifier | Trusted Setup | Post-Quantum |
|---|---|---|---|---|---|
| **Groth16** | ~200 B | Slow | <5 ms | Per-circuit | No |
| **PLONK / Halo2** | 1–5 KB | Moderate | ~10–50 ms | Universal (updatable) | No |
| **STARKs** | 50–200 KB | Fast | ~10 ms | None | Yes (hash-based) |
| **Bulletproofs** | ~1 KB (log n) | Fast | Linear verify | None | No |
| **Nova / Folding** | Small | Incremental, fast | Fast | Per-circuit | No |
| **SNARKs over FRI / Binius / Jolt** | Moderate | Very fast | Fast | None / universal | Mostly yes |

---

## What's built on them

### Blockchain scaling (ZK rollups)

- **StarkNet, zkSync Era, Scroll, Linea, Polygon zkEVM.** Bundle thousands of Ethereum txs into one on-chain proof. Enables private-by-default L2s when combined with encrypted state.

### Privacy coins / mixers

- **Zcash (shielded pools).** Groth16 proofs over the Sapling circuit.
- **Aztec, Tornado Cash (historical), Railgun.** EVM-layer shielded pools.

### Identity and credentials

- **Anon Aadhaar, zkPassport, Semaphore, Rarimo.** Prove "I'm over 18 / I'm a citizen / I'm not in a sanctions list" without revealing identity.
- **Sismo, Gitcoin Passport.** Zero-knowledge reputation portability.

### ZK machine learning (ZKML)

Prove a model output was produced by a committed set of weights on a committed input, without revealing weights or input.

- **EZKL** (zkonnx circuits), **Giza**, **RISC Zero's zkVM**, **Modulus Labs**.
- Current limits: proving a ~10M-param model on a reasonable input takes seconds to minutes, not milliseconds. Workable for verifiable oracles; not for real-time inference.
- Pair with TEEs (see [Confidential-AI-Inference](/confidential-computing/confidential-ai-inference)): TEE handles input/weight privacy, ZK handles output-correctness auditability.

### Private cross-chain, bridges

- **Succinct, =nil;, Polyhedra.** Light-client proofs.

---

## Relation to confidential computing

ZK and TEEs solve overlapping but not identical problems:

| | TEE | ZK |
|---|---|---|
| Input confidentiality | Yes (hardware) | Yes (cryptographic) |
| Output correctness | Attested, not cryptographically proven | Cryptographically proven |
| Output confidentiality | Yes | Only under extra tricks |
| Trust assumption | Silicon vendor, firmware | Math + (maybe) trusted setup |
| Performance | Near-native | 10³–10⁶× slower to prove |
| Post-quantum | N/A (hardware) | STARKs yes, SNARKs no |

A mature confidential-inference stack may use both: TEE for fast private inference, ZK to prove (to third parties, after the fact) that the computation was correct and the expected model was used.

---

## Trade-offs

### Strengths

- Mathematical assurance; no hardware trust required.
- Tiny proofs allow verification on constrained devices (blockchains, browsers, mobile).
- Post-quantum variants (STARKs, hash-based) exist.

### Limitations

- Prover cost. Still orders of magnitude more expensive than native computation.
- Circuit-writing is hard. Domain-specific; one bug can silently void security.
- Trusted-setup ceremonies (Groth16, original PLONK) require careful MPC; a leaked toxic-waste compromises soundness.
- Zero-knowledge is not the same as privacy. ZK proves a specific statement; if the statement leaks info, so does the system.

---

## Attack surface

- Circuit bugs. The overwhelming majority of ZK break-ins are circuit-logic errors, not crypto.
- Trusted setup leakage.
- Fiat-Shamir transforms done incorrectly (weak Fiat-Shamir) lead to soundness failures.
- Proof malleability or replay without proper domain separation.

---

## Related files

- [Overview - Confidential Computing](/confidential-computing)
- [Confidential-AI-Inference](/confidential-computing/confidential-ai-inference)
- [Overview - Fully Homomorphic Encryption](/cryptography/overview-fully-homomorphic-encryption)
- [Overview - Private Information Retrieval](/cryptography/overview-private-information-retrieval)

## Primary sources

- Groth: *On the Size of Pairing-Based Non-Interactive Arguments* — EUROCRYPT 2016
- Ben-Sasson et al.: *Scalable, transparent, and post-quantum secure computational integrity* — IACR 2018 (STARKs)
- Gabizon-Williamson-Ciobotaru: *PLONK* — IACR 2019
- Bünz et al.: *Bulletproofs* — IEEE S&P 2018
- a16z Crypto's ZK canon — `a16zcrypto.com/zero-knowledge-canon`

