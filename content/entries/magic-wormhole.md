---
title: "Magic Wormhole"
slug: magic-wormhole
type: deep-dive
pillars: ["storage", "cryptography"]
readiness: usable
description: "Magic Wormhole transfers files using a short shared code. Understand PAKE authentication, mailbox coordination and transit relay trust."
dek: "A short code establishes an encrypted transfer; the rendezvous service and file relay have different jobs."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: ["opaque-and-pake", "onionshare", "age-encryption", "private-file-sync-and-backup"]
---

## Summary

Magic Wormhole transfers files between two computers using a human-readable, single-use code. A password-authenticated key exchange (PAKE), currently SPAKE2, turns that code into a shared secret without sending the secret to the coordination service. The code is an authentication secret: give it to the intended recipient through a channel you trust.

## How it works

The **mailbox**, also called the rendezvous service, lets the peers find one another and exchange the messages needed to establish keys. Its short numeric nameplate locates a mailbox; the words in the code provide the secret. Later mailbox messages carry encrypted connection hints.

The **transit** connection carries the file. Peers try a direct connection; if that fails, a transit relay joins their outbound connections. Transit records remain encrypted in either case. A relay is therefore a bandwidth intermediary, not a place where a recipient logs in to collect a plaintext upload.

## Trust model / threat model

The documented protocol does not give the mailbox or transit relay the content-encryption keys. A malicious mailbox still has an opportunity to guess the one-time code; the protocol limits guesses rather than making a short code unguessable. Treat a failed or suspicious exchange as a reason to start again with a fresh code.

Content secrecy does not hide the connection from its endpoints or relay. For a different network-exposure model, the client documents Tor support; when both peers use that mode, transfers use a transit relay rather than advertising listening IP addresses. Compare [OnionShare](/kb/onionshare/) and the underlying [PAKE design](/kb/opaque-and-pake/).

## Readiness

**Usable.** The project provides a command-line client and documented mailbox and transit protocols. Test a small transfer before depending on the receiving platform or network.

## Limits

A successful transfer is not a backup policy, and encryption does not make an untrusted received file safe to open. For retained copies, see [age](/kb/age-encryption/) and [Private file sync and backup](/guides/private-file-sync-and-backup/).

## Primary sources

- [Magic Wormhole overview and PAKE design](https://magic-wormhole.readthedocs.io/en/latest/welcome.html)
- [Mailbox server protocol](https://magic-wormhole.readthedocs.io/en/latest/server-protocol.html)
- [Transit protocol and relay](https://magic-wormhole.readthedocs.io/en/latest/transit.html)
- [Tor support](https://magic-wormhole.readthedocs.io/en/latest/tor.html)
