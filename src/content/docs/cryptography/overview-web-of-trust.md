---
title: "Web of Trust"
tags:
  - "web-of-trust"
  - "wot"
  - "trust-network"
  - "reputation"
  - "nostr"
  - "openpgp"
  - "gpg"
  - "identity"
---
## Overview

**Web of Trust (WoT)** is a decentralized model for establishing identity authenticity without relying on centralized certificate authorities. In a WoT system, trust is propagated through a network of peer-to-peer attestations — if Alice trusts Bob, and Bob trusts Charlie, then Alice can derive a trust assessment of Charlie through the transitive relationship.

This model exists in two dominant forms today:

1. **OpenPGP/GPG Web of Trust** — The classic model from PGP (Pretty Good Privacy), established in the 1990s
2. **Nostr WoT** — A modern, social-graph-based trust network emerging from the Nostr protocol

> "In a world where institutions are increasingly untrustworthy, peer-to-peer trust networks become the only viable foundation for digital identity." — Ungovernable.tech

---

## Historical Context

### The Origin (1991)

The concept emerged from Phil Zimmermann's **PGP (Pretty Good Privacy)**, released in 1991. PGP introduced the idea that trust could be established through a "web of trust" rather than hierarchical certificate authorities:

- Users sign each other's public keys
- Trust is transitive: if you trust Alice, and Alice has signed Bob's key, you have a trust path to Bob
- No central authority controls who can trust whom

### The OpenPGP Standard (1996)

The **OpenPGP standard** (RFC 4880, updated to RFC 9580) formalized the web of trust model:

- **Certification signatures** — Keys can sign other keys with trust levels (undefined, none, marginal, full)
- **Trust signatures** — Special signatures that propagate trust
- **Validity** — A key is "valid" if there's a sufficient trust path to a trusted key

### The Modern Revival (2020s)

Two developments have revitalized WoT concepts:

1. **Nostr Protocol (2020)** — Built trust into the protocol itself via follow graphs and NIP-26 delegation
2. **Proof of Usefulness (2023+)** — New metrics that measure trust through actual network activity

---

## How Web of Trust Works

### Core Concepts

```
┌─────────┐        signs         ┌─────────┐
│  Alice  │ ───────────────────► │   Bob   │
└─────────┘                     └─────────┘
     │                               │
     │ trusts                       │ signs
     ▼                               ▼
┌─────────┐                     ┌─────────┐
│ Trust   │ ──────────────────► │ Charlie │
│ Path    │     transitive      │         │
└─────────┘                     └─────────┘
```

### Trust Propagation

The fundamental algorithm is **path-finding** in a directed graph:

1. **Build the graph** — Nodes = keys/users, Edges = trust signatures
2. **Find paths** — Use Dijkstra's algorithm or BFS to find trust paths
3. **Aggregate trust** — Combine edge weights (trust levels) into a path score
4. **Apply threshold** — If accumulated trust exceeds threshold, consider target valid

### Trust Levels (OpenPGP)

| Level | Meaning |
|-------|---------|
| **undefined** | No trust assertion |
| **none** | Key is explicitly untrusted |
| **marginal** | Trust the key, but with caveats |
| **full** | Full trust in this key |

### Validation Threshold

Most implementations require:
- **One path to a fullytrusted key**, OR
- **Two independent paths to marginally-trusted keys**

---

## Major Implementations

### Nostr Web of Trust

**Nostr** (Notes and Other Stuff Transmitted by Relays) has an implicit WoT built from its follow model.

#### Key Components

- **Follow Graph** — Users follow each other, creating an implicit trust network
- **NIP-26 Delegation** — Allows delegated event signing (limited delegation, time-limited)
- **nostr-wot toolkit** — Rust-based open-source tools for computing trust

#### Resources

- **[nostr-wot GitHub](https://github.com/nostr-wot)** — Open-source tools for computing, querying, and visualizing trust networks
- **[nostr-wot.com](https://nostr-wot.com/)** — Browser extension providing NIP-07 signing, Lightning wallet, and trust scoring
- **[NIP-26](https://nips.nostr.com/26)** — Delegated event signing specification
- **[Nostr Protocol NIPs](https://github.com/nostr-protocol/nips)** — Full protocol specification

#### Trust Scoring in Nostr

Nostr WoT implements **social distance scoring**:

- Your "first degree" = people you follow directly
- "Second degree" = people your follows follow
- Trust badges and spam filtering based on your actual network
- No centralized blocklists required

### The Web of Trust Hackathon (2025-2026)

A major initiative driving current development:

- **Timeline**: November 2025 – April 2026 (6-month sprint)
- **Focus**: Open-source tools for decentralized reputation systems
- **Deliverables**: Trust computation, querying, and visualization infrastructure

### nostr-wot Browser Extension

The [nostr-wot.com](https://nostr-wot.com/) extension brings WoT to any Nostr client:

- **NIP-07 signing** — Acts as identity provider for any Nostr app
- **Lightning wallet** — Built-in wallet with zap support
- **Trust scoring** — Calculates trust based on social distance
- **Universal** — Works across all Nostr clients via browser extension
- **Proof of Usefulness** — Achieved 57 PoU score in recent development

### WKD developments (2025-2026)

Web Key Directory continues advancing:

- **New IETF draft**: [draft-koch-openpgp-webkey-service-21](https://datatracker.ietf.org/doc/draft-koch-openpgp-webkey-service/) (November 2025)
- **keys.openpgp.org**: Active production service, default for Thunderbird, GPG Suite, OpenKeychain, Sequoia-PGP
- **Broad adoption**: Major email clients and tools integrate WKD by default

### OpenPGP/GPG Web of Trust

#### Active Implementations

- **[PGPainless](https://pgpainless.org/)** — OpenPGP library for Java with WOT module
  - **[pgpainless-wot](https://github.com/pgpainless/pgpainless-wot)** — Web of Trust implementation with Dijkstra path-finding

- **[Bouncy Castle](https://www.bouncycastle.org/)** — Java cryptography library
  - **[bc-pgp-wot](https://github.com/subshare/bc-pgp-wot)** — OpenPGP WOT implementation

- **[GnuPG](https://www.gnupg.org/)** — The original implementation
  - `gpg --edit-key` → `trust` command for managing trust levels

#### Keyserver Infrastructure

- **SKS Keyserver Network** — Historically the primary keyserver pool (now largely defunct due to poisoning attacks)
- **Web Key Directory (WKD)** — Modern protocol for fetching keys directly from domains
- **[Keyoxide](https://keyoxide.org/)** — Modern key verification service that supports WKD and trust path visualization

#### Resources

- **[gpg.wtf](https://gpg.wtf/)** — Educational resource about OpenPGP WoT
- **[Keyoxide Docs](https://docs.keyoxide.org/)** — Verification and proof documentation

---

## Trust Metrics and Algorithms

### Path-Finding Approaches

| Algorithm | Description | Use Case |
|-----------|-------------|----------|
| **Dijkstra** | Shortest weighted path | Find most trusted path |
| **BFS** | Breadth-first search | Find any path within N hops |
| **PageRank** | Eigenvector centrality | Global reputation scoring |
| **Local Clustering** | Community detection | Identify trust clusters |

### Proof of Usefulness

A newer metric that emerged from Nostr development:

- Measures trust through **actual network activity**
- Combines **social graph analysis** with **proof of work**
- Higher score = more verification through real interactions
- Addresses Sybil attack vulnerabilities in pure graph-based trust

### Trust Score Calculation

```
TrustScore(user) = f(own_trust, first_degree_trust, path_length, ...)
```

Where:
- **own_trust** = direct trust you've assigned
- **first_degree_trust** = trust in people you follow
- **path_length** = longer paths = less trust
- **path_diversity** = multiple independent paths = more trust

---

## Use Cases

### 1. Identity Verification

- Verify that a public key belongs to the claimed identity
- No centralized identity provider needed
- Particularly useful for:
  - Developer verification (commit signing)
  - Encrypted communication
  - Decentralized social networks

### 2. Spam and Abuse Prevention

- Filter content based on trust network
- No centralized blocklists
- Particularly relevant for:
  - Nostr spam filtering
  - Email spam classification
  - Content moderation in decentralized systems

### 3. Reputation Systems

- Build reputation through peer attestations
- Use for:
  - Marketplace trust
  - Content creator verification
  - DAO governance (reputation-weighted voting)

### 4. Key Recovery

- Web of trust can provide key recovery mechanisms
- Social recovery through trusted contacts
- No single point of failure

### 5. Delegation

- NIP-26 style delegated signing
- Allow trusted parties to act on your behalf
- Time-limited, revokable permissions

---

## Evidence at a Glance

| Implementation | Type | Maturity | Status |
|----------------|------|----------|--------|
| **GnuPG** | OpenPGP WoT | Mature | Active, established |
| **PGPainless** | OpenPGP WoT | Emerging | Active development |
| **nostr-wot** | Nostr Trust | Emerging | Active, 2025 hackathon |
| **Keyoxide** | Verification | Beta | Active |
| **NIP-26** | Delegation | Mature | Protocol standard |

---

## Trade-offs

### Strengths

- **Decentralized** — No single point of trust failure
- **Permissionless** — Anyone can participate
- **Transitive** — Trust propagates through the network
- **Resilient** — Network effects improve security

### Limitations

- **Cold start problem** — New users have no trust connections
- **Sybil attacks** — Attackers can create many identities to manipulate trust
- **Fragmentation** — Isolated subgraphs may not connect
- **Complexity** — User experience can be confusing
- **Key rotation** — Trust can become stale

### Attack Vectors

| Attack | Description | Mitigation |
|--------|-------------|------------|
| **Sybil** | Create many fake identities | Proof of work, Proof of use |
| **Trust flooding** | Flood with signatures | Path length limits, thresholding |
| **Key poisoning** | Insert malicious keys | Key pinning, careful verification |
| **Centralization** | Trust concentrates | Monitor central nodes |

---

## Evidence at a Glance

| Implementation | Type | Maturity | Status |
|----------------|------|----------|--------|
| **GnuPG** | OpenPGP WoT | Mature | Active, established |
| **PGPainless** | OpenPGP WoT | Emerging | Active development |
| **nostr-wot** | Nostr Trust | Emerging | Active, 2025-2026 hackathon |
| **nostr-wot extension** | Browser extension | Beta | In production |
| **Keyoxide** | Verification | Beta | Active |
| **Web Key Directory (WKD)** | Key distribution | Mature | IETF draft (Nov 2025) |
| **keys.openpgp.org** | Keyserver | Production | Active service |

---
---

## Related Files

- [Overview - Identity & Pseudonymity](/identity) — Pseudonymous identity and reputation
- [Overview - Decentralized Identity](/identity/overview-decentralized-identity) — Formal DID/VC stacks
- [Overview - Encrypted Messaging](/encrypted-messaging) — PGP usage in messaging, Nostr DMs
- [Overview - Confidential Computing](/confidential-computing) — Complementary trust mechanisms
- [Nostr Deep Dive](/encrypted-messaging/nostr-deep-dive) — Full Nostr protocol analysis

---

## Further Reading

- [OpenPGP RFC 9580](https://datatracker.ietf.org/doc/html/rfc9580) — Updated standard
- [NIP-26 Specification](https://nips.nostr.com/26) — Delegation in Nostr
- [nostr-wot GitHub](https://github.com/nostr-wot) — Trust network tools
- [PGPainless WOT](https://github.com/pgpainless/pgpainless-wot) — Java implementation
- [Keyoxide Documentation](https://docs.keyoxide.org/) — Verification guides
