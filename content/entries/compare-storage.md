---
title: "Choosing Decentralized Storage"
slug: compare-storage
type: comparison
pillars: [storage]
readiness: usable
description: "Compare IPFS, Filecoin, Arweave, Tahoe-LAFS, Syncthing, BitTorrent, Hypercore and Blossom by retention, privacy, updates and operating obligations."
dek: "Choose who keeps the bytes, who can read them and how you recover them before choosing a protocol."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [decentralized-storage, ipfs-and-filecoin, arweave, blossom, tahoe-lafs, syncthing, bittorrent-archives, hypercore, private-file-sync-and-backup]
tags: [storage, comparison, durability, backup]
---

## Summary

Content addressing answers whether retrieved bytes match an identifier. Replication, storage agreements and active operators determine whether those bytes remain retrievable. Encryption determines who can read them. These are separate questions, and the systems below combine them differently.

The comparison covers each base system. Applications and hosting services may add encryption, retention policies or payment arrangements. Costs describe what must be funded, not a price quote. The censorship column is an assessment of the failure points implied by each design, not a measured score or a promise of immunity.

## Comparison

| System | Durability guarantee or condition | Who must stay online for retrieval? | Encryption | Mutability | Censorship resistance and dependencies | Cost model |
|---|---|---|---|---|---|---|
| [IPFS](/kb/ipfs-and-filecoin/) | A CID does not guarantee retention; pin the blocks on retained replicas. | A reachable holder of the required blocks. | Transport encryption; encrypt private content separately. | Changing content changes its CID; [IPNS or DNSLink](/kb/ipns-dnslink/) can update a pointer. | Replicas can serve the same CID; gateways and reachable holders remain blocking points. | Your storage and bandwidth, or a pinning service's terms. |
| [Filecoin](/kb/ipfs-and-filecoin/) | Storage agreements backed by proofs and economic penalties, for an agreed duration. | Storage providers and a working retrieval path. | Encrypt sensitive data before handing it to a provider. | Store changed content as new data and arrange its storage. | Several chosen providers can reduce dependence on one; providers still decide which deals to accept. | Negotiated storage terms; account for retrieval arrangements too. |
| [Arweave](/kb/arweave/) | An endowment-funded permanence design that depends on continued network incentives and operation. | Network nodes holding data and a reachable serving path. | Treat publication as public; encrypt sensitive material beforehand. | Published data is archival; publish new data for an update. | Replication reduces dependence on one host; access still needs functioning network and serving infrastructure. | Upfront upload fee and storage-endowment contribution. |
| [Tahoe-LAFS](/kb/tahoe-lafs/) | Recoverable while at least *k* distinct valid shares survive out of *N*; repair lost redundancy. | Servers holding enough shares, plus the reader's trusted client. | Client encrypts before distributing shares. | Immutable files and mutable files or directories with appropriate capabilities. | Distributed shares tolerate some server loss; enough withholding servers can deny retrieval. | Grid storage, bandwidth and administration; any hosting agreement is separate. |
| [Syncthing](/kb/syncthing/) | Replicas while devices retain files; edits and deletions propagate. | Devices exchanging data must overlap in connectivity, possibly through another retaining device. | TLS; trusted peers hold readable data. Untrusted encrypted storage is beta. | Live folder synchronization. | No required central file host; approved peers and their connectivity remain necessary. | Devices, disks, connectivity and any rented host. |
| [BitTorrent](/kb/bittorrent-archives/) | Available while reachable seeds or peers collectively retain all pieces, or web seeds supply them. | Enough peers or web seeds to supply the requested data. | Encrypt confidential archives before making the torrent; peers see addresses. | A torrent identifies a fixed snapshot. | DHT can remove tracker dependence; missing pieces and blocked peers still stop retrieval. | Seeding bandwidth and storage; any web-seed hosting. |
| [Hypercore / Hyperdrive](/kb/hypercore/) | Operators must retain the needed blocks; sparse replicas may not hold everything. | Peers with requested blocks; a writer must publish new updates. | Noise connections in Hyperswarm; content encryption is an application choice. | Logs and versioned files; the API also permits truncation and forks. | Replication permits several sources; availability depends on retained blocks and reachable peers. | Peer storage, bandwidth and application operation. |
| [Blossom](/kb/blossom/) | Server policy and explicit copies; mirroring is an optional endpoint. | A server retaining the requested blob. | Publicly accessible blobs; encrypt content before upload when needed. | A changed blob gets a different SHA-256 hash. | Re-uploading identical bytes preserves the hash; each server can reject storage or mirroring. | Server terms, including possible upload or mirroring payment. |

## How to choose

- **Working files across your devices:** start with [Syncthing](/kb/syncthing/) and a separate archive. Follow [Private File Sync and Backup](/guides/private-file-sync-and-backup/).
- **Encrypted storage across operators:** assess [Tahoe-LAFS](/kb/tahoe-lafs/), including share placement, capability recovery and repair.
- **Public snapshot distribution:** compare IPFS pins and BitTorrent seeding. Arrange who keeps copies after initial interest fades.
- **Paid retention or permanent publication:** inspect Filecoin's storage and retrieval obligations or Arweave's permanence model. Keep another copy rather than assuming economic incentives remove every failure mode.
- **Application data or media:** compare Hypercore's replicated data APIs, [local-first CRDTs](/kb/local-first-crdts/) for collaborative state, and Blossom's blob-server interfaces.

## Trust model / threat model

Separate loss of a provider from loss of a decryption key, compromised publishing authority, blocked connectivity and an accidental deletion. No single row resolves all of them. A retained ciphertext copy without its recovery key is not a successful backup, and a valid hash without a reachable copy cannot restore a file.

## Readiness

**Usable as a selection framework.** Readiness differs by component: Syncthing's untrusted mode is explicitly beta, Hypercore is a developer toolkit, and Blossom's upload and mirroring documents are drafts. Check each entry and the particular implementation you intend to run.

## Primary sources

- IPFS: [persistence and pinning](https://docs.ipfs.tech/concepts/persistence/), [content addressing](https://docs.ipfs.tech/concepts/content-addressing/) and [privacy and encryption](https://docs.ipfs.tech/concepts/privacy-and-encryption/).
- Filecoin: [storage model and incentives](https://docs.filecoin.io/basics/what-is-filecoin/overview), [storage and retrieval deal flow](https://filecoin.io/blog/how-storage-and-retrieval-deals-work-on-filecoin) and [client-side encryption guidance](https://www.filecoin.io/blog/why-is-decentralized-and-distributed-file-storage-critical-for-a-better-web).
- Arweave: [protocol lightpaper and storage endowment](https://arweave.org/files/arweave-lightpaper.pdf) and [project overview](https://www.arweave.org/).
- Tahoe-LAFS: [security and availability model](https://tahoe-lafs.readthedocs.io/en/latest/about-tahoe.html) and [capabilities and reliability](https://tahoe-lafs.readthedocs.io/en/latest/architecture.html).
- Syncthing: [sync and backup limitations](https://docs.syncthing.net/users/faq.html), [transport security](https://docs.syncthing.net/users/security.html) and [untrusted-device beta](https://docs.syncthing.net/users/untrusted.html).
- BitTorrent: [base protocol](https://www.bittorrent.org/beps/bep_0003.html), [DHT](https://www.bittorrent.org/beps/bep_0005.html) and [web seeds](https://www.bittorrent.org/beps/bep_0019.html).
- Hypercore stack: [log replication](https://github.com/holepunchto/hypercore), [Hyperdrive](https://github.com/holepunchto/hyperdrive) and [Hyperswarm](https://github.com/holepunchto/hyperswarm).
- Blossom: [protocol overview](https://github.com/hzrd149/blossom), [blob upload and server policies](https://github.com/hzrd149/blossom/blob/master/buds/02.md) and [optional mirroring](https://github.com/hzrd149/blossom/blob/master/buds/04.md).
