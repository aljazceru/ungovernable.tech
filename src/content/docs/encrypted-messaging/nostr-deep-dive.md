---
title: "Nostr Deep Dive"
tags:
  - "nostr"
  - "messaging"
  - "e2ee"
  - "decentralized"
  - "social"
  - "deep-dive"
  - "censorship-resistance"
sidebar: {"label":"Nostr Deep Dive"}
---
*"Notes and Other Stuff Transmitted by Relays" — a minimalist, pubkey-rooted social protocol with no accounts, no federation negotiation, and no central kill switch.*

---

## Core Design

Nostr's whole protocol fits in two paragraphs:

1. **Identity is a key.** Each user has a `secp256k1` keypair. The public key (`npub` in bech32) *is* the user — there's no username allocation, no registry, no email. Lose the key, lose the identity.

2. **Events are signed JSON.** A user signs a small JSON object (id, pubkey, created_at, kind, tags, content, sig) and POSTs it to one or more **relays**. Anyone subscribing to that relay receives the event. Clients verify the signature locally; relays are dumb pipes.

That's it. Everything else — long-form posts, DMs, reactions, zaps, marketplaces, NIP-05 identity, gift-wrapped DMs — is layered as **NIPs** (Nostr Implementation Possibilities) over this minimal substrate.

---

## Why It's Different

| Property | Nostr | Federated (ActivityPub) | Signal |
|----------|-------|-------------------------|--------|
| Identity | User-owned keypair | Server-bound handle | Phone number |
| Account portability | Trivial — just publish to new relay | Requires migration tooling | Not portable |
| Censorship of identity | Impossible | Server can suspend | Possible (number ban) |
| Censorship of content | Per-relay only | Per-server | Centralized |
| Discovery | Relay-driven, eventually consistent | Per-server timelines | Contact list only |
| Sybil resistance | None inherent | Server-mediated | Phone uniqueness |

Nostr trades discovery convenience for sovereignty. The discovery problem is real but solved at the application layer (follow lists, web of trust, paid relays).

---

## Event Kinds (selection)

| Kind | Purpose |
|------|---------|
| 0 | Profile metadata |
| 1 | Short text post (a "note") |
| 3 | Contact / follow list |
| 4 | Encrypted DM (legacy NIP-04, deprecated) |
| 5 | Event deletion request |
| 6 | Repost |
| 7 | Reaction |
| 9735 | Lightning zap receipt |
| 30023 | Long-form article |
| 1059 | Gift-wrapped event (NIP-59) |
| 14 | Direct message (NIP-17, gift-wrap envelope) |

NIP registry: [github.com/nostr-protocol/nips](https://github.com/nostr-protocol/nips)

---

## Encrypted DMs: NIP-04 vs NIP-44 vs NIP-17

This is the most important Nostr privacy story.

### NIP-04 (legacy, deprecated)

ECDH between sender/recipient pubkey, AES-256-CBC. Plaintext kind=4 events leak:

- Who sent → who received (relay sees both pubkeys).
- Length and timing.
- The DM relationship as a public fact.

### NIP-44 (modern cipher)

ChaCha20 + HMAC-SHA256, with versioning and proper KDF. Cipher itself is solid; the *envelope* is still public-key-tagged so the relay can route it.

### NIP-17 + NIP-59 (gift wrap, current standard)

Three-layer envelope:

1. **Rumor** — the actual content event (unsigned).
2. **Seal** — rumor encrypted to the recipient's pubkey, signed by sender.
3. **Gift wrap** — seal encrypted to the recipient's pubkey, signed by an *ephemeral* pubkey, kind=1059.

The relay sees only the gift wrap kind=1059 from a random ephemeral key to the recipient. **The social graph is hidden from the relay.** Sender's identity is revealed only after the recipient decrypts.

This is a major step toward Signal-grade metadata properties without Signal's centralization.

---

## Relays

Anyone can run one. No federation handshake — clients just connect via WebSocket and subscribe with filters. Relays are pluggable, with diversity of policies:

- **Permissive** — accept everything (high storage cost).
- **Paid** — Lightning sats per event (spam-resistant, runs on a small disk).
- **Subject-restricted** — relays for niche communities, DEFI traders, etc.
- **Privacy-restricted** — relays that only accept gift-wrapped DMs.

Robust clients connect to **multiple relays simultaneously** (5-10 typical) for both redundancy and reach. A user can move all their content by republishing to new relays — there's no "account migration" because there's no account.

---

## NIP-05: Human-Readable Names

`alice@ungovernable.tech` resolves via HTTPS to `/.well-known/nostr.json` containing the npub. **Resolution requires DNS + HTTPS** — it's a centralization vector.

Mitigations:

- **NIP-05 over PKARR** — same JSON served by a PKARR record under your Pubky pubkey. No DNS dependency.
- **NIP-05 over Tor `.onion`** — works, less common.

The npub is canonical; NIP-05 is just a presentation alias.

---

## Zaps (Lightning Tipping)

NIP-57 wires Lightning payments to Nostr events:

1. User A clicks "zap" on user B's note.
2. Wallet generates a Lightning invoice via B's LNURL endpoint.
3. The receipt is published as kind=9735 on relays.
4. Anyone aggregating zap receipts can compute B's earnings.

This couples Nostr's identity layer with Bitcoin's payment layer — the only major social protocol where the speech and payment substrate are equally censorship-resistant.

---

## Trade-offs

### Strengths

- **Pure pubkey identity.** No KYC, no registrar, no censorship at identity layer.
- **Trivial account portability.** Move relays without losing followers.
- **Permissionless innovation.** New kinds and NIPs deployed by anyone, immediately.
- **Native Lightning integration.** Zaps and paid relays.
- **Simple protocol.** Single-binary clients, single-binary relays, no PKI.

### Limitations

- **Lossy persistence.** Relays may delete or rate-limit; durability depends on which relays you use.
- **Sybil-prone.** Anyone can mint an npub; spam mitigations live in client filters and WoT.
- **Discovery is hard.** Without follow graphs, finding new accounts is non-trivial.
- **Key custody risk.** Losing the key = losing identity. NIP-26 delegation, hardware-wallet-signed events, and account-recovery NIPs help.
- **Metadata leaked outside NIP-17.** Plain notes are public; even with gift-wrapped DMs, posting and follow lists leak.
- **Client diversity → bug surface.** Many clients reimplement the protocol; some don't validate signatures correctly.

---

## Attack Surface

| Attack | Mitigation |
|--------|-----------|
| Relay flood / spam | Paid relays, client-side filters, WoT |
| Eclipse attack via relay subset | Connect to many relays, rotate |
| Sybil follow inflation | Trust only social-graph-rooted accounts |
| Key compromise | Move to new key + announce via signed delegation; consider FROST threshold sig |
| Relay log correlation | Use NIP-17 for DMs; route over Tor |
| NIP-05 takedown | Self-host; serve over PKARR / `.onion` |
| Phishing via npub similarity | Petname systems, NIP-05 verification |

---

## Tools

| Type | Notable |
|------|---------|
| Mobile clients | Damus (iOS), Amethyst (Android), Primal |
| Web clients | Iris, Nostrudel, Coracle, Snort |
| Long-form | Habla.news, Yakihonne |
| Marketplaces | Plebeian Market, shopstr |
| Relay software | strfry, nostr-rs-relay, nostream, khatru |
| Key management | Amber (Android), nos2x (browser), Alby, Keystone (hardware-signed) |

---

## Recent Developments (2024-2026)

- **NIP-17 standardization** — gift-wrapped DMs become default.
- **Outbox model (NIP-65)** — clients publish read/write relay lists; receivers know where to post replies.
- **Nostr-DVMs** — Data Vending Machines, paid compute services discoverable via Nostr.
- **Decentralized recovery** (NIP-XX drafts) — Shamir / FROST-based key recovery.
- **Hardware-wallet signing** — Coldcard and Keystone added Nostr event signing.

---

## Related Files

- [Overview - Encrypted Messaging](/encrypted-messaging/overview-encrypted-messaging)
- [Signal Protocol Technical](/encrypted-messaging/signal-protocol-technical)
- [Matrix and E2EE](/encrypted-messaging/matrix-and-e2ee)
- [Metadata Resistance](/encrypted-messaging/metadata-resistance)
- [Lightning Network Deep Dive](/financial-sovereignty/lightning-network-deep-dive) — zaps integration
- [Overview - Decentralized DNS](/decentralized-dns/overview-decentralized-dns) — NIP-05 over PKARR
- [Overview - Web of Trust](/cryptography/overview-web-of-trust)

---

## Primary Sources

- fiatjaf, *Nostr — Notes and Other Stuff Transmitted by Relays*, 2020. [github.com/nostr-protocol/nostr](https://github.com/nostr-protocol/nostr)
- NIPs registry — [github.com/nostr-protocol/nips](https://github.com/nostr-protocol/nips)
- NIP-17 / NIP-44 / NIP-59 specifications.
- *Nostr — A simple, open protocol* (whitepaper-style overview).

