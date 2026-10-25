---
title: "Slashtags"
slug: slashtags
type: deep-dive
pillars: ["naming", "identity"]
readiness: historical
description: "Slashtags, Synonym's earlier protocol for key-rooted identity and peer-to-peer data sharing: what it attempted and why it was superseded by Pubky."
dek: "The original Synonym-dev protocol for key-rooted, peer-to-peer identity, hyperdrive-backed data sharing, and Slashtags-as-DNS-names. Slashtags is the predecessor and conceptual parent of Pubky Core and PKARR — the same engineering team, the same DHT and cryptographic identity pattern, but earlier, narrower in scope, and now formally superseded. Slashtags itself is best understood as a historical artifact that explains why Pubky Core looks the way it does. See PKARR for the modern production stack; Overview - Decentralized DNS for the comparative landscape."
updated: 2026-10-25
created: 2026-06-22
origin: vault
source: "03-Decentralized-DNS/Slashtags.md"
aliases: ["Slashtags Protocol", "Hyperdrive", "Hyperswarm", "Synonym Slashtags"]
tags: ["slashtags", "synonym", "pkarr", "hyperdrive", "hyperswarm", "identity", "deep-dive"]
---

## What Slashtags was

Slashtags (2019–2024) was a JavaScript implementation of a key-rooted P2P identity and data layer built on top of [Hyperdrives](https://github.com/holepunchto/hyperdrive) (personal append-only file drives) and [Hyperswarm](https://github.com/holepunchto/hyperswarm) (a Kademlia-based DHT with UDP holepunching). The same team (Synonym) later reworked the core idea into PKARR (signed DNS records on the Mainline DHT) and Pubky Core (a production protocol suite with SDKs, homeservers, mobile key custody, and a social graph). The current [Slashtags transition to Pubky Core](https://slashtags.to/) website now redirects to Pubky Core and states:

> "Slashtags is now Pubky Core, which provides infrastructure for decentralized identity management, data routing, and hosting."

So Slashtags as a standalone product is winding down. The historical value of studying it is the *design pattern*: the same architectural choices that Slashtags made in 2019 — BIP-39 mnemonics, Ed25519 keypair, hyperdrive-backed data, Hyperswarm for discovery — reappear in modern PKARR/Pubky in a more focused, less ambitious form.

## Architecture

### The Slashtag

A Slashtag is an Ed25519 keypair derived from a BIP-39 mnemonic seed (the same as a Bitcoin wallet's seed phrase). The user controls one Slashtag (one identity); within that Slashtag, the user can derive multiple hyperdrives by name (a "drive name" + the master key).

### Discovery

The discovery key is `blake2b(public_key)`. A Slashtag's discovery key is published into the Hyperswarm DHT, which is a Kademlia-like network with UDP holepunching. Peers interested in the Slashtag (e.g., contacts) listen on the discovery key, get connected to peers that have the data, and exchange.

This is conceptually similar to [PKARR](/kb/pkarr/) — both publish a public-key-derived identifier into a DHT and resolve it to peers — but the underlying DHT is Hyperswarm rather than the Mainline DHT, and the data model is hyperdrives (file drives) rather than signed DNS records.

### Hyperdrives

A hyperdrive is an append-only log of blocks, similar to a content-addressed log. Slashtags uses hyperdrives for:

- **Profile data**: name, avatar, contact info, payment preferences.
- **Public / private feeds**: social media style.
- **Contacts lists**: who the user has added.
- **Account metadata**: per-service data for Slashtag-enabled services.

The hyperdrive is signed: only the Slashtag's private key can add a new block. Other peers need the drive’s public key to open and verify it. A discovery key identifies the swarm but does not by itself grant read access. Sharing means handing over the public key (or its URI form).

### Access control

| Action | Who can do it |
|--------|---------------|
| Add a block to a drive | Only the Slashtag's private key holder |
| Read a drive | Anyone with the public key, subject to any application encryption |
| Seed a drive | A replicating peer with the drive key and data |
| Discover / find the drive | Any Hyperswarm peer via the DHT |

This is a simple read-public / write-private model. Public writes mean the Slashtag operator's signature is required for any update; any peer can mirror and distribute.

### Data integrity

Each block added to a hyperdrive is committed via a Merkle root. The Slashtag owner signs the root; the signature is verified before the block is added. This is the same Merkle-anchored commit pattern that hyperdrives use in their own protocol, and it ensures that a drive's content history is consistent and tamper-evident.

## The historical progression: Slashtags → PKARR → Pubky Core

| Layer | Slashtags (2019–2024) | PKARR (2023–) | Pubky Core (2025–) |
|-------|------------------------|---------------|---------------------|
| Identity | Ed25519 from BIP-39 | Ed25519 | Ed25519 |
| DHT | Hyperswarm (UDP holepunch) | Mainline DHT (BEP 44) | Mainline DHT |
| Data model | Hyperdrive (file log) | Signed DNS records | Signed DNS records + homeserver key-value data |
| Resolution | Hyperswarm discovery | `pkdns` / pkdns bridge | `pkdns` + Pubky homeserver + Pubky Nexus |
| SDKs | JavaScript only | Rust, JavaScript | Rust, JS, Swift, Kotlin |
| Application | Bitkit wallet profiles | Pubky homeserver | Pubky Core suite, Pubky.app, Pubky Ring, Pubky Nexus |
| Active status (2026) | Historical, superseded | Production | Production |

The conceptual through-line is unbroken: **key-rooted identity, signed data, DHT discovery, no registrar, no chain, no fees**. What changed between Slashtags and Pubky Core was the choice of DHT (Hyperswarm → Mainline), the data model (hyperdrive → signed DNS records + homeserver KV), and the platform support (JS only → multi-language SDKs + mobile + social app + indexing).

## Why the Slashtags design is still worth studying

1. **BIP-39 mnemonics as identity seed.** A Slashtag's key is derived from the same 12/24-word seed a Bitcoin wallet uses. The user has one mnemonic, multiple Slashtags (different keypairs derived from different BIP-39 derivation paths). This is the same pattern FROST and threshold-custody schemes often use.
2. **Hyperdrives as a content model.** Append-only logs with Merkle-anchored commits are exactly the structure that social applications need (immutable history, signed by the user, replicated by peers).
3. **Read-public / write-private.** Slashtags made this default; the same idea persists in Nostr (events are public, signed by the user) and PKARR (records are public, signed by the key).
4. **No chain, no token, no registrar.** A consistent philosophy across all three generations.

## Slashtags in production: Bitkit

The primary production use of Slashtags was the **Bitkit** wallet (formerly Synonym's P2P Bitcoin wallet). Bitkit used Slashtags to power:

- User profile (avatar, display name, contact info).
- Contacts list (P2P, no central server).
- Payment preferences (Lightning address book).
- Authentication (signed in to Slashtags-aware services with the wallet key).
- Private / public feeds (encrypted to contacts).

With the move to Pubky Core, Bitkit is one of the early wallets that will integrate PKARR-based discovery. The conceptual compatibility makes the migration straightforward.

## What was harder about Slashtags

1. **Limited language support.** JavaScript only at the protocol layer. Rust SDKs came later via PKARR, and even later for full Pubky Core (Rust / JS / Swift / Kotlin).
2. **Hyperswarm DHT scale.** Hyperswarm is excellent for small-to-medium-scale P2P apps but not as ambient as the Mainline DHT (which has ~10M nodes and 15+ years of uptime).
3. **Hyperdrive storage overhead.** A hyperdrive is heavier than a signed DNS record; mobile devices and low-resource peers struggled to maintain full hyperdrive replicas.
4. **DHT reachability in hostile networks.** Both Hyperswarm discovery and the BitTorrent Mainline DHT use UDP. UDP restrictions can affect either network.

These four issues are the technical reasons for the move to Mainline DHT + signed DNS records in PKARR. The lessons carried forward; the engineering substrate changed.

## Trade-offs (historical snapshot)

### Strengths of Slashtags

- Single mnemonic, multiple Slashtags — clean key-derivation story.
- Hyperdrives gave a familiar file-system-like mental model.
- No chain, no token, no fees.
- Read-public / write-private was a natural privacy model for social apps.
- DHT discovery worked without any server-side infrastructure.

### Limitations of Slashtags (relative to modern Pubky Core)

- JS-only SDKs; no first-party mobile or Rust.
- Hyperswarm DHT is less ambient than Mainline.
- Hyperdrives are heavy for mobile and small devices.
- No production homeserver; data lived in P2P networks.
- Limited tooling for indexing / social-graph queries.

## Use cases (then and now)

| Use case | Slashtags era | Today |
|---------|----------------|-------|
| Wallet profile | Bitkit | Bitkit on Pubky |
| Contact list | Bitkit, Slashtags auth demo | Pubky + Nostr cross-signed contacts |
| Service discovery | Slashtags auth demo | PKARR + pkdns |
| Social feed | Bitkit public/private feeds | Pubky.app social PWA |
| NIP-05 alias | N/A at the time | PKARR-backed NIP-05 |
| Censorship-resistant website | Custom hyperdrive hosting | PKARR + Pubky homeserver |

## Evidence at a glance

| Item | Evidence | What it supports |
|------|----------|------------------|
| [Slashtags implementation](https://github.com/synonymdev/slashtags) repo | 568 commits; beta status; documentation still in progress; npm package `@synonymdev/slashtag` | Real implementation, but explicitly beta and now superseded |
| [Slashtags transition to Pubky Core](https://slashtags.to/) website | "Slashtags is now Pubky Core" | Official redirection to Pubky Core |
| `synonymdev/slashtags-widget-price-feed`, `…news-feed`, `…bitcoin-feed` | Public Slashtags widget examples | Public data publishing pattern that Slashtags pioneered |
| Bitkit wallet integration | Slashtags powers Bitkit profile, contacts, payments | First and longest-running Slashtag production deployment |
| BIP-39 key derivation | `specs/slashtags-derivation.md` in the Slashtags repo | Standard mnemonic-based identity |
| Hyperswarm DHT | [Hyperswarm implementation](https://github.com/holepunchto/hyperswarm) | Underlying discovery network |
| Hyperdrive file drives | [Hyperdrive implementation](https://github.com/holepunchto/hyperdrive) | Underlying data model |

## Recent developments (2023–2026)

- **Slashtags → Pubky Core transition (2024–2025)**: Synonym formally redirected Slashtags branding to Pubky Core. The Slashtags npm packages still exist for backwards compatibility, but new work is on Pubky.
- **Bitkit wallet integration with Pubky Core (2025)**: Bitkit is one of the early wallets building PKARR-backed identity.
- **Community history in PKARR/Pubky docs**: Slashtags is cited as the conceptual predecessor in PKARR's design notes.

## Primary sources

- [Pubky Core: current project](https://pubky.org/)
- [Slashtags implementation](https://github.com/synonymdev/slashtags)
- [Slashtag package source](https://github.com/synonymdev/slashtags/tree/master/packages/slashtag)
- [Slashtags key derivation specification](https://github.com/synonymdev/slashtags/blob/master/specs/slashtags-derivation.md)
- [Bitkit source](https://github.com/synonymdev/bitkit)
- [Slashtags authentication example](https://github.com/synonymdev/slashtags-auth-demo)
- [Hyperswarm implementation](https://github.com/holepunchto/hyperswarm)
- [Hyperdrive implementation](https://github.com/holepunchto/hyperdrive)
- [Maymounkov and Mazières: Kademlia](https://pdos.csail.mit.edu/~petar/papers/maymounkov-kademlia-lncs.pdf)
- [BEP 5: BitTorrent DHT over UDP](https://www.bittorrent.org/beps/bep_0005.html)
- [Slashtags transition to Pubky Core](https://slashtags.to/)
