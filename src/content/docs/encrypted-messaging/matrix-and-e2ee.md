---
title: "Matrix and E2EE"
tags:
  - "matrix"
  - "e2ee"
  - "federation"
  - "mls"
  - "olm"
  - "megolm"
  - "messaging"
  - "deep-dive"
sidebar: {"label":"Matrix and E2EE"}
---
*Federated, decentralized, eventually-consistent communication — large-group E2EE at the cost of richer metadata exposure than Signal or Nostr.*

---

## What Matrix Provides

Matrix is a **federated** open standard for real-time communication: chat, VoIP, IoT, file sharing. The unit of identity is `@user:homeserver.tld`; rooms span multiple homeservers via federation. Compared to Signal: more complex, more flexible, more metadata. Compared to Nostr: stronger consistency, harder identity portability.

Pillars:

- **Open spec** — Matrix Specification (CS API, S2S API, AS API).
- **Federated** — homeservers exchange events; no single org runs the network.
- **E2EE optional but default in Element** — Olm (1:1) and Megolm (group).
- **Rich room model** — power levels, state events, persistent room state, threaded replies.
- **Bridges** — gateways to IRC, XMPP, Telegram, Discord, Signal, etc. (E2EE breaks at the bridge).

---

## Encryption: Olm and Megolm

### Olm — Double Ratchet variant

Per-device pairwise encryption. Equivalent design to Signal's Double Ratchet adapted for Matrix's "many devices per user" model. Each user's devices have their own keys.

### Megolm — group ratchet

For rooms, a sender publishes a **session** (ratcheting symmetric chain) to all members. Members encrypt incoming Megolm sessions per-device using Olm. Properties:

- **Forward secrecy** — yes, per ratchet step.
- **Post-compromise security** — only on session rotation (which clients do periodically and on member changes).
- **Membership privacy** — limited; the homeserver knows the room roster.

### Cross-signing & key verification

Identity verification across devices via cross-signed keys. UX: emoji or numeric short-code comparison. Reduces TOFU footgun substantially since 2020.

### MLS migration

Matrix has an MLS profile in development that replaces Olm/Megolm with the IETF MLS standard (RFC 9420). Production rollout staged; stable group E2EE with TreeKEM for large rooms.

---

## Federation Model

```
homeserver A          homeserver B
   │                       │
@alice:A           @bob:B
   │                       │
   └── room !abc:A ────────┘
       events propagate via S2S API
```

The room is **owned by its origin server** and replicated to all servers with members. Server outages = partial outage for that server's users; the room continues elsewhere.

### What homeservers see

| About own users | About remote users |
|-----------------|--------------------|
| Identity, login, devices | Their MXIDs (visible in room) |
| Encrypted message metadata (sender, time, room) | Same |
| Room rosters, membership changes | Same for federated rooms |
| Local IPs, login timing | Indirect (via S2S timing) |

E2EE protects content; **room participation, timing, and topology are not hidden** at the federation layer.

---

## Trade-offs vs Signal and Nostr

| Property | Signal | Matrix | Nostr |
|----------|--------|--------|-------|
| Identity | Phone | MXID `@u:server` | npub (key) |
| Account portability | None | MSC4133 in progress | Trivial |
| Federation | None | Yes | No formal federation; relays |
| Metadata exposure | Lower | Higher (homeservers) | Higher for unencrypted; gift-wrap fixes for DMs |
| Group scaling | Limited (Sender Keys) | Good (Megolm; MLS coming) | Application-layer rooms |
| Censorship-resistance | Low | Medium | High |
| Rich messaging features | Medium | Highest | Growing |

---

## Implementations

### Servers

- **Synapse** (reference, Python) — most-deployed; matures slowly.
- **Dendrite** (Go, microservices) — more performant.
- **Conduit** (Rust, single-binary) — community-favorite for small homeservers.
- **MAS** (Matrix Authentication Service, OIDC bridge) — replaces password login for newer Synapse.

### Clients

- **Element** (web, desktop, iOS, Android) — reference client.
- **FluffyChat** (Flutter) — multi-platform.
- **Cinny** (web) — Discord-like UI.
- **Element X** (Matrix Rust SDK) — newer, faster, sliding-sync-based.

---

## Operational Concerns

### Self-hosting

A 100-user Synapse homeserver is feasible on a $10/month VPS — until it joins a popular room with thousands of remote members and storage explodes (the classic "join Matrix HQ" gotcha). Plan disk, plan database (Postgres), plan media storage (S3-compatible).

### Privacy hardening

- Disable URL previews (homeserver fetches URLs, leaking room contents).
- Disable presence unless needed.
- Use ephemeral / disposable MXIDs for sensitive joins.
- Pair E2EE with Tor SOCKS for the client.
- Audit room state for unwanted user-impersonating bots.

### Account recovery

Cross-signing + key backup means recovery is possible from a Recovery Key (essentially a passphrase-encrypted backup of decryption keys). Lose it AND all devices → cannot decrypt history.

---

## Trade-offs

### Strengths

- **Rich, well-specified protocol.** No reverse engineering.
- **Federation removes single org control.** Matrix.org is *one* server, not the only one.
- **Bridges to legacy networks.** Pragmatic interoperability.
- **Open, audited E2EE.** Megolm has had bugs; they get fixed in the open.
- **Strong group support.** Multi-thousand-member encrypted rooms.

### Limitations

- **Metadata via federation.** Homeservers see who-is-in-which-room.
- **Complexity.** Synapse is heavyweight; running it correctly takes care.
- **Identity portability is poor today.** Rebinding `@old:A` to `@new:B` loses follower-equivalent context.
- **E2EE off-by-default in legacy contexts.** Old public rooms are unencrypted; bridged rooms break encryption.
- **Inconsistent client crypto correctness.** Bugs surface at the boundary of Olm/Megolm + room state machine.

---

## Attack Surface

| Attack | Description | Mitigation |
|--------|-------------|------------|
| Compromised homeserver | Inject device keys, exfiltrate metadata | Cross-signing, key verification, self-host |
| Federation poisoning | Malicious S2S claims | Server-key signing, ACLs |
| Bridge injection | Bridge logs unencrypted plaintext | Don't bridge sensitive rooms; treat bridges as "not E2EE" |
| Key-reuse via room rejoin | Stale Megolm session compromise | Periodic rotation, member-change rotation |
| Unsigned device additions | Malicious device added via account takeover | Cross-signing verification on every new device |
| Room state poisoning | Attacker promotes themselves via crafted state event | Bug-class, fixed by spec; audit power-level events |

---

## Recent Developments (2024-2026)

- **MLS migration profile** — partial rollout in Element X.
- **Sliding Sync (MSC3575)** — drastically faster client cold-start; deployed.
- **Element X stable releases** — Rust SDK reaches feature parity.
- **MAS / OIDC** — modern auth replacing password login.
- **Account migration spec (MSC4133)** — early draft.

---

## Related Files

- [Overview - Encrypted Messaging](/encrypted-messaging/overview-encrypted-messaging)
- [Signal Protocol Technical](/encrypted-messaging/signal-protocol-technical)
- [Nostr Deep Dive](/encrypted-messaging/nostr-deep-dive)
- [Metadata Resistance](/encrypted-messaging/metadata-resistance)

---

## Primary Sources

- Matrix Specification — [spec.matrix.org](https://spec.matrix.org)
- *Olm specification* — [gitlab.matrix.org/matrix-org/olm](https://gitlab.matrix.org/matrix-org/olm)
- *Megolm specification* — same repo.
- Hodgson, *Matrix.org: an open standard for decentralised communication*, FOSDEM talks 2014–2024.
- Matrix Foundation reports — [matrix.org/blog](https://matrix.org/blog)
- RFC 9420, *Messaging Layer Security* — for the MLS migration.

