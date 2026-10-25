---
title: "Decentralized DNS and Sovereign Naming"
slug: decentralized-dns
type: explainer
pillars: ["naming"]
description: "Naming without ICANN, registrars or certificate authorities: blockchain registries, key-rooted names and overlay names compared by how sovereign they are."
dek: "Naming systems that don't depend on ICANN, a TLD registrar, or a CA. Seizure, sanctions, and content-based takedowns flow through exactly those three places."
updated: 2026-10-25
created: 2026-04-17
origin: vault
source: "03-Decentralized-DNS/Overview - Decentralized DNS.md"
aliases: ["dDNS", "Alternative DNS"]
tags: ["dns", "ens", "handshake", "pkarr", "namecoin", "decentralized", "pubky", "gns", "nomen", "cardano", "overlay", "mesh", "unstoppable-domains", "slashtags"]
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
| 2025 | GNUnet 0.26.0 | GNS implementation; GNUnet remains early alpha |
| Aug 2025 | Handshake soft fork | Airdrop claims ended; HNS supply cut ~56% (2.04B → 889M); bullish for miners and investors |
| Feb 2026 | ENS stays on L1 | Nick Johnson abandons Namechain L2, focuses on L1 scaling |
| Mar 2026 | GNUnet 0.27.0 | GNS improved; new major release |
| May 11 2026 | ENSv2 App + Explorer Alpha | ENS App and ENS Explorer deployed on Sepolia testnet for community testing |
| May 19 2026 | ENSv2 Role-Based Permissions | Launched — granular per-role access control for .eth names, replacing single-owner model for team/corp deployments; supports separate wallets for record updates, resolver management, and administrative settings |
| May 2026 | ENS contracts update | `ICompositeResolver.requiresOffchain()` removal (#541) and `_toResponseArray()` multicall safety (#543) merged May 19 |
| 2026 | pkdns matures | Production DNS server for PKARR resolution |
| 2026 | Pubky Core active | SDKs (Rust/JS/Swift/Kotlin), semantic social graph, homeserver discovery; pubky-core update to pkarr 6.0.1; JS SDK grant auth feature landed May 29; pubky-nexus API input validation landed May 28 |
| Jan 2026 | Iroh + PKARR integration | FOSDEM 2026 presentation; Iroh uses PKARR as one endpoint-ID discovery mechanism alongside DNS, mDNS, and Mainline DHT; establishes peer connections via QUIC with address-agnostic endpoint IDs |
| Mar–Apr 2026 | DNNS announced | Lithosphere introduced DNNS (Decentralized Naming System), an on-chain programmable identity/routing layer for Web4; on-chain routing announced April 2026 |
| 2026 | ENS ICANN engagement | D3 Protocol partnership, .brand gTLD application under consideration (ICANN 84) |
| 2026 | Nomen tracked as experimental | Bitcoin + Nostr naming model documented; low current activity |
| May 2026 | cdnsd updated | blinklabs-io/cdnsd Docker dependency updates landed May 31 |
| Jun 1 2026 | ViaBTC HNS pool closes | ViaBTC discontinued HNS mining pool — pool represented ~half of network hashrate; price impact immediate; community views as opportunity for decentralization |
| Jun 2 2026 | Namebase fully winds down | Namebase fully shut down operations; user coins and names returned; formerly the dominant Handshake registrar/marketplace |
| Jun 2026 | Handshake 2nd halving approaching | Estimated ~July 22 2026 (block 340,000); block reward drops from 2000 HNS → 1000 HNS |
| Jun 2026 | ENS Turkey adoption | Republic of Türkiye Directorate of Communications registered cbiletisim.eth as official decentralized identity for AI/blockchain initiative |
| Jun 2026 | Nostr WoT matures | Browser extension (Chrome Web Store), JS SDK (npm), WoT Oracle (Rust indexer), NIP-85 Trusted Assertions support; Dandelion Labs + MappingBitcoin backing |

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
| Registration and renewal | Auction followed by periodic renewal transactions; names expire without renewal |
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

#### Nomen

[Nomen](/kb/nomen/) is an experimental Bitcoin + Nostr naming protocol. Bitcoin supplies global ordering for first-claim-wins human-readable names; Nostr transports signed record updates from the owner key.

| Feature | Detail |
|---------|--------|
| Registry | Bitcoin transaction ordering |
| Records | Nostr kind `38300` events |
| Cost | Bitcoin tx fee for claim; Nostr updates cheap |
| Resolution | Indexer / name server materializes Bitcoin + Nostr state |
| Governance | Protocol rules, no new chain |
| Maturity | Experimental; low GitHub activity since 2023 |

Nomen's design is valuable because it composes existing censorship-resistant systems instead of launching another chain. Its weakness is distribution: no mainstream client support, tiny repo footprint, and reliance on indexers. See [Nomen](/kb/nomen/).

#### Cardano DNS

[Cardano DNS](/kb/cardano-dns/) is a Blink Labs / Gimbalabs effort to build a Handshake + Cardano DNS marketplace. Handshake anchors top-level-domain authority; Cardano native assets and smart contracts represent second-level domains and DNS record updates; `cdnsd` indexes chain state and serves DNS answers.

| Feature | Detail |
|---------|--------|
| TLD authority | Handshake |
| SLD / marketplace layer | Cardano native assets + Plutus contracts |
| Resolver | `blinklabs-io/cdnsd` Go DNS daemon |
| Profiles | `cardano`, `ada`, `hydra`, auto-discovery preprod profiles |
| Maturity | Experimental but active; `cdnsd` pushed May 2026 |

Cardano DNS is more complex than [ENS](/kb/ens/) or [PKARR](/kb/pkarr/), but useful where the product is a sovereign second-level-domain marketplace rather than merely service discovery. See [Cardano DNS](/kb/cardano-dns/).

### 2. Public-key-addressed names

The name *is* a public key. No blockchain, no registrar, just cryptographic identity.

#### PKARR (Public-Key-Addressable Resource Records)

Names are Ed25519 public keys. Signed DNS records are published to the BitTorrent Mainline DHT (around 10M nodes) under each key's hash. No blockchain, no registrar, no fees. The primary production stack is [Pubky](/kb/pubky/), which extends PKARR with homeservers, SDKs (Rust, JavaScript, Swift, Kotlin), semantic social graph, and RESTful HTTP APIs. See [PKARR](/kb/pkarr/) for the deep dive and [Pubky](/kb/pubky/) for the full system.

**Iroh integration (FOSDEM 2026):** Iroh, a library for direct QUIC connections between peers, uses PKARR as one of its endpoint-ID discovery mechanisms alongside DNS, mDNS, and Mainline DHT. This means PKARR-based identities can serve as Iroh endpoint identifiers for peer-to-peer connections — the key's hash resolves to a relay URL and IP address, enabling NAT穿透 and direct connection establishment without address-based identities. See the [FOSDEM 2026 Iroh presentation](https://fosdem.org/2026/schedule/event/T9ACNE-iroh_p2p_connections/) and [Pubky Dev Call #2](https://www.youtube.com/watch?v=ZL-MxJtTIks) for the integration details.

| Feature | Detail |
|---------|--------|
| Registry | Mainline DHT (~10M nodes) |
| TLD | None (key is the name); pkdns bridges via configurable TLD |
| Cost | Free (DHT storage) |
| Resolution | pkdns, native PKARR resolvers |
| Crypto | Ed25519 signing |
| Governance | None (protocol only) |
| Production stack | [Pubky](/kb/pubky/) Core — SDKs, semantic social graph, Pubky.app social, Pubky Ring mobile key manager, Pubky Nexus indexing |

Strengths: self-authenticating, free, no chain, no seizure path. Trade-offs: no human-readable names without a layer on top, DHT churn requires periodic republication, lookup observability is low. See [PKARR](/kb/pkarr/) for the full threat model and composition patterns.

#### Nostr NIP-05

Human-readable aliases resolved over HTTPS to a pubkey. Not censorship-resistant alone, but composable.

- `user@domain.com` maps to an npub.
- Uses DNS / HTTPS for resolution.
- Can be served over PKARR for full self-sovereignty.

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

## How this composes with confidential inference

A confidential LLM endpoint whose domain can be seized isn't actually uncensorable. Pair attested TLS (key pinned inside the enclave) with a decentralized name — `.eth`, `.onion`, or PKARR — and the only way to take the service down is to shut down the underlying TEE nodes. Attestation public key plus a pubkey-addressed name yields a self-authenticating endpoint with no CA, no registry, and no DNS to seize.

### Stack comparison

|| Component | Traditional | Decentralized |
|-----------|-------------|---------------|
|| Domain | registrar.com | .eth / .onion / pkarr |
|| TLS cert | Let's Encrypt / DigiCert | Attested TEE (inside enclave) |
|| Resolution | ICANN → registrar → DNS | Blockchain / DHT / Tor |
|| Seizure path | Court order to registrar | None (self-hosted key) |

## Mesh and off-grid naming

When the global internet is not reachable, the naming model has to change. Two production systems address this directly:

- **Yggdrasil** — encrypted IPv6 overlay where every node has a stable, key-derived address in `200::/8` or `300::/8`. The address is the key. No DNS, no registrar, no chain. v0.5.12 (Dec 2024) is the current reference.
- **cjdns** — the older cousin, with addresses in `fc00::/8`, routed by Kademlia DHT, with the CryptoAuth header that prevents IP spoofing. Maintenance-mode but still powers Hyperboria.

At the application layer, **Briar** shows the most extreme case: there is no global namespace at all. The "address book" is built from out-of-band contact exchange (QR codes, Bluetooth, Wi-Fi), and each contact's display name is local. Transports fall back through Tor, then pluggable transports, then Bluetooth and Wi-Fi.

The architectural pattern is the same one [PKARR](/kb/pkarr/) and [Overlay Naming - Tor .onion and I2P](/kb/onion-and-i2p-naming/) use: name = key = address. What mesh adds is **transport independence**: the addressing layer doesn't care whether the underlying network is fiber, mesh radio, Bluetooth, or nothing. See [Mesh & Off-Grid Naming](/kb/mesh-naming/) for the full deep-dive.

## Cautionary case study — Unstoppable Domains

The taxonomy of decentralized naming is incomplete without naming what *isn't* decentralized. **Unstoppable Domains** (UD) sells blockchain-anchored names (`.crypto`, `.wallet`, `.nft`, `.x`, `.bitcoin`, …) on Polygon and other chains. ~4.6M+ names are registered. The names are tokens in a wallet, which feels decentralized. But UD is a company with a website, a resolver, and an ICANN accreditation.

In **September 2025**, a patent application filed by UD in February 2024 was published: "Deactivation of decentralized domains." The patent describes a wallet-vote-based takedown mechanism, with anti-abuse design (wallet age, reliability scores, time windows) but explicit takedown path that exists outside the chain.

UD is also ICANN-accredited — the only Web3 naming company with both a Web3 chain-anchored product *and* the traditional registrar credential. This means UD is bound by UDRP, court orders, and ICANN contractual obligations, like any other accredited registrar.

The lesson for an Ungovernable.tech stack: **blockchain-anchored ownership is not the same as decentralized governance.** True decentralized naming has no off-chain operator that can take the name down. ENS, Handshake, Namecoin, GNS, PKARR, Nomen, Tor, I2P, and Yggdrasil all satisfy this. UD does not. See [Unstoppable Domains](/kb/unstoppable-domains/) for the full case study.

## Summary

|| System | Type | TLD | Governance | Maturity | Status |
|--------|------|-----|------------|----------|--------|
|| [ENS](/kb/ens/) | Blockchain | .eth | DAO | Mature | Active, ENSv2 in progress (Role-Based Permissions live May 19 2026, Sepolia alpha testing) |
|| [Handshake](/kb/handshake/) | Blockchain | Any | Permissionless | Niche | Active but strained; ViaBTC HNS pool closed Jun 1 (was ~50% hashrate); Namebase wound down Jun 2; 2nd halving ~Jul 22 2026 (2000→1000 HNS); resolver work continues; ecosystem shifting to smaller pools + self-hosted tools (BobWallet, ShakeDex) |
|| [Namecoin](/kb/namecoin/) | Blockchain | .bit | Permissionless | Legacy-active | Namecoin Core nc31.1 (Jul 2026, tracks Bitcoin Core 31.x); ncp11 + ncdns + ncgencert end-to-end stack; FOSDEM 2026 + 39C3 talks |
|| [PKARR](/kb/pkarr/) / [Pubky](/kb/pubky/) | DHT | Custom | None | Emerging | Active dev, Pubky Core suite (2025-26), Pubky Nexus pushed 2026-05-31 |
|| Tor v3 `.onion` | Overlay | .onion | None | Mature | Stable; v2 fully retired 2021-12-15 |
|| I2P `.b32.i2p` | Overlay | .b32.i2p | None | Mature | Stable; PQ migration in progress (Proposal 169) |
|| [GNS](/kb/gnu-name-system/) | DHT | Custom | None | Mature | RFC 9498, GNUnet 0.27.0 (Mar 2026) |
|| [Nomen](/kb/nomen/) | Bitcoin + Nostr | Custom | Protocol only | Experimental | Low activity, useful design pattern |
|| [Cardano DNS](/kb/cardano-dns/) | Handshake + Cardano | HNS-backed TLDs | Contract / marketplace rules | Experimental | Active `cdnsd`, Catalyst funded |
|| [DNNS](/kb/dnns/) | Lithosphere L1 | Programmable | On-chain governance | Announced | No public repo yet |
|| [Slashtags](/kb/slashtags/) | Hyperswarm DHT | Custom | None | Historical | Superseded by Pubky Core; design pattern lives on |
|| [Mesh & Off-Grid Naming](/kb/mesh-naming/) (Yggdrasil) | Encrypted IPv6 overlay | 200::/8 / 300::/8 (IPv6) | None | Active | v0.5.12 Dec 2024; embedded Go library |
|| [Mesh & Off-Grid Naming](/kb/mesh-naming/) (cjdns) | DHT-routed IPv6 overlay | fc00::/8 (IPv6) | None | Maintenance-mode | Hyperboria community; cryptoAuth |
|| [Mesh & Off-Grid Naming](/kb/mesh-naming/) (Briar) | Local petname + transport fallback | Local petname | None | Mature | Briar 1.5.17 Mar 2026; Desktop 0.6.0-beta 2026 |
|| [Unstoppable Domains](/kb/unstoppable-domains/) | Blockchain + company | .crypto, .wallet, .x, .bitcoin, … | Company + ICANN | Cautionary | 4.6M+ names; takedown patent filed 2024, published 2025 |

## Evidence at a glance

|| Evidence item | Source | What it supports |
||---------------|--------|------------------|
| `pubky/pkarr` — 412 stars, Rust, pushed 2026-05-29; 1 commit post-May 25 | GitHub API, 2026-06-01 | PKARR remains actively maintained; pkarr 6.0.1 integrated into pubky-core |
| `pubky/pkdns` — 191 stars, 25 releases, pushed 2026-03-23 | GitHub API | DNS bridge for PKARR is production-shaped, not only a library |
| `pubky/pubky-core` — 77 stars, pushed 2026-05-29; JS SDK grant auth landed | GitHub API, 2026-06-01 | Pubky Core production launch; Rust/JS/Swift/Kotlin SDKs; semantic social graph; pubky.app social |
| `pubky/pubky-ring` — 10 stars, pushed 2026-05-29; Android/iOS fixes | GitHub API, 2026-06-01 | iOS/Android key management for Pubky identity |
| `pubky/pubky-nexus` — 19 stars, pushed 2026-05-31; API input validation landed | GitHub API, 2026-06-01 | Social graph indexing for Pubky apps; staging + production APIs |
| `pubky/pubky-app` — 22 stars, pushed 2026-05-31 | GitHub API, 2026-06-01 | Pubky.app social PWA |
| `pubky/pkarr` relay split — HTTP and DHT rate limiting merged May 29 | GitHub commit `c25227d6` | New relay architecture separating HTTP and DHT transport; better DoS resistance |
| `ensdomains/ens-contracts` — 721 stars, pushed 2026-05-19; #541 and #543 merged May 19 | GitHub API, 2026-06-01 | ENS core contracts actively maintained; ENSv2 development progressing |
| `handshake-org/hnsd` — 307 stars, pushed 2026-03-21 | GitHub API | Handshake SPV resolver remains active despite niche adoption |
| `blinklabs-io/cdnsd` — 11 stars, pushed 2026-05-31; Docker action updates | GitHub API, 2026-06-01 | Cardano DNS resolver is early but actively maintained |
| `ursuscamp/nomen` — 18 stars, last pushed 2023-11-26 | GitHub API | Nomen is experimental and currently low-activity |
| ENSv2 Role-Based Permissions launched May 19 2026 | ENS blog, 2026-05-19 | Per-role access control replacing single-owner model for organizational use |
| ENS App + Explorer Alpha on Sepolia | ENS blog, 2026-05-11 | ENSv2 protocol rewrite in community testing phase |
| DNNS announced March–April 2026 | Globe and Mail / Newsfile Corp press releases | On-chain programmable naming for Web4; no public repo confirmed |
| RFC 9498 published Nov 2023 | RFC Editor | GNS has a formal protocol specification, though informational / non-IETF-consensus |
| ViaBTC HNS pool closed Jun 1 2026 | ViaBTC support article, SkyInclude Jun 2026 report | ViaBTC discontinuation removed ~50% of HNS hashrate; price impact confirmed; indicates centralization risk in niche chains |
| Namebase fully wound down Jun 2 2026 | Namebase / X announcement @NamebaseHQ | Dominant Handshake registrar/marketplace closed; coins + names returned to users; community migrating to BobWallet, ShakeDex |
| Handshake 2nd halving ~Jul 22 2026 | altcoinsbox.com halving countdown, NiceHash | Block 340,000; reward 2000→1000 HNS; in-flight ecosystem stress due to Jun 2026 service disruptions |
| ENS Turkey cbiletisim.eth adoption Jun 2026 | ENS X @ensdomains | Republic of Türkiye Directorate of Communications uses ENS for official decentralized identity; institutional adoption signal |
| Nostr WoT extension 2026 | Chrome Web Store, GitHub nostr-wot | Browser extension, JS SDK (npm), Rust Oracle; NIP-85 Trusted Assertions; Dandelion Labs + MappingBitcoin backing |
| [Namecoin](/kb/namecoin/) Core 28.0 released Dec 15 2024; **nc31.1 Jul 13 2026** (Bitcoin Core 31.1 base) | namecoin.org, GitHub | 2024-12-15 / 2026-07-13 | Continuous upstream rebases; codebase current through Bitcoin Core 31.x |
| [Namecoin](/kb/namecoin/) FOSDEM 2026 + 39C3 Dec 2025 | namecoin.org front page 2026-01-26 | Active community presence at major conferences; 15 years of operation |
| `ncp11` PKCS#11 module code-quality improvements May 2025 | namecoin.org blog 2025-05-13 | The path that makes `.bit` HTTPS work in stock Firefox/Chrome is actively maintained |
| `ncgencert` rename Sep 20 2025 | namecoin.org blog 2025-09-20 | Renamed from `generate_nmc_cert`; current tool for `.bit` TLS server setup |
| `Encasha` off-chain SSHFP records Sep 27 2025 | namecoin.org blog 2025-09-27 | Extends Encaya (server-side name lookup) with off-chain SSHFP |
| Windows 11 CryptoAPI AIA URL limit investigation Sep 7 2025 | namecoin.org blog 2025-09-07 | Investigates edge case in the AIA+PKCS#11 path that lets `.bit` work in stock browsers |
| "[Unstoppable Domains](/kb/unstoppable-domains/) 'Deactivation of decentralized domains' patent filed Feb 2024, published Aug 2025 | Domain Name Wire, Sept 2 2025 | Major Web3 domain company files patent for takedown mechanism; explicit contradiction of "unstoppable" branding |
| Oxford Info Labs + AFNIC blockchain domains study | oxil.uk 2025 mapping report | 31 blockchain domain providers studied; only Freename and Unstoppable Domains are ICANN-accredited; blockchain domains = 0.5% of total DNS in Q4 2023 |
| Yggdrasil `yggdrasil-go` v0.5.12 (Dec 18 2024) | pkg.go.dev deps.dev 2025-11-30 | Reference Go implementation current; embedded Go library released 2024 |
| Briar 1.5.17 (Mar 12 2026), Briar Desktop 0.6.0-beta (2026) | briarproject.org front page | Active Briar development; Bluetooth/Wi-Fi/Tor transport stack |
| Slashtags → Pubky Core transition | slashtags.to redirects to Pubky Core; UD synonyms | Slashtags is formally superseded; PKARR is the modern primitive |

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

## Attack surface

| Attack | Affected systems | Mitigation |
|--------|------------------|------------|
| Key compromise | PKARR, Tor, I2P | Key splitting, threshold sigs |
| Registrar coercion | ENS (partial) | Smart contract upgrades |
| 51% attack | ENS, Handshake | PoS/PoW security |
| DHT poisoning | PKARR | Signed records, multiple sources |
| Front-running | ENS auctions | Commit-reveal schemes |
| DNS hijacking | Traditional resolvers | DNSSEC, DANE |

## Primary sources

- [hsd mainnet renewal window](https://github.com/handshake-org/hsd/blob/master/lib/protocol/networks.js)
- [hsd name-expiry rule](https://github.com/handshake-org/hsd/blob/master/lib/covenants/namestate.js)

- [GNUnet software status](https://www.gnunet.org/en/about.html)

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
- [pubky/pubky-core](https://github.com/pubky/pubky-core) — SDKs, homeserver, semantic social graph
- [pubky/pubky-ring](https://github.com/pubky/pubky-ring) — mobile key manager
- [pubky/pubky-nexus](https://github.com/pubky/pubky-nexus) — social graph indexing
- [pubky/pubky-app](https://github.com/pubky/pubky-app) — Pubky.app social PWA
- [handshake-org/hnsd](https://github.com/handshake-org/hnsd)
- [namecoin/namecoin](https://github.com/namecoin/namecoin)
- [ursuscamp/nomen](https://github.com/ursuscamp/nomen)
- [ursuscamp/noms](https://github.com/ursuscamp/noms)
- [blinklabs-io/cardano-dns](https://github.com/blinklabs-io/cardano-dns)
- [blinklabs-io/cdnsd](https://github.com/blinklabs-io/cdnsd)

### Research

- Chor et al., *Private Information Retrieval*, JACM 1998.
- GNUnet, *The GNU Name System* (RFC 9498, 2023).
