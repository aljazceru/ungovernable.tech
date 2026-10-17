---
title: "SLH-DSA (FIPS 205)"
slug: slh-dsa
type: deep-dive
pillars: ["pqc"]
readiness: usable
description: "SLH-DSA (FIPS 205), the conservative hash-based post-quantum signature standard: large signatures, minimal assumptions, and when to use it."
dek: "The conservative post-quantum signature standard (FIPS 205, August 2024). Built on hash functions only — no number-theoretic and no lattice assumption. Huge signatures, but the smallest cryptographic attack surface of any PQ scheme NIST has standardized."
updated: 2026-04-26
created: 2026-04-26
origin: vault
source: "10-Post-Quantum/SLH-DSA.md"
aliases: ["SPHINCS+", "FIPS 205"]
tags: ["slh-dsa", "sphincs", "hash-based", "signatures", "fips-205", "post-quantum", "deep-dive"]
---

## What it is

SLH-DSA is the FIPS 205 standardization of **SPHINCS+** by Bernstein, Hülsing, Kölbl, Niederhagen, Rijneveld, and Schwabe (NIST PQC round 3 alternate winner, finalized as a standard alongside ML-KEM and ML-DSA in the August 13, 2024 publication). The "stateless" in the name distinguishes it from XMSS and LMS (see [Stateful Hash Signatures](/kb/stateful-hash-signatures/)), which require the signer to track which one-time keys have been used.

Its security rests on a single assumption: **the underlying hash function (SHA-2 or SHAKE) is one-way and second-preimage resistant**. No structured number theory, no lattice problem, no code-decoding hardness. If hash functions are broken, the entire field of cryptography has bigger problems than SLH-DSA.

## Why it exists alongside ML-DSA

[ML-DSA](/kb/ml-dsa/) is the workhorse PQ signature. It's smaller, faster, and designed for general-purpose use. But its security rests on **Module-LWE / Module-SIS**, lattice problems whose concrete hardness is an active research question. A breakthrough in lattice cryptanalysis (the way SIKE collapsed in 2022) would invalidate ML-DSA overnight.

SLH-DSA is the safety net. NIST standardized both deliberately so the world has a hash-only fallback whose security depends on the same primitives that Merkle trees, HMAC, and Bitcoin already rely on. The cost is signature size, 7 to 50 KB versus ML-DSA's 2-5 KB or Ed25519's 64 bytes, but for high-value, low-frequency signing the trade is acceptable.

## How it works (conceptually)

SLH-DSA stacks three constructions on top of a hash function:

```
Layer 3:  Hyper-tree of WOTS+ / FORS  (stateless many-time signing)
            │
Layer 2:  XMSS-style Merkle authentication paths  (binds OTS to root key)
            │
Layer 1:  WOTS+ one-time signatures + FORS few-time signatures
            │
Layer 0:  SHA-2-256 / SHA-2-512 / SHAKE-256
```

- **WOTS+** (Winternitz one-time signature, plus): a one-time signature using hash chains.
- **FORS** (Forest of Random Subsets): a few-time signature scheme used at the bottom of the hyper-tree to absorb the message hash.
- **Hypertree**: a Merkle tree of Merkle trees. The root is the public key. The signature is a FORS signature plus a chain of WOTS+ signatures authenticating up the tree.

Statelessness comes from selecting the FORS leaf pseudo-randomly from the message: the signer never has to remember which leaf it last used.

## Parameter sets

FIPS 205 specifies twelve variants: three security levels (NIST categories 1, 3, 5 ≈ AES-128, AES-192, AES-256) crossed with two hash families (SHA-2, SHAKE) and two profiles (`s` = small signature, `f` = fast signing).

| Variant | Security level | Public key | Signature | Sign time | Verify time |
|---------|---------------|-----------|-----------|-----------|-------------|
| **SLH-DSA-SHA2-128s** | Cat 1 | 32 B | 7,856 B | slow | fast |
| **SLH-DSA-SHA2-128f** | Cat 1 | 32 B | 17,088 B | fast | medium |
| **SLH-DSA-SHA2-192s** | Cat 3 | 48 B | 16,224 B | slow | fast |
| **SLH-DSA-SHA2-192f** | Cat 3 | 48 B | 35,664 B | fast | medium |
| **SLH-DSA-SHA2-256s** | Cat 5 | 64 B | 29,792 B | slow | fast |
| **SLH-DSA-SHA2-256f** | Cat 5 | 64 B | 49,856 B | fast | medium |

(SHAKE variants are size-equivalent; speed depends on hardware acceleration of SHA-2 vs Keccak.)

`s` versus `f` is a hyper-tree depth trade. Smaller signatures need a shallower tree, which makes signing slower because each leaf is more expensive to derive. The `f` variants take roughly 10x more bandwidth to gain about 50x faster signing.

Public keys stay tiny (32-64 bytes). Signatures are the cost.

## Performance

Order-of-magnitude figures on a modern x86-64 CPU (without dedicated SHA-NI in some cases):

- **SLH-DSA-SHA2-128s sign**: ~1-3 seconds on commodity hardware. Verify: ~1-5 ms.
- **SLH-DSA-SHA2-128f sign**: ~10-50 ms. Verify: ~1-10 ms.
- Key generation: comparable to a single signing operation.

For comparison, Ed25519 signs in ~50 µs. SLH-DSA-128s is roughly 20,000-60,000x slower per signature. This rules it out for high-throughput interactive protocols (TLS handshakes at scale, per-event signing in messaging) but is fine for code-signing release pipelines or root-CA operations measured in operations per day.

## When to use SLH-DSA

| Use case | Why it fits |
|----------|-------------|
| **Long-term archival signatures** | Signed documents, notarizations expected to remain verifiable for 50+ years. Hash assumption is the most durable. |
| **Root certificates** | Issued rarely, verified often, must outlive any one cryptographic family. |
| **Code signing for safety-critical systems** | Aerospace, medical, automotive firmware where a lattice break would be catastrophic. |
| **Conservative high-value signing** | National-security signing keys, root KMS attestation keys. |
| **Belt-and-suspenders alongside ML-DSA** | Co-sign with both; verifier requires both signatures valid. |
| **Air-gapped HSMs** | Slow signing is fine when the HSM signs once a quarter. |

When **not** to use it:

- TLS handshakes (use ML-DSA or hybrid with Ed25519).
- Per-message signing in messaging protocols (signatures swamp the messages).
- Blockchain transaction signing (50-KB signatures destroy the block budget).
- Anything bandwidth-constrained.

## Comparison with the other FIPS PQ signature standards

| Property | SLH-DSA (FIPS 205) | ML-DSA (FIPS 204) | FN-DSA / Falcon (FIPS 206) |
|----------|-------------------|-------------------|----------------------------|
| **Math** | Hash functions | Module-LWE / SIS | NTRU lattices |
| **Signature size (Cat 1)** | 7,856 B | 2,420 B | ~666 B |
| **Public key size** | 32 B | 1,312 B | 897 B |
| **Sign speed** | Slow (ms-s) | Fast (~100 µs) | Medium |
| **Verify speed** | Medium (~ms) | Fast | Fast |
| **Side-channel risk** | Low (no fp, no rejection) | Medium (rejection sampling) | High (Gaussian fp sampling) |
| **Assumption** | Hash one-wayness | Module-LWE hard | NTRU SIS hard |

SLH-DSA has the most conservative cryptographic assumption and the smallest implementation surface, at the cost of bandwidth.

## Standardization status

- **FIPS 205**: published August 13, 2024 (`nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf`).
- Reference implementation in liboqs (Open Quantum Safe) and the SPHINCS+ project repository.
- HSM support: emerging through 2025-2026 in Thales, Utimaco, and AWS CloudHSM firmware roadmaps.
- IETF: hybrid signature drafts (e.g., `draft-ietf-lamps-pq-composite-sigs`) include SLH-DSA composites.

## Side-channel and implementation properties

SLH-DSA is unusually friendly to constant-time implementation:

- No floating-point arithmetic (unlike Falcon).
- No rejection sampling (unlike ML-DSA).
- No conditional branches on secret data in the canonical flow.
- All arithmetic is over hash function inputs and outputs.

The dominant attack surface is **fault injection during the hyper-tree traversal** — glitching the WOTS+ chain computation can leak chain values. Standard fault-detection countermeasures (recompute and compare) handle this with a 2x signing cost.

## Trade-offs

### Strengths

- Minimal cryptographic assumption (hash one-wayness only).
- Stateless: no operational state to corrupt or reuse.
- Tiny public keys; suitable for embedding in certificates.
- Easy to implement correctly and to audit.
- Survives a hypothetical lattice cryptanalysis breakthrough.

### Limitations

- Signatures are 7-50 KB. This is the dominant operational cost.
- Slow signing (especially `s` variants).
- Not suitable for high-frequency or bandwidth-constrained protocols.
- 256-bit security variants are particularly bulky.

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Hash function break (preimage) | Move to a longer-output hash; SHA-3 or SHAKE alternative |
| Fault injection during signing | Recompute-and-compare; redundant Merkle verification |
| Side-channel on hash core | Constant-time SHA-2 / Keccak implementations |
| Quantum attack on hash (Grover) | 256-bit hashes give 128-bit post-Grover security; parameter sets account for this |
| Birthday attack on FORS | FORS parameter selection in FIPS 205 chosen with margin |

## Deployment patterns

1. **Root CA signing** — issue intermediate CA certs with SLH-DSA. Intermediate CAs use ML-DSA for daily issuance.
2. **Firmware signing** — sign release manifests with SLH-DSA + classical Ed25519 hybrid; verifier requires both.
3. **Long-term notarization** — Sigstore-style transparency log entries cosigned by an SLH-DSA key for archival assurance.
4. **Hybrid composite signatures** — `draft-ietf-lamps-pq-composite-sigs` defines `Ed25519+SLH-DSA-SHA2-128s`-style composite OIDs for X.509.

## Primary sources

- NIST, *FIPS 205: Stateless Hash-Based Digital Signature Standard*, August 13, 2024. `nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf`.
- Bernstein, Hülsing, Kölbl, Niederhagen, Rijneveld, Schwabe, *The SPHINCS+ Signature Framework*, ACM CCS 2019.
- SPHINCS+ submission to NIST PQC, round 3 (2020). `sphincs.org`.
- Hülsing, Rijneveld, Schwabe, *ARMed SPHINCS — Computing a 41 KB signature in 16 KB of RAM*, PKC 2016.
- liboqs SLH-DSA implementation — `github.com/open-quantum-safe/liboqs`.
- IETF, *Composite ML-DSA / SLH-DSA Signatures for X.509*, `draft-ietf-lamps-pq-composite-sigs`.
