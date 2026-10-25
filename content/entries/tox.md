---
title: "Tox"
slug: tox
type: deep-dive
pillars: [messaging]
readiness: experimental
description: "Tox offers encrypted peer-to-peer messaging without central accounts. Its public-key identities, exposed peer IPs and experimental core shape its limits."
dek: "Direct encrypted communication with a public-key contact identity, but no promise of hiding your network address from friends."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [jami, quiet, compare-messengers, metadata-resistance]
---

## Summary

Tox is a peer-to-peer messaging protocol implemented by a core library and client applications. Contacts exchange a **Tox ID**, rather than registering with a central messaging server. The [official FAQ](https://tox.chat/faq.html) describes default end-to-end encryption and direct communication between contacts.

## How it works

Bootstrap nodes help a client find the distributed hash table. Tox uses that network for discovery and libsodium cryptography for encrypted communication. Bootstrap infrastructure is a discovery dependency, not a central account service.

## Trust model / threat model

The FAQ is explicit: Tox does not hide your IP address from friends you communicate with. An encrypted peer-to-peer connection is not an anonymity network. Check whom you add, protect your local identity keys, and compare [Jami](/kb/jami/) and the [messenger comparison](/kb/compare-messengers/).

## Readiness

**Experimental.** The canonical [c-toxcore repository](https://github.com/TokTok/c-toxcore) calls it an experimental cryptographic network library, says it has not received a formal independent cryptographic audit, and says its security model is not fully specified. Available clients do not remove that limitation.

## Limits

Client behaviour and the underlying protocol are separate things to evaluate. Do not choose Tox on the assumption that removing a central server hides communication relationships or provides an independently validated security design.

## Primary sources

- [Tox FAQ: identities, discovery, encryption and IP exposure](https://tox.chat/faq.html).
- [Canonical Tox core and its security warning](https://github.com/TokTok/c-toxcore).
