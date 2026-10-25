---
title: "Decentralized Storage"
slug: decentralized-storage
type: explainer
pillars: ["storage"]
description: "Storage that survives platform failure, account seizure and takedowns: IPFS, Filecoin, Arweave, Sia, Storj, Swarm and Blossom compared by guarantees."
dek: "Storage that survives platform failure, account seizure, domain takedown, and cloud-provider policy changes by making data independently addressable, replicated, paid for, or mirrored across operators."
updated: 2026-04-28
created: 2026-04-28
origin: vault
source: "12-Decentralized-Storage/Overview - Decentralized Storage.md"
aliases: ["Decentralized Storage"]
tags: ["decentralized-storage", "ipfs", "filecoin", "arweave", "sia", "storj", "swarm", "blossom", "overview"]
---

## The Core Distinction

Decentralized storage is not one thing. Systems in this space answer different questions:

| Question | Primitive | Example |
|----------|-----------|---------|
| How do I know this is the exact file? | Content addressing | IPFS CID, Blossom SHA-256 |
| Who keeps a copy online? | Pinning or storage deal | IPFS pinning, Filecoin deal |
| Who pays for persistence? | Market or endowment | Filecoin, Sia, Storj, Arweave |
| How do apps find it? | Gateway, name, or server list | ENS, PKARR, Blossom kind 10063 |
| Is the content private? | Client-side encryption | Sia renter encryption, age before upload |

The most common mistake is treating **content addressing** as **availability**. An IPFS CID proves integrity, but if nobody pins the blocks, retrieval fails. A Blossom URL contains a SHA-256 hash, but if no server keeps the blob, the hash only proves what disappeared.

## Families

### Content-addressed retrieval

IPFS gives files content identifiers (CIDs), splits them into blocks, and retrieves them from peers over libp2p. It is excellent for integrity and distribution. Persistence is external: run your own node, use a pinning service, or pair IPFS with Filecoin.

### Storage markets with proofs

Filecoin and Sia pay storage providers to keep user data. Filecoin adds Proof-of-Replication and Proof-of-Spacetime to prove storage over time. Sia uses file contracts and renter-side erasure coding. These systems are closer to cloud storage markets than to social-media media hosting.

### Permanent public archives

Arweave uses a pay-once model backed by an endowment and proof-of-access-style mining. It is a fit for public artifacts intended to remain immutable: publications, NFT metadata, source snapshots, legal records, and web archives.

### Encrypted object storage

Storj behaves like S3-compatible object storage where data is encrypted client-side, split, erasure-coded, and distributed across independent storage nodes. It gives less ideological purity than a fully trust-minimized protocol, but better operational ergonomics for backups and applications.

### Application media layer

Blossom is Nostr's pragmatic blob layer: HTTP servers store SHA-256-addressed blobs, users authenticate with Nostr keys, and clients discover a user's preferred servers via a replaceable Nostr event. It is not a global storage blockchain; it is a portable media-server protocol.

## Comparison

| System | Addressing | Persistence model | Privacy default | Best fit |
|--------|------------|-------------------|-----------------|----------|
| IPFS | CID | Pinning / replication | Public unless encrypted | Distribution and verifiable links |
| Filecoin | PieceCID / deal | Paid storage deals + proofs | Public unless encrypted | Large datasets, verifiable retention |
| Arweave | Transaction ID | Pay-once archival endowment | Public unless encrypted | Immutable public archives |
| Sia | Contracted shards | Renter contracts | Client-side encryption | Low-cost backup/object storage |
| Storj | Object keys | Commercial node network | Client-side encryption | S3-like app storage |
| Swarm | Content hash | Postage batches + incentives | Public unless encrypted | Ethereum dapp assets |
| Blossom | SHA-256 | User/server policy + mirroring | Public unless encrypted | Nostr media and file portability |

## Threat Model

### What these systems improve

- **Integrity.** Content hashes make substitution obvious.
- **Provider independence.** Data can move across gateways, mirrors, nodes, or storage providers.
- **Censorship resistance.** Takedown requires suppressing every meaningful replica, not one account.
- **Longevity.** Paid contracts or archival models make persistence explicit.

### What they do not solve alone

- **Confidentiality.** Public storage should be treated as public. Encrypt sensitive data before upload.
- **Discovery.** A content hash is not a human name. Pair with [Overview - Decentralized DNS](/kb/decentralized-dns/), [PKARR](/kb/pkarr/), ENS, or a signed index.
- **Deletion.** Durable public storage and deletion rights are in tension.
- **Endpoint compromise.** If the user's device leaks keys or plaintext, storage decentralization does not help.
- **Gateway trust.** HTTP gateways can censor or log requests. Verify content hashes client-side and use multiple gateways for availability.

## Operational Patterns

### Public artifact

Use Arweave for immutable archival copy, IPFS for broad distribution, and publish both identifiers through ENS, PKARR, or a signed website.

### Private backup

Encrypt locally with [age Toolchain](/kb/age-encryption/), then store copies across Sia/Storj plus an ordinary cloud account. Decentralization is the availability layer; encryption is the privacy layer.

### Nostr media

Upload media to Blossom servers listed in the author's kind `10063` server list. Include the SHA-256-addressed URL or NIP-94 metadata in posts. Mirror popular files across several servers.

### dapp frontend

Build static assets, publish to IPFS and Arweave, pin on multiple providers, and put the root CID / transaction ID behind ENS or another resilient name.

## Attack Surface

| Attack | Affected systems | Mitigation |
|--------|------------------|------------|
| Content substitution | Gateway-based retrieval | Verify CID / SHA-256 locally |
| Data unavailability | IPFS, Blossom, unpaid mirrors | Pin, mirror, or pay for storage contracts |
| Provider collusion | Storage markets | Erasure coding, multiple providers, audits |
| Traffic analysis | Public gateways and DHTs | Tor, private gateways, local nodes |
| Plaintext exposure | All public storage | Encrypt before upload |
| Legal takedown | Gateways and hosted servers | Multi-jurisdiction replication, content-addressed mirrors |
| Key loss | Encrypted storage | Hardware-backed key custody and recovery plan |

## Primary Sources

- Benet, *IPFS - Content Addressed, Versioned, P2P File System*, arXiv 2014.
- Protocol Labs, *Filecoin: A Decentralized Storage Network*, 2017.
- Williams, *Arweave: A Protocol for Economically Sustainable Information Permanence*, 2018.
- Vorick and Champine, *Sia: Simple Decentralized Storage*, 2014.
- Storj Labs, *Storj: A Decentralized Cloud Storage Network Framework*, 2018.
- Trón et al., *Swarm: Storage and Communication Infrastructure for a Self-Sovereign Digital Society*, Ethereum Foundation.
- Blossom BUD specifications — [github.com/hzrd149/blossom](https://github.com/hzrd149/blossom).

For a practical selection table, see [Choosing Decentralized Storage](/kb/compare-storage/). Continue with [Syncthing](/kb/syncthing/), [Tahoe-LAFS](/kb/tahoe-lafs/), [Local-first Software and CRDTs](/kb/local-first-crdts/), [BitTorrent for Archive Distribution](/kb/bittorrent-archives/), [IPNS and DNSLink](/kb/ipns-dnslink/), [Hypercore and Hyperdrive](/kb/hypercore/) and [Kiwix](/kb/kiwix/). For a worked setup, follow [Private File Sync and Backup](/guides/private-file-sync-and-backup/). For replicated code and collaboration records, see [Radicle](/kb/radicle/).
