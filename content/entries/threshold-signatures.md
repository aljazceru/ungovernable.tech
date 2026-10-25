---
title: "Threshold Signatures"
slug: threshold-signatures
type: explainer
pillars: ["cryptography", "money"]
description: "Threshold signatures let any t of n parties sign while t-1 cannot: FROST, MuSig and threshold ECDSA, and their use in custody and protocols."
dek: "Signing protocols where any `t` of `n` parties can produce a signature, and `t−1` cannot. The output is indistinguishable from a single-key signature: an on-chain verifier doesn't need to know the signature was threshold-produced. The whole construction is a special case of MPC, narrowed to the signing function."
updated: 2026-04-26
created: 2026-04-26
origin: vault
source: "02-Cryptography/Threshold Signatures.md"
aliases: ["Threshold Signing", "t-of-n Signatures"]
tags: ["threshold-signatures", "frost", "gg18", "gg20", "cmp", "dkls", "bls", "schnorr", "ecdsa", "mpc", "cryptography", "deep-dive"]
---

## Why threshold instead of multisig

A 2-of-3 P2SH/P2WSH multisig in Bitcoin lists three public keys on-chain and reveals which two signed. Costs and privacy implications:

- Larger transaction (multiple keys + multiple sigs).
- Public knowledge of the policy structure.
- Fingerprintable as multisig output.

Threshold signatures collapse `t-of-n` cooperation into a *single* signature under a *single* public key. On-chain it's indistinguishable from single-sig. The complexity moves off-chain, into the signing protocol that the `t` cooperating signers run.

## What threshold protocols must solve

| Problem | Solution component |
|---------|-------------------|
| No party ever holds the full secret key | Distributed Key Generation (DKG) |
| Any `t` parties can sign | t-of-n secret sharing of `sk` |
| Fewer than `t` learn nothing | secrecy of shares + zero-knowledge proofs |
| Party going offline doesn't break the group | DKG + key resharing |
| Malicious party producing a wrong share | verifiable secret sharing (VSS) |
| Replay or reorder of signing rounds | per-session nonces, transcripts |

DKG is its own protocol — see Pedersen 1991 (the canonical VSS-based DKG) and Gennaro et al. 1999 for the JF-DKG variant fixing biases in Pedersen. Many production protocols specify DKG separately from the signing protocol.

## Schnorr threshold: FROST

Komlo and Goldberg, *FROST: Flexible Round-Optimized Schnorr Threshold Signatures*, IACR 2020/852. Standardized as **RFC 9591** (Sep 2024).

Two-round signing:

```
round 1: each signer publishes a pair of nonce commitments (D_i, E_i)
round 2: signers compute the binding factor, derive group commitment R,
         each contributes its share s_i = d_i + e_i · ρ_i + λ_i · sk_i · c
final:   signature σ = (R, s) where s = Σ s_i
```

Properties:

- Two rounds (lower than three-round Stinson-Strobl variants).
- Compatible with `secp256k1` (Bitcoin) and Ed25519.
- Concurrent-signing-safe with the binding factor (the original FROST paper had a subtle issue under aggressive concurrency; RFC 9591 specifies the binding-factor mitigation).
- Identifiable abort: cheaters are detectable.

### ROAST

Ruffing, Ronge, Jin, Schneider-Bensch, *ROAST: Robust Asynchronous Schnorr Threshold Signatures*, CCS 2022. Wraps FROST with retry semantics so the protocol completes even if a minority of signers go offline mid-protocol. Used where liveness matters more than minimizing rounds (Lightning, custody).

### FROST3 / FROST round-1 batching

Newer drafts and ports add per-signer pre-shared nonce caches for ahead-of-time round 1, reducing signing latency to a single online round. Trade-off: nonce reuse risk if cache state isn't tracked carefully.

## ECDSA threshold

ECDSA's non-linearity (the signature involves division by the nonce) makes threshold harder than Schnorr. Heavyweight constructions:

### GG18 / GG20

Gennaro and Goldfeder, *Fast Multiparty Threshold ECDSA with Fast Trustless Setup*, CCS 2018 (GG18); follow-up GG20 (2020) tightens the security proof and reduces rounds.

- Multi-round protocol (typically 6+ rounds for signing).
- Uses Paillier homomorphic encryption inside to multiply shares securely.
- Active-secure variants require zero-knowledge proofs at each Paillier step.

### CMP

Canetti, Makriyannis, Peled, *UC Non-Interactive, Proactive, Threshold ECDSA*, CCS 2020 / IACR 2020/492. Drops Paillier setup overhead via different primitives, formalized in UC framework. Used by some custody platforms in production.

### DKLs (Doerner, Kondi, Lee, Shelat)

A line of work optimizing threshold ECDSA via OT-based multiplication instead of Paillier:

- *Secure Two-party Threshold ECDSA from ECDSA Assumptions*, S&P 2018.
- *Threshold ECDSA from ECDSA Assumptions: The Multiparty Case*, S&P 2019.
- *Threshold ECDSA in Three Rounds*, S&P 2024.

DKLs23 / DKLs24 reach three-round ECDSA threshold signing without Paillier. Faster on commodity hardware than GG-line protocols, with a different setup story.

## BLS threshold

BLS (Boneh, Lynn, Shacham) signatures are uniquely friendly to thresholdization:

```
sign:    σ_i = sk_i · H(m)        (each signer computes locally, no rounds)
combine: σ = Σ λ_i · σ_i           (Lagrange combine)
verify:  e(g, σ) =? e(pk, H(m))
```

Properties:

- **Non-interactive signing.** Signers don't need to coordinate online; partial sigs combine algebraically.
- **Aggregation.** Many signatures on the same message compress to a single curve point.
- **Compact.** ~96 bytes per signature on BLS12-381 G2 (or 48 bytes on G1, depending on profile).

Used by:

- **Ethereum** validator attestations (BLS12-381 G2 sigs aggregated per slot).
- **Filecoin** consensus.
- **Chia** signatures.
- **drand** randomness beacon (League of Entropy).
- **Cosmos / Tendermint** experiments.

Caveats:

- Pairing arithmetic is heavier than Schnorr.
- BLS DKG is its own non-trivial protocol; rogue-key attacks require proof-of-possession or message-prefixing as in BLS-MPL.
- Quantum-broken (Shor on the pairing curve).

## Comparison by curve

| Curve | Scheme | Standardization | Production |
|-------|--------|-----------------|------------|
| `secp256k1` | FROST-Schnorr | RFC 9591 | Bitcoin Taproot multisig (BIP-340 verifiers) |
| `secp256k1` | GG20 / DKLs | none (academic) | Custody platforms (Fireblocks, Coinbase, BitGo) |
| Ed25519 | FROST | RFC 9591 cipher suite | Solana experiments, Nostr custody |
| `secp256r1` (P-256) | FROST | RFC 9591 cipher suite | enterprise / FIDO2 adjacent |
| BLS12-381 G2 | BLS threshold | IETF blog draft + ad-hoc specs | Ethereum, Filecoin, drand |
| Ristretto255 / sr25519 | FROST-style | community | Polkadot / Substrate |

## Production deployments

### Bitcoin: FROST-Bitcoin, BIPs

A draft BIP for FROST threshold Schnorr over `secp256k1` (BIP authors include Tim Ruffing, Jonas Nick, Yannick Seurin) reached active discussion in 2024. Reference implementations (`secp256k1-zkp`, `frost-secp256k1-tr`). Goal: 2-of-3 cold storage that looks like Taproot single-sig on-chain. Adoption is gated on tooling; Sparrow, BlueWallet, and Nunchuk have explored integration.

### Nostr: Frostr / NIP drafts

Frostr ([github.com/cmdruid/frost](https://github.com/cmdruid/frost), draft NIP) lets a Nostr key be split across devices for recovery without a single point of compromise. Niche but active.

### Lightning channel keys

Lightning per-channel keys (revocation, payment, htlc) are candidates for threshold-Schnorr custody once the spec stabilizes. Some operator-tier setups use threshold ECDSA today via custody vendors.

### MPC custody platforms

| Platform | Curves | Algorithm family |
|----------|--------|------------------|
| Fireblocks | secp256k1, Ed25519, etc. | GG-line + custom |
| Coinbase Custody | secp256k1, BLS | DKLs + BLS |
| Anchorage | various | hardware-rooted MPC |
| BitGo | secp256k1 | TSS (GG-derived) |
| ZenGo (now part of Coinbase) | secp256k1 | GG18 / DKLs |
| Lit Protocol | secp256k1, BLS | DKG + threshold signing for general programmable custody |

Aggregate AUM through MPC custody crossed double-digit billions of USD by 2024.

### Ethereum and proof-of-stake

Ethereum's beacon chain uses BLS threshold-friendly aggregation (not signer-thresholding per-validator, but aggregating per-slot attestations). Several staking pools use threshold-BLS (Obol's Distributed Validator Technology, SSV Network) to split validator keys across operators.

## Trade-offs by curve

| Property | Schnorr / Ed25519 / FROST | ECDSA / GG20-DKLs | BLS threshold |
|----------|---------------------------|-------------------|---------------|
| Signing rounds | 2 | 3–6 | 1 (non-interactive) |
| DKG complexity | moderate | high | moderate |
| On-chain size (one sig) | ~64 B | ~71 B (DER) | ~96 B (G2) or 48 B (G1) |
| Aggregation | partial (MuSig2) | hard | excellent |
| Bitcoin compatibility | yes (Taproot) | yes (legacy) | no |
| Ethereum L1 compatibility | no (yet) | yes (precompiles) | yes (BLS precompile) |
| Security proof maturity | strong (RFC 9591) | strong but newer | strong |
| Quantum safety | no | no | no |
| Library ecosystem | growing | mature in custody | mature in PoS |

Pick FROST when you control the verifier (Bitcoin Taproot, Solana, Nostr).
Pick threshold ECDSA when you must produce a legacy ECDSA signature (Bitcoin pre-Taproot, Ethereum txs from EOAs).
Pick threshold BLS when aggregation matters and the verifier supports BLS (PoS chains, drand).

## Pitfalls

- **DKG is the hard part.** A flawed DKG biases the group key in subtle ways; production deployments use audited DKG (Pedersen + JF or similar).
- **Nonce reuse breaks Schnorr/ECDSA threshold catastrophically.** State must be carefully tracked across rounds.
- **Concurrent signing without binding factors leaks the secret key.** RFC 9591's binding-factor construction is non-negotiable for FROST.
- **Rogue-key attacks** in BLS aggregation: every aggregator must verify proof-of-possession or use distinct domain separation.
- **Side-channels.** Each signer's local execution leaks (timing, EM, memory). High-stakes deployments run signers inside TEEs or formally-verified contexts.
- **Liveness.** `t < n` is required for liveness; choosing `t = n` means any single offline signer halts the group.
- **Resharing protocols** to change `t`, `n`, or the participant set are separate protocols and have their own security stories.

## Composability

- **TEE + threshold:** each signer runs inside an SGX/TDX enclave, raising the cost of corrupting any one share. Useful when `n` is small (2-of-3) and operational diversity is hard.
- **MPC + threshold:** the signing committee itself runs an inner MPC for, e.g., signing-with-policy without revealing the policy to verifiers.
- **ZK + threshold:** prove the threshold signature was produced over a hidden message satisfying a predicate.
- **Threshold VRF:** combines the unbiasability of [VRFs](/kb/verifiable-random-functions/) with the trust-distribution of threshold signing.

## Primary sources

- Pedersen, *A Threshold Cryptosystem without a Trusted Party*, EUROCRYPT 1991.
- Gennaro, Jarecki, Krawczyk, Rabin, *Secure Distributed Key Generation for Discrete-Log Based Cryptosystems*, EUROCRYPT 1999.
- Boneh, Lynn, Shacham, *Short Signatures from the Weil Pairing*, ASIACRYPT 2001.
- Komlo, Goldberg, *FROST: Flexible Round-Optimized Schnorr Threshold Signatures*, IACR 2020/852.
- Connolly, Komlo, Goldberg, *Two-Round Threshold Schnorr Signatures with FROST*, RFC 9591 (Sep 2024).
- Gennaro, Goldfeder, *Fast Multiparty Threshold ECDSA with Fast Trustless Setup*, CCS 2018; GG20 follow-up.
- Canetti, Makriyannis, Peled, *UC Non-Interactive, Proactive, Threshold ECDSA*, CCS 2020.
- Doerner, Kondi, Lee, Shelat, *Threshold ECDSA in Three Rounds*, IEEE S&P 2024.
- Ruffing, Ronge, Jin, Schneider-Bensch, *ROAST: Robust Asynchronous Schnorr Threshold Signatures*, CCS 2022.
- frost-secp256k1: [github.com/ZcashFoundation/frost](https://github.com/ZcashFoundation/frost).
- multi-party-ecdsa (ZenGo / Coinbase): [github.com/ZenGo-X/multi-party-ecdsa](https://github.com/ZenGo-X/multi-party-ecdsa).
- BLS reference: [github.com/supranational/blst](https://github.com/supranational/blst).
- Frostr (Nostr): [github.com/cmdruid/frost](https://github.com/cmdruid/frost).

Continue with [drand and tlock](/kb/drand-tlock/).
