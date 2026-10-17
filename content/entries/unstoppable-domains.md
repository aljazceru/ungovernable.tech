---
title: "Unstoppable Domains"
slug: unstoppable-domains
type: deep-dive
pillars: ["naming"]
readiness: cautionary
description: "A cautionary case study: Unstoppable Domains sells blockchain-minted names, but the company's control over resolution undermines the sovereignty claim."
dek: "A cautionary case study in decentralized naming. Unstoppable Domains sells blockchain-minted names (`.crypto`, `.wallet`, `.nft`, `.x`, `.bitcoin`, and more) on Polygon and other chains, marketed as censorship-resistant, and now (per a Sept 2025 patent filing) building a wallet-vote-based takedown mechanism. The lesson: blockchain-anchored ≠ decentralized governance. See Overview - Decentralized DNS for the comparative landscape; Namecoin for the original chain-DNS that has no company at all."
updated: 2026-06-22
created: 2026-06-22
origin: vault
source: "03-Decentralized-DNS/Unstoppable Domains.md"
aliases: ["UD", "Unstoppable", ".crypto", ".wallet", ".nft", ".x", ".bitcoin"]
tags: ["unstoppable-domains", "web3", "naming", "takedown", "centralization", "deep-dive"]
---

## Summary

Unstoppable Domains (UD) is a VC-backed company founded in 2018 that sells second-level names registered on blockchain networks (initially Ethereum, now primarily Polygon). It claims ~4.6M+ names across many TLDs. The names are **technically** minted on a chain (so the name itself is a token), but the **registry interface** is the UD company's website, and the company has been actively pursuing the ability to take names down via a patent-pending mechanism that uses wallet-vote thresholds.

This is the structural difference between [ENS](/kb/ens/) / [Handshake](/kb/handshake/) / [Namecoin](/kb/namecoin/) (which are protocol-level systems with no off-chain operator that can take a name down) and a company that happens to use a chain as a database. The patent filing is significant because it explicitly acknowledges the centralization that critics have pointed out for years.

## What UD sells

- **`.crypto`** — the original UD TLD.
- **`.wallet`** — wallet-themed names.
- **`.nft`**, **`.x`**, **`.bitcoin`**, **`.dao`**, **`.888`**, **`.zil`**, **`.go`**, **`.blockchain`**, others.
- Multi-chain: Polygon (primary), Zilliqa (legacy), Ethereum (legacy).

Each name is minted as a token; the buyer holds the token in their wallet. Names are sold once (no annual renewal). Sales model: premium prices for short and common names; otherwise $5–$40 typical.

The technical claim: the name is a token, so it's "yours forever." The practical claim: the company maintains the resolution infrastructure (resolver service), the website (where you mint), and the customer support.

## Why UD is a centralized system in decentralized packaging

A real decentralized naming system has three properties:

1. **Ownership** is determined by the chain state, not by an operator.
2. **Resolution** works without the operator's cooperation.
3. **Takedowns** are infeasible without a chain reorg or a key compromise.

UD satisfies (1) at the token level — the NFT is yours in your wallet — but not (2) or (3):

| Property | UD | ENS | Handshake | Namecoin |
|----------|----|----|-----------|----------|
| Token/chain ownership | Yes (NFT) | Yes (NFT) | Yes (UTXO) | Yes (UTXO) |
| Resolution independent of company | Limited (relying on UD resolver) | Yes (any RPC) | Yes (hnsd, public resolvers) | Yes (ncdns) |
| Takedown by operator | **Yes (claimed in patent)** | No (no operator) | No (no operator) | No (no operator) |
| Renewal required | No (one-time) | Yes (annual rent) | No (auction + burn) | Yes (every 200 days) |
| ICANN accreditation | Yes (also sells `.com`) | No | No | No |

UD is also **ICANN-accredited** — the only blockchain-domain company with both the ICANN registrar credential *and* the ICANN 84 partner D3 Protocol partnership. This means UD can sell both legacy Web2 domains and Web3 names. It also means UD is bound by UDRP, court orders, and the ICANN contractual regime, like any other accredited registrar.

## The takedown patent (Sept 2025)

In **September 2025**, news emerged that UD had filed a US patent application (filed Feb 2024, published Aug 2025) titled "Deactivation of decentralized domains." The patent describes a mechanism where a name can be deactivated if:

1. A threshold of wallet accounts signs messages saying the name is problematic (a "takedown" vote).
2. A "reviewing authority" signs a message on behalf of a domain takedown organization.
3. The name's safety score drops below a threshold (computed from access patterns, complaints, content).

The patent's own text is candid:

> "One of the features of blockchain-based naming systems is also a bug: it's not possible to take down domains that are used in bad ways. ... taking down and suspending domains is critical to a functioning naming system and necessary to attract end-user companies."

The patent also describes anti-abuse design: wallet age, account reliability, time windows — these prevent trivial Sybil-based takedown attacks. So the proposed mechanism is a "soft" takedown requiring community agreement, not a unilateral kill switch.

But the structural fact remains: **there is a takedown path that does not require a chain reorg or a key compromise**. That is a meaningful departure from what the marketing ("Unstoppable") implies.

## Why UD built the takedown mechanism

The company's stated reason: brands and enterprise customers need a way to remove names used for fraud, phishing, or abuse. Without a takedown path, mainstream adoption is blocked. The implicit reason: UDRP, ICANN contractual obligations, and reputational concerns with hosting a global phishing platform push toward having a takedown mechanism regardless.

The patent suggests a quasi-decentralized mechanism (community voting + reviewing authority) rather than unilateral takedowns. The proposed design is at least more sophisticated than a single admin key, but it is still a takedown path that exists outside the chain.

## Comparison with the truly decentralized alternatives

| System | Can an operator take the name down? | Resolution path | Renewal | Censorship-resistance story |
|--------|--------------------------------------|------------------|---------|-----------------------------|
| **Unstoppable Domains** | **Yes (per Sept 2025 patent)** | UD resolver / DApps | No (one-time) | Weak — operator has takedown path |
| [ENS](/kb/ens/) | No | Any RPC, CCIP-Read | Yes (annual rent) | Strong — chain + DAO |
| [Handshake](/kb/handshake/) | No | hnsd, HNS-aware resolvers | No (auction + burn) | Strong — chain, no operator |
| [Namecoin](/kb/namecoin/) | No | ncdns locally | Yes (every ~200 days) | Strongest — no operator, 15-year track record |
| [GNS](/kb/gnu-name-system/) | N/A (no global namespace) | GNUnet resolver | No | Strong — petname system |
| [PKARR](/kb/pkarr/) / [Pubky](/kb/pubky/) | No | pkdns, Mainline DHT | No | Strong — Ed25519, no operator |
| [Overlay Naming - Tor .onion and I2P](/kb/onion-and-i2p-naming/) | No | Overlay-native | No | Strongest — no operator at all |
| [Cardano DNS](/kb/cardano-dns/) | No | cdnsd | No (auction) | Strong — Handshake + Cardano |
| [Nomen](/kb/nomen/) | No | Indexer | No | Experimental — Bitcoin + Nostr |
| [DNNS](/kb/dnns/) | Unknown (no public code) | Lithosphere | Unknown | Unverified |

The pattern is clear: a system with a corporate operator cannot make an "unstoppable" promise. ENS, Handshake, Namecoin, GNS, PKARR, Tor, I2P, and Nomen all have no operator that can take a name down. UD has one.

## UD as the proof-by-counterexample

UD is useful as a *case study* in decentralized naming precisely because it shows the limits of "blockchain-anchored but company-controlled":

1. **The chain anchors ownership at the token level.** UD's NFT-mint is real, on a real chain, in a real wallet.
2. **The chain does not anchor governance.** The company can change the resolver, mint new names, refuse to support a name in their tools, and (per the patent) deactivate a name.
3. **The user's experience is centralized.** Most users buy names through the UD website, use the UD resolver, and rely on the UD's browser extension or mobile app to resolve `.crypto` and friends.
4. **The "decentralized" branding is misleading.** The token is on a chain; the system is not.

For an Ungovernable.tech stack, the lesson is that "decentralized" should be reserved for systems whose governance and resolution are also decentralized. Chain-anchored ownership is necessary but not sufficient.

## UD's positioning in 2026

UD continues to operate as a Web3 naming company, but with three structural constraints:

1. **Patent-pending takedown mechanism** — explicit acknowledgment that the system is not "unstoppable" in the literal sense.
2. **ICANN accreditation** — UD is also a real registrar for real Web2 domains; the company has both a Web2 and a Web3 business.
3. **D3 Protocol partnership (announced at ICANN 84)** — tokenization of Web2 domains; this is a different product (D3's `.box`, `.art`, `.locker` TLDs) that intersects with UD's domain business.

The crypto-native users who wanted a "decentralized domain" generally migrated to ENS, Handshake, or PKARR. UD's customer base is now primarily enterprise and Web2 brands exploring tokenized domain products.

## Trade-offs

### Strengths (relative to the alternatives)

- Easy onboarding — credit card, no crypto wallet needed.
- One-time payment, no renewal.
- ICANN-accredited; can also sell real `.com` and friends.
- Big marketing budget; "Unstoppable" branding had a real effect on awareness.
- Customer support; enterprise integrations.

### Limitations (relative to decentralized alternatives)

- Operator can take a name down (per Sept 2025 patent).
- Resolution depends on UD's resolver infrastructure.
- Tied to UD's chain of choice (Polygon) for the .crypto family.
- ICANN-bound by UDRP and contractual obligations.
- Premium pricing for short names; speculative secondary market.
- No real censorship-resistance story.

## Use cases (real and aspirational)

| Use case | Reality |
|---------|---------|
| Crypto wallet address | Workable, but ENS has more wallet integrations |
| Censorship-resistant website | Weak — UD has a takedown path |
| Brand domain (Web3 + Web2 dual) | UD's strongest use case; D3 partnership extends this |
| Speculative investment | Real market; the 2021 peak drove a secondary-market boom |
| Enterprise / corporate identity | Real market; less censorship-resistance, more convenience |

## Evidence at a glance

| Item | Evidence | What it supports |
|------|----------|------------------|
| UD "Deactivation of decentralized domains" patent | Filed Feb 2024, published Aug 2025; reported Sept 2025 by Domain Name Wire | UD is building an explicit takedown mechanism |
| 4.6M+ names registered | Domain Details 2025 KB | Real, large user base |
| ICANN accreditation | Oxford Info Labs / AFNIC report | UD is a real registrar, not only a Web3 company |
| D3 Protocol partnership | MarkMonitor blog 2025 | UD / D3 working on tokenized Web2 domains |
| Oxford Information Labs / AFNIC report | Q4 2023; 31 blockchain providers studied; blockchain = 0.5% of total domains | Scale of blockchain domains is small but real |
| Forbes America's Best Startup Employers 2025 | UD blog Mar 2025 | UD is a real, growing company |

## Recent developments (2024–2026)

- **Feb 2024 → Aug 2025**: UD files and publishes the takedown patent.
- **Sep 2025**: Domain Name Wire exposes the patent; community discussion on the contradiction with "Unstoppable" branding.
- **2025**: D3 Protocol partnership announced; ICANN 84 partnership materializes.
- **2025**: Oxford Information Labs + AFNIC publish mapping study; UD is one of only two ICANN-accredited blockchain providers (with Freename).
- **2025**: UD appears on Forbes America's Best Startup Employers list for the fourth consecutive year.
- **2026**: UD continues to operate; the takedown mechanism remains in patent-pending state, not yet activated in production.

## Primary sources

- Unstoppable Domains — `unstoppabledomains.com`.
- "Deactivation of decentralized domains" patent — `domainnamewire.com/wp-content/Unstoppable-takedown-patent.pdf` (Domain Name Wire coverage Sept 2025).
- Domain Name Wire coverage — `domainnamewire.com/2025/09/02/unstoppable-domains-files-patent-for-way-to-take-down-blockchain-domains`.
- Oxford Information Labs + AFNIC report — `oxil.uk/news/mapping-blockchain-domain-providers-10-key-findings-from-oxford-information-labs-and-afnic`.
- MarkMonitor Web3 update 2025 — `markmonitor.com/blog/web3-and-web2-updates-on-blockchain-domains-in-2025`.
- Domain Details Web3 investing KB 2025 — `domaindetails.com/kb/domain-investing/blockchain-domains-web3-investing`.
