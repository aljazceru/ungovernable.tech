---
title: "IPFS and Filecoin"
slug: ipfs-and-filecoin
type: deep-dive
pillars: ["storage"]
readiness: battle-tested
description: "IPFS gives data a content address that anyone can serve; Filecoin pays providers to store it and prove they do. How the pair works and fails."
dek: "IPFS gives data a content address. Filecoin pays storage providers to keep content-addressed data available and prove they are storing it. Together they form the Protocol Labs storage stack: retrieval and naming on one side, durable storage deals on the other."
updated: 2026-10-25
created: 2026-04-28
origin: vault
source: "12-Decentralized-Storage/IPFS and Filecoin.md"
aliases: ["IPFS", "Filecoin"]
tags: ["ipfs", "filecoin", "decentralized-storage", "content-addressing", "cid", "deep-dive"]
---

## IPFS

IPFS is a peer-to-peer content-addressed data network. A file is chunked into blocks, each block is hashed, and the root becomes a **CID** (Content Identifier). If a client asks for a CID, any peer with the blocks can serve it. The client verifies the blocks by hash.

Key mechanics:

- **CIDs.** Self-certifying identifiers that include a multihash and codec information.
- **DAGs.** Files and directories are represented as Merkle DAGs.
- **Bitswap.** Block exchange protocol used by IPFS peers.
- **libp2p.** Networking stack for peer discovery, streams, and transports.
- **Gateways.** HTTP bridges that let browsers fetch IPFS content without running a local node.

IPFS solves integrity and distribution. It does not automatically solve persistence. Content stays available only while at least one reachable node pins or serves it.

## Filecoin

Filecoin is a storage market built around cryptographic storage proofs. Clients make deals with storage providers; providers commit data into sectors and periodically prove they still store it.

Core pieces:

- **Storage deals.** Client and provider agree on size, duration, price, and collateral.
- **Proof-of-Replication.** Provider proves a unique sealed copy of the data exists.
- **Proof-of-Spacetime.** Provider repeatedly proves storage over the deal duration.
- **Sectors.** Storage units sealed by providers and proven on-chain.
- **Retrieval markets.** Data retrieval can happen through separate retrieval paths and gateways.

Filecoin is not "IPFS with a token." IPFS retrieves content by CID. Filecoin creates economic guarantees that someone stores a piece over time.

## How They Compose

```
User data
  → chunk / encode
  → CID or PieceCID
  → pin locally / publish via IPFS
  → make Filecoin storage deals for persistence
  → publish CID through ENS, PKARR, website, Nostr, or signed metadata
```

For user-facing applications, the common stack is:

1. Put data in IPFS-compatible form.
2. Pin it on at least two pinning providers.
3. Store archival copies through Filecoin deals.
4. Publish the CID in a signed index or decentralized name.

## Use Cases

| Use case | Fit |
|----------|-----|
| Static websites / dapp frontends | Strong, if pinned |
| NFT metadata | Strong, with pinning and archival deal |
| Public datasets | Strong, with Filecoin deals |
| Private backups | Use only after client-side encryption |
| Low-latency app database | Poor fit; use a database and publish snapshots |

## Trade-offs

### Strengths

- Content hashes make tampering obvious.
- Gateway and provider choice reduce platform lock-in.
- Filecoin proofs make storage claims auditable.
- CIDs compose cleanly with decentralized names and smart contracts.

### Limitations

- IPFS availability depends on pinning.
- Public gateways leak request metadata and can censor.
- Filecoin deal UX remains more complex than ordinary cloud storage.
- Retrieval performance depends on provider behavior and caching.
- Plaintext data is public data unless encrypted first.

## Attack Surface

| Attack | Mitigation |
|--------|------------|
| Gateway serves wrong bytes | Verify CID in client |
| CID disappears from network | Pin on multiple nodes; add Filecoin deals |
| Provider stores but retrieval is slow | Separate hot cache from archival storage |
| DHT observation | Run local node over Tor or use privacy-aware gateway strategy |
| Malicious pinning provider | Multi-pin and audit availability |
| Plaintext leak | Encrypt before publishing |

## Primary sources

- [Benet: IPFS, Content Addressed, Versioned, P2P File System](https://arxiv.org/abs/1407.3561)
- [IPFS persistence and pinning](https://docs.ipfs.tech/how-to/pin-files/)
- [Filecoin storage proofs](https://docs.filecoin.io/basics/the-blockchain/proofs)
- [Trautwein et al.: Design and Evaluation of IPFS](https://arxiv.org/abs/2208.05877)
- [Filecoin protocol specification](https://spec.filecoin.io/intro/)

Continue with [IPNS and DNSLink](/kb/ipns-dnslink/) for naming, [BitTorrent for Archive Distribution](/kb/bittorrent-archives/) for another distribution model, and [Choosing Decentralized Storage](/kb/compare-storage/) for the retention and privacy comparison.
