---
title: "FN-DSA (Falcon)"
slug: fn-dsa-falcon
type: deep-dive
pillars: ["pqc"]
readiness: experimental
description: "FN-DSA (Falcon), the compact lattice signature scheme being standardised as FIPS 206: how it works, its implementation pitfalls and its status."
dek: "Fast Fourier-NIST Signature — a lattice-based digital signature algorithm based on the NTRU lattice and Gaussian sampling, standardized as FIPS 206 (draft)."
updated: 2026-06-06
created: 2026-04-26
origin: vault
source: "10-Post-Quantum/FN-DSA Falcon.md"
aliases: ["Falcon", "FIPS 206"]
tags: ["fn-dsa", "falcon", "ntru", "signatures", "fips-206", "post-quantum", "deep-dive"]
---

## What it is

Falcon (Fast-Fourier Lattice-based Compact signatures over NTRU) was submitted to the NIST PQC competition by **Prest, Fouque, Hoffstein, Kirchner, Lyubashevsky, Pornin, Ricosset, Seiler, Whyte, and Zhang**. Selected as a winner in the third round (July 2022), it is being standardized as **FIPS 206 / FN-DSA**, with the initial public draft published August 11, 2025 by NIST.

Falcon's reason for existing alongside [ML-DSA](/kb/ml-dsa/) is signature size. At NIST category 1, a Falcon-512 signature is about 666 bytes versus ML-DSA-44's 2,420 bytes. For protocols where signatures are embedded in chains (X.509 certificate chains, DNSSEC records, blockchain witness data), this is a meaningful saving.

The cost is implementation difficulty: Falcon is the only NIST PQ signature that uses **floating-point Gaussian sampling** in its hot path.

## Mathematical foundation (light)

Falcon is a **GPV-style hash-and-sign** signature over **NTRU lattices**. The high-level structure:

1. The keypair is a short basis for an NTRU lattice. The public key is a hash of the lattice; the secret key is a "good" (short) basis.
2. To sign a message `m`, hash to a random point `c` in the lattice space.
3. Sample a lattice point `s` near `c` using the secret short basis. The "near" sampling uses a **discrete Gaussian distribution** to avoid leaking the basis.
4. The signature is the offset `c - s`.
5. Verification checks that the offset is short and hashes correctly.

The Gaussian sampling step is what makes Falcon fast and compact, and what makes it dangerous to implement.

### Why floating-point

Sampling from a discrete Gaussian over an arbitrary center requires high-precision evaluations of `exp(-x²/2σ²)`. The reference implementation uses IEEE 754 double-precision floating point because:

- Hardware fp is fast (single-cycle on modern CPUs).
- The Fourier-transform-based fast sampler relies on fp arithmetic.
- Integer-only alternatives are slower or larger.

This decision is the central trade-off of Falcon.

## Parameter sets

FIPS 206 (draft, August 2025) specifies two parameter sets:

| Variant | Security level | Public key | Signature | NTRU degree |
|---------|---------------|-----------|-----------|-------------|
| **FN-DSA-512** (Falcon-512) | NIST Cat 1 (~AES-128) | 897 B | ~666 B | 512 |
| **FN-DSA-1024** (Falcon-1024) | NIST Cat 5 (~AES-256) | 1,793 B | ~1,280 B | 1024 |

Notable absences:

- No Cat 3 variant. Falcon-768 was considered but dropped for clean NTRU degree-power-of-two parameters.
- Signature sizes are **average** — Falcon's signatures vary slightly in length because of the rejection-sampling step.

Compared to the alternatives at Cat 1:

| Scheme | Public key | Signature |
|--------|-----------|-----------|
| Ed25519 | 32 B | 64 B |
| ML-DSA-44 | 1,312 B | 2,420 B |
| **FN-DSA-512** | **897 B** | **~666 B** |
| SLH-DSA-SHA2-128s | 32 B | 7,856 B |

Falcon sits between Ed25519 and ML-DSA on signature size. Public keys are also smaller than ML-DSA's.

## The implementation problem

Floating-point Gaussian sampling is the hardest part of any cryptographic library to make safe.

### Side-channel exposure

- **Timing**: floating-point operations on most CPUs are constant-time, but denormals, NaNs, and subnormal handling can leak.
- **Platform variance**: x86 80-bit extended precision (legacy x87) versus IEEE 754 double versus ARM NEON give different rounding. The reference implementation pins everything to IEEE 754 double, but this requires careful compiler flags.
- **Microarchitectural**: speculative execution and rounding-mode-dependent paths are hard to audit.

### Attacks demonstrated

- **Karabulut and Aysu, 2021**: power-analysis side-channel against Falcon's Gaussian sampler.
- **Guerreau, Martinelli, Ricosset, Rossi, 2022**: profiling attack on the FFT step.
- **Zhang, Lin, Yu, Wang, 2023**: cache-timing attack against the table lookup in the Gaussian sampler.

NIST and the Falcon team have responded with constant-time samplers (Howe, Prest, Apon, "Isochronous Gaussian Sampling: From Inception to Implementation," PQCrypto 2020), but constant-time floating-point remains hardware-dependent.

### Where it bites

- Embedded devices without IEEE 754-compliant fp (common in smartcards, low-end microcontrollers).
- Anywhere the toolchain might enable `-ffast-math` or fused-multiply-add reordering.
- HSMs that use integer-only crypto cores must implement an integer Gaussian sampler, which is much slower.

## Performance

On modern x86-64 with IEEE 754 fp:

- **Falcon-512 sign**: ~150-300 µs
- **Falcon-512 verify**: ~30-60 µs
- **Falcon-512 keygen**: ~10-30 ms (slow because of NTRU key generation, including a basis-reduction step)

Verification is fast (faster than ML-DSA on most platforms). Signing is comparable to ML-DSA. Key generation is much slower than either ML-DSA or SLH-DSA — Falcon keygen involves solving the NTRU equation, which can take hundreds of milliseconds.

This makes Falcon poorly suited to ephemeral keys but fine for long-lived signing keys.

## When to use FN-DSA

| Use case | Why it fits |
|----------|-------------|
| **TLS handshake signatures** | Smaller than ML-DSA helps cert chain bloat |
| **Certificate chains** | Multiple Falcon signatures in a chain still fit in typical TCP segments |
| **DNSSEC** | Records are size-constrained; small signatures matter |
| **Blockchain witness data** | Falcon signatures fit better in block budgets than ML-DSA |
| **Smart-card attestation** | Once the constant-time sampler problem is solved, the small signature is attractive |

When **not** to use it:

- Embedded environments without a trustworthy fp unit.
- HSMs that don't have a Falcon-aware integer sampler.
- High-volume signing workloads where keygen-per-session is needed (use ML-DSA instead).
- Anywhere a constant-time guarantee on the signing side is required and the platform can't enforce it.

## Comparison with the other PQ signature standards

| Property | FN-DSA / Falcon | ML-DSA (FIPS 204) | SLH-DSA (FIPS 205) |
|----------|----------------|-------------------|--------------------|
| **Signature size (Cat 1)** | ~666 B | 2,420 B | 7,856 B |
| **Public key (Cat 1)** | 897 B | 1,312 B | 32 B |
| **Sign speed** | Medium | Fast | Slow |
| **Verify speed** | Fast | Fast | Medium |
| **Keygen speed** | Slow (NTRU) | Fast | Fast |
| **Implementation difficulty** | High (fp Gaussian) | Medium (rejection) | Low (hash chains) |
| **Side-channel risk** | High | Medium | Low |
| **Assumption** | NTRU-SIS | Module-LWE / SIS | Hash one-wayness |
| **Best for** | Size-constrained | General purpose | Conservative archival |

## Standardization status

- **NIST selection**: announced July 2022, alongside CRYSTALS-Dilithium and SPHINCS+.
- **FIPS 206 initial public draft (IPD)**: August 11, 2025 — the draft standard was submitted for public comment, not merely announced.
- **Public comment period**: closed late 2025.
- **Final standard**: expected late 2026 / early 2027. The IETF `draft-ietf-cose-falcon-04` reference note states "FIPS 206 (expected to be published in late 2026 early 2027)." The NIST 6th PQC Conference (2025) confirmed active discussion of SUF-CMA requirements, hedged variants, key/message-recovery mode, and fixed-point signing — the final standard will reflect resolution of these open questions.
- **COSE integration**: `draft-ietf-cose-falcon-04` (current, expires April 2026) tracks FIPS 206 alignment. The COSE-wg milestone is January 2026 for "one or more documents describing the proper use of algorithms."
- **liboqs**: Falcon implemented; tracking FIPS 206 alignment in current releases.
- **HSM support**: limited. Most major HSM vendors await final FIPS 206 before shipping production code.

## Hybrid deployment

Like ML-DSA, Falcon is typically deployed in hybrid form alongside a classical signature:

```
combined_sig = (Ed25519_sig, Falcon_sig)
verify: BOTH must validate
```

For TLS the most likely deployment is `Ed25519 + Falcon-512` certificate signatures, which keeps total signature size well under 1 KB combined. Compare to `Ed25519 + ML-DSA-44` at over 2.5 KB.

The CA/B Forum and IETF LAMPS WG drafts include Falcon composites in the hybrid signature ladder.

## Trade-offs

### Strengths

- Smallest signatures of any NIST-standardized PQ signature scheme.
- Smaller public keys than ML-DSA (897 B vs 1,312 B at Cat 1).
- Verification is fast.
- Mature cryptanalysis after years of NIST review.
- NTRU is one of the older lattice problems (since 1998) with a long study history.

### Limitations

- Floating-point Gaussian sampling is the hardest crypto code to get right and audit.
- Side-channel resistance is platform-dependent and fragile.
- Keygen is slow and complex (NTRU equation solving).
- Constant-time enforcement requires careful compiler flags and may break on cross-platform builds.
- HSM ecosystem is behind ML-DSA.

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Timing leak from fp Gaussian sampler | Isochronous sampler (Howe-Prest-Apon 2020); platform-pinned IEEE 754 |
| Power analysis on signing | Masked sampler implementations |
| Compiler reordering of fp ops | Strict `-fno-fast-math`, `-fno-fp-contract=off`; audit binary |
| Fault injection into NTRU keygen | Recompute and compare; verify before publishing |
| NTRU lattice cryptanalysis breakthrough | Hybrid with classical Ed25519 |
| Quantum attack on NTRU | NTRU is conjectured PQ-secure; standardization assumes so |

## Implementation libraries

- **Falcon reference**: `github.com/algorand/falcon` (Pornin's reference, used in NIST submission).
- **liboqs**: `github.com/open-quantum-safe/liboqs` includes Falcon and tracks FIPS 206 alignment.
- **PQClean**: `github.com/PQClean/PQClean` has clean and AVX2 implementations.
- **OpenSSL**: hybrid Falcon X.509 support via OQS provider.
- **BouncyCastle (Java)**: Falcon implementation in development.

## Primary sources

- NIST, *FIPS 206: FN-DSA (Falcon) — Initial Public Draft*, August 11, 2025. `csrc.nist.gov/pubs/fips/206/ipd`.
- Prest, Fouque, Hoffstein, Kirchner, Lyubashevsky, Pornin, Ricosset, Seiler, Whyte, Zhang, *Falcon: Fast-Fourier Lattice-based Compact Signatures over NTRU*, NIST PQC submission round 3, 2020. `falcon-sign.info`.
- Gentry, Peikert, Vaikuntanathan, *Trapdoors for Hard Lattices and New Cryptographic Constructions*, STOC 2008. (GPV signature framework)
- Hoffstein, Pipher, Silverman, *NTRU: A Ring-Based Public Key Cryptosystem*, ANTS-III 1998.
- Howe, Prest, Apon, *Isochronous Gaussian Sampling: From Inception to Implementation*, PQCrypto 2020.
- Karabulut, Aysu, *Falcon Down: Breaking Falcon Post-Quantum Signature Scheme through Side-Channel Attacks*, DAC 2021.
- liboqs Falcon implementation — `github.com/open-quantum-safe/liboqs`.
