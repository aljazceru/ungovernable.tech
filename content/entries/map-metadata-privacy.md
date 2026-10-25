---
title: "Map: Metadata Privacy"
slug: map-metadata-privacy
type: map
pillars: ["anonymity", "messaging"]
description: "A map of metadata privacy: hiding who, when, where, how often and how much, which often reveals more than the content of communications."
dek: "A Map of Content for hiding who, when, where, how often, and how big — the data about communications that often reveals more than the content itself."
updated: 2026-10-25
created: 2026-04-25
origin: vault
source: "00 - Meta/MOC - Metadata Privacy.md"
tags: ["meta", "moc", "metadata-resistance", "privacy", "overview"]
---



## Why metadata is harder

End-to-end encryption protects content. Packet headers, timing, sizes, and routing decisions stay visible. A global passive adversary can correlate flows without breaking any cipher. Metadata privacy requires changing observable patterns, not just hiding payloads.

## What leaks at each layer

| Layer | Visible to | What it reveals |
|-------|-----------|----------------|
| TCP/IP | Any on-path observer | Source IP, destination IP, ports, timing, sizes |
| TLS | Same | ClientHello fields such as SNI/ALPN unless protected; TLS 1.3 encrypts the server certificate |
| Application protocols | Server, traffic analyst | Auth tokens, request paths, identifiers |
| DNS | Resolver, ISP | Every domain you look up |
| Cloud control planes | Cloud provider | Workload location, scale, access patterns |
| Database | Server | Which records you read (unless [Overview - Private Information Retrieval](/kb/private-information-retrieval/)) |

## Defenses by mechanism

### Network-level mixing

[Overview - Mix Networks](/kb/mix-networks/) covers Tor, Nym, Katzenpost, and I2P. Layered encryption combined with path multiplicity. Loopix-style mixnets add latency and cover traffic for stronger guarantees against global adversaries.

### Sealed sender and metadata-light envelopes

- Signal sealed sender: the sender identity is encrypted to the recipient, so the server only sees the recipient.
- Nostr NIP-17 gift wrap: gift wraps conceal the original sender but expose the recipient’s public key and delivery timing.
- SimpleX queue model: pairwise queues addressed by random IDs, with no user accounts.

### Private retrieval

[Overview - Private Information Retrieval](/kb/private-information-retrieval/) lets a client fetch records without revealing the index. Practical for DNS, certificate transparency, key servers, and LLM RAG.

### Padding and cover traffic

- Cover traffic and padding: Loopix adds cover messages; Tor has padding mechanisms. WireGuard persistent keepalives preserve NAT mappings and are not constant-rate traffic-analysis protection.
- Length padding: message-length flooring so sizes do not leak.

### Onion-routed authentication

- Tor v3 client authorization: only authorized keys can connect to a hidden service. The access log does not even see attempts.
- Hashcash and blind tokens: pay or prove human-ness without identifying yourself.

### Timing decorrelation

- Asynchronous messaging: store-and-forward with random delivery delay.
- Batching: Mixmaster's classic "send when N arrived"; modern variants in Katzenpost.

## Useful patterns

### Sealed message over a mixnet

Signal Protocol envelope plus Nym SURBs (single-use reply blocks). The recipient can reply without learning the sender's network identity.

### Confidential RAG

PIR over a public corpus, FHE-evaluated retrieval scoring, and a TEE-hosted LLM with no logging.

### Ephemeral peer ID

did:peer or per-relationship keypairs so a persistent ID does not leak across contexts. Foundation of [Overview - Identity & Pseudonymity](/kb/identity-and-pseudonymity/).

## Files most relevant

- [Overview - Mix Networks](/kb/mix-networks/)
- [Overview - Private Information Retrieval](/kb/private-information-retrieval/)
- [Overview - Encrypted Messaging](/kb/encrypted-messaging/)
- [Overview - Confidential Computing](/kb/confidential-computing/)
- [Confidential-AI-Inference](/kb/confidential-ai-inference/)
- [Overview - Identity & Pseudonymity](/kb/identity-and-pseudonymity/)

## Primary sources

- [Tor: The Second-Generation Onion Router](https://www.usenix.org/conference/13th-usenix-security-symposium/tor-second-generation-onion-router)
- [The Loopix Anonymity System](https://www.usenix.org/conference/usenixsecurity17/technical-sessions/presentation/piotrowska)
- [Pung: Unobservable Communication over Fully Untrusted Infrastructure](https://www.usenix.org/conference/osdi16/technical-sessions/presentation/angel)
- [RFC 8446: TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446.html)
- [Nostr NIP-59: visible recipient tags](https://github.com/nostr-protocol/nips/blob/master/59.md)
- [WireGuard: persistent keepalives](https://www.wireguard.com/quickstart/)
- [Signal: sealed sender](https://signal.org/blog/sealed-sender/)
- [Vuvuzela: Scalable Private Messaging Resistant to Traffic Analysis](https://pdos.csail.mit.edu/papers/vuvuzela:sosp15.pdf)
