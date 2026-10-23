---
title: "Web of Trust on Nostr"
slug: nostr-web-of-trust
type: deep-dive
pillars: ["identity"]
readiness: experimental
description: "How Nostr uses the social graph to fight spam and rank content without central moderation: trust scores, NIPs, implementations and attacks."
dek: "Nostr's Web of Trust (WoT) is the practical answer to a problem created by the protocol's strongest property: anyone can create a keypair and publish signed events to relays without asking permission."
updated: 2026-08-27
created: 2026-05-07
origin: vault
source: "02-Cryptography/Nostr Web of Trust.md"
aliases: ["Nostr WoT", "Nostr trust graph", "NIP-85 reputation"]
tags: ["web-of-trust", "nostr", "trust-graph", "sybil-resistance", "reputation", "spam-filtering"]
---

## Summary

Nostr's Web of Trust (WoT) is the practical answer to a problem created by the protocol's strongest property: anyone can create a keypair and publish signed events to relays without asking permission. That makes [Nostr](/kb/nostr-identity/) censorship-resistant, but it also means clients and relays cannot rely on platform accounts, KYC, or central moderation to decide which pubkeys and events deserve attention.

The Nostr WoT pattern treats the social graph as a local, user-chosen reputation substrate. A client, relay, or oracle starts from a set of trusted seed pubkeys, crawls follow lists and other graph signals, and asks questions such as:

- Is this author within one or two hops of my graph?
- Do people I trust mute or report this pubkey?
- Has a trusted service provider published a signed [NIP-85](https://nips.nostr.com/85) rank for this user or event?
- Should my personal relay store this event, reject it, or keep it only after a proof-of-work fallback?

The key design point is **not** a universal score. A Nostr WoT score is only meaningful when you know the seed set, edge types, decay rules, algorithm, provider key, freshness, and context. A global rank can help discovery; a local graph helps spam filtering; a community graph can enforce norms; a relay policy can save disk and bandwidth. Collapsing all of these into one opaque number recreates platform moderation under a decentralized brand.

## Historical context

### From OpenPGP certification to graph-native social trust

The original [OpenPGP Web of Trust](/kb/openpgp-web-of-trust/) asked whether an OpenPGP certificate was valid: does this public key belong to this name/email, and do enough trusted introducers certify it? Nostr asks a more dynamic question: among millions of public-key identities, which authors, replies, relays, lists, zaps, and reports should a user see or believe?

Nostr identities are not certificate bundles. They are secp256k1 pubkeys that sign events. Relays do not interpret identity; they store and serve events. That means the WoT data is not attached to a certificate in the OpenPGP sense. It emerges from Nostr event kinds:

- **NIP-02 follow lists** — weak positive edges; "I subscribe to this pubkey".
- **NIP-51 lists** — mute lists, curated sets, bookmarks, communities, relay lists, and other user-maintained collections.
- **NIP-56 reports** — negative edges or abuse assertions.
- **NIP-57 zaps** — costly positive signals when combined with Lightning payments.
- **NIP-72 communities** — community-specific moderator and membership context.
- **NIP-85 trusted assertions** — signed provider-computed ranks, counts, and WoT metrics.

The result is a more flexible but messier trust graph. A follow is not a certification. A zap is not necessarily trust. A report can be abuse or retaliation. The system works only when software preserves edge semantics and lets users choose policy.

### Why NIP-85 matters

[NIP-85 Trusted Assertions](https://nips.nostr.com/85) exists because many WoT calculations require crawling large portions of the event graph and recomputing metrics over time. Mobile clients and simple web clients often cannot do this locally. NIP-85 lets a user declare trusted service providers via kind `10040`; those providers publish signed, addressable assertion events:

| Subject | Event kind | Typical result tags |
|---|---:|---|
| Pubkey / user | `30382` | `rank`, `followers`, `post_cnt`, `zap_amt_recd`, `reports_cnt_recd` |
| Regular event | `30383` | `rank`, `comment_cnt`, `reaction_cnt`, `zap_amount` |
| Addressable event | `30384` | rank and engagement for replaceable/addressable objects |
| External identifier | `30385` | rank for NIP-73 identifiers such as websites, books, places, hashtags |

A provider's assertion is not globally authoritative. It is a signed output from an algorithm and key the user chose. The NIP explicitly requires providers to use different service keys for distinct algorithms, including personalized algorithms, so clients can distinguish "global rank" from "Alice's local trust graph".

## Major implementations and tools

| Project | Role | Maturity / activity | Notes |
|---|---|---|---|
| [nostr-wot/nostr-wot](https://github.com/nostr-wot/nostr-wot) | Toolkit, SDK, extension API, oracle pattern | Experimental / active; GitHub API 2026-05-07: 6 stars, 2 forks, TypeScript, MIT, not archived, pushed 2026-04-29 | Query social distance between pubkeys; self-hostable graph/oracle infrastructure. |
| [nostr-wot/nostr-wot-sdk](https://github.com/nostr-wot/nostr-wot-sdk) | Monorepo JavaScript/TypeScript SDK with scoped packages | Active; 47 commits, MIT, monorepo with 4 scoped packages | `@nostr-wot/data` (portable fetchers + React hooks), `@nostr-wot/wot` (scoring + extension bridge), `@nostr-wot/relay` (low-level pool/batcher), `nostr-wot-sdk` (back-compat meta-package); React/Solid hooks, NIP-65 outbox. |
| [nostr-wot-extension](https://github.com/nostr-wot/nostr-wot-extension) | Browser extension exposing WoT queries | Experimental / active; 6 stars, 2 forks, TypeScript, MIT, pushed 2026-04-26 | Useful browser boundary, but risky if combined with key custody; pair with [Remote Signing](/kb/remote-signing/) where possible. |
| [wot-relay](https://github.com/barrydeen/wot-relay) | Personal/archival Nostr relay | Emerging / active; 85 stars, 28 forks, Go, pushed 2026-04-22 | Archives notes from people followed by the owner and people they follow; can expose via HTTPS or Tor. |
| [Chronicle](https://github.com/dtonon/chronicle) | Personal relay with WoT spam protection | Active; v0.5.0 released May 2026; 30 stars, 4 forks, Go, pushed 2026-04-30 | Stores conversations owner participated in; second-degree WoT + PoW fallback; Blossom media server built in; WoT as relay policy. |
| [Brainstorm](https://github.com/Pretty-Good-Freedom-Tech/brainstorm) | Personalized WoT relay with self-hosted NIP-85 scoring | Paused; MIT; Freedom-tech-specific | Last push Feb 2026 (docs only). Generates own nsec, signs kind 30382 events, publishes kind 10040, filters spam by social graph, auto-publishes scores every N hours. Valuable reference design; active development stalled. |
| [wot-scoring](https://github.com/joelklabo/wot-scoring) | PageRank-based scoring and NIP-85 publishing | Experimental; 2 stars, Go, MIT, pushed 2026-02-11 | Demonstrates provider-computed rank publication as NIP-85 events; ~~live at wot.klabo.world~~ **dead — wot.klabo.world DNS NXDOMAIN as of 2026-08-20** |
| [nostr-relay-plugin WoT Guard](https://github.com/CodyTseng/nostr-relay-plugin) | Relay filtering plugin concept | Small / active; 1 star, TypeScript, MIT, pushed 2026-04-15 | Relay-side guard pattern; useful but demands transparent policy. |
| [DCoSL](https://github.com/wds4/DCoSL) | Decentralized curation / score ledger concept | Experimental; 12 stars, MIT, pushed 2024-03-11 | Minimal protocol for decentralized reputation and web-of-trust signals. |
| [Noswot](https://codeberg.org/weex/noswot) | Nostr follows/reports WoT builder | Experimental; Codeberg repo, Python, updated 2024-12-03 | Builds a web of trust from follows and reports. |
| [Nostr Compass: Web of Trust](https://nostrcompass.org/en/topics/web-of-trust/) | Educational reference | Active documentation | Concise explanation of graph construction, seed selection, propagation, cutoffs, and NIP-85. |

## How scoring is computed

### 1. Social distance / hop count

The simplest WoT rule is graph distance:

```text
me ─follow→ Alice ─follow→ Bob ─follow→ Carol
```

Bob is two hops away. Carol is three hops away. A client can choose to show first- and second-degree replies by default while hiding farther accounts unless they have other signals. This is explainable and cheap, but it overweights bridge nodes and treats follows as endorsements.

### 2. Weighted edges

A better model preserves edge type:

| Edge | Meaning | Suggested use |
|---|---|---|
| Follow | Subscription / weak endorsement | Positive but low weight; do not treat all follows equally. |
| Curated list | Intentional inclusion in a named context | Stronger if list purpose is explicit. |
| Mute / block | Negative preference | Strong only if you trust the muter and context. |
| Report | Abuse/spam allegation | Rate-limit and weight carefully; vulnerable to brigading. |
| Zap | Costly positive signal | Useful when combined with sender reputation; can be bought. |
| NIP-05 / domain proof | Key controls a domain mapping | Identity-control proof, not moral trust. |
| NIP-85 assertion | Provider-computed score | Trust depends on provider key and methodology. |

### 3. PageRank-like propagation

PageRank-style algorithms propagate score through incoming links. They help global discovery because highly endorsed accounts surface even when the user has a sparse graph. The downside is centralization: high-degree accounts become de facto trust roots, and small communities may be drowned out by global popularity.

### 4. Local seeded rank

A local seeded graph starts from the user's own follow list or a manually chosen seed set. It is more Sybil-resistant for personal spam filtering because attackers need edges from the user's real graph. It is less useful for new users, who have no graph and must either import defaults or trust a provider.

### 5. Relay policy

Relays can use WoT at ingestion time. `wot-relay` archives events from the owner's follow graph. Chronicle accepts events from conversations the owner participated in, then applies a second-degree WoT rule and optional PoW fallback. This shifts computation away from clients and reduces storage, but relay policy becomes critical infrastructure. Good relays should publish policy, allow user override, and support exit.

## Use cases

### Spam filtering

The strongest live use case is spam reduction. A decentralized social protocol cannot depend on one spam team. WoT lets clients and relays ask whether a reply, DM, mention, or event comes from an account near the user's graph. Unknown accounts can be hidden, rate-limited, charged, or asked for proof-of-work.

### Content discovery

Global search and trending feeds are Sybil magnets. A WoT feed can rank notes by trusted graph proximity, trusted zaps, trusted reposts, and trusted reports. This is especially useful for topic-specific communities where global popularity is a bad proxy for quality.

### Payment and merchant directories

Lightning address directories, merchant listings, event calendars, and service marketplaces need impersonation resistance. WoT can answer "who in my graph has interacted with this merchant?" rather than "does a centralized directory say this merchant is legitimate?"

### Decentralized moderation

Communities can curate trusted moderator lists, report providers, or allowed-author sets without imposing that policy globally. The freedom-tech requirement is that users can switch clients, relays, seed sets, or NIP-85 providers.

### Key transition and pseudonym continuity

A pseudonym can migrate keys by publishing signed transition statements, getting attestations from trusted peers, and retaining graph edges. This does not solve account recovery by itself, but it supplies social evidence that a new key is likely a continuation. See [Nostr Key Custody and Recovery](/guides/nostr-key-custody/) and [Overview - Identity & Pseudonymity](/kb/identity-and-pseudonymity/).

## Trade-offs and attack surface

| Issue | Why it matters | Mitigation |
|---|---|---|
| Cold start | New users have no graph and inherit defaults. | Starter packs should be visible, editable, and removable; encourage local seed selection. |
| Ambiguous follows | A follow can mean friendship, curiosity, hate-reading, or monitoring. | Preserve edge semantics; combine with lists, mutes, reports, and zaps. |
| Sybil clusters | Fake accounts can trust each other. | Anchor scoring in local trusted seeds; cap tightly connected new clusters; add cost signals. |
| Bridge capture | One high-degree account shortens many paths. | Limit path length, cap influence, diversify paths, expose explanations. |
| Oracle capture | One NIP-85 provider becomes hidden moderation authority. | Support multiple providers, self-hosting, visible provider keys, and signed methodology. |
| Graph deanonymization | Follows, mutes, and reports leak social structure. | Use private/encrypted lists where possible; split personas; avoid universal identifiers. |
| Report brigading | Coordinated reports can punish targets. | Weight reports by trusted reporters; rate-limit; require evidence/context. |
| Stale trust | Old follows and scores outlive relationships. | Time decay, refresh windows, revocations, periodic review. |

## Evidence at a glance

| Evidence | Source | Strength | What it shows |
|---|---|---|---|
| NIP-85 spec | [nips.nostr.com/85](https://nips.nostr.com/85) | Primary spec; draft optional | Nostr has a standardized event pattern for signed provider-computed trust/rank assertions. |
| nostr-wot toolkit | [GitHub](https://github.com/nostr-wot/nostr-wot) | Working code; experimental | WoT oracle/SDK/extension pattern is active as of 2026-04. |
| wot-relay | [GitHub](https://github.com/barrydeen/wot-relay) | Working relay; emerging adoption | Relay-side archiving based on first/second-degree graph is practical. |
| Chronicle | [GitHub](https://github.com/dtonon/chronicle) | Working personal relay; active 2026 | Personal relays can combine Outbox model, Blossom media, owner-participation rules, and WoT spam control. |
| Nostr Compass | [Web of Trust topic](https://nostrcompass.org/en/topics/web-of-trust/) | Secondary reference | Clear articulation of graph construction, seed selection, score propagation, and NIP-85 trade-offs. |
| Brainstorm WoT relay | [GitHub](https://github.com/Pretty-Good-Freedom-Tech/brainstorm) | Active; MIT; Freedom-tech org | Personalized WoT relay: generates own nsec, signs kind 30382 events, publishes kind 10040, auto-publishes scores. |
| Nostr empirical study | [arXiv:2402.05709](https://arxiv.org/html/2402.05709v2) | Academic network analysis | Nostr is large enough that graph structure, decentralization, and relay behavior need empirical measurement. |

## Design rules

1. Treat WoT as **local policy**, not universal truth.
2. Preserve edge types; do not collapse follows, mutes, zaps, and reports into one opaque score without provenance.
3. Separate identity-control proofs from reputation claims.
4. Publish provider keys, algorithms, freshness, and seed assumptions.
5. Prefer self-hostable or multi-provider architectures.
6. Give users override, explanation, and exit.
7. Combine WoT with cost signals for unknown accounts, not as a magic Sybil cure.
8. Avoid leaking more graph data than the user intentionally publishes.

## Late-May 2026 Developments

### Cross-Client WoT Trust Score Display (Q1 2026)

Multiple independent Nostr clients began displaying WoT-based trust scores in their UI during Q1 2026. Amethyst (Android), Primal, and Coracle all surface trust scores on user profiles. Amethyst's changelog notes that "by connecting to a WoT provider, you can see trust scores and verified follower counts directly on user pictures." Coracle displays "If you can't tell the difference between me and a scammer, use a nostr client with web of trust support."

This marks WoT transitioning from developer-facing library feature to user-visible product feature — significant for adoption, but raises UX design questions about presenting trust without a surveillance-score aesthetic.

### FROST RFC 9591 and Frostr Ecosystem Maturity

RFC 9591 (FROST Protocol) was published by the IRTF in June 2024, giving threshold Schnorr signatures a stable normative reference. For Nostr's Frostr ecosystem, this means Bifrost, Igloo, and other Frostr-related libraries now have a standard to implement against. The RFC covers the signing protocol but not distributed key generation — trusted-dealer vs. DKG remains an implementation choice. Nonce reuse is the critical footgun across all FROST deployments.

### NIP-26 Delegation Revocation Gap

GitHub issue #654 on the NIPs repository proposes a revocation mechanism for NIP-26 delegated keys. NIP-26 currently only supports time-bounded expiry, not revocation. When NIP-46 bunker signers use long-expiry NIP-26 delegation keys for UX, a compromised delegate can operate until natural expiry. The proposed fix — root-key-signed revocation certificates distributed to relays — would let the root key burn a compromised delegate immediately. This is important for the custody model because delegation is central to the NIP-46 flow, and currently delegation has no consent revocation path.

### Brainstorm WoT Relay (Freedom-Tech Specific)

Brainstorm from Pretty-Good-Freedom-Tech continues active development as a self-hostable personalized WoT relay. It generates its own nsec at install time, signs and publishes NIP-85 kind 30382 events, declares itself as a kind 10040 provider, filters content by the user's social graph, and auto-publishes scores every N hours. Notable as an explicitly freedom-tech-aligned project in the WoT relay space.

### May 28 Update — GitHub Activity Snapshot

| Project | Stars | Forks | Last push | Notes |
|---------|------:|------:|-----------|-------|
| [gpg/gnupg](https://github.com/gpg/gnupg) | 938 | 201 | 2026-05-26 | Active GnuPG development continues |
| [openpgpjs/openpgpjs](https://github.com/openpgpjs/openpgpjs) | 5,948 | 821 | 2026-05-26 | JavaScript OpenPGP remains actively maintained |
| [barrydeen/wot-relay](https://github.com/barrydeen/wot-relay) | 85 | 28 | 2026-04-22 | Personal WoT relay; NIP-11 update merged Apr 22 |
| [nostr-wot/nostr-wot](https://github.com/nostr-wot/nostr-wot) | 6 | 2 | 2026-04-29 | Extension and SDK active; React hook fixes merged |
| [nostr-wot/nostr-wot-sdk](https://github.com/nostr-wot/nostr-wot-sdk) | 4 | — | 2026-04-29 | SDK monorepo with @nostr-wot/data 0.4.2, React #185 fix |
| [dtonon/chronicle](https://github.com/dtonon/chronicle) | 30 | 4 | 2026-04-30 | Negentropy sync support restricted to relay owner by default |
| [mailvelope/mailvelope](https://github.com/mailvelope/mailvelope) | 1,824 | 222 | 2026-05-21 | Active maintenance; stable browser extension ecosystem |

**Key observations:** The Nostr WoT ecosystem remains in the experimental-to-emerging band. GnuPG and OpenPGP.js show steady production maintenance. The PGPainless WoT module's last commits were September 2025 (Gradle 8.8 upgrade), suggesting the funded development phase may be concluding. The Brainstorm freedom-tech WoT relay project has not had commits since February 2026 (minor documentation edits). The overall ecosystem is functional and maintained but not rapidly growing in contributor count.

### Late-May 2026 GitHub Freshness Snapshot

|| Project | Stars | Last push | Notes ||
||---------|------:|-----------|-------|
|| [nostr-protocol/nips](https://github.com/nostr-protocol/nips) | 2,978 | 2026-05-31 | Protocol spec — active maintenance confirms ongoing NIP refinement |
|| [nbd-wtf/nostr-tools](https://github.com/nbd-wtf/nostr-tools) | 843 | 2026-05-19 | Dominant Rust SDK; 21-PR architecture overhaul in May 2026 |
|| [greenart7c3/Amber](https://github.com/greenart7c3/Amber) | 314 | 2026-05-30 | Highest-starred dedicated Nostr signer; NIP-07 + NIP-46 on Android |
|| [openpgpjs/openpgpjs](https://github.com/openpgpjs/openpgpjs) | 5,948 | 2026-05-26 | Steady production; 821 forks |
|| [barrydeen/wot-relay](https://github.com/barrydeen/wot-relay) | 85 | 2026-04-22 | +1 star since prior check; NIP-11 relay info update merged Apr 22 |
|| [dtonon/chronicle](https://github.com/dtonon/chronicle) | 32 | 2026-04-30 | +2 stars since prior check; personal relay with second-degree WoT filtering |
|| [pubky/pubky-core](https://github.com/pubky/pubky-core) | 77 | 2026-05-29 | Ed25519 + PKARR identity; active maintenance |
|| [FROSTR-ORG/igloo-server](https://github.com/FROSTR-ORG/igloo-server) | 8 | 2026-05-28 | Self-hostable Frostr server; NIP-46-compatible interface |
|| [FROSTR-ORG/bifrost](https://github.com/FROSTR-ORG/bifrost) | 10 | 2026-02-16 | TypeScript Frostr core; commit gap likely v2 spec phase |
|| [nostrcg/did-nostr](https://github.com/nostrcg/did-nostr) | 9 | 2026-01-11 | W3C CG draft; secp256k1 as DID identifier; no update/delete ops |
|| [forgesworn/bark](https://github.com/forgesworn/bark) | 0 | 2026-05-25 | NIP-07-to-NIP-46 bridge; any NIP-07 client works with any bunker |

**Key observations:** The Nostr WoT ecosystem is stable rather than rapidly expanding. Amber (314 stars) leads dedicated signer apps by a wide margin. The NIPs repo push on 2026-05-31 confirms the protocol is still actively refined. Bifrost's commit gap (Feb–May 2026) aligns with the Igloo v2 architectural direction — normal for library code between major versions. The bark bridge project (NIP-07 → NIP-46) is strategically important because it decouples NIP-46 adoption from every client implementing the protocol natively.

### NIP-85 Trust Scores: Cross-Client Convergence Accelerating

Amethyst, Primal, and Coracle have all shipped WoT trust score display in their UIs during Q1–Q2 2026, making trust metadata a user-visible product feature across independently developed Nostr clients. This convergence means the NIP-85 oracle provider model is becoming load-bearing infrastructure: clients that cannot compute the graph locally depend on signed assertions from provider keys. The implication for this library: WoT is no longer a developer-facing API — it is a user-visible layer that ordinary users now encounter in production clients.

### NIP-85 Deployment Summary (Early June 2026)

By early June 2026, NIP-85 trusted assertions have reached a notable milestone: implemented across independently developed clients (Amethyst, Primal, Coracle), served by multiple relay types (personal relays, public WoT relays, and dedicated scoring oracles), and generating signed events that ordinary users encounter as trust scores in their feeds. This cross-client, multi-provider deployment confirms that NIP-85 has transitioned from a draft proposal to load-bearing infrastructure in the Nostr WoT stack.

The architectural implication: clients that cannot crawl and compute the graph locally now depend on signed assertions from declared provider keys. The provider declaration mechanism (kind `10040`) is a critical trust anchor — its security and transparency properties directly determine whether the WoT remains user-sovereign or drifts toward centralized oracle dominance.

A technical critique from Vertex Lab (vertexlab.io) argues that NIP-85 fundamentally conflicts with WoT's discovery function: the protocol requires users to already know the pubkeys of providers they're looking for, which inverts the purpose of a trust graph — WoT should help discover unknown accounts, not just rank those already known. This articulates a real tension: provider-computed assertions help clients with existing graph context, but they do not help new users bootstrap or help existing users discover outside their bubble.

### wot.nostr.net — New Public WoT Relay (Bitvora, June 2026)

A new production public WoT relay appeared at `wss://wot.nostr.net`, built and maintained by Bitvora and powered by the Khatru relay framework. The relay implements web-of-trust filtering as a first-class feature: it serves content from accounts within a user's follow graph, reducing spam and noise compared to open public relays. Source code is available at [github.com/bitvora/wot-relay](https://github.com/bitvora/wot-relay). This is the first production public WoT relay from a known Nostr infrastructure provider, and serves as a counterpart to the self-hosted `wot-relay` (barrydeen) and the personal relay pattern established by Chronicle.

### NIP-26 Delegation Revocation: Issue #654 Still Open

GitHub issue #654 in the NIPs repository proposing a revocation mechanism for NIP-26 delegated keys remains open as of early June 2026. NIP-26 currently only supports time-bounded expiry, not revocation. When long-expiry NIP-26 delegations are combined with NIP-46 bunker signers for UX, a compromised delegate can operate until natural expiry — the proposed root-key-signed revocation certificates distributed to relays would close this window. This is a known gap in Nostr's delegation model that matters directly for WoT-adjacent custody: NIP-26 delegation is central to the NIP-46 remote signing flow, and without revocation, a compromised delegate is a live attack surface until expiry.

## June 18, 2026 Update — Relatr, wot-scoring maturation, Fourteenth Wave grants

### Relatr — New Personalized Trust Scoring Service (ContextVM)

The most significant addition to the Nostr WoT infrastructure this week is **Relatr** from [ContextVM](https://opensats.org/projects/contextvm) — an OpenSats-funded project that bridges Nostr with the Model Context Protocol (MCP). Relatr is a production-grade trust-scoring service designed for both human clients and AI agents:

- **Source:** [github.com/ContextVM/relatr](https://github.com/ContextVM/relatr) — 178 commits, 11 stars, last push 2026-05-26
- **License:** see repository; DuckDB-backed, Bun runtime, Docker Compose deploy
- **Live service:** [relatr.net](https://relatr.net) — search for Nostr profiles using the Relatr trust scoring system
- **Nostr identity:** [npub profile](https://nostr.com/nprofile1qqs82p5zxq7f7rw66av5rdy7mjw5dcldxp4eacen2vu2yx37gpx9lgcpzemhxue69uhhwmm5wgh8yetvv968ytnc09az7ylzepe) — published as kind 0 with `about: "A decentralized web of trust metric service for Nostr that computes personalized trust scores by combining social graph distances with profile validation metrics"`

What makes Relatr notable for the Nostr WoT layer:

1. **Personalized scoring from any source pubkey.** Unlike wot-scoring's global PageRank, Relatr lets the user pick a `DEFAULT_SOURCE_PUBKEY` and computes scores relative to that anchor.
2. **MCP server interface.** Relatr runs as an MCP server, so any AI agent that supports MCP can ask "who do I trust?" without writing Nostr-specific code. This is the first time the Nostr WoT has been exposed as a standard AI tool.
3. **Tunable parameters** in `.env`: `NUMBER_OF_HOPS`, `DECAY_FACTOR`, `CACHE_TTL_HOURS`, `TA_ENABLED`. Users can self-host with their own policy.
4. **Modular plugin system** with AI-assisted plugin authoring (`skills/relatr-elo-plugin-author`).

ContextVM is a separate grant wave from the projects below — it received funding in the **fifteenth wave** of OpenSats Nostr grants, while the projects in the next section received funding in the **fourteenth wave**.

### wot-scoring Maturation — Provider Composition + Community Detection

The [joelklabo/wot-scoring](https://github.com/joelklabo/wot-scoring) project (still 1 star, last push 2026-02-11, but algorithmically influential and powering wot.klabo.world) has accumulated the following capabilities that materially change what "WoT scoring" means in production:

- **Composite scoring across multiple NIP-85 providers** — clients can declare multiple trusted providers via kind `10040` and require N-of-M agreement rather than binding to a single provider's algorithm. This is a structural answer to the "oracle capture" risk identified in the broader WoT literature.
- **Label-propagation community detection** — algorithmic clustering of follow-graph components into sub-communities. Practical use cases include Sybil cluster detection (densely connected new accounts cluster together) and community-specific reputation scoring (treat members of the same community as more similar than members of different communities).
- **Mute-list integration via NIP-51 kind `10000`** — user's mute lists are read as community-moderation signals that down-rank authors the user has explicitly muted.
- **trustedrelays.xyz enrichment** — couples relay-level reputation with WoT scoring; a high-quality relay that is well-connected to the user's graph gets preference.

### OpenSats Fourteenth Wave — Three WoT-Adjacent Grants

The [Fourteenth Wave of Nostr Grants](https://opensats.org/blog/fourteenth-wave-of-nostr-grants) includes three projects that interact directly with the WoT layer:

1. **YakiHonne** — multi-platform Nostr client with WoT features built in. Repos at [YakiHonne/web-app](https://github.com/YakiHonne/web-app) (21 stars, 2026-05-17) and [YakiHonne/mobile-app](https://github.com/YakiHonne/mobile-app) (27 stars, 2026-05-14). Planned grant work: offline-first publishing, NsecBunker integration, Cashu and Nutzaps (NIP-60/NIP-61), relay-level paid feeds with cross-client compatibility.
2. **Quartz** — Kotlin Multiplatform Nostr library developed alongside [Amethyst](https://github.com/KotlinGeekDev/amethyst). Grant work includes a refactor for shared multiplatform modules and an iOS version of Amethyst. Quartz is the substrate that will carry Amethyst's WoT-aware UI to iOS users.
3. **Nostr Feedz + relay.pleb.one** — RSS+Nostr feed reader ([PlebOne/Nostr-Feedz](https://github.com/PlebOne/Nostr-Feedz)) with a companion WoT-gated relay at [relay.pleb.one](https://relay.pleb.one/) implementing the same invite-only-WoT-access pattern as [fiatjaf/pyramid](https://github.com/fiatjaf/pyramid) and [bitvora/wot-relay](https://github.com/bitvora/wot-relay).

The "WoT-gated relay access" pattern is now triply instantiated: pyramid (66 stars, June 17 push), bitvora/wot-relay (84 stars, wot.nostr.net production), and relay.pleb.one (PlebOne). This is enough independent implementation that it should be considered a stable architectural pattern rather than an experiment.

### Bitcoin 2026 Conference — WoT Reputation Layer on the Main Stage

David Strayhorn of [NosFabrica](https://nosfabrica.com) presented the Brainstorm WoT reputation layer at the Bitcoin 2026 Conference panel ["Protocol vs Platform: Nostr's Utility Beyond Social Media"](https://www.youtube.com/watch?v=wrlE0DMoTSc) on May 15, 2026. Chapter list confirms the WoT focus:

> 14:00 — NosFabrica's Brainstorm And The Web Of Trust Reputation Layer
> 17:00 — How AI Agents Are Integrating With Nostr Natively
> 22:30 — Nostr Marketplaces, Identity And The Open Internet Stack

This is the first Bitcoin-industry main-stage presentation of a Nostr WoT project. The audience reach (the Bitcoin Conference typically draws tens of thousands of attendees and broader livestream coverage) significantly raises the visibility of WoT as a Bitcoin/freedom-tech primitive.

### HAVEN v1.2.0 — Bitvora Personal Relay WoT Improvements

[Bitvora's HAVEN](https://github.com/bitvora/haven) ("High Availability Vault for Events on Nostr") released **v1.2.0** with WoT improvements: configurable depth levels, 24-hour auto-refresh of the user's WoT view, lockless optimization for higher throughput, multi-npub support with whitelist/blacklist, and a portable JSONL backup format. Coverage in [Nostr Compass #11](https://buttondown.com/nostrcompass/archive/nostr-compass-11). HAVEN sits beside Chronicle and wot-relay in the personal-relay-with-WoT stack.

### Updated GitHub Activity — June 18, 2026

| Project | Stars | Last push | Notes |
|---------|------:|-----------|-------|
| [ContextVM/relatr](https://github.com/ContextVM/relatr) | 11 | 2026-05-26 | New personalized WoT service; MCP server; 178 commits |
| [ContextVM/sdk](https://github.com/ContextVM/sdk) | 10 | 2026-06-17 | MCP-over-Nostr SDK; TypeScript + Rust |
| [ContextVM/wotrlay](https://github.com/ContextVM/wotrlay) | 2 | 2026-01-11 | WoT-aware relay (early) |
| [ContextVM/contextvm-docs](https://github.com/ContextVM/contextvm-docs) | 1 | 2026-06-16 | Docs repo |
| [YakiHonne/web-app](https://github.com/YakiHonne/web-app) | 21 | 2026-05-17 | Multi-platform Nostr client with WoT |
| [YakiHonne/mobile-app](https://github.com/YakiHonne/mobile-app) | 27 | 2026-05-14 | iOS/Android |
| [fiatjaf/pyramid](https://github.com/fiatjaf/pyramid) | 66 | 2026-06-17 | Invite-only WoT relay, active today |
| [nostr-protocol/nips](https://github.com/nostr-protocol/nips) | 2,997 | 2026-06-16 | NIP refinement continues |
| [nbd-wtf/nostr-tools](https://github.com/nbd-wtf/nostr-tools) | 846 | 2026-06-15 | Rust SDK |
| [greenart7c3/Amber](https://github.com/greenart7c3/Amber) | 321 | 2026-06-17 | Dominant Nostr signer |
| [hzrd149/blossom](https://github.com/hzrd149/blossom) | 281 | 2026-06-15 | Personal Blossom server |
| [bitvora/wot-relay](https://github.com/bitvora/wot-relay) | 84 | 2026-04-22 | Powers wot.nostr.net |
| [barrydeen/wot-relay](https://github.com/barrydeen/wot-relay) | 84 | 2026-04-22 | Original wot-relay |
| [dtonon/chronicle](https://github.com/dtonon/chronicle) | 35 | 2026-04-30 | Personal relay v0.5.0 |
| [joelklabo/wot-scoring](https://github.com/joelklabo/wot-scoring) | 1 | 2026-02-11 | PageRank + composite + community detection |
| [PlebOne/Nostr-Feedz](https://github.com/PlebOne/Nostr-Feedz) | 1 | 2026-01-28 | RSS+Nostr reader |
| [PlebOne/relay.pleb.one](https://github.com/PlebOne/relay.pleb.one) | 1 | 2026-02-10 | Invite-only WoT relay |
| [nostr-wot/nostr-wot](https://github.com/nostr-wot/nostr-wot) | 7 | 2026-06-02 | Toolkit +1 star since June 11 |
| [pgpainless/pgpainless-wot](https://github.com/pgpainless/pgpainless-wot) | 0 | 2026-04-28 | NLnet project; quiet |

**Key observations:**

1. **ContextVM stack is the new structural addition.** Relatr brings personalized scoring, MCP accessibility, and AI-agent integration in one project — a meaningful capability upgrade over wot-scoring's global PageRank and wot-relay's graph filtering.
2. **fiatjaf/pyramid remains the most-starred WoT-gated relay at 66 stars.** It is the architectural reference for the pattern; PlebOne's relay and Bitvora's wot.nostr.net both implement similar invite-only-WoT-access policies.
3. **Activity is split between protocol-layer and application-layer projects.** Protocol-layer projects (ContextVM SDK, nips, rust-nostr, Amber, fiatjaf/pyramid) are pushed within the last 48 hours; application-layer WoT projects (wot-scoring, wot-relay, chronicle, nostr-wot) are at April-May activity. The pattern suggests the protocol is moving faster than the WoT-specific applications.
4. **Brainstorm remains paused** (last non-doc commit Feb 2026). The Bitcoin 2026 talk by Strayhorn suggests future activity is plausible but not imminent.

## August 6, 2026 Update — Rust Oracle v1.0.0, Desktop WoT, AlgoRelay Production, Full-Stack Maturation

### nostr-wot Organization — Three-Tier Stack Complete

The [nostr-wot GitHub org](https://github.com/nostr-wot) has evolved from a single toolkit into a production three-tier architecture (12 followers, MIT-licensed):

```
┌─────────────────────────────────────────────────────────┐
│  Browser Extension (nostr-wot-extension, 8 stars)       │
│  NIP-07 signer + encrypted vault + Lightning wallet     │
│  Trust badges injected into Nostr sites                 │
└──────────────┬──────────────────────┬───────────────────┘
               │                      │
       ┌───────▼──────┐      ┌───────▼───────┐
       │  JS SDK       │      │  Rust Oracle   │
       │ (4 stars)     │      │ (5 stars)      │
       │ React hooks   │      │ Docker v1.0.0  │
       │ Ext-first     │      │ Full-graph BFS │
       └───────────────┘      └────────────────┘
```

**nostr-wot-oracle v1.0.0** ([GitHub](https://github.com/nostr-wot/nostr-wot-oracle)) — the structural upgrade. A Rust backend that continuously syncs Kind 3 follow lists from Nostr relays into an in-memory graph (backed by SQLite), then serves pairwise distance queries via REST API:

- **Performance**: <1ms cached, <50ms uncached, 10,000+ queries/second, bidirectional BFS with O(b^(d/2)) complexity, LRU cache (default 10K entries, 5-min TTL).
- **API**: `GET /distance?from=A&to=B` returns hop count, path count, bridging nodes. `POST /distance/batch` for multi-target queries. `GET /stats` for graph statistics.
- **Self-hosting**: `docker pull ghcr.io/nostr-wot/nostr-wot-oracle:v1.0.0`. Configurable relays, port, DB path, rate limit, cache via environment variables. Rust 1.75+ for source builds.
- **Public instance**: `wot-oracle.mappingbitcoin.com` (rate-limited 100 req/min/IP).

This is the first production-grade self-hostable Rust backend for Nostr WoT queries. The extension-first SDK pattern (use extension if available, fall back to oracle) means the WoT follows the user across clients — the core portability thesis from the HackerNoon launch article (Leon Acosta, February 2026) is now architecturally realized.

**nostr-wot-extension** (8 stars, pushed 2026-07-29) has evolved into a full Nostr identity provider:
- NIP-07 signer (sign events, encrypt NIP-04/NIP-44 messages on any client)
- AES-256-GCM encrypted vault with auto-lock and secure backup
- Multi-account with HD derivation, watch-only, NIP-46 remote signer
- Built-in Lightning wallet (NWC, LNbits, one-click setup)
- Color-coded trust badges injected into Nostr sites
- WebLN provider (`window.webln`)
- 6 languages (EN, ES, PT, DE, FR, IT)

**nostr-wot-sdk** (4 stars, pushed 2026-07-04): `npm install nostr-wot-sdk`. Extension-first design with React hooks (`WoTProvider`, `useWoT`). Falls back to oracle when extension unavailable.

**⚠️ UPDATE (August 13, 2026)**: The nostr-wot extension has **removed its WoT trust-graph layer entirely**. The README now states: "Earlier versions shipped an experimental Web-of-Trust trust-graph layer (oracles, follow-graph sync, trust scoring, a page-injected `window.nostr.wot` API, and trust badges). That subsystem has been removed." The extension is now a pure NIP-07 signer + WebLN wallet. Version 0.4.0 (August 11, 2026) pivoted to **post-quantum identity keys** (ML-KEM-1024 + ML-DSA-87 derived as siblings from the BIP-39 seed) with `kind:10203` attestations and post-quantum NIP-44/NIP-59 messaging. The `@nostr-wot/pq` npm package (v0.2.0) provides the reference wire-format implementation. The nostr-wot-oracle (Rust backend) has been dormant since June 4, 2026. NIP-85 providers (wot.klabo.world) and AlgoRelay are now the sole remaining WoT-filtering infrastructure. See [Web of Trust Thursday — August 13 2026 Weekly Update](/briefings/web-of-trust/2026-08-13/) for full analysis.

### nostr-relay-tray — Desktop WoT for Everyone (106 Stars)

[CodyTseng/nostr-relay-tray](https://github.com/CodyTseng/nostr-relay-tray) (106 stars, 6 forks, 112 commits) is the highest-starred personal relay with built-in WoT. Cross-platform desktop app (macOS, Windows, Linux) built on the extracted [nostr-relay](https://github.com/CodyTseng/nostr-relay) TypeScript framework. Zero-config start, full-text search, instant public access.

**WoT filtering architecture**: Two-layer event filter — Block Rules (reject) → Allow Rules / WoT / PoW (at least one must pass). The WoT layer accepts events from trusted users or relays. This is the `wot-relay`/`pyramid` pattern packaged for non-technical desktop users.

### AlgoRelay — Social-Graph-Ranked Feeds Across 4 Clients

[AlgoRelay](https://github.com/bitvora/algo-relay) (Bitvora, developer utxo) is now adopted by **four Nostr clients**: Jumble, Coracle, Nostur, and NoStrudel. The ranking algorithm lives at the relay level — users add AlgoRelay to their relay list and receive personalized feeds. A user dashboard allows weight tuning with signature validation. This is the first production evidence of social-graph-based content ranking working across multiple independent clients — the "content discovery via WoT" use case validated.

### OpenSats Relay Infrastructure Report — WoT as Established Pattern

[OpenSats' "Advancements in Nostr Relays"](https://opensats.org/blog/advancements-in-nostr-relays) documents WoT filtering as a production pattern across the relay ecosystem:

> "The relay has been up and running for four or five months now. I have zero spam issues since it is a web-of-trust relay, and I get to keep it free for everyone."

The report covers ten funded projects. WoT-relevant: nostr-relay framework (CodyTseng, extracted from nostr-relay-nestjs), nostr-relay-tray (desktop WoT), relay.tools (read-level access control for strfry via auth proxy), nostr.watch (NIP-66 decentralized monitoring), and AlgoRelay (social-graph feeds). HAVEN (Bitvora) continues with WoT improvements from v1.2.0.

### OpenSats Seventeenth Wave — WoT Expertise Spreading

[Seventeenth Wave](https://opensats.org/blog/seventeenth-wave-of-nostr-grants) (May 19, 2026): 44Billion (app launcher), NosCall (encrypted calls), Routstr (AI inference via Nostr), Wisp (Android client by **Barry Deen** — creator of wot-relay). Zapstore renewal. Barry Deen's grant for Wisp means the wot-relay creator is now funded on a Nostr client — WoT expertise is propagating into the broader client ecosystem.

### RUSTSEC-2026-0225 — nostr Crate Credential Leak

[RUSTSEC-2026-0225](https://rustsec.org/advisories/RUSTSEC-2026-0225.html) (August 2, 2026): `nostr` crate (>=0.44.7) derived `Debug` on NIP-46/NIP-60 types containing credentials (connection secrets, private keys, Cashu proofs). Fixed with custom redacting `Debug` implementations. WoT relevance: NIP-46 bunker signing is central to the identity custody model that WoT infrastructure depends on — credential leaks at the signer layer undermine trust above.

### NIPs Repo at 3.1K Stars

[nostr-protocol/nips](https://github.com/nostr-protocol/nips) at **3,100 stars** and **786 forks** (up from 2,978 on May 31, 2,997 on June 16). NIP-85 kinds (30382–30385) confirmed in canonical listing. NIP-72 (Moderated Communities) deprecated in favor of NIP-29 (Relay-based Communities), which composes with WoT-gated relay access.

### Updated GitHub Activity — August 6, 2026

| Project | Stars | Last push | Notes |
|---------|------:|-----------|-------|
| [nostr-wot-extension](https://github.com/nostr-wot/nostr-wot-extension) | 8 | 2026-07-29 | Full identity provider; +2 stars since June |
| [nostr-wot-oracle](https://github.com/nostr-wot/nostr-wot-oracle) | 5 | 2026-06-04 | **New**: Rust v1.0.0; Docker; bidirectional BFS |
| [nostr-wot](https://github.com/nostr-wot/nostr-wot) (toolkit) | 6 | 2026-07-04 | Active; +0 since June |
| [nostr-wot-sdk](https://github.com/nostr-wot/nostr-wot-sdk) | 4 | 2026-07-04 | npm package; React hooks |
| [CodyTseng/nostr-relay-tray](https://github.com/CodyTseng/nostr-relay-tray) | **106** | active | **New entry**: Desktop WoT relay; highest-starred WoT personal relay |
| [bitvora/algo-relay](https://github.com/bitvora/algo-relay) | — | active | **New entry**: Social-graph feeds; 4-client adoption |
| [nostr-protocol/nips](https://github.com/nostr-protocol/nips) | **3,100** | active | +103 stars since May 31; 786 forks |
| [barrydeen/wot-relay](https://github.com/barrydeen/wot-relay) | ~85 | 2026-04-22 | Stable |
| [dtonon/chronicle](https://github.com/dtonon/chronicle) | ~35 | 2026-04-30 | Stable |
| [fiatjaf/pyramid](https://github.com/fiatjaf/pyramid) | ~66 | 2026-06-17 | Reference WoT-gated relay |
| [bitvora/wot-relay](https://github.com/bitvora/wot-relay) | ~84 | 2026-04-22 | Powers wot.nostr.net |
| [ContextVM/relatr](https://github.com/ContextVM/relatr) | 11 | 2026-05-26 | MCP WoT server |
| [joelklabo/wot-scoring](https://github.com/joelklabo/wot-scoring) | 2 | 2026-02-11 | PageRank oracle; +1 star |

**Key observations**:
1. **nostr-relay-tray (106 stars) is the breakout project.** It brings WoT filtering to the desktop with a GUI — the accessibility layer the WoT ecosystem needed.
2. **The nostr-wot org is architecturally complete but adoption is still modest** (extension 8 stars, oracle 5 stars). The infrastructure is production-quality; the user base has not yet caught up.
3. **AlgoRelay's 4-client adoption validates social-graph content ranking** in production across independent implementations.
4. **NIPs repo growth (+103 stars in 9 weeks)** confirms active protocol-level interest, which feeds WoT development.

## August 20, 2026 Update — The Shadow Protocol Phase; a WoT Provider Dies

Full detail in [Web of Trust Thursday — August 20 2026 Weekly Update](/briefings/web-of-trust/2026-08-20/). Key developments:

### Post-quantum Nostr, specified but unratified

The nostr-wot org published its PQ stack as **four NIP draft specs** (Aug 17) in the extension repo — key derivation, `kind:10203` attestation, hybrid NIP-44 envelope, `window.nostr.nip44.schemes` capability marker — explicitly *not* submitted upstream, "in enough detail that a second implementation can interoperate without reading our source." **Obelisk** (29★, daily pushes) is the 1.5th implementation (SDK-consuming). Extension shipped **v0.5.0–v0.5.2** (Aug 15–19): PQ key *import* for non-derivable accounts (`origin: independent` provenance tags, round-trip key validation), seed-handling audit fixes (mnemonic out of session storage; vault KDF corrected to 600K PBKDF2-SHA-256), a full consent-model overhaul (zero host permissions, decaying "Not now"), and an AMO-forced Node 22+ toolchain. The SDK reached **v1.0.1** with PQ sealing moved into the signer layer and seal/rumor verification added to `unwrapGiftWrap`.

### The upstream veto is now explicit

nostr-tools PR #541 (PQ keys) was **closed unmerged** after fiatjaf: "I am not thinking about it and I won't think about it until it happens (it will not)... work on a new protocol that is similar to Nostr but does everything post-quantum instead." NIPs PR #2434 (same design, +517 lines, test vectors against NIP-06 fixtures) sits open with no review. nostr-wot's response is the cypherpunk fallback: spec it, ship it, invite forks — "the risk asymmetry is relevant to me" (leonacostaok).

### Adoption measured — the flat line

Direct relay queries (Aug 20): **24 unique pubkeys** have ever published `kind:10203` (relay.damus.io 21, nos.lol 22, union 24). By first-seen date: 19 on Aug 10 (launch), 4 on Aug 11, **1 on Aug 18, zero otherwise**. Average attestation 12,226 B. `@nostr-wot/pq` at 282 downloads/week. The launch cohort *is* the user base; the opt-in essay (rewritten 3× in one day, final title "Post-quantum direct messages should not be opt-in") locates the cause in identity design: the npub has no algorithm/version/capability field — NIP-44 payloads carry a version byte, the identity beneath them carries nothing — so every key migration is structurally opt-in.

### wot.klabo.world is gone

The PageRank NIP-85 provider lost its DNS record (NXDOMAIN Aug 20; apex klabo.world resolves). wot-scoring repo dormant since Feb 11. This vault previously listed it as live — corrected above. The WoT-filtering load now rests on **self-hostable patterns** (wot-relay, Chronicle, HAVEN, nostr-relay-tray at 108★, pyramid) and Bitvora's operated relays/AlgoRelay. Every WoT death this year (Brainstorm paused, oracle dormant June, klabo dead August) has been on the *hosted* side — the surviving pattern is exactly the self-hostable one. Nostr.Band unreachable from the research vantage point; flagged for re-verification.

### GitHub snapshot — August 20, 2026

| Project | Stars | Last push | Notes |
|---------|------:|-----------|-------|
| [nostr-wot-extension](https://github.com/nostr-wot/nostr-wot-extension) | 8 | 2026-08-19 | v0.5.2; 4 PQ NIP drafts; PQ import; consent overhaul |
| [nostr-wot](https://github.com/nostr-wot/nostr-wot) (toolkit) | 7 | 2026-08-19 | Opt-in essay (3 rewrites); false-claim fix |
| [nostr-wot-sdk](https://github.com/nostr-wot/nostr-wot-sdk) | 5 | 2026-08-17 | v1.0.1; PQ in signer layer; first external PR |
| [nostr-wot-oracle](https://github.com/nostr-wot/nostr-wot-oracle) | 5 | 2026-06-04 | Dormant 11 weeks |
| [obelisk-app/obelisk](https://github.com/obelisk-app/obelisk) | 29 | 2026-08-19 | 2nd PQ impl; WoT-filtered chat/voice; PQ shield UI |
| [nostr-protocol/nips](https://github.com/nostr-protocol/nips) | 3,080 | 2026-08-19 | PR #2434 stalled; no PQ engagement |
| [nbd-wtf/nostr-tools](https://github.com/nbd-wtf/nostr-tools) | — | PQ PR #541 closed unmerged | Aug 10 |
| [CodyTseng/nostr-relay-tray](https://github.com/CodyTseng/nostr-relay-tray) | 108 | 2026-02-02 | Stable; desktop WoT relay |
| [gpg/gnupg](https://github.com/gpg/gnupg) | 967 | 2026-08-18 | One commit; TOFU watch continues |
| [sequoia-pgp (GitLab)](https://gitlab.com/sequoia-pgp/sequoia) | 473 | 2026-08-17 | openpgp 2.4.1; direct-key trust sigs; PQ pending |

**Key observations**:
1. **PQ Nostr is a shadow protocol**: fully specified, 1.5× implemented, honestly measured (24 pubkeys), ratified by no one. Upstream veto stable across three venues.
2. **The crypto-agility essay is the reusable insight**: an identity system that cannot say "this identity uses algorithm X" makes every migration opt-in and therefore incomplete. Same root cause as DNSSEC/OpenPGP v4→v6 migration pains.
3. **The WoT bifurcation hardens**: hosted scorers keep dying; self-hostable relay patterns carry the load. Build on what you can run yourself.
4. **Consent UX is now extension review criteria**: v0.5.1's permission model and v0.5.2's AMO Node-20 rejection show stores shaping not just security but CI toolchains.

## August 27, 2026 Update — Maintenance Mode; the Org Pivots to an Autonomous Newsroom

Re-measurement week. Every adoption indicator of the post-quantum stack went flat or down, the extension has been frozen since Aug 19, and the organization's engineering velocity moved to a new product: a daily AI-operated news publication. Full detail in [Web of Trust Thursday — August 27 2026 Weekly Update](/briefings/web-of-trust/2026-08-27/).

**Adoption plateau (verified Aug 27, direct relay queries).** nos.lol carries 22 unique `kind:10203` pubkeys — identical to Aug 20, identical first-seen dates (Aug 10: 17, Aug 11: 4, Aug 18: 1 on that relay). Zero new publishers in the nine days since Aug 18. relay.damus.io now rejects unauthenticated WebSocket connections, blocking the two-relay union count; relay.primal.net and nostr.wine carry none. npm downloads collapsed to ambient: `@nostr-wot/pq` 282→**26**/week, `nostr-wot-sdk` 235→**59**/week; neither package has shipped since Aug 16. The PQ stack is a completed, documented, deployed experiment in maintenance mode at ~24 identities — awaiting an environmental change (client default-on or NIP ratification) that no further engineering by the org can cause.

**The newsroom pivot.** The main repo ([nostr-wot/nostr-wot](https://github.com/nostr-wot/nostr-wot)) took ~30 commits Aug 21–26 building `nostr-wot.com/news`: per-locale RSS/JSON feeds, Google News sitemap, a six-month archive retrofill (followed by "correct four factual errors found in review of the retrofill"), and — the governance layer worth archiving — `docs/newsroom/playbook.md`, a run log, and a `content/news/PAUSE` kill switch. The playbook mandates **GitHub-API-only sourcing** ("Do not search the web for news, and do not treat any fetched prose page as a source"), a rule created after a fabrication incident during the retrofill: a fetched "newsletter" page returned content describing a private repository "in terms lifted from internal notes, for a project with no public footprint." Run-log semantics distinguish `published | skipped | paused | failed`; the Aug 26 `skipped` line names the considered-and-rejected stories. This is the strongest public specimen of autonomously operated publishing with reviewable editorial governance this library has recorded — directly relevant as a Daemon-network design pattern (structured-API-only sourcing, log-every-run-including-no-ops, kill-switch-as-file, machine-generated disclosure).

**Infrastructure.** Hosted side: nostr.band unreachable from a **second vantage point** (second consecutive week) — treated as operationally dead; wot.klabo.world still NXDOMAIN; oracle dormant 12 weeks. Self-hostable side: **fiatjaf/pyramid pushed its first commit since June** ("Add restrited prefix when not a member", Aug 21; 73★), and bitvora's wot.nostr.net answers HTTP 200. The 2026 pattern — hosted WoT dies, self-hostable WoT persists — holds and strengthened.

**Upstream.** NIPs PR #2434 untouched for 16 days (sole comment remains fiatjaf's rejection link). NIPs merged NIP-A3 payto (RFC-8905 payment targets), NIP-30 emoji on kind 1111, and NIP-22's kind-1 reply permission — nothing PQ. Obelisk: two maintenance commits (signer-latency fix, pm2 ops), still SDK-consuming — the "second independent implementation" threshold remains unmet.

## Primary sources

- [NIP-85 — Trusted Assertions](https://nips.nostr.com/85)
- [NIP-02 — Follow List](https://github.com/nostr-protocol/nips/blob/master/02.md)
- [NIP-51 — Lists](https://nips.nostr.com/51)
- [NIP-56 — Reporting](https://nips.nostr.com/56)
- [Nostr Protocol NIPs repository](https://github.com/nostr-protocol/nips)
- [nostr-wot/nostr-wot](https://github.com/nostr-wot/nostr-wot)
- [nostr-wot/nostr-wot-sdk](https://github.com/nostr-wot/nostr-wot-sdk)
- [nostr-wot/nostr-wot-extension](https://github.com/nostr-wot/nostr-wot-extension)
- [barrydeen/wot-relay](https://github.com/barrydeen/wot-relay)
- [dtonon/chronicle](https://github.com/dtonon/chronicle)
- [joelklabo/wot-scoring](https://github.com/joelklabo/wot-scoring)
- [CodyTseng/nostr-relay-plugin](https://github.com/CodyTseng/nostr-relay-plugin)
- [Nostr Compass — Web of Trust](https://nostrcompass.org/en/topics/web-of-trust/)
- [RFC 9591 — FROST Protocol](https://datatracker.ietf.org/doc/rfc9591/) — IRTF stable threshold Schnorr spec
- [nostr-protocol/nips#654](https://github.com/nostr-protocol/nips/issues/654) — NIP-26 delegation revocation proposal
- [DCoSL](https://github.com/wds4/DCoSL)
- [Noswot](https://codeberg.org/weex/noswot)
- [An Empirical Analysis of the Nostr Social Network](https://arxiv.org/html/2402.05709v2)
- [FROST paper](https://eprint.iacr.org/2020/852) — Komlo and Goldberg, Flexible Round-Optimized Schnorr Threshold Signatures
- [FROST NIST MPTS 2026 preview writeup](https://csrc.nist.gov/csrc/media/Projects/threshold-cryptography/documents/TCall-1/FROST-PW01.pdf) — FROST Team, version 0.1, March 2026
- [Hermine: Lattice-based FROST-like Threshold Signatures](https://eprint.iacr.org/2026/419) — eprint 2026/419
- [Hermine project website](https://hermine-th.org)
- [ContextVM project page](https://opensats.org/projects/contextvm) — MCP-over-Nostr protocol
- [ContextVM/relatr](https://github.com/ContextVM/relatr) — personalized trust scoring service (live at relatr.net)
- [ContextVM/wotrlay](https://github.com/ContextVM/wotrlay) — WoT-aware relay
- [ContextVM/sdk](https://github.com/ContextVM/sdk) — TypeScript + Rust MCP-over-Nostr SDKs
- [fiatjaf/pyramid](https://github.com/fiatjaf/pyramid) — invite-only WoT-gated relay (66 stars, June 17 push)
- [bitvora/haven](https://github.com/bitvora/haven) — personal relay, v1.2.0 with WoT improvements
- [OpenSats Fourteenth Wave of Nostr Grants](https://opensats.org/blog/fourteenth-wave-of-nostr-grants) — YakiHonne, Quartz, Nostr Feedz
- [YakiHonne/web-app](https://github.com/YakiHonne/web-app) / [mobile-app](https://github.com/YakiHonne/mobile-app) — multi-platform Nostr client
- [PlebOne/Nostr-Feedz](https://github.com/PlebOne/Nostr-Feedz) and [PlebOne/relay.pleb.one](https://github.com/PlebOne/relay.pleb.one) — RSS+Nostr with WoT-gated relay
- [Bitcoin 2026 Protocol vs Platform panel](https://www.youtube.com/watch?v=wrlE0DMoTSc) — Brainstorm WoT reputation presentation
- [nostr-wot/nostr-wot-oracle](https://github.com/nostr-wot/nostr-wot-oracle) — Rust follow-graph indexer, v1.0.0 Docker, bidirectional BFS
- [nostr-wot.com/oracle](https://nostr-wot.com/oracle) — Oracle API docs and self-hosting guide
- [CodyTseng/nostr-relay-tray](https://github.com/CodyTseng/nostr-relay-tray) — Desktop personal relay with WoT filtering (106 stars)
- [bitvora/algo-relay](https://github.com/bitvora/algo-relay) — Social-graph-ranked feed relay; 4-client adoption
- [OpenSats — Advancements in Nostr Relays](https://opensats.org/blog/advancements-in-nostr-relays) — Relay ecosystem report documenting WoT as production pattern
- [OpenSats — Seventeenth Wave](https://opensats.org/blog/seventeenth-wave-of-nostr-grants) — Wisp (Barry Deen/wot-relay creator)
- [RUSTSEC-2026-0225](https://rustsec.org/advisories/RUSTSEC-2026-0225.html) — nostr crate Debug credential leak (NIP-46, NIP-60)
- [nostr-wot-extension NIP drafts](https://github.com/nostr-wot/nostr-wot-extension/tree/main/nips) — the four PQ specs (derivation, kind:10203, envelope, capability marker), Aug 2026
- [nostr-tools PR #541](https://github.com/nbd-wtf/nostr-tools/pull/541) — PQ keys PR closed unmerged; fiatjaf's response
- [NIPs PR #2434](https://github.com/nostr-protocol/nips/pull/2434) — NIP-XX: Post-Quantum Identity Keys (stalled)
- [obelisk-app/obelisk](https://github.com/obelisk-app/obelisk) — Nostr chat/voice with WoT filtering; second PQ implementation
- [nostr-wot.com — opt-in essay](https://nostr-wot.com/blog/opt-in-quantum-resistant-direct-messages) — "Post-quantum direct messages should not be opt-in" (Aug 2026)
- [obelisk dm-metadata-privacy notes](https://github.com/obelisk-app/obelisk/blob/main/docs/dm-metadata-privacy.md) — what PQ does not fix (NIP-17 metadata)
