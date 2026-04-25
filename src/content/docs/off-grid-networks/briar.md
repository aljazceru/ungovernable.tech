---
title: "Briar"
tags:
  - "briar"
  - "p2p"
  - "e2ee"
  - "tor"
  - "bluetooth"
  - "off-grid"
  - "messaging"
  - "deep-dive"
---
*Peer-to-peer messaging built for the worst conditions: internet shutdowns, hostile networks, disrupted mesh. The same client switches between Tor, Bluetooth, and Wi-Fi-direct transparently.*

---

## Design goals

Briar inverts the standard messenger architecture. Instead of "chat with reachable contacts via a central server", it asks "what comms remain possible when every layer is hostile?". The answers shaped the design:

- No accounts. Identity is local. There is no server-stored profile to subpoena.
- No phone number, no email. Contacts are added by exchanging QR codes or by mediated introductions.
- Four sync transports: Tor (when internet works), Bluetooth, Wi-Fi (LAN or mobile hotspot), and removable media (USB, SD). Same client, transparent switching.
- No metadata at the server. Direct peer-to-peer; nothing to log.
- Forums and blogs work offline. Briar's group features replicate via gossip rather than centralized publishing.

The reference users are journalists, activists, and crisis responders in hostile environments. The threat model is a state-level adversary actively interrupting the network.

---

## Identity and contact establishment

Each Briar account generates a long-term Ed25519 keypair locally. The public key is the contact-list entry.

Adding a contact requires out-of-band key exchange, typically scanning a QR code in person. There is no Signal-style server-mediated discovery. The trade-off: phishing-proof contact, friction for the first introduction.

Once added, contacts are reachable over whichever transport currently works.

---

## Transports

### Tor (default when internet works)

Each Briar instance hosts a Tor v3 hidden service. Contacts connect to one another via these hidden services. Properties:

- IP not visible to either side.
- Connection works through any NAT or firewall that allows Tor.
- Both peers must be online concurrently for direct delivery (or via Briar Mailbox; see below).
- Tor is sufficient on its own for basic operation.

### Bluetooth

When in physical proximity, Briar can sync directly over Bluetooth. No internet required. Two phones in a building or a backpack can pass messages, attachments, and forum posts.

### Wi-Fi (LAN / mobile hotspot)

Higher bandwidth than Bluetooth. Briar accepts connections over a shared LAN or via one device acting as a Wi-Fi hotspot for the other.

### Removable media (USB / SD)

Sneakernet sync. Briar can write its outbox to removable media for hand-carried delivery. Useful when no other transport works (deep adversarial conditions, air-gapped recipients).

The client probes all available transports; messages get through whichever first succeeds. A user moving from a city (Tor) into a building with no internet (Bluetooth or Wi-Fi LAN) experiences continuous service.

---

## Briar Mailbox

The async-delivery problem: if both peers are not online at the same time, direct delivery fails. Briar Mailbox is a separate, single-purpose Android app that runs on a spare device (an old phone left at home, ideally on a UPS).

- Peers deliver messages to your mailbox over Tor.
- You sync from the mailbox when you next connect.
- The mailbox sees only opaque ciphertext, encrypted under your contact's keys, not the mailbox's.
- The mailbox doesn't learn the message, the sender, or the recipient pair (it only knows it's holding stuff for "you").

This recovers Signal-like asynchronous semantics without a server fleet.

---

## Forums and blogs

Briar groups synchronize via gossip: when you connect to any contact who is also a member, the latest forum state replicates between you. No central server holds the forum.

Effects:

- Eventually consistent; recent messages may not be immediate everywhere.
- Member set determines reach; a forum with one member is invisible to non-members.
- Survives total internet outage; Bluetooth-only sync between members keeps the forum alive.

Blogs work the same way: each user has their own append-only blog, replicated to subscribers via gossip.

---

## Cryptography

- Ed25519 for identity and authentication.
- Curve25519 ECDH for session keys.
- AES-256-GCM for bulk encryption.
- BQP key agreement (Bramble's contact-protocol) for the contact-establishment ceremony.
- Forward secrecy via per-session ephemeral keys.
- Recent (post-2023) work on post-quantum hybrid handshakes (research-stage in 2026).

Storage is encrypted with a passphrase-derived key. The passphrase is the only way back into a Briar account; there is no recovery.

---

## What Briar doesn't do

- Voice / video. Text and small attachments only. The threat model and constraints don't favor real-time media.
- Multi-device. A single account is bound to a single device. Migration via export/import (encrypted backup).
- Discovery. No directory; no search. Contacts are added intentionally.
- Federation. Pure P2P; not a server-based protocol.

---

## Threat model

| Adversary | Defended? |
|-----------|-----------|
| ISP / state-level network adversary | Yes; Tor for backbone, Bluetooth/Wi-Fi for radio fallback |
| Server compromise | N/A; no server |
| Phone seizure (without passphrase) | Yes; passphrase-encrypted storage |
| Phone seizure (with passphrase coercion) | Limited; duress wallet patterns not built in |
| Network shutdown | Yes; Bluetooth and Wi-Fi-direct |
| Side-channel on radio | Partial; short-range only, harder DF than LoRa beacons |
| Endpoint malware | No; same as everywhere |

---

## Trade-offs

### Strengths

- Three transports plus transparent switching. Survives internet shutdowns.
- No metadata server. Nothing to subpoena.
- No accounts. Identity local; recoverable from backup with passphrase.
- Forums work offline via gossip.
- Open source, Free Software. Auditable.
- Designed for hostile environments, not retrofitted.

### Limitations

- Mobile-first, Android-primary. A desktop client (briar headless / desktop) exists; iOS is unsupported (Apple's restrictions on Tor and background networking).
- Manual contact establishment. No discovery means deliberate introduction every time.
- Smaller user base than mainstream messengers. Network effects favor Signal/Telegram/etc.
- Battery cost of always-on Tor.
- Single-device binding. No history sync across phones.
- No voice or video.

---

## Operational patterns

### Activist comms

```
Phone with Briar → Tor (when internet works)
                 → Bluetooth (when internet shut down)
                 → Wi-Fi-direct (in groups, room-scale)
```

Pre-arranged: distribute QR codes in person. Set up a Briar Mailbox on a spare phone at a safe location. Use forums for group coordination.

### Journalism / source contact

The source uses a fresh Briar identity on a clean phone. The journalist receives via Briar Mailbox. No server logs the contact.

For higher-stakes scenarios (whistleblower, classified material): pair Briar with SecureDrop for asynchronous large-document submission, and Briar for ongoing communication.

### Disaster comms

In a regional internet outage, two Briar phones in the same building sync over Bluetooth. As mesh density grows, gossip carries forum updates across users.

---

## Recent developments (2024-2026)

- Briar Desktop: JavaFX-based stable client; cross-platform.
- Briar Mailbox: production for Android; consumer-friendly setup.
- Hybrid post-quantum handshake research.
- Native Tor in client: improved bootstrap and bridge support.
- Forum scalability improvements.

---

## Related files

- [Overview - Off-Grid Networks](/off-grid-networks)
- [Off-Grid Messaging](/encrypted-messaging/off-grid-messaging)
- [Metadata Resistance](/encrypted-messaging/metadata-resistance)
- [Overview - Encrypted Messaging](/encrypted-messaging)
- [Overview - Mix Networks](/mix-networks)

---

## Primary sources

- Briar Project — [briarproject.org](https://briarproject.org)
- Source — [code.briarproject.org/briar](https://code.briarproject.org/briar)
- Briar Protocol Specification — *Bramble, Briar's transport protocol*.
- Mailbox documentation — [briarproject.org/manual/mailbox](https://briarproject.org/manual/mailbox)
- Open Technology Fund audits.

