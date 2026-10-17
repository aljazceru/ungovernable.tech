---
title: "Session"
slug: session-messenger
type: deep-dive
pillars: ["messaging"]
readiness: usable
description: "Session, a messenger that needs no phone number and routes messages over an onion network of nodes: how it works and its cryptographic trade-offs."
dek: "A messenger that uses an X25519 keypair as the only identifier (no phone number, no email) and routes messages over the Oxen Service Node onion network. Storage relays hold encrypted messages for offline recipients. Originally a Signal Protocol fork; replaced X3DH with a simpler onion-routed key agreement; still uses Double Ratchet for direct conversations. Funded by the $OXEN token; that's both its strength (incentivized infrastructure) and its main critique (token economics, smaller deployment)."
updated: 2026-04-26
created: 2026-04-26
origin: vault
source: "07-Encrypted-Messaging/Session.md"
aliases: ["Session Messenger", "Oxen Session", "Loki Messenger"]
tags: ["session", "oxen", "lokinet", "onion-routing", "e2ee", "no-phone", "x25519", "deep-dive"]
---

## Identity = X25519 keypair

Open Session, generate a keypair, you have a **Session ID**:

```
05 [32-byte X25519 public key in hex]
e.g.   05a3b7e1f2c9...   (66 hex chars total)
```

That's the entire identity. No phone number, no email, no display name needed at the protocol layer. Two users connect by exchanging Session IDs (QR codes, scrap of paper, another channel). There is no centralized directory.

This is the same primitive as Signal's username-based contacts (introduced 2024) but Session has done it from day one (2019).

The `05` prefix is a version/network byte. Underneath, identity is a Curve25519 keypair, and message authentication uses Ed25519-from-X25519 conversions where signatures are needed.

## Routing: Oxen Service Nodes

Where Signal has central servers and SimpleX has relay queues, Session uses a global onion-routed network of **Oxen Service Nodes** (formerly Loki Service Nodes; the project rebranded from Loki to Oxen in 2021 to escape the OPM/Lazarus naming overlap).

Each Service Node is a server staked by some operator with $OXEN tokens. Service Nodes:

- Run Lokinet (a Tor-like onion-routed mixnet, separate product from Session itself).
- Participate in **Session's storage layer**: a Service Node group ("swarm") holds encrypted messages for accounts whose Session ID falls in a particular range of the keyspace.
- Earn $OXEN block rewards for being online and serving requests.

When Alice sends a message to Bob:

1. Alice's client encrypts the message to Bob's X25519 public key.
2. Alice constructs an onion-routed path through three Service Nodes.
3. The exit node delivers the message to Bob's swarm (the Service Nodes responsible for his Session ID).
4. The swarm stores the encrypted blob.
5. When Bob next polls his swarm (push notifications via APNs/FCM are a separate question), he downloads waiting messages.

Bob's IP is never exposed to Alice; Alice's IP is never exposed to the swarm; the swarm cannot decrypt the content.

This is what Session means when it says "no phone number, no metadata." The metadata is real — it includes "this Session ID has stored messages on this swarm" — but the user-IP-to-Session-ID linkage that Signal exposes (via account creation, push tokens, contact discovery) is genuinely absent.

## Cryptography

### Content encryption

For 1:1 chats Session uses **Double Ratchet** — the same Signal Protocol primitive, with the X25519 keypair as the long-term identity input. Forward secrecy and post-compromise security via Diffie-Hellman ratcheting on every message round-trip.

Originally Session used Signal's full X3DH for session setup. In **2020 they replaced X3DH with a simpler onion-routed handshake** because X3DH's prekey publishing model assumed central servers and Session didn't have those. The simpler design reuses long-term identity keys for initial key derivation; the trade-off is that the very-first-message has weaker forward secrecy than Signal's prekey design provides.

### Group messaging

Session has used several group designs:

- **Closed groups** — Sender Keys (Signal-style): a shared symmetric key per group, rotated on member changes. O(N) cost per change, weak post-compromise security at group level.
- **Open groups (community servers)** — server-relayed, lighter encryption, public-channel use case.
- **MLS-style groups (2024+)** — Session has been integrating an MLS-derived design (TreeKEM, RFC 9420) for stronger group security. As of 2026 this is rolling out alongside the older closed-group implementation.

The MLS migration mirrors what Wire ([Wire MLS](/kb/mls-wire/)) did earlier and what [Marmot Protocol](/kb/marmot-protocol/) is doing in the Nostr ecosystem — the industry has converged on MLS as the right primitive for large encrypted groups.

## Comparison

| Property | Signal | Session | SimpleX |
|----------|--------|---------|---------|
| User identifier | Phone (or username 2024+) | X25519 pubkey (Session ID) | None |
| Phone number required | Yes (or username) | No | No |
| Onion routing built-in | No (sealed sender helps) | Yes (Oxen Service Nodes) | No (use Tor manually) |
| Content E2EE | Double Ratchet + X3DH/PQXDH | Double Ratchet, simpler setup | Double Ratchet |
| Asynchronous delivery | Yes (Signal servers) | Yes (Service Node swarms) | Yes (SMP queues) |
| Post-quantum | PQXDH (2023+) | No public deployment plan | Hybrid Kyber (2023+) |
| Funding model | Signal Foundation (Brian Acton donation, donations) | $OXEN token + grants | Grants + venture |
| Self-hostable infrastructure | No (server is open but the network is closed) | Run a Service Node (requires staking $OXEN) | Yes, run an SMP relay |
| Adoption (2026) | Hundreds of millions | ~1M active (estimated) | ~200K-500K active |

## Tokenomics critique

Session is funded by the Oxen Privacy Tech Foundation, whose original revenue model is the **$OXEN token** (formerly $LOKI). Service Node operators stake $OXEN to run nodes; block rewards (15,000-coin emissions) pay them; the foundation funds development.

The honest critiques:

- **Token incentives can drift from user welfare.** The economic incentive is to operate Service Nodes and serve requests, not to advocate for users against subpoenas or jurisdictional pressure.
- **Service-node operator concentration.** As with most PoS networks, operator distribution skews. A handful of operators run a substantial fraction of nodes.
- **Project governance.** OPTF is registered in Australia. Australian legislation (Assistance and Access Act 2018) gives authorities broad capabilities to compel technical assistance. Session has stated they would refuse / publicize, but the legal framework is real.
- **Rug-pull risk.** A token-funded project depends on token price to fund development. The 2022 crypto winter visibly stressed many such projects; Session survived, but the dependency is structural.

Counterarguments:

- The economic incentive does buy real, distributed infrastructure that does not concentrate around a single legal entity.
- Service Nodes don't have access to plaintext or to a useful social graph by design; even a fully compromised operator set leaks limited information.
- The codebase is open, the network is verifiable, the token is incidental to message delivery.

For users who want a fully working metadata-light messenger today and are uninterested in self-hosting, Session is one of the few options. For users who want to avoid token-economics governance, SimpleX with Tor or Briar may fit better.

## Threat model

### What Session prevents

- **Server-side social-graph reconstruction by a single operator.** No central server, no operator-account index.
- **IP-to-identity linkage.** Onion routing keeps your IP off your Session ID.
- **Sender-receiver linkage at the swarm.** Senders go through onion paths; receivers poll over onion paths.
- **Plaintext in transit.** Standard E2EE.

### What it doesn't

- **Endpoint compromise.** Same as always.
- **Service-node global passive adversary.** A coordinated entity running enough Service Nodes could perform timing correlation to deanonymize specific traffic. The published Session research argues this is hard at current Service Node counts; it is not impossible.
- **Compromise of Session ID exchange channels.** If an adversary controls how Alice and Bob exchanged IDs, they can MITM at first contact. Out-of-band verification (compare ID strings via voice / in person) addresses this.
- **Quantum.** Curve25519 throughout; no post-quantum option as of 2026.

## Deployment status

- **Clients**: iOS, Android, macOS, Linux, Windows. F-Droid available.
- **License**: GPL-3.0.
- **Audits**: Quarkslab audited the cryptographic core in 2020 ([published findings](https://github.com/oxen-io/oxen-docs)). NCC Group audited Lokinet in 2020. Audit cadence is less frequent than Signal's; 2024-2026 audit transparency is mixed.
- **Users**: official statements claim ~1 million active users; the absence of phone numbers means there's no exact count. Conditional claim: low single-digit millions of installs, hundreds of thousands of active monthly users.

## Operational notes

- Back up your seed phrase (recovery phrase encodes the X25519 private key). Lose it, lose your identity and your message history.
- Push notifications on iOS/Android use Google FCM and Apple APNs as wake-up signals; the actual messages are still pulled by the client over onion paths. The push token is associated with the Session ID at the push-server, which is the one piece of operator-side metadata Session does keep.
- For higher-stakes use, disable push notifications; the client polls instead.
- Run a Session ID alongside SimpleX or Signal as redundancy; treat each as a separate channel for separate threat models.

## Primary sources

- Session whitepaper — [getsession.org/whitepaper](https://getsession.org/whitepaper).
- Oxen documentation — [docs.oxen.io](https://docs.oxen.io).
- Session source — [github.com/oxen-io/session-android](https://github.com/oxen-io/session-android), [session-ios](https://github.com/oxen-io/session-ios), [session-desktop](https://github.com/oxen-io/session-desktop).
- Lokinet (Oxen onion routing) — [lokinet.org](https://lokinet.org).
- Oxen Privacy Tech Foundation — [optf.ngo](https://optf.ngo).
- Quarkslab audit (2020) — published in OPTF blog and GitHub.
- Marlinspike & Perrin, "The Double Ratchet Algorithm" (2016).
- Australian Assistance and Access Act 2018 — [legislation.gov.au](https://www.legislation.gov.au/Details/C2018A00148) (jurisdictional context).
