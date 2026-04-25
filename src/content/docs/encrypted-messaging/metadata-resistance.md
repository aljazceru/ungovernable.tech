---
title: "Metadata Resistance"
tags:
  - "metadata-resistance"
  - "simplex"
  - "session"
  - "anonymity"
  - "deep-dive"
  - "messaging"
  - "privacy"
---
*Encryption hides what you say. Metadata resistance hides who you said it to, when, and how often. Few systems take it seriously; the ones that do trade convenience for it.*

---

## What "metadata-resistant" means in practice

A messenger is metadata-resistant if a network observer (server, ISP, cloud provider, lawful intercept) cannot answer questions like:

| Question | Signal | Nostr (default) | SimpleX | Session | Cwtch |
|----------|--------|-----------------|---------|---------|-------|
| Who is the sender? | Sealed sender hides from server | Visible (npub) | Hidden (no user IDs) | Hidden | Hidden |
| Who is the recipient? | Visible to server | Visible | Hidden (queue ID) | Hidden | Hidden |
| How often does Alice talk to Bob? | Visible (frequency) | Visible | Per-queue, not per-pair | Per-mailbox | Per-Tor-circuit |
| Are Alice and Bob friends? | Contact list | Public follow list | Hidden | Hidden | Hidden |
| Where is Alice? | IP at server | IP at relay | IP at SMP server (or Tor) | Hidden via Lokinet | Hidden via Tor |
| When is Alice online? | Visible | Visible per relay | Polling-pattern visible | Mailbox check pattern | Tor-only |

The leading metadata-resistant designs sacrifice features (search, push notifications, group scale) for these properties.

---

## The designs

### SimpleX

The most architecturally radical. No user IDs. Pairs of users share a *queue ID* on a relay (SMP server). Alice and Bob each connect to the queue server via separate one-way connections; the server sees two anonymous connections, not "Alice ↔ Bob".

Properties:

- No user identifiers. Just per-relationship queue IDs.
- Unidirectional queues. Sender and recipient connect separately.
- Optional Tor for full IP anonymization.
- Push notifications via separate notification servers, also without user IDs.
- Multi-server by default; queues split across operators.

Trade-off: contact discovery is out-of-band (QR code or one-time link). No global directory.

### Session

Forked from Signal, dropped phone numbers. Routes through Lokinet, a Loki-mixnet-derived overlay similar to Tor. Identity is a public key (`05XXX…` Session ID).

- No phone, no email.
- Lokinet-routed by default. IP not visible to Session servers.
- Mailbox-based delivery. Recipient pulls; sender pushes to a swarm of nodes hosting the mailbox.
- Onion-routed message envelopes.

Trade-off: smaller user base, less audited than Signal.

### Cwtch (Tor-only)

Tor v3 hidden services as the entire transport. No central server, no message storage, peers must be online to deliver in real time.

- Tor v3 client auth. Only authorized peers connect.
- No accounts, no servers.
- Async via "untrusted infrastructure" — message queueing nodes are blind, just hold ciphertext.
- Open Privacy Foundation project.

Trade-off: synchronous-only without untrusted infra; tiny ecosystem; battery hungry on mobile.

### Briar (P2P + Tor + offline)

Built around adversarial network conditions. Three transport modes: Tor, Bluetooth, Wi-Fi direct. No servers at all.

- Direct peer-to-peer. No infrastructure.
- Forum / blog model for groups.
- Designed for journalists and activists in repressive regimes.

Trade-off: peers must be reachable (online over Tor, or physically nearby). Async via "Briar Mailbox" — a separate device that holds messages while peers are offline.

### Status / Waku v2

DApp-friendly P2P messaging over libp2p with relay-style propagation. Full nodes hold message queues; light nodes use Discovery and ephemeral identities.

---

## Comparing mechanisms

| Mechanism | Hides social graph | Hides timing | Battery / UX cost |
|-----------|--------------------|-------------|--------------------|
| Sealed sender (Signal) | From server | No | None |
| Gift wrap (NIP-17) | From relay | No | Low |
| Mixnet (Nym) | From global observer | Partially | High |
| Tor onion service (Cwtch, Briar) | From upstream | No | Medium |
| Per-relationship queue (SimpleX) | Architecturally | No | Medium |
| Constant-rate cover traffic | From timing analysis | Yes | High |

True timing-attack resistance still requires constant-rate cover traffic. Only Loopix-derived mixnets ([Overview - Mix Networks](/mix-networks)) and academic systems (Vuvuzela, Pung) provide it for messaging.

---

## What even the best systems don't hide

- Endpoint compromise. Malware reads everything. Hardware security modules and runtime attestation help; software E2EE alone does not.
- You being a user. Even SimpleX needs *some* network presence at SMP servers; an adversary at your ISP knows you talk to SimpleX servers.
- Your contacts in non-adversarial settings. Real-world graphs (people you actually talk to in person) leak through phone records, photos, and posts.

The honest framing: metadata-resistance reduces leakage to specific adversaries. There is no "perfect anonymity for messaging" in deployed software.

---

## Composing for maximum privacy

```
Endpoint:    OS hardened, FDE, biometric or hardware key for unlock
   ↓
App:         SimpleX or Session or Briar (no user IDs)
   ↓
Transport:   Tor or Lokinet (anonymizes network identity)
   ↓
Identity:    Per-relationship keys; rotate; don't link to clearnet identity
   ↓
Backups:     Local encrypted; never to cloud
```

For ultra-high-stakes work (whistleblowing, journalism in repressive regimes), the recommended stack is Tails OS (amnesic) + Tor + (Cwtch or SecureDrop for source-journalist contact, depending on async needs) + an air-gapped device for handling content.

---

## Trade-offs summary

### Strengths

- Drastically reduces server-visible information.
- Resists subpoena. Servers literally don't have the data.
- Supports pseudonymity by design. Phone-number registration is impossible.

### Limitations

- Discovery is hard. No directory means out-of-band contact establishment.
- Push notifications are tricky. True push requires *some* identifier; clever workarounds exist.
- Smaller user bases. Network effects favor mainstream apps.
- No multi-device E2EE history sync in some systems.
- Battery cost from always-on Tor / mixnet routing.

---

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Endpoint compromise | Hardware-isolated keys (Secure Enclave, hardware tokens), runtime attestation |
| Server log correlation | Metadata-resistant queue model, multiple servers, Tor |
| Long-term timing analysis | Constant-rate cover traffic (Nym), random delays |
| Social-graph inference via volume | Pad messages; use multiple queues |
| Hardware fingerprinting | Tails / amnesic systems |
| Forced device unlock | Hidden volumes, duress wallets, plausible deniability |

---

## Related Files

- [Overview - Encrypted Messaging](/encrypted-messaging)
- [Signal Protocol Technical](/encrypted-messaging/signal-protocol-technical)
- [Nostr Deep Dive](/encrypted-messaging/nostr-deep-dive) — NIP-17 metadata properties
- [Overview - Mix Networks](/mix-networks) — strongest metadata defense
- [MOC - Metadata Privacy](/meta/moc-metadata-privacy)

---

## Primary Sources

- Evgeny Poberezkin, *SimpleX Messaging Protocol*, 2021. [github.com/simplex-chat/simplexmq/blob/master/protocol/simplex-messaging.md](https://github.com/simplex-chat/simplexmq/blob/master/protocol/simplex-messaging.md)
- Session Foundation, *Session Whitepaper*, 2020.
- Open Privacy Research Society, *Cwtch: Privacy-preserving infrastructure*.
- van den Hooff et al., *Vuvuzela: Scalable Private Messaging Resistant to Traffic Analysis*, SOSP 2015.
- Angel & Setty, *Unobservable Communication over Fully Untrusted Infrastructure*, OSDI 2016 (Pung).
- Briar Project, *Briar protocol specification*.

