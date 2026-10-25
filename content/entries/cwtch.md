---
title: "Cwtch"
slug: cwtch
type: deep-dive
pillars: ["messaging", "anonymity"]
readiness: usable
description: "Cwtch, from Open Privacy, builds metadata-resistant one-to-one and group messaging on Tor onion services, with no central servers learning who talks."
dek: "A messenger that uses Tor v3 onion services as the messaging substrate. Each user runs their own onion service; conversations are direct onion-to-onion connections. Group chats use untrusted servers as relays — servers see encrypted blobs but cannot read content or membership. Built by Open Privacy Research Society (Sarah Jamie Lewis et al.), descendant in spirit of Ricochet, with explicit research grounding in metadata-resistant messaging design."
updated: 2026-10-25
created: 2026-04-26
origin: vault
source: "07-Encrypted-Messaging/Cwtch.md"
aliases: ["Cwtch Messenger", "Open Privacy Cwtch"]
tags: ["cwtch", "tor", "hidden-services", "metadata-resistance", "ricochet", "e2ee", "deep-dive"]
---

The Welsh word "cwtch" means a hug or a safe place. The project's framing is that messaging should provide that without requiring trust in any infrastructure operator.

## Architecture

Each Cwtch user is a **Tor v3 onion service**. A user's identifier is their onion address — a 56-character base32 encoding of the Ed25519 public key, a two-byte SHA3-256 checksum and a version byte:

```
mfrjeb7zfu3l3ec6ohm5zg7g4j7v...d.onion
```

Two Cwtch clients communicating directly:

```
[Alice's client] ── Tor circuit ──► [Alice's onion service]
                                            │
                                       (rendezvous)
                                            │
[Bob's client]   ── Tor circuit ──► [Bob's onion service]
```

There is no Cwtch server, no Cwtch directory, no central registry. To connect to Bob you need his onion address (exchanged out-of-band: QR code, scrap of paper, voice).

This is the same design pattern as **Ricochet** (2014, original by Patrick Stadler, later "Ricochet Refresh" by Blueprint for Free Speech). Cwtch is a more developed and more research-grounded successor — the Ricochet design without the unmaintained codebase.

## Group chat: untrusted servers

Direct onion-to-onion is fine for 1:1 chat but breaks down for groups: a group of 10 people would need 10 onion services online simultaneously, all the time, for any message to be delivered.

Cwtch's solution is **untrusted group servers**. A volunteer or self-hosted server hosts a "group" — but the server only sees encrypted ciphertexts and cannot read content or determine membership.

How:

1. The group has a shared symmetric key (distributed at group creation, rotated on membership changes).
2. Members encrypt messages under that key and post them as opaque blobs to the group server.
3. The server stores blobs and serves them to anyone who knows the group's identifier.
4. Decoy traffic and uniform-size blobs limit traffic-analysis leakage.

The group server cannot:

- Read message content (no key).
- Identify who posted a given blob (clients connect over Tor; no posting identity).
- Determine group membership (anyone with the group key can fetch).

The group server *can*:

- See request patterns (timing, blob sizes).
- Be subpoenaed for stored ciphertexts (which are useless without keys).
- Refuse service.

Cwtch's design philosophy: don't trust the server, but don't avoid using a server when one solves the offline-delivery problem cleanly. Make the server's role minimal and verifiable.

## Cryptography

- **Ed25519** for identity (the onion service key is the identity).
- **X25519** for key agreement.
- **Cwtch Profile Engine** uses authenticated encryption for direct messages with per-message ratcheting (Cwtch's own design, not Double Ratchet).
- **Group symmetric key** for group ciphertexts; rotation on member changes.

The cryptographic novelty is modest. The design choice is in *what you encrypt* and *what infrastructure you assume*, not in inventing new primitives.

Sarah Jamie Lewis and Open Privacy have published extensive design rationale, including the "Cwtch: Privacy Preserving Infrastructure for Asynchronous, Decentralized, Multi-Party and Metadata Resistant Applications" paper (2018) and several follow-up articles. The threat-model framing is unusually rigorous for a messenger.

## Comparison with similar designs

| Property | Cwtch | Ricochet Refresh | Briar | SimpleX |
|----------|-------|-------------------|-------|---------|
| Substrate | Tor v3 hidden services | Tor v3 hidden services | Tor + BLE + Wi-Fi-direct | SMP relays |
| Identifier | Onion address | Onion address | Briar profile (TLS pubkey) | None (per-conversation queues) |
| Group chat | Untrusted server (encrypted blobs) | Not really supported | Forums (P2P sync) | SMP-based groups |
| Asynchronous delivery | Group server (or both online) | Both online required | Both online OR mailbox | SMP queues |
| Mobile support | Android; Linux, macOS and Windows desktop; no listed iOS client | Desktop primarily | Android primary; desktop limited; no iOS | iOS, Android, desktop |
| Research lineage | Open Privacy / Lewis | Hermes Center / Stadler | Briar Project / Sussex | SimpleX Chat Ltd. |
| Maintenance status | See project releases | See project releases | Maintenance mode since 9 July 2026 | See project releases |

Cwtch is the most actively developed and most research-grounded of the Tor-based messengers in 2026. Ricochet Refresh remains a credible if slower-moving alternative.

## Threat model

The Cwtch threat model is documented at [docs.cwtch.im/security/threat_model](https://docs.cwtch.im/security/threat_model/) and is unusually candid.

### What Cwtch protects against

- **Single-operator metadata harvesting.** No Cwtch operator exists. The closest thing is a group server, which sees encrypted blobs and request timings.
- **Account-discovery enumeration.** No directory, no usernames, no phone numbers. Identifiers are 56-character random-looking strings.
- **Network-level identity correlation.** All traffic goes through Tor; client IPs are not visible to peers.
- **Plaintext in transit.** All connections are E2EE between onion services or to group servers (which see ciphertext).

### What it doesn't

- **Endpoint compromise.** Same as everywhere.
- **Tor compromise.** If the global passive adversary attack succeeds against Tor, Cwtch inherits it.
- **Out-of-band onion-address exchange.** If you send your Cwtch address via a surveilled channel, the social graph leaks at that point.
- **Group server collusion across many groups.** A network observer running many group servers and many Tor relays could approximate membership timing for some groups.

The published threat model also distinguishes "cryptographic correctness" from "metadata resistance" cleanly — a refreshing contrast to messengers that conflate the two.

## Deployment

- **Platforms**: Android, Linux, macOS and Windows. The official supported-platform list does not list an iOS client.
- **License**: MIT for clients, BSD-style for server.
- **Source**: [git.openprivacy.ca/cwtch.im](https://git.openprivacy.ca/cwtch.im) and mirrored on GitHub.
- **Funding**: Open Privacy Research Society, a Canadian nonprofit; partly grant-funded (NLnet, NGI, occasional government research grants).
- **User base**: small, low thousands. Cwtch is a research-driven project with high quality and modest adoption.

## Operational notes

- Each Cwtch installation generates a profile (the onion key). Back it up; lose it, lose your identity.
- A Cwtch profile can be password-encrypted at rest; consider using this on shared devices.
- Group servers can be self-hosted on a $5 VPS using the open-source server binary. For a circle of friends or activists, running your own group server is straightforward.
- Onion-service connection latency is real: 1-3 seconds for typical message delivery is normal.
- Battery and bandwidth: continuous Tor connectivity costs more than Signal. Plan for it on mobile.

## Why this design

Sarah Jamie Lewis's broader argument (across her papers and Open Privacy's work): metadata resistance is incompatible with treating "the server" as a trusted operator. Either the server cannot read or correlate content + metadata, or your design is leaking. Cwtch is the working illustration of "what does a messenger look like if you start from that constraint?"

The cost is performance, mobile-platform friction, and small user base. The benefit is a system whose threat model is honest at every layer and whose worst-case operator-compromise scenario is dramatically smaller than the Signal model.

For activists, journalists, and anyone whose threat model includes "the messenger company itself might be compelled to harm me," Cwtch is structurally better than centralized alternatives. For everyday messaging, Signal or SimpleX are easier.

## Primary sources

- [Cwtch supported platforms](https://docs.cwtch.im/docs/getting-started/supported_platforms)
- [Tor v3 onion-address encoding](https://spec.torproject.org/rend-spec/encoding-onion-addresses.html)
- [Briar maintenance-mode announcement](https://briarproject.org/news/2026-maintenance-mode/)
- [Cwtch downloads for Android and desktop](https://cwtch.im/download/)

Compare [Quiet](/kb/quiet/), [Jami](/kb/jami/) and the other architectures in [Choosing a private messenger](/kb/compare-messengers/). For document submissions, see [OnionShare](/kb/onionshare/) and [SecureDrop](/kb/securedrop/).
