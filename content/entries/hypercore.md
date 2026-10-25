---
title: "Hypercore and Hyperdrive"
slug: hypercore
type: deep-dive
pillars: [storage]
readiness: usable
description: "Hypercore verifies replicated logs with signed Merkle trees; Hyperdrive adds files and Hyperswarm connects peers, with retention left to operators."
dek: "Replicate verifiable data streams and changing files, while deciding explicitly which peers keep the bytes."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [local-first-crdts, syncthing, bittorrent-archives, compare-storage, decentralized-storage]
tags: [hypercore, hyperdrive, hyperswarm, holepunch, storage]
---

## Summary

The Holepunch repositories provide several distinct components: **Hypercore** for verifiable replicated logs, **Hyperdrive** for a distributed file system, and **Hyperswarm** for finding and connecting peers. Together they provide building blocks for applications that distribute data without a single download server.

They do not supply an automatic retention contract. Decide which machines will download and retain the data before relying on it as an archive.

## How it works

**Hypercore** describes itself as an append-only log. Signed Merkle trees let readers verify replicated data against the log's authentication information. Sparse replication lets a reader download selected blocks rather than the entire log. A block that has not been downloaded still requires a reachable peer holding it.

There is an important qualification to “append-only”: the current API includes **truncation and forks**. Applications must decide how to handle those operations. Do not treat the label as a promise that an authorized writer cannot revise the log's history.

**Hyperdrive** adds a file-oriented API with paths, reads, writes and deletions. It supports version checkouts and explicit downloads of file content. Opening or following a drive is therefore different from arranging a complete retained copy of all its files.

**Hyperswarm** finds peers interested in a shared topic through a DHT. Its API separates announcing a server for a topic from searching for servers. Connections are end-to-end encrypted with Noise. Discovery provides connections to peers; it does not store their file data for them.

## Trust model / threat model

Signed log data lets a reader detect data that fails verification. The application still needs to obtain the correct log identity and decide which writers to trust. A valid signature does not establish that an update is desirable.

Transport encryption protects a connection. Hypercore also supports application-supplied encryption, but an application must make its own choices about content confidentiality and key distribution. Do not infer private storage from the presence of a public key or a signed tree. Likewise, encrypted connections are not a promise to hide peer network addresses.

## Readiness

**Usable as developer components**, with documented replication, networking and filesystem APIs. This rating does not imply a finished backup application. Evaluate the actual software built on them, including its writer permissions, retained blocks and restore procedure.

## Limits

Sparse replicas may lack the block you need when other peers go offline. Retention, storage capacity and any hosting costs belong to the deployment. Writer compromise and application mistakes remain possible despite valid signatures. Truncation needs explicit handling where immutable history matters.

Compare [BitTorrent](/kb/bittorrent-archives/) for fixed archive distribution, [local-first CRDTs](/kb/local-first-crdts/) for merging concurrent application edits, and [Syncthing](/kb/syncthing/) for an existing folder-sync application.

## Primary sources

- [Holepunch Hypercore repository: signed trees, sparse replication, encryption and truncation](https://github.com/holepunchto/hypercore).
- [Holepunch Hyperdrive repository: file operations, versions and downloads](https://github.com/holepunchto/hyperdrive).
- [Holepunch Hyperswarm repository: DHT discovery and Noise connections](https://github.com/holepunchto/hyperswarm).

Continue with [Secure Scuttlebutt](/kb/secure-scuttlebutt/).
