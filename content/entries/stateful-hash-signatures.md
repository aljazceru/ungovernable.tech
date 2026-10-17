---
title: "Stateful Hash-Based Signatures (XMSS, LMS)"
slug: stateful-hash-signatures
type: deep-dive
pillars: ["pqc"]
readiness: usable
description: "XMSS and LMS, stateful hash-based signatures: small, conservative post-quantum signatures that are safe only if the signer never reuses state."
dek: "The narrow-but-bulletproof PQ signature option: smaller than SLH-DSA, hash-only assumption, but you must track the signed-index. Reusing an index breaks the scheme. NIST SP 800-208 (October 2020) blesses these for code signing and firmware updates only."
updated: 2026-04-26
created: 2026-04-26
origin: vault
source: "10-Post-Quantum/Stateful Hash Signatures.md"
aliases: ["XMSS", "LMS", "Stateful Hash-Based Signatures"]
tags: ["xmss", "lms", "hash-based", "signatures", "stateful", "rfc-8391", "rfc-8554", "post-quantum", "deep-dive"]
---

## What stateful means

A stateful hash-based signature scheme uses a tree of one-time signature keys. Each leaf can sign exactly once. The signer must:

1. Track which leaves have been used.
2. Persist that state durably across reboots, backups, restores.
3. Never sign with the same leaf twice — the security proof collapses if it does.

Stateless schemes like [SLH-DSA](/kb/slh-dsa/) avoid this by selecting leaves pseudo-randomly and using larger trees with FORS few-time signatures at the bottom. The cost of statelessness is signature size (7-50 KB). Stateful schemes are 2-3 KB at comparable security, but require operational state-machine discipline.

## XMSS — eXtended Merkle Signature Scheme

### Standardization

**RFC 8391**, "XMSS: eXtended Merkle Signature Scheme," published May 2018 by Hülsing, Butin, Gazdag, Rijneveld, Mohaisen. NIST SP 800-208 (October 2020) approved XMSS for federal use in narrow scenarios.

### Construction

XMSS is a Merkle tree of WOTS+ (Winternitz One-Time Signature) keys. The public key is the Merkle tree root. To sign:

1. Pick the next unused leaf (state-tracked counter).
2. Generate the WOTS+ keypair for that leaf deterministically from a master seed.
3. Sign the message hash with WOTS+.
4. The signature is the WOTS+ signature plus the Merkle authentication path to the root.

A single XMSS tree of height `h` supports `2^h` signatures total. After that, the key is exhausted.

### XMSS-MT (multi-tree)

XMSS-MT is a hyper-tree of XMSS trees: a top-level tree whose leaves sign the roots of mid-level trees, whose leaves sign the roots of bottom-level trees. This allows much larger signing capacity (`2^60` or more) without huge keygen cost.

### Parameter sets (RFC 8391)

| Variant | Tree height | Signatures | Signature size | Hash |
|---------|-------------|------------|----------------|------|
| XMSS-SHA2_10_256 | 10 | 1,024 | ~2.5 KB | SHA-256 |
| XMSS-SHA2_16_256 | 16 | 65,536 | ~2.7 KB | SHA-256 |
| XMSS-SHA2_20_256 | 20 | 1,048,576 | ~2.8 KB | SHA-256 |
| XMSSMT-SHA2_20/2_256 | 20 (2 layers) | 1,048,576 | ~5 KB | SHA-256 |
| XMSSMT-SHA2_60/3_256 | 60 (3 layers) | 2^60 | ~8 KB | SHA-256 |

Public keys are 64 bytes. Signatures grow linearly with tree height because of the longer authentication path.

## LMS — Leighton-Micali Signatures

### Standardization

**RFC 8554**, "Leighton-Micali Hash-Based Signatures," published April 2019 by McGrew, Curcio, Fluhrer. NIST SP 800-208 (October 2020) approved LMS alongside XMSS.

### Construction

LMS is conceptually similar to XMSS — a Merkle tree of LM-OTS one-time signatures — but with simpler structure:

- LM-OTS: a Winternitz-like one-time signature.
- LMS: a Merkle tree of LM-OTS keys.
- HSS (Hierarchical Signature System): the LMS counterpart to XMSS-MT, layering LMS trees.

LMS prioritizes implementation simplicity and verification speed. It is slightly faster than XMSS in software and was the choice for several industry standards.

### Parameter sets (RFC 8554)

| Variant | Tree height | Signatures | Signature size |
|---------|-------------|------------|----------------|
| LMS_SHA256_M32_H10 | 10 | 1,024 | ~1.6 KB |
| LMS_SHA256_M32_H15 | 15 | 32,768 | ~1.8 KB |
| LMS_SHA256_M32_H20 | 20 | 1,048,576 | ~2.0 KB |
| LMS_SHA256_M32_H25 | 25 | 33,554,432 | ~2.2 KB |

LMS signatures are slightly smaller than XMSS at comparable parameters because of differences in the WOTS variant (LM-OTS vs WOTS+).

## NIST SP 800-208 — what it allows

NIST published *Recommendation for Stateful Hash-Based Signature Schemes* (SP 800-208, October 2020) to define when these schemes may be used in federal systems. The scope is deliberately narrow:

> **Approved use cases**: code signing, firmware signing, and other applications where the signing operation is performed in a controlled environment and signature state can be reliably maintained.
>
> **Not approved**: general-purpose public-key signatures, TLS, document signing, anywhere the signer is a normal end-user device.

The reasoning: state management is the failure mode. A signing system that loses or duplicates state will produce two signatures with the same leaf, and the security proof breaks. In a controlled signing pipeline (release engineering, firmware build server) this can be enforced. On a phone or laptop it cannot.

## The state-management problem in detail

Reusing an index in XMSS or LMS is **catastrophic**. With two signatures on different messages from the same WOTS+ key, an attacker can usually forge signatures on a third message. The relevant attack:

```
Sign(m1, idx=k) → reveals certain hash chain values
Sign(m2, idx=k) → reveals different hash chain values
Combine: enough chain values exposed to forge sign(m3) where H(m3) is a coordinate-wise weak point
```

State is lost in many ways:

- Backup-and-restore. The signer ships its state to backup storage; later a restore brings back an earlier state, and the signer reuses leaves.
- VM snapshot. Cloning a VM gives two systems with identical signing state.
- Crash before persisting. The signer increments its in-memory counter, signs, then crashes before flushing to disk. On reboot it signs with the same counter again.
- Concurrent signers. Two threads or two replicas signing from the same key file.

### Defenses

1. **Hardware security module with non-cloneable state**. The HSM enforces that the counter only ever increases, with anti-rollback hardware.
2. **Counter persistence with fsync barriers**. Increment counter, fsync, sign, fsync. Slow but robust.
3. **Reserve-then-sign**. Allocate a batch of leaves to a signer (idx 1000-1100), and the signer never touches anything outside that range.
4. **Multi-tree with batch reservation**. In XMSS-MT, allocate sub-trees to specific signers.
5. **Don't use stateful**. Use SLH-DSA if the operational discipline isn't available.

## Real-world deployments

### Linux kernel module signing

The Linux kernel community experimented with XMSS and LMS for module signing as an alternative to RSA-PSS, motivated by PQ migration. Discussion on linux-crypto and lkml has continued since 2020. Production adoption depends on state-management tooling.

### Firmware signing

- **Quantum-resistant firmware signing**: Cisco, HPE, and others have piloted LMS for signed firmware. The signing infrastructure is one batch process per release; state can be tracked.
- **AWS**: published guidance on using LMS for AWS Nitro and Graviton firmware paths.

### Code signing

- **Microsoft Authenticode**: PQ extensions under discussion include LMS as an option.
- **Sigstore**: SLH-DSA more likely than LMS because of the stateless property.

### Government

- **Germany / BSI**: lists XMSS and LMS in its TR-02102-1 catalog for narrow applications.
- **NSA CNSA 2.0** (September 2022): allows LMS for software/firmware signing as part of the suite of post-quantum recommendations.

## Comparison with stateless SLH-DSA

| Property | XMSS / LMS (stateful) | SLH-DSA (stateless) |
|----------|----------------------|---------------------|
| Signature size (Cat 1) | ~2 KB | ~7.8 KB |
| Public key | 32-64 B | 32 B |
| Signing capacity | Fixed by tree height | Effectively unbounded |
| Signing operational risk | High (state corruption) | None (stateless) |
| Sign speed | Fast (single hash chain) | Slow-medium |
| Verify speed | Fast | Medium |
| NIST status | SP 800-208 (narrow scope) | FIPS 205 (general) |
| Cryptographic assumption | Hash one-wayness | Hash one-wayness |

The cryptographic assumption is the same. The difference is purely operational. If the signing environment is locked down, XMSS / LMS give you 4x smaller signatures. If not, use SLH-DSA.

## Trade-offs

### Strengths

- Hash-only assumption (same conservative footing as SLH-DSA).
- Signatures 4-5x smaller than SLH-DSA.
- Fast signing and verification.
- Standardized via stable RFCs (8391, 8554) and NIST SP 800-208.
- Well-suited to controlled signing pipelines.

### Limitations

- Stateful. State corruption is catastrophic.
- Capacity is bounded by tree height.
- Operational complexity (counter persistence, backup discipline).
- NIST narrowly approves only for code/firmware signing.
- Not suitable for end-user signing (phones, laptops, browsers).

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| State rollback (reuse leaf) | HSM with anti-rollback hardware; fsync discipline |
| Two signers sharing state | Disjoint sub-tree allocation |
| Backup/restore brings back used state | "Don't restore signing state from backup; regenerate keys" policy |
| Hash function break | Migrate hash family (parameter sets allow SHA-256, SHA-512, SHAKE) |
| Fault injection during traversal | Recompute-and-compare |

## When to pick XMSS or LMS

| You have | Use |
|----------|-----|
| Locked-down release pipeline, want smallest signatures | LMS or XMSS |
| HSM with anti-rollback, signing rare events | LMS or XMSS |
| Distributed signing environment, can't centralize state | SLH-DSA |
| End-user devices signing | SLH-DSA or ML-DSA |
| Already using XMSS in standards (e.g., ETSI quantum-safe certificate profiles) | XMSS |
| Already using LMS in standards (e.g., NSA CNSA 2.0 firmware) | LMS |

## Primary sources

- IETF, *RFC 8391: XMSS — eXtended Merkle Signature Scheme*, May 2018. Hülsing, Butin, Gazdag, Rijneveld, Mohaisen. `datatracker.ietf.org/doc/rfc8391/`.
- IETF, *RFC 8554: Leighton-Micali Hash-Based Signatures*, April 2019. McGrew, Curcio, Fluhrer. `datatracker.ietf.org/doc/rfc8554/`.
- NIST, *SP 800-208: Recommendation for Stateful Hash-Based Signature Schemes*, October 2020. Cooper, Apon, Dang, Davidson, Dworkin, Miller. `csrc.nist.gov/publications/detail/sp/800-208/final`.
- NSA, *CNSA Suite 2.0*, September 7, 2022. `media.defense.gov/2022/Sep/07/2003071834/-1/-1/0/CSA_CNSA_2.0_ALGORITHMS_.PDF`.
- Buchmann, Dahmen, Hülsing, *XMSS — A Practical Forward Secure Signature Scheme based on Minimal Security Assumptions*, PQCrypto 2011.
- Leighton, Micali, *Large provably fast and secure digital signature schemes from secure hash functions*, US Patent 5,432,852, 1995.
