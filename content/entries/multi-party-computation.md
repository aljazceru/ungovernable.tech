---
title: "Multi-Party Computation"
slug: multi-party-computation
type: explainer
pillars: ["cryptography"]
readiness: usable
description: "Secure multi-party computation lets parties compute a function over their private inputs while learning nothing else: protocols, tools and uses."
dek: "Cryptographic protocols where parties jointly compute a function over their private inputs while learning nothing beyond the output. The defining property: no party (including all attackers up to a threshold) sees inputs other than its own."
updated: 2026-10-25
created: 2026-04-25
origin: vault
source: "02-Cryptography/Multi-Party Computation.md"
aliases: ["MPC", "Secure Multi-Party Computation", "SMPC"]
tags: ["mpc", "multi-party-computation", "threshold-signatures", "frost", "gg20", "deep-dive", "cryptography"]
---

## What MPC provides

Three parties want the average of their salaries without revealing them. A bank wants to know if a customer's wallet balance exceeds a threshold without learning the balance. A genomics consortium wants population statistics without pooling raw genomes. A signing committee wants a Bitcoin transaction signed without any single member holding the key.

All of these are MPC. The shared abstraction:

```
party_1 (input x_1) ─┐
party_2 (input x_2) ─┼─► joint protocol ─► f(x_1, x_2, …, x_n) ─► all parties
…                    │
party_n (input x_n) ─┘
```

What's hidden: every input except your own. What's revealed: only `f`'s output (and whatever the output reveals about inputs).

## Security models

| Model | Adversary | Defends against |
|-------|-----------|-----------------|
| **Semi-honest** | Follows the protocol but tries to learn inputs from messages | Curious-but-honest peer |
| **Malicious** | Deviates arbitrarily (lies, withholds, sends garbage) | Active attacker |
| **Covert** | Cheats with non-trivial detection probability | Risk-averse attacker |
| **Honest-majority** | < n/2 parties corrupt | Majority assumption |
| **Dishonest-majority** | Up to n−1 parties corrupt | Strongest guarantee |

Practical systems pick a point on these axes. Threshold signatures (FROST, GG20) typically target malicious plus dishonest-majority, the strongest model with the most overhead.

## Foundational techniques

### Secret sharing

A secret `s` split into `n` shares such that any `t` reconstruct it; `t-1` reveal nothing. Shamir's Secret Sharing (1979) does this with polynomial interpolation:

```
P(x) = s + a_1·x + a_2·x² + … + a_{t-1}·x^{t-1}   (random a_i)
share_i = P(i)
```

Reconstruction: Lagrange interpolation over any `t` shares.

### Garbled circuits (Yao, 1986)

For two-party computation: encode the function as a Boolean circuit, garble each gate's truth table with random keys, send to the evaluator. The evaluator decrypts only the path corresponding to the inputs and never sees intermediate wire values. Modern variants: half-gates, fixed-key AES (free XOR).

### Oblivious Transfer (OT)

Sender has two messages `m_0`, `m_1`; receiver has a bit `b`. Receiver learns `m_b`; sender learns nothing about `b`. The bedrock primitive: virtually all 2PC reduces to OT. OT extension makes large numbers of OTs cheap.

### BGW / GMW protocols

Honest-majority arithmetic circuit MPC via additive secret sharing of inputs and per-gate communication for multiplications. Foundation of practical honest-majority systems.

### SPDZ

Dishonest-majority MPC with information-theoretic MACs to detect malicious behavior. Active-secure even when n−1 parties are malicious. Used for high-stakes joint computation in industry.

## Threshold cryptography

A specialization of MPC: instead of a generic `f`, the function is a cryptographic operation (signing, decryption). Properties:

- **Threshold signatures.** `t` of `n` parties cooperate to sign; `t−1` cannot. The output looks identical to a normal single-key signature (no on-chain flag that it's threshold).
- **Threshold decryption.** A ciphertext encrypted to a threshold key is decrypted only with `t` cooperating partial decryptions.

### Schnorr threshold (FROST)

Komlo & Goldberg (2020), standardized as **RFC 9591** (2024). Two-round signing protocol with several ciphersuites, including Ed25519 and secp256k1. Bitcoin Taproot requires BIP-340-compatible handling; generic RFC 9591 secp256k1 signatures are not a drop-in replacement. Used for:

- Bitcoin Taproot multisig that looks like single-sig on-chain.
- Nostr threshold key custody (research and early production).
- Lightning node operator key sharding.

FROST supports threshold signing; MuSig2 is an n-of-n multisignature protocol. They address different participation requirements.

### ECDSA threshold (GG20, CMP)

Gennaro-Goldfeder 2018/2020 and follow-ups. ECDSA is harder to threshold than Schnorr because of its non-linear structure; protocols are more complex with more rounds. Used by:

- Fireblocks, Coinbase Custody, Anchorage for institutional key custody.
- Bitcoin pre-Taproot multi-party signing where on-chain visibility of a multisig is unacceptable.

### MuSig2

Schnorr multi-signature aggregation (BIP-327). Two rounds, n-of-n only. Differs from FROST in that all signers must participate; FROST tolerates `t < n`.

## Use cases by adversary class

| Use case | Typical setup | Why MPC |
|----------|---------------|---------|
| Threshold custody | t-of-n FROST or GG20 | Key never reconstructed in one place |
| Joint analytics | SPDZ over arithmetic circuits | Joint statistics without pooling raw data |
| Federated eCash mints (Fedimint) | Threshold blind signatures | No single guardian can issue alone; a signing quorum remains trusted |
| MPC-based RNG / DKG | Distributed key generation | Sample a key no party knows |
| Auctions / voting | Garbled circuits or honest-majority arithmetic | Bid privacy with public verifiability |
| ZK proof generation | Distributed prover | Avoid centralizing the proving key |
| Confidential ML inference | MPC vs FHE-or-TEE | Splits the trust into multiple non-colluders |

## MPC vs FHE vs ZK vs TEE

These primitives often get conflated. Quick distinction:

| Primitive | Hides | Trust model |
|-----------|-------|-------------|
| **MPC** | Inputs from peer parties | Threshold of parties non-colluding |
| **FHE** | Plaintext from compute provider | Math (lattice hardness) |
| **ZK** | Witness from verifier | Math (under setup assumptions) |
| **TEE** | RAM from cloud / OS / hypervisor | Hardware vendor |

They compose. FHE+MPC distributes the FHE secret key across parties so no single one can decrypt. ZK+MPC lets parties produce a proof neither would produce alone. TEE+MPC lowers the threshold (each TEE-attested party is harder to corrupt than a software-only party).

## Production libraries

| Library | Language | Focus |
|---------|----------|-------|
| **mp-spdz** | C++ | SPDZ-family research/benchmark suite |
| **MP-SPDZ-style cloud** (e.g. Pyte, Sharemind) | Various | Honest-majority production analytics |
| **frost-secp256k1**, **frost-ed25519** | Rust | RFC 9591 reference implementations |
| **ZenGo / multi-party-ecdsa** | Rust | GG18/GG20 ECDSA threshold |
| **CMP / Lit Protocol** | Rust + JS | ECDSA threshold for Web3 wallet custody |
| **EMP-toolkit** | C++ | Garbled circuits, semi-honest 2PC |

## Operational patterns

### Threshold custody

Replace 2-of-3 hardware-wallet multisig with a 2-of-3 FROST signing committee where the on-chain output is a single Schnorr signature. Trade-offs: better privacy and cheaper on-chain, but more protocol complexity off-chain (signers must coordinate two rounds for each signature).

### Distributed trusted setup

Generate Groth16 or PLONK trusted setup parameters via MPC ceremony (the "Powers of Tau"). Any single honest contributor among thousands suffices for soundness. Used by Zcash, Filecoin, Aleo, Aztec.

### Confidential ML inference (MPC variant)

Two non-colluding servers each hold a share of the model weights and the input. Inference proceeds with per-layer MPC arithmetic. Trade-off vs FHE: faster (often by orders of magnitude) but requires a non-collusion assumption.

### Federated eCash mints

Fedimint distributes mint authority across guardians using threshold blind signatures. Cashu’s basic protocol uses a mint signing key and does not itself require a threshold federation.

## Trade-offs

### Strengths

- No single point of trust. The secret is distributed across `n` parties.
- Strong literature on what guarantees hold under what assumptions.
- Composable with FHE, ZK, and TEEs.
- Output indistinguishability. Threshold signatures look like normal sigs on-chain.

### Limitations

- Communication-heavy. Many rounds, large messages, orders of magnitude slower than centralized computation.
- Liveness assumptions. Threshold protocols halt if too few parties online.
- Setup ceremony. Distributed key generation (DKG) is its own protocol with its own trust assumptions.
- Operational complexity. Coordinating signers across organizations is hard; tooling is improving but not consumer-grade.
- Side-channel surface. Each party's local execution leaks (timing, memory). High-stakes use needs TEE or formally-verified implementations.

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Threshold-1 collusion | Geographic / organizational diversity of signers |
| Malicious key generation | DKG with verifiable secret sharing (VSS) |
| Replay / reorder of messages | Per-protocol nonces + transcripts |
| Side-channel on a signer | Run signers in TEEs |
| Liveness DoS | t-of-n with t < n; design slack into threshold |
| Implementation bugs | Audited libraries (frost-rs, multi-party-ecdsa); fuzzing |

## Recent developments (2024-2026)

- FROST standardization as **RFC 9591** (June 2024).
- Production threshold custody at scale (Coinbase, Fireblocks, BitGo) with billions in AUM.
- DKG ceremony tooling matured; simpler bootstrapping for new threshold groups.
- Active-secure variants of FROST and GG20 with proven simulators.
- Mobile MPC SDKs (ZenGo, Lit Protocol). Distributed wallets without hardware keys.
- MPC-in-the-head signature schemes (such as Picnic) explored for PQ.

## Primary sources

- [Yao: Protocols for Secure Computations](https://research.cs.wisc.edu/areas/sec/yao1982-ocr.pdf)
- [Completeness Theorems for Non-Cryptographic Fault-Tolerant Distributed Computation](https://www.math.ias.edu/~avi/PUBLICATIONS/MYPAPERS/GBW88/GBW88.pdf)
- [Multiparty Computation from Somewhat Homomorphic Encryption](https://eprint.iacr.org/2011/535)
- [FROST: Flexible Round-Optimized Schnorr Threshold Signatures](https://eprint.iacr.org/2020/852)
- [RFC 9591: FROST](https://www.rfc-editor.org/rfc/rfc9591.html)
- [UC Non-Interactive, Proactive, Threshold ECDSA](https://eprint.iacr.org/2020/492)
- [Secure Multiparty Computation (MPC)](https://eprint.iacr.org/2020/300)
- [MP-SPDZ implementation](https://github.com/data61/MP-SPDZ)
- [FROST implementation](https://github.com/ZcashFoundation/frost)
- [MuSig2: BIP 327](https://github.com/bitcoin/bips/blob/master/bip-0327.mediawiki)
- [Fedimint protocol](https://github.com/fedimint/fedimint)
- [Cashu NUT-00](https://github.com/cashubtc/nuts/blob/main/00.md)
- [Fast Secure Two-Party ECDSA Signing](https://eprint.iacr.org/2017/552)
