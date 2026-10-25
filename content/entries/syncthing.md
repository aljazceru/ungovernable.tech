---
title: "Syncthing"
slug: syncthing
type: deep-dive
pillars: [storage]
readiness: usable
description: "Syncthing replicates files between devices you choose, with authenticated TLS, discovery and relays, plus an experimental encrypted storage mode."
dek: "Keep working copies on your own devices, while separating encrypted transport, encrypted storage and recovery from mistakes."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [private-file-sync-and-backup, tahoe-lafs, local-first-crdts, compare-storage, encrypting-files-and-backups]
tags: [syncthing, file-sync, storage, encryption]
---

## Summary

Syncthing synchronizes folders between devices you approve. Creation, edits and deletions propagate between those devices when they can connect. You choose the machines that hold the files; a central file-hosting account is not required. This makes it useful for keeping working documents on several computers. A separate archive is still necessary for recovery from unwanted changes.

## How it works

The **Block Exchange Protocol (BEP)** exchanges file indexes containing metadata and block hashes. Devices use those indexes to request missing or changed blocks from peers. The protocol transfers file blocks; it does not merge the meaning of concurrent document edits like a [CRDT](/kb/local-first-crdts/).

Connections use **TLS**. A device ID represents the SHA-256 hash of that device's certificate, encoded for exchange between users. Each side must approve the other's ID. The ID authenticates a device key; verifying whose device it belongs to is your job.

Discovery and relays help approved devices connect:

| Mechanism | Role | Information exposed |
|---|---|---|
| Global discovery | Looks up connection addresses for device IDs | The discovery operator learns IDs, advertised addresses and lookup requests, allowing relationships between devices to be inferred. |
| Local discovery | Announces devices on the local network | Local observers can see device IDs and listening ports. |
| Relays | Carry traffic when devices need a relayed connection | The relay learns the connecting device IDs. File traffic remains encrypted between the endpoints. |

These services help connectivity; they do not make Syncthing anonymous. Discovery and relaying can be disabled or configured to use selected infrastructure.

## Untrusted encrypted devices

A trusted device can set a password when sharing a particular folder with an untrusted device. The receiving device uses the **Receive Encrypted** folder type. It stores encrypted content, filenames and metadata without reproducing the original directory layout. Folder IDs, labels and file sizes remain exposed.

Another trusted device can recover readable files through that encrypted replica using the same folder password and folder ID. Keep both independently. On trusted devices, marking the remote device **Untrusted** prevents a connection if a shared folder is missing its encryption password.

The documentation explicitly labels this feature **beta / testing only**. It should be an additional copy while you test recovery, with an independent backup retained.

## Trust model / threat model

Ordinary trusted peers receive readable files. TLS protects transfer, not files on those peers' disks. Their operating systems, Syncthing configuration and identity keys remain part of the trust boundary. Someone who obtains a device's keys and configuration can impersonate it to its peers. Revoke a lost device from the other devices.

The untrusted mode reduces what a storage host can read. It cannot force that host to retain files or stay reachable.

## Readiness

**Usable** for ordinary device-to-device folder synchronization. Treat the encrypted untrusted-device feature as **experimental**, following its own documentation rather than the readiness of the core sync service.

## Limits

Synchronization spreads deletions and damaging edits as well as useful changes. Syncthing's FAQ explicitly discourages treating it as the only backup. Devices also need overlapping connectivity, directly or through another device holding the data. Discovery is not storage.

Follow [Private File Sync and Backup](/guides/private-file-sync-and-backup/) for a setup with a separate offline archive. Compare [Tahoe-LAFS](/kb/tahoe-lafs/) when the main task is encrypted storage across several operators.

## Primary sources

- [Syncthing project](https://syncthing.net/).
- [Block Exchange Protocol specification](https://docs.syncthing.net/specs/bep-v1.html).
- [Security principles, discovery and relay exposure](https://docs.syncthing.net/users/security.html).
- [Untrusted encrypted devices: configuration, recovery and beta warning](https://docs.syncthing.net/users/untrusted.html).
- [Syncthing FAQ: synchronization and backup limitations](https://docs.syncthing.net/users/faq.html).
