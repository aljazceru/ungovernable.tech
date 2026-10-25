---
title: "Encrypted Messaging"
slug: encrypted-messaging
type: explainer
pillars: ["messaging"]
description: "How end-to-end encrypted messaging works, what it protects, and why identifiers, servers and metadata decide how private a messenger really is."
dek: "Encrypted messaging makes sure only the intended recipients can read your communications."
updated: 2026-04-26
created: 2026-04-15
origin: vault
source: "07-Encrypted-Messaging/Overview - Encrypted Messaging.md"
aliases: ["End-to-End Encryption", "E2EE", "Secure Messaging"]
tags: ["encrypted-messaging", "e2ee", "signal", "matrix", "nostr", "communications"]
---

## What this section is about

Encrypted messaging makes sure only the intended recipients can read your communications. Not the platform, not your ISP, not anyone intercepting traffic. Modern E2EE goes beyond TLS to provide forward secrecy (compromise of a long-term key does not expose past session keys), post-compromise security (a compromised session heals after subsequent rounds), and varying degrees of metadata protection.

This section covers:

- Signal Protocol — the reference asynchronous E2EE design (X3DH/PQXDH + Double Ratchet + Sesame).
- Matrix — federated chat with Olm/Megolm; MLS profile in development.
- Nostr — public-key-rooted broadcast protocol; encrypted DMs via NIP-44, gift-wrapped DMs via NIP-17, group E2EE via [Marmot Protocol](/kb/marmot-protocol/) (MLS over Nostr).
- Metadata-resistant designs — SimpleX, Session, Cwtch, Briar.

> "Every company or individual is one court order away from needing to decide how long they are willing to spend behind bars for not sharing the data with the government." — Ungovernable.tech

## The metadata problem

Encryption protects content. Metadata often reveals more:

| Data type | Example | Risk |
|----------|---------|------|
| Who | Alice → Bob | Social graph |
| When | Timestamp | Pattern of life |
| Where | IP address | Location |
| How | Device, client | Fingerprinting |
| Size | Message length | Traffic analysis |

Truly private systems address metadata, not just content.

## Key technologies

### Signal Protocol

The reference for asynchronous E2EE messaging. Deployed by Signal, WhatsApp (default since April 2016), Google Messages RCS (since 2020), and Meta's Messenger and Instagram DMs (rolled out 2023-2024 using a Signal-Protocol-derived design).

Core components:

- Double Ratchet — per-message key evolution; forward secrecy plus post-compromise security.
- X3DH (Extended Triple DH) — asynchronous initial key agreement. Replaced in Signal by **PQXDH** (X25519 + ML-KEM-1024 hybrid) in late 2023.
- Sesame — session management for multi-device.

How it works:

1. Alice and Bob exchange long-term and one-time prekeys via the server.
2. PQXDH/X3DH derives an initial shared secret asynchronously.
3. Double Ratchet evolves a fresh key per message; compromise of any single key does not expose past or future messages.

Limitations:

- Signal app itself requires a phone number (metadata).
- Centralized servers (Signal, WhatsApp).
- Not metadata-resistant beyond sealed-sender for the recipient identifier.

### Matrix

A federated chat protocol with E2EE via Olm (1:1) and Megolm (groups).

Architecture:

- Homeservers store message history; users pick or self-host one.
- Bridges connect to IRC, Slack, Discord, XMPP, etc.
- E2EE is on by default for new private rooms since Element X / Matrix 2.0 (2022). Public rooms remain unencrypted by design.
- MLS profile (RFC 9420) in development to replace Megolm for groups.

Trade-offs:

- Pros: federated, open-source, rich room model, bridging.
- Cons: large per-user state, history-visibility trade-offs, server learns metadata (room membership, timing, device list).

### Nostr

"Notes and Other Stuff Transmitted by Relays" — a public-key-rooted protocol where the user *is* their secp256k1 keypair (npub/nsec, BIP-340 Schnorr). Public events (kind 1 notes, profile metadata, reactions) are signed but unencrypted by design — they're meant to be public posts. Encrypted communication uses dedicated event kinds.

Architecture:

- Keys: npub (public) / nsec (private), Schnorr over secp256k1.
- Relays: simple WebSocket message brokers; anyone can run one.
- Clients: any app that knows the protocol; clients verify signatures themselves.

Encryption layers:

| Use case | Mechanism | Notes |
|----------|-----------|-------|
| Public posts | Signed only | Public broadcast is the design goal |
| Direct messages (legacy) | NIP-04 — ECDH + AES-256-CBC | Deprecated; metadata leaks recipient |
| Direct messages (current) | NIP-44 v2 — secp256k1 ECDH → ChaCha20 + HMAC-SHA-256 | Versioned format with padding |
| Metadata-protected DMs | NIP-17 + NIP-59 gift-wrap | Wraps NIP-44 content in a randomly-keyed envelope; relays cannot link sender |
| Group messaging | [Marmot Protocol](/kb/marmot-protocol/) — MLS (RFC 9420) over Nostr | Forward secrecy + post-compromise security; KeyPackages kind 30443, gift-wrapped Welcomes kind 1059, encrypted group events kind 445 |

Trade-offs:

- Pros: censorship-resistant by relay redundancy; key-rooted identity (no phone, no server account); client and relay diversity; composes with Lightning zaps and other key-bound protocols.
- Cons: legacy DMs (NIP-04) leak who-talks-to-whom to relays; NIP-44 still leaks recipient pubkey unless wrapped in NIP-17; no built-in spam control; relay discovery is application-defined.

Resources:

- [NIPs](https://github.com/nostr-protocol/nips) — protocol specs (active list)
- [awesome-nostr](https://github.com/aljazceru/awesome-nostr) — curated client/relay list
- [Marmot Protocol](/kb/marmot-protocol/) — MLS group E2EE over Nostr
- [Nostr Deep Dive](/kb/nostr-protocol/) — protocol internals

### SimpleX

A messaging protocol designed for metadata resistance. Detailed in [SimpleX](/kb/simplex/).

Features:

- No global user identifiers — addressable by per-conversation queue addresses on relay servers.
- Onion-routed connections to relays (with optional Tor).
- No address-book correlation; the recipient's invite link is delivered out of band.

Trade-offs:

- Pros: relays cannot link conversations to a single user; no social graph centralized anywhere.
- Cons: still requires out-of-band invite delivery; smaller ecosystem; UX cost of no contact discovery.

### Session

X25519-keypair identity; no phone number, no email. Onion-routed over the Oxen Service Node network ([Session](/kb/session-messenger/)). Originally a Signal Protocol fork; replaced X3DH with a simpler onion-routed handshake; still uses Double Ratchet for direct messages. Group encryption is migrating to MLS-style designs in 2024-2026. Funded by the $OXEN token (a real critique line).

### Cwtch

Tor v3 onion services as messaging substrate ([Cwtch](/kb/cwtch/)). Each user runs an onion service; conversations are direct hidden-service-to-hidden-service. Group servers are untrusted relays — they see encrypted blobs, not content or membership. Built by Open Privacy Research Society with explicit metadata-resistance research grounding.

### Wire (MLS)

Wire is a Swiss / German enterprise messenger and the canonical production reference deployment of MLS (RFC 9420), alongside Cisco Webex ([Wire MLS](/kb/mls-wire/)). Distinct cryptographic lineage from Signal — Wire's earlier Proteus protocol ran in parallel for a decade before the MLS migration in 2022.

## Network comparison

| Protocol | Metadata | Decentralized | E2EE | Open source |
|----------|---------|-------------|-------|------------|
| Signal | Poor (phone number) | No | Yes (PQXDH + Double Ratchet) | Yes (clients + server) |
| WhatsApp | Poor (phone number) | No | Yes (Signal Protocol since 2016) | Closed-source clients; protocol documented |
| Matrix | Moderate (server learns metadata) | Yes (federated) | Default-on for private rooms (Olm/Megolm) | Yes |
| Nostr | Mixed — public posts are public; DMs depend on NIP used | Yes (relay-based) | Public posts: no (by design). DMs: NIP-44 / NIP-17. Groups: [Marmot Protocol](/kb/marmot-protocol/) (MLS) | Yes |
| SimpleX | Good (no user IDs) | Partial (relays + clients) | Yes (Double Ratchet) | Yes |
| Session | Good (no phone, onion-routed) | Yes (Oxen service nodes) | Yes (post-2023 group MLS-style; 1:1 lacks PFS) | Yes |
| Briar | Good (Tor + LAN + BLE + USB transports) | Yes (peer-to-peer) | Yes (BTP, Bramble) | Yes |
| Cwtch | Good (Tor v3 hidden services) | Yes (peer-to-peer) | Yes | Yes |

## Clients

### Centralized E2EE

| Client | Platform | Protocol | Notes |
|--------|----------|---------|-------|
| Signal | All | Signal Protocol | Reference implementation |
| WhatsApp | All | Signal Protocol | Default-on E2EE since 2016 |

### Federated / decentralized

| Client | Platform | Protocol | Notes |
|--------|----------|---------|-------|
| Element / Element X | All | Matrix | Reference Matrix client; Element X is the current rewrite |
| Damus | iOS, macOS | Nostr | Largest iOS Nostr client |
| Primal | iOS, Android, web | Nostr | Reads + DMs + zaps; Primal cache server optional |
| Amethyst | Android | Nostr | Most full-featured Android client |
| Nostur | iOS | Nostr | Long-running iOS Nostr client |
| Coracle | Web | Nostr | Web-first; experimental NIPs |

### Metadata-resistant

| Client | Platform | Protocol | Notes |
|--------|----------|---------|-------|
| SimpleX Chat | All | SimpleX | No user IDs; per-queue routing |
| Session | All | Session / Oxen | Onion-routed; X25519 identity |
| Cwtch | All | Tor v3 hidden services | Peer-to-peer over Tor |
| [Briar](/kb/briar/) | Android, desktop (alpha) | Bramble (BTP/BSP/BQP) | Tor + Bluetooth + Wi-Fi LAN + USB |

## Evidence at a glance

| Technology | Maturity | Evidence |
|------------|----------|----------|
| Signal Protocol | Production | Billions of users via Signal/WhatsApp |
| Matrix (Olm/Megolm) | Production | Active development; matrix.org + thousands of homeservers |
| Nostr | Production | Active relay ecosystem; multi-million npubs published |
| Marmot Protocol (MLS over Nostr) | Active | Spec stable; reference implementations shipping |
| SimpleX | Production | ~250K users (2024 audit by Trail of Bits + Galois) |
| Session | Production | Oxen network live since 2020 |
| Briar | Production | F-Droid + Play Store; long-running Tor-based design |

## Trade-offs

### Strengths

- Content privacy — only sender and receiver can read.
- Forward secrecy and post-compromise security in Signal-family designs.
- Censorship resistance via relay redundancy (Nostr) or transport diversity (Briar).
- Self-sovereign identity (Nostr, Pubky, did:key).

### Limitations

- Metadata leaks — most platforms still expose *who* and *when* to the server or relay.
- Endpoint compromise — E2EE does not help if the device is malware.
- Identity binding — verifying that a key belongs to the intended human is out-of-band work.
- Jurisdiction — app-store and provider availability varies.

Two newer MLS-based projects on Nostr identities: [White Noise](/kb/white-noise/), a relay-native messenger built on Marmot, and [Cordn](/kb/cordn/), group messaging through a coordinator you can run yourself.

For a current comparison of identifiers, metadata, encryption defaults and readiness, see [Choosing a private messenger](/kb/compare-messengers/). Additional entries cover [Delta Chat](/kb/delta-chat/), [XMPP with OMEMO](/kb/xmpp-omemo/), [Jami](/kb/jami/), [Tox](/kb/tox/), [Quiet](/kb/quiet/) and [Veilid](/kb/veilid/).
