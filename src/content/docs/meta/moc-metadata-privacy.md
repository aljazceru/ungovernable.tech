---
title: "Metadata Privacy"
tags:
  - "meta"
  - "moc"
  - "metadata-resistance"
  - "privacy"
  - "overview"
---
*A Map of Content for hiding who, when, where, how often, and how big — the data about communications that often reveals more than the content itself.*

> "We kill people based on metadata." — Michael Hayden, former NSA Director.

---

## Why metadata is harder

End-to-end encryption protects content. Packet headers, timing, sizes, and routing decisions stay visible. A global passive adversary can correlate flows without breaking any cipher. Metadata privacy requires changing observable patterns, not just hiding payloads.

---

## What leaks at each layer

| Layer | Visible to | What it reveals |
|-------|-----------|----------------|
| TCP/IP | Any on-path observer | Source IP, destination IP, ports, timing, sizes |
| TLS | Same | SNI (until ECH), certificate chain, ALPN |
| Application protocols | Server, traffic analyst | Auth tokens, request paths, identifiers |
| DNS | Resolver, ISP | Every domain you look up |
| Cloud control planes | Cloud provider | Workload location, scale, access patterns |
| Database | Server | Which records you read (unless [Overview - Private Information Retrieval](/cryptography/overview-private-information-retrieval)) |

---

## Defenses by mechanism

### Network-level mixing

[Overview - Mix Networks](/mix-networks) covers Tor, Nym, Katzenpost, and I2P. Layered encryption combined with path multiplicity. Loopix-style mixnets add latency and cover traffic for stronger guarantees against global adversaries.

### Sealed sender and metadata-light envelopes

- Signal sealed sender: the sender identity is encrypted to the recipient, so the server only sees the recipient.
- Nostr NIP-17 gift wrap: DM events are wrapped in a public-key-encrypted envelope so relays cannot see the social graph.
- SimpleX queue model: pairwise queues addressed by random IDs, with no user accounts.

### Private retrieval

[Overview - Private Information Retrieval](/cryptography/overview-private-information-retrieval) lets a client fetch records without revealing the index. Practical for DNS, certificate transparency, key servers, and LLM RAG.

### Padding and cover traffic

- Constant-rate fills: WireGuard keepalives, Loopix loops, Tor v3 padding.
- Length padding: message-length flooring so sizes do not leak.

### Onion-routed authentication

- Tor v3 client authorization: only authorized keys can connect to a hidden service. The access log does not even see attempts.
- Hashcash and blind tokens: pay or prove human-ness without identifying yourself.

### Timing decorrelation

- Asynchronous messaging: store-and-forward with random delivery delay.
- Batching: Mixmaster's classic "send when N arrived"; modern variants in Katzenpost.

---

## Useful patterns

### Sealed message over a mixnet

Signal Protocol envelope plus Nym SURBs (single-use reply blocks). The recipient can reply without learning the sender's network identity.

### Confidential RAG

PIR over a public corpus, FHE-evaluated retrieval scoring, and a TEE-hosted LLM with no logging.

### Ephemeral peer ID

did:peer or per-relationship keypairs so a persistent ID does not leak across contexts. Foundation of [Overview - Identity & Pseudonymity](/identity).

---

## Files most relevant

- [Overview - Mix Networks](/mix-networks)
- [Overview - Private Information Retrieval](/cryptography/overview-private-information-retrieval)
- [Overview - Encrypted Messaging](/encrypted-messaging)
- [Overview - Confidential Computing](/confidential-computing)
- [Confidential-AI-Inference](/confidential-computing/confidential-ai-inference)
- [Overview - Identity & Pseudonymity](/identity)

---

## Reading list

- Roger Dingledine et al., *Tor: The Second-Generation Onion Router*, USENIX 2004.
- Piotrowska et al., *The Loopix Anonymity System*, USENIX 2017.
- Chen et al., *Vuvuzela: Scalable Private Messaging Resistant to Traffic Analysis*, SOSP 2015.
- Angel & Setty, *Unobservable Communication over Fully Untrusted Infrastructure*, OSDI 2016 (Pung).

