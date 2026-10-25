---
title: "Verifiable Random Functions (VRFs)"
slug: verifiable-random-functions
type: explainer
pillars: ["cryptography"]
readiness: usable
description: "Verifiable random functions give pseudorandom outputs plus a proof the key holder computed them correctly, used in consensus and key transparency."
dek: "A pseudorandom function whose outputs come with a non-interactive proof that the holder of a secret key produced them correctly. Anyone with the public key can verify the output is the unique value the keyholder committed to."
updated: 2026-10-25
created: 2026-04-26
origin: vault
source: "02-Cryptography/VRFs.md"
aliases: ["VRF", "Verifiable Random Function", "ECVRF"]
tags: ["vrf", "ecvrf", "randomness", "cryptography", "deep-dive", "rfc-9381"]
---

## Definition

A VRF is a triple `(KeyGen, Prove, Verify)`:

- `KeyGen() → (sk, pk)`
- `Prove(sk, α) → (β, π)` where `α` is an input, `β` the pseudorandom output, `π` the proof.
- `Verify(pk, α, β, π) → {accept, reject}`

Three properties matter:

1. **Pseudorandomness.** Without `sk`, `β` is indistinguishable from random for an adversary that hasn't queried `α`.
2. **Uniqueness.** For each `(pk, α)` there is exactly one `β` for which any valid proof exists. The keyholder cannot pick between multiple outputs.
3. **Collision-resistance** of the input-to-output map under the proof check.

The combination is the point: a PRF gives pseudorandomness, a signature gives verifiability, but a VRF binds the two so the holder cannot grind multiple "random" outputs and pick the favorable one.

Originally defined by Micali, Rabin and Vadhan (FOCS 1999).

## Relation to nearby primitives

| Primitive | Pseudorandom | Publicly verifiable | Unique per `(pk, α)` |
|-----------|--------------|---------------------|----------------------|
| PRF | yes | no | yes (secret) |
| Hash-then-sign | depends | yes | no (signatures rerandomize) |
| Deterministic signature (e.g. RFC 6979 ECDSA) | yes | yes | depends on scheme |
| **VRF** | **yes** | **yes** | **yes** |

A naive "sign the input, hash the signature" construction fails uniqueness for any signature scheme that admits multiple valid signatures (ECDSA, Schnorr with random nonces). VRFs require a scheme designed for the property.

## Constructions

### ECVRF

Goldberg, Reyzin, Papadopoulos and Včelák, *Verifiable Random Functions* — the IRTF/CFRG track that became **RFC 9381** (August 2023). Construction:

```
H = hash_to_curve(pk || α)
Γ = sk · H
β = hash(Γ)
π = (Γ, c, s)         where c, s are a Schnorr-style proof
                      that log_H(Γ) = log_G(pk) = sk
```

Verification recomputes `H`, checks the Schnorr equation, then derives `β` from `Γ`. Uniqueness comes from the fact that a single point `Γ = sk·H` exists per `(sk, α)`.

RFC 9381 specifies four ECVRF suites (and a separate RSA-FDH-VRF construction):

| Suite | Curve | Hash-to-curve |
|-------|-------|---------------|
| `ECVRF-P256-SHA256-TAI` | NIST P-256 | try-and-increment |
| `ECVRF-P256-SHA256-SSWU` | NIST P-256 | Simplified SWU (RFC 9380) |
| `ECVRF-EDWARDS25519-SHA512-TAI` | edwards25519 | try-and-increment |
| `ECVRF-EDWARDS25519-SHA512-ELL2` | edwards25519 | Elligator2 |


Try-and-increment leaks timing on `α` (the number of iterations is input-dependent); SSWU and Elligator2 are constant-time and preferred for new deployments.

### ristretto255 / Ristretto-VRF

A non-RFC variant over the ristretto255 prime-order group, used inside Polkadot (sr25519, schnorrkel) and similar systems. Equivalent security argument with a clean group structure.

### BLS-based VRF

Pairing-based VRF where `β = e(sk·H(α), g)`. Shorter outputs but pairing verification is slower than elliptic-curve-only ECVRF. Used in some consensus designs (early DFINITY).

## Applications

### Algorand consensus self-selection

Each round, a committee is sampled by having every account compute `VRF(sk_account, seed_round)` and check whether the output falls below a stake-weighted threshold. Self-selection is private until the player publishes its proof, which makes the committee unpredictable to an attacker until the moment members reveal themselves. Chen and Micali, *Algorand* (2017).

### Chainlink VRF

Off-chain oracle holds the VRF secret key, smart contract sends a request, oracle responds with `(β, π)`. The contract verifies `π` on-chain. The output is the source for lotteries, NFT minting, gaming randomness. Trust assumption: the oracle (and that the request seed includes a recent block hash so the oracle cannot pre-grind).

### DNSSEC NSEC5

Goldberg and co-authors proposed replacing NSEC3 (which leaks a hash of every name in the zone via dictionary attack) with a VRF-authenticated negative response. The zone signs `VRF(α)` for every name; a non-existence proof reveals the VRF output for the queried name without enabling offline enumeration. Proposed in `draft-vcelak-nsec5` (now expired); influenced production thinking but not deployed.

### Cloudflare Privacy Pass

Original Privacy Pass (Davidson, Goldberg, Sullivan, 2018) and the IETF Privacy Pass standardization use a related primitive (verifiable oblivious PRF, VOPRF) which is a two-party VRF where the client provides a blinded input. The same uniqueness logic — a token cannot be redeemed twice for different values — relies on the VRF property.

### Nostr and federated systems

Several Nostr relay-selection and committee-rotation proposals use VRF-based sortition. Same logic as Algorand: unpredictable, self-verifiable selection.

## VRF vs commit-reveal randomness

| Property | Commit-reveal | VRF | VRF + on-chain seed |
|----------|---------------|-----|---------------------|
| Round trips | 2 (commit, reveal) | 1 | 1 |
| Bias by withholding a result | yes | possible | possible |
| Bias by choosing input | n/a | grind seed before commit | block-hash seed mitigates |
| Public verifiability | after reveal | immediate | immediate |
| Operator can withhold | yes (drops) | yes (refuse to publish) | yes (but seed is public) |

A VRF fixes the output for a given public key and input, but the keyholder can still withhold an unfavorable result. Fixing the input in advance limits input grinding; a surrounding protocol must also address withholding. See [VDFs](/kb/verifiable-delay-functions/) for the complementary problem of the input itself being predictable far in advance.

## Security assumptions

- ECVRF on NIST/edwards/secp curves: discrete-log hardness in the corresponding group, plus random-oracle assumptions for the hash-to-curve and challenge derivation.
- Side-channel: `sk` use must be constant-time. Try-and-increment hash-to-curve leaks timing; SSWU/Elligator2 preferred.
- Quantum: all listed VRFs are broken by Shor. Lattice-based VRFs are research-stage as of 2026 (Esgin et al., constructions are concretely large).

## Standardization state

- **RFC 9381** (Aug 2023): IRTF/CFRG-published VRF specification with four ECVRF cipher suites. Stable; multiple production implementations.
- **draft-irtf-cfrg-vrf-15** preceded the RFC; older deployments may pin to specific drafts.
- No NIST profile yet. NIST has not standardized VRFs separately from broader random-beacon work.

## Implementation notes

- Reference: `c2sp/vrf-r255` (Filippo Valsorda) for ristretto255 ECVRF.
- Algorand's `go-algorand` ships its own audited ECVRF implementation.
- Chainlink VRF v2/v2.5 uses a Solidity verifier for `ECVRF-secp256k1-SHA256`.

- Constant-time hash-to-curve is non-trivial; pin to RFC 9380 SSWU/Elligator2 implementations rather than rolling your own.

## Trade-offs

### Strengths

- One round of communication.
- Unbiasable by the keyholder once the input is fixed.
- Compact proofs (~80 bytes for edwards25519 ECVRF).
- Composable with VDFs and beacon protocols.

### Limitations

- Single-key trust. The keyholder still chooses *when* to publish; censorship by withholding is the residual attack.
- Input grinding if `α` is attacker-chosen.
- Quantum-vulnerable on every standardized curve.
- Pseudorandomness only — not a verifiable delay; for unpredictable-future randomness add a VDF or beacon.

## Primary sources

- [RFC 9381: Verifiable Random Functions](https://www.rfc-editor.org/rfc/rfc9381.html)
- [RFC 9380: Hashing to Elliptic Curves](https://www.rfc-editor.org/rfc/rfc9380.html)
- [Chen and Micali: Algorand](https://arxiv.org/abs/1607.01341)
- [NSEC5: Provably Preventing DNSSEC Zone Enumeration](https://eprint.iacr.org/2014/582)
- [Micali, Rabin and Vadhan: Verifiable Random Functions](https://people.seas.harvard.edu/~salil/research/VRF-abs.html)
- [Privacy Pass: Bypassing Internet Challenges Anonymously](https://petsymposium.org/2018/files/papers/issue3/popets-2018-0026.pdf)
