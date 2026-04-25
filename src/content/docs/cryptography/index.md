---
title: "Cryptography"
tags:
  - "cryptography"
  - "fhe"
  - "zk"
  - "pir"
sidebar: {"label":"Overview","order":0}
---
This section covers advanced cryptographic primitives that enable privacy-preserving computation — FHE, ZK proofs, PIR, and post-quantum algorithms.

---

## Key Files

### [Overview - Fully Homomorphic Encryption](/cryptography/overview-fully-homomorphic-encryption)

FHE enables computation on encrypted data — the foundation of privacy-preserving cloud computing.

### [Overview - Private Information Retrieval](/cryptography/overview-private-information-retrieval)

PIR lets a client fetch record `i` without the server learning `i` — useful for DNS, certificate transparency, LLM retrieval over public corpora.

### [Overview - Web of Trust](/cryptography/overview-web-of-trust)

Decentralized trust models — OpenPGP WoT and Nostr social-graph WoT.

### Cross-section overviews

These topics live in their own sections but are cryptography-adjacent:

- [Overview - Zero-Knowledge Proofs](/zero-knowledge) — under [09 - Zero-Knowledge](../09-Zero-Knowledge)
- [Overview - Post-Quantum Cryptography](/post-quantum) — under [10 - Post-Quantum](../10-Post-Quantum)
- Bulletproofs, BBS+, threshold signatures — see [Glossary](/meta/glossary)

---

## Technology Map

```
Cryptography
├── FHE
│   ├── OpenFHE
│   ├── Zama
│   └── Applications
├── Zero-Knowledge
│   ├── SNARKs
│   ├── STARKs
│   └── Applications
├── PIR
│   ├── Libraries
│   └── Use Cases
└── Post-Quantum
    ├── ML-KEM
    └── ML-DSA
```

---

## Quick Reference

| Problem | Solution |
|---------|----------|
| Compute on encrypted data | FHE |
| Prove without revealing | ZK |
| Query privately | PIR |
| Quantum resistance | PQC |
