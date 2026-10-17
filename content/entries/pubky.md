---
title: "Pubky"
slug: pubky
type: deep-dive
pillars: ["identity", "naming"]
readiness: experimental
description: "Pubky, an open protocol for key-based identity and data built on PKARR and the Mainline DHT: homeservers, the social app and its status."
dek: "An open protocol and identity platform built around PKARR (Public-Key-Addressable Resource Records) over the BitTorrent Mainline DHT. Pubky Core is the production-grade suite from Synonym that adds SDKs, homeservers, a semantic social graph, mobile key management, and indexing infrastructure. The result is a censorship-resistant, fee-free, key-rooted identity and data platform. See PKARR for the underlying naming primitive."
updated: 2026-05-11
created: 2026-04-25
origin: vault
source: "11-Identity/Pubky.md"
aliases: ["Pubky Core", "Pubky Network", "PKARR"]
tags: ["pubky", "pkarr", "identity", "dht", "mainline", "deep-dive"]
---

## What Pubky Core is

Pubky Core is the full-stack realization of the PKARR primitive. Rather than stopping at signed DNS records on a DHT, Pubky Core provides:

- **Pubky Core protocol** — formal specification for key-based authentication, capability tokens, key-value storage semantics, and homeserver discovery.
- **Pubky Homeserver** — production-ready server hosting per-user key-value data over a RESTful HTTP API, with multiple persistence backends.
- **Pubky Core SDK** — client libraries in Rust, JavaScript/WASM, Swift (iOS/macOS), and Kotlin (Android).
- **Pubky Ring** — mobile key manager app (iOS/Android) for managing pubkys, authorizing apps, and controlling sessions.
- **Pubky.app** — a live social media PWA built on the protocol.
- **Pubky Nexus** — production indexing service for social features and API.
- **pkdns** — DNS resolver bridging PKARR into legacy DNS.

The guiding philosophy: *"The Web, long centralized, must decentralize; Long decentralized, must centralize."* Pubky Core targets the practical middle ground between fully centralized web2 and purely theoretical decentralized systems.

## Architecture

### Three-layer stack

```
Identity layer:
  Ed25519 keypair → public key as zone identifier
  └─ PKARR: DHT[hash(pk)] = signed DNS records

Data plane layer:
  Pubky Homeserver: RESTful HTTP API over HTTPS
  └─ Key-value store per public key
  └─ Publishes homeserver location in PKARR record

Application layer:
  Pubky Core SDK → apps (social, identity, etc.)
  Pubky Nexus → indexing and social graph
  Pubky Ring → mobile key management
```

### Homeserver architecture

The homeserver is the core data plane. Each user has a homeserver (self-hosted or hosted) that stores signed key-value records. The address is discovered via PKARR.

Properties:
- Multiple persistence backends: Files, LMDB, SQL (SQLite, PostgreSQL).
- RESTful HTTP API over HTTPS — works with existing web infrastructure.
- Pub/sub event streams for real-time features.
- Rate limiting (DDoS protection), Prometheus metrics, admin API.
- Session management with secure, time-limited sessions.
- Recovery files for encrypted backup and key recovery.

### SDK availability

| Language | Package | Notes |
|----------|--------|-------|
| Rust | `pubky` on crates.io | Full-featured native SDK |
| JavaScript/WASM | `@synonymdev/pubky` on npm | Browser and Node.js |
| Swift | `pubky-swift` | iOS/macOS native |
| Kotlin | `pubky-kotlin` | Android native |

The JavaScript SDK supports both browser and Node.js environments, enabling web app development without native dependencies.

### Pubky Ring — mobile key manager

[github.com/pubky/pubky-ring](https://github.com/pubky/pubky-ring) is the mobile companion app:

- Manages pubky keys on iOS and Android.
- Authorizes applications with scoped capability tokens.
- Controls active sessions.
- Signs and verifies data with the stored key.

This separates key custody from application access — the Ring holds the key, apps request authorization through it.

### Pubky Nexus — indexing and social graph

[github.com/pubky/pubky-nexus](https://github.com/pubky/pubky-nexus) is the production indexing service:

- Staging API: `https://nexus.staging.pubky.app/swagger-ui/`
- Production API: `https://nexus.pubky.app/swagger-ui/`
- Provides social graph features (follows, blocks, semantic relationships) that require cross-user aggregation.
- Enables search and discovery across the Pubky social ecosystem.

## Semantic social graph

The distinguishing application-layer feature. Tagged relationships enable:

- **User-controlled filtering** — each user tags their relationships (friend, colleague, community) and filters content accordingly.
- **Discovery and matching** — tagged graphs support algorithmic matching without centralized profiling.
- **Coordination** — community organization through structured relationship metadata.
- **Privacy-preserving** — the graph lives in user-controlled homeservers; Nexus aggregates only what users explicitly share.

The semantic social graph is distinct from both Nostr's flat relay event model and ActivityPub's server-federation model: each user owns structured, tagged relationship data that can be selectively shared or aggregated.

## Operational patterns

### Self-hosted personal stack

```
1. Generate Ed25519 keypair → Pubky identity (zone key)
2. Run pkdns locally or use a community resolver
3. Publish PKARR record with homeserver pointer (TXT record)
4. Run Pubky Homeserver (Docker, ~one-VM workload)
5. Use Pubky.app social PWA or SDK-based client
6. Manage keys with Pubky Ring mobile app
```

The equivalent of self-hosting an online presence without DNS, a domain, or a platform.

### NIP-05 over PKARR (for Nostr users)

For Nostr users who want a censorship-resistant NIP-05 alias:

```
PKARR record → points homeserver URL
homeserver → serves /.well-known/nostr.json
nostr.json → maps username → npub
```

An adversary can attack the homeserver host but cannot compel ICANN, a registrar, or a DNS provider.

### Combined Nostr + Pubky stack

Hold both keys and bind them via cross-signed records. Use Nostr for real-time social and Pubky for structured content (long-form posts, profile, file storage, follow lists).

## Pubky vs Nostr at the identity layer

Both are key-rooted identity systems. They differ:

| Dimension | [Nostr](/kb/nostr-identity/) | Pubky |
|-----------|-----------|-------|
| Identity | secp256k1 / Schnorr (`npub`) | Ed25519 (PKARR key) |
| Discovery / addressing | Relays + NIP-05 | Mainline DHT (PKARR) |
| Data model | Append-only signed events to relays | Key-value signed records on homeserver |
| Naming | NIP-05 alias | PKARR + optional NIP-05 |
| Social graph | Relay-scoped event streams | Semantic social graph with user-controlled tagging |
| SDK support | Multiple (ndk, swift-nostr, etc.) | Rust / JS / Swift / Kotlin (first-party) |
| Mobile key manager | Third-party | Pubky Ring (first-party) |
| Censorship resistance | Per-relay; multi-relay redundancy | Per-homeserver + DHT |
| Latency | Real-time event stream | HTTP fetch + DHT resolve |
| Ecosystem maturity | Larger (2024-2026) | Smaller, growing |

The systems are more complementary than competing. Many users hold both keys or use cross-signing to bind them.

## Threat model

### Defends against

- **Record forgery** — signatures bind records to the zone key.
- **Replay** — sequence numbers and BEP 44 semantics order updates.
- **Registrar coercion** — there is no registrar.
- **TLD seizure** — there is no TLD.
- **Platform deplatforming** — homeservers are user-controlled or freely chosen.
- **CA compromise** — TLS is used but not required for PKARR resolution itself.

### Does not defend against

- **DHT record-hiding** — an adversary near a key's hash can refuse to serve it. Mitigations: republish to multiple bootstrap nodes, pin via known peers.
- **Lookup observation** — DHT queries leak the key hash to intermediate nodes. Use Tor for private lookups.
- **Key compromise** — lose the key, lose the zone. Threshold custody (FROST) is the mitigation.
- **Quantum attack** — Ed25519 is not post-quantum. No PQ migration path specified yet.
- **Homeserver availability** — the homeserver host can go down. Multi-homing and backup are the mitigations.

## Trade-offs

### Strengths

- No blockchain, no token, no fees. Just cryptography and an ambient DHT (~10M nodes, 15+ years proven).
- Self-authenticating names — the address proves the key.
- Bridges into legacy DNS via pkdns.
- No takedown vector at the naming layer.
- Production SDKs (four languages), homeserver, social app, mobile key manager, and indexing service — a coherent full stack rather than a fragmented ecosystem.
- Semantic social graph provides structure that Nostr's relay model lacks.
- Pubky Ring provides first-party key management for mobile.
- "Credible exit": switch homeservers/apps/identity managers without losing data or social graph.

### Limitations

- DHT availability is an assumption. Mainline is ambient but adversarial scenarios are less studied than Tor or I2P.
- Records are small; non-trivial data lives on the homeserver, not in PKARR.
- Homeserver hosting is an operational burden for non-technical users.
- Public homeservers re-introduce some centralization.
- Quantum vulnerability: Ed25519-based, no deployed PQ migration path.

## Recent developments (2024–2026)

- `pkdns` reached stable production with Linux and Docker deployments (2024–2025).
- Pubky homeserver reference implementation matured (2025).
- Pubky.app social launched in 2025.
- **Pubky Core SDK suite launched (2025–2026)** — Rust, JavaScript/WASM, Swift, Kotlin SDKs released with comprehensive documentation.
- **Pubky Ring mobile key manager** — iOS/Android app released for key custody and session management.
- **Pubky Nexus** — production indexing API launched (staging + production endpoints).
- **Iroh integration explored (2026)** — Pubky Dev Community Call #2 examined integrating Iroh (a modern Rust P2P library) with PKARR for improved relay/transport reliability.
- Semantic social graph tooling and API stabilized (2025–2026).
- Community bridges with Nostr (NIP-05 over PKARR) continue to develop.
- No PQ-signature variant standardized yet.

## Primary sources

### Documentation and specs
- Pubky docs — [docs.pubky.org](https://docs.pubky.org)
- Pubky Core overview — [docs.pubky.org/Explore/PubkyCore/Introduction](https://docs.pubky.org/Explore/PubkyCore/Introduction)
- Pubky API reference — [docs.pubky.org/Explore/PubkyCore/API](https://docs.pubky.org/Explore/PubkyCore/API)
- Pubky security model — [docs.pubky.org/Explore/PubkyCore/SecurityModel](https://docs.pubky.org/Explore/PubkyCore/SecurityModel)

### Repositories
- [pubky/pubky-core](https://github.com/pubky/pubky-core) — SDKs, homeserver, protocol specs (MIT)
- [pubky/pkarr](https://github.com/pubky/pkarr) — the PKARR protocol library
- [pubky/pkdns](https://github.com/pubky/pkdns) — DNS resolver bridging PKARR
- [pubky/pubky-ring](https://github.com/pubky/pubky-ring) — mobile key manager (iOS/Android)
- [pubky/pubky-nexus](https://github.com/pubky/pubky-nexus) — social graph indexing API
- [pubky/pubky-app](https://github.com/pubky/pubky-app) — Pubky.app social PWA
- [pubky/pubky-homeserver](https://github.com/pubky/pubky) — homeserver reference implementation

### Research and background
- Aiello, Hartshorn et al., *PKARR — Public-Key-Addressable Resource Records*, 2023.
- Maymounkov & Mazières, *Kademlia: A Peer-to-Peer Information System Based on the XOR Metric*, IPTPS 2002.
- BEP 44 — *Storing arbitrary data in the DHT* (BitTorrent Enhancement Proposal).
