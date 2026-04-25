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

Web of Trust (WoT) is a decentralized model for establishing identity authenticity without relying on centralized certificate authorities. Trust is propagated through a network of peer-to-peer attestations: if Alice trusts Bob, and Bob has signed Charlie's key, Alice can derive a trust assessment of Charlie through the transitive relationship.

Two dominant forms exist today:

1. OpenPGP/GPG Web of Trust, the classic model from PGP (Pretty Good Privacy), established in the 1990s.
2. Nostr WoT, a newer social-graph-based trust network from the Nostr protocol.

> "In a world where institutions are increasingly untrustworthy, peer-to-peer trust networks become the only viable foundation for digital identity." — Ungovernable.tech

---

## Historical context

### The origin (1991)

The concept came from Phil Zimmermann's PGP (Pretty Good Privacy), released in 1991. PGP introduced the idea that trust could be established through a "web of trust" rather than hierarchical certificate authorities:

- Users sign each other's public keys.
- Trust is transitive: if you trust Alice, and Alice has signed Bob's key, you have a trust path to Bob.
- No central authority controls who can trust whom.

### The OpenPGP standard (1996)

The OpenPGP standard (RFC 4880, updated to RFC 9580) formalized the web of trust model:

- Certification signatures. Keys can sign other keys with trust levels (undefined, none, marginal, full).
- Trust signatures. Special signatures that propagate trust.
- Validity. A key is "valid" if there is a sufficient trust path to a trusted key.

### Recent revival (2020s)

Two developments brought WoT concepts back to attention:

1. The Nostr protocol (2020) built trust into the protocol itself via follow graphs and NIP-26 delegation.
2. Proof of Usefulness (2023+) introduced new metrics that measure trust through actual network activity.

---

## How web of trust works

### Core concepts

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

### Trust propagation

The basic algorithm is path-finding in a directed graph:

1. Build the graph. Nodes are keys/users, edges are trust signatures.
2. Find paths. Use Dijkstra or BFS to find trust paths.
3. Aggregate trust. Combine edge weights (trust levels) into a path score.
4. Apply a threshold. If accumulated trust exceeds the threshold, treat the target as valid.

### Trust levels (OpenPGP)

| Level | Meaning |
|-------|---------|
| **undefined** | No trust assertion |
| **none** | Key is explicitly untrusted |
| **marginal** | Trust the key, but with caveats |
| **full** | Full trust in this key |

### Validation threshold

Most implementations require:
- One path to a fully trusted key, or
- Two independent paths to marginally-trusted keys.

---

## Major implementations

### Nostr web of trust

Nostr (Notes and Other Stuff Transmitted by Relays) has an implicit WoT built from its follow model.

#### Components

- Follow graph. Users follow each other, creating an implicit trust network.
- NIP-26 delegation. Allows delegated event signing with limits and an expiry.
- nostr-wot toolkit. Rust-based open-source tools for computing trust.

#### Resources

- **[nostr-wot GitHub](https://github.com/nostr-wot)** — Open-source tools for computing, querying, and visualizing trust networks
- **[nostr-wot.com](https://nostr-wot.com/)** — Browser extension providing NIP-07 signing, Lightning wallet, and trust scoring
- **[NIP-26](https://nips.nostr.com/26)** — Delegated event signing specification
- **[Nostr Protocol NIPs](https://github.com/nostr-protocol/nips)** — Full protocol specification

#### Trust scoring in Nostr

Nostr WoT uses social distance scoring:

- "First degree" is the people you follow directly.
- "Second degree" is the people your follows follow.
- Trust badges and spam filtering are based on your actual network.
- No centralized blocklists are required.

### The Web of Trust Hackathon (2025-2026)

An initiative driving current development:

- Timeline: November 2025 to April 2026 (six-month sprint).
- Focus: open-source tools for decentralized reputation systems.
- Deliverables: trust computation, querying, and visualization infrastructure.

### nostr-wot browser extension

The [nostr-wot.com](https://nostr-wot.com/) extension brings WoT to any Nostr client:

- NIP-07 signing. Acts as identity provider for any Nostr app.
- Lightning wallet. Built-in wallet with zap support.
- Trust scoring. Calculates trust based on social distance.
- Universal. Works across all Nostr clients via browser extension.
- Proof of Usefulness. Reached a 57 PoU score in recent development.

### WKD developments (2025-2026)

Web Key Directory continues to advance:

- New IETF draft: [draft-koch-openpgp-webkey-service-21](https://datatracker.ietf.org/doc/draft-koch-openpgp-webkey-service/) (November 2025).
- keys.openpgp.org: active production service, default for Thunderbird, GPG Suite, OpenKeychain, Sequoia-PGP.
- Broad adoption: major email clients and tools integrate WKD by default.

### OpenPGP/GPG web of trust

#### Active implementations

- **[PGPainless](https://pgpainless.org/)** — OpenPGP library for Java with WOT module
  - **[pgpainless-wot](https://github.com/pgpainless/pgpainless-wot)** — Web of Trust implementation with Dijkstra path-finding

- **[Bouncy Castle](https://www.bouncycastle.org/)** — Java cryptography library
  - **[bc-pgp-wot](https://github.com/subshare/bc-pgp-wot)** — OpenPGP WOT implementation

- **[GnuPG](https://www.gnupg.org/)** — The original implementation
  - `gpg --edit-key` → `trust` command for managing trust levels

#### Keyserver infrastructure

- SKS Keyserver Network. Historically the primary keyserver pool, now largely defunct because of poisoning attacks.
- Web Key Directory (WKD). Modern protocol for fetching keys directly from domains.
- **[Keyoxide](https://keyoxide.org/)** — Modern key verification service that supports WKD and trust path visualization.

#### Resources

- **[gpg.wtf](https://gpg.wtf/)** — Educational resource about OpenPGP WoT
- **[Keyoxide Docs](https://docs.keyoxide.org/)** — Verification and proof documentation

---

## Trust metrics and algorithms

### Path-finding approaches

| Algorithm | Description | Use case |
|-----------|-------------|----------|
| **Dijkstra** | Shortest weighted path | Find most trusted path |
| **BFS** | Breadth-first search | Find any path within N hops |
| **PageRank** | Eigenvector centrality | Global reputation scoring |
| **Local Clustering** | Community detection | Identify trust clusters |

### Proof of usefulness

A newer metric from Nostr development:

- Measures trust through actual network activity.
- Combines social graph analysis with proof of work.
- Higher score means more verification through real interactions.
- Targets Sybil attack vulnerabilities in pure graph-based trust.

### Trust score calculation

```
TrustScore(user) = f(own_trust, first_degree_trust, path_length, ...)
```

Where:
- `own_trust` is direct trust you have assigned.
- `first_degree_trust` is trust in people you follow.
- `path_length` means longer paths give less trust.
- `path_diversity` means multiple independent paths give more trust.

---

## Use cases

### 1. Identity verification

- Verify that a public key belongs to the claimed identity.
- No centralized identity provider needed.
- Useful for:
  - Developer verification (commit signing).
  - Encrypted communication.
  - Decentralized social networks.

### 2. Spam and abuse prevention

- Filter content based on the trust network.
- No centralized blocklists.
- Relevant for:
  - Nostr spam filtering.
  - Email spam classification.
  - Content moderation in decentralized systems.

### 3. Reputation systems

- Build reputation through peer attestations.
- Use for:
  - Marketplace trust.
  - Content creator verification.
  - DAO governance (reputation-weighted voting).

### 4. Key recovery

- Web of trust can provide key recovery mechanisms.
- Social recovery through trusted contacts.
- No single point of failure.

### 5. Delegation

- NIP-26 style delegated signing.
- Allow trusted parties to act on your behalf.
- Time-limited, revocable permissions.

---

## Evidence at a glance

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

- Decentralized. No single point of trust failure.
- Permissionless. Anyone can participate.
- Transitive. Trust propagates through the network.
- Resilient. Network effects improve security.

### Limitations

- Cold start. New users have no trust connections.
- Sybil attacks. Attackers can create many identities to manipulate trust.
- Fragmentation. Isolated subgraphs may not connect.
- Complexity. User experience can be confusing.
- Key rotation. Trust can become stale.

### Attack vectors

| Attack | Description | Mitigation |
|--------|-------------|------------|
| **Sybil** | Create many fake identities | Proof of work, Proof of use |
| **Trust flooding** | Flood with signatures | Path length limits, thresholding |
| **Key poisoning** | Insert malicious keys | Key pinning, careful verification |
| **Centralization** | Trust concentrates | Monitor central nodes |

---

## Evidence at a glance

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

## Related files

- [Overview - Identity & Pseudonymity](/identity) — Pseudonymous identity and reputation
- [Overview - Decentralized Identity](/identity/overview-decentralized-identity) — Formal DID/VC stacks
- [Overview - Encrypted Messaging](/encrypted-messaging) — PGP usage in messaging, Nostr DMs
- [Overview - Confidential Computing](/confidential-computing) — Complementary trust mechanisms
- [Nostr Deep Dive](/encrypted-messaging/nostr-deep-dive) — Full Nostr protocol analysis

---

## Further reading

- [OpenPGP RFC 9580](https://datatracker.ietf.org/doc/html/rfc9580) — Updated standard
- [NIP-26 Specification](https://nips.nostr.com/26) — Delegation in Nostr
- [nostr-wot GitHub](https://github.com/nostr-wot) — Trust network tools
- [PGPainless WOT](https://github.com/pgpainless/pgpainless-wot) — Java implementation
- [Keyoxide Documentation](https://docs.keyoxide.org/) — Verification guides

