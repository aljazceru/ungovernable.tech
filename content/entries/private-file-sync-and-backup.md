---
title: "Private File Sync and Backup"
slug: private-file-sync-and-backup
type: guide
pillars: [storage, cryptography]
readiness: usable
description: "Replicate files across your devices with Syncthing, test an untrusted encrypted replica, and keep a separate offline archive with a recovery plan."
dek: "Maintain useful working copies, limit what a remote storage host can read, and preserve a way back from mistakes."
updated: 2026-10-25
created: 2026-10-25
origin: original
level: intermediate
related: [syncthing, tahoe-lafs, encrypting-files-and-backups, age-encryption, kiwix, compare-storage]
tags: [syncthing, backup, file-sync, encryption, offline]
---

## Summary

This setup has three roles: trusted devices with readable working files, an optional remote device holding an encrypted replica, and an offline archive that stays outside synchronization. Start with disposable files and complete a restore before adding important data.

[Syncthing](/kb/syncthing/) propagates changes, including deletion. Its **untrusted encrypted-device feature is explicitly beta / testing only**. Keep an independent backup while evaluating it, and do not make that encrypted replica your only recovery path.

## 1. Prepare trusted devices

Install Syncthing on the computers you control using the project distribution or an appropriate package for the operating system. Follow its getting-started guide to launch the local administration interface.

Choose a dedicated folder for the first sync test. Avoid beginning with your entire home directory. Keep a copy of the starting files outside the shared folder.

On each device, use **Actions → Show ID**. Compare the IDs through a channel you already trust, then use **Add Remote Device** on both sides. Device IDs are certificate hashes; a convenient device name is not the identity check. Keep the administration interface local unless you have deliberately configured secure remote access.

## 2. Share and test a folder

Share the test folder with the other trusted device and accept the folder there. The **folder ID must match**; the local directory paths can be chosen for each machine. For ordinary synchronization between trusted devices, leave the per-device folder encryption password empty.

Create a disposable file, let it arrive, edit it on the other device, and check the result. Disconnect a device, make another change and reconnect it. Finally delete the disposable file and observe that the deletion propagates too. Wait for synchronization to finish before treating the other device as an up-to-date copy.

Decide whether the convenience of discovery and relays fits your metadata requirements. Global discovery can link device IDs to addresses; local discovery announces IDs and ports on the LAN. Relays learn device IDs while carrying encrypted traffic. These settings do not provide anonymity.

## 3. Add an untrusted encrypted device

Use a separate test folder first. The remote host may store and serve the encrypted replica, but the password belongs on trusted devices.

1. Add the remote device by its verified ID. On each trusted device, mark that remote device **Untrusted** in its advanced device settings. This prevents a connection if a shared folder lacks an encryption password.
2. In the trusted device's folder-sharing settings, set a strong folder password for that remote device. Save the password and folder ID independently of the remote host. Use an uninformative folder label if the label itself is sensitive.
3. On the remote device, accept the folder with type **Receive Encrypted**. Do not enter the plaintext folder password there.
4. Let synchronization finish. Inspect the remote storage to confirm that expected filenames and contents are not present as plaintext. This is a configuration check, not a cryptographic audit.
5. Test recovery on another trusted device: share the same folder ID with the encrypted device, supply the same password in that trusted device's sharing settings and use an empty local destination. Verify that the recovered files open correctly.

The feature hides file data, filenames and other file metadata, including the original directory structure. **Folder ID, label and file sizes remain exposed.** A remote operator can also refuse service or lose the replica. Password loss and deletion propagation remain your responsibility.

## 4. Add versioning, then an offline archive

Enable a suitable versioning policy on trusted receiving devices if you want older copies of files replaced or deleted by another device. Syncthing versioning is configured per folder and device, is off by default, and does **not** preserve the previous version of a change made locally on that same device.

Create a separate archive after checking that the source files are intact. Copy or back up the chosen files to removable storage outside every synchronized folder. For private material, follow [Encrypting Files, Disks and Backups](/guides/encrypting-files-and-backups/) to encrypt the archive and arrange recovery of its key.

Restore a sample to a different directory, open it and compare it with the original. Then disconnect the archive disk and keep it separately. Retain earlier archives when making new ones so that a new copy of damaged files does not replace your only good copy. Write down the date, contents and restore procedure.

For offline reference material rather than personal documents, add a tested [Kiwix](/kb/kiwix/) reader and the archives you need before an outage.

## Trust model / threat model

Trusted devices can read and change shared files. Their identity keys and configuration need protection alongside the data. Remove a lost device from the remaining peers. The encrypted host should lack the folder password, but it still controls availability. The offline archive supplies a separate recovery point only if its media and recovery key remain usable.

## Readiness and limits

Ordinary folder sync is **usable**; the encrypted untrusted-device component is **experimental**. Expect to maintain the setup and repeat restore exercises. Synchronization cannot recover an earlier state it no longer holds, offline archives become stale between updates, and no encryption protects readable data on a compromised trusted device.

If running a remote replica is unsuitable, compare [Tahoe-LAFS](/kb/tahoe-lafs/) and the other models in [Choosing Decentralized Storage](/kb/compare-storage/).

## Primary sources

- [Syncthing getting started: device pairing and folder sharing](https://docs.syncthing.net/intro/getting-started.html).
- [Syncthing security: identities, discovery, relays and device compromise](https://docs.syncthing.net/users/security.html).
- [Untrusted devices: setup, exposed metadata and recovery](https://docs.syncthing.net/users/untrusted.html).
- [File versioning: configuration and local-change limitation](https://docs.syncthing.net/users/versioning.html).
- [Syncthing FAQ: matching folder IDs and why sync is not a backup](https://docs.syncthing.net/users/faq.html).

Continue with [CryptPad](/kb/cryptpad/).
