---
title: "Cordn"
slug: cordn
type: deep-dive
pillars: [messaging, identity]
readiness: experimental
description: "Cordn is MLS group messaging run through a coordinator you can self-host anywhere, reached over Nostr relays via ContextVM, with Nostr keys as identity."
dek: "MLS needs someone to keep the order of events. Cordn keeps that coordinator and makes it something you can run from a laptop behind a firewall and move."
updated: 2026-10-19
created: 2026-10-19
origin: original
related: [white-noise, marmot-protocol, mls-wire, nostr-protocol, nostr-identity, encrypted-messaging, metadata-resistance, choosing-a-secure-messenger]
aliases: ["Cordn messaging"]
tags: ["cordn", "contextvm", "mls", "nostr", "e2ee", "group-messaging", "self-hosting", "deep-dive"]
---

Cordn is private group messaging that you can run yourself. It uses [MLS (RFC 9420)](/kb/mls-wire/) for end-to-end encryption and Nostr key pairs for identity. A small **coordinator** service keeps each group's messages in order. That service is reached through *ContextVM*, a protocol for exposing services over Nostr relays, so it needs no domain name, TLS certificate, open port or public server. You can run a coordinator from home, from behind a NAT or firewall, or for a single session and then throw it away. The project includes a TypeScript coordinator, a web and Android client, and a CLI, and is at an early, beta stage.

## The design choice: keep the coordinator

MLS is not coordination-free. Every member has to converge on the same ordered history of commits and epochs. Most MLS deployments solve this with a central *Delivery Service*. [Marmot](/kb/marmot-protocol/) and [White Noise](/kb/white-noise/) take the opposite route: they publish MLS traffic directly to many public Nostr relays and let clients resolve conflicting or out-of-order commits. Cordn deliberately sits between the two. It keeps **one active coordinator per group**, which gives each group a single ordered stream with monotonic, per-group cursors. It also makes that coordinator cheap to run anywhere, so the coordination point does not have to be a conventional, exposed and easily suppressed internet service.

## How it works

- **Identity.** A member's MLS `BasicCredential` is bound to their Nostr public key. KeyPackages are published to the coordinator inside signed payloads that clients verify independently, so the coordinator cannot forge someone's identity. Stable identity is needed only where impersonation would matter, such as publishing or deleting your own KeyPackages.
- **Posting.** Once you are in a group, MLS authenticates messages, so ordinary group posts can be sent under **ephemeral transport keys**. The coordinator does not need to learn who in the group is speaking.
- **Opaque payloads.** The coordinator stores and serves each group's stream as opaque bytes, keyed by a delivery id that is not the MLS group id. Clients seal payloads with a per-epoch key from the MLS exporter. The coordinator never parses content and holds no MLS state. All MLS validation happens on the clients. Application messages use a Nostr-shaped envelope inside MLS, and group metadata is carried in an MLS extension (`0xC04D`).
- **Transport.** Coordinators and clients exchange encrypted ContextVM traffic over Nostr relays. A fresh client uses a default public coordinator through the ContextVM relays and relay.primal.net. You can point it at any other coordinator, or start your own with one command (`docker run --rm ghcr.io/cordn-msg/cordn:latest`). The default storage is in-memory, so a throwaway coordinator leaves nothing behind; SQLite is available for persistent deployments. Cordn messages are not published as public Nostr events.
- **Clients.** There is a web app at cordn.net/chat (MIT-licensed, v0.6.0 released October 2026), an Android build distributed through Zapstore and Obtainium, and `@cordn/cli` for scripted use. All of them build on the `ts-mls` library.

## What it protects against

- **Content exposure.** The coordinator and the relays carry only MLS-protected, sealed ciphertext.
- **Identity capture.** There are no phone numbers, emails or account servers. Identity is a Nostr key you hold.
- **Infrastructure suppression.** Because a coordinator needs no public address, it is hard to find, block or seize. If one disappears, you can stand up another from ordinary hardware.
- **Public metadata trails.** Group identifiers and traffic are not published network-wide as protocol-specific events. Cordn activity is mixed into general encrypted ContextVM traffic, which makes it less legible to relay operators and outside observers than designs that publish openly to relays.
- **Ordering failures.** A single ordered stream per group avoids the forked or stale group state that weakly ordered relay delivery can cause.

## What it trusts, and the limits

- **The coordinator sees the shape of the group.** It can see that a group is active and learn its timing and volume. It can also delay, drop or censor messages, although it cannot read or forge them. A public coordinator is a convenience trade-off. For groups with higher stakes, Cordn's own answer is to self-host a personal, circle-wide or one-session coordinator.
- **Availability depends on one coordinator per group.** If that coordinator is down, the group stalls; group state survives on members' devices. Moving a group between coordinators is anticipated in the design (per-group cursors exist partly for that), but the current specification leaves migration out of scope.
- **Relays and the network.** ContextVM relays carry the traffic and see connection metadata, including your IP address. To hide that, use a network-level tool such as [Tor](/kb/tor/).
- **Young code and draft specs.** All four specification documents are marked *Draft*. The project dates from April 2026, has a small community, and no independent audit has been published. At the time of writing, the coordinator repository carries no licence file, although the web client is MIT. Check the licence before building on it.
- **Your device and your key**, as with any end-to-end encrypted messenger.

## Readiness

**Experimental.** The design is clearly reasoned and honest about its trade-offs, and the code runs today. But the specifications are drafts, the software is beta, there has been no audit, and the user base is small. Treat it as a promising way to run sovereign MLS group chat, and as an instructive contrast to relay-native Marmot, rather than as a messenger for high-risk use.

## Primary sources

- Cordn: https://cordn.net/ · Why Cordn: https://cordn.net/why · Web app: https://cordn.net/chat
- Coordinator and specification: https://github.com/Cordn-msg/cordn · Spec 00 (coordinator and identity model): https://github.com/Cordn-msg/cordn/blob/master/spec/00.md · Spec 01 (group metadata extension): https://github.com/Cordn-msg/cordn/blob/master/spec/01.md · Spec 02 (application-message envelope): https://github.com/Cordn-msg/cordn/blob/master/spec/02.md · Spec 03 (opaque group payloads): https://github.com/Cordn-msg/cordn/blob/master/spec/03.md
- Web client: https://github.com/Cordn-msg/cordn-web · Releases: https://github.com/Cordn-msg/cordn-web/releases
- ContextVM: https://contextvm.org/
- ts-mls: https://github.com/LukaJCB/ts-mls · MLS: RFC 9420 https://www.rfc-editor.org/rfc/rfc9420
