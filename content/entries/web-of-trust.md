---
title: "Webs of Trust"
slug: web-of-trust
type: explainer
pillars: ["identity"]
description: "Webs of trust establish reputation through social and cryptographic graphs instead of central authorities: models, uses on Nostr and PGP, and attacks."
dek: "A decentralized model for establishing trust and reputation through interconnected social and cryptographic graphs, rather than centralized authorities. In the cypherpunk tradition, WoT empowers individuals to curate their own trust networks for filtering spam, verifying identities, and building resilient reputation systems."
updated: 2026-10-15
created: 2026-07-09
origin: vault
source: "11-Identity/Overview - Web of Trust.md"
aliases: ["Web of Trust", "WoT", "Trust Networks", "Nostr WoT", "GPG WoT"]
tags: ["web-of-trust", "wot", "nostr", "gpg", "pgp", "trust-graphs", "reputation", "decentralized-identity", "nip-85", "rfc-9980", "gpg-2-5-23"]
---

## Summary

Web of Trust (WoT) replaces hierarchical Public Key Infrastructure (PKI) with a peer-to-peer graph where trust flows through personal endorsements. Users sign or follow keys/people they verify, creating paths of transitive trust. Modern implementations on Nostr leverage the social follow graph (NIP-02) for dynamic, queryable trust scores. GPG/PGP remains the foundational cryptographic example with its "strong set" of ~60,000 interconnected keys.

Key applications in freedom tech:
- Spam and Sybil resistance on decentralized social protocols (Nostr)
- Content discovery and reputation scoring
- Pseudonymous identity verification without central issuers
- Cross-client trust portability via oracles and extensions

## Historical Context and Evolution

### Classic Era: PGP/GPG Web of Trust (1991–present)
- Introduced by Phil Zimmermann in PGP (1991) as a decentralized alternative to centralized CAs.
- Users exchange signatures at key-signing parties; trust is calculated based on signature chains and user-assigned trust levels (unknown, marginal, full, ultimate).
- "Strong set": The largest strongly connected component of the keyring. Grew to ~62k by 2018, stabilized around 57-60k by 2022.
- Limitations exposed: Usability issues, key revocation problems, vulnerability to social engineering, and failure to scale beyond crypto enthusiasts. Many analyses (e.g., 2014 Cryptography Engineering blog) highlighted why it "failed" for mainstream use.

### Nostr Era: Social Graph WoT (2022–present)
- Nostr's key-based identities + follow lists enable lightweight, protocol-native WoT.
- Trust propagation via hops in the directed follow graph.
- 2024–2026 explosion of tooling: nostr-wot projects, browser extensions, PageRank-based scoring oracles, visual playgrounds.
- Focus on practical spam filtering for the growing Nostr ecosystem (notes, DMs, marketplaces).

### Trust Graphs Today
Directed graphs combining:
- Positive signals: Follows (NIP-02), endorsements
- Negative signals: Mutes, reports, blocks (NIP-51 lists)
- Computation: Distance (hops), PageRank, custom scoring

## Major Implementations and Projects

### GPG/PGP Foundations
- **GnuPG (GPG)**: Primary implementation. `gpg --list-sigs`, trust database (`trustdb.gpg`).
- Strong set analysis tools and keyservers (though keyservers are deprecated in favor of WKD, DANE).
- Documentation: [Wikipedia Web of trust](https://en.wikipedia.org/wiki/Web_of_trust), RFC 4880.

### Nostr WoT Ecosystem (Primary Modern Focus)
- **nostr-wot organization** (https://github.com/nostr-wot):
  - nostr-wot-extension: Browser extension (Chrome/Brave/etc.) for local trust graph computation. Chrome Web Store available.
  - nostr-wot: Core toolkit for querying social graph distance.
  - nostr-wot-oracle: API service (e.g., wot-oracle.mappingbitcoin.com) for shared trust computation.
  - nostr-wot-sdk: TypeScript/npm library.
- **nostr-wot.com**: Playground for visualizing trust graphs, guides, docs.
- **wot-scoring** (https://github.com/joelklabo/wot-scoring): PageRank-based scoring. Publishes NIP-85 events (kinds 30382–30385). Live at wot.klabo.world. Crawls follow graph and assigns per-pubkey trust.
- **Web of Trust Foundation** (https://weboftrustfoundation.com/): Netherlands-based, Nostr-focused, building open-source protocol software for digital trust.
- Other: Custom client implementations in Damus, Coracle, etc., often using simple hop-distance or follow-graph filters.

### Related Tools & Visualizations
- Graph views inspired by Obsidian (colored edges for trust/mute/unknown).
- NIP-85 for standardized WoT event kinds.
- Integration with other Nostr primitives (NIP-51 lists for custom trust sets).

## How It Works

### Trust Propagation Models
1. **Hop Distance (Simple)**: 
   - 0 hops: Self
   - 1 hop: Direct follows (high trust)
   - 2 hops: Follows-of-follows (medium)
   - 3+ hops: Low trust / noise
   - Example query: `WoT.getDistance(pubkey)` returns hops, paths, mutual follows.

2. **PageRank / EigenTrust variants**: Global or personalized scores accounting for graph structure (used in wot-scoring).

3. **Hybrid**: Local graph + oracle cache + negative signals (mutes reduce score).

### GPG Model
- Signature chains + owner trust levels.
- `gpg --update-trustdb` computes validity.

### Nostr-Specific
- Seed from your own follow list (or curated seeds).
- Clients/oracles rebuild or query the graph on-demand.
- Portable across clients via extensions/oracles.

## Use Cases and Trade-offs

### Use Cases
- **Nostr Spam Filtering**: Automatically hide notes from users >2-3 hops away or with low trust scores.
- **Reputation Systems**: Aggregate trust for marketplaces, DAOs, or content ranking.
- **Pseudonymous Verification**: Confirm "real" humans via social proof without doxxing.
- **Cross-Platform Trust**: Browser extension syncs your WoT everywhere.
- **Governance**: Sybil-resistant voting or airdrops based on social distance.

### Trade-offs & Challenges
- **Sybil Attacks**: Easy to create sockpuppets; mitigated by requiring established connections or proof-of-personhood hybrids.
- **Graph Centralization**: Popular hubs (influencers) dominate scores; "follow the leader" effect.
- **Computation & Privacy**: Full graph crawling is resource-intensive; local computation preferred but limited by client data.
- **Revocation & Dynamics**: Follows change; negative signals important but can be gamed.
- **GPG Legacy Issues**: Poor UX, key management burden, limited adoption.
- **Nostr Advantages**: Lightweight, real-time, integrated with protocol; no separate infrastructure needed.
- Evidence of maturity: Active GitHub orgs, live oracles, published papers on Nostr security (2025), growing extension user base (2026).

### Evidence at a Glance

| Aspect              | GPG/PGP WoT                  | Nostr WoT                          | Maturity          |
|---------------------|------------------------------|------------------------------------|-------------------|
| **Core Mechanism** | Key signatures & trustdb    | Follow graph (NIP-02) + lists     | GPG: Mature<br>Nostr: Active |
| **Scale**           | ~60k strong set             | Millions of pubkeys (growing)     | Nostr expanding  |
| **Key Projects**    | GnuPG                       | nostr-wot/*, wot-scoring, nostr-wot.com | High activity 2026 |
| **Primary Use**     | Email encryption            | Spam filter, reputation on Nostr  | Nostr practical  |
| **Trade-offs**      | Usability, revocation       | Sybil, computation                | Both evolving    |
| **Primary Sources** | Wikipedia, RFC 4880         | GitHub nostr-wot, NIP docs        | Well documented  |

## August 6, 2026 Update — Three-Tier Nostr WoT Stack, RFC 9980, Desktop WoT

This update covers the five-week gap since the July 02 weekly. See [Web of Trust Thursday — August 06 2026 Weekly Update](/briefings/web-of-trust/2026-08-06/) for the full report. Key themes:

### Nostr WoT: Production Infrastructure

The nostr-wot org has completed its three-tier architecture: (1) **Rust oracle** ([nostr-wot-oracle](https://github.com/nostr-wot/nostr-wot-oracle), v1.0.0 Docker, <1ms cached queries, 10K+ QPS, bidirectional BFS), (2) **browser extension** (8 stars, NIP-07 signer + encrypted vault + Lightning wallet + trust badges, 6 languages, updated July 29), (3) **SDK** (npm `nostr-wot-sdk`, React hooks, extension-first fallback). The extension-first design means the WoT follows the user across clients.

[nostr-relay-tray](https://github.com/CodyTseng/nostr-relay-tray) (106 stars) is the breakout WoT project: a desktop personal relay with built-in WoT filtering (Block Rules → Allow Rules / WoT / PoW) packaged for non-technical users. Highest-starred personal relay with WoT.

[AlgoRelay](https://github.com/bitvora/algo-relay) (Bitvora) — social-graph-ranked feeds now adopted by **4 clients** (Jumble, Coracle, Nostur, NoStrudel), validating content discovery via social graph in production.

OpenSats' [relay infrastructure report](https://opensats.org/blog/advancements-in-nostr-relays) documents WoT filtering as a production pattern: "zero spam issues since it is a web-of-trust relay."

### OpenPGP WoT: Post-Quantum Standard and Permanent Schism

[RFC 9980 (Post-Quantum Cryptography in OpenPGP)](https://datatracker.ietf.org/doc/rfc9980) published as IETF Proposed Standard (June 2026). Composite ML-KEM+X25519 for encryption, ML-DSA+Ed25519 for signatures (AND-construction). SLH-DSA standalone permitted. No RSA composite — migration means new key material. v4 carve-out for ML-KEM-768+X25519 is the political compromise for the LibrePGP installed base.

[GnuPG 2.5.21](https://www.gnupg.org) released July 2, 2026 — same day **GnuPG 2.4 was declared end-of-life**. Distributions must adopt 2.5 (LibrePGP v5, not RFC 9580/9980) or fork. The schism is now structural after 2+ years.

[Sequoia `sq` v1.4.0](https://sequoia-pgp.org) (July 6, 2026) — `--cert-store` for alternate certificate stores, WKD improvements, continued RFC 9580/9980 alignment. Sequoia is the RFC-aligned reference implementation.

## October 15, 2026 Update — Amethyst Desktop NIP-85 Production Surface, Bunker 1.0.0, GnuPG 2.5.22–2.5.24 Catch-up

This update covers the eight-week gap since the August 6 reading. See [Web of Trust Thursday — October 15 2026 Weekly Update](/briefings/web-of-trust/2026-10-15/) for the full W42 report. Headline developments:

### Amethyst desktop ships NIP-85 trust provider surface (production)

[Amethyst v1.18.0 (Oct 11 19:27 UTC, 328 commits, "Amethyst Desktop, Web of Trust, etc")](https://github.com/vitorpamplona/amethyst/releases/tag/v1.18.0) is the **first desktop build of Amethyst** and the **first major-client production consumer of NIP-85 trusted-assertion provider scores**. The user's own kind:10040 list (NIP-85 trust providers) is locally indexed; scores are used in requests, notifications and badges with user-selected providers and thresholds. [PR #4437 (Oct 12 16:21 UTC, "fix(tor): count the relays in the user's kind 10040 as their own")](https://github.com/vitorpamplona/amethyst/pull/4437) makes the trust-provider relay set join `TrustedRelayListsState` so that `scores.brainstorm.world` and similar providers route clearnet by default, and NIP-42 auto-auth now fires against provider relays. [Amethyst v1.19.0 (Oct 14 13:16 UTC, 70 commits, "A New Login, Remote Signers on Android, Wayland, and Marketplace Cards")](https://github.com/vitorpamplona/amethyst/releases/tag/v1.19.0) adds native Wayland, NIP-46 remote signing on Android login, per-client rate limiting with NIP-01 backoff (PR #4422), and desktop video compression via FFmpeg. **The W40–W41 oracle work has a consumer in the largest Nostr Android/Desktop client.** This is the production validation of the [Aug 6](/briefings/web-of-trust/2026-08-06/) three-tier Nostr-WoT architecture: oracle → SDK → extension → major-client surface.

### Nostr-WoT org hits stable on NIP-46 server side

[@nostr-wot/bunker 1.0.0 stable on npm (Oct 12 22:31:53 UTC)](https://www.npmjs.com/package/@nostr-wot/bunker) — the **first Nostr-WoT production-ready release** (the org's first server-side package, after 0.2.0 on Oct 5 and a 0.2.1 patch on Oct 8). Direct deps: `@noble/hashes`, `@nostr-wot/relay` (new org-owned relay client); peer: `nostr-tools >= 2.0.0`. The 1.0.0 stamp signals *the NIP-46 server-side surface is stable* — third-party hosts can now build on it without tracking every patch release. The same minute (22:31:13 UTC) the extension committed `808458cd` "Adopt GPLv3 licensing and accurate store metadata" — the org is shipping a *coordinated* stable-on-server + license-consolidation-on-client release.

[Amber 6.6.9 (Oct 14 12:42 UTC)](https://github.com/greenart7c3/Amber/releases/tag/v6.6.9) ships three GHSA advisories: [GHSA-8f7m-9g64-vrjw](https://github.com/greenart7c3/Amber/security/advisories/GHSA-8f7m-9g64-vrjw) (cache race on permission revocation + "fully trusted" overriding active reject; reported by @mptfire), [GHSA-g62f-m6pm-jv9p](https://github.com/greenart7c3/Amber/security/advisories/GHSA-g62f-m6pm-jv9p) (60s clipboard clear for copied secrets), [GHSA-wv7c-hq2j-ppc5](https://github.com/greenart7c3/Amber/security/advisories/GHSA-wv7c-hq2j-ppc5) ("require unlocked device" preserves old wrapping key until migration completes). The signing key `885822EED3A26A6D` is **expired**; users verifying the tag should treat the signature as advisory. **The bunker 1.0.0 stable + Amber security fix combo is the trust-stack's "vulnerability-before-stable" closing.**

### GnuPG 2.5.22 → 2.5.23 → 2.5.24 — three-release cluster the prior readings missed

The W40 + W41 readings both read "GnuPG 2.5.22 unreleased" based on stale master NEWS. The actual timeline:

- **2.5.22 (2026-08-31)** — bug-fix release: TOFU trust model fix to check UTK signatures (T8404, security-relevant), trustdb recursive-lock fix (T8317), double-free in import_revoke_cert (T8328), bkuptocard regression fix.
- **2.5.23 (2026-09-22) — the RFC 9980 gate**: `gpg --allow-9980` opt-in flag, ML-KEM (Kyber) with X448/X25519/Brainpool/NIST curves in 9980 mode, ED25519/X25519 under names "ietf27"/"ietf25" per RFC 9580, experimental `--compliance=fips` GCM bulk-encryption mode. **Security fixes**: exploitable printf bug in `gpgsm --debug x509` (rGe6d92ff7af), OOB read in DNS CERT record parser (T8464), OOB in faulty-card DO parsing (T8465). Werner Koch political line: *"The use of this option is only recommended if external policy requirements demand the use of these governmental approved specification. PGP folks requiring some PQC resistance should keep on using the standard LibrePGP Kyber algorithm introduced 2 years ago."*
- **2.5.24 (2026-09-23)** — one-day hotfix for smartcard detection regression in 2.5.23 (Nitrokey 3 + pcsc-shared, T8331). Gpg4win 5.1.1 released alongside.
- **2.5.25 (unreleased) — T8466**.

**The W41 trigger-event model needs correction**: 2.5.22 + 2.5.23 + 2.5.24 all shipped and **no kind:10203 stair-step fired** — the bottleneck is the Nostr client integration (no major client wires GnuPG into a kind:10203 publisher), not the GnuPG release. The Nostr-WoT extension's `npm run pqc:keygen` (v0.4.0, unchanged since Aug 11) and Obelisk (QuantaKrypto) are still the only kind:10203 publishers. **NIP #2434 (PQ identity keys) now 68 days frozen** (W41: 61; the longest gap in 2026).

### Evidence at a Glance (Updated October 2026)

| Aspect | GPG/PGP WoT | Nostr WoT | Maturity |
|--------|-------------|-----------|----------|
| **Core Mechanism** | Key signatures & trustdb (TOFU fixed in 2.5.22) | Follow graph (NIP-02) + NIP-85 trusted assertions (kinds 30382–30385, 10040) + kind:10040 trust-provider relay list | GPG: Mature + active RFC 9980 integration<br>Nostr: Production (Amethyst desktop consumer) |
| **Scale** | ~60k strong set (GPG); 1.25M+ pubkeys (oracle) | 1.25M+ pubkeys indexed (oracle) | Nostr expanding |
| **PQ Standard** | RFC 9980 published June 2026; 2.5.23 ships `--allow-9980` opt-in | kind:10203 ML-KEM-1024 + ML-DSA-87 (CNSA 2.0 Cat 5); plateau 26 for 28 days | RFC 9980 partial impl; 2.5.23 = opt-in only |
| **Key Projects** | GnuPG 2.5.22 → 2.5.23 → 2.5.24, Sequoia sq 1.4.0 (95 days dormant) | nostr-wot oracle/extension/SDK/bunker (1.0.0 stable Oct 12), nostr-relay-tray (106★), AlgoRelay (4 clients), **Amethyst 1.18.0 NIP-85 consumer** | High activity W42 |
| **Primary Use** | Email encryption, code signing | Spam filter (production, **Amethyst desktop with NIP-85**), feeds (4 clients), reputation, secure remote signing (NIP-46 bunker 1.0.0 + Amber 6.6.9 hardened) | Both production |
| **Trade-offs** | Usability, LibrePGP schism, PQ migration opt-in only, 2.5.23 kind:10203 = no Nostr-client bridge | Sybil, computation, kind:30385 collision (PR #2418, 89d open), kind:10203 plateau (28d, no trigger), NIP #2434 68d frozen | Both evolving |
| **Primary Sources** | RFC 9580, RFC 9980, gnupg.org, gnupg-announce lists | GitHub nostr-wot, NIP docs, OpenSats reports, Compass #43 + #44, Amethyst 1.18.0 release notes | Well documented |

### Out-of-scene

**Sequoia `sq`** v1.4.0 (July 6, 2026) is still the most recent release — **95 days dormant**. **OpenPGP.js** 7 commits no PQC. **Idena, Rarimo, World ID 4.0** unchanged at the spec level. **RFC 9980 (Post-Quantum Cryptography in OpenPGP)** unchanged since June 2026, no new errata. **NIP #2434 (PQ identity keys) now 68 days frozen** — the longest gap in 2026. **PR #2418 (NIP-XX Trusted Relay Assertions / kind:30385 collision) now 89 days open** — collision becoming de-facto standard. **Letdown2491's parallel project `forgesworn/nostr-attestations` (kind 31000 unified attestation, npm package)** is maintenance-mode — the same author as the kind:30385 dispute, with effort split across two parallel attestation surfaces.

### Evidence at a Glance (Updated August 2026)

| Aspect              | GPG/PGP WoT                  | Nostr WoT                          | Maturity          |
|---------------------|------------------------------|------------------------------------|-------------------|
| **Core Mechanism** | Key signatures & trustdb    | Follow graph (NIP-02) + lists     | GPG: Mature<br>Nostr: Active/Production |
| **Scale**           | ~60k strong set             | 1.25M+ pubkeys indexed (oracle)    | Nostr expanding  |
| **PQ Standard**     | RFC 9980 published June 2026; GnuPG follows LibrePGP | N/A (Nostr uses secp256k1) | RFC 9980 defined; implementation bifurcated |
| **Key Projects**    | GnuPG 2.5.21, Sequoia sq 1.4.0 | nostr-wot oracle/extension/SDK, nostr-relay-tray (106★), AlgoRelay (4 clients) | High activity 2026 |
| **Primary Use**     | Email encryption, code signing | Spam filter (production), feeds (4 clients), reputation | Both production  |
| **Trade-offs**      | Usability, LibrePGP schism, PQ migration | Sybil, computation, adoption gap | Both evolving    |
| **Primary Sources** | RFC 9580, RFC 9980, gnupg.org | GitHub nostr-wot, NIP docs, OpenSats reports | Well documented  |

## Sources & Further Reading

- nostr-wot GitHub: https://github.com/nostr-wot
- Nostr WoT site: https://nostr-wot.com/
- HackerNoon article on extension (Feb 2026)
- Wikipedia: Web of trust (GPG history)
- wot-scoring repo and live demo
- Web of Trust Foundation
- Academic: Analyses of PGP strong set (various papers 2003–2022)
- Nostr protocol NIPs (especially NIP-02, NIP-51, NIP-85)

*This note synthesized from primary GitHub repos, project sites, Wikipedia, and recent 2024–2026 articles. Updated weekly as part of UngovernableTech research rotation.*

*Tags for Obsidian graph: #web-of-trust #nostr #decentralization #cypherpunk*
