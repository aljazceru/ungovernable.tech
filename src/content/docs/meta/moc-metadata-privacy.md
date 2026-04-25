---
title: "MOC - Metadata Privacy"
tags:
  - "meta"
  - "moc"
  - "metadata-resistance"
  - "privacy"
  - "overview"
sidebar: {"label":"MOC - Metadata Privacy"}
---
*A Map of Content for hiding **who, when, where, how often, how big** — the data about communications that often reveals more than the content.*

> "We kill people based on metadata." — Michael Hayden, former NSA Director.

---

## Why Metadata Is Harder

End-to-end encryption protects content. The packet headers, timing, sizes, and routing decisions remain visible. A global passive adversary can correlate flows even without breaking any cipher. Metadata privacy requires *changing* observable patterns, not just hiding payloads.

---

## What Leaks at Each Layer

| Layer | Visible to | What it reveals |
|-------|-----------|----------------|
| TCP/IP | Any on-path observer | Source IP, destination IP, ports, timing, sizes |
| TLS | Same | SNI (until ECH), certificate chain, ALPN |
| Application protocols | Server, traffic analyst | Auth tokens, request paths, identifiers |
| DNS | Resolver, ISP | Every domain you look up |
| Cloud control planes | Cloud provider | Workload location, scale, access patterns |
| Database | Server | Which records you read (unless [Overview - Private Information Retrieval](/cryptography/overview-private-information-retrieval)) |

---

## Defenses by Mechanism

### Network-level mixing

[Overview - Mix Networks](/mix-networks/overview-mix-networks) — Tor, Nym, Katzenpost, I2P. Layered encryption + path multiplicity. Loopix-style mixnets add latency + cover traffic for stronger guarantees against global adversaries.

### Sealed sender / metadata-light envelopes

- **Signal sealed sender** — sender identity is encrypted to the recipient; the server sees only the recipient.
- **Nostr NIP-17 gift wrap** — wraps DM events in a public-key-encrypted envelope so relays can't see the social graph.
- **SimpleX queue model** — pairwise queues addressed by random IDs; no user accounts.

### Private retrieval

[Overview - Private Information Retrieval](/cryptography/overview-private-information-retrieval) — fetch records without revealing the index. Practical for DNS, certificate transparency, key servers, LLM RAG.

### Padding & cover traffic

- **Constant-rate fills** — WireGuard's keepalives, Loopix loops, Tor v3 padding.
- **Length padding** — message-length flooring so sizes don't leak.

### Onion-routed authentication

- **Tor v3 client authorization** — only authorized keys can connect to a hidden service; the access log doesn't even see attempts.
- **Hashcash / blind tokens** — pay or prove human-ness without identifying.

### Timing decorrelation

- **Asynchronous messaging** — store-and-forward with random delivery delay.
- **Batching** — Mixmaster's classic "send when N arrived"; modern variants in Katzenpost.

---

## Useful Patterns

### "Sealed message over a mixnet"

Signal Protocol envelope + Nym SURBs (single-use reply blocks) → recipient can reply without learning sender's network identity.

### "Confidential RAG"

PIR over a public corpus + FHE-evaluated retrieval scoring + TEE-hosted LLM with no logging.

### "Ephemeral peer ID"

did:peer or per-relationship keypairs so persistent ID doesn't leak across contexts. Foundation of [Overview - Identity & Pseudonymity](/identity/overview-identity-pseudonymity).

---

## Files Most Relevant

- [Overview - Mix Networks](/mix-networks/overview-mix-networks)
- [Overview - Private Information Retrieval](/cryptography/overview-private-information-retrieval)
- [Overview - Encrypted Messaging](/encrypted-messaging/overview-encrypted-messaging)
- [Overview - Confidential Computing](/confidential-computing/overview-confidential-computing)
- [Confidential-AI-Inference](/confidential-computing/confidential-ai-inference)
- [Overview - Identity & Pseudonymity](/identity/overview-identity-pseudonymity)

---

## Reading List

- Roger Dingledine et al., *Tor: The Second-Generation Onion Router*, USENIX 2004.
- Piotrowska et al., *The Loopix Anonymity System*, USENIX 2017.
- Chen et al., *Vuvuzela: Scalable Private Messaging Resistant to Traffic Analysis*, SOSP 2015.
- Angel & Setty, *Unobservable Communication over Fully Untrusted Infrastructure*, OSDI 2016 (Pung).

