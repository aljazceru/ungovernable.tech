---
title: "Overview - Identity & Pseudonymity"
tags:
  - "identity"
  - "pseudonymity"
  - "nostr"
  - "reputation"
  - "proof-of-personhood"
  - "sybil-resistance"
---
*Identity rooted in cryptographic keys rather than institutional verification — where pseudonymity is a feature, not a bug, and reputation emerges from behavior, not credentials.*

---

## Why It Matters

The legacy identity model requires verification through institutions — governments, banks, social platforms — each of which can freeze, revoke, or expose your identity. Key-based pseudonymous identity inverts this: your identity *is* your keypair, and reputation accumulates through action, not approval.

This model is fundamental to:
- **Censorship-resistant communication** (Nostr, encrypted messaging)
- **Sybil-resistant governance** (DAO voting, airdrop distribution)
- **Privacy-preserving access** (age gates, content filters without identity)
- **Self-sovereign reputation** (no platform can delete your history)

---

## Core Primitives

### Key-Based Identity

Instead of username/password or OAuth, your identity is a cryptographic keypair:

| Format | Purpose | Example |
|--------|---------|---------|
| **npub/nsec** | Nostr keys (Bech32) | `npub1...` / `nsec1...` |
| **hex pubkey** | Raw format | `32-character hex string` |
| **did:key** | Self-contained DID | `did:key:z6Mk...` |

The private key (`nsec`) signs messages; the public key (`npub`) identifies you. Lose the private key = lose the identity. No recovery, no reset.

### Nostr Identity Model

Nostr (Notes and Other Stuff Transmitted by Relays) pioneered modern key-based identity:

```
┌─────────────────────────────────────────────────────────┐
│                    Nostr Identity                       │
├─────────────────────────────────────────────────────────┤
│  Keypair: npub (identity) + nsec (auth)                │
│      │                                                   │
│      ├──► Sign events (notes, DMs, follows)             │
│      │                                                   │
│      └──► Choose relays (your feed, your publisher)     │
└─────────────────────────────────────────────────────────┘
```

**Properties:**
- No email, phone, or identity document required
- No central server owns your account
- No "terms of service" that can ban you
- Your identity persists as long as you hold the key

### NIP-05: Human-Readable Verification

Raw keys are unwieldy. NIP-05 maps public keys to human-readable identifiers:

```
# Request
GET /.well-known/nostr.json?npub=npub1...

# Response
{
  "names": {
    "alice": "abc123...hexpubkey"
  }
}
```

Now `alice@domain.com` = your public key. This provides:
- **Verification** — clients confirm the key owns the domain
- **Spoofing resistance** — can't fake the mapping without domain control
- **Lightning addresses** — `alice@domain.com` = lnurl1... payment

---

## Pseudonymity Patterns

### The Pseudonymity Spectrum

| Level | Description | Example |
|-------|-------------|---------|
| **Anonymous** | No identifier, no history | Tor-only poster |
| **Pseudonymous** | Persistent key-identity, no real name | Most Nostr users |
| **Verified-pseudo** | Key linked to domain/NIP-05 | `alice@domain.com` |
| **Named-pseudo** | Persistent handle, real name optional | `@alice` on Nostr |
| **Real-named** | Keys linked to legal identity | Worldcoin, government VC |

### Multiple Identities

Sophisticated users maintain separate keypairs for different contexts:

```
┌─────────────────────────────────────────────────────┐
│            Identity Segregation                    │
├─────────────────────────────────────────────────────┤
│  Work Identity    ──► Professional content, DMs    │
│  Personal Identity ──► Friends, family            │
│  activist Identity ──► Political, sensitive        │
│  Degen Identity  ──► Trading, gambling             │
│  AI Agent Identity ──► Automated services          │
└─────────────────────────────────────────────────────┘
```

Each identity is independent — no link between them unless you choose to correlate.

Tools for managing multiple identities:
- **nostr-crypt** — encrypted key storage
- **GnuPG + SSH agent** — key management
- **Hardware wallets** — cold storage for main identity

### AI Agent Identity

Emerging pattern: AI agents get their own Nostr identity:

- **Keychat Agent** — each AI agent has sovereign pubkey
- **ZK-Dev** (ETHGlobal 2025) — prove code contributions without revealing identity
- **Agent authentication** — delegatable signing (NIP-26) from human to agent

---

## Reputation Systems

### Trust Scoring in Nostr

Nostr implements reputation through the **follow graph**:

```
Your follows ──────────► First degree (trusted)
    │
    └──► Their follows ──► Second degree (transitive)
           │
           └──► ... ───────► Nth degree (diminishing trust)
```

**Scoring approaches:**

| Method | Description |
|--------|-------------|
| **Social distance** | Path length from you = trust weight |
| **PageRank** | Global influence based on incoming follows |
| **GrapeRank** (Taltech) | Average score × average influential followers |
| **Proof of Work** | Zap (Lightning payments) as reputation signal |
| **Muted list propagation** | Block lists propagate through network |

### Trust Metrics

**Nostr WoT** tools (nostr-wot GitHub):
- Dijkstra path-finding for trust scores
- BFS for reachability
- Local clustering for community detection

**Proof of Usefulness** (2023+):
- Measures trust through *actual network activity*
- Combines social graph + Lightning zaps + engagement
- Addresses Sybil attacks in pure graph-based trust

### Reputation beyond Nostr

| System | Approach |
|--------|----------|
| **Gitcoin Passport** | Sybil-resistant scoring via credentials |
| **Rabbithole** | Proof-of-work quests = reputation |
| **Lens Protocol** | Follow graph + engagement = profile score |
| **Farcaster** | Social graph + verified accounts |

---

## Proof of Personhood

When pseudonymity isn't enough — when you need "one human, one vote" — proof of personhood systems provide Sybil resistance:

### Active Systems

| Project | Method | Controversy |
|---------|--------|-------------|
| **Worldcoin** | Orb (iris scanning) → biometric hash | Centralized hardware, biometric collection |
| **Idena** | CAPTCHA + synchronous validation sessions | Energy-intensive, session coordination |
| **Proof of Humanity** | Video submission + KYC + community voting | Centralized KYC, human review |
| **BrightID** | Social graph verification (no biometrics) | Relies on existing verified humans |

### ZK-Based Approaches

Emerging research combines ZK proofs with minimal verification:

- **Semaphore** — proof of membership in a set without revealing which
- **Rarimo** — ZK over government IDs, prove "I have a passport" without ID number
- **Anon Aadhaar** — prove Indian Aadhaar holder without revealing number

### Trade-offs

| Approach | Privacy | Sybil Resistance | UX Complexity |
|----------|---------|------------------|----------------|
| Biometric (Worldcoin) | Low | Very High | Medium |
| Social Graph (BrightID) | High | Medium | Low |
| ZK + Minimal ID (Rarimo) | High | High | Medium |
| CAPTCHA (Idena) | High | Medium | High (sync sessions) |

---

## Attack Vectors and Mitigations

### Key Compromise

- **Attack:** Private key stolen or lost
- **Mitigation:** Hardware wallet, multi-sig (experimental), social recovery (emerging)

### Sybil Attack

- **Attack:** Create many fake identities to manipulate reputation
- **Mitigation:** Proof of personhood, proof of work/zaps, path-length thresholds

### Reputation Farming

- **Attack:** Pump reputation through sybil then dump
- **Mitigation:** Temporal weighting (older follows = more weight), crosslinking requirements

### Domain Hijacking

- **Attack:** Compromise domain to redirect NIP-05 mappings
- **Mitigation:** DNSSEC, client-side key pinning

### Linkage Attacks

- **Attack:** Correlate multiple pseudonyms to de-anonymize
- **Mitigation:** Pairwise DIDs, onion routing, avoiding fingerprintable behavior

---

## Relation to Other Topics

### Confidential Computing

- TEE-backed credentials can bind to Nostr keys
- Attestation as "proof of personhood" without biometrics
- Private LLM endpoints with key-based identity + TEE verification

### Web of Trust

- Nostr follow graph *is* an implicit WoT
- NIP-26 delegation = trust propagation
- Trust scoring algorithms (nostr-wot) apply WoT concepts

### Decentralized DNS

- NIP-05 uses DNS for verification
- ENS names can link to Nostr keys
- `.onion` + Nostr = self-authenticating, censorship-resistant identity

### Encrypted Messaging

- Nostr DMs use NIP-04 (encrypted with recipient pubkey)
- Key-based identity enables E2EE without prior handshake
- PGP keys can link to Nostr (cross-identity verification)

---

## Evidence at a Glance

| Implementation | Type | Maturity | Status |
|---------------|------|----------|--------|
| **Nostr (key-based)** | Protocol | Mature | Active, widely deployed |
| **NIP-05** | Verification | Mature | Standard, widely supported |
| **nostr-wot** | Trust scoring | Emerging | Active development |
| **Worldcoin** | PoP | Mature | 10M+ users, controversial |
| **Idena** | PoP | Active | Ongoing validation sessions |
| **BrightID** | Social PoP | Active | Growing adoption |
| **ZK-Dev** | ZK reputation | Experimental | Hackathon prototype |

---

## Related Files

- [Overview - Decentralized Identity](/identity/overview-decentralized-identity) — Formal DID/VC systems
- [Overview - Web of Trust](/cryptography/overview-web-of-trust) — Trust graph algorithms, OpenPGP WoT
- [Overview - Encrypted Messaging](/encrypted-messaging/overview-encrypted-messaging) — Nostr DMs, E2EE
- [Overview - Decentralized DNS](/decentralized-dns/overview-decentralized-dns) — NIP-05, ENS integration
- [Overview - Zero-Knowledge Proofs](/zero-knowledge/overview-zero-knowledge-proofs) — ZK reputation, selective disclosure
- [Overview - Confidential Computing](/confidential-computing/overview-confidential-computing) — TEE-based identity verification

---

## Primary Sources

- Nostr Protocol: `nostr-protocol.org`, GitHub `nostr-protocol/nips`
- NIP-05 Specification: `nips.nostr.com/05`
- nostr-wot: `github.com/nostr-wot`
- Idena: `idena.io`
- Worldcoin: `worldcoin.org`
- BrightID: `brightid.org`
- Blockchain Commons Pseudonymity Guide: `github.com/BlockchainCommons/Pseudonymity-Guide`
