---
title: "Fully Homomorphic Encryption"
tags:
  - "fhe"
  - "fully-homomorphic-encryption"
  - "cryptography"
  - "privacy"
  - "homomorphic-encryption"
---
## Overview

Fully Homomorphic Encryption (FHE) is an encryption scheme that allows computation on encrypted data without decrypting it. The result:

- Data stays encrypted in the cloud through its entire lifecycle.
- AI models can process encrypted inputs without seeing the plaintext.
- Multiple parties can contribute data to a joint computation without revealing their inputs.

This differs from other privacy technologies:
- Encryption at rest: data is encrypted on disk.
- Encryption in transit: data is encrypted over the wire.
- FHE: data is encrypted during computation.

> "In a world where your private information is not for sale and your attention is not the product, data is a liability not an asset. FHE can enable privacy-preserving solutions for many/most database applications." — Ungovernable.tech

---

## Historical context

### The problem (1978)

Rivest, Adleman, and Dertouzos asked whether encryption schemes could allow arbitrary computation on encrypted data. They called the idea "privacy homomorphisms."

### The solution (2009)

Craig Gentry, working at IBM, published the first FHE scheme in his Stanford PhD dissertation. The breakthrough was "bootstrapping": self-referential encryption that lets the scheme evaluate its own decryption function.

The catch: Gentry's scheme was theoretically correct but impossibly slow, roughly 1 trillion times slower than plaintext computation.

### Progress (2011-present)

Multiple generations of FHE schemes improved performance:

| Generation | Scheme | Speedup vs Gentry | Trusted Setup |
|------------|--------|-----------------|-------------|
| 1st | 2009 Gentry | 1x (baseline) | Yes |
| 2nd | Brakerski-Gentry-Vaikuntanathan (2011) | ~100x | Yes |
| 3rd | Fan-Vercauteren (2012, BFV) | ~10,000x | Yes |
| 4th | Cheon-Kim-Kim-Song (CKKS, ASIACRYPT 2017) | ~100,000x | Yes |
| 5th | TFHE (2016) | ~1,000,000x | No |

### Current state (2024+)

FHE is now practical for specific use cases. The leading libraries are within 100-1000x of plaintext for appropriate workloads. Notable developments:

- Zama: Concrete (TFHE-based), fhEVM (EVM + FHE).
- OpenFHE: open-source, multiple schemes.
- Google FHE-Wasm: WASM implementation.

---

## How FHE works

### Core concept

In regular encryption:
```
Encrypt(plaintext) → ciphertext
Decrypt(ciphertext) → plaintext
Encrypt(a) + Encrypt(b) ≠ Encrypt(a + b)  ← Addition doesn't preserve
```

In homomorphic encryption:
```
Encrypt(a) ⊕ Encrypt(b) = Encrypt(a + b)    ← Arithmetic on ciphertext
Encrypt(a) ⊗ Encrypt(b) = Encrypt(a × b)
```

You can send encrypted numbers to a server, have the server do math on them, and get back an encrypted result that you can decrypt.

### Mathematical underpinnings

Modern FHE schemes rely on lattice-based cryptography:

- Ring-Learning With Errors (RLWE), the foundation of most modern FHE.
- LWE (Learning With Errors), simpler but less efficient.
- NTRU, an alternative lattice problem.

Security rests on the hardness of:
- Shortest Vector Problem (SVP)
- Learning With Errors (LWE)
- Ring-LWE

### The challenge: noise

Every multiplication increases "noise" in the ciphertext. When noise grows too large, decryption fails. Solutions:

1. Bootstrapping: refresh ciphertext by homomorphically decrypting and re-encrypting.
2. Modulus switching: rescale the ciphertext.
3. Careful parameter selection: larger keys give more room for noise.

---

## FHE schemes comparison

| Scheme | Year | Use Case | Pros | Cons |
|--------|------|---------|------|------|
| **BFV** | 2012 | Integer arithmetic | Exact arithmetic | Large ciphertext |
| **CKKS** | 2017 | Approximate math | Efficient | Approximation error |
| **TFHE** | 2016 | Boolean circuits | Bootstrapping, no trust setup | Slower for large data |
| **BGV** | 2012 | Integer arithmetic | Mature | Requires expertise |

### When to use each

- BFV: integer operations, financial calculations.
- CKKS: machine learning (inference), signal processing.
- TFHE: Boolean logic, complex functions, privacy-preserving AI.

---

## Major implementations

### Open source

- **[OpenFHE](https://www.openfhe.org/)** — Open-source, multiple schemes (Brakerski-Fan-Vercauteren, CKKS, BGV, TFHE). The most comprehensive library.

- **[Zama](https://www.zama.ai/)** — Concrete (TFHE-wasm), fhEVM (EVM + FHE). Commercial.

- **[Microsoft SEAL](https://github.com/microsoft/SEAL)** — BFV and CKKS. Academic-friendly.

- **[FHE-Wasm](https://github.com/google/fhe-owasm)** — Google's WASM implementation of TFHE.

### Commercial / cloud

- Zama Cloud: SaaS FHE.
- Google FHE Inference: hosted service.
- Intel HE Toolkit: hardware acceleration.

---

## Use cases

### 1. Privacy-preserving AI inference

Encrypted data goes in, the model processes encrypted, encrypted output comes back, you decrypt.

- Medical AI on sensitive patient data.
- Financial models on transaction data.
- Personal AI assistants without data leakage.

### 2. Private Information Retrieval (PIR)

Query a database without the server knowing what you asked for:

- Private database search.
- Voting systems.
- Private set intersection.

### 3. Confidential smart contracts

Execute EVM code on encrypted state:

- [fhEVM](https://www.zama.ai/product/fhevm), FHE plus Ethereum.
- Private DeFi.
- Confidential voting.

### 4. Secure multi-party computation

Parties contribute encrypted inputs, joint computation runs, results are revealed only to authorized parties.

---

## Evidence at a glance

| Use Case | Maturity | Evidence |
|----------|----------|----------|
| AI Inference | Emerging | Research + startups |
| PIR | Beta | Active development |
| fhEVM | Alpha | Zama, early users |
| MPC | Production | Established tools |

---

## Trade-offs

### Strengths

- Mathematical privacy, not dependent on operational security.
- No trusted party for confidentiality. You hold the keys.
- Composable. Can combine with other FHE schemes and with ZK or TEEs.

> Important caveat: FHE alone does not provide verifiability. A malicious server can return any ciphertext it wants and the decryptor cannot tell the result is correct. To get integrity, combine FHE with a SNARK/STARK over the homomorphic circuit (verifiable FHE / vFHE), with an attested TEE running the FHE evaluator, or with a multi-party FHE protocol with active-secure thresholds.

### Limitations

- Performance: 100-1000x slower than plaintext.
- Complexity: high implementation expertise required.
- Noise management: requires careful parameter tuning.
- Key size: large keys (MB to GB for some schemes).
- Functionality limits: not all functions are efficient.

### Hybrid approaches

In practice, FHE is often combined with:
- TEEs (confidential computing) for better performance.
- Secure enclaves for key management.
- ZK proofs for integrity verification.

---

## Related files

- [Overview - Confidential Computing](/confidential-computing) — FHE + TEEs for stronger guarantees
- [Overview - Private Information Retrieval](/cryptography/overview-private-information-retrieval) — Private queries (a key FHE use case)
- [Overview - Zero-Knowledge Proofs](/zero-knowledge) — Integrity verification (FHE alone does *not* give verifiability)
- [Overview - Post-Quantum Cryptography](/post-quantum) — Lattice assumptions are shared

