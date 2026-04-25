---
title: "FHE Bootstrapping and Verification"
tags:
  - "fhe"
  - "bootstrapping"
  - "vfhe"
  - "verifiable-fhe"
  - "cryptography"
  - "deep-dive"
---
*Two technical problems that shape every real FHE deployment: how to compute deeply (bootstrapping) and how to know the server didn't lie (verifiability). The Overview file explains why; this one explains how.*

---

## The bootstrapping problem

Every FHE multiplication adds noise to the ciphertext. After enough multiplications, noise saturates and the ciphertext fails to decrypt. Solutions:

- **Leveled FHE.** Bound the multiplicative depth in advance and pick parameters so noise doesn't saturate within that depth. Cheap but limited.
- **Bootstrapping.** Homomorphically run the decryption circuit on the noisy ciphertext, producing a fresh ciphertext encrypting the same plaintext with reset noise. Unlimited depth but expensive.

Bootstrapping is what makes FHE "fully" homomorphic. Without it you have somewhat-homomorphic encryption (SHE), which has practical uses (especially for shallow ML circuits) but isn't full FHE.

---

## Bootstrapping approaches

### Gentry's original (2009)

Run the decryption circuit symbolically on the ciphertext using FHE itself. Catastrophically slow: tens of minutes per bit on Gentry's original scheme, with parameters in the gigabytes.

### CGGI / TFHE (Chillotti-Gama-Georgieva-Izabachène, 2016)

Per-bit boolean bootstrapping using LWE over the torus. Each gate operation includes a bootstrap, so noise never accumulates. Tens of milliseconds per gate, fast enough for practical Boolean circuits.

Used in: Zama Concrete, fhEVM.

### CKKS bootstrapping (Cheon et al., 2018+)

CKKS supports approximate arithmetic; bootstrapping operates on packed slots and adds quantifiable approximation error. Recent work has driven CKKS bootstrapping under one second for 2¹⁵-slot polynomials, opening real-time approximate ML inference.

Used in: OpenFHE, Microsoft SEAL (CKKS module), Lattigo.

### BGV / BFV bootstrapping (Halevi-Shoup, 2014+)

For exact integer arithmetic. Slower than CKKS bootstrapping per slot but exact. The HElib reference implementation pioneered the techniques.

### Programmable bootstrapping (PBS)

A TFHE variant where the bootstrap evaluates an arbitrary lookup table while refreshing noise: a function evaluation folded into bootstrapping for free. Important for programmable FHE compilers (Zama Concrete's "TFHE-rs" lineage uses this heavily).

---

## Performance snapshot (early 2026)

| Operation | Library | Throughput |
|-----------|---------|------------|
| TFHE Boolean gate + bootstrap | tfhe-rs / Concrete | ~10-30 ms/gate single-thread |
| CKKS 2¹⁵-slot bootstrap | OpenFHE | ~3-10 s on a 16-core CPU |
| BGV bootstrap (HElib) | HElib | ~10-30 s for medium parameters |
| Programmable bootstrap (PBS) | tfhe-rs | ~10-30 ms for 4-bit LUT |

These numbers improve year over year. The 2024 PRIO+ work and follow-ups have driven deep neural-net inference under FHE to seconds-per-image for small models.

---

## Why FHE doesn't give verifiability

Plain FHE protects confidentiality: the server doesn't see the plaintext. It does not protect integrity: a malicious server can return any ciphertext it wants and the decryptor learns whatever the server chose to compute. Worse, FHE schemes are typically malleable by design, since operations on ciphertexts are how you compute homomorphically.

The decryptor sees: a ciphertext it received from the server.
What the decryptor wants to know: that the server actually computed `f(input)` and not, say, `g(input)` or "always return 0".

Without verifiability, FHE protects you against honest-but-curious servers, not malicious ones. For most threat models in this vault, that's not enough.

---

## Three solutions

### 1. vFHE: FHE composed with a SNARK

The server produces a SNARK proof that "I evaluated the agreed circuit `C` on the input ciphertext I received and produced this output ciphertext." The decryptor verifies the SNARK in milliseconds, then decrypts.

```
Client:  enc(x) ─► Server
Server:  computes c = C(enc(x))
         proves π = SNARK("c is C applied to enc(x)")
Client:  verifies π, decrypts c
```

Active research area. Examples: Rinocchio (2018), the original vFHE construction, still impractical. Modern follow-ups in Aleo, Zama experiments. Open problem: SNARK overhead on FHE circuits is currently 100x-1000x the FHE cost, making vFHE 10⁴-10⁶x slower than plaintext for non-trivial circuits.

### 2. FHE inside an attested TEE

The server runs the FHE evaluator inside a TEE (TDX, SEV-SNP, H100 CC). The TEE attestation pins the binary; the binary's source is audited; therefore the evaluator computed the agreed function. Confidentiality is double-bound (FHE plus TEE), and integrity comes from the TEE.

This is the production pattern in 2026 for any deployed FHE-with-integrity. Faster than vFHE by orders of magnitude.

Trade-off: trust shifts from "math alone" to "math plus hardware vendor". For users who already trust TEEs (which is most production deployments), this is a free win.

### 3. Threshold FHE with active-secure MPC

The FHE secret key is split across `n` parties via threshold sharing; computation happens in the open over public ciphertexts; final decryption is threshold. With active-secure MPC during decryption, malicious parties are detected and the protocol aborts with proof.

Crucially: threshold FHE alone does not give evaluation integrity. It gives:

- Distributed decryption-key trust.
- Active-secure MPC during the threshold-decrypt step.

For evaluation correctness, you still need a SNARK over the homomorphic circuit, an attested TEE, or honest-majority MPC over the evaluation itself.

This pattern fits multi-party FHE settings (consortiums, federated learning) where no single party is trusted to hold the decryption key.

---

## Composition patterns

| Goal | Stack |
|------|-------|
| **Cheapest, no integrity** | Plain FHE — assumes honest server |
| **Mathematical integrity** (no hardware trust) | FHE + SNARK over the circuit (vFHE) |
| **Production integrity** (vendor trust OK) | FHE inside attested TDX/SEV-SNP CVM |
| **Multi-party trust split** | Threshold FHE + active-secure MPC for decryption |
| **Maximum** | All of the above stacked, where the cost is acceptable |

---

## Real deployments

- **Zama fhEVM** — confidential smart contracts on Ethereum. Uses leveled CKKS-style FHE; integrity via consensus plus a threshold-decryption committee. Not full vFHE.
- **Apple Private Cloud Compute** — TEE-based confidentiality with code transparency, not FHE. The architecture explicitly chose TEEs over FHE for performance.
- **Microsoft SEAL / Confidential Inferencing** — FHE-via-TEE patterns, both library and Azure-hosted.
- **Phala Cloud / Marlin Oyster** — TEE-attested compute, with FHE composable on top for specific use cases.

In 2026, production FHE-with-integrity is FHE-in-TEE, not vFHE. Pure-math vFHE remains research.

---

## Why this matters for this vault

The Confidential Computing section sometimes leans on FHE as the future of confidential AI; the Cryptography section sometimes leans on FHE as a TEE-replacement. Both elide the integrity gap. Honest framing:

- FHE is best at confidentiality against an honest-but-curious server with sufficient compute.
- TEEs are best at confidentiality plus integrity against a curious-or-malicious server, with a hardware-vendor trust assumption.
- vFHE is best at eventually removing the hardware-vendor assumption, but the 100x-1000x SNARK cost makes it impractical today for most workloads.
- Threshold FHE is best at key-trust splitting; orthogonal to evaluation integrity.

Knowing which one you're picking, and why, is the discipline.

---

## Trade-offs

### Strengths

- Bootstrapping unlocks unlimited depth: true FHE.
- Multiple integrity options depending on threat model and budget.
- Active research field, with performance improvements year over year.

### Limitations

- Bootstrap is expensive. Even with PBS, deep circuits take seconds; not real-time for most workloads.
- vFHE is currently impractical. Research only.
- TEE-FHE composition introduces TEE trust to FHE's pure-math story.
- Parameter selection is delicate; mistakes break security or performance.

---

## Related files

- [Overview - Fully Homomorphic Encryption](/cryptography/overview-fully-homomorphic-encryption) — main overview
- [Overview - Zero-Knowledge Proofs](/zero-knowledge) — SNARK side of vFHE
- [Multi-Party Computation](/cryptography/multi-party-computation) — threshold FHE composition
- [Overview - Confidential Computing](/confidential-computing) — TEE-FHE pattern
- [MOC - Composing Primitives](/meta/moc-composing-primitives)

---

## Primary sources

- Gentry, *A Fully Homomorphic Encryption Scheme*, Stanford PhD thesis, 2009.
- Halevi & Shoup, *Bootstrapping for HElib*, EUROCRYPT 2015.
- Chillotti, Gama, Georgieva, Izabachène, *TFHE: Fast Fully Homomorphic Encryption over the Torus*, ASIACRYPT 2016.
- Cheon et al., *Bootstrapping for Approximate Homomorphic Encryption*, EUROCRYPT 2018.
- Fiore, Gennaro, Pastro, *Efficiently Verifiable Homomorphic Computations*, ePrint 2014.
- Bois, Cascudo, Fiore, Kim, *Flexible and Efficient Verifiable Computation on Encrypted Data*, PKC 2021 (vFHE under PIOP).
- Atapoor, Smart, Lopez, *Compact Verifiable Computation* and follow-ups.
- OpenFHE: [openfhe.org](https://www.openfhe.org).
- tfhe-rs (Zama Concrete): [github.com/zama-ai/tfhe-rs](https://github.com/zama-ai/tfhe-rs).
- HElib: [github.com/homenc/HElib](https://github.com/homenc/HElib).

