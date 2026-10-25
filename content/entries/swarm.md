---
title: "Swarm"
slug: swarm
type: deep-dive
pillars: ["storage"]
readiness: usable
description: "Swarm, Ethereum's content-addressed storage and messaging network with postage-stamp incentives and the Bee client: design and status."
dek: "Ethereum's storage-and-communication sibling: a content-addressed chunk network with incentives, postage batches, and the Bee client. It targets dapp assets, web hosting, and Ethereum-adjacent data availability rather than generic cloud backup."
updated: 2026-10-25
created: 2026-04-28
origin: vault
source: "12-Decentralized-Storage/Swarm.md"
aliases: ["Ethereum Swarm", "Bee"]
tags: ["swarm", "ethereum", "decentralized-storage", "postage-batches", "deep-dive"]
---

## What It Is

Swarm stores data as chunks addressed by cryptographic hashes. A user uploads content through a Bee node, pays with **postage batches**, and the network distributes chunks to nodes whose overlay addresses are close to the chunk address.

Core concepts:

- **Chunks.** Fixed-size pieces addressed by hash.
- **Manifests.** Directory-like structures mapping paths to chunks.
- **Postage batches.** Prepaid stamps attached to chunks to signal storage payment.
- **Bee.** Reference Swarm node implementation.
- **Neighborhoods.** Overlay routing and storage based on proximity order.

Swarm's conceptual home is Ethereum's decentralized web stack: smart contracts on Ethereum, names through ENS, storage through Swarm, and wallets for identity/payment.

## How It Works

```
file / directory
  → chunk into Swarm data chunks
  → build manifest
  → attach postage stamps
  → upload via Bee
  → retrieve by content hash or manifest path
```

The content hash gives integrity. The postage system gives the network a way to price storage. Retrieval can be done through local Bee nodes or gateways.

## Swarm vs IPFS

| Property | Swarm | IPFS |
|----------|-------|------|
| Origin | Ethereum ecosystem | Protocol Labs |
| Addressing | Content hash | CID / multihash |
| Incentives | Built-in postage/stamps | External pinning or Filecoin |
| Client | Bee | Kubo, Helia, many clients |
| Best fit | Ethereum dapp assets | Broad content-addressed distribution |
| Ecosystem size | Smaller | Larger |

Swarm is more opinionated and Ethereum-native. IPFS has broader ecosystem gravity and more tooling.

## Use Cases

- Static dapp frontends paired with ENS.
- Public assets for Ethereum applications.
- Signed manifests for web apps.
- Data blobs that should be content-addressed and paid for at upload time.

For large archival datasets, compare with [IPFS and Filecoin](/kb/ipfs-and-filecoin/) and [Arweave](/kb/arweave/). For private backups, compare with [Sia and Storj](/kb/sia-and-storj/).

## Trade-offs

### Strengths

- Content addressing and manifest model are natural for dapp frontends.
- Ethereum-native payment and naming integrations.
- Postage model ties storage to explicit payment.
- Bee gives a self-hostable node path.

### Limitations

- Smaller network and ecosystem than IPFS.
- Public data needs local encryption for privacy.
- Gateway UX can hide the trust model from casual users.
- Dapp developers often choose IPFS/Arweave because tooling is broader.

## Attack Surface

| Attack | Mitigation |
|--------|------------|
| Gateway censorship | Use local Bee node or multiple gateways |
| Chunk loss | Monitor availability and re-upload/stamp as needed |
| Manifest hijack | Sign manifests or anchor roots in ENS / smart contracts |
| Plaintext exposure | Encrypt before upload |
| Economic underpayment | Use adequate postage and monitor retention |

## Primary sources

- [Bee client](https://github.com/ethersphere/bee)
- [Swarm whitepaper](https://www.ethswarm.org/swarm-whitepaper.pdf)
- [Swarm documentation](https://docs.ethswarm.org/)
- [Swarm: postage stamps](https://docs.ethswarm.org/docs/desktop/postage-stamps)
