---
title: "Identity"
tags:
  - "identity"
  - "pseudonymity"
  - "nostr"
  - "reputation"
  - "proof-of-personhood"
  - "sybil-resistance"
sidebar: {"label":"Overview","order":0}
---
*Identity rooted in cryptographic keys rather than institutional verification. Pseudonymity is treated as a feature, and reputation comes from behavior rather than credentials.*

---

## Why it matters

The legacy identity model relies on verification through institutions (governments, banks, social platforms). Each can freeze, revoke, or expose your identity. Key-based pseudonymous identity inverts this: the identity is the keypair, and reputation accumulates through action, not approval.

This model is the basis for:
- Censorship-resistant communication (Nostr, encrypted messaging)
- Sybil-resistant governance (DAO voting, airdrop distribution)
- Privacy-preserving access (age gates, content filters without identity)
- Self-sovereign reputation (no platform can delete your history)

---

## Core primitives

### Key-based identity

Instead of a username/password or OAuth, the identity is a cryptographic keypair:

| Format | Purpose | Example |
|--------|---------|---------|
| **npub/nsec** | Nostr keys (Bech32) | `npub1...` / `nsec1...` |
| **hex pubkey** | Raw format | `32-character hex string` |
| **did:key** | Self-contained DID | `did:key:z6Mk...` |

The private key (`nsec`) signs messages; the public key (`npub`) identifies you. Lose the private key and the identity is gone. There is no recovery and no reset.

### Nostr identity model

Nostr (Notes and Other Stuff Transmitted by Relays) was the first widely deployed key-based identity:

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

Properties:
- No email, phone, or identity document required.
- No central server owns the account.
- No terms of service that can ban you.
- The identity persists as long as the key does.

### NIP-05: human-readable verification

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

Now `alice@domain.com` resolves to the public key. This gives:
- Verification: clients confirm the key owns the domain.
- Spoofing resistance: the mapping cannot be faked without domain control.
- Lightning addresses: `alice@domain.com` doubles as an `lnurl1...` payment endpoint.

---

## Pseudonymity patterns

### The pseudonymity spectrum

| Level | Description | Example |
|-------|-------------|---------|
| **Anonymous** | No identifier, no history | Tor-only poster |
| **Pseudonymous** | Persistent key-identity, no real name | Most Nostr users |
| **Verified-pseudo** | Key linked to domain/NIP-05 | `alice@domain.com` |
| **Named-pseudo** | Persistent handle, real name optional | `@alice` on Nostr |
| **Real-named** | Keys linked to legal identity | Worldcoin, government VC |

### Multiple identities

Sophisticated users keep separate keypairs for different contexts:

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

Each identity is independent. There is no link between them unless the user chooses to correlate.

Tools for managing multiple identities:
- nostr-crypt for encrypted key storage.
- GnuPG with the SSH agent for key management.
- Hardware wallets for cold storage of the main identity.

### AI agent identity

A pattern that has emerged: AI agents get their own Nostr identity.

- **Keychat Agent** gives each AI agent a sovereign pubkey.
- **ZK-Dev** (ETHGlobal 2025) proves code contributions without revealing identity.
- **Agent authentication** uses NIP-26 to delegate signing from a human to an agent.

---

## Reputation systems

### Trust scoring in Nostr

Nostr implements reputation through the follow graph:

```
Your follows ──────────► First degree (trusted)
    │
    └──► Their follows ──► Second degree (transitive)
           │
           └──► ... ───────► Nth degree (diminishing trust)
```

Scoring approaches:

| Method | Description |
|--------|-------------|
| **Social distance** | Path length from you = trust weight |
| **PageRank** | Global influence based on incoming follows |
| **GrapeRank** (Taltech) | Average score × average influential followers |
| **Proof of Work** | Zap (Lightning payments) as reputation signal |
| **Muted list propagation** | Block lists propagate through network |

### Trust metrics

Nostr WoT tools (nostr-wot on GitHub):
- Dijkstra path-finding for trust scores.
- BFS for reachability.
- Local clustering for community detection.

Proof of Usefulness (2023+):
- Measures trust through actual network activity.
- Combines social graph, Lightning zaps, and engagement.
- Targets Sybil attacks against pure graph-based trust.

### Reputation beyond Nostr

| System | Approach |
|--------|----------|
| **Gitcoin Passport** | Sybil-resistant scoring via credentials |
| **Rabbithole** | Proof-of-work quests = reputation |
| **Lens Protocol** | Follow graph + engagement = profile score |
| **Farcaster** | Social graph + verified accounts |

---

## Proof of personhood

When pseudonymity is not enough and the goal is "one human, one vote", proof-of-personhood systems provide Sybil resistance.

### Active systems

| Project | Method | Controversy |
|---------|--------|-------------|
| **Worldcoin** | Orb (iris scanning) → biometric hash | Centralized hardware, biometric collection |
| **Idena** | CAPTCHA + synchronous validation sessions | Energy-intensive, session coordination |
| **Proof of Humanity** | Video submission + KYC + community voting | Centralized KYC, human review |
| **BrightID** | Social graph verification (no biometrics) | Relies on existing verified humans |

### ZK-based approaches

Recent research combines ZK proofs with minimal verification:

- **Semaphore** proves membership in a set without revealing which member.
- **Rarimo** runs ZK over government IDs to prove "I have a passport" without the ID number.
- **Anon Aadhaar** proves Indian Aadhaar holdership without revealing the number.

### Trade-offs

| Approach | Privacy | Sybil Resistance | UX Complexity |
|----------|---------|------------------|----------------|
| Biometric (Worldcoin) | Low | Very High | Medium |
| Social Graph (BrightID) | High | Medium | Low |
| ZK + Minimal ID (Rarimo) | High | High | Medium |
| CAPTCHA (Idena) | High | Medium | High (sync sessions) |

---

## Attack vectors and mitigations

### Key compromise

- **Attack:** Private key stolen or lost.
- **Mitigation:** Hardware wallet, multi-sig (experimental), social recovery (emerging).

### Sybil attack

- **Attack:** Create many fake identities to manipulate reputation.
- **Mitigation:** Proof of personhood, proof of work or zaps, path-length thresholds.

### Reputation farming

- **Attack:** Pump reputation through Sybils, then dump.
- **Mitigation:** Temporal weighting (older follows weigh more), crosslinking requirements.

### Domain hijacking

- **Attack:** Compromise a domain to redirect NIP-05 mappings.
- **Mitigation:** DNSSEC, client-side key pinning.

### Linkage attacks

- **Attack:** Correlate multiple pseudonyms to de-anonymize.
- **Mitigation:** Pairwise DIDs, onion routing, avoiding fingerprintable behavior.

---

## Relation to other topics

### Confidential computing

- TEE-backed credentials can bind to Nostr keys.
- Attestation can stand in for proof of personhood without biometrics.
- Private LLM endpoints can use key-based identity plus TEE verification.

### Web of trust

- The Nostr follow graph is an implicit WoT.
- NIP-26 delegation is a form of trust propagation.
- Trust scoring algorithms (nostr-wot) apply WoT concepts.

### Decentralized DNS

- NIP-05 uses DNS for verification.
- ENS names can link to Nostr keys.
- A `.onion` address plus Nostr produces a self-authenticating, censorship-resistant identity.

### Encrypted messaging

- Nostr DMs went from NIP-04 (legacy, deprecated for metadata leakage) to NIP-44 (modern cipher) to **NIP-17 with NIP-59 gift-wrap (current)** for metadata protection. See [Nostr Deep Dive](/encrypted-messaging/nostr-deep-dive).
- Key-based identity enables E2EE without a prior handshake.
- PGP keys can link to Nostr for cross-identity verification.
- For groups: see [Marmot Protocol](/encrypted-messaging/marmot-protocol) (MLS over Nostr).

---

## Evidence at a glance

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

## Related files

- [Overview - Decentralized Identity](/identity/overview-decentralized-identity) — Formal DID/VC systems
- [Overview - Web of Trust](/cryptography/overview-web-of-trust) — Trust graph algorithms, OpenPGP WoT
- [Overview - Encrypted Messaging](/encrypted-messaging) — Nostr DMs, E2EE
- [Overview - Decentralized DNS](/decentralized-dns) — NIP-05, ENS integration
- [Overview - Zero-Knowledge Proofs](/zero-knowledge) — ZK reputation, selective disclosure
- [Overview - Confidential Computing](/confidential-computing) — TEE-based identity verification

---

## Primary sources

- Nostr Protocol: `nostr-protocol.org`, GitHub `nostr-protocol/nips`
- NIP-05 Specification: `nips.nostr.com/05`
- nostr-wot: `github.com/nostr-wot`
- Idena: `idena.io`
- Worldcoin: `worldcoin.org`
- BrightID: `brightid.org`
- Blockchain Commons Pseudonymity Guide: `github.com/BlockchainCommons/Pseudonymity-Guide`

