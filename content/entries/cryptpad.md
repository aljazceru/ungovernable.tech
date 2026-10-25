---
title: "CryptPad"
slug: cryptpad
type: deep-dive
pillars: ["storage", "messaging"]
readiness: usable
description: "CryptPad encrypts collaborative documents in the browser. Understand instance metadata, sharing-link trust and the responsibilities of self-hosting."
dek: "Encrypted collaboration reduces what stored documents reveal, while the browser still depends on code delivered by the instance."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: ["local-first-crdts", "decentralized-storage", "private-file-sync-and-backup"]
---

## Summary

CryptPad is a collaborative document suite with client-side, end-to-end encryption. Its implementation encrypts content in the browser before sending it to the server. Collaboration and confidentiality are separate design choices; see [local-first software and CRDTs](/kb/local-first-crdts/) for that distinction.

## How it works

Clients exchange encrypted document changes through an instance. The project provides the source code and an administrator guide for installing and maintaining your own instance. Self-hosting chooses who operates the service; it also assigns you the work of configuring, updating and maintaining it.

## Trust model / threat model

The security guide explicitly requires trusting the chosen instance to deliver the published code and carry network messages. Under those assumptions the instance cannot read document contents. A server that supplies altered browser code breaks that assumption.

The instance can still see the user's IP address and browser/operating-system information. CryptPad calls this only weak anonymity. Collaborators must also be trusted with sharing links: forwarding a link can give another person access. The guide documents passwords as an additional protection when a sharing link crosses an insecure channel.

## Readiness

**Usable.** The project publishes user documentation, production installation instructions and its implementation. Use the production guide for a real instance; a development configuration is not a production deployment.

## Limits

Encryption is not a promise of uninterrupted availability or recovery from every mistaken deletion. Plan separate recovery arrangements for important work; see [Private file sync and backup](/guides/private-file-sync-and-backup/) and [decentralized storage](/kb/decentralized-storage/).

## Primary sources

- [CryptPad project](https://cryptpad.org/)
- [Security assumptions, metadata and sharing links](https://docs.cryptpad.org/en/user_guide/security.html)
- [Administrator guide](https://docs.cryptpad.org/en/admin_guide/index.html)
- [Implementation and production deployment guidance](https://github.com/cryptpad/cryptpad)
