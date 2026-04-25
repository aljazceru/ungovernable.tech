---
title: "Meta"
tags:
  - "meta"
  - "readme"
  - "glossary"
  - "methodology"
sidebar: {"label":"Overview","order":0}
---
This directory contains the foundational documentation for the Ungovernable.tech knowledge base — its philosophy, methods, glossary, and evaluation standards.

---

## Philosophy

Ungovernable.tech represents a fundamentally different approach to digital infrastructure:

| Principle | Description |
|-----------|-------------|
| **Privacy by Default** | Systems should not leak metadata |
| **Cryptographic Sovereignty** | Your keys, your coins, your data |
| **Decentralization** | No single point of failure |
| **First-Principles Thinking** | Evaluate trust models rigorously |
| **Operational Security** | Usability matters for security |
| **Resilience** | Works when the internet doesn't |

---

## Files

### **README**

Ungovernable.tech is a knowledge base for building an uncensorable, surveillance-resistant, and financially sovereign digital infrastructure. Philosophy: cryptography over legislation, decentralization over centralization, individual sovereignty over institutional trust.

### [Glossary](/meta/glossary)

Comprehensive definitions of all key terms:

| Category | Key Terms |
|----------|-----------|
| **Confidential Computing** | TEE, SGX, SEV-SNP, TDX, CoCo, Attestation |
| **Cryptography** | FHE, ZK, PIR, ORAM, Bulletproofs |
| **Networking** | DTN, DHT, Mixnet, Yggdrasil, LoRa |
| **Financial** | Lightning, CoinJoin, Hardware wallets |
| **Identity** | DID, VC, SSI, WOT |

### **Research Methodology**

Systematic approach to evaluating privacy and decentralization claims:

1. **Primary Sources Only** — Academic papers (ePrint, IACR), audited specs
2. **Trust Model Analysis** — What must you trust? What happens if trust is broken?
3. **Attack Surface** — What are practical attack vectors?
4. **Decentralization Claims** — How many entities can shut it down?
5. **Operational Complexity** — What's the user experience?

---

## Key Vault Statistics

| Metric | Value |
|--------|-------|
| Total content files | ~50 |
| Primary Sections | 12 |
| Cross-cutting MOCs | 4 |
| Status | Active expansion |

> Stats are approximate. Run `find . -name "*.md" \| wc -l` for current count.

---

## Cross-Reference Map

This Meta section connects to all other vault sections:

| Section | Focus | Landing page |
|---------|-------|--------------|
| 01 — Confidential Computing | TEEs, Hardware Security | [Overview - Confidential Computing](/confidential-computing) |
| 02 — Cryptography | FHE, ZK, PIR, WoT | [Overview - Fully Homomorphic Encryption](/cryptography/overview-fully-homomorphic-encryption) |
| 03 — Decentralized DNS | DNS alternatives | [Overview - Decentralized DNS](/decentralized-dns) |
| 04 — Decentralized Compute | P2P markets | [Overview - Decentralized Compute](/decentralized-compute) |
| 05 — Off-Grid Networks | Mesh, DTN | [Overview - Off-Grid Networks](/off-grid-networks) |
| 06 — Financial Sovereignty | Bitcoin tech | [Overview - Financial Sovereignty](/financial-sovereignty) |
| 07 — Encrypted Messaging | E2EE protocols | [Overview - Encrypted Messaging](/encrypted-messaging) |
| 08 — Mix Networks | Tor, I2P, Nym | [Overview - Mix Networks](/mix-networks) |
| 09 — Zero-Knowledge | ZK proofs | [Overview - Zero-Knowledge Proofs](/zero-knowledge) |
| 10 — Post-Quantum | NIST algorithms | [Overview - Post-Quantum Cryptography](/post-quantum) |
| 11 — Identity | SSI, DIDs, pseudonymity | [Overview - Decentralized Identity](/identity/overview-decentralized-identity) |

---

## Contributing to This Vault

### Quality Standards

Every file must have:
- YAML frontmatter with title, tags, category, created, updated, status
- Hierarchical structure (H2/H3 headings)
- Internal wikilinks to related files
- Primary source citations
- "Trade-offs" and "Attack Surface" sections

### Priority Areas

1. **Confidential Computing** — High practical value
2. **Off-Grid Networks** — Growing interest
3. **Financial Sovereignty** — Always relevant
4. **Encrypted Messaging** — Nostr ecosystem expansion

### Next Steps

- Review **Research Methodology** before adding content
- Use existing ungovernable.tech pages as content sources
- Link new content to existing files via wikilinks
