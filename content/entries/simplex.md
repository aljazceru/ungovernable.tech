---
title: "SimpleX Chat"
slug: simplex
type: deep-dive
pillars: ["messaging"]
readiness: usable
description: "SimpleX Chat, a messenger with no user identifiers at all: one-way message queues on relays you can choose or run, and what that hides."
dek: "A messenger built on a bet that the user-identifier is the wrong primitive: instead of \"user has a phone number / npub / pubkey, contacts route to that,\" each conversation gets its own pair of unidirectional queue addresses on relay servers, and a user has no global identifier at all. Relays cannot link conversations to a single user. Double Ratchet still encrypts content; the architectural innovation is what's removed, not what's added."
updated: 2026-10-25
created: 2026-04-26
origin: vault
source: "07-Encrypted-Messaging/SimpleX.md"
aliases: ["SimpleX Chat", "SimpleX Network", "SMP", "XFTP"]
tags: ["simplex", "smp", "xftp", "e2ee", "metadata-resistance", "double-ratchet", "queue-based", "deep-dive"]
---

## What SimpleX is doing differently

Most messengers — Signal, WhatsApp, Matrix, Session, even Nostr — give every user a single identifier (phone number, account, public key, npub) that all their contacts route to. The server / relay sees inbound traffic concentrated at that identifier and can build a social graph from connection patterns even if it can't read content.

SimpleX rejects that primitive. There is no "@alice" or `npub1...alice...`. Instead:

- Alice and Bob each run a client.
- For each contact pair, they create **two unidirectional queues** on SMP relays.
- Each queue is a per-conversation address (a long random string) hosted on some relay.
- Messages from Alice to Bob land in one queue; messages from Bob to Alice in another.
- Different conversations use different queues, often on different relays.

A relay watching its queues sees: "queue ABC123 received a 487-byte ciphertext at 12:33:14." It does not see "Alice sent this," and it cannot link queue ABC123 to queue DEF456 (Alice's other conversation) because Alice has no identifier the relay knows.

The protocol that talks to relays is **SMP** (Simplex Messaging Protocol). File transfers use **XFTP** (XFTP, "X File Transfer Protocol"), a similar queue-oriented transfer protocol with chunking and rotating addresses.

This is a strong threat model claim, and a real architectural commitment: there is no user database, ever, on any relay.

## Architecture

```
┌──────────────┐                                 ┌──────────────┐
│ Alice client │                                 │  Bob client  │
└──────┬───────┘                                 └──────┬───────┘
       │                                                │
       │   Send to Bob's queue on relay R1              │
       ├───────────────────────────────────────────────►│
       │                                                │
       │             Receive from Alice's queue on R2   │
       │◄───────────────────────────────────────────────┤
       │                                                │
       │  (each queue lives on whichever relay was      │
       │   chosen at conversation-creation time)        │
```

Components:

- **Client.** Holds long-term identity keys *that are never published to any server*. Holds Double Ratchet state per conversation. Holds the list of queues for each contact.
- **SMP relay** (server). Stores per-queue messages, accepts subscriptions, expires old data. Stateless about users.
- **XFTP server.** Same model for file blobs.

There are no accounts to register. Installing a fresh client and creating a fresh contact link is the entire onboarding. Identity is per-device until the user explicitly migrates it.

## Cryptography

- **Double Ratchet** for content (the same X3DH-then-Symmetric-Ratchet + DH-Ratchet design as Signal, with SimpleX-specific key agreement at session setup).
- **Curve25519** for long-term identity and ephemeral keys.
- **NaCl crypto_box** primitives for queue authorization (each queue has a signing key for the recipient).
- **Post-quantum** key agreement: SimpleX added a hybrid Kyber-based handshake in late 2023 / early 2024. As of 2026 SimpleX is one of the few production messengers with a PQ option enabled by default for new conversations. (Signal added PQXDH in 2023 for direct messages; SimpleX is in similar territory.)

What SimpleX does *not* do cryptographically novel: the content encryption is conventional Signal-Protocol-style. The novelty is in identity and routing, not in the ratchet itself.

## Connection establishment

SimpleX has no directory. Two users connect by exchanging a one-time **invitation link** out-of-band. The invitation contains:

- A queue address on a chosen SMP relay.
- An ephemeral key.
- Optional metadata (display name suggestion, etc.).

The mechanics:

1. Alice creates an invitation. Her client sets up an empty queue on a relay.
2. Alice gives Bob the link (via QR code, signal flare, scrap of paper, another messenger, etc.).
3. Bob's client connects to the queue, sends its own queue address back, and the two clients run a handshake to derive Double Ratchet root keys.
4. From that point on, Alice and Bob have a paired conversation with two queues; the original invitation queue is discarded.

This is the threat-model honesty point: **invitation-link delivery is out of SimpleX's threat model**. If you send your invite link via WhatsApp, the WhatsApp servers know you and Bob are about to be connected. SimpleX protects everything *after* invitation delivery; the invitation itself needs a separate trust path (in person, over a different secure channel, printed and hand-delivered).

For ongoing relationships you can also use **contact addresses** — long-lived, multi-use addresses you publish (e.g. on a website) so anyone can request to connect. The cost: a slightly weaker unlinkability story for that specific address.

## Relays and decentralization

SimpleX maintains preset relays (operated by SimpleX Chat Ltd.) that new clients use by default. Self-hosting is straightforward: the [github.com/simplex-chat/simplexmq](https://github.com/simplex-chat/simplexmq) server is a single Haskell binary, runs on a $5 VPS, and clients can be configured to use arbitrary relay sets.

In practice users tend to keep a mix: some preset relays, some self-hosted, distributed across jurisdictions and operators. A queue lives on whichever relay was chosen when the conversation was created; nothing forces all of a user's queues onto the same relay.

This gives SimpleX a federation-by-disposition story rather than a federation-by-protocol-design story like Matrix. There's no consensus, no homeserver federation, just relays a client happens to use.

## Comparison

| Property | Signal | Session | SimpleX | Briar |
|----------|--------|---------|---------|-------|
| User identifier | Phone number (or username, 2024+) | Curve25519 pubkey | None (per-conversation queues) | TLS pubkey + Tor onion |
| Server can build social graph | Limited (sealed sender helps) | No (onion routing) | No (no user identifier) | No (peer-to-peer over Tor / BLE) |
| Online presence | Asynchronous via servers | Asynchronous via storage relays | Asynchronous via SMP queues | Both peers must be online (or via Tor mailbox) |
| Bootstrap | Phone-number contact discovery | QR / Session ID | Out-of-band invitation link | Pairing in person or via mailbox |
| Forward secrecy | Yes (Double Ratchet) | Yes (Double Ratchet) | Yes (Double Ratchet) | Yes (BTP) |
| PQ key exchange | PQXDH (2023+) | No public deployment | Hybrid Kyber (2023+) | No |
| Self-hostable | No (Signal-server is open but the network is closed) | Service-node operators | Yes (relays) | N/A |
| Phone number | Required (or username for handles) | No | No | No |

The honest comparison: SimpleX and Session both target the metadata problem more aggressively than Signal. They differ in mechanism — Session uses onion routing and a global user-pubkey identifier; SimpleX uses queue-based routing and no user identifier. Briar is a different beast (peer-to-peer over Tor, presence-aware) for a different threat model.

For metadata resistance with mainstream usability and a usable iOS client, SimpleX in 2026 is the strongest practical option in this group.

## Threat model

### What SimpleX prevents

- **Server-side social graph reconstruction.** Even a malicious or compromised relay sees disconnected per-conversation queues, no user-pinning, no inter-conversation linkability.
- **User enumeration.** No global directory, no phone-number lookup, no Sybil-easy account harvesting.
- **Plaintext in transit.** Standard E2EE on every message.
- **Persistence of message content on relays.** Messages are deleted on delivery (or after a configurable TTL); no message archive.

### What it doesn't prevent

- **Endpoint compromise.** Same as everywhere — the device holds plaintext.
- **Network-level traffic analysis.** A passive observer between Alice and a relay sees Alice's IP. Use a VPN or Tor (SimpleX has built-in SOCKS support) to hide IPs.
- **Compromise of the invitation channel.** If an adversary intercepts the invite link, they can connect *as Bob*. This is why out-of-band delivery matters.
- **Simultaneous multi-relay observers.** A coordinated adversary running every SMP relay Alice uses could correlate traffic to Alice's IPs across queues if she does not Tor-route. SimpleX recommends Tor for this case.

The team has been honest in their published threat model documentation about the invitation-link issue and the IP-observability issue. Treat SimpleX as: strong protection of social graph against operator, weaker protection against a network-position adversary unless combined with Tor.

## Audits and provenance

- **Trail of Bits — 2022 audit** of the SimpleX Chat clients and SimpleX Messaging Protocol implementation. Findings published; fixes shipped. ([report](https://simplex.chat/blog/20221108-simplex-chat-v4.2-security-audit-by-trail-of-bits.html))
- **Trail of Bits — 2024 audit** of the cryptographic protocols including the post-quantum handshake. Limited findings; addressed in releases.
- Independent cryptographic review of the post-quantum design has appeared in 2024 reports; ongoing.

The audit cadence is real and the company publishes results. That puts SimpleX above most niche messengers in transparency, though Signal still has a longer audit history.

## Deployment

- **Clients**: SimpleX Chat for iOS, Android, macOS, Linux, Windows. Reproducible builds for desktop. F-Droid for Android.
- **License**: AGPL-3.0 for the network components, MPL-2.0 for clients.
- **Funding**: SimpleX Chat Ltd. (UK), partly grant-funded (NLnet / NGI Zero), partly venture funding (2023 round).
- **Users**: hard to pin since there is no account database. Public statements and download counts suggest **on the order of 200K-500K active users in 2025-2026**. Treat that range as "small but growing, far below Signal."

## Operational notes

- Use the built-in Tor support if your network adversary worries you. SimpleX runs over SOCKS to a local Tor instance; queues remain reachable.
- Self-host an SMP relay if you want a stable, jurisdiction-controlled queue host. Make sure clients configure it as part of their preset list.
- Rotate contact addresses for high-risk public connect points; per-conversation queues already rotate.
- **Groups** are fully decentralized: each client stores the group profile and its pairwise connections to other members. An inviting member introduces a newcomer to existing members and forwards messages while their connections are established. Relays carry the connections’ queues; the protocol does not define a relay-owned group membership list or a shared sender-key group.

## Primary sources

- [SimpleX Chat protocol: decentralized group design](https://simplex.chat/docs/protocol/simplex-chat.html)

- SimpleX whitepaper — [simplex.chat/docs/protocol/simplex-chat.html](https://simplex.chat/docs/protocol/simplex-chat.html).
- SimpleX Messaging Protocol (SMP) — [simplex.chat/docs/protocol/simplex-messaging.html](https://simplex.chat/docs/protocol/simplex-messaging.html).
- XFTP — [simplex.chat/docs/protocol/xftp.html](https://simplex.chat/docs/protocol/xftp.html).
- Source repositories — [github.com/simplex-chat](https://github.com/simplex-chat).
- Trail of Bits audit (2022) — [simplex.chat/blog/20221108-simplex-chat-v4.2-security-audit-by-trail-of-bits.html](https://simplex.chat/blog/20221108-simplex-chat-v4.2-security-audit-by-trail-of-bits.html).
- Trail of Bits audit (2024) — published in SimpleX blog, 2024 release notes.
- SimpleX threat model — [simplex.chat/docs/glossary.html](https://simplex.chat/docs/glossary.html) and protocol documents.
- Marlinspike & Perrin, "The Double Ratchet Algorithm" (2016) — the underlying content-encryption primitive.

Compare this approach with [Delta Chat](/kb/delta-chat/), [XMPP with OMEMO](/kb/xmpp-omemo/) and [Jami](/kb/jami/) in [Choosing a private messenger](/kb/compare-messengers/).
