---
title: "Delay-tolerant networking"
slug: delay-tolerant-networking
type: explainer
pillars: ["mesh"]
readiness: usable
description: "Delay-tolerant networks store messages across broken links. Compare Bundle Protocol v7, BPSec and the separate delivery designs of offline messengers."
dek: "Store, carry and forward lets delivery span disconnected periods; security and delivery responsibility need their own design."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: ["off-grid-networks", "reticulum", "briar", "bitchat"]
---

## Summary

Delay-tolerant networking (DTN) is designed for paths that may not exist end to end at the moment a message is sent. Nodes can retain data until a suitable contact becomes available. RFC 4838 describes this store-and-forward architecture, including persistent storage across interruptions.

## How it works

**Bundle Protocol v7**, specified in RFC 9171, carries application data in bundles across different underlying transports. Bundle lifetime bounds how long a bundle remains useful; extension blocks can record age and hop count. The protocol does not make the next contact arrive or guarantee sufficient storage.

**Custody** is responsibility for retaining a bundle until another node accepts that responsibility. It appears in the earlier DTN architecture, but RFC 9171 explicitly moves custody transfer out of the base protocol to a separate bundle-in-bundle encapsulation specification. Do not describe custody transfer as an automatic BPv7 feature.

**BPSec**, RFC 9172, defines integrity and confidentiality services for bundle blocks. Its protection can span disconnected forwarding steps. Security policy, key management and which blocks receive protection still have to be configured.

## Related delivery designs

[Reticulum](/kb/reticulum/)'s LXMF messaging layer documents propagation nodes that store encrypted messages for offline recipients. [Briar](/kb/briar/) synchronizes through direct Bluetooth or Wi-Fi contacts as well as online connections. [Bitchat](/kb/bitchat/)'s whitepaper describes opportunistic couriers and store-and-forward delivery.

These are useful comparisons for intermittent delivery. Their own documented protocols should guide interoperability decisions; this comparison does not establish Bundle Protocol compatibility.

## Trust model / threat model

A forwarding node can withhold or discard a stored message. Encryption protects selected contents, not the existence of a contact, storage consumption or successful eventual delivery. Decide which nodes may hold copies, how long they may retain them and how the sender will learn about delivery.

## Readiness

**Usable.** BPv7 and BPSec are published standards. A usable deployment also needs compatible implementations, security contexts and an operational contact plan; the standards alone are not a phone messenger.

## Limits

A courier cannot deliver without a future path. Budget storage and expiry for the longest interruption you intend to tolerate, then rehearse it. Start with [off-grid networks](/kb/off-grid-networks/) for the wider transport choices.

## Primary sources

- [RFC 4838: DTN architecture and persistent storage](https://www.rfc-editor.org/rfc/rfc4838.html)
- [RFC 9171: Bundle Protocol v7, including custody changes](https://www.rfc-editor.org/rfc/rfc9171.html)
- [RFC 9172: Bundle Protocol Security](https://www.rfc-editor.org/rfc/rfc9172.html)
- [LXMF propagation and offline delivery](https://github.com/markqvist/LXMF)
- [Briar connection and synchronization model](https://briarproject.org/how-it-works/)
- [Bitchat courier and retention design](https://github.com/permissionlesstech/bitchat/blob/main/WHITEPAPER.md)
