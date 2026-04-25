---
title: "Decentralized DNS"
tags:
  - "dns"
  - "ens"
  - "handshake"
  - "pkarr"
  - "namecoin"
  - "decentralized"
  - "pubky"
  - "gns"
sidebar: {"label":"Overview","order":0}
---
*Naming systems that don't depend on ICANN, a TLD registrar, or a CA. Seizure, sanctions, and content-based takedowns flow through exactly those three places.*

---

## Why it matters

The DNS + X.509 stack has five choke points: root zone operators, TLD registries, registrars, recursive resolvers, and CAs. Any of them can be compelled or compromised to remove, redirect, or observe traffic on a domain. Encrypted transports like DoH and DoT change who can snoop but don't change who controls the names.

### Seizures and takedowns

Some recent examples:

- 2023: ICANN's handling of the .ONION renewal disrupted privacy tooling.
- 2022-2024: Russian authorities seized .RU domains in bulk.
- 2024: sanctions-driven seizures hit several crypto projects.
- Ongoing: content-based takedowns through UDRP, URS, and court orders.

The structural issue is that legacy DNS ties a name to a registrar's database row, and that row can be modified, deleted, or transferred without the holder's consent.

---

## Historical context

### Early work (1990s-2010)

| Year | Development | Notes |
|------|-------------|-------|
| 1991 | PGP web of trust | First decentralized identity (keys, not names) |
| 1997 | DNSSEC (RFC 2065) | Authenticated DNS records — didn't solve governance |
| 1998 | OpenPGP (RFC 2440) | Formalized key signing |
| 2011 | Namecoin | First functional blockchain DNS, merged-mined with Bitcoin |
| 2017 | ENS launched | Ethereum-based naming |
| 2018 | Handshake (HNS) | Public testnet — proposes replacing the root zone |

### Recent activity (2020-2026)

| Year | Development | Notes |
|------|-------------|-------|
| 2020 | ENS v2 planning | Layer 2 plans, gas optimization |
| 2023 | PKARR / Pubky | DHT-based naming on existing P2P infrastructure |
| 2023 | GNS RFC 9498 | GNS standardized |
| 2024 | ENS gas reductions | Lower registration cost after L1 throughput improvements |
| 2025 | GNUnet 0.26.0 | RFC 9498 GNS in production |
| Feb 2026 | ENS stays on L1 | Nick Johnson abandons Namechain L2, focuses on L1 scaling |
| 2026 | pkdns matures | Production DNS server for PKARR resolution |

---

## Approaches

### 1. Blockchain-anchored names

These systems store ownership records on a chain and use the chain as the source of truth.

#### ENS (Ethereum Name Service)

`.eth` names registered on Ethereum, used as wallet addresses, IPFS content hashes, and DIDs.

| Feature | Detail |
|---------|--------|
| Registry | Ethereum smart contract |
| TLD | .eth only |
| Cost | ~$5-50/year (gas fluctuates) |
| Resolution | ENS contracts → resolver → records |
| Resolver | PublicResolver, CCIP-read for off-chain |
| Governance | DAO + multi-sig |

2025-2026 changes:

- Gas costs dropped after Ethereum throughput improvements; ENS registrations got materially cheaper.
- ENSv2 (Feb 2026): Nick Johnson announced ENS would stay on L1 instead of launching the planned Namechain L2.
- CCIP-read (EIP-3668) is the standard pattern for cheap off-chain subname issuance.

Resources:

- [docs.ens.domains](https://docs.ens.domains)
- [ens.domains](https://ens.domains)

#### Handshake (HNS)

Replaces the DNS root zone with a blockchain. You can own your own TLD.

| Feature | Detail |
|---------|--------|
| Registry | Handshake blockchain |
| TLD | Any (you own your own root) |
| Cost | One-time (auction + renewal) |
| Resolution | Handshake resolvers |
| Mining | PoW-style mining |
| Governance | Permissionless |

Status (2026):

- Active but small.
- Second halving expected mid-2026 (block 340,000; tracker estimates range late April to late July depending on hashrate).
- Resolver work continues (HSD, hnsd).
- Mainstream adoption is minimal.

Resources:

- [handshake.org](https://handshake.org)
- [HNSd resolver](https://github.com/handshake-org/hnsd)

#### Namecoin

The original blockchain DNS (2011). Still running, with a small user base.

- Oldest blockchain naming system.
- .bit TLD.
- Merged-mined with Bitcoin.
- Tiny ecosystem, longest track record.

#### Unstoppable Domains

A centralized company that sells blockchain names. Lock-in concerns apply.

- Sells .crypto, .wallet, etc.
- The company can freeze or transfer names.
- Not actually decentralized despite the marketing.

---

### 2. Public-key-addressed names

The name *is* a public key. No blockchain, no registrar, just cryptographic identity.

#### PKARR (Public-Key-Addressable Resource Records)

Names are Ed25519 public keys. Signed DNS records are published to the BitTorrent Mainline DHT (around 10M nodes) under each key's hash. No blockchain, no registrar, no fees. Used in Pubky and Slashtags. See [PKARR](/decentralized-dns/pkarr) for the deep dive.

| Feature | Detail |
|---------|--------|
| Registry | Mainline DHT (~10M nodes) |
| TLD | None (key is the name); pkdns bridges via configurable TLD |
| Cost | Free (DHT storage) |
| Resolution | pkdns, native PKARR resolvers |
| Crypto | Ed25519 signing |
| Governance | None (protocol only) |

Strengths: self-authenticating, free, no chain, no seizure path. Trade-offs: no human-readable names without a layer on top, DHT churn requires periodic republication, lookup observability is low. See [PKARR](/decentralized-dns/pkarr) for the full threat model and composition patterns.

#### Nostr NIP-05

Human-readable aliases resolved over HTTPS to a pubkey. Not censorship-resistant alone, but composable.

- `user@domain.com` maps to an npub.
- Uses DNS / HTTPS for resolution.
- Can be served over PKARR for full self-sovereignty.

---

### 3. Overlay and hidden naming

Censorship-resistant naming inside separate networks.

#### Tor .onion

Self-authenticating addresses where the name is the public key. Fully decentralized, with the strongest operator confidentiality.

- v3 names: base32(Ed25519 pubkey ‖ checksum ‖ version), 56 characters.
- v2 (deprecated 2021) used truncated SHA-1 of an RSA-1024 key, 16 characters.
- No registry, no CA. The name verifies the key directly.
- The only seizure path is compromising the private key.

Trade-off: hidden services only, not general DNS.

#### I2P .b32.i2p

Analogous to onion addresses. I2P's naming.

- Base32-encoded destination keys.
- End-to-end encryption is mandatory.
- Less widely deployed than Tor.

#### GNUNet GNS (GNU Name System)

Petname-based hierarchical lookup with cryptographic roots.

- RFC 9498 (published 2023).
- Hierarchical like DNS, but with cryptographic delegation.
- Privacy-preserving (minimal metadata).
- Integrated into GNUnet 0.26.0 (Nov 2025).

Features:

- Petnames: local nicknames for keys.
- Delegation: zone-to-zone control delegation.
- Privacy from the ground up.
- No blockchain. Uses GNUnet's DHT.

Resources:

- [GNUnet](https://www.gnunet.org/en/gns.html)
- [RFC 9498](https://www.rfc-editor.org/rfc/rfc9498)
- [NLnet GNS project](https://nlnet.nl/project/GNS/)

---

## How this composes with confidential inference

A confidential LLM endpoint whose domain can be seized isn't actually uncensorable. Pair attested TLS (key pinned inside the enclave) with a decentralized name — `.eth`, `.onion`, or PKARR — and the only way to take the service down is to shut down the underlying TEE nodes. Attestation public key plus a pubkey-addressed name yields a self-authenticating endpoint with no CA, no registry, and no DNS to seize.

### Stack comparison

| Component | Traditional | Decentralized |
|-----------|-------------|---------------|
| Domain | registrar.com | .eth / .onion / pkarr |
| TLS cert | Let's Encrypt / DigiCert | Attested TEE (inside enclave) |
| Resolution | ICANN → registrar → DNS | Blockchain / DHT / Tor |
| Seizure path | Court order to registrar | None (self-hosted key) |

---

## Summary

| System | Type | TLD | Governance | Maturity | Status |
|--------|------|-----|------------|----------|--------|
| ENS | Blockchain | .eth | DAO | Mature | Active, 2025-26 stable |
| Handshake | Blockchain | Any | Permissionless | Niche | Active, low adoption |
| Namecoin | Blockchain | .bit | Permissionless | Legacy | Running |
| PKARR/Pubky | DHT | Custom | None | Emerging | Active dev, 2025-26 |
| Tor .onion | Overlay | .onion | None | Mature | Stable |
| I2P | Overlay | .b32.i2p | None | Mature | Stable |
| GNS | DHT | Custom | None | Mature | RFC 9498, 0.26.0 |

---

## Trade-offs

### What's good

- No seizure risk: the name is the key, not a database row.
- No renewal fees on PKARR, Tor, or I2P. One-time key generation.
- Self-authenticating: the name proves ownership cryptographically.
- Censorship-resistant: no central record to remove.
- Composable with TEEs, FHE, and MPC.

### What's hard

- Usability. Users need resolvers, extensions, or bridges.
- Search isolation. Search indexes don't cover these spaces.
- Phishing. Homoglyph and typo attacks are easier in new namespaces.
- Blockchain costs. ENS needs ETH, HNS needs HNS, gas varies.
- Root governance varies. Handshake is permissionless; ENS root has multi-sig governance.
- Key management. Lose the key, lose the name (especially with PKARR).

---

## Attack surface

| Attack | Affected systems | Mitigation |
|--------|------------------|------------|
| Key compromise | PKARR, Tor, I2P | Key splitting, threshold sigs |
| Registrar coercion | ENS (partial) | Smart contract upgrades |
| 51% attack | ENS, Handshake | PoS/PoW security |
| DHT poisoning | PKARR | Signed records, multiple sources |
| Front-running | ENS auctions | Commit-reveal schemes |
| DNS hijacking | Traditional resolvers | DNSSEC, DANE |

---

## Related files

- [Overview - Encrypted Messaging](/encrypted-messaging)
- [Overview - Decentralized Identity](/identity/overview-decentralized-identity)
- [Confidential-AI-Inference](/confidential-computing/confidential-ai-inference)
- [Overview - Mix Networks](/mix-networks)
- [Overview - Web of Trust](/cryptography/overview-web-of-trust)

---

## Primary sources

### Documentation and specs

- ENS docs — `docs.ens.domains`
- Handshake — `handshake.org`
- PKARR — `github.com/pubky/pkarr`
- pkdns — `github.com/pubky/pkdns`
- GNS RFC 9498 — `rfceditor.org/rfc/rfc9498`
- Tor Rendezvous Specification v3 — `spec.torproject.org`

### Repositories

- [pubky/pkarr](https://github.com/pubky/pkarr)
- [pubky/pkdns](https://github.com/pubky/pkdns)
- [handshake-org/hnsd](https://github.com/handshake-org/hnsd)
- [namecoin/namecoin](https://github.com/namecoin/namecoin)

### Research

- Chor et al., *Private Information Retrieval*, JACM 1998.
- GNUnet, *The GNU Name System* (RFC 9498, 2023).

