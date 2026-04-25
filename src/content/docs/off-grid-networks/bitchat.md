---
title: "Bitchat"
tags:
  - "bitchat"
  - "ble-mesh"
  - "bluetooth"
  - "nostr"
  - "off-grid"
  - "messaging"
  - "deep-dive"
---
*Bluetooth-LE mesh messaging with a Nostr fallback for global reach. No accounts, no phone numbers, no servers. IRC vibes for a world that occasionally loses internet.*

---

## What Bitchat is

Bitchat (by [Permissionlesstech](https://github.com/permissionlesstech)) is a peer-to-peer messenger built around two complementary transports:

1. Bluetooth LE mesh: nearby devices discover each other and relay messages across up to seven hops. Works fully offline.
2. Nostr: when internet is available, geohash-coded "location channels" route through the global Nostr relay network for wider reach.

Same client, same UX, transport selected automatically. Released into the public domain; native apps for iOS, macOS, and Android.

It occupies a distinct niche from the rest of the section:

- More consumer-friendly than [Briar](/off-grid-networks/briar) (App Store install vs. F-Droid hand-holding).
- More localized than [Reticulum](/off-grid-networks/reticulum) or [FIPS](/off-grid-networks/fips) (Bluetooth-range first-class).
- Different trust assumption from [Meshtastic](/off-grid-networks/meshtastic) (no shared-channel-key model; per-pair Noise sessions).
- Native Nostr integration: geohash channels, NIP-17 gift-wrap for Nostr-side DMs, ephemeral keys per geohash area.

---

## Architecture

### Bluetooth LE mesh (offline)

- Discovery: automatic GAP advertisement; peers announce and connect over LE.
- Relay model: every device is a router; messages forward through up to seven hops.
- Encryption: Noise Protocol (Noise XX-style handshake) per pair, with forward secrecy.
- Wire format: compact binary protocol tuned for BLE's MTU and bandwidth limits; LZ4 compression on payloads.
- Battery model: adaptive duty-cycling. Phones in low-power mode advertise less aggressively while staying reachable.

### Nostr (online)

- Geohash channels: `block #dr5rsj7`, `neighborhood #dr5rs`, `city #dr5r`, `country #dr`, etc. The geohash precision determines the channel's geographic scope.
- 290+ relay network: connects to many public Nostr relays for redundancy.
- NIP-17 gift-wrapped DMs for the online direct-message path.
- Ephemeral keys per geohash area to limit cross-area linkability.

### Transport selection

For a direct message:

1. If a Bluetooth Noise session is open with the recipient, use it.
2. Otherwise, fall back to Nostr if the recipient publishes a reachable Nostr identity.
3. Otherwise, queue.

Effects: in a crowded venue, Bluetooth carries everything cheaply; outside venues, Nostr extends reach; in an internet outage, only Bluetooth-reachable peers receive.

---

## Identity model

- No phone number, no email, no account.
- Ephemeral identity per device session for mesh, with optional persistence.
- The Nostr-side identity is a generated keypair, used only within the geohash flow (ephemeral keys per area).
- No persistent global identifier by default. Closer to "chat alias" semantics than to [Nostr](/identity/nostr)'s identity-as-key model.

For users who want persistent identity, the Nostr-side ephemeral pattern is a deliberate trade-off: it limits cross-context linkability at the cost of reputation continuity.

---

## Cryptography

### Mesh

- Noise Protocol Framework for handshake and session encryption.
- Forward secrecy via Noise's ephemeral keys.
- Per-pair sessions, no shared channel keys (vs. [Meshtastic](/off-grid-networks/meshtastic)'s default model).

### Nostr

- NIP-44 cipher for content.
- NIP-17 / NIP-59 gift-wrap for metadata-protected DMs.
- Ephemeral signing keys per geohash area for sender unlinkability across areas.

### Emergency wipe

Triple-tap to clear all data on the device: sessions, message history, ephemeral keys. A common feature in adversarial-threat-model messengers (Briar has equivalents).

---

## IRC-style commands

Bitchat's UX leans into IRC nostalgia:

```
/slap <user>
/msg <user> <text>
/who
/join <channel>
/me <action>
```

This is a reasonable choice for a hyper-local mesh: small set of users, shared geographic context, command-driven UX is information-dense.

---

## Comparison

| Dimension | [Bitchat](/off-grid-networks/bitchat) | [Meshtastic](/off-grid-networks/meshtastic) | [Briar](/off-grid-networks/briar) | [Reticulum](/off-grid-networks/reticulum) |
|-----------|-------------|----------------|-----------|---------------|
| Transport | BLE mesh + Nostr | LoRa | Tor + BLE + Wi-Fi-direct | Anything (LoRa, TCP, BLE) |
| Range per hop | Bluetooth (~10-100 m) | LoRa (1-30 km) | Bluetooth (~10-100 m) for offline | Transport-dependent |
| Max hops | 7 | Configurable | 1 (P2P) | Bounded by RNS path-table |
| Hardware | Phone (built-in BLE) | Dedicated LoRa device | Phone | Phone, Pi, RNode, etc. |
| Encryption | Noise (mesh), NIP-44 (Nostr) | AES-256-CTR per channel | Noise/AES | Curve25519 + AES-256 |
| Forward secrecy | Yes (Noise) | No | Yes (Noise) | Yes |
| Identity | Ephemeral / no persistent | Hardware ID + key | Local keypair, manual exchange | Identity destinations (key) |
| Online fallback | Nostr (built-in) | MQTT bridge | Tor | Reticulum-over-TCP |
| Platforms | iOS, macOS, Android | LoRa hardware + phone | Android primarily | Cross-platform |
| Threat model | Censorship + surveillance + outage | Outage + local privacy | Hostile network + surveillance | Adversarial mesh + privacy |

---

## When to use Bitchat

- Crowded venues, conferences, protests. Phone-only, no extra hardware. Local mesh comes up in seconds.
- Internet-shutdown regions where some users still have phones.
- Local-community chat with a Nostr-backed online tier when participants leave the building.
- Backup channel during events where conventional messengers fail (cell network congestion, deliberate shutdown).

When not to use Bitchat:

- Long-range deployments. Bluetooth's range is fundamentally short. Use [Meshtastic](/off-grid-networks/meshtastic) or [Reticulum](/off-grid-networks/reticulum) over LoRa.
- High-stakes activist comms. [Briar](/off-grid-networks/briar) has been hardened by audit and has a more conservative threat model.
- Persistent pseudonymous identity. Bitchat's ephemeral-by-default conflicts with reputation continuity. Use plain [Nostr](/identity/nostr).

---

## Trade-offs

### Strengths

- Truly phone-only. No extra hardware, native apps on iOS/macOS/Android.
- Multi-hop mesh. Seven hops over BLE actually reaches across a venue.
- Hybrid transport. Bluetooth for the local case, Nostr for global reach. Same client.
- Public domain, no licensing friction.
- Performance work: LZ4 compression, adaptive batteries, optimized BLE packet format.
- NIP-17 gift-wrap: metadata protection on the Nostr side, not just content.

### Limitations

- Bluetooth range: 10-100 m per hop, which fundamentally limits local geography.
- Battery cost of always-on BLE advertisement.
- Ephemeral identity by default limits reputation continuity.
- Newer codebase, less audit history than [Briar](/off-grid-networks/briar).
- Bluetooth fingerprinting: BLE MAC addresses leak some identity unless properly randomized.
- iOS BLE constraints: Apple's background-execution model limits how aggressively the mesh can run.

---

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Hop relay misbehavior | Noise per-pair encryption; relays see only ciphertext |
| BLE MAC tracking | Random / rotating MAC addresses (OS-supported) |
| Geohash channel cross-correlation | Ephemeral keys per geohash area |
| Lost / seized device | Emergency triple-tap wipe |
| BLE protocol-level exploits | iOS/Android stack hardening; firmware updates |
| Sybil at mesh layer | Limited; per-pair Noise sessions can't be flooded blindly |
| Endpoint compromise | Out of scope; standard hygiene |
| Quantum (future) | Curve25519-based; PQ migration not yet specified |

---

## Composition

Bitchat fits into the broader vault:

- Pair with [Briar](/off-grid-networks/briar) for higher-stakes activist work: Bitchat for local, Briar for adversarial backbone.
- Pair with [Meshtastic](/off-grid-networks/meshtastic) in disaster-resilience kits: LoRa for kilometers, Bitchat for in-venue.
- Pair with [Nostr](/identity/nostr) identity. Although Bitchat defaults to ephemeral, advanced users can bind to a persistent npub for cross-app continuity.
- In-venue plus [Lightning Network Deep Dive](/financial-sovereignty/lightning-network-deep-dive): Bluetooth-mesh chat with Lightning zaps over an MQTT bridge or Nostr fallback.

---

## Recent developments (2024-2026)

- Public-domain release with native iOS / macOS / Android.
- Nostr fallback: second transport added, geohash channel design.
- Performance work: LZ4 compression, adaptive battery modes, optimized packet format.
- Community forks including beechat (karnagebitcoin) and a Flutter port (bitchat-flutter).

---

## Related files

- [Overview - Off-Grid Networks](/off-grid-networks)
- [Meshtastic](/off-grid-networks/meshtastic)
- [Reticulum](/off-grid-networks/reticulum)
- [Briar](/off-grid-networks/briar)
- [FIPS](/off-grid-networks/fips) — Nostr-keyed mesh routing (different scope)
- [Off-Grid Messaging](/encrypted-messaging/off-grid-messaging)
- [Nostr Deep Dive](/encrypted-messaging/nostr-deep-dive) — Bitchat's online transport
- [Glossary](/meta/glossary) — Noise Protocol, NIP-17, geohash

---

## Primary sources

- Bitchat — [bitchat.free](https://bitchat.free)
- Source — [github.com/permissionlesstech/bitchat](https://github.com/permissionlesstech/bitchat)
- Technical wiki — [deepwiki.com/permissionlesstech/bitchat](https://deepwiki.com/permissionlesstech/bitchat)
- Noise Protocol Framework — [noiseprotocol.org](https://noiseprotocol.org/)
- NIP-17, NIP-44, NIP-59 — [github.com/nostr-protocol/nips](https://github.com/nostr-protocol/nips)
- Geohash — [en.wikipedia.org/wiki/Geohash](https://en.wikipedia.org/wiki/Geohash)

