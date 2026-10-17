---
title: "BBS+ Signatures"
slug: bbs-signatures
type: deep-dive
pillars: ["cryptography", "identity"]
readiness: experimental
description: "BBS+ signatures let a credential holder reveal only chosen attributes and prove the rest in zero knowledge: the scheme behind private verifiable credentials."
dek: "A pairing-based signature scheme that lets a holder prove possession of a signature on a message vector while revealing only a chosen subset of the messages. The disclosed subset, the unrevealed messages, and the original signer's identity all bind together cryptographically — but the signer never learns which attributes were shown to which verifier."
updated: 2026-04-26
created: 2026-04-26
origin: vault
source: "02-Cryptography/BBS Plus.md"
aliases: ["BBS+", "BBS Plus", "BBS Signatures"]
tags: ["bbs", "signatures", "selective-disclosure", "verifiable-credentials", "anonymous-credentials", "cryptography", "deep-dive"]
---

## What's distinctive

A BBS+ signature is over a *vector* of messages, not a single byte string. Given a signature on `(m_1, m_2, …, m_L)`:

- The holder can derive a presentation that reveals any subset `D ⊂ {1, …, L}` and proves the rest exist without disclosing them.
- The verifier learns the disclosed messages, the public key of the issuer, and a zero-knowledge proof that an issuer-signed vector satisfies the predicate.
- The verifier learns nothing about the unrevealed messages beyond what the disclosed ones imply.
- Signatures are short (one G1 point + one scalar ≈ 80 bytes for BLS12-381) and aggregatable.

This is the cryptographic backbone of "show me your driver's license but only the over-21 bit and your photo, nothing else" — the mDL / EU Digital Identity Wallet pattern.

## Origin and naming

- **BBS** (Boneh, Boyen, Shacham), *Short Group Signatures*, CRYPTO 2004 — the underlying short signature.
- **BBS+** (Au, Susilo, Mu, *Constant-Size Dynamic k-TAA*, SCN 2006; Camenisch and Lysyanskaya developed the credential-system framing in CL signatures, with BBS+ as a successor) — extends BBS to a vector of messages with efficient zero-knowledge proof of knowledge.
- The signing equation, in BLS12-381 notation:

  ```
  σ = (A, e, s) where  A = (g_1 · h_0^s · h_1^{m_1} · … · h_L^{m_L})^{1/(x + e)}
  ```

  with `x` the issuer's secret key, `e` and `s` per-signature randomness, and `h_0, …, h_L` public generators. Verification uses a pairing equation; possession can be proven in zero knowledge via a Schnorr-style sigma protocol.

## What you can do with a BBS+ signature

| Operation | Result |
|-----------|--------|
| Sign a vector `(m_1, …, m_L)` | issuer-bound credential |
| Reveal subset `D` | verifier sees `m_i for i ∈ D` and a ZK proof of validity |
| Prove a predicate over hidden messages | range proofs, set membership, equality across credentials (with extra circuits) |
| Linkable presentation (per-verifier pseudonym) | optional pseudonym binding |
| Unlinkable presentation across verifiers | default — no two presentations from the same credential are linkable |

The unlinkability is the headline. With a conventional X.509 certificate or a JWT, every presentation is bit-identical and trivially linkable; BBS+ presentations are freshly randomized every time.

## IETF standardization

The CFRG track:

- `draft-irtf-cfrg-bbs-signatures` (initially submitted 2022 by Looker, Lodder, Kalos, Whitehead and others). Active as of 2026.
- Defines BBS over **BLS12-381**, with hash-to-curve per RFC 9380.
- Specifies signing, deterministic verification, proof generation (the ZK presentation), and proof verification.
- A separate **BBS Blind Signatures** draft adds blind issuance — issuer signs without seeing the messages.
- A **Pseudonyms with BBS** draft adds verifier-binding for sybil control without compromising cross-verifier unlinkability.

The drafts have iterated several times — implementers should pin to a specific draft revision.

## Cipher suites in the draft

| Suite | Curve | Hash | Note |
|-------|-------|------|------|
| `BBS_BLS12381G1_XMD:SHA-256_SSWU_RO_` | BLS12-381 G1 | SHA-256 + SSWU | mainline |
| `BBS_BLS12381G1_XOF:SHAKE-256_SSWU_RO_` | BLS12-381 G1 | SHAKE-256 + SSWU | XOF variant |

Both fix the curve and message-encoding to BLS12-381 G1 for the disclosed-attribute side. Selecting BLS12-381 ties BBS+ deployments to the same curve as Ethereum's BLS aggregate signatures and Filecoin / Zcash, which simplifies tooling.

## Production and pilot deployments

### Hyperledger AnonCreds

The AnonCreds credential format (used in Hyperledger Indy and the broader self-sovereign-identity stack) originally used CL signatures. The 2.0 line moves to BBS+. AnonCreds adds revocation registries (cryptographic accumulators) on top of BBS+ presentations.

### W3C Verifiable Credentials with BBS+

The W3C VC Data Model is signature-agnostic. A BBS+-signed VC profile lets the holder derive a redacted VC for each verifier. Reference work and demos by the DIF (Decentralized Identity Foundation) and MATTR.

### EU Digital Identity Wallet (EUDI / eIDAS 2.0)

The EUDI Wallet specifications (ARF — Architecture and Reference Framework) reference BBS+ as one of the privacy-preserving signature options alongside SD-JWT. Pilots launched 2024–2025 with member-state issuers; production timeline is staggered through 2026–2027.

### mDL (ISO/IEC 18013-5) and adjacent profiles

The base mDL spec uses CBOR Web Tokens with SHA-256 hash-based selective disclosure, not BBS+. However, the mDL ecosystem has explored BBS+ as a future profile for stronger unlinkability — current mDL presentations leak a per-credential identifier across verifiers, which BBS+ would eliminate.

### MATTR, Trinsic, Spruce ecosystem

Several SSI vendors ship BBS+ in production credential issuance flows for B2B identity. Volumes are in the millions, not billions.

## BBS+ vs SD-JWT

The two compete head-to-head for selective-disclosure credentials.

| Property | BBS+ | SD-JWT |
|----------|------|--------|
| Cryptographic basis | pairing (BLS12-381) | hash + JWS (any curve) |
| Selective disclosure | algebraic, signer-blind | hash-based (`_sd` claims) |
| Cross-verifier unlinkability | yes (default) | no — the JWS stays the same |
| Verifier sees presentation count | ZK each time | yes, identical artifact |
| Predicates over hidden values | possible (range, set membership with extra ZK) | no |
| Tooling maturity (2026) | growing, library-fragmented | broad — fits existing JWT stacks |
| Quantum-safe | no (pairing-broken by Shor) | partial — JWS-PQ profile exists; hash side is PQ |
| IETF status | CFRG draft | RFC 8949 + draft-ietf-oauth-selective-disclosure-jwt |

Pragmatically: SD-JWT is winning on adoption because it slots into existing OAuth/OIDC flows. BBS+ wins on cryptographic privacy guarantees. The EU and several national wallets carry both as parallel profiles.

## BBS+ vs CL signatures

CL (Camenisch-Lysyanskaya) signatures predate BBS+ and were the original choice in AnonCreds 1.0. BBS+ is preferred now because:

- Smaller signatures (single curve point vs RSA-large).
- Faster verification on modern hardware.
- Cleaner integration with BLS-curve tooling (no separate RSA setup).

CL is still in older AnonCreds deployments and in some legacy academic credential systems.

## Aggregation and threshold

BBS+ supports **issuer aggregation** — multiple issuer signatures over the same message vector compress to a single proof of validity (with per-issuer public keys). Used for multi-issuer attestations.

**Threshold BBS+** issuance is an active research area. Doerner, Kondi, Lee, Shelat and others have published threshold-friendly variants (2023–2024). Production implementations are sparse as of 2026.

## Trade-offs

### Strengths

- Unlinkable presentations across verifiers.
- Selective disclosure without trusted hardware.
- Compact signatures and proofs.
- Composable with predicate proofs (range, equality, set membership).

### Limitations

- **Pairing-based — broken by quantum.** No drop-in PQ replacement; lattice-based selective-disclosure schemes (e.g., LaBRADOR-derived constructions, BBS-inspired lattice variants) are research-stage with much larger artifacts.
- **Implementation maturity.** Fewer production-grade libraries than SD-JWT. Reference implementations exist in Rust (`pairing-crypto`, `bbs`), TypeScript (`@mattrglobal/bbs-signatures`), and Go.
- **Side-channel surface.** Pairing arithmetic is delicate; constant-time pairing implementations are not as ubiquitous as constant-time elliptic-curve code.
- **Revocation.** BBS+ alone does not provide revocation; it must be paired with an accumulator (see [Authenticated Data Structures](/kb/authenticated-data-structures/)) or a status list (StatusList2021).
- **Issuer compromise.** A leaked issuer key forges all credentials; revocation/rotation strategies are critical.

## Pitfalls

- **Don't reuse domain separators.** The hash-to-scalar and hash-to-curve domain tags are part of the cipher suite — mixing suites breaks unlinkability and security.
- **Don't expose `e` or `s`.** They are per-signature randomness; revealing them links the presentation to the original signature.
- **Pin draft versions.** The CFRG draft has changed parameter encodings between revisions.
- **Watch unlinkability scope.** Network metadata (TLS session, IP) trivially de-anonymizes BBS+ presentations. Use Tor / mixnets for full unlinkability across verifiers.

## Primary sources

- Boneh, Boyen, Shacham, *Short Group Signatures*, CRYPTO 2004.
- Au, Susilo, Mu, *Constant-Size Dynamic k-TAA*, SCN 2006.
- Camenisch, Drijvers, Lehmann, *Anonymous Attestation Using the Strong Diffie Hellman Assumption Revisited*, TRUST 2016.
- Tessaro, Zhu, *Revisiting BBS Signatures*, EUROCRYPT 2023 — modern security proof.
- IRTF/CFRG, *The BBS Signature Scheme*, draft-irtf-cfrg-bbs-signatures (active, 2025).
- IRTF/CFRG, *BBS per-Verifier Linkability*, draft-irtf-cfrg-bbs-per-verifier-linkability.
- ISO/IEC 18013-5, *Personal identification — ISO-compliant driving licence — Mobile driving licence (mDL) application*, 2021.
- W3C Verifiable Credentials Data Model 2.0, 2024.
- Reference Rust impl: [github.com/mattrglobal/pairing_crypto](https://github.com/mattrglobal/pairing_crypto).
- Hyperledger AnonCreds: [github.com/hyperledger/anoncreds-spec](https://github.com/hyperledger/anoncreds-spec).
