---
title: "Identity and Pseudonymity"
slug: identity-and-pseudonymity
type: explainer
pillars: ["identity"]
description: "Identity rooted in cryptographic keys instead of institutions: why pseudonymity matters, how identities get linked, and how to keep them apart."
dek: "Identity rooted in cryptographic keys rather than institutional verification. Pseudonymity is treated as a feature, and reputation comes from behavior rather than credentials."
updated: 2026-10-25
created: 2026-04-19
origin: vault
source: "11-Identity/Overview - Identity & Pseudonymity.md"
aliases: ["Pseudonymous Identity", "Key-Based Identity", "Reputation Systems"]
tags: ["identity", "pseudonymity", "nostr", "reputation", "proof-of-personhood", "sybil-resistance"]
---

## Why it matters

The legacy identity model relies on verification through institutions (governments, banks, social platforms). Each can freeze, revoke, or expose your identity. Key-based pseudonymous identity inverts this: the identity is the keypair, and reputation accumulates through action, not approval.

This model is the basis for:
- Censorship-resistant communication (Nostr, encrypted messaging)
- Sybil-resistant governance (DAO voting, airdrop distribution)
- Privacy-preserving access (age gates, content filters without identity)
- Self-sovereign reputation (no platform can delete your history)

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

### DID:Nostr — W3C DID method for Nostr keys (2025–2026)

The W3C Nostr Community Group published a draft DID method specification for `did:nostr` in 2025–2026, enabling Nostr secp256k1 keys to function as full W3C Decentralized Identifiers:

```
did:nostr:124c0fa99407182ece5a24fad9b7f6674902fc422843d3128d38a0afbee0fdd2
```

**What it adds over raw npubs:**

- Standard W3C DID document format — Nostr keys become resolvable through the global DID ecosystem.
- Multikey verification method: BIP-340 x-only secp256k1 keys transformed into Verifiable Credentials Data Integrity format via multicodec.
- Optional service endpoints pointing to Nostr relays.
- `alsoKnownAs` field linking to other DIDs or platform identities (with privacy caveats — this creates public linkage).
- Profile field derived from kind 0 events (name, about, picture, timestamp).
- `follows` field derived from kind 3 contact lists for social graph attestation.

**Resolution:**

- HTTP: `https://<domain>/.well-known/did/nostr/<pubkey>.json`
- Minimal resolution requires only the DID itself — no network needed for basic verification.
- Enhanced resolution queries Nostr relays for metadata and NIP-05 endpoints.

**Important constraints:**
- **No update operation** — DID documents are immutable snapshots derived from on-network events.
- **No delete/revoke** — the DID cannot be voluntarily removed from the ecosystem.
- DIDs use raw hex public keys, not Bech32 npubs.

The specification is a W3C Community Group draft, not a W3C Standard. See [nostrcg/did-nostr](https://github.com/nostrcg/did-nostr) and the rendered spec at [nostrcg.github.io/did-nostr](https://nostrcg.github.io/did-nostr/).

### HTTP Schnorr Signature Authentication (W3C CG draft)

A sibling specification from the W3C Nostr Community Group defines how to authenticate HTTP requests using Schnorr signatures — the same primitives used in Nostr and Bitcoin Taproot:

```
Authorization: Nostr <base64-encoded-signed-json-event>
```

The event contains the request URL, HTTP method, and timestamp, signed by the user's keypair. This enables:

- **Decentralized HTTP authentication** without passwords, OAuth, or session cookies.
- Seamless Nostr identity as an HTTP auth credential.
- Privacy-preserving: no account registration, no shared secrets stored server-side.

Specification at [nostrcg.github.io/http-schnorr-auth](https://nostrcg.github.io/http-schnorr-auth/). This is a research-grade draft, but the combination of `did:nostr` + HTTP Schnorr Auth points toward a world where a single secp256k1 keypair serves as: Nostr identity, DID identifier, HTTP authentication credential, and Lightning payment sender.

### 2026 custody stack: signers, bunkers, threshold keys

The largest live change since the first version of this note is that Nostr identity is moving away from "paste the `nsec` into every app" toward dedicated custody layers. See [Nostr Key Custody and Recovery](/guides/nostr-key-custody/) for the deep dive. The short version:

| Layer | Standard / project | What it changes | Maturity signal |
|---|---|---|---|
| Browser signer | [NIP-07](https://nips.nostr.com/07) | Web clients ask an extension to sign; they do not hold the `nsec` | Widely deployed |
| Remote signer / bunker | [NIP-46](https://nips.nostr.com/46) | Clients communicate with a phone, daemon, server, or hardware signer over encrypted Nostr events | Active standard; Amber and bunker tools exist |
| Android signer | [Amber](https://github.com/greenart7c3/Amber) | Smartphone acts as the user's Nostr signing device | Active GitHub development; pushed 2026-04-29 |
|| Threshold signing | [Frostr](https://opensats.org/projects/frostr), [Bifrost](https://github.com/FROSTR-ORG/bifrost), [Igloo Server](https://github.com/FROSTR-ORG/igloo-server) | Split the identity key into shares; any quorum signs without reconstructing the `nsec` | OpenSats-funded; active 2026 repos; FROST NIST submission and Hermine PQ variant give long-term standardization path |
| Trust assertions | [NIP-85](https://nips.nostr.com/85) | Signed provider outputs for ranks, follower counts, zaps, reports, and WoT metrics | Draft/optional; cross-client deployment in Amethyst, Primal, Coracle as of Q1–Q2 2026 |

This matters because key-rooted identity only works at civilizational scale if users can survive stolen phones, malicious clients, dead laptops, and organizational turnover without giving control back to platforms.

## Pseudonymity patterns

### The pseudonymity spectrum

| Level | Description | Example |
|-------|-------------|---------|
| **Anonymous** | No identifier, no history | Tor-only poster |
| **Pseudonymous** | Persistent key-identity, no real name | Most Nostr users |
| **Verified-pseudo** | Key linked to domain/NIP-05 | `alice@domain.com` |
| **Named-pseudo** | Persistent handle, real name optional | `@alice` on Nostr |
| **Real-named** | Keys linked to legal identity | Government VC, EUDI wallet |

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

A pattern that has emerged: AI agents get their own Nostr identity. Key developments:

**NIP-26: Delegated Event Signing — unrecommended**

The NIPs README marks this proposal as unrecommended. The following describes the historical proposal, not a recommended custody pattern.
- Allows key delegation: Authorize another keypair (agent) to publish on your behalf.
- Time-bounded permissions (e.g., "can post for 30 days").
- Used by AI agents that need to act on behalf of humans.

**NIP-EE: MLS End-to-End Encryption**
- Uses the Messaging Layer Security (MLS) protocol for Nostr.
- Nostr identity key is NOT used for MLS encryption — compromise of npub doesn't expose messages.
- Supports group messaging with key agreement.

**Agent Directory (agentdex.id)**
- Open directory for AI agents on Nostr.
- Agents register with npub, capabilities, framework, model.
- Kind 31339 events for agent metadata.
- Can be claimed via NIP-05 (e.g., `agent@agentdex.id`).

**Keychat**
- OpenClaw plugin that gives each AI agent a sovereign pubkey.
- Agents can be added as contacts and messaged directly.

**Frostr (OpenSats 2025-2026 grant)**
- Multi-device signing, key rotation, share replacement.
- Enabled by FROST (Friendly Out-of-order Threshold Signatures).
- Projects: Frost, Bifrost, nostrp2p + clients (Igloo, Frost2x, Heimdall, Frostbite, Permafrost).

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

## Proof of personhood

When pseudonymity is not enough and the goal is "one human, one vote", proof-of-personhood systems provide Sybil resistance.

### Active systems

| Project | Method | Controversy | Status |
|---------|--------|-------------|--------|
| **Idena** | CAPTCHA + synchronous validation sessions | Energy-intensive, session coordination | Active |
| **Proof of Humanity** | Video submission + KYC + community voting | Centralized KYC, human review | Stalled |
| **BrightID** | Social graph verification (no biometrics) | Relies on existing verified humans | Active, growing |

### Rarimo (2025+)

Rarimo launched its ZK Roll-up in March 2025, backed by $2.5M from Vitalik Buterin and others:

- **ZK Identity Registry**: Register credentials once, prove membership infinitely.
- **Freedom Tool**: Prove "I am a citizen of X" without revealing your ID.
- **ZK Voting**: Anonymous voting with ZK proofs that every voter is eligible.
- **RariMe wallet**: Self-custody ZK wallet generating zero-knowledge proofs for identity verification.

Trade-off: Requires government-issued ID for initial verification → higher trust but lower pseudonymity.

### Cryptographic Framework for Proof of Personhood (2026)

A notable 2026 academic paper from IACR (*A Cryptographic Framework for Proof of Personhood*, eprint 2026/333) formalized the problem with two credential types:

- **Personhood Credentials (PHCs)**: issued by trusted authorities to attest to uniqueness and basic attributes (e.g., "is a unique human, age > 18").
- **Verifiable Relationship Credentials (VRCs)**: issued peer-to-peer to capture reputation and real-world interactions (e.g., "Alice and Bob have met").

The paper provides formal security definitions — Sybil-resistance, authenticated personhood, and unlinkability across contexts — and efficient cryptographic constructions combining PHCs, VRCs, and ZK proofs. This is the most rigorous treatment of the problem to date and useful for anyone designing or evaluating PoP systems.

### Semaphore

Privacy-oriented ZK identity from Privacy & Scaling Explorations:

- Proves membership in a set (e.g., "I am a verified human") without revealing which member.
- Used forAnonymous moderation, reputation, and blocking.
- Cannot prove specific attributes — only membership.

### Anon Aadhaar

Proves Indian Aadhaar holdership without revealing the Aadhaar number. Use cases: age verification, residency proof.

### Trade-offs

| Approach | Privacy | Sybil Resistance | UX Complexity |
|----------|---------|------------------|----------------|
| Social Graph (BrightID) | High | Medium | Low |
| ZK + Minimal ID (Rarimo) | High | High | Medium |
| CAPTCHA (Idena) | High | Medium | High (sync sessions) |

## Attack vectors and mitigations

### Key compromise

- **Attack:** Private key stolen or lost. On Nostr, the public key *is* the account, so key compromise is identity compromise and key loss is account loss.
- **Mitigation:** dedicated signers (NIP-07 / Amber), remote signing (NIP-46), hardware-backed signing where available, threshold custody via Frostr/FROST, and out-of-band migration statements signed by old/new keys plus trusted peers.
- **Status:** NIP-46 is usable today; Amber is active; Frostr/Bifrost/Igloo are promising but still emerging. See [Nostr Key Custody and Recovery](/guides/nostr-key-custody/).

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

- Nostr DMs went from NIP-04 (legacy, deprecated for metadata leakage) to NIP-44 (modern cipher) to **NIP-17 with NIP-59 gift-wrap (current)** for metadata protection. See [Nostr Deep Dive](/kb/nostr-protocol/).
- Key-based identity enables E2EE without a prior handshake.
- PGP keys can link to Nostr for cross-identity verification.
- For groups: see [Marmot Protocol](/kb/marmot-protocol/) (MLS over Nostr).

## Evidence at a glance

| Implementation | Type | Maturity | Status |
|---------------|------|----------|--------|
| **Nostr (key-based)** | Protocol | Mature | Active, widely deployed; `nostr-protocol/nips` pushed 2026-04-29 |
| **NIP-05** | Verification | Mature | Standard, widely supported; depends on DNS/TLS unless bridged to PKARR/.onion |
| **NIP-07** | Browser signer | Mature | Common web-client interface for local signers |
| **NIP-46** | Remote signer / bunker | Active | Standardized remote signing; avoids giving every client the raw `nsec` |
| **Amber** | Android signer | Active | GitHub active through 2026-04-29; practical mobile custody |
| **Frostr / Bifrost / Igloo** | Threshold key custody | Emerging | OpenSats-funded; active 2026 repos; solves single-device loss/compromise |
| **NIP-26 delegation** | Delegated event signing | Unrecommended | The NIPs README advises against it |
| **NIP-85** | Trusted assertions | Draft / optional | Signed reputation/ranking metrics; early services and repos |
| **nostr-wot** | Trust scoring | Emerging | Active 2026 repos; social-distance / oracle pattern |
| **wot-scoring (joelklabo)** | PageRank WoT scoring | Emerging | Publishes NIP-85 kind 30382/30383/30384/30385 events; browser extension |
| **did:nostr** | W3C DID method | Draft | W3C Nostr CG; secp256k1 as DID identifier; no update/delete operations |
| **HTTP Schnorr Auth** | Auth mechanism | Draft | W3C CG; Nostr keys as HTTP auth credentials; research-grade |
| **Pubky** | Key-rooted identity + DHT discovery | Active | `pubky/pubky-core` active through 2026-05-01; Ed25519 + PKARR |
| **Rarimo / Semaphore / Anon Aadhaar** | ZK identity / PoP | Emerging | Useful for eligibility proofs, but weaker pseudonymity if rooted in government ID |
| **Cryptographic PoP Framework** | Academic / formal | Research | IACR eprint 2026/333; PHC + VRC formalization; foundational |
| **agentdex / Keychat-style agents** | Agent identity | Experimental | Agents owning keys directly; early ecosystem |

## Mid-May 2026 Developments

This week brought several notable Nostr ecosystem updates worth tracking:

### Ecosystem Integrations

**Primal Android — NIP-46 + NIP-55 signing hub (May 2026)**
Primal Android shipped NIP-46 remote signing and NIP-55 local signer support, making Android a full signing hub for other apps on the same device. This is a significant step in the signer-per-device pattern: instead of every app holding its own `nsec`, apps can delegate signing to a dedicated signer app. This reduces key exposure surface and aligns with the NIP-46 bunker architecture.

**White Noise v0.3.0 — Amber + real-time messaging (May 2026)**
White Noise shipped v0.3.0 with 160+ merged improvements, including real-time messaging and Amber signer integration. The Amber integration extends the Android signer ecosystem to another client, and real-time messaging indicates continued investment in Nostr as a protocol rather than just a microblogging platform.

**Mostro P2P Bitcoin trading — public beta (May 2026)**
Mostro, a P2P Bitcoin trading app built on Nostr, shipped its first public beta after three years of development. This demonstrates Nostr's utility beyond social media — it can serve as a transport and identity layer for marketplace interactions. The key implication: your Nostr keypair can serve as identity for a decentralized exchange without KYC.

**NIP-42 relay AUTH + protected events — cross-app rollout (May 2026)**
OAuth Bunker, Amber, and strfry added NIP-42 (`AUTH` command for relay-client authentication) and protected-event support across app, signer, and relay software. This strengthens relay-level access control and prevents unauthorized write access to relays.

**rust-nostr SDK — major API redesign (May 2026)**
rust-nostr shipped a 21-PR architecture overhaul of its SDK, indicating active protocol development. Major SDK refactors typically signal that lower-level tooling is stabilizing and the ecosystem is investing in developer experience.

**Zeus + Cashu + NIP-47 improvements (May 2026)**
Zeus shipped 17 merged PRs focused on NIP-47 (Nostr Wallet Connect) fixes and Cashu (Chaumian e-cash) improvements, strengthening the Lightning + Nostr integration for mobile wallet use cases.

### Protocol Maturation Pattern

These developments — signer hubs, relay AUTH, SDK refactor, P2P trading beta — suggest the Nostr identity stack is moving from "key in every app" toward a layered custody model. The mid-May 2026 pattern mirrors the broader trend documented in the 2026 custody stack table: dedicated signers, relay-level access control, and NIP-85 trust assertions are all converging toward a composable identity layer rather than a monolithic client-key relationship.

## Late-May 2026 Developments

### FROST RFC 9591 Published (June 2024 — Now Active Standard)

The IRTF published [RFC 9591](https://datatracker.ietf.org/doc/rfc9591/) — the FROST Protocol — in June 2024, giving threshold Schnorr signatures a stable public specification. For Nostr's Frostr ecosystem, this provides the normative reference that library implementations (Bifrost, Igloo, frost-java) can be measured against. The RFC specifies the signing protocol but does not standardize distributed key generation, leaving trusted-dealer and DKG approaches as implementation choices. Nonce reuse remains the critical footgun: one reused nonce leaks the secret share.

### NIP-26 Delegation Revocation (GitHub Issue #654)

NIP-26 is marked unrecommended in the NIPs README. Historical discussion of delegation revocation should not be read as current endorsement. NIP-46 remote signing does not depend on NIP-26 delegation.

The proposed solution: the root private key can sign a revocation certificate for the delegation key, which is then distributed to relays. Clients must treat events signed by the revoked delegation key as invalid once the revocation certificate is validated. This adds a critical missing piece to the delegation model: consent revocation without waiting for expiry. The issue is open and awaiting NIP spec endorsement.

### Cross-Client WoT Trust Score Display (Q1 2026)

Multiple independent Nostr clients began displaying WoT-based trust scores in their UI during Q1 2026. Amethyst (Android), Primal, and Coracle all show trust scores on user profiles, indicating cross-client convergence on the WoT visibility pattern. Amethyst's changelog notes that "by connecting to a WoT provider, you can see trust scores and verified follower counts directly on user pictures. This helps filter signal from noise." Coracle displays a trust indicator with the message: "If you can't tell the difference between me and a scammer, use a nostr client with web of trust support."

This is significant because WoT is transitioning from developer-facing library features to user-visible product features. The practical implication: ordinary users are now seeing trust metadata surfaced by their clients, creating both better spam filtering and new design questions about how to present trust without creating a surveillance-score aesthetic.

### OpenPGP WoT: PGPainless WoT Module and u4/u5 Identifiers

The NLnet/NGI Assure-funded PGPainless WoT module (based on Sequoia-PGP's published WoT specification) continues active development, adding Java/Kotlin path computation to an ecosystem that has historically omitted it. For Android email tools and server-side OpenPGP workflows, this fills a tooling gap.

A notable new development is the [OpenPGP ID u4/u5 specification](https://foopgp.org/blog/2026-04-28-openpgp-id-spec/) (draft submitted to IETF, in production use in Djibian OS):

- **u4** (human identifier): derived from birth surname + given names + date of birth, processed through MD5 and Base64url encoding. Produces a 39-character identifier that fits in an OpenPGP UID comment field. Pseudonymous — the identifier is permanent (does not change on marriage, name change, or naturalisation) but the raw inputs remain private.

- **u5** (universal identifier for anything): Unix timestamp + geographic coordinates, identifying any entity by its moment and place of origin. Used for AI agents, software components, or humans who prefer not to disclose civil data.

For WoT purposes, u4/u5 represents an attempt to build persistent pseudonymous identity on OpenPGP certificates without a central registry.

### NIP-26 revocation as key-recovery partial

NIP-26 is unrecommended; its proposed extensions are not a basis for a new recovery plan. See [Nostr Key Custody and Recovery](/guides/nostr-key-custody/) for signing-device and custody considerations.

## Early-June 2026 Developments

### nips repository active — 2,978 stars, pushed 2026-05-31

The [nostr-protocol/nips](https://github.com/nostr-protocol/nips) repository shows active maintenance with 2,978 stars and a push on 2026-05-31. This is the canonical NIP spec repository — its continued activity means the protocol is still being refined. The 2,978-star count reflects broad ecosystem investment in the specification layer.

### rust-nostr SDK v0.3 — 843 stars, pushed 2026-05-19

[nbd-wtf/nostr-tools](https://github.com/nbd-wtf/nostr-tools) (843 stars) and the broader rust-nostr ecosystem remain active through mid-May 2026. The rust-nostr SDK shipped a 21-PR architecture overhaul in May 2026 (per the mid-May developments). The 843-star count indicates rust-nostr is the dominant Rust implementation and the reference for several production relay and client projects.

### Amber Android signer — 314 stars, pushed 2026-05-30

[greenart7c3/Amber](https://github.com/greenart7c3/Amber) hit 314 stars with a push on 2026-05-30, making it the highest-starred dedicated Nostr signer app. The push date confirms active maintenance as of late May 2026. Amber remains the reference Android implementation for the NIP-07 browser signer API and NIP-46 remote signing flows, handling event previews, approval prompts, and per-app permission scoping on Android.

### Igloo Server + Frostr v2 direction — 8 stars, pushed 2026-05-28

[FROSTR-ORG/igloo-server](https://github.com/FROSTR-ORG/igloo-server) shows 8 stars with a push on 2026-05-28. The Igloo suite is transitioning from a v1 app approach toward Bifrost v2 + self-hostable Igloo Server as the canonical Frostr tooling. The architectural direction is a self-hosted signing server that holds threshold shares and presents a NIP-46 bunker-compatible interface to clients — combining the liveness of a hosted service with the security of threshold custody.

### Bifrost core library — 10 stars, pushed 2026-02-16

[FROSTR-ORG/bifrost](https://github.com/FROSTR-ORG/bifrost) shows 10 stars, last pushed 2026-02-16. The library is the TypeScript Frostr implementation and the foundation for Igloo tooling. The gap from February to May 2026 likely reflects the project being in a design/spec phase rather than active code push — the v2 architectural direction for Igloo may be where Bifrost is being evolved. The OpenSats Frostr grant remains active and the RFC 9591 reference is stable, so this is a normal maturation pause rather than abandonment.

### did:nostr specification — 9 stars, pushed 2026-01-11

The [nostrcg/did-nostr](https://github.com/nostrcg/did-nostr) DID method specification sits at 9 stars with a January 2026 push. The spec is a W3C Community Group draft (not a W3C Standard) and covers mapping secp256k1 keys to the W3C DID document format with multicodec verification methods and optional NIP-05 / relay service endpoints. The spec's immaturity (no update/delete operations, draft status) means active production use is limited to experimental projects, but the DID:Nostr approach remains the canonical path for bridging Nostr key identity into the formal W3C DID ecosystem.

### did:nostr: public-key-as-identity pattern gaining mindshare

The `did:nostr` method and the companion HTTP Schnorr Signature Authentication draft (both from the W3C Nostr Community Group) together represent a maturing identity pattern: a single secp256k1 keypair functioning simultaneously as:

- Nostr account identifier (`npub` / hex pubkey)
- W3C DID (`did:nostr:hexpubkey`)
- HTTP authentication credential (`Authorization: Nostr <base64-signed-event>`)
- Lightning payment sender (zaps, NIP-57)

This convergence is significant for ungovernable infrastructure: it means a user can maintain one cryptographic identity that works across social (Nostr), web authentication (HTTP Schnorr), payments (Lightning), and formal credentials (DID document). The key-custody and key-recovery requirements for that single identity are therefore also shared across all four contexts — which is why the NIP-46 / Frostr / Amber custody stack matters so much.

### OpenPGP WoT: PGPainless last commit September 2025, Sequoia-PGP reference solid

The PGPainless WoT module (NLnet/NGI Assure-funded, Java/Kotlin) last showed significant commits in September 2025 (Gradle 8.8 upgrade), suggesting the funded development phase may be concluding. The module implements path computation based on Sequoia-PGP's published WoT specification, which remains the definitive formal reference for OpenPGP trust path calculation. For the UngovernableTech vault: OpenPGP WoT is at a stable, mature point in its lifecycle rather than a rapid-development phase. The practical takeaway is that Sequoia's specification is what implementations should test against, and PGPainless is the Java/Kotlin integration point.

### Trust score visibility: from library feature to UI default

The cross-client WoT visibility trend noted in late May (Amethyst, Primal, Coracle surfacing trust scores in Q1 2026) has continued into late May. The practical implication for this library's Identity & Pseudonymity and WoT files: trust scores are now a user-facing product feature, not just a developer API. This creates new design questions about how to present trust without an opaque surveillance-score aesthetic, and it means the NIP-85 oracle provider model is becoming load-bearing for mainstream clients that cannot compute the graph locally.

### FROST at NIST MPTS 2026 — EdDSA threshold submission active

FROST was submitted to the NIST Threshold Call (NIST IR 8214C) in 2026, with a preview presentation at MPTS 2026 (NIST Workshop on Multi-Party Threshold Schemes, January 2026). The FROST Team — Chelsea Komlo, Ian Goldberg, Jonathan Katz, Mary Maller, and others — published a preview writeup (version 0.1, March 2026) targeting Category N1.1 (Threshold EdDSA Signing). Key points from the workshop:

- **Adaptive security**: New results on adaptive security of threshold Schnorr signatures were presented, relevant to all FROST implementations including Frostr.
- **Determinism vs. security**: The FROST team explicitly recommended against requiring single-party EdDSA-style determinism in multi-party settings — doing so introduces vulnerabilities even when attempting to mitigate nonce-reuse attacks. This is a directly actionable finding for Frostr and Bifrost implementers.
- **Standardization path**: If FROST is standardized by NIST, it would provide a normative reference for threshold EdDSA that Frostr library implementations could be formally audited against.

For Nostr's Frostr ecosystem specifically: FROST is the cryptographic basis, RFC 9591 is the stable IRTF reference, and the NIST submission represents the path toward government-standardized threshold EdDSA.

### Hermine: post-quantum FROST-like threshold signatures for the PQ migration era

[Hermine](https://hermine-th.org) (eprint 2026/419, presented at MPTS 2026) is a post-quantum lattice-based threshold signature scheme that replicates FROST's feature set under standard lattice assumptions:

- **Design**: FROST-like, partially non-interactive, two-round signing (one preprocessing round + one message-dependent round). Targets medium-scale deployments (N ≤ 64 parties) with ~11KB signatures.
- **Advanced properties**: Identifiable aborts (misbehaving participants are identified and excluded), proactive share refresh (periodic share renewal without changing the public key), and distributed key generation.
- **Security basis**: Standard lattice assumptions (not contingent on exotic assumptions). Aligned with NIST PQC standardization trajectory.
- **PQ migration significance**: If FROST is the classical threshold Schnorr solution, Hermine is the post-quantum counterpart. For long-lived Nostr identities facing quantum threat timelines, Hermine represents the eventual migration path. Proactive refresh is especially valuable for identities that must survive over decade-long horizons — a compromised share can be renewed without rotating the public key.

The Hermine team submitted Hermine as its own package to the NIST Threshold Call, running in parallel with the FROST submission. The coexistence of classical FROST and PQ Hermine in the NIST process reflects the real-world migration planning happening in threshold cryptography: design for classical deployment now, architect for PQ transition later.

### OpenPGP ecosystem: active IETF maintenance (June 2026)

Three active IETF drafts show the OpenPGP ecosystem receiving unusual maintenance attention:

- [draft-gallagher-openpgp-signatures-03](https://datatracker.ietf.org/doc/html/draft-gallagher-openpgp-signatures-03) (June 2026): Grammar and semantics clarifications for OpenPGP signatures — maintenance of RFC 9580 addressing edge cases that cause valid certifications to be rejected or invalid ones accepted.
- [draft-gallagher-openpgp-messages-00](https://datatracker.ietf.org/doc/html/draft-gallagher-openpgp-messages-00): Complementary OpenPGP message grammar updates.
- A new HKP draft addressing v6 certificate handling, v2 key lookup, and content-type requirements for ASCII-armored bundles — affecting WoT-compatible key discovery at the transport layer.

Collectively these drafts signal that OpenPGP, far from being dormant, is under active protocol maintenance — relevant for anyone relying on GPG WoT as part of their identity stack.

## June 14, 2026 — Sunday Weekly Update

### NIP-57 Zap Milestone: 1 Million Zaps

Nostr surpassed 1 million zaps (NIP-57 Lightning payments attached to notes and profiles), confirming that Bitcoin Lightning integration has become a primary reputation signal on Nostr. Zap economics: zaps are Lightning payments, which have a real cost — unlike follows (free) or reactions (free). This cost means zap-based reputation is harder to Sybil-manufacturate than pure social graph signals. The practical consequence for identity: a zap count is a rough proxy for "this content was worth paying for," making it a scarce-signal reputation mechanism. This reinforces the [Overview - Web of Trust](/kb/web-of-trust/) observation that NIP-85's `zap_amt_recd` tag is one of the most meaningful edge weights because it encodes actual economic cost rather than mere social adjacency.

### Primal Android NIP-46 Bunker: Signing Hub Maturation

Primal Android (already noted as a NIP-46 + NIP-55 signing hub in the mid-May update) continues to mature as a full signing hub. The significance: Primal Android joining Amber as a primary Android signer establishes the pattern of **signer-as-mobile-hub**. This is the key architectural pattern for the 2026 custody stack: instead of the phone being one more device holding the raw `nsec`, it becomes the signing authority that other apps query via NIP-46. The identity no longer lives in each app — it lives in the signer, and apps become dumb clients.

### NIP-39 External Identities: Moving to Dedicated Events

A notable NIP evolution: NIP-39 (external identity claims — GitHub, Twitter, etc.) has moved identity tags from kind 0 (profile metadata) to **dedicated kind events**. This separates the data type from the profile blob: separate the data type from the profile blob into its own event kind. The advantage: external identity proofs become independently addressable, delegable, and revokable without touching the user's profile. The privacy implication: external identity tags are no longer stuck in the profile that every relay stores permanently — they can be deleted by publishing a replacement kind 0 without the tags. For pseudonymous users who want to prove GitHub or Twitter ownership without permanent linkage, this is a meaningful privacy improvement.

### Anonymous Aadhaar: ZK Proof of Government ID Without Revealing ID

[Anon Aadhaar](https://anon-aadhaar.com/) continues active development as a zero-knowledge proof system for Indian Aadhaar holders. The use case: prove you hold a valid Aadhaar (the world's largest government ID system, covering ~1.4B people) without revealing the Aadhaar number or any other personal data. The architecture: a smartphone app captures the Aadhaar XML (issued by UIDAI), generates a ZK proof locally, and presents the proof to verifiers. The verifier learns only "this person is a valid Aadhaar holder" — not the number, name, or any other field. For proof-of-personhood in South Asia and the diaspora, Anon Aadhaar is the most deployed ZK+government-ID system in the freedom-tech space. Trade-off: requires trusting the Aadhaar issuance authority — the ZK proof proves you hold a valid credential, not that the credential was legitimately issued.

### WoT Extension: Trust Assertions and Services Integration

The [nostr-wot extension](https://nostr-wot.com) has evolved beyond basic WoT queries to add trust assertions and trusted service discovery. The extension now exposes a `window.nostr.wot` API that web clients can call to ask: "what is my trust distance from this pubkey?" and "which trusted services has this pubkey declared?" The extension also integrates Lightning wallet functions and NIP-07 signing. For the identity picture: this extension is becoming a browser-native identity provider that handles authentication (NIP-07), payments (zaps), and trust scoring (WoT) in one surface. The privacy risk: combining identity, wallet, and trust in one extension concentrates key custody risk. The privacy benefit: instead of each web app holding `nsec` or querying a remote bunker, the browser extension acts as a local secure enclave for the user's full identity stack.

### Marmot Protocol: MLS over Nostr Status

The [Marmot Protocol](https://github.com/lightningrod/marmot) (MLS-based encrypted group messaging over Nostr) continues development as the NIP-17 reference implementation. MLS (Messaging Layer Security) provides:
- **Forward secrecy**: compromised past keys don't decrypt old messages.
- **Post-compromise security**: future messages are secure after a key compromise.
- **Group key agreement**: dynamic group membership without re-keying everyone.
- **Sender ratchet**: each message advances the chain, preventing forward access.

Critically: the Nostr identity key (npub/nsec) is **not** used for MLS encryption. The MLS key agreement happens separately, so a compromised npub does not automatically expose MLS group messages. This is a critical separation: Nostr identity handles social graph and event signing, while MLS handles message-layer confidentiality. For pseudonymous groups, this means even a fully doxxed npub doesn't expose the group's message history.

### Stateless Key Rotation: NIP Issue #103

GitHub issue [#103](https://github.com/nostr-protocol/nips/issues/103) proposes stateless key rotation using a series of hidden commitments derived from an initial seed. The model: instead of one keypair, a user generates a chain of keypairs all derived from a seed, and publishes "I am rotating from key A to key B" events. Old followers can discover the new key by walking backward through the chain from the seed. The benefit: no central key server, no trusted third party, no loss of followers on rotation. The unsolved problem: how do new followers discover the chain if they encounter the user for the first time at key B? They would need an external anchor (domain, NIP-05, or trusted introducer) to bootstrap. This NIP is a draft proposal, not an adopted standard, but it addresses the most critical usability gap in key-rooted identity: key rotation without follower loss.

### NIP-05 + Lightning Address Convergence

The convergence of NIP-05 identifiers and Lightning addresses (`alice@domain.com`) continues to mature. A single domain-hosted JSON file now resolves both:
- The Nostr public key for social identity.
- The Lightning address for payment identity.

This means one human-readable handle anchors both the social layer and the payment layer to the same cryptographic identity. For reputation: zap receipts flow to the same Lightning address that resolves through the same NIP-05 that maps to the npub. The unified handle is significant because it makes reputation portable across social and payment contexts without requiring a platform to bridge them.

### June 14 Evidence Table Update

| Project | Stars | Last Push | Status |
|---------|------:|-----------|--------|
| [nostr-protocol/nips](https://github.com/nostr-protocol/nips) | 2,978 | 2026-05-31 | Active spec maintenance |
| [nbd-wtf/nostr-tools](https://github.com/nbd-wtf/nostr-tools) | 843 | 2026-05-19 | Dominant Rust SDK |
| [greenart7c3/Amber](https://github.com/greenart7c3/Amber) | 314 | 2026-05-30 | Leading Android signer |
| [FROSTR-ORG/igloo-server](https://github.com/FROSTR-ORG/igloo-server) | 8 | 2026-05-28 | Self-hostable Frostr server |
| [FROSTR-ORG/bifrost](https://github.com/FROSTR-ORG/bifrost) | 10 | 2026-02-16 | In spec/design phase |
| [Anon Aadhaar](https://anon-aadhaar.com/) | — | Active | ZK government ID proofs, live deployment |
| [Marmot Protocol](https://github.com/lightningrod/marmot) | — | Active | MLS over Nostr, NIP-17 reference |
| [nostr-wot extension](https://nostr-wot.com) | — | Active | Trust assertions, NIP-07, Lightning wallet |

## Primary sources

- [NIPs README: NIP-26 status](https://github.com/nostr-protocol/nips)
- [NIP-46 remote signing](https://github.com/nostr-protocol/nips/blob/master/46.md)

- [Nostr NIPs](https://github.com/nostr-protocol/nips) and [Nostr protocol specifications](https://nips.nostr.com/)
- [NIP-05](https://nips.nostr.com/05) — DNS-based key aliases
- [NIP-07](https://nips.nostr.com/07) — browser signer API
- [NIP-26](https://nips.nostr.com/26) — delegated event signing
- [NIP-46](https://nips.nostr.com/46) — Nostr remote signing / bunkers
- [NIP-85](https://nips.nostr.com/85) — trusted assertions for ranks, counts, zaps, reports, and WoT metrics
- [DID:Nostr specification](https://nostrcg.github.io/did-nostr/) — W3C Nostr Community Group draft
- [did-nostr GitHub](https://github.com/nostrcg/did-nostr) — specification repository
- [HTTP Schnorr Signature Authentication](https://nostrcg.github.io/http-schnorr-auth/) — W3C CG draft
- [Frostr OpenSats project page](https://opensats.org/projects/frostr), [FROSTR-ORG/bifrost](https://github.com/FROSTR-ORG/bifrost), [FROSTR-ORG/igloo-server](https://github.com/FROSTR-ORG/igloo-server)
- [Amber Android signer](https://github.com/greenart7c3/Amber)
- [nostr-wot organization](https://github.com/nostr-wot), [nostr-wot/nostr-wot](https://github.com/nostr-wot/nostr-wot), [wot-scoring](https://github.com/joelklabo/wot-scoring)
- [Pubky core](https://github.com/pubky/pubky-core), [PKARR](https://pkarr.org/)
- [Verifiable Credentials Data Model v2.0](https://www.w3.org/TR/vc-data-model-2.0/)
|- [FROST paper](https://eprint.iacr.org/2020/852) — Komlo and Goldberg, Flexible Round-Optimized Schnorr Threshold Signatures
- [FROST NIST MPTS 2026 preview writeup](https://csrc.nist.gov/csrc/media/Projects/threshold-cryptography/documents/TCall-1/FROST-PW01.pdf) — FROST Team, version 0.1, March 2026
- [Hermine: Lattice-based FROST-like Threshold Signatures](https://eprint.iacr.org/2026/419) — eprint 2026/419
- [Hermine project website](https://hermine-th.org)
- [Cryptographic Framework for Proof of Personhood](https://eprint.iacr.org/2026/333) — IACR 2026
- [Blockchain Commons Pseudonymity Guide](https://github.com/BlockchainCommons/Pseudonymity-Guide)
- [draft-gallagher-openpgp-signatures-03](https://datatracker.ietf.org/doc/html/draft-gallagher-openpgp-signatures-03) — OpenPGP signature updates, June 2026
- [draft-gallagher-openpgp-messages-00](https://datatracker.ietf.org/doc/html/draft-gallagher-openpgp-messages-00) — OpenPGP message updates
