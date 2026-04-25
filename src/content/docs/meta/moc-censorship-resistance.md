---
title: "MOC - Censorship Resistance"
tags:
  - "meta"
  - "moc"
  - "censorship-resistance"
  - "overview"
---
*A Map of Content for the cross-cutting theme of resisting takedown, blocking, and content removal across the network stack.*

> **What is censorship resistance?** The property that no single entity — registrar, host, ISP, payment processor, app store — can unilaterally remove or block content. Achieved by removing single points of control: decentralized naming, P2P transport, self-custodied keys, alternative payment rails.

---

## The Censorship Stack

| Layer | Choke point in legacy stack | Decentralized alternatives |
|-------|-----------------------------|----------------------------|
| **Naming** | Registrars, ICANN, TLD operators | [Overview - Decentralized DNS](/decentralized-dns/overview-decentralized-dns) — ENS, Handshake, PKARR, Tor `.onion` |
| **TLS** | Certificate Authorities | Attested TLS in TEEs, key-pinned protocols, Tor authenticated services |
| **Transport** | ISP routing, DPI | [Overview - Mix Networks](/mix-networks/overview-mix-networks), [Overview - Off-Grid Networks](/off-grid-networks/overview-off-grid-networks) |
| **Hosting** | Cloud providers, hyperscaler ToS | [Overview - Decentralized Compute](/decentralized-compute/overview-decentralized-compute), self-hosting, Tor hidden services |
| **Application** | Platform moderation | [Overview - Encrypted Messaging](/encrypted-messaging/overview-encrypted-messaging) — Nostr, SimpleX, Matrix federations |
| **Payment** | Banks, card networks, Stripe | [Overview - Financial Sovereignty](/financial-sovereignty/overview-financial-sovereignty) — Bitcoin, Lightning |
| **Identity** | KYC providers, government IDs | [Overview - Decentralized Identity](/identity/overview-decentralized-identity), [Overview - Identity & Pseudonymity](/identity/overview-identity-pseudonymity) |

---

## Recurring Patterns

### 1. Self-authenticating identifiers

When the **name is the key**, no registry can move it. Examples: Tor v3 onion, Nostr npub, PKARR records, did:key, Bitcoin addresses.

### 2. Permissionless write paths

When anyone can publish, content moderation must happen at the *read* side. Examples: Nostr relays, Bitcoin txs, BitTorrent DHT, IPFS.

### 3. Code transparency

When the binary is publicly reproducible and logged, takedown attempts are observable. Examples: Apple PCC transparency log, Sigstore, deterministic builds.

### 4. Layered redundancy

When traffic can fall back to alternative transports, blocking one doesn't sever the channel. Examples: Tor pluggable transports, Reticulum over heterogeneous links, Briar over Bluetooth/Wi-Fi/Tor.

---

## Reference Stacks

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

See [Confidential-AI-Inference](/confidential-computing/confidential-ai-inference) and [Private-LLM-Inference-Patterns](/confidential-computing/private-llm-inference-patterns).

### Maximum-resistance social account

```
Nostr keypair (your local file)
   ↓
Posts signed locally → broadcast to many relays
   ↓
NIP-05 over PKARR or .onion (no DNS dependency)
   ↓
Lightning zaps for monetization
```

---

## Threat Model Themes

- **Takedown via choke point** — addressed by removing the choke point.
- **Sanctions / financial deplatforming** — addressed by self-custodied money.
- **Court order on operator** — addressed by no-knowledge architectures (E2EE, sealed-sender, attested TEEs without persistence).
- **Mass deplatforming of consumers** — addressed by app stores being optional (web, sideloading, alternative app stores).

---

## Files Most Relevant

- [Overview - Decentralized DNS](/decentralized-dns/overview-decentralized-dns)
- [Overview - Mix Networks](/mix-networks/overview-mix-networks)
- [Overview - Off-Grid Networks](/off-grid-networks/overview-off-grid-networks)
- [Overview - Decentralized Compute](/decentralized-compute/overview-decentralized-compute)
- [Overview - Encrypted Messaging](/encrypted-messaging/overview-encrypted-messaging)
- [Overview - Financial Sovereignty](/financial-sovereignty/overview-financial-sovereignty)
- [Overview - Confidential Computing](/confidential-computing/overview-confidential-computing)
- [Confidential-AI-Inference](/confidential-computing/confidential-ai-inference)

