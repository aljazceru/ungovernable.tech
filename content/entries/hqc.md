---
title: "HQC"
slug: hqc
type: deep-dive
pillars: ["pqc"]
readiness: experimental
description: "HQC, the code-based key encapsulation mechanism NIST selected in 2025 as a backup to ML-KEM: how it works, its sizes and standardisation timeline."
dek: "The code-based KEM selected by NIST in March 2025 for standardization as a second PQ KEM, alongside ML-KEM. Different mathematical assumption (random quasi-cyclic codes), larger ciphertexts, and the assumption-diversity hedge against a hypothetical lattice break."
updated: 2026-10-25
created: 2026-04-26
origin: vault
source: "10-Post-Quantum/HQC.md"
aliases: ["Hamming Quasi-Cyclic"]
tags: ["hqc", "code-based", "kem", "post-quantum", "deep-dive"]
---

## What it is

HQC is a key-encapsulation mechanism whose security rests on the hardness of decoding random **quasi-cyclic codes** — a problem in the McEliece / Niederreiter family of code-based cryptography. It was submitted to the NIST PQC competition by Aguilar Melchor, Aragon, Bettaieb, Bidoux, Blazy, Deneuville, Gaborit, Persichetti, Zémor, and Bourges-Sevenier. After being a round-4 alternate alongside BIKE and Classic McEliece, NIST announced in **March 11, 2025** that HQC would be standardized as a second KEM, as an additional code-based KEM.

Why a second KEM? **Assumption diversity.** [ML-KEM](/kb/ml-kem/) (FIPS 203) is the workhorse, but its security depends on Module-LWE, a lattice problem. Lattice-based and code-based cryptography rest on independent mathematical assumptions; if one collapses, the other survives. HQC is the belt-and-suspenders against a future lattice cryptanalysis breakthrough.

## Code-based cryptography

Code-based public-key cryptography goes back to **McEliece, 1978**. The basic idea: pick a code with a fast decoding algorithm, scramble it into something that looks like a random code, and use the discrepancy as a trapdoor.

McEliece used Goppa codes. The large object in Classic McEliece is the public key, not the ciphertext. **Niederreiter** (1986) is a dual variant. **Classic McEliece** is the conservative NIST PQC submission with very large keys and small ciphertexts. **BIKE** uses moderate-density parity-check codes for smaller keys. **HQC** uses quasi-cyclic codes and has a different security reduction:

- HQC reduces to the **Quasi-Cyclic Syndrome Decoding (QCSD)** problem.
- The decoder is built from a concatenation of a Reed-Muller code and a Reed-Solomon code, with decoding tailored to that concatenated code.
- Unlike McEliece-style schemes, HQC has a clean IND-CCA2 security reduction without the structural concerns of hidden Goppa codes.

This last point — that HQC's underlying code is **random**, not a structured code disguised — is the security argument that won HQC the second-KEM slot.

## Mathematical foundation (light)

HQC works over `F_2[X] / (X^n - 1)` for `n` prime. Operations are polynomial multiplication mod `X^n - 1`.

- **KeyGen**: pick small-weight `x, y`. Public key is `h, s = x + h·y` for random `h`.
- **Encaps**: pick small-weight `e, r1, r2`. Compute `u = r1 + h·r2` and `v = m·G + s·r2 + e` where `G` is a generator matrix of the inner concatenated code. Send `(u, v)`.
- **Decaps**: receiver computes `v - u·y = m·G + (e + ...)` where the noise has bounded weight, and decodes through the concatenated Reed-Muller / Reed-Solomon code.

The "small-weight" constraint is what makes the scheme one-way: given `s`, recovering `(x, y)` is the QCSD problem.

The IND-CCA2 transformation is the **Fujisaki-Okamoto** construction, the same as ML-KEM uses.

## Parameter sets

The August 2025 HQC specification names the parameter sets HQC-1, HQC-3 and HQC-5. They target the same NIST security categories as ML-KEM:

| Variant | Security level | Public key | Ciphertext | Shared secret |
|---------|---------------|-----------|------------|---------------|
| **HQC-1** | NIST Cat 1 (~AES-128) | 2,241 B | 4,433 B | 32 B |
| **HQC-3** | NIST Cat 3 (~AES-192) | 4,514 B | 8,978 B | 32 B |
| **HQC-5** | NIST Cat 5 (~AES-256) | 7,237 B | 14,421 B | 32 B |

Compared to ML-KEM:

| Scheme | Public key | Ciphertext |
|--------|-----------|------------|
| ML-KEM-512 | 800 B | 768 B |
| **HQC-1** | **2,241 B** | **4,433 B** |
| ML-KEM-768 | 1,184 B | 1,088 B |
| **HQC-3** | **4,514 B** | **8,978 B** |
| ML-KEM-1024 | 1,568 B | 1,568 B |
| **HQC-5** | **7,237 B** | **14,421 B** |

HQC ciphertexts are roughly **4-9x larger** than ML-KEM at comparable security levels. This is the cost of the assumption-diversity hedge.

## Performance

The HQC specification reports implementation-specific benchmarks and identifies its test platform. Compare implementations on the intended hardware; a generic microsecond range is not a portable performance guarantee.

## When to use HQC

The honest answer in early 2026 is: **rarely on its own**. HQC's role is as a hedge.

| Use case | Approach |
|----------|----------|
| **Triple hybrid** | `X25519 + ML-KEM-768 + HQC-3` for protocols with extreme assumption-diversity needs |
| **Government / regulated environments** | Where policy mandates code-based plus lattice-based |
| **Long-term secrecy archives** | Where multi-decade harvest-now-decrypt-later resistance demands two PQ KEMs |
| **Migration hedge** | Systems already shipped with ML-KEM that want to add HQC support for future flexibility |

For most deployments, ML-KEM alone (or hybrid X25519+ML-KEM) is the right call. HQC is the algorithm to keep on the shelf in case lattice cryptanalysis advances.

### Triple-hybrid pattern

```
shared_secret = KDF(
    X25519_shared,
    ML-KEM_shared,
    HQC_shared
)
```

If any one of the three is broken (or even all three), the others provide security. Cost is 5-15 KB extra per handshake, depending on parameters.

## Comparison with ML-KEM and other code-based KEMs

| Property | ML-KEM (FIPS 203) | HQC | Classic McEliece | BIKE |
|----------|-------------------|-----|------------------|------|
| **Math** | Module-LWE | QCSD | Goppa codes | QC-MDPC codes |
| **Public key (Cat 1)** | 800 B | 2,241 B | ~261 KB | 1,541 B |
| **Ciphertext (Cat 1)** | 768 B | 4,433 B | ~128 B | 1,573 B |
| **Encaps speed** | Fast | Medium | Fast | Medium |
| **Decaps speed** | Fast | Medium-slow | Fast | Slow |
| **Standardization status** | FIPS 203 (final 2024) | NIST selected Mar 2025; FIPS 2026 | NIST round 4, no decision | NIST round 4 alternate |
| **Decryption failures** | Negligible | Non-zero (handled by FO) | Zero | Non-zero |

Classic McEliece has the smallest ciphertexts but the largest public keys (~261 KB at Cat 1), which is impractical for most protocols. BIKE has decoding-failure issues. HQC sits in a middle ground: moderate keys, moderate ciphertexts, and a clean security reduction.

## Standardization status

- **NIST round 4 selection**: announced March 11, 2025. NIST internal report IR 8528 "Status Report on the Fourth Round of the NIST Post-Quantum Cryptography Standardization Process" identifies HQC as the chosen alternate KEM.
- **FIPS document**: in drafting; expected initial public draft late 2026, final standard 2027. Unlike ML-KEM's 2024 release, HQC's FIPS is still being formatted to NIST publication requirements.
- **liboqs**: HQC included since v0.9; v0.14.0 (July 2025) fixed a security fix for secret-dependent branching in HQC; v0.16.0 milestone tracks updated HQC reference implementation for NIST FIPS alignment.
- **TLS / IETF**: hybrid HQC drafts under discussion in the TLS WG; no production deployment yet.
- **Hardware vendors**: limited; awaiting final FIPS document before HSM and accelerator support.

## Trade-offs

### Strengths

- Different mathematical assumption from lattice schemes — the assumption-diversity hedge.
- Long history of code-based cryptography (McEliece, 1978).
- Random-code security argument is cleaner than structured-code (Goppa) constructions.
- IND-CCA2 secure via Fujisaki-Okamoto.
- Constant-time-friendly (no rejection sampling, no Gaussian sampling).

### Limitations

- Ciphertexts and public keys are 4-9x larger than ML-KEM.
- Slower than ML-KEM by 5-10x on most operations.
- Non-zero decryption failure rate (handled by FO transform but adds analytical complexity).
- Decoder for the concatenated Reed-Muller / Reed-Solomon code is more complex than ML-KEM's NTT.
- Ecosystem support is behind ML-KEM by 18-24 months.

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| QCSD breakthrough | Hybrid with ML-KEM and / or X25519 |
| Side-channel on decoder | Constant-time concatenated decoder; reference implementations being hardened |
| Decryption failure information leak | FO transform absorbs single-query failures; multi-query rate-limit |
| Implementation bugs in polynomial arithmetic | Audit; cross-implementation interop testing |
| Quantum attack on QCSD | QCSD is conjectured PQ-secure; standardization rests on this |

## Future hybrid patterns

HQC fits into hybrid migration strategies in three ways:

1. **Today**: X25519 + ML-KEM-768 (currently the deployed hybrid).
2. **Conservative add-on**: X25519 + ML-KEM-768 + HQC-3 (triple hybrid; cost 5-15 KB).
3. **Post-quantum-only**: ML-KEM + HQC (drop classical, depend on PQ assumption diversity).

Step 3 becomes interesting when classical cryptanalysis of curve schemes catches up to PQ confidence levels — likely 2030+.

## Primary sources

- [NIST IR 8545: Fourth-round status report](https://nvlpubs.nist.gov/nistpubs/ir/2025/NIST.IR.8545.pdf)
- [HQC specification](https://pqc-hqc.org/doc/hqc_specifications_2025_08_22.pdf)
- [Efficient Encryption from Random Quasi-Cyclic Codes](https://eprint.iacr.org/2016/1194)
- [McEliece: A Public-Key Cryptosystem Based on Algebraic Coding Theory](https://ipnpr.jpl.nasa.gov/progress_report2/42-44/44N.PDF)
- [A Modular Analysis of the Fujisaki-Okamoto Transformation](https://eprint.iacr.org/2017/604)
- [liboqs HQC implementation](https://github.com/open-quantum-safe/liboqs/tree/main/src/kem/hqc)
