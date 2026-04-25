---
title: "Overview - Fully Homomorphic Encryption"
tags:
  - "fhe"
  - "fully-homomorphic-encryption"
  - "cryptography"
  - "privacy"
  - "homomorphic-encryption"
---
## Overview

**Fully Homomorphic Encryption (FHE)** is a revolutionary encryption scheme that allows computation on **encrypted data** without ever decrypting it. This might sound like magic, but it's real mathematics. In the world that FHE enables:

- Your data stays encrypted in the cloud throughout its entire lifecycle
- AI models can process your encrypted inputs without ever seeing the plaintext
- Multiple parties can contribute data to a joint computation without revealing their inputs

This is fundamentally different from other privacy technologies:
- **Encryption at rest**: Data is encrypted on disk
- **Encryption in transit**: Data is encrypted over the wire
- **FHE**: Data is encrypted *during computation*

> "In a world where your private information is not for sale and your attention is not the product, data is a liability not an asset. FHE can enable privacy-preserving solutions for many/most database applications." — Ungovernable.tech

---

## Historical Context

### The Problem (1978)

Rivest, Adleman, and Dertouzos posed the problem: can we create encryption schemes that allow arbitrary computation on encrypted data? They called it "privacy homomorphisms."

### The Solution (2009)

Craig Gentry, working at IBM, published the first FHE scheme in his Stanford PhD dissertation. His breakthrough used a technique called "bootstrapping" — self-referential encryption that allows the encryption scheme to evaluate its own decryption function.

**The problem**: Gentry's scheme was theoretically correct but impossibly slow — approximately **1 trillion times** slower than plaintext computation.

### The Progress (2011-Present)

Multiple generations of FHE schemes improved performance:

| Generation | Scheme | Speedup vs Gentry | Trusted Setup |
|------------|--------|-----------------|-------------|
| 1st | 2009 Gentry | 1x (baseline) | Yes |
| 2nd | Brakerski-Gentry-Vaikuntanathan (2011) | ~100x | Yes |
| 3rd | Fan-Vercauteren (2012, BFV) | ~10,000x | Yes |
| 4th | Cheon-Kim-Kim-Song (2016, CKKS) | ~100,000x | Yes |
| 5th | TFHE (2016) | ~1,000,000x | No |

### The Current State (2024+)

FHE is now practical for specific use cases. The leading libraries are within **100-1000×** slower than plaintext for appropriate workloads. Key developments:

- **Zama** — Concrete (TFHE-based), fhEVM (EVM + FHE)
- **OpenFHE** — Open-source, multiple schemes
- **Google (FHE-Wasm)** — WASM implementation

---

## How FHE Works

### The Core Concept

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

This means you can send encrypted numbers to a server, have the server do math on them, and get back an encrypted result that you can decrypt.

### The Mathematical Underpinnings

Modern FHE schemes rely on **lattice-based cryptography**:

- **Ring-Learning With Errors (RLWE)** — The foundation of most modern FHE
- **LWE (Learning With Errors)** — Simpler but less efficient
- **NTRU** — Alternative lattice problem

The security rests on the hardness of:
- Shortest Vector Problem (SVP)
- Learning With Errors (LWE)
- Ring-LWE

### The Challenge: Noise

Every multiplication increases "noise" in the ciphertext. When noise grows too large, decryption fails. Solutions:

1. **Bootstrapping**: Refresh ciphertext by homomorphically decrypting and re-encrypt
2. **Modulus switching**: Rescale the ciphertext
3. **Careful parameter selection**: Larger keys = more room for noise

---

## FHE Schemes Comparison

| Scheme | Year | Use Case | Pros | Cons |
|--------|------|---------|------|------|
| **BFV** | 2012 | Integer arithmetic | Exact arithmetic | Large ciphertext |
| **CKKS** | 2016 | Approximate math | Efficient | Approximation error |
| **TFHE** | 2016 | Boolean circuits | Bootstrapping, no trust setup | Slower for large data |
| **BGV** | 2012 | Integer arithmetic | Mature | Requires expertise |

### When to Use Each

- **BFV**: Integer operations, financial calculations
- **CKKS**: Machine learning (inference), signal processing
- **TFHE**: Boolean logic, complex functions, privacy-preserving AI

---

## Major Implementations

### Open Source

- **[OpenFHE](https://www.openfhe.org/)** — Open-source, multiple schemes (Brakerski-Fan-Vercauteren, CKKS, BGV, TFHE). The most comprehensive library.

- **[Zama](https://www.zama.ai/)** — Concrete (TFHE-wasm), fhEVM (EVM + FHE). Commercial.

- **[Microsoft SEAL](https://github.com/microsoft/SEAL)** — BFV and CKKS. Academic-friendly.

- **[FHE-Wasm](https://github.com/google/fhe-owasm)** — Google's WASM implementation of TFHE.

### Commercial/Cloud

- **Zama Cloud** — SaaS FHE
- **Google FHE Inference** — Hosted service
- **Intel HE Toolkit** — Hardware acceleration

---

## Use Cases

### 1. Privacy-Preserving AI Inference

Your encrypted data → Model processes encrypted → Encrypted output → You decrypt

- Medical AI on sensitive patient data
- Financial models on transaction data
- Personal AI assistants without data leakage

### 2. Private Information Retrieval (PIR)

Query a database without the server knowing what you asked for:

- Private database search
- Voting systems
- Private set intersection

### 3. Confidential Smart Contracts

Execute EVM code on encrypted state:

- [fhEVM](https://www.zama.ai/product/fhevm) — FHE+Ethereum
- Private DeFi
- Confidential voting

### 4. Secure Multi-Party Computation

Parties contribute encrypted inputs → Joint computation → Results revealed only to authorized parties

---

## Evidence at a Glance

| Use Case | Maturity | Evidence |
|----------|----------|----------|
| AI Inference | Emerging | Research + startups |
| PIR | Beta | Active development |
| fhEVM | Alpha | Zama, early users |
| MPC | Production | Established tools |

---

## Trade-offs

### Strengths

- **Mathematical privacy** — Not dependent on operational security
- **No trusted party for confidentiality** — You hold the keys
- **Composable** — Can combine with other FHE schemes and with ZK / TEEs

> **Important caveat:** FHE alone does **not** provide verifiability. A malicious server can return any ciphertext it wants and the decryptor cannot tell the result is correct. To get integrity you need to combine FHE with a SNARK/STARK over the homomorphic circuit (verifiable FHE / vFHE), with an attested TEE running the FHE evaluator, or with a multi-party FHE protocol with active-secure thresholds.

### Limitations

- **Performance** — 100-1000x slower than plaintext
- **Complexity** — High implementation expertise required
- **Noise management** — Requires careful parameter tuning
- **Key size** — Large keys (MB to GB for some schemes)
- **Functionality limits** — Not all functions are efficient

### Hybrid Approaches

In practice, FHE is often combined with:
- **TEEs** (confidential computing) for better performance
- **Secure enclaves** for key management
- **ZK proofs** for integrity verification

---

## Related Files

- [Overview - Confidential Computing](/confidential-computing/overview-confidential-computing) — FHE + TEEs for stronger guarantees
- [Overview - Private Information Retrieval](/cryptography/overview-private-information-retrieval) — Private queries (a key FHE use case)
- [Overview - Zero-Knowledge Proofs](/zero-knowledge/overview-zero-knowledge-proofs) — Integrity verification (FHE alone does *not* give verifiability)
- [Overview - Post-Quantum Cryptography](/post-quantum/overview-post-quantum-cryptography) — Lattice assumptions are shared
