---
title: "Map: Censorship Resistance"
slug: map-censorship-resistance
type: map
pillars: ["circumvention"]
description: "A map of censorship resistance across the stack: naming, storage, transport, messaging and publishing, and how the pieces in this library combine."
dek: "A Map of Content for the cross-cutting theme of resisting takedown, blocking, and content removal across the network stack."
updated: 2026-04-28
created: 2026-04-25
origin: vault
source: "00 - Meta/MOC - Censorship Resistance.md"
tags: ["meta", "moc", "censorship-resistance", "overview"]
---

> Censorship resistance is the property that no single entity (registrar, host, ISP, payment processor, app store) can unilaterally remove or block content. It comes from removing single points of control: decentralized naming, P2P transport, self-custodied keys, alternative payment rails.

## The censorship stack

| Layer | Choke point in the legacy stack | Decentralized alternatives |
|-------|-----------------------------|----------------------------|
| Naming | Registrars, ICANN, TLD operators | [Overview - Decentralized DNS](/kb/decentralized-dns/) — ENS, Handshake, PKARR, Tor `.onion` |
| TLS | Certificate Authorities | Attested TLS in TEEs, key-pinned protocols, Tor authenticated services |
| Transport | ISP routing, DPI | [Overview - Mix Networks](/kb/mix-networks/), [Overview - Off-Grid Networks](/kb/off-grid-networks/) |
| Hosting | Cloud providers, hyperscaler ToS | [Overview - Decentralized Compute](/kb/decentralized-compute/), self-hosting, Tor hidden services |
| Storage | Object stores, CDNs, account bans | [Overview - Decentralized Storage](/kb/decentralized-storage/) — IPFS, Arweave, Filecoin, Blossom |
| Application | Platform moderation | [Overview - Encrypted Messaging](/kb/encrypted-messaging/) — Nostr, SimpleX, Matrix federations |
| Payment | Banks, card networks, Stripe | [Overview - Financial Sovereignty](/kb/financial-sovereignty/) — Bitcoin, Lightning |
| Identity | KYC providers, government IDs | [Overview - Decentralized Identity](/kb/decentralized-identity/), [Overview - Identity & Pseudonymity](/kb/identity-and-pseudonymity/) |

## Recurring patterns

### 1. Self-authenticating identifiers

When the name is the key, no registry can move it. Examples: Tor v3 onion, Nostr npub, PKARR records, did:key, Bitcoin addresses.

### 2. Permissionless write paths

When anyone can publish, content moderation has to happen at the read side. Examples: Nostr relays, Bitcoin txs, BitTorrent DHT, IPFS, Arweave, Blossom mirrors.

### 3. Code transparency

When the binary is publicly reproducible and logged, takedown attempts are observable. Examples: Apple PCC transparency log, Sigstore, deterministic builds.

### 4. Layered redundancy

When traffic can fall back to alternative transports, blocking one does not sever the channel. Examples: Tor pluggable transports, Reticulum over heterogeneous links, Briar over Bluetooth, Wi-Fi, and Tor.

## Reference stacks

### Maximum-resistance LLM endpoint

```
PKARR or .onion
   ↓
Attested TLS bound to enclave key
   ↓
Confidential VM (TDX/SEV-SNP) + H100 CC
   ↓
Open-weights model + transparency-logged build
   ↓
Lightning paywall (no KYC)
```

See [Confidential-AI-Inference](/kb/confidential-ai-inference/) and [Private-LLM-Inference-Patterns](/kb/private-llm-inference-patterns/).

### Maximum-resistance social account

```
Nostr keypair (your local file)
   ↓
Posts signed locally → broadcast to many relays
   ↓
Media on Blossom servers → mirrored by SHA-256
   ↓
NIP-05 over PKARR or .onion (no DNS dependency)
   ↓
Lightning zaps for monetization
```

### Sovereign node (no internet, no banks, no cloud)

```
Local AI inference
   ↓
LoRa mesh (MeshCore / Meshtastic / Blackout)
   ↓
Cashu ecash (now with TEE mint path) + Bitcoin
   ↓
Encrypted chunked comms + local maps
```

See [MeshCore](/kb/meshcore/), [Cashu and Chaumian Ecash](/kb/cashu-ecash/), and new composition examples in [MOC - Composing Primitives](/kb/map-composing-primitives/).

## Threat model themes

- Takedown via choke point: addressed by removing the choke point.
- Sanctions or financial deplatforming: addressed by self-custodied money.
- Court order on operator: addressed by no-knowledge architectures (E2EE, sealed-sender, attested TEEs without persistence).
- Mass deplatforming of consumers: addressed by app stores being optional (web, sideloading, alternative app stores).

## Files most relevant

- [Overview - Decentralized DNS](/kb/decentralized-dns/)
- [Overview - Mix Networks](/kb/mix-networks/)
- [Overview - Off-Grid Networks](/kb/off-grid-networks/)
- [Overview - Decentralized Compute](/kb/decentralized-compute/)
- [Overview - Decentralized Storage](/kb/decentralized-storage/)
- [Overview - Encrypted Messaging](/kb/encrypted-messaging/)
- [Overview - Financial Sovereignty](/kb/financial-sovereignty/)
- [Overview - Confidential Computing](/kb/confidential-computing/)
- [Confidential-AI-Inference](/kb/confidential-ai-inference/)
