---
title: "Overview - Decentralized DNS"
tags:
  - "dns"
  - "ens"
  - "handshake"
  - "pkarr"
  - "namecoin"
  - "decentralized"
  - "pubky"
  - "gns"
sidebar: {"hidden":true}
---
*Naming systems that don't depend on ICANN, a TLD registrar, or a CA — because seizure, sanctions, and content-based takedowns flow through exactly those choke points.*

---

## Why It Matters

The legacy DNS + X.509 trust chain has five choke points: root zone operators, TLD registries, domain registrars, recursive resolvers, and CAs. Any of them can be compelled — or compromised — to remove, redirect, or spy on a domain. Encrypted transports (DoH/DoT) shift who can snoop but don't solve the governance problem.

### The Seizure Problem

Recent examples demonstrate why decentralized naming matters:

- **2023**: ICANN rejected .ONION renewal for privacy tools, creating operational chaos
- **2022-2024**: Russian authorities seized .RU domains en masse
- **2024**: sanctions-driven domain seizures affecting crypto projects
- **Ongoing**: Content-based takedowns via UDRP, URS, and court orders

The fundamental issue: **legacy DNS ties your identity to a registrar's database entry** — and that entry can be modified, deleted, or transferred without your consent.

---

## Historical Context

### Early Pioneers (1990s-2010)

| Year | Development | Significance |
|------|-------------|---------------|
| 1991 | **PGP web of trust** | First decentralized identity (keys, not names) |
| 1997 | **DNSSEC** (RFC 2065) | Authenticated DNS records — didn't solve governance |
| 1998 | **OpenPGP (RFC 2440)** | Formalized key signing |
| 2011 | **Namecoin** | First functional blockchain DNS, merged-mined with Bitcoin |
| 2017 | **ENS launched** | Ethereum-based naming goes live |
| 2018 | **Handshake (HNS)** | Public testnet — proposes replacing the root zone itself |

### The Modern Era (2020-2026)

| Year | Development | Significance |
|------|-------------|---------------|
| 2020 | **ENS v2 planning** | Layer 2 support, gas optimization |
| 2023 | **PKARR/Pubky** | DHT-based naming using existing P2P infra |
| 2024 | **ENS gas reductions** | 99% reduction in registration costs |
| 2025 | **ENS stays on L1** | Abandoned Namechain L2, focused on L1 scaling |
| 2025 | **GNUnet 0.26.0** | RFC 9498 published — GNS standardized |
| 2026 | **PKDNS launches** | Production DNS server for PKARR resolution |

---

## Approaches

### 1. Blockchain-Anchored Names

These systems store name records on a blockchain, using the blockchain as the source of truth for ownership.

#### ENS (Ethereum Name Service)

**.eth names registered on Ethereum; usable as wallet addresses, content hashes (IPFS), DIDs.**

| Feature | Detail |
|---------|--------|
| **Registry** | Ethereum smart contract |
| **TLD** | .eth only |
| **Cost** | ~$5-50/year (gas fluctuates) |
| **Resolution** | ENS contracts → resolver → records |
| **Resolver** | PublicResolver, CCIP-read for off-chain |
| **Governance** | DAO + multi-sig |

**2025-2026 Developments:**

- **99% gas reduction**: Ethereum gas limit increases (30M → 60M in 2025) made ENS registrations affordable
- **ENSv2**: Abandoned Namechain L2 plan; focusing on L1 scaling
- **2026 outlook**: Average ENS price forecast ~$15, stable adoption
- **CCIP-read**: Off-chain data resolution (IPFS, HTTPS) widely adopted

**Resources:**

- [docs.ens.domains](https://docs.ens.domains)
- [ens.domains](https://ens.domains)

#### Handshake (HNS)

**Replaces the DNS root zone with a blockchain; you can own your own TLD.**

| Feature | Detail |
|---------|--------|
| **Registry** | Handshake blockchain |
| **TLD** | Any (you own your own root) |
| **Cost** | One-time (auction + renewal) |
| **Resolution** | Handshake resolvers |
| **Mining** | PoW-style mining |
| **Governance** | Permissionless |

**Status (2026):**

- Active but niche (~0.5¢ HNS price)
- Halving scheduled July 2026
- Integration work ongoing (cDNSd)
- Minimal mainstream adoption

**Resources:**

- [handshake.org](https://handshake.org)
- [HNSd resolver](https://github.com/handshake-org/hnsd)

#### Namecoin

**Original blockchain DNS (2011). Still running; small user base.**

- Oldest blockchain naming system
- .bit TLD
- Merged-mined with Bitcoin
- Very small ecosystem but longest track record

#### Unstoppable Domains

**Centralized company selling blockchain names; user lock-in concerns.**

- Sells .crypto, .wallet, etc.
- **Warning**: Centralized company — can freeze/transfer names
- Not truly decentralized despite marketing

---

### 2. Public-Key-Addressed Names

**Names *are* public keys.** No blockchain, no registrar — just cryptographic identity.

#### PKARR (Public-Key-Addressable Resource Records)

**Names are Ed25519 public keys; DHT (Mainline/BitTorrent) stores signed DNS records under the key. No blockchain; used in Pubky / Slashtags.**

| Feature | Detail |
|---------|--------|
| **Registry** | Mainline DHT (~10M nodes) |
| **TLD** | .pk, custom |
| **Cost** | Free (DHT storage) |
| **Resolution** | pkdns, resolvers |
| **Crypto** | Ed25519 signing |
| **Governance** | None (protocol only) |

**How It Works:**

```
1. Generate Ed25519 keypair
2. Create DNS records (TXT, A, AAAA, etc.)
3. Sign records with private key
4. Publish to DHT under key hash
5. Anyone resolves by looking up your public key hash
```

**The name IS your public key:**
- `npub1...` style naming
- Self-authenticating (name proves ownership)
- No renewal fees
- No seizure possible (without compromising the key)

**2025-2026 Developments:**

- **Pubky** emerged as the primary implementation
- **pkdns** — production DNS server resolving PKARR
- Growing ecosystem for self-sovereign identity

**Resources:**

- [pubky/pkarr GitHub](https://github.com/pubky/pkarr)
- [pubky/pkdns GitHub](https://github.com/pubky/pkdns)
- [docs.pubky.org](https://docs.pubky.org)

#### Nostr NIP-05

**Human-readable aliases resolved via HTTPS to a pubkey; not censorship-resistant by itself but composable.**

- `user@domain.com` maps to npub
- Uses DNS/HTTPS for resolution
- Can be combined with PKARR for full self-sovereignty

---

### 3. Overlay / Hidden Naming

These systems provide censorship-resistant naming by operating in separate networks.

#### Tor .onion

**Self-authenticating addresses (the name *is* the public key). Fully decentralized, strongest confidentiality for the operator.**

- v3 name = base32(Ed25519 pubkey ‖ checksum ‖ version) — 56 characters
- v2 (deprecated 2021) used truncated SHA-1 of an RSA-1024 key — 16 chars
- No registry, no CA — name verifies the key directly
- **Only way to seize**: compromise the private key

**Trade-off**: Hidden service only, not general DNS

#### I2P .b32.i2p

**Analogous to onion addresses, I2P's naming system.**

- Base32 encoded destination keys
- End-to-end encryption mandatory
- Less widely deployed than Tor

#### GNUNet GNS (GNU Name System)

**Petname-based hierarchical lookup with cryptographic roots.**

- RFC 9498 (published 2023)
- Hierarchical like DNS but with cryptographic delegation
- Privacy-preserving (minimal metadata)
- Integrated into GNUnet 0.26.0 (Nov 2025)

**Features:**

- **Petnames**: Local nicknames for keys
- **Delegation**: Control delegation between zones
- **Privacy**: Built-in privacy from ground up
- **No blockchain**: Uses GNUnet's distributed hash table

**Resources:**

- [GNUnet](https://www.gnunet.org/en/gns.html)
- [RFC 9498](https://www.rfc-editor.org/rfc/rfc9498)
- [NLnet GNS project](https://nlnet.nl/project/GNS/)

---

## Relation to Confidential Inference

A confidential LLM endpoint whose domain can be seized is not actually uncensorable. Pair attested TLS (pinned inside the enclave) with a decentralized name — `.eth`, `.onion`, or PKARR — and the only way to take the service offline is to shut down the underlying TEE nodes. The attestation public key + a pubkey-addressed name yields a self-authenticating endpoint: no CA, no registry, no DNS to seize.

### The Complete Picture

| Component | Traditional | Decentralized |
|-----------|-------------|---------------|
| **Domain** | registrar.com | .eth / .onion / pkarr |
| **TLS Cert** | Let's Encrypt / DigiCert | Attested TEE (inside enclave) |
| **Resolution** | ICANN → registrar → DNS | Blockchain / DHT / Tor |
| **Seizure path** | Court order to registrar | None (self-hosted key) |

---

## Evidence at a Glance

|| System | Type | TLD | Governance | Maturity | Status |
||--------|------|-----|------------|----------|--------|
| **ENS** | Blockchain | .eth | DAO | Mature | Active, 2025-26 stable |
| **Handshake** | Blockchain | Any | Permissionless | Niche | Active, low adoption |
| **Namecoin** | Blockchain | .bit | Permissionless | Legacy | Running |
| **PKARR/Pubky** | DHT | Custom | None | Emerging | Active dev, 2025-26 |
| **Tor .onion** | Overlay | .onion | None | Mature | Stable |
| **I2P** | Overlay | .b32.i2p | None | Mature | Stable |
| **GNS** | DHT | Custom | None | Mature | RFC 9498, 0.26.0 |

---

## Trade-offs

### Strengths

- **No seizure risk** — Name is the key; no registry to attack
- **No renewal fees** (PKARR, Tor, I2P) — One-time key generation
- **Self-authenticating** — Name proves ownership cryptographically
- **Censorship-resistant** — No central point to remove records
- **Composable** — Works with TEEs, FHE, MPC

### Limitations

- **Usability.** Users must run resolvers, install extensions, or use bridges.
- **Search isolation.** Search indexes ignore these spaces.
- **Phishing.** Homoglyph and typo-squatting are easier, not harder, in new name systems.
- **Blockchain costs.** ENS needs ETH; HNS needs HNS; gas fluctuates.
- **Root governance varies.** "Decentralized" varies — Handshake is permissionless; ENS root has multi-sig governance.
- **Key management.** Lose the key = lose the name (especially PKARR).

---

## Attack Surface

| Attack | Affected Systems | Mitigation |
|--------|------------------|------------|
| **Key compromise** | PKARR, Tor, I2P | Key splitting, threshold sigs |
| **Registrar coercion** | ENS (partial) | Smart contract upgrades |
| **51% attack** | ENS, Handshake | PoS/PoW security |
| **DHT poisoning** | PKARR | Signed records, multiple sources |
| **Front-running** | ENS auctions | Commit-reveal schemes |
| **DNS hijacking** | Traditional resolvers | DNSSEC, DANE |

---

## Related Files

- [Overview - Encrypted Messaging](/encrypted-messaging/overview-encrypted-messaging)
- [Overview - Decentralized Identity](/identity/overview-decentralized-identity)
- [Confidential-AI-Inference](/confidential-computing/confidential-ai-inference)
- [Overview - Mix Networks](/mix-networks/overview-mix-networks)
- [Overview - Web of Trust](/cryptography/overview-web-of-trust)

---

## Primary Sources

### Documentation & Specs

- ENS docs — `docs.ens.domains`
- Handshake — `handshake.org`
- PKARR — `github.com/pubky/pkarr`
- pkdns — `github.com/pubky/pkdns`
- GNS RFC 9498 — `rfceditor.org/rfc/rfc9498`
- Tor Rendezvous Specification v3 — `spec.torproject.org`

### GitHub Repositories

- [pubky/pkarr](https://github.com/pubky/pkarr)
- [pubky/pkdns](https://github.com/pubky/pkdns)
- [handshake-org/hnsd](https://github.com/handshake-org/hnsd)
- [namecoin/namecoin](https://github.com/namecoin/namecoin)

### Research

- Chor et al.: *Private Information Retrieval*, JACM 1998 (foundational)
- GNUnet: *The GNU Name System* (RFC 9498, 2023)

