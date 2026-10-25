---
title: "Tahoe-LAFS"
slug: tahoe-lafs
type: deep-dive
pillars: [storage]
readiness: usable
description: "Tahoe-LAFS encrypts files before distributing erasure-coded shares across a storage grid, with capabilities controlling read and write access."
dek: "Storage servers hold encrypted shares; your capabilities decide who can read, update or verify the data."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [syncthing, compare-storage, decentralized-storage, sia-and-storj, private-file-sync-and-backup]
tags: [tahoe-lafs, capabilities, erasure-coding, storage]
---

## Summary

Tahoe-LAFS is a distributed storage system built around **provider-independent security**. A client encrypts files, encodes the ciphertext into shares and distributes them across a grid of storage servers. Servers need not be trusted with plaintext or with the ability to substitute valid file contents. They are still trusted to supply enough shares when you need them.

## How it works

**Erasure coding.** A file is encoded into *N* shares and can be reconstructed from any *k* valid shares. This tolerates missing shares without storing a complete copy on every server. It does not mean that any *k* arbitrary servers will suffice: placement determines which shares each server holds. Shared power, administration or hosting can also make supposedly separate servers fail together.

**Capabilities.** A capability is a bearer credential, not an account name. Sharing it delegates the authority it contains.

| Capability | Authority |
|---|---|
| Read cap | Locate, validate and decrypt the file. An immutable file cap identifies fixed bytes; a mutable file cap follows versions of that file. |
| Write cap | Read and publish a new version of a mutable file or directory. |
| Verify cap | Check the integrity of stored shares without obtaining the power to decrypt the contents. |

Keep capabilities out of public messages and logs. Passing someone a read cap cannot make them forget a copy they already downloaded. Mutable files support updates; immutable files require a new capability when their bytes change.

**Discovery.** Introducers distribute storage-server announcements. Clients can combine announcements from several introducers, or use static server definitions without an introducer. Introducers help clients find the grid; they do not replace the capabilities that authorize access to data.

## Operating a grid

Run the client or gateway on a machine you trust. Encryption and integrity checking happen there; using somebody else's gateway moves that trust to their machine.

Choose storage operators with independent failure risks. Configure the encoding parameters and review actual share placement. Tahoe-LAFS provides checking, verification and repair mechanisms, but operating the grid means arranging when they run and replacing missing redundancy before too many shares disappear. Keep an independent copy of essential capabilities and recovery instructions.

## Trust model / threat model

The design separates **confidentiality and integrity** from **availability**. Storage servers can withhold or destroy shares, but should not be able to read the file or forge content accepted under its capability. Losing enough distinct shares defeats recovery regardless of how strong the encryption is.

Tahoe-LAFS does not promise anonymity. Its architecture documentation describes exposure of file sizes and opportunities to correlate uploads and downloads. Compromising the client or stealing a capability also bypasses the intended storage-server boundary.

## Readiness

**Usable** for people prepared to run or join a storage grid and manage capabilities. The project supplies client, server and administration software. Availability remains an operational responsibility, not a guarantee supplied by the name of the protocol.

## Limits

Erasure coding adds storage and repair work. A grid concentrated under one operator has correlated failure risk. A lost read capability can be as serious as a lost decryption key. Compare these obligations with ordinary [Syncthing](/kb/syncthing/) replication and the alternatives in [Choosing Decentralized Storage](/kb/compare-storage/).

## Primary sources

- [Tahoe-LAFS canonical repository](https://github.com/tahoe-lafs/tahoe-lafs).
- [Provider-independent security and gateway trust](https://tahoe-lafs.readthedocs.io/en/latest/about-tahoe.html).
- [Architecture: capabilities, encoding, verification and reliability](https://tahoe-lafs.readthedocs.io/en/latest/architecture.html).
- [Node configuration: encoding parameters, introducers and static servers](https://tahoe-lafs.readthedocs.io/en/latest/configuration.html).
