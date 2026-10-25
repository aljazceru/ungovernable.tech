---
title: "Arweave"
slug: arweave
type: deep-dive
pillars: ["storage"]
readiness: usable
description: "Arweave, a permanent storage network funded by a one-time payment: how the blockweave and endowment work, and what permanence really guarantees."
dek: "A blockchain-style permanent storage network. Users pay once, data is written into Arweave's blockweave, and miners are incentivized to retain and serve historical data through a storage endowment model."
updated: 2026-04-28
created: 2026-04-28
origin: vault
source: "12-Decentralized-Storage/Arweave.md"
aliases: ["Permaweb"]
tags: ["arweave", "decentralized-storage", "archival-storage", "permaweb", "deep-dive"]
---

## What It Is

Arweave is designed for durable public storage rather than mutable cloud objects. Its social contract is "pay once, store for a very long time." The user submits a transaction containing data or a pointer to bundled data. The network stores it and makes it retrievable through gateways.

Important concepts:

- **Blockweave.** Arweave's chain-like data structure, where miners prove access to previous data.
- **Proof of Access / Succinct Proofs of Random Access.** Mining is tied to access to historical data.
- **Storage endowment.** Part of the upload payment is allocated to subsidize long-term storage.
- **Permaweb.** Web-like applications hosted on immutable Arweave data.
- **Bundlr / Irys-style bundling.** Batching layer used by many apps to reduce friction and improve throughput.

## Where It Fits

Arweave is strongest when immutability is a feature:

- Publications and public archives.
- NFT metadata and art.
- Legal or governance records.
- Software release artifacts.
- Static frontends and permaweb apps.
- Datasets that should outlive the original operator.

It is weaker for private, mutable, or deletion-sensitive content. Anything sensitive should be encrypted before upload, and even encrypted data should be treated as long-lived.

## Arweave vs IPFS/Filecoin

| Property | Arweave | IPFS | Filecoin |
|----------|---------|------|----------|
| Primary goal | Permanent archive | Content-addressed retrieval | Paid storage market |
| Payment model | Pay once | External pinning | Deals over time |
| Mutability | Immutable data; mutable pointers via layers | Mutable names via IPNS/DNSLink | Deals can renew or expire |
| Retrieval | Gateways and nodes | Peers and gateways | Providers, retrieval markets, gateways |
| Best for | Public artifacts | Distribution | Large retained datasets |

Arweave competes more with "permanent publication" than with S3. IPFS/Filecoin is more modular; Arweave is more opinionated.

## Trust Model

You trust:

- The Arweave economic model to keep storage incentives above storage costs.
- Gateways for convenience, unless the client verifies data against transaction IDs and hashes.
- Upload tooling and bundlers to correctly submit data.

You do not trust:

- A single hosting account.
- A domain registrar.
- A specific CDN.

The most important caveat is that public archival storage is intentionally hard to erase. That is a feature for censorship resistance and a liability for personal data.

## Trade-offs

### Strengths

- Strong fit for immutable public records.
- Simple mental model: pay once, retrieve through transaction ID or gateway.
- Broad adoption in NFT metadata, permaweb apps, and public web archives.
- Content persistence is part of the protocol's economic design.

### Limitations

- Mutable app state needs layers above Arweave.
- Private data requires client-side encryption and key custody.
- Gateway availability and indexing still matter for user experience.
- The storage endowment model depends on long-run economic assumptions.
- Deletion and legal compliance are structurally difficult.

## Attack Surface

| Attack | Mitigation |
|--------|------------|
| Gateway censorship | Use multiple gateways; verify transaction IDs |
| Bad upload path | Verify transaction inclusion and content hash |
| Plaintext disclosure | Encrypt locally before upload |
| Economic underfunding | Use Arweave for public archives with realistic risk tolerance; keep secondary copies |
| Mutable-pointer hijack | Sign manifests and use hardware-backed keys |

## Primary Sources

- Williams, *Arweave: A Protocol for Economically Sustainable Information Permanence*, 2018.
- Arweave Docs — [docs.arweave.org](https://docs.arweave.org/)
- Arweave Yellow Paper and protocol documentation.
- Trautwein et al., *Design and Evaluation of IPFS*, for comparison with content-addressed networks.

For alternatives and their operating obligations, see [Choosing Decentralized Storage](/kb/compare-storage/) and [BitTorrent for Archive Distribution](/kb/bittorrent-archives/).
