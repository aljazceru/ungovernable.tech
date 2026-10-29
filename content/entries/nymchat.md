---
title: "Nymchat"
slug: nymchat
type: deep-dive
pillars: [messaging, mesh]
readiness: experimental
description: "Nymchat is a pseudonymous Nostr chat app with geohash channels, NIP-17 private chats, a Bitchat-compatible Bluetooth mesh and hybrid post-quantum encryption."
dek: "Pick a throwaway nym and talk: public geohash and topic channels over Nostr relays, gift-wrapped private and group chats, and a Bluetooth mesh shared with Bitchat for when the internet is gone. Feature-rich and open source, with a hosted backend you should understand before relying on it."
updated: 2026-10-29
created: 2026-10-29
origin: original
related: [bitchat, white-noise, nostr-protocol, compare-messengers, metadata-resistance, off-grid-messaging, internet-shutdown-preparedness, choosing-a-secure-messenger, post-quantum-cryptography, zapstore]
aliases: ["NYM", "Nostr Ynstant Messenger", "Nymchat app"]
tags: ["nymchat", "nostr", "nip-17", "geohash", "bitchat", "ble-mesh", "post-quantum", "messaging", "deep-dive"]
---

Nymchat, also called **NYM** (Nostr Ynstant Messenger), is a chat client built on [Nostr](/kb/nostr-protocol/). It runs as a web app at [web.nymchat.app](https://web.nymchat.app/) and as native Android and iOS apps. You can start chatting without registering: the app generates a temporary keypair and a random nickname for the session, or you can log in with an existing Nostr identity. It is developed by 21 Million LLC, which also runs other Nostr infrastructure (the Nosflare relay, NostrMedia and NostrAddress) under the Nostr Services name. The source, including the Flutter code for the native apps, is published under AGPL-3.0 at [github.com/Spl0itable/NYM](https://github.com/Spl0itable/NYM). The repository dates from August 2025 and releases are frequent.

**Not to be confused with Nym.** Despite the name, Nymchat does not use the [Nym mixnet](/kb/nym/) and is not made by Nym Technologies. "Nym" here means a pseudonym. A separate, now-archived project called nymCHAT did build messaging on the Nym mixnet.

## How it works

**Public channels.** Channels are Nostr ephemeral events: kind `20000` for **geohash** channels, which are scoped to a place from a whole region down to a city block (for example `#dr5r`), and kind `23333` for named topic channels. Geohash channels are the same location channels [Bitchat](/kb/bitchat/) uses, so Nymchat and Bitchat users see each other's messages. Channel messages are public, unencrypted and readable by anyone on the relays. Users appear as a nickname plus a four-character suffix from their public key, such as `cyber_wolf#a3f2`.

**Private and group chats.** Direct messages use [NIP-17](https://github.com/nostr-protocol/nips/blob/master/17.md): the message is sealed and then gift-wrapped (kind `1059`) under a one-time sender key, with timestamps randomised by up to two hours so relays cannot easily link sender, recipient and timing. Group chats send a separate gift wrap to each member, up to 100 members. Nymchat adds its own extension: each member advertises a fresh ephemeral key inside every encrypted message, and later messages are addressed to that key rather than the member's real public key. The goal is to stop relays inferring group membership from a burst of wraps to the same known keys, and to let a member recover from a compromised key simply by sending a new message. The README also lists optional per-message forward secrecy and disappearing messages for DMs.

**Hybrid post-quantum encryption.** Between Nymchat users, the key exchange behind NIP-44 encryption is combined with **ML-KEM-768** (FIPS 203), aiming to keep recorded traffic confidential even if elliptic-curve cryptography is later broken by a quantum computer. Each client announces its ML-KEM public key in a signed Nostr event, and peers without one (Bitchat, other Nostr clients, older builds) receive standard NIP-17 instead. The project is explicit about the scope: this protects confidentiality, not signatures, which remain secp256k1. There is a deeper catch in how the ML-KEM key is made. The README describes it as derived from the Nostr secret key, and the current app labels such a key "legacy": a quantum computer that recovers the identity key from the public npub recovers the ML-KEM key with it. Newer builds root the key in a separate post-quantum recovery code instead. The protection is therefore real only when both sides hold such a code, and in groups only when every member does. A browser-extension or remote-signer login can always send post-quantum, but it can receive post-quantum only once it has a recovery code; without one it receives classical NIP-44.

**Bluetooth mesh.** The Android and iOS apps join a Bluetooth Low Energy mesh that is wire-compatible with Bitchat, including its Noise XX encrypted sessions. Messages hop from phone to phone with no internet, and the app switches between the internet and the mesh automatically. The web app can join from Chromium browsers (Chrome, Edge, Opera, Brave), but only as a leaf: a browser cannot advertise itself, so it must be paired once with a nearby phone running a native client that relays for it, and two browsers cannot link to each other. A laptop alone is not an offline messenger. An opt-in **Ghost Mode** replaces every identifier the device announces on the mesh (keys, Bluetooth name, nickname and Nostr link) with throwaway values and rotates them roughly every 15 minutes. The project itself says this makes you much harder to follow, not anonymous: the phone's Bluetooth hardware address is controlled by the operating system, and writing style and contacts can still identify you.

**Everything else.** Peer-to-peer audio and video calls over WebRTC with signalling inside NIP-17 wraps, Lightning zaps, polls, threads, file sharing, a panic-wipe gesture, optional on-device encryption of the saved key with a password, PIN or passkey, and a built-in AI bot, Nymbot, whose private 1:1 mode is paid in Lightning credits.

**The backend.** The web app is static files plus Cloudflare Pages Functions run by the developer. According to the README and source, these act as a proxy for relays and media so third-party relays and servers see Cloudflare's addresses rather than users', generate link previews, run Nymbot, translate messages, filter spam, and store encrypted settings, purchases and an archive in Cloudflare's D1 database. The project states that relays and D1 only ever hold ciphertext for private messages and group chats. The relay pool also archives public channel events.

**Verifiable builds.** The web build is deterministic and attested by a GitHub Actions workflow, so anyone can rebuild a commit and compare its hash with the one the app's About dialog shows. Android builds published through [Zapstore](/kb/zapstore/) can be checked against the hash in the signed release event. The repository also publishes a signed warrant canary.

## What it protects against

- **Account-based identification.** No phone number, email or registration. A fresh session key is the default identity.
- **Reading of private messages by relays.** DMs and group chats are end-to-end encrypted. Between Nymchat users whose post-quantum keys are not derived from their Nostr key, the hybrid layer also covers "harvest now, decrypt later".
- **Relays mapping who talks to whom.** Gift wraps under one-time keys, randomised timestamps and rotating recipient keys in groups make relationship metadata harder to collect from relays.
- **Single-relay censorship.** Messages go to many community relays at once.
- **Internet shutdowns, locally.** The Bluetooth mesh keeps nearby phones talking with no infrastructure, together with Bitchat users. Browsers need a native phone nearby to relay for them.

## What it trusts, and the limits

- **"Ephemeral" does not mean unrecorded.** Public channel messages are plaintext on public relays, and anyone, including Nymchat's own relay pool, can store them. Treat channels as public broadcasts that may be archived.
- **The operator's backend.** When you use the hosted app, its Cloudflare infrastructure sees your IP address and the relay and media traffic it proxies. That hides you from third-party relays but concentrates the view in one company and one cloud provider. The hiding is not guaranteed either: if the proxy becomes unreachable, the web app's code automatically falls back to connecting directly to relays, which then see your real IP address. The README does not state retention periods for the archive. For maximum pseudonymity the project itself recommends Tor or a VPN paid for with cash or Monero.
- **Calls reveal your IP.** WebRTC calls connect directly, and the project warns that your real IP address may be visible to the other participants.
- **New cryptography, not independently audited.** The group-key rotation scheme and the post-quantum combiner are the project's own designs on top of Nostr standards. They are documented in detail and the ML-KEM code is tested against NIST vectors, but we found no published independent security audit.
- **One small vendor.** Development, the hosted web app, the backend and the app-store listings all run through one company. The AGPL source makes forks possible; the hosted conveniences do not move with them.
- **Self-verification has limits.** An About dialog that checks its own code is useful against a tampered mirror, but a compromised server could also serve a dialog that lies. The independent check is rebuilding from source.
- **Mesh metadata.** Without Ghost Mode, the device announces a stable identity to anyone in Bluetooth range, the same weakness documented for Bitchat.
- **Feature surface.** AI bots, payments, shops, translation and calls all add code and services to what you trust. A high-risk user should switch off what they do not need.

## Readiness

**Experimental.** Nymchat is actively developed, open source, unusually well documented, and available on the web, Android (Google Play and Zapstore) and iOS (App Store, with TestFlight builds). It is a lively way to join Bitchat's location channels and mesh from more devices, with a post-quantum layer on top of standard NIP-17 whose real strength depends on how each side's keys were created. Its custom cryptographic extensions are unaudited, it changes quickly, and the hosted backend is a central point of trust and visibility. For high-risk conversations, prefer a messenger with an audited protocol and a smaller trust surface; see [Choosing a private messenger](/kb/compare-messengers/).

## Primary sources

- Nymchat site and FAQ: https://nymchat.app/ · knowledge base: https://nymchat.app/docs/ · web app: https://web.nymchat.app/
- Source code, protocol notes and build verification (AGPL-3.0): https://github.com/Spl0itable/NYM
- Security policy and scope notes: https://github.com/Spl0itable/NYM/blob/main/SECURITY.md
- Warrant canary: https://github.com/Spl0itable/NYM/blob/main/canary.json
- Developer (21 Million LLC, Nostr Services): https://nostrservices.com/
- Zapstore listing: https://zapstore.dev/apps/com.nym.bar
- NIP-17 private direct messages: https://github.com/nostr-protocol/nips/blob/master/17.md · NIP-59 gift wrap: https://github.com/nostr-protocol/nips/blob/master/59.md · NIP-44 encryption: https://github.com/nostr-protocol/nips/blob/master/44.md
- ML-KEM (FIPS 203): https://csrc.nist.gov/pubs/fips/203/final
- Not this project: the archived Nym-mixnet nymCHAT, https://github.com/code-zm/nymCHAT
