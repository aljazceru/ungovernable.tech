---
title: "Handshake"
tags:
  - "handshake"
  - "hns"
  - "naming"
  - "dns"
  - "blockchain"
  - "deep-dive"
---
*The most ambitious decentralized naming project: replace the DNS root zone itself with a permissionless blockchain. Niche in adoption, distinctive in design, and architecturally relevant beyond its market footprint.*

---

## The position

ENS replaces *one TLD* (`.eth`). Handshake replaces *the entire root zone* — the small set of authoritative servers run by ICANN's root operators that decide which TLDs exist. Anyone can register their own TLD on Handshake; the chain decides which name is canonical.

This is a structural rather than incremental claim against legacy DNS:

| Layer | DNS today | Handshake |
|-------|-----------|-----------|
| Root zone | ICANN's 13 root servers | Handshake blockchain |
| TLD operators | ~1,500 ICANN-approved registries | Anyone (auction-based) |
| TLD list | gTLDs + ccTLDs as ratified | Top names by stake/auction |
| Censorship vector | ICANN policy + CA chain | Handshake consensus |

If you accept the premise that ICANN's root and the X.509 CA system are too tightly coupled to government and corporate interests, Handshake is the cleanest architectural answer.

---

## How it works

### Auction-based name acquisition

To register a TLD, you bid in a Vickrey-style sealed-bid auction:

1. Open the auction by sending a small bid (commitment).
2. Other participants bid (committed values, hidden).
3. Reveal phase: all bids revealed.
4. Highest bidder wins; pays the second-highest price.
5. The HNS spent is burned, not paid to anyone.

Effects:

- Truthful bidding is the dominant strategy (Vickrey property).
- Prices reflect demand without enriching a registrar.
- Burn-based monetary supply makes each registration mildly deflationary.

### Names

Hundreds of thousands of TLDs are registered. The "good" ones (short, memorable, generic) went in early auctions for substantial HNS. The "bad" ones (long, niche) are essentially free.

### Resolution

Handshake doesn't replace recursive DNS resolvers. It replaces the root zone. A Handshake-aware resolver:

1. Synchronizes (or queries) the Handshake chain to get current TLD ownership.
2. For a query like `something.alice/`, asks Handshake for `alice`'s current authoritative nameservers.
3. Forwards the query to those nameservers, which return records using normal DNS semantics.

Resolution implementations:

- hsd (full node) — the reference Handshake daemon.
- hnsd (light client) — SPV-style, queries chain headers.
- HSResolver — recursive DNS server frontend integrating with hnsd.

A user runs a local Handshake-aware resolver, configures their OS to use it, and Handshake names work alongside legacy ICANN names.

---

## Mining and consensus

- PoW (Cuckoo Cycle variant; ASIC-friendly Cuckatoo32 since the early 2020s).
- Block time ~10 minutes.
- Halving every 170,000 blocks (~3.25 years at 10-minute blocks).
- Total supply 2.04B HNS, mostly distributed via auction-name burns.

The chain is small (low transaction throughput, mostly naming operations). Block size and chain growth are bounded.

---

## Halving schedule

- First halving: ~April 2024 (block 170,000).
- Second halving: mid-2026 (block 340,000); tracker estimates range late April to late July depending on hashrate.
- Subsequent halvings: ~3.25 years apart.

Halvings cut the miner subsidy; auction burns continue to drive deflation.

---

## Use cases

### Self-sovereign TLD ownership

If you own `.alice` on Handshake, no registrar can take it. ICANN doesn't recognize it (which is the point), but every Handshake-aware resolver does.

### Brand or community TLDs

Companies experimentally own their brand as a TLD (for example `.shopify`, `.nostr`) and serve services there.

### Decentralized website hosting

`yoursite.alice` resolves to your IP via Handshake, served over HTTPS using certificates you control. Combined with self-signed or DANE-style cert binding, you get a full DNS+CA replacement.

---

## The cert story

The hard problem: browsers don't trust Handshake names by default. Solutions:

- DANE (DNS-Based Authentication of Named Entities) binds certs to DNS records, validated via DNSSEC. Handshake records support DANE; some Handshake-aware browsers (Beacon, Fingertip) honor it.
- Self-signed plus manual trust. Install your TLD's self-signed cert in the browser trust store. Friction for the user.
- A CA on Handshake names. None of the major CAs sign certs for non-ICANN TLDs. Niche CAs like Let's Authenticate and experimental ACME-Handshake exist but aren't widely adopted.
- Resolver-injected proxy. Handshake-aware resolvers can transparently proxy HTTPS with locally generated certs, bridging to DANE underneath.

The cert problem is the single biggest barrier to mainstream Handshake adoption.

---

## Resolution and browser support

| Method | UX |
|--------|-----|
| HNS-aware browser (Beacon, Fingertip) | Native — type `.alice` and it resolves |
| Local hsd / hnsd + system DNS | Works for all apps; cert UX still rough |
| HSD.is, h.tube, etc. gateways | Centralized HTTPS proxy — defeats the point |
| NextDNS, Brave with HNS | Convenient; trust shifts to that resolver |

Adoption is small but committed. Cloudflare experimentally resolved Handshake; that ended in 2022.

---

## Comparison

| Dimension | [ENS](/decentralized-dns/ens) | Handshake | [GNS](/decentralized-dns/gns) | Tor v3 .onion |
|-----------|---------|-----------|---------|---------------|
| Scope | One TLD (`.eth`) | Whole root zone | Hierarchical petnames | Self-auth onion |
| Ownership | NFT on Ethereum | HNS auction | Local petname → key | None — key is name |
| Censorship vector | Ethereum L1 | Handshake consensus | None | None |
| Cert story | Existing CAs work for Web3 use | Hard | Privacy-first GNS protocol | Built into Tor |
| Adoption | High | Niche | Niche | Wide (in Tor users) |

---

## Trade-offs

### Strengths

- Permissionless TLDs. Anyone can own one.
- No registrar, so no coercion vector at the naming layer.
- The auction model distributes premium names by willingness-to-pay rather than gatekeeping.
- Vickrey + burn is theoretically clean: incentive-compatible bidding, deflationary supply.

### Limitations

- The cert problem is unsolved at browser level. Without HTTPS, the modern web won't accept it.
- Adoption is small; few resolvers, few apps.
- Mainstream resolvers (Cloudflare, Google) don't natively resolve Handshake. Users have to run their own.
- Auctions favor early adopters who acquired good TLDs cheaply; the resale market is shallow.
- Phishing risk. `.alice` looks like a TLD and may confuse users about whether they're on a legitimate-looking site.

---

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| 51% attack on Handshake chain | Cuckatoo32 PoW raises cost; small attack-surface concern relative to ENS |
| Front-running auction reveals | Sealed bids; commit-reveal scheme |
| Compromised resolver | Run your own |
| Phishing via homoglyph TLD | Petname systems; resolver-side warnings |
| Cert MITM | DANE; pinned certs |
| Resolver service shutdown | Distributed resolver software |

---

## Operational patterns

### Self-hosted Handshake resolver

```
[App] → systemd-resolved → hsd (port 53) → upstream legacy DNS for ICANN names
                                          → local Handshake chain for HNS names
```

DNSSEC plus DANE for cert validation in supporting clients.

### Brand or community TLD

Acquire `.yourthing` at auction. Run authoritative DNS for it. Issue subdomains via standard DNS tools. Users with HNS-aware resolvers reach you; others see DNS NXDOMAIN.

### Bridge to ICANN

Some Handshake names alias to ICANN names via DNS records. A user resolves `mybrand` on Handshake, gets a CNAME to `mybrand.com`, follows that to legacy DNS. Useful for migration and dual-presence.

---

## Recent developments (2024-2026)

- First halving (April 2024) cut supply.
- Cuckatoo32 ASIC rollout has stabilized hashrate.
- HNS-aware browsers (Beacon, Fingertip) are maintained but niche.
- Cloudflare's HNS resolver retired; the community runs alternatives.
- Handshake-as-identity experiments tying Handshake names to PGP and DID workflows; small-scale.
- Second halving mid-2026 (block 340,000).

---

## Related files

- [Overview - Decentralized DNS](/decentralized-dns)
- [ENS](/decentralized-dns/ens)
- [GNS](/decentralized-dns/gns)
- [Pubky](/identity/pubky) — sibling permissionless naming
- [Overview - Identity & Pseudonymity](/identity)

---

## Primary sources

- Handshake Whitepaper — [handshake.org](https://handshake.org/files/handshake.txt).
- hsd (Handshake daemon) — [github.com/handshake-org/hsd](https://github.com/handshake-org/hsd).
- hnsd (light client) — [github.com/handshake-org/hnsd](https://github.com/handshake-org/hnsd).
- Cuckoo Cycle — Tromp, [github.com/tromp/cuckoo](https://github.com/tromp/cuckoo).
- DANE — RFC 6698.
- Beacon Browser — [beacon.cloud](https://beacon.cloud).

