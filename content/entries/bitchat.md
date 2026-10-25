---
title: "Bitchat"
slug: bitchat
type: deep-dive
pillars: [mesh, messaging]
readiness: experimental
description: "Bitchat is a phone-only messenger that relays encrypted chat over a Bluetooth mesh with no internet, and falls back to Nostr relays when a connection exists."
dek: "No accounts, no phone numbers, no servers: nearby phones form a Bluetooth mesh, and Nostr bridges separate meshes over the internet. A useful outage tool with honestly documented metadata weaknesses."
updated: 2026-10-23
created: 2026-04-25
origin: original
related: [briar, meshtastic, meshcore, reticulum, off-grid-messaging, off-grid-networks, internet-shutdown-preparedness, building-a-mesh, nostr-protocol, metadata-resistance, choosing-a-secure-messenger]
aliases: ["BitChat", "Bitchat Mesh"]
tags: ["bitchat", "ble-mesh", "bluetooth", "nostr", "off-grid", "messaging", "deep-dive"]
---

Bitchat is a peer-to-peer messenger for phones and laptops that works with or without the internet. Nearby devices discover each other over Bluetooth Low Energy (BLE) and relay messages for one another, forming an ad-hoc mesh with no servers, accounts or phone numbers. When a device does have a connection, private messages to trusted contacts and location-based public rooms travel over ordinary [Nostr](/kb/nostr-protocol/) relays, which bridges meshes that are far apart. It is published by permissionlesstech. The iOS/macOS app is released into the public domain (Unlicense). The Android app is fully protocol-compatible, but its repository's licence file is GPL-3.0, even though its README says public domain. The project started in July 2025 and ships native apps on the App Store, Google Play and GitHub releases.

## How it works

**Two transports, one router.** Every device is both a Bluetooth central and peripheral. A message router prefers a live mesh link and falls back to Nostr. If neither can deliver promptly, it hands the message to the store-and-forward layer.

**The Bluetooth mesh.** Packets use a compact binary format and are relayed by a controlled flood. They start with a TTL of 7 hops, which relays clamp to 5 in dense crowds. Relays add random jitter, suppress duplicates, and send broadcasts to only a subset of links. Each node gossips a list of its direct neighbours, so when a confirmed path exists, packets can be source-routed along it instead of flooded. Large packets are fragmented to fit BLE's small frames. On supported Android devices, Wi-Fi Aware adds a higher-bandwidth local link.

**Encryption.**
- *Live private chats* use a Noise `XX` handshake (Curve25519, ChaCha20-Poly1305, SHA-256), which gives mutual authentication and forward secrecy. Relays see only opaque ciphertext.
- *Mail for someone who is out of range* is sealed to the recipient's static key with the one-way Noise `X` pattern. It can be handed to up to three passing phones (**couriers**), which spread copies through a moving crowd in a "spray and wait" pattern and deliver when they meet the recipient. Couriers see only a recipient tag that rotates daily. They learn no sender, recipient or content.
- *Over Nostr*, messages between **mutual favourites** use Bitchat's own envelope: an XChaCha20-Poly1305 construction with secp256k1 ECDH, inside a gift-wrap-style kind `1059` event signed by a one-time key. The project states plainly that this reuses Nostr kind numbers but is **not** NIP-17, NIP-44 or NIP-59 compatible, so it works only between Bitchat clients. Relays hold these envelopes as mailboxes for 24 hours.
- *Public rooms* are signed broadcasts. Recent history (6 hours) is gossip-synced between phones, so someone who walks between two groups carries the conversation across. *Location channels* are public Nostr rooms scoped by geohash, from a city block up to a whole region.

**Identity.** Each device holds a Curve25519 key for Noise and an Ed25519 key for signing. The 8-byte peer ID shown on the mesh is derived from the Noise key. It is **stable** across sessions and reinstalls until you wipe. Favouriting pins a contact's key, and a QR code can verify a contact in person. Location channels use a separate key per geohash area.

**Safety features.** Triple-tap **panic wipe** erases keys, favourites, carried mail, the sealed outbox and history. The Android app includes Tor (Arti) for its internet traffic. The project publishes per-release hash manifests and reproducible Android builds. This matters because the repository has faced takedown demands, and unofficial mirrors cannot be verified.

## What it protects against

- **Network shutdowns and congested or absent cell service.** Chat keeps working among phones within Bluetooth range of each other, extended hop by hop and by people physically carrying mail.
- **Servers and accounts.** There is no operator to subpoena or suspend, and no phone number or email to link to you.
- **Reading by relays.** Mesh relays, couriers and Nostr relays carry only ciphertext for private messages.
- **Key compromise, for live sessions.** Noise forward secrecy protects past live chats.

## What it trusts, and the limits

The whitepaper is unusually candid that **metadata is the weakest part of the design**:

- **You are trackable by radio.** Every packet carries your stable peer ID. Announcements broadcast your nickname and static public keys in cleartext. Anyone with a receiver in range can count participants and follow a device from place to place. Announcements also list your direct neighbours, which hands a single sniffer the local contact graph, and hop counts reveal who originated a packet. Rotating on-air identities are listed as future work.
- **No forward secrecy for stored mail.** Courier envelopes and Nostr mailbox messages are sealed to static keys. If a recipient's key is later compromised, any retained ciphertext addressed to it can be decrypted.
- **Traffic sizes leak.** Only Noise frames are padded, so most traffic is sent at its natural length.
- **Nostr exposes the recipient.** The outer envelope's `p` tag shows relays the recipient's Nostr key, and location channels are public by design.
- **Media is not sealed at rest.** Accepted images and voice notes are stored protected by the operating system rather than by app-level encryption.
- **Security history.** Within days of launch in July 2025, researchers showed that unsigned announcements let anyone impersonate a nickname and man-in-the-middle a "secure" chat. Cure53 audited the apps in November 2025 (findings BCH-01, published as Android issues in January 2026). In June 2026 the iOS app fixed three critical and seven high findings from a further audit. These included forgeable Nostr DMs, which became a breaking wire change, public-message impersonation and identity-store poisoning. At the time of writing, two Cure53 findings are still open on Android: **nickname-based impersonation (High)** and **replay of announce packets (Medium)**. Verify fingerprints in person before trusting a contact.
- **Physics and platforms.** Bluetooth reaches roughly 10–100 m per hop, so the mesh needs a crowd. iOS limits background Bluetooth activity, and an always-on mesh costs battery.

## Bitchat beside other off-grid tools

| | Bitchat | [Briar](/kb/briar/) | [Meshtastic](/kb/meshtastic/) / [MeshCore](/kb/meshcore/) |
|---|---|---|---|
| Hardware | The phone you have | The phone you have | A separate LoRa radio |
| Range | Bluetooth, multi-hop (TTL 7) | Bluetooth / Wi-Fi peer-to-peer, plus Tor online | Kilometres per hop |
| Online path | Nostr relays | Tor | Optional MQTT / gateways |
| Live-chat forward secrecy | Yes (Noise XX) | Yes | No |
| Radio-layer tracking | Stable peer ID, cleartext announcements | Connects only to existing contacts | Node IDs broadcast |
| Platforms | iOS, macOS, Android | Android (desktop beta) | Radio plus phone app |

## Readiness

**Experimental.** It is easy to install, cross-platform, and in very active development, and the cryptography for live chats is sound. But the protocol is young and still changing: in June 2026 a fix broke wire compatibility between old and new versions. The project's own documentation lists serious metadata exposure on the radio layer. Audits have found critical flaws, and some findings are still open on Android. It works well as an outage, festival or protest backup channel among people who expect it. It is not the tool for high-risk conversations near a hostile listener. For those, [Briar](/kb/briar/) has the longer audit record. For kilometres of range, use LoRa ([Meshtastic](/kb/meshtastic/) or [MeshCore](/kb/meshcore/)).

For the wider comparison of online and off-grid choices, see [Choosing a private messenger](/kb/compare-messengers/).

## Primary sources

- Bitchat: https://bitchat.free/ · Whitepaper (v2.0, July 2026): https://github.com/permissionlesstech/bitchat/blob/main/WHITEPAPER.md
- iOS/macOS source: https://github.com/permissionlesstech/bitchat · Unlicense: https://github.com/permissionlesstech/bitchat/blob/main/LICENSE · Verifying a build: https://github.com/permissionlesstech/bitchat/blob/main/docs/VERIFYING-A-BUILD.md
- Android source: https://github.com/permissionlesstech/bitchat-android · Releases: https://github.com/permissionlesstech/bitchat-android/releases · Licence file (GPL-3.0): https://github.com/permissionlesstech/bitchat-android/blob/main/LICENSE.md · Reproducible builds: https://github.com/permissionlesstech/bitchat-android/blob/main/docs/reproducible-builds.md
- App stores: https://apps.apple.com/us/app/bitchat-mesh/id6748219622 · https://play.google.com/store/apps/details?id=com.bitchat.droid
- Security: Cure53 BCH-01 findings https://github.com/permissionlesstech/bitchat-android/issues?q=BCH-01 (open: https://github.com/permissionlesstech/bitchat-android/issues/589 and https://github.com/permissionlesstech/bitchat-android/issues/593) · June 2026 audit fixes https://github.com/permissionlesstech/bitchat/pull/1345 · Early impersonation flaw (SPR, July 2025) https://www.supernetworks.org/pages/blog/agentic-insecurity-vibes-on-bitchat
- Noise Protocol Framework: https://noiseprotocol.org/
