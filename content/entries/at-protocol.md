---
title: "AT Protocol and did:plc"
slug: at-protocol
type: deep-dive
pillars: ["identity"]
readiness: usable
description: "Bluesky's AT Protocol identity model: portable signed repositories anchored to did:plc or did:web, and how much of it depends on Bluesky itself."
dek: "Bluesky's identity model: signed, portable user repositories anchored to a DID, with did:plc as the operationally centralized log Bluesky runs while the data model leaves room for future decentralization. This file looks at how the architecture actually works in 2026 and where the centralization sits."
updated: 2026-10-25
created: 2026-04-26
origin: vault
source: "11-Identity/AT Protocol and did-plc.md"
aliases: ["AT Protocol", "ATProto", "did:plc", "Bluesky Identity"]
tags: ["atproto", "bluesky", "did-plc", "identity", "pds", "appview", "deep-dive"]
---

## What AT Protocol is

The **Authenticated Transfer Protocol (AT Protocol, atproto)** is the underlying protocol Bluesky launched on. It was designed to be:

- **Account-portable**: a user's data and identity can move between hosting providers without losing followers or history.
- **Federated-ish**: hosting providers (PDSs) are independent, but a global network of indexers and relays serves a unified view.
- **Self-authenticating**: data is signed by the user, so any provider can serve it and verifiers can check authenticity.

The architecture was published in 2022 by Bluesky (a Public Benefit LLC originally incubated by Twitter, now independent), and the network went public in 2023.

## Three-component architecture

```
                         ┌────────────┐
                         │  AppView   │  (indexers serving the
                         │  (bsky.app)│   "feed" view to clients)
                         └─────┬──────┘
                               │ reads from
                               ▼
              ┌───────────────────────────────────┐
              │         Relay (firehose)          │  (Aggregates the
              │   public stream of all repo ops   │   global event log)
              └─────┬─────────────────────────────┘
                    │ subscribes to
                    ▼
           ┌─────────┐  ┌─────────┐  ┌─────────┐
           │  PDS A  │  │  PDS B  │  │  PDS C  │  (Personal Data
           │ (hosts  │  │  ...    │  │  ...    │   Servers — store
           │ Alice)  │  │         │  │         │   user repositories)
           └─────────┘  └─────────┘  └─────────┘
                  ▲                                   ▲
                  │                                   │
              ┌───┴────┐                         ┌────┴────┐
              │ Alice's│                         │  did:plc│
              │ client │ <-- looks up DID -->    │   log   │  (centralized
              │        │                         │         │   directory)
              └────────┘                         └─────────┘
```

### PDS — Personal Data Server

The user's data lives on a PDS. A PDS:

- Stores the user's repository (a Merkle-search-tree of records).
- Serves authenticated reads to clients.
- Signs records on the user's behalf if it holds the rotation key (or accepts client-signed records if not).
- Publishes the user's commits to the relay firehose.

Anyone can run a PDS. The default is `bsky.social`, run by Bluesky PBC, but third-party PDSs exist. Account migration between PDSs is a defined protocol step.

### Relay

The relay subscribes to all PDSs and republishes a unified firehose of events: every commit on every repo, in real time. Anyone can run a relay. There is one dominant relay (Bluesky's), but the protocol allows multiple.

### AppView

An AppView indexes the firehose and serves derived views (timelines, search, notifications) to clients. The official `bsky.app` AppView is what most users hit. Independent AppViews exist (e.g., `frontpage.fyi`, custom feed services).

### Lexicon

AT Protocol uses a schema language called **Lexicon** to define record types. This is the equivalent of defining "what a post / like / follow looks like" — and lets third-party AppViews understand the data structure.

## Repository signing

Each user repository is a **Merkle-search-tree** of records. The MST root is signed with the user's repository signing key on every commit. This means:

- Any record can be verified by anyone, with just the user's pubkey, by checking the Merkle proof from the record up to the signed root.
- The PDS doesn't need to be trusted. It serves data; cryptographic verification happens on the client.
- Migration between PDSs is just copying the repository to the new host and updating the DID to point there.

Repository signing key is held by the PDS in current deployments — meaning the PDS can sign anything on the user's behalf. This is operational simplicity but a meaningful trust assumption: **your PDS can write to your repository**.

## did:plc — the identity layer

Each user has a DID. The dominant method is `did:plc`. The identifier is opaque and random:

```
did:plc:ewvi7nxzyoun6zhxrhs64oiz
```

PLC expands to **"provisional ledger of credentials"** in Bluesky's original naming, reflecting the intent to keep the log replaceable. As of 2026, `did:plc` remains the deployed AT Protocol identity log.

### How did:plc works

The PLC operator (currently a Bluesky-run service at `plc.directory`) maintains an **append-only log of signed operations** for every DID. Each DID's history is a chain:

```
op1 (genesis): create did:plc:..., signed by initial rotation keys
   ↓
op2 (update): rotate keys, change PDS endpoint, ..., signed by current rotation keys
   ↓
op3 (update): ...
```

Anyone can fetch the operation log for a DID from `plc.directory` and verify the signature chain. The current DID Document is derived from the latest valid operation.

### What's signed

Each operation is signed by **rotation keys** — keys whose authority is to update the DID. A typical user has:

- 1-2 rotation keys (one held by the user / their wallet, optionally one held by the PDS).
- The PDS's signing key (registered in the DID Document).

To rotate the PDS or update key material, the user signs a new operation with a rotation key and submits it to plc.directory.

### What "centralized log" means in practice

Bluesky operates `plc.directory`. This means:

- Bluesky controls the canonical PLC log. They could refuse to accept operations, censor specific DIDs, or rewrite history (subject to detection).
- Verifiers can detect rewriting by comparing operation hashes across cached copies of the log. There are independent mirrors (e.g., `plc.bsky.app` and community-run mirrors) but no consensus protocol that prevents the operator from misbehaving.
- The data model is designed to be portable to a decentralized substrate (Bluesky has discussed running PLC on a BFT consensus layer or anchoring it to Bitcoin in the future). **As of 2026, this has not happened.**

### The honest critique

did:plc carries the "DID" framing — implying decentralization — but is **operationally centralized**. The PLC log is run by one organization. A user's identity is portable between PDSs, but the DID itself depends on Bluesky continuing to run plc.directory and accept operations honestly.

This is a different centralization than did:web (DNS) or did:plc's competitors:

- **did:web**: DNS-trust-rooted; everyone running their own domain has independent control. But identifiers are domain-bound.
- **did:plc**: identifiers are random and portable across PDSs, but the log is run by one operator. **Slightly more decentralized for ordinary users than did:web (you don't need a domain), substantially less so than did:ion (Bitcoin-anchored).**
- **did:ion**: Bitcoin-anchored via Sidetree. Decentralized, but operationally heavier and slower.

In practice: did:plc is "decentralized enough" for Bluesky's threat model (Twitter-replacement social) but is not what a user looking for cypherpunk-grade sovereign identity should rely on.

## did:web fallback

ATProto also accepts `did:web` for users who own a domain. A user's DID can be `did:web:alice.example.com`, with the DID Document served at `https://alice.example.com/.well-known/did.json`. This:

- Removes plc.directory from the trust path.
- Trades plc.directory for DNS + CA trust.
- Lets users with their own domain own their identifier independently of Bluesky.

A handful of users, mostly developers and organizations, run did:web identities on ATProto. The mass-market UX is did:plc.

## Account portability

A user with a did:plc identity can migrate their account from one PDS to another:

1. New PDS pulls the repository from the old PDS.
2. User signs a PLC operation rotating the PDS endpoint to the new PDS, signed by their rotation key.
3. Submit operation to plc.directory.
4. Old PDS marks the account as migrated; new PDS becomes authoritative.

This actually works. People run their own PDSs (or use third-party hosting like PDS-as-a-service providers) and migrate accounts without losing followers or post history. This is a meaningful achievement.

The catch: **the migration depends on plc.directory**. Bluesky operating the log is the bottleneck. If they refuse to accept your operation, your account is stuck.

## Comparison with Nostr's pure-keypair model

| Property | AT Protocol (did:plc) | Nostr (pubkey) |
|----------|----------------------|---------------|
| **Identifier** | Opaque DID + portable | Public key (npub) |
| **Identity registry** | plc.directory (centralized) | None |
| **Rotation** | Yes, via signed PLC operations | Not native; NIP-26 delegation is unrecommended |
| **Account portability** | Yes (PDS migration via DID update) | Trivial (key works on any relay) |
| **Hosting** | PDS holds repository | Relays hold events; user-signed |
| **Recovery** | Rotation keys held offline | None native; external schemes (FROST, multisig) |
| **Discovery** | AppView + handles via DNS (`alice.bsky.social`) | NIP-05 + WoT |
| **Censorship-resistance** | Limited by plc.directory and PDS / relay availability | Strong (any relay works) |
| **Data model** | Lexicon-typed records | Free-form events with kinds |

The key trade-off: ATProto bought account portability and rotation by accepting a centralized PLC log. Nostr kept everything pure-key but pays in lack of native rotation.

For a user who wants:
- **Mass-market social** with rotation and migration: ATProto / did:plc.
- **Censorship-resistant pseudonymity**: Nostr.
- **Both**: keep accounts on both networks.

## Trade-offs

### Strengths

- Account portability between PDSs actually works in practice.
- Self-authenticating data: records signed by user, MST roots verifiable.
- Rotation via signed PLC operations.
- Lexicon schemas allow third-party AppViews.
- Production scale: tens of millions of users as of 2025-2026.
- Smooth UX. The user doesn't need to know what a DID is.

### Limitations

- **Centralized PLC log**. The "DID" framing is generous; one operator runs the canonical log.
- PDS holds the signing key in current deployments (not the user) — your PDS can sign on your behalf.
- AppView centralization. Most users hit one AppView (`bsky.app`); algorithmic curation lives there.
- Relay centralization. Bluesky's relay is the dominant firehose.
- did:web is the only fully self-hosted option, and it inherits DNS / CA trust.
- Account portability is a single-operator feature: it depends on plc.directory accepting your operation.

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| plc.directory censors / refuses operations | did:web fallback; future migration to decentralized PLC substrate |
| PDS forges records on user's behalf | User-side signing where supported; attestation of PDS behavior |
| Rotation key compromise | Multiple rotation keys, kept offline; recovery via secondary rotation keys |
| Repository signing key compromise | Rotation to new key via PLC operation |
| AppView fabricates feed contents | Independent AppViews; user verification of records via PDS |
| DNS hijack of did:web | Same as did:web — DNSSEC, registrar lock |
| Quantum attack on signing keys | atproto signature-agnostic in principle; production uses Ed25519/secp256k1 |

## Future decentralization paths

Bluesky has discussed several paths to decentralizing the PLC log:

1. **BFT consensus across multiple operators**. Several organizations run independent PLC nodes; consensus on each operation. Discussed publicly; not deployed.
2. **Bitcoin / blockchain anchoring**. Like did:ion's Sidetree. Slow but decentralized. Not on Bluesky's near-term roadmap.
3. **Migrate to a different DID method**. Users who care can move to did:web today. There is no migration scheme from did:plc to a future fully decentralized method.

As of early 2026, none of these have moved. plc.directory remains operationally centralized. The data model gives Bluesky an exit ramp; whether they take it depends on community pressure and engineering priorities.

## When to use AT Protocol

| Use case | Fit |
|----------|-----|
| Mass-market public social media | Strong fit; production-scale UX |
| Account portability across hosting providers | Strong fit |
| Censorship-resistant identity | Weak fit; use Nostr instead |
| Sovereign-grade identity | Weak fit; use Nostr, KERI, or did:ion |
| Rich record schemas (lexicons) | Strong fit |
| End-to-end encrypted messaging | Not a fit; ATProto is public by design (use Marmot on Nostr or Signal) |

## Primary sources

- [NIPs README: NIP-26 status](https://github.com/nostr-protocol/nips)

- Bluesky, *AT Protocol Specification*, `atproto.com/specs/atp`.
- Bluesky, *did:plc method spec*, `github.com/did-method-plc/did-method-plc`.
- Bluesky, *AT Protocol Lexicon*, `atproto.com/specs/lexicon`.
- Bluesky, *PLC Directory*, `web.plc.directory`.
- Bluesky, *Account Migration*, `atproto.com/guides/account-migration`.
- W3C, *DID Core 1.0*, 2022. `w3.org/TR/did-core/`.
- AT Protocol public repos — `github.com/bluesky-social/atproto`.
- Reference PLC mirror implementations — `github.com/did-method-plc`.
