---
title: "White Noise"
slug: white-noise
type: deep-dive
pillars: [messaging, identity]
readiness: experimental
description: "White Noise is an open-source messenger built on Marmot: MLS group encryption over Nostr relays, with no phone number, no email and no central server."
dek: "The flagship Marmot client. MLS gives it Signal-class group encryption; Nostr gives it keys you own and relays you choose. It is audited, actively shipped, and still beta."
updated: 2026-10-25
created: 2026-10-19
origin: original
related: [marmot-protocol, mls-wire, cordn, nostr-protocol, nostr-identity, nostr-key-custody, encrypted-messaging, choosing-a-secure-messenger, metadata-resistance, signal-protocol, simplex, nymchat]
aliases: ["Whitenoise", "White Noise messenger"]
tags: ["white-noise", "marmot", "mls", "nostr", "e2ee", "group-messaging", "deep-dive"]
---

White Noise is a private messenger for one-to-one and group chat that needs no phone number, email address or real name: you pick a name, the app generates a Nostr key pair, and that key *is* your account. Under the hood it is the reference application of the [Marmot protocol](/kb/marmot-protocol/), which runs [MLS (RFC 9420)](/kb/mls-wire/) group encryption over ordinary [Nostr](/kb/nostr-protocol/) relays. It is free, open source (the apps are AGPL-3.0, the Marmot Development Kit is MIT), and published by the Internet Privacy Foundation (IPF). Its own site describes it as beta.

## How it works

**Identity.** Your account is a Nostr key pair. Contacts are added by profile link, QR code or public key. You can hold several identities at once, for example one for work, one for friends, and a throwaway for people you have just met. There is no account server to register with, so there is nothing for an operator to suspend. The flip side is that nobody can reset a lost key for you (see [Nostr key custody](/kb/nostr-key-custody/)).

**Encryption.** Every conversation, including a one-to-one chat, is an MLS group. MLS provides forward secrecy and post-compromise security, and it scales to large groups because adding or removing a member costs a logarithmic number of operations rather than one per member.

**Transport.** The Marmot spec maps MLS onto Nostr events. A user publishes *KeyPackages* (kind `30443`) so others can invite them asynchronously. Invitations (*Welcomes*, kind `444`) travel inside NIP-59 gift wraps (kind `1059`), which hide the recipient's group membership from relays. Group traffic (proposals, commits and messages) is published as kind `445` events. Each kind `445` event is signed by a **fresh ephemeral key** and tagged only with an opaque group id, and its content carries an extra layer of encryption derived from the MLS group secret. A relay therefore sees opaque blobs from throwaway keys rather than "Alice posted to group X". The client connects to several relays at once, and the spec requires redundant delivery, so a relay that goes down, gets blocked or turns hostile does not break the group. You can choose your relays or run your own.

**Everything else.** Media is encrypted on the device before it is uploaded to Blossom servers that you can pick; IPF runs none of them. Optional push notifications go through *Transponder*, a notification relay that IPF operates. It receives gift-wrapped triggers sent from ephemeral keys and passes on content-free pushes through Apple and Google. Usage telemetry is off by default.

**Platforms and code.** There are native apps for Android (Zapstore, Google Play, GitHub releases) and iPhone (TestFlight beta), with macOS and Linux clients in development. Releases ship on roughly a weekly cadence. The protocol logic lives in the Rust *MDK* (Marmot Development Kit), with bindings for other languages; a TypeScript implementation, marmot-ts, also exists. Any developer can build a compatible client without permission. White Noise can also add a self-hosted software agent as an ordinary contact over the same encrypted channel.

## What it protects against

- **Reading by servers.** Relays, media hosts and the push service see only ciphertext. Neither IPF nor relay operators can read messages.
- **Identity capture.** There is no phone number or email to subpoena, SIM-swap or link back to a legal identity. There is no account server either.
- **De-platforming and single points of failure.** Messages go out to several independent relays, and you can switch relays or self-host without losing your identity or contacts. Because the protocol is open, you can also change apps.
- **Key compromise over time.** MLS forward secrecy and post-compromise security limit how much a stolen key exposes, in both directions in time.
- **Invitation content.** Gift wrapping encrypts the invitation and conceals its original sender. A visible NIP-59 event still exposes the recipient public key in its `p` tag; observers can see recipient and timing metadata.

## What it trusts, and the limits

- **Your device and your key.** Anyone with an unlocked or compromised phone reads everything on it. White Noise cannot recover a lost private key. The key alone is also not a backup of your history: conversation state lives on the device, and linked multi-device support is still being designed in Marmot.
- **Relays for availability, not secrecy.** Relays can drop, delay or refuse events, and they see your IP address, when you connect, and roughly how much traffic you move. White Noise itself warns that using it does not make you anonymous. For network-level privacy, put it behind [Tor](/kb/tor/) or a VPN.
- **Visible metadata.** Publishing KeyPackages reveals that a key uses Marmot. Receiving gift wraps reveals that you are being contacted. Ordering in a relay-based design is weaker than with a central server, so concurrent commits must be resolved by the clients. [Cordn](/kb/cordn/) is a project that makes the opposite trade-off.
- **Optional IPF infrastructure.** If you enable push notifications, IPF's Transponder handles platform push tokens. It is designed not to persist them or link them to identities, but it is still a service run by a single operator. Leave push off if that matters to you.
- **A moving specification.** In 2026 Marmot moved from its numbered MIP documents to a reorganised specification marked "adopted". The changelog still records normative changes every week. Least Authority reviewed the protocol (November 2025) and audited both the MDK (final report March 2026) and the whitenoise-rs backend (April 2026). Those audits covered the code as it stood then, before the current native apps and the spec reorganisation.

## Readiness

**Experimental.** The cryptography is the IETF standard, the code is open and has had independent audits, and the apps are in active, frequent release. However, the project describes itself as beta, distributes on iOS through TestFlight, lacks linked-device support, and builds on a specification that is still changing week to week. It is a good choice for people who already live on Nostr and want encrypted groups without a phone number. For high-stakes use, run it alongside a battle-tested messenger rather than instead of one. See [Choosing a Secure Messenger](/guides/choosing-a-secure-messenger/).

For a comparison of identifiers, relay exposure and readiness, see [Choosing a private messenger](/kb/compare-messengers/).

## Primary sources

- [NIP-59: visible recipient tags](https://github.com/nostr-protocol/nips/blob/master/59.md)

- White Noise: https://www.whitenoise.chat/ · FAQ: https://www.whitenoise.chat/faq · Privacy policy: https://www.whitenoise.chat/privacy · Downloads: https://www.whitenoise.chat/download
- Marmot protocol specification: https://github.com/marmot-protocol/marmot · Nostr transport: https://github.com/marmot-protocol/marmot/blob/master/transports/nostr.md · Changelog: https://github.com/marmot-protocol/marmot/blob/master/changes.md
- Code: MDK https://github.com/marmot-protocol/mdk · Android https://github.com/marmot-protocol/whitenoise-android · iOS https://github.com/marmot-protocol/whitenoise-ios · Transponder https://github.com/marmot-protocol/transponder · marmot-ts https://github.com/marmot-protocol/marmot-ts
- Audits (Least Authority): protocol review https://leastauthority.com/blog/audit-of-white-noise-marmot-protocol-review/ · MDK https://leastauthority.com/blog/audit-of-white-noise-marmot-development-kit-mdk/ · whitenoise-rs https://leastauthority.com/blog/audit-of-white-noise-whitenoise-rs/
- MLS: RFC 9420 https://www.rfc-editor.org/rfc/rfc9420
