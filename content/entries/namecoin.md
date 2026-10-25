---
title: "Namecoin"
slug: namecoin
type: deep-dive
pillars: ["naming"]
readiness: usable
description: "Namecoin, the first fork of Bitcoin and the first blockchain naming system: how .bit names work, what it got right, and why adoption stayed small."
dek: "The original blockchain DNS — the first Bitcoin fork (April 2011) and the first system to put human-meaningful names on a permissionless chain. Active development continues 15 years later, with Namecoin Core 28.0 released in December 2024; the user-facing ecosystem is small but the technical lineage runs through every chain-anchored name that followed. See Overview - Decentralized DNS for the comparative landscape; Handshake for the spiritual successor that replaced the DNS root zone."
updated: 2026-10-25
created: 2026-06-22
origin: vault
source: "03-Decentralized-DNS/Namecoin.md"
aliases: ["Namecoin Core", ".bit", "NMC", "First blockchain DNS"]
tags: ["namecoin", "dot-bit", ".bit", "bitcoin", "fork", "decentralized-dns", "deep-dive", "zooko"]
---

## Summary

Namecoin is a key/value store on a Bitcoin-derived proof-of-work chain, merged-mined with Bitcoin since 2011. The key innovation: it was the first deployed system to put a human-readable name (`example.bit`) on a blockchain, with the property that the name is owned by whoever first registered it and only that person can update or transfer it. The same chain can store other identity data — GPG keys, Bitmessage addresses, TLS certificate fingerprints — and the same consensus rules apply.

Namecoin was the first to claim it squared Zooko's triangle: human-meaningful + decentralized + secure, all three, on a single Bitcoin-derived chain. The implementation has been around for 15 years, longer than any other blockchain-DNS effort, and is still maintained by a small but active team (Jeremy Rand, lead maintainer).

The current production reality: technical leadership and protocol innovation are real, but mainstream adoption of `.bit` is tiny. The reference deployment is `ncdns` plus `ncp11` plus `generate_nmc_cert` (now `ncgencert`), which together make `.bit` sites work in stock Firefox and Chrome with no browser patching. This is the *most polished* end-to-end dDNS stack of any chain-DNS system.

## Historical context

| Date | Event |
|------|-------|
| Sep 2010 | BitDNS discussion on BitcoinTalk; Gavin Andresen and Satoshi Nakamoto weigh in |
| Dec 2010 | Reward posted for BitDNS implementation |
| 18 Apr 2011 | Namecoin launched; first Bitcoin fork |
| 19200 block (2011) | Merged mining activated with Bitcoin |
| 2013 | NameID launched; OpenID provider for `.bit` names |
| 2013 (Oct) | Critical security bug found in foreign-name-update logic; fixed quickly |
| 2015 | Most-publicized study: 120,000 names registered, 28 in active use |
| 2018–2019 | OpenNIC votes to drop `.bit` from its alternative root (July 2019) |
| 2021 | Namecoin Core 0.21.0 released |
| 2024 (Dec) | **Namecoin Core 28.0** released — modern Bitcoin Core base |
| 2025 (May) | ncp11 code-quality improvements merged |
| 2025 (Jul–Sep) | Hashed TLSA records, Encasha off-chain SSHFP, Windows 11 CryptoAPI AIA URL investigation |
| 2025 (Sep) | Unstoppable Domains files takedown patent; Namecoin's positioning as the "actually decentralized" alternative sharpens |
| 2025 (Dec) | 39C3 assembly in Hamburg (CDC cluster) |
| 2026 (Jan) | **FOSDEM 2026** talk scheduled (Brussels, 31 Jan – 1 Feb 2026) |
| 2026 (Jul) | **Namecoin Core nc31.1** released — tracks Bitcoin Core 31.1; continuous rebasing continues into year 15 |

## Architecture

### The chain

- **Algorithm**: SHA-256 proof-of-work; **merged-mined** with Bitcoin since 2011 (block 19,200 of Namecoin).
- **Block time**: 10 minutes.
- **Supply cap**: 21,000,000 NMC (same as Bitcoin).
- **Block reward**: halving cycle same as Bitcoin (every 210,000 blocks).

A Bitcoin miner with `getauxval`-style support mines Namecoin blocks in parallel with Bitcoin ones at near-zero marginal cost. The merged-mining security model is the same as Bitcoin's for whatever fraction of hashrate mines Namecoin, which historically has been a large fraction when a major pool like F2Pool / ViaBTC / AntPool opts in.

### Names as key/value records

A Namecoin name is a path of the form `namespace/name`. The most-used namespace is `d/` (DNS). A `d/example` record corresponds to `example.bit` and contains DNS records in standard DNS zone format.

Names have:
- A name (the key).
- A value (data; up to ~520 bytes for typical operations).
- An expiration (default 36,000 blocks ≈ 200 days; renewable).
- An owner (the pubkey script of the registrant).

The record fee is small (0.01 NMC) plus the Bitcoin-style transaction fee. First-come-first-served: whoever registers first owns the name until expiration. No smart contracts; the name-update logic is in the consensus rules.

### Resolver stack

| Component | Role |
|-----------|------|
| `ncdns` | The current resolver; runs as a local DNS server, watches the Namecoin chain, and answers `.bit` queries from chain state. Replaces the older `nmcontrol`. |
| `ncp11` | PKCS#11 module that lets standard TLS clients (NSS / GnuTLS) reach Namecoin-owned keys for `.bit` HTTPS. The crucial piece that makes `.bit` work in stock Firefox/Chrome. |
| `ncgencert` (renamed from `generate_nmc_cert` Sep 2025) | Tool for setting up a Namecoin TLS server. |
| `Encaya` | Server-side name lookup service — useful when running TLS at scale; supports off-chain TLSA and SSHFP records. |

`ncdns` + `ncp11` + `ncgencert` is the working end-to-end path. With those three, a `.bit` site can serve HTTPS in an unmodified browser — a milestone that Handshake, Namecoin's spiritual successor, has not matched.

### The cert problem (solved differently than Handshake)

Namecoin's answer to "no CAs sign certs for `.bit`" is `ncp11` + AIA (Authority Information Access) + PKCS#11. Here's the dance:

1. A `.bit` operator generates a self-signed certificate.
2. The cert contains an AIA URL pointing to a chain-trust file hosted on the Namecoin chain (or, with `Encaya`, an off-chain file).
3. `ncp11` runs as a PKCS#11 provider in the browser's NSS library.
4. When the browser validates the cert, NSS resolves the AIA URL against the Namecoin chain via `ncdns`, gets the trust anchor, and trusts the self-signed cert.

This is the **interoperability magic of AIA and PKCS#11** that Jeremy Rand cites in talks: a special form of TLS cert that works in stock browsers without browser patching and without MITM-by-CA. The October 2025 work on `Encasha` (off-chain SSHFP) and the September 2025 work on AIA URLs (Windows 11 CryptoAPI URL length limit) are iterations of the same idea.

## Maturity and active development

| Component | Repository | Activity (mid-2026) |
|-----------|------------|---------------------|
| `namecoin-core` | `github.com/namecoin/namecoin-core` | 51,352 commits; 27+ releases; current stable **Namecoin Core nc31.1 (Jul 2026**, Bitcoin Core 31.1 base); master branch regularly built and tested |
| `ncdns` resolver | `github.com/namecoin/ncdns` | Active; v0.0.7+ series; current as of 2025–2026 |
| `ncp11` PKCS#11 module | `github.com/namecoin/ncp11` | Code-quality improvements merged May 2025 |
| `Encaya` server | `github.com/namecoin/encaya` | Hashed TLSA (Sep 2025), Encasha SSHFP (Sep 2025), off-chain TLSA (Sep 2025) — active dev |
| `ncgencert` (renamed Sep 2025) | `github.com/namecoin/ncgencert` | Replaces `generate_nmc_cert`; current |
| `sockstrace` | Active tooling | Major update Jul 2025 |

**Interpretation**: Namecoin is a real, active project with a small but expert maintainer team and continuous upstream Bitcoin Core rebases. The 28.0 release in Dec 2024 is a major proof of life — the codebase is current and not abandoned.

## Use cases

### 1. Censorship-resistant web presence

A `.bit` site hosted on a self-managed server, with a Namecoin-anchored HTTPS cert. The end-to-end stack (`ncdns` + `ncp11` + `ncgencert`) means a user with `ncdns` configured gets a working, secure, decentralized HTTPS site with no trust in any CA, registrar, or registry.

In practice, the user base is small (a few thousand power users), but the *technological answer* to "can a decentralized name have HTTPS?" is the most polished of any dDNS system.

### 2. Identity / NameID

The NameID protocol (2013) maps a Namecoin name to an OpenID-compatible identity. The use case has not scaled — the OpenID ecosystem itself declined — but the same `id/` namespace mechanism is still available for self-asserted identity records: GPG keys, Bitmessage addresses, OTR keys, BTC addresses, TLS fingerprints.

### 3. Anchored identity for other systems

A Namecoin name can carry a GPG or SSH key fingerprint in a `id/` namespace record. The pattern: register `pgp/alice.bit` once, reference the same record from email signatures, PGP keyservers, and other systems. The record is anchored to the Namecoin chain; the keyserver mirrors are not the source of truth.

### 4. SSHFP records via Encasha

The September 2025 Encasha work extends off-chain TLSA to off-chain SSHFP, providing a Namecoin-anchored SSH server fingerprint. Use case: SSH clients verifying host keys without trusting TOFU + known_hosts alone.

## Trade-offs

### Strengths

- **First mover, longest track record** — 15 years of operation, longer than any chain-DNS competitor.
- **Squares Zooko's triangle** — first to claim it, technically defensible.
- **End-to-end HTTPS works in stock browsers** — `ncp11` + AIA is the cleanest answer to the cert problem of any dDNS system.
- **Merged mining** with Bitcoin — the security budget is Bitcoin's hashrate when miners opt in.
- **Active development** — Namecoin Core 28.0 in Dec 2024, plus a steady stream of resolver / TLS / SSHFP improvements through 2025.
- **Real community events** — FOSDEM 2026, 39C3 in Dec 2025, GCER 2025.
- **Open governance** — no company, no token-holder vote, no DAO smart contract.

### Limitations

- **Tiny user-facing ecosystem.** A handful of working sites; mainstream awareness is low.
- **Name squatting** — first-claim-wins with no auction; valuable names (short, common) were taken in 2011–2013 and have not been released.
- **Renewal friction** — names expire every 36,000 blocks (~200 days) unless renewed; lose the key, lose the name.
- **Bitcoin-derived cost** — name registration cost follows Bitcoin fee markets; cheap in normal times, expensive in congestion.
- **OpenNIC dropped `.bit` (2019)** — public alternative-root support evaporated.
- **No smart contracts** — limits composability (compared to ENS, Cardano DNS, DNSSEC-into-ENS).
- **On-chain privacy** — name registrations are public, like all UTXO-chain transactions.

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Mining majority attack (rename / double-claim) | Bitcoin's hashrate when miners opt in; economic cost same as Bitcoin 51% attack |
| Name squatting | Auctions, secondary markets, social conventions |
| OpenNIC de-listing | Run `ncdns` locally; no alternative root needed |
| TLS hijack | AIA + PKCS#11 path; ncp11 verifications |
| Lost key | Hardware wallet; backup of name_update privkey |
| AIA URL spoofing | ncp11 verifies against the chain; URL is signed data |
| Post-quantum | PQC exploration 2025–2026; `Is Post-Quantum Namecoin TLS Feasible?` Sept 2025 |

## Comparison

| System | Crypto | Naming model | HTTPS in stock browser | Maturity (2026) | Track record |
|--------|--------|--------------|------------------------|-----------------|--------------|
| [Namecoin](/kb/namecoin/) | SHA-256 PoW + merged mining | Key/value on chain | **Yes** (ncp11 + AIA) | Legacy-active; actively maintained | 15 years |
| [Handshake](/kb/handshake/) | BLAKE2b + SHA3 PoW | UTXO chain; auction | Hard (DANE, niche browsers) | Niche; 2nd halving Jul 2026 | 8 years |
| [ENS](/kb/ens/) | Ethereum PoS | Smart contract | Yes (any CA; CCIP-Read) | Mainstream | 9 years |
| [Cardano DNS](/kb/cardano-dns/) | Cardano / Handshake | Native asset + plutus | Not yet | Experimental | 2–3 years |
| [DNNS](/kb/dnns/) | Lithosphere PoS | On-chain | Unknown (no public repo) | Announced | 0 |

Namecoin is the system to study if you want the most "no-trust-at-all" answer to "can a decentralized name have HTTPS without a CA?" — and if you're willing to live with a small ecosystem.

## Operational notes

If you want to use Namecoin in 2026:

1. **Run a Namecoin node** or use a hosted RPC. For a `.bit` site operator, run `namecoind` and `ncdns` on the server.
2. **Generate a name keypair** for the `.bit` name. Store the privkey on a hardware wallet or a strong passphrase-protected wallet.
3. **Register the name** (a name_firstupdate transaction), then renew before expiration (every 200 days).
4. **Generate the TLS cert** with `ncgencert` (renamed from `generate_nmc_cert` in Sep 2025).
5. **Configure ncp11** on every client that needs to verify your cert — most easily via Firefox, which loads NSS PKCS#11 modules.
6. **Configure `ncdns`** as the system resolver for `.bit`, or use a community resolver.

For a `.bit` site visitor:

1. Install `ncdns` locally.
2. Configure your system resolver to use `ncdns` for `.bit`.
3. (Optional) Install `ncp11` in Firefox for the TLS verification path.

## Primary sources

- [hsd proof-of-work implementation](https://github.com/handshake-org/hsd/blob/master/lib/primitives/abstractblock.js)

- Namecoin website — `namecoin.org`.
- Namecoin Core source — `github.com/namecoin/namecoin-core`.
- `ncdns` resolver — `github.com/namecoin/ncdns`.
- `ncp11` PKCS#11 — `github.com/namecoin/ncp11`.
- `Encaya` server — `github.com/namecoin/encaya`.
- Namecoin Core 28.0 release notes — `namecoin.org/2024/12/15/namecoin-core-28.0-released.html`.
- Jeremy Rand, "Is Post-Quantum Namecoin TLS Feasible?" — `namecoin.org/2025/09/23/...`.
- Jeremy Rand, "Code Quality Improvements in ncp11" — `namecoin.org/2025/05/13/...`.
- Wikipedia, "Namecoin" — `en.wikipedia.org/wiki/Namecoin`.
- Aaron Swartz, "Squaring the Triangle" (2011) — `sqz.swartzfamily.com/2011/05/01/squaring-the-triangle/`.
