---
title: "Object Capabilities: Spritely Goblins and OCapN"
slug: object-capabilities
type: deep-dive
pillars: [apps, cryptography]
readiness: experimental
description: "Object-capability security gives code only the references it is handed. How Spritely Goblins and the OCapN protocol bring it to peer-to-peer apps."
dek: "If holding a reference is the only way to use something, an app can do nothing you did not hand it. Capability security is the quiet idea under sandboxed applets, delegated tokens and the most ambitious peer-to-peer programming work."
updated: 2026-10-29
created: 2026-10-29
origin: original
related: [sovereign-applications, napplet, biscuit, tails-qubes-whonix, threat-modeling]
aliases: ["ocap", "object-capability security", "Spritely Goblins", "OCapN", "CapTP", "Spritely Institute"]
tags: ["ocap", "capabilities", "spritely", "goblins", "ocapn", "captp", "least-authority", "deep-dive"]
---

## Summary

Most software runs with **ambient authority**: a program you start can read every file you can read and reach every server you can reach. **Object-capability** (ocap) security replaces that with one rule: to use something, you must hold a reference to it, and the only ways to get a reference are to create the object, be given the reference, or have been born with it. Authority then follows the references you deliberately pass around, which makes the **principle of least authority** something the system enforces rather than something developers promise.

The same idea appears throughout this pillar. A [napplet](/kb/napplet/) can use only the capability domains its shell injects. A WebAssembly module can call only the host functions it imports. A [Biscuit](/kb/biscuit/) token carries exactly the rights it was attenuated to. Compartmentalised systems such as Qubes ([Tails, Qubes OS and Whonix](/kb/tails-qubes-whonix/)) apply the same instinct at the level of whole virtual machines.

## Spritely Goblins

The Spritely Institute's **Goblins** is a distributed object programming environment built on capability security. Objects can live anywhere on the network, and calling a remote object looks like ordinary asynchronous programming. Goblins provides automatic transactions for synchronous operations within one process, distributed debugging tools, and a persistence and upgrade model designed not to break its security properties. It is available for Guile Scheme and Racket (version 0.18.0 for both at the time of writing), and the Guile release is signed.

## OCapN

**OCapN** (Object Capability Network) is the protocol work that lets capability systems talk across machines and languages. Its pre-standardisation group includes Agoric, the Spritely Institute, Cap'n Proto and independent experts. It covers:

- **CapTP**, the Capability Transport Protocol, for programming against networked objects.
- **Third-party handoffs**, so one peer can securely give another a reference to an object on a third peer, using a certificate-based approach.
- **Netlayers**, a generic transport interface with specified implementations, which the group says can range from Tor onion services and I2P to libp2p.
- **A URI scheme** for addressing machines and objects.

Implementations include Goblins for Guile and Racket, Endo (JavaScript) and DObjects (Dart).

## What it protects against

- **Confused deputies and over-privileged code.** A component cannot misuse authority it was never handed.
- **Damage from a compromised component.** A buggy or malicious part of an app is limited to the references it held.
- **Hidden network dependencies.** Remote authority is explicit and can run over anonymising transports such as Tor onion services.

## What it trusts, and the limits

- **The runtime.** Capability discipline holds only if the language runtime and the netlayer enforce it.
- **Programmers keeping to the model.** Reintroducing ambient authority through a convenient global undoes the benefit.
- **Revocation and delegation design.** Capabilities can be passed on; limiting or revoking them needs deliberate patterns.
- **Maturity.** OCapN is still pre-standard and Goblins is pre-1.0. This is the research frontier of the pillar, not something to deploy for high-risk users today.

## Readiness

**Experimental.** The ideas are decades old and well understood. The distributed tooling that would let ordinary peer-to-peer apps use them is real, open source and under active development, but still early.

## Primary sources

- Spritely Goblins: https://spritely.institute/goblins/
- Guile Goblins documentation: https://files.spritely.institute/docs/guile-goblins/latest/
- OCapN pre-standardization group: https://ocapn.org/ · GitHub: https://github.com/ocapn/ocapn
- Endo (JavaScript): https://github.com/endojs/endo
- WebAssembly security model: https://webassembly.org/docs/security/
