---
title: "Webs of Trust: The Long Survey"
slug: web-of-trust-survey
type: reference
pillars: ["identity"]
description: "A long survey of webs of trust: how decentralized systems decide which keys and people to trust, from PGP to Nostr, with algorithms and attacks."
dek: "A Web of Trust (WoT) is a decentralized answer to the question: \"which public keys, accounts, relays, merchants, or claims should I treat as credible?\" Instead of a certificate authority, government registry, platform moderation team, or KYC provider deciding for everyone, each participant starts with local trust anchors and extends outward through signed attestations, follow relationships, endorsements, mutes, reports, zaps, or other graph edges."
updated: 2026-10-25
created: 2026-04-16
origin: vault
source: "02-Cryptography/Overview - Web of Trust.md"
aliases: ["WoT", "Trust Graph", "Reputation Network", "Social Graph Trust"]
tags: ["web-of-trust", "wot", "trust-graph", "reputation", "sybil-resistance", "nostr", "openpgp", "gpg", "identity"]
---

## Summary

A Web of Trust (WoT) is a decentralized answer to the question: **"which public keys, accounts, relays, merchants, or claims should I treat as credible?"** Instead of a certificate authority, government registry, platform moderation team, or KYC provider deciding for everyone, each participant starts with local trust anchors and extends outward through signed attestations, follow relationships, endorsements, mutes, reports, zaps, or other graph edges.

The model appears in two important freedom-tech lineages:

1. **OpenPGP / GPG WoT** — key certification: people sign each other's OpenPGP certificates after verifying identity. GnuPG can decide whether a key is valid by walking paths through locally trusted introducers.
2. **Nostr WoT** — social-graph trust: clients, relays, and oracle services use follows, mute lists, trusted assertions, and graph distance to rank or filter pubkeys and events without a platform-wide moderation authority.

The practical point is not "trust everyone your friends trust." The practical point is **user-chosen trust computation**: a client can ask, "is this pubkey within 2 hops of my graph?", "did a provider I chose publish a NIP-85 rank for this event?", or "does this OpenPGP certificate have a path to one of my own trusted keys?" That makes WoT a composable primitive for [Overview - Identity & Pseudonymity](/kb/identity-and-pseudonymity/), decentralized social spam filtering, marketplace reputation, software maintainer verification, and community moderation.

## Mental model

```text
Local trust anchor(s)      Edges / attestations           Target
┌───────────────┐          ┌───────────────┐          ┌───────────────┐
│ my key / seed │ ───────► │ trusted peer  │ ───────► │ unknown pubkey│
└───────────────┘          └───────────────┘          └───────────────┘
       │                          │                           │
       │                          ├─ signed OpenPGP cert       │
       │                          ├─ follows / mute lists      │
       │                          ├─ NIP-85 assertion          │
       │                          └─ zap / report / review     │
       ▼
Policy: path length, edge type, score threshold, freshness, context
```

A WoT system needs four layers:

| Layer | Question | OpenPGP example | Nostr example |
|---|---|---|---|
| Identity object | What is the node? | OpenPGP certificate / fingerprint | secp256k1 public key / npub |
| Trust edge | What does an edge mean? | Certification signature; ownertrust | Follow list, mute list, report, NIP-85 rank |
| Discovery | Where do I get graph data? | WKD, keys.openpgp.org, key files | Relays, indexers, graph crawlers, WoT oracle |
| Policy | How do I decide? | Full vs marginal introducers | hop distance, PageRank, community-specific algorithm |

A good WoT design keeps these layers separate. A follow is not always a strong endorsement. A key signature may prove identity but not moral trust. A global score is convenient but drifts toward centralization. A per-user graph preserves autonomy but costs more to compute.

## Historical context

### PGP and the original Web of Trust (1991–1998)

Phil Zimmermann released PGP in 1991 with a trust model deliberately unlike X.509 certificate authorities. In X.509, a small set of root CAs can vouch for names. In PGP, users exchange fingerprints, sign each other's keys, and choose their own trusted introducers.

OpenPGP standardized the message and certificate formats. The modern standard is [RFC 9580](https://www.rfc-editor.org/rfc/rfc9580.html), published in July 2024, which obsoletes RFC 4880 / RFC 5581 / RFC 6637 and updates OpenPGP with v6 keys, mandatory Ed25519/X25519 support, AEAD containers, Argon2 S2K, and stronger algorithm guidance. RFC 9580 is mostly a wire-format and interoperability document; the local trust policy remains an implementation and user-experience problem.

The classic PGP WoT grew through:

- **Key-signing parties** — people verified passports / fingerprints and signed keys.
- **Keyservers** — public distribution of certificates and third-party signatures.
- **Local ownertrust** — the user's own decision that a key is a full, marginal, or untrusted introducer.
- **Certification paths** — validity derived from enough trusted signatures.

### Keyserver collapse and abuse resistance (2010s)

The old SKS keyserver pool was append-only and aggressively synchronized. That made distribution robust, but it also made abuse permanent: anyone could attach huge numbers of third-party signatures or offensive identity packets to someone else's certificate. The poisoning attacks against prominent OpenPGP certificates turned the historical WoT/keyserver model into a warning: decentralized append-only data structures need consent and garbage-collection mechanisms.

Modern key discovery shifted toward:

- **Web Key Directory (WKD)** — fetch a key from the domain associated with an email address.
- **keys.openpgp.org** — a centralized but abuse-resistant keyserver that verifies email addresses and does **not** distribute third-party certifications by default.
- **First-party attested third-party certifications** — a compromise where third-party certifications can be distributed only when the certificate holder explicitly attests to them.
- **Keyoxide / Ariadne proofs** — self-published proofs linking an OpenPGP key or profile to accounts across services.

The lesson for newer WoT systems is clear: let people publish graph edges, but do not let arbitrary third parties permanently mutate someone else's identity object.

### Nostr and graph-native trust (2020s)

Nostr made public keys first-class identities. A Nostr user is a secp256k1 keypair; relays are dumb event stores; clients choose how to interpret events. That creates both the problem and the opportunity for WoT:

- Problem: there is no platform-wide account verification, spam filter, moderation team, or account recovery desk.
- Opportunity: the protocol already produces machine-readable trust signals — follow lists, mute lists, relay lists, reports, communities, zaps, and app-specific reputation events.

Nostr WoT is therefore less about signing identity documents and more about **local graph computation**. If a pubkey is followed by people you follow, appears on curated lists you trust, receives useful zaps from your graph, and is not widely muted or reported by your community, a client can rank it higher. If an account is far outside your graph and posts low-cost spam, a relay or client can downrank or reject it.

### Trusted assertions (NIP-85)

A recent Nostr development is [NIP-85 Trusted Assertions](https://nips.nostr.com/85), a draft optional standard for publishing computed metrics as signed replaceable events. It exists because many WoT calculations require large event histories or expensive graph processing that mobile clients cannot do locally.

NIP-85 defines assertion kinds:

| Subject | Event kind | Examples |
|---|---:|---|
| User / pubkey | `30382` | rank, followers, post count, reports, zap amount |
| Regular event | `30383` | event rank, reactions, zaps, quote count |
| Addressable event | `30384` | rank and engagement for replaceable events |
| External identifier | `30385` | rank for NIP-73 books, locations, websites, hashtags |

Users declare trusted service providers with kind `10040`. That is an important decentralization point: a NIP-85 score is not universally authoritative; it is a signed output from a provider whose methodology and key the user chooses to trust.

## Major implementations and active projects

### Nostr Web of Trust toolkit

- **Primary source:** [github.com/nostr-wot/nostr-wot](https://github.com/nostr-wot/nostr-wot)
- **Type:** Nostr graph toolkit, SDK, extension, oracle API
- **Status:** experimental / active; MIT licensed; GitHub API on 2026-04-30 showed 6 stars, 2 forks, not archived, last pushed 2026-04-29.

The Nostr WoT project frames the problem directly: Nostr has no central authority for spam filtering or identity verification, so applications need open infrastructure for trust-based filtering. Its components include:

- A browser extension exposing a `window.nostr.wot` API.
- A JavaScript / TypeScript SDK for app integration.
- A Rust-backed oracle that maintains a Nostr follow graph and answers distance / trust queries over a REST API.
- A self-hosting model: run your own oracle, fork the extension, or build a community-specific scoring stack.

The canonical use case is simple: a client wants to know how close another pubkey is to the user's graph. First-degree follows are near; friends-of-friends are still plausible; accounts several hops away are lower priority unless other signals compensate.

### Cross-client WoT adoption (Q1 2026)

A notable development from early 2026: multiple independent Nostr clients have begun implementing and displaying trust scores. According to Q1 2026 ecosystem reports, Amethyst, Primal, and Coracle are all showing WoT-based trust scores in their UI. This is the cross-client convergence that the nostr-wot extension approach was designed to enable — the WoT infrastructure layer is becoming visible to ordinary users without requiring a specific client.

The practical implication: WoT is transitioning from a developer-facing library feature to a user-visible product feature. This creates both better spam filtering for users and new design questions about how to present trust without making it feel like a surveillance score.

### Nostr WoT browser extension

- **Primary source:** [github.com/nostr-wot/nostr-wot-extension](https://github.com/nostr-wot/nostr-wot-extension), [nostr-wot.com](https://nostr-wot.com/)
- **Type:** browser extension combining NIP-07 signing, Lightning wallet / zaps, and trust scoring
- **Status:** experimental / active; MIT licensed; GitHub API on 2026-04-30 showed 6 stars, 2 forks, not archived, last pushed 2026-04-26.

The extension approach is strategically interesting because it avoids waiting for every Nostr client to implement its own graph engine. The extension can act as an identity provider and a trust oracle at the browser boundary. Any web client that can call the extension can ask trust questions.

Trade-off: browser extensions are a high-value key custody surface. Combining identity signing, Lightning wallet functions, and reputation in one extension is convenient, but it concentrates risk. For serious identity, pair this with [Remote Signing](/kb/remote-signing/) / NIP-46-style signing or hardware-backed key handling where possible.

### wot-relay

- **Primary source:** [github.com/barrydeen/wot-relay](https://github.com/barrydeen/wot-relay) (also surfaced as bitvora/wot-relay in search due to repository ownership naming)
- **Type:** Nostr relay that archives notes from a user's web of trust
- **Status:** active; GitHub API on 2026-04-30 showed 83 stars, 27 forks, not archived, last pushed 2026-04-22.

A WoT relay moves trust filtering from the client into relay policy. Instead of archiving the entire global firehose, it stores content produced by people in the configured graph — for example, accounts followed by the user and accounts followed by those accounts. This reduces spam and storage pressure but makes the relay's graph policy critical infrastructure.

### Chronicle personal relay

- **Primary source:** [github.com/dtonon/chronicle](https://github.com/dtonon/chronicle)
- **Type:** Nostr personal relay with Outbox-model support, Blossom media handling, and WoT spam protection
- **Status:** active; Chronicle v0.5.0 released with quick summary: Chronicle is a personal relay Nostr, built on the Khatru framework, that stores complete conversations where the owner participated. Events from others are accepted only when the conversation is relevant to the owner and the author is within the owner's graph up to the second degree, unless proof-of-work fallback is enabled. GitHub API on 2026-05-07 showed 30 stars, 4 forks, not archived, last pushed 2026-04-30.

Chronicle v0.5.0 released in May 2026 — a significant update to the personal relay that implements WoT as an operational relay policy rather than only a client-ranking algorithm. It stores conversations in which the owner participated, accepts external events only when relevant to those conversations and the author is within the owner's graph (second degree), with optional PoW fallback. Includes built-in Blossom media server and optional backup for other authors' blobs. See [Nostr Web of Trust](/kb/nostr-web-of-trust/) for the deeper Nostr-specific treatment.

### Brainstorm WoT relay (Pretty-Good-Freedom-Tech)

- **Primary source:** [github.com/Pretty-Good-Freedom-Tech/brainstorm](https://github.com/Pretty-Good-Freedom-Tech/brainstorm)
- **Type:** Personalized WoT relay that generates its own nsec, signs NIP-85 kind 30382 events, and filters content through the user's social graph
- **Status:** active; MIT license; notable as a freedom-tech-specific project in the Nostr WoT space

Brainstorm is a newer entry in the self-hostable WoT relay pattern. At installation it generates a new nsec for the relay (stored in config), uses that to sign NIP-85 kind 30382 events, and publishes kind 10040 to declare the relay pubkey to clients. The relay filters spam by social graph and auto-publishes kind 30382 events every N hours. Notable because it comes from the Pretty-Good-Freedom-Tech organization, explicitly oriented toward freedom-tech values. The project demonstrates the growing pattern of WoT-as-relay-policy: the relay enforces trust filtering at storage time rather than relying on clients to do it.

### wot-scoring

- **Primary source:** [github.com/joelklabo/wot-scoring](https://github.com/joelklabo/wot-scoring)
- **Type:** PageRank-based Nostr trust scoring; publishes NIP-85 kinds `30382`–`30385`
- **Status:** experimental / active; MIT licensed; GitHub API on 2026-04-30 showed 1 star, not archived, last pushed 2026-02-11.

This project matters less because of adoption and more because it demonstrates the direction of travel: graph crawlers compute trust / rank, then publish signed NIP-85 assertions that clients can choose to consume. The architecture separates computation from UI while retaining signed provenance for the score.

### nostr-relay-plugin WoT Guard

- **Primary source:** [github.com/CodyTseng/nostr-relay-plugin](https://github.com/CodyTseng/nostr-relay-plugin)
- **Type:** plugin monorepo for `nostr-relay`; includes WoT Guard and PoW Guard concepts
- **Status:** small but active; MIT licensed; not archived; last pushed 2026-04-15.

Relay-side guards are the Nostr equivalent of email MTA policy: they can reject or downrank messages before clients ever see them. The risk is policy opacity. A good WoT relay should publish its criteria, permit user override, and avoid becoming an unaccountable blocklist provider.

### nostr-wot oracle (global follow-graph indexer)

- **Primary source:** [github.com/nostr-wot/nostr-wot-oracle](https://github.com/nostr-wot/nostr-wot-oracle)
- **Type:** global follow-graph indexer that answers pairwise distance queries
- **Status:** active; part of the nostr-wot GitHub org

The nostr-wot oracle is the computation backend for the nostr-wot toolkit. It maintains a global Nostr follow graph and answers distance queries — given two npubs, it returns hop count, path count, and bridging nodes between them. This is the core primitive for the oracle pattern: instead of every client crawling and computing the graph, clients query a shared indexer that has already done the work. The oracle publishes signed results, and users can self-host or choose between oracle providers, preserving the "choose your trust anchor" property.

### PGPainless WoT implementation (NLnet-funded)

- **Primary source:** [github.com/pgpainless/pgpainless-wot](https://github.com/pgpainless/pgpainless-wot), [NLnet project page](https://nlnet.nl/project/PGPainless/)
- **Type:** OpenPGP WoT implementation in Kotlin/Java
- **Status:** active; funded by NGI Assure through NLnet; based on Sequoia-PGP's WoT specification

PGPainless is adding WoT support based on Sequoia-PGP's published WoT specification. The NLnet project description states the goal: "make the Web of Trust more interoperable and accessible to client applications, overall increasing the usability and ergonomics of OpenPGP for the end-user." This matters because Java/Kotlin is the primary implementation stack for Android applications and server-side email tools, and most Java OpenPGP libraries have historically omitted WoT path computation. The project builds on Sequoia's formal specification, which provides test vectors via [wot-test-suite](https://github.com/pgpainless/pgpainless-wot/tree/main/wot-test-suite).

### GnuPG / OpenPGP WoT

- **Primary sources:** [gnupg.org](https://www.gnupg.org/), [github.com/gpg/gnupg](https://github.com/gpg/gnupg), [RFC 9580](https://www.rfc-editor.org/rfc/rfc9580.html)
- **Type:** mature OpenPGP implementation with local trust database
- **Status:** mature / active; GitHub mirror API on 2026-04-30 showed 917 stars, 195 forks, not archived, last pushed 2026-04-28. Maintainers do not use GitHub PRs/issues as the canonical workflow.

GnuPG remains the reference cultural implementation of WoT. It distinguishes:

- **Certificate validity** — whether a public key is believed to belong to an identity.
- **Ownertrust** — whether the user trusts that certificate holder to correctly certify others.
- **Certification signatures** — signatures over keys / user IDs.
- **Trust signatures** — delegated introducer signatures that can propagate trust.

The classic local policy is often summarized as "one fully trusted introducer or multiple marginal introducers," but actual trust decisions are local and configurable. Modern usage often bypasses full WoT UX in favor of pinned fingerprints, WKD, or TOFU-style workflows.

### keys.openpgp.org

- **Primary source:** [keys.openpgp.org FAQ](https://keys.openpgp.org/about/faq/)
- **Type:** abuse-resistant OpenPGP key discovery service
- **Status:** production; not decentralized in the old SKS sense.

keys.openpgp.org is not part of the SKS pool and does not use open federation. Its FAQ explicitly cites reliability, abuse-resistance, privacy, and usability concerns with SKS-style federation. It verifies email addresses, permits only one verified key per email at a time, and does not distribute third-party certifications by default because they allow arbitrary data to be attached to someone else's certificate.

For a cypherpunk reader, this is a compromise rather than a pure WoT: less decentralized than SKS, but far more survivable against poisoning and spam.

### First-party approved OpenPGP certifications

- **Primary sources:** [IETF draft-dkg-openpgp-1pa3pc-02](https://www.ietf.org/archive/id/draft-dkg-openpgp-1pa3pc-02.html), [JISA 2024 certificate-poisoning article](https://journals-sol.sbc.org.br/index.php/jisa/article/view/3810)
- **Type:** mitigation for OpenPGP certificate poisoning and certificate bloat
- **Status:** protocol design / research; important because it preserves third-party certifications only when approved by the certificate holder.

This is the most important modern lesson from the OpenPGP lineage: third-party attestations are useful, but arbitrary third parties should not be able to permanently enlarge or mutate someone else's certificate. First-party approved third-party certifications let keyholders explicitly approve which certifications should travel with their certificate, giving relying parties a principled pruning rule. See [OpenPGP Web of Trust](/kb/openpgp-web-of-trust/).

### OpenPGP Key Replacement (draft-ietf-openpgp-replacementkey)

- **Primary source:** [IETF draft-ietf-openpgp-replacementkey-07](https://datatracker.ietf.org/doc/draft-ietf-openpgp-replacementkey/)
- **Authors:** Daphne Shaw, Andrew Gallagher
- **Status:** Active IETF draft, version 07 (April 2026); expires October 2026
- **Type:** protocol extension for key migration signalling

This IETF draft specifies a mechanism for OpenPGP users to communicate that a new key should replace an expired, revoked, or superseded one. The draft (26 pages plus appendices) defines replacement key signalling — when a user publishes a new primary key, they can include a signed signal pointing to the replacement, and users who receive the old key see a machine-readable hint about where to find the successor.

The freedom-tech relevance is direct: long-lived OpenPGP identities need key rotation paths, and a replacement signal lets the WoT carry trust forward to a new key without requiring re-verification from all prior certifiers. This is not automatic recovery — it still requires the user to publish the replacement — but it makes the transition legible to clients and reduces the probability that old-key communications silently fail after rotation.

### OpenPGP ID: u4 and u5 Universal Identifiers

- **Primary source:** [foopgp.org blog, April 2026](https://foopgp.org/blog/2026-04-28-openpgp-id-spec/)
- **Specification:** draft-foopgp-openpgp-id-00, on [Codeberg](https://codeberg.org/foopgp/foopgp-hugowebsite/src/branch/public/public/documents/en/draft-foopgp-openpgp-id-00.txt)
- **Status:** first draft specification; submitted to IETF; production use in Djibian OS

This specification introduces two privacy-respecting universal identifiers derived from civil-registry-style data:

- **u4 (human identifier):** derived from last birth surname + first and second given names + date of birth. Processed through MD5 (for compatibility with identifiers generated since 2010) and Base64url encoding, with a geographic coordinates suffix. Produces a 39-character identifier that fits in an OpenPGP UID comment field. Pseudonymous — without the exact input data, the individual cannot be identified, but the identifier is permanent (does not change on marriage, name change, or naturalisation).

- **u5 (universal identifier for anything):** Unix timestamp + geographic coordinates, identifying any entity by its moment and place of origin. Used for associations, software components, AI agents, or humans who prefer not to disclose civil data.

The spec's privacy argument is specific: producing two individuals with the same surname, given name, and date of birth is described as "beyond the reach of any computer — even the most powerful." The WoT certification fabric provides the real barrier: a u4 has value only when at least one certified human has physically verified the identity document.

Practical applications include using u4/u5 as HKP keysserver search keys, Unix user IDs in reserved ranges, YubiKey/NitroKey login-data fields, and POSIX home directory names. The reference implementation is in bash with a [Codeberg repository](https://codeberg.org/foopgp/bash-libs).

For WoT purposes, u4/u5 represents an attempt to build persistent pseudonymous identity on top of OpenPGP certificates without a central registry — the identifier is derived, not issued.

### Keyoxide and Ariadne proofs

- **Primary sources:** [keyoxide.org](https://keyoxide.org/), [docs.keyoxide.org](https://docs.keyoxide.org/), [Keyoxide OpenPGP docs](https://docs.keyoxide.org/service-providers/openpgp/)
- **Type:** decentralized online identity proof verification
- **Status:** active ecosystem; docs updated through 2024-12 per extracted page.

Keyoxide links profiles to proofs across platforms using notations and service-specific proof formats. For OpenPGP profiles, proofs can use `openpgp4fpr:FINGERPRINT` or related identifiers. The important privacy feature is persona separation: Keyoxide can prove that a pseudonymous profile controls several accounts without requiring a state-issued identity.

This is adjacent to WoT rather than a replacement for it. It answers "does this profile control these accounts?" WoT answers "given my graph and policy, how much should I trust this key / profile / claim?"

### OpenPGP libraries and clients

|| Project | Link | Role | Maturity |
|---|---|---|---|
| GnuPG | [gnupg.org](https://www.gnupg.org/) | CLI and agent ecosystem; mature local trust model | Mature |
| OpenPGP.js | [github.com/openpgpjs/openpgpjs](https://github.com/openpgpjs/openpgpjs) | JavaScript OpenPGP implementation | Mature / active; 5,945 stars, last pushed 2026-04-09 |
| Mailvelope | [github.com/mailvelope/mailvelope](https://github.com/mailvelope/mailvelope) | Browser extension for OpenPGP in webmail | Mature / active; 1,825 stars, last pushed 2026-01-16 |
| Sequoia-PGP | [sequoia-pgp.org](https://sequoia-pgp.org/) | Rust OpenPGP implementation and tooling | Mature / active ecosystem |
| PGPainless | [pgpainless.org](https://pgpainless.org/) | Java OpenPGP library; NLnet-funded WoT implementation in progress | Active; WoT module at [pgpainless-wot](https://github.com/pgpainless/pgpainless-wot) |
| Sequoia WoT | [sequoia-wot.gitlab.io](https://sequoia-pgp.gitlab.io/sequoia-wot/) | Formal WoT specification and Rust reference implementation | Mature / reference spec; ABNF grammar, OpenPGP concepts, path-finding algorithms |

## How trust is computed

### 1. Path distance

The simplest Nostr WoT query is hop distance:

```text
me → follow → Alice → follow → Bob
```

Bob is two hops away. A client might show Bob's replies by default while hiding accounts beyond three hops. This works well for spam reduction because low-cost Sybil accounts usually start outside the user's social graph.

Strengths:

- Easy to explain.
- Personalized.
- Works with existing Nostr follow events.

Limitations:

- A follow is not always endorsement.
- Popular bridge accounts can shorten paths too much.
- Communities with different norms may not want the same path threshold.

### 2. Weighted edges

Edges can be weighted by type:

| Edge type | Possible meaning | Suggested weight caution |
|---|---|---|
| Follow | I want to see this account | Weak endorsement; can include curiosity follows |
| List membership | I curated this account into a set | Stronger if list purpose is explicit |
| Mute / block | I do not want this account | Strong negative only if you trust the muter |
| Report | I allege abuse / spam | Needs rate limits and context |
| Zap | I sent value to this account | Costly signal; can still be gamed |
| OpenPGP certification | I verified this user ID / key binding | Identity-specific, not universal reputation |
| Keyoxide proof | This profile controls another account | Control proof, not character proof |

The core safety rule: **never collapse all edge types into one undifferentiated "trust" scalar without preserving provenance.**

### 3. PageRank / eigenvector scoring

PageRank-like algorithms rank nodes by endorsements from other ranked nodes. They are attractive for global discovery and marketplace reputation, and wot-scoring explicitly uses PageRank-style scoring for Nostr.

Strengths:

- Produces a sortable score.
- Captures recursive endorsement.
- Useful for default ranking when users have small graphs.

Limitations:

- Can centralize around high-degree accounts.
- Harder to explain to users.
- Vulnerable to collusive clusters unless combined with local trust anchors.

### 4. Threshold validity

Classic OpenPGP asks whether a certificate is valid, not whether it has a global rank. The policy can be threshold-based:

- One fully trusted introducer signs the key.
- Or several marginally trusted introducers sign the key.
- Or a local direct signature pins it.

This is useful for binary decisions like "should I encrypt to this key?" It is less useful for social ranking, where a continuous score and context matter.

### 5. Trusted assertions

NIP-85 turns computed trust into signed data. A provider can publish a `rank` tag for a pubkey, event, addressable event, or external identifier. Users choose trusted providers with kind `10040`.

This pattern is powerful because it creates a market for reputation algorithms. One provider can optimize for spam filtering; another for merchant reliability; another for research credibility; another for a private community. The danger is that clients may quietly ship one default provider and recreate platform moderation under a new name.

## Use cases

### Spam filtering in decentralized social

Nostr needs spam filtering without a single platform operator. WoT gives several levers:

- Hide replies from accounts outside the user's graph.
- Require relay AUTH and a minimum graph score for writes.
- Use NIP-51 mute lists and NIP-85 ranks as local inputs.
- Prefer event recommendations from people or services the user already trusts.

This pairs naturally with proof-of-work and paid relays. PoW raises cost for unknown accounts; WoT reduces friction for accounts near the user's graph.

### Merchant and marketplace reputation

The [nostr-wot](https://github.com/nostr-wot/nostr-wot) repository lists Mapping Bitcoin as a project using WoT-based trust filtering. Merchant directories, freelancer markets, and local exchange boards need reputation, but a centralized Yelp-like score is both censorable and gameable. A WoT merchant view can ask: "who in my graph has interacted with this merchant?"

### Software maintainer verification

Open-source ecosystems already use identity graphs informally: maintainers sign releases, projects list maintainers, Linux distributions pin keys, and users inherit trust from package maintainers. OpenPGP WoT can still help in high-assurance contexts, but modern practice often prefers reproducible builds, Sigstore-style transparency, maintainers' signing keys, and direct fingerprint verification.

WoT remains relevant when the question is not just "is this artifact signed?" but "do I know a path to the person or group controlling this key?"

### Community moderation

NIP-72 communities, relay policies, and NIP-51 lists create the raw material for community-specific trust. A community can trust moderators, curated author lists, or report providers without forcing that policy on the whole network.

The freedom-tech requirement is exit: users must be able to change relays, change clients, change assertion providers, or fork the policy.

### Pseudonymous identity and proof bundles

A pseudonym may want reputation without doxxing. Keyoxide-style proofs, Nostr event history, zaps, signed statements, and WoT edges can form a reputation bundle. This supports [Overview - Identity & Pseudonymity](/kb/identity-and-pseudonymity/): long-lived pseudonyms can accumulate trust while retaining separation from legal identity.

### Key transition and recovery

WoT can help a community accept key rotation. If an old key signs a new key, and trusted peers also attest to the migration, clients can treat the new key as a likely continuation. This is not automatic account recovery; it is social evidence around a key transition.

## Evidence at a glance

|| System / project | Primary source | Maturity | Active development | What it proves |
|---|---|---|---|---|
| GnuPG / OpenPGP WoT | [gnupg.org](https://www.gnupg.org/), [RFC 9580](https://www.rfc-editor.org/rfc/rfc9580.html) | Mature | Active; GitHub mirror pushed 2026-04-28 | Long-running local trust database and certification model |
| RFC 9580 OpenPGP | [RFC Editor](https://www.rfc-editor.org/rfc/rfc9580.html) | Standard | Published July 2024 | Current OpenPGP format, v6 keys, modern algorithms |
| OpenPGP Key Replacement | [draft-ietf-openpgp-replacementkey-07](https://datatracker.ietf.org/doc/draft-ietf-openpgp-replacementkey/) | Active IETF draft | Version 07, April 2026 | Machine-readable key migration signalling for WoT continuity |
| OpenPGP ID (u4/u5) | [foopgp.org spec](https://foopgp.org/blog/2026-04-28-openpgp-id-spec/) | Early / in production (Djibian) | Spec submitted to IETF 2026 | Privacy-respecting pseudonymous identifiers derived from civil registry data |
| keys.openpgp.org | [FAQ](https://keys.openpgp.org/about/faq/) | Production | Active service | Abuse-resistant key discovery; intentionally limits third-party cert distribution |
| First-party approved certifications | [IETF draft](https://www.ietf.org/archive/id/draft-dkg-openpgp-1pa3pc-02.html), [JISA 2024](https://journals-sol.sbc.org.br/index.php/jisa/article/view/3810) | Research / draft protocol | Active as design lineage | Consentful mitigation for SKS-style certificate poisoning |
| Keyoxide | [keyoxide.org](https://keyoxide.org/), [docs](https://docs.keyoxide.org/) | Production / community | Active docs and ecosystem | Decentralized account-control proofs for pseudonymous profiles |
| Nostr NIP-51 Lists | [nips.nostr.com/51](https://nips.nostr.com/51) | Draft optional | Used by clients | Follow, mute, relay, community, and curation lists as graph inputs |
| Nostr NIP-85 Trusted Assertions | [nips.nostr.com/85](https://nips.nostr.com/85) | Draft optional | Recent / evolving | Signed provider-computed ranks and metrics |
| nostr-wot toolkit | [github.com/nostr-wot/nostr-wot](https://github.com/nostr-wot/nostr-wot) | Experimental | Last pushed 2026-04-29 | Self-hostable graph distance / oracle infrastructure |
| nostr-wot oracle | [github.com/nostr-wot/nostr-wot-oracle](https://github.com/nostr-wot/nostr-wot-oracle) | Emerging | Part of nostr-wot org | Shared global follow-graph indexer answering pairwise distance queries |
| nostr-wot extension | [github.com/nostr-wot/nostr-wot-extension](https://github.com/nostr-wot/nostr-wot-extension) | Experimental | Last pushed 2026-04-26 | Browser-level identity + wallet + trust API |
| wot-relay | [github.com/barrydeen/wot-relay](https://github.com/barrydeen/wot-relay) | Emerging | 85 stars, pushed 2026-04-22 | Relay-side archiving / filtering by user's graph |
| wot-scoring | [github.com/joelklabo/wot-scoring](https://github.com/joelklabo/wot-scoring) | Experimental | Last pushed 2026-02-11 | PageRank-style WoT metrics published as NIP-85 events; live at wot.klabo.world |
| Chronicle | [github.com/dtonon/chronicle](https://github.com/dtonon/chronicle) | Active; v0.5.0 May 2026 | 32 stars, pushed 2026-04-30 | Personal relay with owner-participation rules, second-degree WoT spam protection, Blossom media built in |
| Brainstorm WoT relay | [github.com/Pretty-Good-Freedom-Tech/brainstorm](https://github.com/Pretty-Good-Freedom-Tech/brainstorm) | Paused | 5 stars, pushed 2026-02-28 | Personalized WoT relay; self-signed NIP-85 kind 30382 events; kind 10040 provider declaration |
| PGPainless WoT | [github.com/pgpainless/pgpainless-wot](https://github.com/pgpainless/pgpainless-wot) | In development | NLnet/NGI Assure funded | Java/Kotlin OpenPGP WoT path computation; test vectors from Sequoia |
| rust-nostr SDK | [github.com/nbd-wtf/nostr-tools](https://github.com/nbd-wtf/nostr-tools) | Mature | 843 stars, pushed 2026-05-19 | Dominant Rust implementation; shipped 21-PR architecture overhaul May 2026 |

## Trade-offs

### Strengths

- **No universal root authority.** Trust starts from the user or community, not a CA or platform.
- **Local autonomy.** Different users can apply different trust policies to the same public graph.
- **Sybil friction.** Fake identities are cheap, but infiltrating many independent trust graphs is harder.
- **Composability.** WoT can combine with [Overview - Decentralized DNS](/kb/decentralized-dns/), [Overview - Encrypted Messaging](/kb/encrypted-messaging/), [Nostr](/kb/nostr-identity/), [Pubky](/kb/pubky/), [ENS as Identity](/kb/ens-identity/), and [Remote Signing](/kb/remote-signing/).
- **Pseudonym-friendly.** Reputation can attach to keys and behavior rather than passports.

### Limitations

- **Cold start.** New users have no graph. Defaults become powerful.
- **Ambiguous edges.** A follow, signature, zap, report, and mute mean different things.
- **UI complexity.** Users rarely want to manage trust paths manually.
- **Graph leakage.** Publishing follows and endorsements reveals social structure.
- **Staleness.** Old certifications and follows may outlive the relationship they represent.
- **Capture risk.** A default oracle or extension can become a de facto central authority.

### Attack surface

| Attack | Description | Mitigation |
|---|---|---|
| Sybil cluster | Attacker creates many identities that trust each other | Anchor scores in the user's local graph; cap benefit from tightly connected new clusters |
| Trust farming | Attacker gains follows from many users through benign behavior, then abuses trust | Freshness, behavior windows, negative signals, manual override |
| Bridge-node capture | Compromise or manipulate a highly connected introducer | Limit path length; diversify paths; expose why a score is high |
| Key poisoning | Attach malicious data/signatures to a target certificate | First-party attestation, consentful keyservers, WKD, local pinning |
| Oracle capture | A scoring provider becomes the hidden arbiter | Multiple providers, self-hosting, signed methodology, visible provider key |
| Social graph deanonymization | Trust edges reveal relationships | Private lists, NIP-44 encrypted list entries, per-context pseudonyms |
| Stale trust | Old signatures or follows remain after compromise or relationship change | Expiring edges, revocations, periodic review, time decay |

## Design rules for freedom-tech WoT

1. **Start local.** The user's own trust anchors should matter more than global popularity.
2. **Preserve edge semantics.** Do not treat follows, payments, reports, and certifications as the same signal.
3. **Make provenance visible.** A score should explain which provider, algorithm, graph snapshot, and edge types produced it.
4. **Support exit.** Users must be able to change clients, relays, assertion providers, and trust policies.
5. **Prefer consentful identity mutation.** Do not let third parties permanently attach arbitrary data to someone else's identity object.
6. **Assume Sybils.** A trust graph is not magic; combine it with cost signals, manual curation, and rate limits.
7. **Separate identity from reputation.** "Controls this key" and "is trustworthy in this context" are different claims.
8. **Plan for key rotation.** Long-lived pseudonyms need migration paths, signed transition events, and community attestation.

## June 11, 2026 Update — OpenPGP Schism and GnuPG 2.5.20

### The OpenPGP Split: LibrePGP v5 vs RFC 9580

The most significant development since the May 28 snapshot is the full crystallization of the OpenPGP standard split. This is not merely a technical disagreement — it represents a governance fracture with direct consequences for WoT interoperability.

**Two competing visions:**

1. **RFC 9580 (IETF "v6" OpenPGP)** — the official IETF proposed standard, produced through a multi-year multi-stakeholder process. Supported by Sequoia-PGP, OpenPGP.js v6 (November 2024), and Proton Mail. RFC 9580 became a draft standard in March 2025 when two independent interoperable implementations (Sequoia-PGP v2 + OpenPGP.js v6) confirmed implementations. This version obsoletes RFC 4880/5581/6637, introduces v6 keys, AEAD containers, Argon2 S2K, and mandatory Ed25519/X25519.

2. **LibrePGP (GnuPG "v5")** — GnuPG maintainer Werner Koch's competing proposal, described by critics as a fork from a pre-RFC9580 draft. GnuPG's own home page (as of 2026) still describes itself as implementing "RFC 4880," deliberately avoiding RFC 9580. The IETF OpenPGP Working Group did not adopt LibrePGP.

**GnuPG 2.5.20 (May 13, 2026)** is the key event: Werner Koch's release announcement explicitly introduces Kyber/ML-KEM (FIPS 203) as a post-quantum encryption algorithm in the 2.5 series, adds GCM encryption to `gpgsm`, and warns that the 2.4 series approaches end-of-life. Critically, GnuPG 2.5.20 implements LibrePGP v5 features, not RFC 9580 v6. The release notes do not mention RFC 9580 compatibility. This means GnuPG — the dominant OpenPGP implementation in GNU/Linux distributions, package managers, and server tooling — is diverging from the IETF standard.

**Why this matters for WoT:** The OpenPGP WoT depends on shared certificate formats and signature semantics. If GnuPG and Sequoia/OpenPGP.js can no longer process each other's certificates, cross-signing between the two camps becomes impossible. Key validation paths break. The trust graph literally cannot connect keys from the two ecosystems. For freedom-tech deployments relying on OpenPGP certifications for [OpenPGP Web of Trust](/kb/openpgp-web-of-trust/), this is a critical fragmentation risk.

**Nuance:** The schism is partly about what constitutes a "clean break" vs backward compatibility. RFC 9580 intentionally drops legacy features; LibrePGP attempts to preserve them. But the practical interoperability issue is real — the IETF has one standard, GnuPG implements another.

### Two New Gallagher IETF Drafts (June 2026)

Andrew Gallagher has published two complementary OpenPGP maintenance drafts that update and clarify RFC 9580:

1. **[draft-gallagher-openpgp-signatures-03](https://datatracker.ietf.org/doc/draft-gallagher-openpgp-signatures/)** (June 2026, expires December 2026) — "OpenPGP Signatures." Clarifies grammar and semantics for signature packets, third-party signatures, notary signatures (Type 40), and certification signatures. The abstract notes: "This document specifies several updates and clarifications to the grammar and semantics of OpenPGP signatures." This is maintenance of RFC 9580 rather than a new direction.

2. **[draft-gallagher-openpgp-messages-00](https://datatracker.ietf.org/doc/draft-gallagher-openpgp-messages/)** (June 2026, expires December 2026) — "OpenPGP Message Grammar." Companion document clarifying OpenPGP message formats, One-Pass Signature packet semantics, and message structure. The abstract: "This document specifies several updates and clarifications to the grammar and semantics of OpenPGP messages."

3. **OpenPGP HTTP Keyserver Protocol** (draft-gallagher-openpgp-hkp-andrewgdotcom) — defines how keyservers should handle v6 certificates (v6 keys must NOT be returned for legacy machine-readable requests, but MAY be returned for human-readable). Also specifies v2 lookup using `by-keyid` and `by-vfingerprint` categories.

These drafts represent continued IETF-side maintenance of the RFC 9580 ecosystem and are independent of the GnuPG/LibrePGP split.

### OpenPGP Key Replacement Draft-07 (April 2026)

[draft-ietf-openpgp-replacementkey-07](https://datatracker.ietf.org/doc/draft-ietf-openpgp-replacementkey/) reached version 07 in April 2026, expiring October 2026. The draft specifies machine-readable key replacement signalling — when a user rotates to a new primary key, they publish a signed replacement event that clients can interpret to automatically migrate trust paths. This directly benefits long-lived [OpenPGP Web of Trust](/kb/openpgp-web-of-trust/) identities: a replacement signal lets prior certifications carry forward to a new key without requiring all certifiers to re-sign.

### wot.nostr.net — New Production Public WoT Relay (Bitvora, June 2026)

A new public WoT relay appeared at `wss://wot.nostr.net` in June 2026, built by Bitvora using the Khatru relay framework. Unlike self-hosted personal relays (Chronicle, wot-relay), this is a public relay with WoT filtering as a first-class feature — it serves content from accounts within a user's declared follow graph, reducing spam and noise. Source: [github.com/bitvora/wot-relay](https://github.com/bitvora/wot-relay). This represents the first production public WoT relay from an established Nostr infrastructure provider, complementing the self-hosted patterns established by Chronicle and barrydeen's wot-relay.

### Updated GitHub Activity (June 11, 2026)

||| Project | Stars | Last push | Notes ||
|||---------|------:|-----------|-------|
||| [gpg/gnupg](https://github.com/gpg/gnupg) | 938 | 2026-05-26 | GnuPG 2.5.20 (May 13) introduces ML-KEM but follows LibrePGP v5, not RFC 9580 |
||| [openpgpjs/openpgpjs](https://github.com/openpgpjs/openpgpjs) | 5,948 | 2026-05-26 | RFC 9580 v6 support since November 2024 |
||| [barrydeen/wot-relay](https://github.com/barrydeen/wot-relay) | 85 | 2026-04-22 | Stable personal WoT relay |
||| [bitvora/wot-relay](https://github.com/bitvora/wot-relay) | — | 2026-06 | New public WoT relay from Bitvora; Khatru framework |
||| [dtonon/chronicle](https://github.com/dtonon/chronicle) | 32 | 2026-04-30 | Personal relay; v0.5.0 May 2026 |
||| [nostr-wot/nostr-wot](https://github.com/nostr-wot/nostr-wot) | 6 | 2026-04-29 | Extension + SDK; stable |
||| [greenart7c3/Amber](https://github.com/greenart7c3/Amber) | 314 | 2026-05-30 | Dominant Nostr signer app |
||| [nbd-wtf/nostr-tools](https://github.com/nbd-wtf/nostr-tools) | 843 | 2026-05-19 | May 2026 architecture overhaul shipped |

**Key observations:** The OpenPGP ecosystem now has a clear fork. GnuPG 2.5.20 (May 13, 2026) follows LibrePGP v5 rather than RFC 9580. This means the dominant CLI/tooling implementation is technically non-standard relative to the IETF. Sequoia-PGP, OpenPGP.js, and Proton remain on RFC 9580. For WoT, this creates two certificate universes that cannot cross-certify — a serious fragmentation with no resolution in sight.

### Brainstorm WoT Relay: Corrected Status

The Brainstorm WoT relay from Pretty-Good-Freedom-Tech was described as "Active" in the Nostr WoT file but marked "Paused" in the Overview. Confirmed status: **Paused**. Last non-documentation commit was February 2026. The project's MIT license and self-hosted WoT relay architecture remain valuable as a reference design, but active development has stalled.

## Late-May 2026 Developments

### Cross-Client WoT Trust Score Display (Q1 2026)

Multiple independent Nostr clients began displaying WoT-based trust scores in their UI during Q1 2026. Amethyst (Android), Primal, and Coracle all surface trust scores on user profiles. Amethyst's changelog notes that "by connecting to a WoT provider, you can see trust scores and verified follower counts directly on user pictures. This helps filter signal from noise." Coracle displays a trust indicator with the message: "If you can't tell the difference between me and a scammer, use a nostr client with web of trust support."

This marks WoT transitioning from a developer-facing library feature to a user-visible product feature — significant for mainstream adoption, but raises design questions about presenting trust signals without creating a surveillance-score aesthetic or opaque authority.

### FROST RFC 9591 — Stable Specification Supports Frostr Maturation

RFC 9591 (FROST Protocol) was published by the IRTF in June 2024, giving threshold Schnorr signatures a stable normative reference. The Nostr Frostr ecosystem — Bifrost (core TypeScript library), Igloo Server (self-hostable signer), and the Igloo app suite — now has a stable spec to implement against. The RFC covers the signing protocol but explicitly does not standardize distributed key generation; trusted-dealer vs. DKG remains an implementation choice. Nonce reuse is the critical footgun across all FROST deployments: one reused nonce leaks the secret share.

### NIP-26 Delegation Has No Revocation Mechanism

NIP-26 delegated event signing is marked unrecommended in the NIPs README. Historical discussion of revocation does not make it a recommended custody mechanism. NIP-46 remote signing does not require NIP-26.

### OpenPGP Key Replacement Draft-ietf-openpgp-replacementkey-07 (April 2026)

The IETF active draft specifies a machine-readable mechanism for OpenPGP users to signal that a new key should replace an expired, revoked, or superseded one. When a user publishes a new primary key, they can include a signed signal pointing to the replacement; users who receive the old key see a machine-readable hint about where to find the successor. For WoT continuity, this matters: long-lived OpenPGP identities need key rotation paths, and the replacement signal lets trust carry forward to a new key without requiring re-verification from all prior certifiers. Draft version 07 was published April 2026 and expires October 2026.

### OpenPGP ID u4/u5 Universal Identifiers (IETF Draft, Djibian OS Production)

The foopgp.org [draft-foopgp-openpgp-id-00](https://foopgp.org/blog/2026-04-28-openpgp-id-spec/) introduces two privacy-respecting identifiers derived from civil-registry-style data:

- **u4** (human identifier): derived from last birth surname + first and second given names + date of birth, processed through MD5 and Base64url encoding. Produces a 39-character identifier that fits in an OpenPGP UID comment field. Pseudonymous — without the exact input data, re-identification is computationally intractable, but the identifier is permanent across marriage, name change, or naturalisation.

- **u5** (universal identifier for anything): Unix timestamp + geographic coordinates, identifying any entity by its moment and place of origin. Used for AI agents, software components, or humans who prefer not to disclose civil data.

For WoT purposes, u4/u5 represents an attempt to build persistent pseudonymous identity on OpenPGP certificates without a central registry. The spec has been submitted to IETF and is in production use in Djibian OS.

### May 28 Update — GitHub Activity Snapshot

Checked GitHub API May 28, 2026 for key WoT project activity:

| Project | Stars | Forks | Last push | Notes |
|---------|------:|------:|-----------|-------|
| [gpg/gnupg](https://github.com/gpg/gnupg) | 938 | 201 | 2026-05-26 | Active GnuPG development continues |
| [openpgpjs/openpgpjs](https://github.com/openpgpjs/openpgpjs) | 5,948 | 821 | 2026-05-26 | JavaScript OpenPGP remains actively maintained |
| [barrydeen/wot-relay](https://github.com/barrydeen/wot-relay) | 84 | 28 | 2026-04-22 | Personal WoT relay; NIP-11 update merged Apr 22 |
| [nostr-wot/nostr-wot](https://github.com/nostr-wot/nostr-wot) | 6 | 2 | 2026-04-29 | Extension and SDK active; React hook fixes merged |
| [nostr-wot/nostr-wot-sdk](https://github.com/nostr-wot/nostr-wot-sdk) | 4 | — | 2026-04-29 | SDK monorepo with @nostr-wot/data 0.4.2, React #185 fix |
| [dtonon/chronicle](https://github.com/dtonon/chronicle) | 30 | 4 | 2026-04-30 | Negentropy support restricted to relay owner by default |
| [mailvelope/mailvelope](https://github.com/mailvelope/mailvelope) | 1,824 | 222 | 2026-05-21 | Active maintenance; stable browser extension ecosystem |

**Key observations:** The Nostr WoT ecosystem remains in the experimental-to-emerging band. GnuPG and OpenPGP.js show steady production maintenance. The PGPainless WoT module's last commits were September 2025 (Gradle 8.8 upgrade), suggesting the funded development phase may be concluding. The Brainstorm freedom-tech WoT relay project has not had commits since February 2026 (minor documentation edits). The overall ecosystem is functional and maintained but not rapidly growing in contributor count.

### Late-May 2026 GitHub Freshness Snapshot

As of May 28–31, 2026, fresh GitHub API data for key WoT-related repositories:

|| Project | Stars | Last push | Notes ||
||---------|------:|-----------|-------|
|| [nostr-protocol/nips](https://github.com/nostr-protocol/nips) | 2,978 | 2026-05-31 | Protocol spec repo — active maintenance confirms ongoing NIP refinement |
|| [nbd-wtf/nostr-tools](https://github.com/nbd-wtf/nostr-tools) | 843 | 2026-05-19 | Dominant Rust Nostr SDK; shipped 21-PR architecture overhaul May 2026 |
|| [greenart7c3/Amber](https://github.com/greenart7c3/Amber) | 314 | 2026-05-30 | Highest-starred dedicated Nostr signer; NIP-07 + NIP-46 on Android |
|| [openpgpjs/openpgpjs](https://github.com/openpgpjs/openpgpjs) | 5,948 | 2026-05-26 | Steady production maintenance; 821 forks |
|| [barrydeen/wot-relay](https://github.com/barrydeen/wot-relay) | 85 | 2026-04-22 | +1 star since May 28; NIP-11 relay info update merged Apr 22 |
|| [dtonon/chronicle](https://github.com/dtonon/chronicle) | 32 | 2026-04-30 | +2 stars since May 28; personal relay with second-degree WoT filtering |
|| [pubky/pubky-core](https://github.com/pubky/pubky-core) | 77 | 2026-05-29 | +1 star since last check; Ed25519 + PKARR identity stack |
|| [FROSTR-ORG/igloo-server](https://github.com/FROSTR-ORG/igloo-server) | 8 | 2026-05-28 | +0 stars; self-hostable Frostr server with NIP-46-compatible interface |
|| [FROSTR-ORG/bifrost](https://github.com/FROSTR-ORG/bifrost) | 10 | 2026-02-16 | +0 stars; likely in spec/design phase for v2 direction |
|| [nostrcg/did-nostr](https://github.com/nostrcg/did-nostr) | 9 | 2026-01-11 | W3C CG draft; secp256k1 as DID identifier; no update/delete ops |

**Key observations:** The Nostr WoT ecosystem is stable rather than rapidly expanding. Amber (314 stars) is the clear leader among dedicated signer apps. The NIPs repo's push on 2026-05-31 confirms the protocol layer is still actively maintained. The gap in Bifrost commits (Feb–May 2026) aligns with the Igloo v2 architectural direction — likely a spec/design phase rather than abandonment. OpenPGP.js (5,948 stars) continues steady maintenance as the reference JavaScript implementation.

### Early-June 2026 Developments

#### wot.nostr.net — New Public WoT Relay by Bitvora

A new public WoT relay appeared at `wot.nostr.net` (WebSocket: `wss://wot.nostr.net`), built and maintained by Bitvora and powered by the Khatru relay framework. The relay implements a web-of-trust filtering model: it serves content from accounts within a user's follow graph, dramatically reducing noise and spam compared to open public relays. Source code is available at [github.com/bitvora/wot-relay](https://github.com/bitvora/wot-relay). This represents the first production public WoT relay from a known Nostr infrastructure provider, and serves as a notable counterpart to the self-hosted `wot-relay` by barrydeen and the personal relay pattern established by Chronicle.

#### Vertex Lab: Why They Don't Use NIP-85

A technical critique from Vertex Lab (vertexlab.io) argues that NIP-85 trusted assertions fundamentally conflict with WoT's discovery function. Their core objection: NIP-85 requires users to already know the pubkeys of people they're looking for, which inverts the purpose of a trust graph — WoT should help discover unknown accounts, not just rank known ones. The Vertex position is worth tracking because it articulates a real tension: provider-computed assertions help clients that already have graph context, but they don't help new users bootstrap or help existing users discover outside their bubble. This connects to the cold-start and oracle capture issues already noted in the Trade-offs section.

#### NIP-26 Delegation Revocation: Issue #654 Active

NIP-26 remains an unrecommended proposal. Use the current NIPs README for its status rather than treating a historical revocation discussion as an endorsement of delegation.

#### GitHub Activity — Early June 2026

||| Project | Stars | Last push | Notes ||
|||---------|------:|-----------|-------|
||| [bitvora/wot-relay](https://github.com/bitvora/wot-relay) | ~90+ | 2026-06-01 | New Bitvora fork; powers wot.nostr.net; active ||
||| [nostr-wot/nostr-wot](https://github.com/nostr-wot/nostr-wot) | 6 | 2026-04-29 | SDK/extension/org toolkit — no significant change ||
||| [barrydeen/wot-relay](https://github.com/barrydeen/wot-relay) | 85 | 2026-04-22 | Original wot-relay; NIP-11 update merged Apr 22 ||
||| [dtonon/chronicle](https://github.com/dtonon/chronicle) | 32 | 2026-04-30 | Personal relay; second-degree WoT + PoW fallback ||
||| [gpg/gnupg](https://github.com/gpg/gnupg) | 938+ | 2026-06-02 | Active GnuPG; steady maintenance ||
||| [nbd-wtf/nostr-tools](https://github.com/nbd-wtf/nostr-tools) | 843+ | 2026-06-03 | Dominant Rust SDK; architecture overhaul complete May 2026 ||

**Key observations:** The Bitvora wot-relay fork is the most significant new development — it brings a production-grade public relay online with WoT filtering as a first-class feature. The NIPs repo continues active maintenance through early June 2026. The overall WoT tooling ecosystem is stable, with no major new projects appearing but existing projects receiving consistent maintenance.

#### NIP-85 Deployment Summary

By early June 2026, NIP-85 trusted assertions have reached a notable milestone: they are now implemented across independently developed clients (Amethyst, Primal, Coracle), served by multiple relay types (personal relays, public WoT relays, and dedicated scoring oracles), and generating signed events that ordinary users encounter as trust scores in their feeds. This cross-client, multi-provider deployment confirms that NIP-85 has transitioned from a draft proposal to load-bearing infrastructure in the Nostr WoT stack.

The architectural implication remains unchanged: clients that cannot crawl and compute the graph locally now depend on signed assertions from declared provider keys. This makes the provider declaration mechanism (kind `10040`) a critical trust anchor — its security and transparency properties directly determine whether the WoT remains user-sovereign or drifts toward centralized oracle dominance.

## Open questions

- Can Nostr clients converge on interoperable WoT APIs without blessing a single scoring provider?
- Should follows be treated as endorsements, subscriptions, or simply routing preferences?
- What is the right privacy model for graph-based spam filtering when social graphs are sensitive?
- Can NIP-85 providers publish enough methodology for users to audit bias and capture?
- How should WoT handle key compromise, death, coercion, and long-term inactivity?
- Can reputation be portable across Nostr, Pubky, ENS, OpenPGP, and DID systems without creating a universal surveillance identifier?
- Does NIP-85's provider model help discovery or does it require users to already know providers they trust, defeating the discovery use case? (See Vertex Lab critique above.)

## June 18, 2026 Update — ContextVM WoT Stack, OpenPGP PQC RFC, Fourteenth Wave Grants

### ContextVM / Relatr — New Personalized Trust Scoring Service

The most significant new development this week is the emergence of [ContextVM](https://opensats.org/projects/contextvm) and its companion WoT service **Relatr**. ContextVM is a protocol for exposing and calling **Model Context Protocol (MCP)** servers over Nostr — replacing domain names, API keys, and open ports with public-key identity and relay transport. The motivation is directly WoT-relevant: if AI agents and MCP services can find each other through cryptographic keys over Nostr, then the WoT becomes the natural trust layer for autonomous agents.

OpenSats funded ContextVM in the **fifteenth wave of Nostr grants** to support protocol work, SDK improvements, and shared relay infrastructure. The roadmap includes payment support (extending CEP-8 to a wider toolset), TypeScript/Rust SDK parity, one-click deployments, and tighter integration with open-source developer tooling.

**Relatr** ([github.com/ContextVM/relatr](https://github.com/ContextVM/relatr)) is the WoT-specific component of the ContextVM stack. Per its README:

> "Relatr is a decentralized web of trust metric service for Nostr that computes personalized trust scores by combining social graph distances with profile validation metrics."

Technical specifications:

- **Runtime:** Bun (Node.js-compatible)
- **Database:** DuckDB (in-memory columnar store, social graph fits well)
- **Components:** `nostr-social-duck` core, `relo`/`elo` modules, web config UI via process-pastry
- **Plugin system:** official plugins + community plugins + `skills/relatr-elo-plugin-author` for AI-assisted plugin creation
- **MCP server support:** runs as an MCP server itself, so AI agents can ask Relatr for trust scores via the standard MCP protocol — a self-referential architecture where the WoT infrastructure is reachable by the agents it is meant to assess
- **Tunable parameters:** `NUMBER_OF_HOPS` (graph traversal depth), `DECAY_FACTOR` (trust decay over distance), `CACHE_TTL_HOURS`, `DEFAULT_SOURCE_PUBKEY` (personalized root), and `TA_ENABLED` (Trusted Assertions support)
- **178 commits** as of mid-June 2026, **11 stars**, last pushed 2026-05-26; production deployment via Docker Compose

The architecture is important because it generalizes the Oracle pattern: instead of every client crawling the follow graph, clients (or AI agents) query a Relatr instance with their source pubkey and get back a personalized score. The user picks the Relatr server, the Relatr server picks the algorithm, and the result is signed and cacheable — the same trust boundaries as NIP-85 providers, but accessible to AI agents through MCP.

A complementary repo, [ContextVM/wotrlay](https://github.com/ContextVM/wotrlay) (tags: `contextvm`, `mcp`, `nostr`, `web-of-trust`, `wot`), is a WoT-aware relay that filters events through the social graph before serving them. Topics metadata confirms the WoT-first design intent.

### wot-scoring Maturation — Community Detection + Composite Providers

The [joelklabo/wot-scoring](https://github.com/joelklabo/wot-scoring) repository (still small at 1 star, last push 2026-02-11, but algorithmically influential) has accumulated several capabilities that materially change what "WoT scoring" means in practice:

- **Consumes kind `10040`** (provider authorization declarations) — verifies which providers the user has explicitly trusted
- **Consumes kind `10000`** (mute lists from NIP-51) — uses mute lists as community-moderation signal inputs
- **Enriches relay data from trustedrelays.xyz** with social reputation metadata — couples relay quality to WoT
- **Detects trust communities via label propagation** — algorithmic clustering of follow-graph components; useful for finding sub-communities and Sybil clusters
- **Composes trust scores from external NIP-85 providers** — when one provider is missing or stale, the system can fall back to a second declared provider

The composite-provider design directly addresses the "oracle capture" risk already flagged in the trade-offs section above: instead of binding to a single provider, clients can require N-of-M provider agreement and treat divergence as a signal to investigate. The label-propagation community detection is the first Nostr WoT algorithm I have seen that explicitly tries to identify Sybil clusters rather than just filter them out.

### OpenSats Fourteenth Wave of Nostr Grants (June 2026)

The [Fourteenth Wave of Nostr Grants](https://opensats.org/blog/fourteenth-wave-of-nostr-grants) includes three WoT-relevant projects:

**1. YakiHonne (first-time grant)** — multi-platform Nostr client (web, iOS, Android, Zapstore). Already implements outbox-style relay publishing and Web-of-Trust mechanisms. Planned work under grant: offline-first publishing with queued delivery, NsecBunker integration, Cashu and Nutzap support (NIP-60/NIP-61), and exploration of relay-level paid feeds. The repository is split across [YakiHonne/web-app](https://github.com/YakiHonne/web-app) (21 stars, last push 2026-05-17) and [YakiHonne/mobile-app](https://github.com/YakiHonne/mobile-app) (27 stars, last push 2026-05-14). YakiHonne matters because it is one of the few full-featured clients that ships WoT as a first-class user-visible feature rather than an experimental toggle.

**2. Quartz (first-time grant)** — Kotlin Multiplatform library implementing Nostr functionality for reuse across projects. Developed alongside [Amethyst](https://github.com/KotlinGeekDev/amethyst) and already used in production. The planned work is a refactor to move Android-specific code into shared multiplatform modules and build a first **iOS version of Amethyst** that can read and post on Nostr. The Quartz repository ([github.com/KotlinGeekDev/quartz](https://github.com/KotlinGeekDev/quartz)) is currently a directory inside the Amethyst monorepo. KMP Nostr libraries matter for WoT because client diversity is the only structural defense against any single client becoming the de facto trust UI; bringing Amethyst's WoT-aware UI to iOS is a significant cross-platform extension.

**3. Nostr Feedz (first-time grant)** — web app letting users follow traditional RSS feeds alongside Nostr long-form content (NIP-23), with a public guide/directory for discovering writers. Maintained by PlebOne ([github.com/PlebOne/Nostr-Feedz](https://github.com/PlebOne/Nostr-Feedz)). The companion relay at [relay.pleb.one](https://relay.pleb.one/) uses **invite-only Web-of-Trust access** with an admin dashboard for invite management — similar to fiatjaf's [pyramid](https://github.com/fiatjaf/pyramid) and utxo's WoT Relay. This is the third invite-only-WoT-access relay pattern after pyramid and wot-relay, indicating that "WoT-gated relay access" is becoming a recognized deployment pattern, not a one-off experiment.

The broader themes of the wave are offline-first architecture, payment interoperability (Cashu, Nutzaps), RSS ↔ Nostr bridging, and paid relay feeds with cross-client compatibility — all of which interact with WoT in different ways (paid feeds imply reputation, offline-first publishing implies relay-side trust filtering).

### OpenPGP PQC RFC 9980 — Almost Published

The most consequential OpenPGP development of 2026 for long-term WoT continuity is now nearly published as an RFC. The IETF datatracker history for [draft-ietf-openpgp-pqc](https://datatracker.ietf.org/doc/draft-ietf-openpgp-pqc/history) shows:

> 2026-01-06: RFC Editor state changed to EDIT.
> 2026-01-06: IESG state changed to RFC Ed Queue from Approved-announcement sent.

This is draft version 17, expires 17 July 2026, currently in **RFC-Ed-ACK** state per [IANA's 2026 IETF draft status](https://www.iana.org/performance/ietf-draft-status/2026). The [OpenPGP standards page](https://www.openpgp.org/about/standard) now lists **RFC 9980: Post-Quantum Cryptography in OpenPGP** alongside RFC 9580 — RFC 9980 is the official RFC number assigned to the PQC extension. This is the first new RFC number on the page since 2024.

**Why this matters for WoT:** The OpenPGP certification graph is composed of signed certificates whose validity spans years or decades. A WoT certificate signed today must continue to verify in a post-quantum world. The PQC RFC gives the OpenPGP ecosystem a defined path to ML-KEM (Kyber) key encapsulation and ML-DSA / SLH-DSA signatures inside the certificate format itself. Until RFC 9980 (or its eventual v5/v6 successor) is widely deployed, certifiers are signing with classical algorithms whose long-term verifiability is uncertain; once it is deployed, the WoT can carry forward trust across algorithm transitions rather than starting over.

**Important caveat — LibrePGP vs RFC 9980:** GnuPG 2.5.20 (May 13, 2026) introduced Kyber/ML-KEM as part of LibrePGP v5, **not** RFC 9980. RFC 9980 uses the IETF's chosen algorithm profile, which may differ in parameter selection or additional algorithm requirements. The same WoT-validity fragmentation risk flagged in the June 11 update applies: cross-signing between the LibrePGP and RFC 9580/9980 universes may not be possible.

### Additional OpenPGP Maintenance Drafts (June 2026)

The IETF OpenPGP working group [active drafts listing](https://datatracker.ietf.org/wg/openpgp) shows a cluster of new and updated drafts in late May / early June 2026:

- **[draft-ietf-openpgp-replacementkey-08](https://datatracker.ietf.org/doc/draft-ietf-openpgp-replacementkey/)** — updated May 29, 2026 (one month after version -07 covered in the June 11 update). The replacement-key mechanism is approaching IETF last call; this is the draft that lets long-lived OpenPGP identities signal key rotation without losing prior certifications.
- **[draft-ietf-openpgp-hkp-01](https://datatracker.ietf.org/doc/draft-ietf-openpgp-hkp/)** — "OpenPGP HTTP Keyserver Protocol," dated 2026-06-05, 51 pages. Defines how keyservers should handle v6 certificates — v6 keys must NOT be returned for legacy machine-readable requests but MAY be returned for human-readable requests. Also specifies v2 lookup using `by-keyid` and `by-vfingerprint` categories. This is the first IETF-standardized HTTP keyserver protocol since the SKS-era HKP, and it codifies the lessons from keys.openpgp.org about consentful certification distribution.
- **[draft-ietf-openpgp-nist-bp-comp-03](https://datatracker.ietf.org/doc/draft-ietf-openpgp-nist-bp-comp/)** — PQ/T Composite Schemes for OpenPGP using NIST and Brainpool elliptic curve domain parameters, dated 2026-01-08, 93 pages. Composite signatures combining classical (Brainpool) and post-quantum algorithms give certifiers a migration path that does not break verifiers still on classical algorithms.
- **Three new Andrew Gallagher drafts, all dated 2026-06-04:**
  - [draft-gallagher-openpgp-certificates-00](https://datatracker.ietf.org/doc/draft-gallagher-openpgp-certificates/) (25 pages) — OpenPGP Certificate Grammar
  - [draft-gallagher-openpgp-messages-00](https://datatracker.ietf.org/doc/draft-gallagher-openpgp-messages/) (9 pages) — OpenPGP Message Grammar
  - [draft-gallagher-openpgp-signatures-03](https://datatracker.ietf.org/doc/draft-gallagher-openpgp-signatures/) (25 pages) — OpenPGP Signatures (now at v03)

The cluster represents an unusually active week for the OpenPGP working group. The semantics of the certificate and signature grammars are the substrate the WoT walks; clarifying them is foundational maintenance that reduces the ambiguity that has historically allowed certificate poisoning to succeed.

### HAVEN v1.2.0 — Bitvora Personal Relay Now Multi-Npub + WoT Improvements

[Bitvora's HAVEN](https://github.com/bitvora/haven) ("High Availability Vault for Events on Nostr") reached **v1.2.0** with substantial WoT improvements, per the [release notes](https://github.com/bitvora/haven/releases) and coverage in [Nostr Compass #11](https://buttondown.com/nostrcompass/archive/nostr-compass-11):

- **Multi-npub support** with whitelisting and blacklisting
- **Rewritten backup system** using portable JSONL format with `haven restore` command
- **Cloud integration** via `--to-cloud`/`--from-cloud` flags
- **Web of Trust improvements:** configurable depth levels, 24-hour auto-refresh, lockless optimization for higher throughput
- **Data export** to compressed JSONL

HAVEN is the most sovereignty-oriented personal relay in the Nostr stack: full data export, multi-npub whitelist/blacklist, and WoT filtering at configurable graph depth. The 24-hour auto-refresh means the relay stays current with the user's evolving social graph without manual reconfiguration.

### fiatjaf/pyramid — Still Active, 66 Stars, Pushed June 17

[fiatjaf/pyramid](https://github.com/fiatjaf/pyramid) — the canonical invite-only-WoT-access relay pattern — remains active with **66 stars** and was last pushed **2026-06-17** (today). It is the original WoT-gated relay that the Bitvora wot-relay and PlebOne relay.pleb.one both follow as architectural references. The continued activity confirms that the pyramid pattern is stable infrastructure rather than a one-off experiment.

### Bitcoin 2026 Conference — WoT Curation Discussion (May 15, 2026)

The Bitcoin 2026 Conference panel ["Protocol vs Platform: Nostr's Utility Beyond Social Media"](https://www.youtube.com/watch?v=wrlE0DMoTSc) explicitly covered Web-of-Trust curation. From the chapter list:

> 14:00 — NosFabrica's Brainstorm And The Web Of Trust Reputation Layer
> 17:00 — How AI Agents Are Integrating With Nostr Natively
> 22:30 — Nostr Marketplaces, Identity And The Open Internet Stack

David Strayhorn of NosFabrica (the Brainstorm WoT relay project lead) presented the WoT reputation layer to a Bitcoin-native audience. This is the first major Bitcoin-industry stage presentation specifically on Nostr WoT reputation, suggesting the WoT layer is now recognized as part of the broader Bitcoin / freedom-tech stack rather than a niche Nostr experiment.

### Updated GitHub Activity — June 18, 2026 Snapshot

| Project | Stars | Last push | Notes |
|---------|------:|-----------|-------|
| [gpg/gnupg](https://github.com/gpg/gnupg) | 949 | 2026-06-17 | Active GnuPG; 2.5.20 stable, 2.4 EOL warning posted |
| [openpgpjs/openpgpjs](https://github.com/openpgpjs/openpgpjs) | 5,956 | 2026-06-17 | RFC 9580 v6 production |
| [nostr-protocol/nips](https://github.com/nostr-protocol/nips) | 2,997 | 2026-06-16 | NIP refinement continues |
| [nbd-wtf/nostr-tools](https://github.com/nbd-wtf/nostr-tools) | 846 | 2026-06-15 | Rust SDK steady |
| [greenart7c3/Amber](https://github.com/greenart7c3/Amber) | 321 | 2026-06-17 | Dominant Nostr signer |
| [fiatjaf/pyramid](https://github.com/fiatjaf/pyramid) | 66 | 2026-06-17 | Invite-only WoT relay, active |
| [hzrd149/blossom](https://github.com/hzrd149/blossom) | 281 | 2026-06-15 | Personal Blossom server |
| [ContextVM/sdk](https://github.com/ContextVM/sdk) | 10 | 2026-06-17 | MCP-over-Nostr SDK, new |
| [ContextVM/relatr](https://github.com/ContextVM/relatr) | 11 | 2026-05-26 | Personalized WoT scoring with MCP server |
| [ContextVM/wotrlay](https://github.com/ContextVM/wotrlay) | 2 | 2026-01-11 | WoT-aware relay (early) |
| [ContextVM/contextvm-docs](https://github.com/ContextVM/contextvm-docs) | 1 | 2026-06-16 | Documentation repo, new |
| [barrydeen/wot-relay](https://github.com/barrydeen/wot-relay) | 84 | 2026-04-22 | Stable |
| [bitvora/wot-relay](https://github.com/bitvora/wot-relay) | 84 | 2026-04-22 | Powers wot.nostr.net |
| [bitvora/haven](https://github.com/bitvora/haven) | n/a | 2026-Q2 | HAVEN v1.2.0 WoT improvements shipped |
| [dtonon/chronicle](https://github.com/dtonon/chronicle) | 35 | 2026-04-30 | Personal relay v0.5.0 |
| [nostr-wot/nostr-wot](https://github.com/nostr-wot/nostr-wot) | 7 | 2026-06-02 | Toolkit +1 star since June 11 |
| [pgpainless/pgpainless-wot](https://github.com/pgpainless/pgpainless-wot) | 0 | 2026-04-28 | Still no new commits since April |
| [joelklabo/wot-scoring](https://github.com/joelklabo/wot-scoring) | 1 | 2026-02-11 | Algorithmically influential, low repo activity |
| [YakiHonne/web-app](https://github.com/YakiHonne/web-app) | 21 | 2026-05-17 | YakiHonne client (web) |
| [YakiHonne/mobile-app](https://github.com/YakiHonne/mobile-app) | 27 | 2026-05-14 | YakiHonne client (mobile) |

**Key observations:**

1. **ContextVM / Relatr is the new WoT story of the month.** A WoT scoring service that runs as an MCP server is structurally important because it makes WoT callable from any AI agent that supports MCP — and 2026 is the year MCP is being adopted broadly. The 178-commit Relatr repo, MCP-server integration, and OpenSats funding combine into a real production path from "AI agent" to "ask the WoT who is trustworthy" without bespoke protocol work.

2. **OpenPGP PQC RFC 9980 is almost published.** Six months after draft-17 entered the RFC Editor queue (January 6, 2026), the official RFC number has been assigned. This is the structural answer to "what happens to the OpenPGP WoT when RSA and Ed25519 fall to quantum attack?" — and the LibrePGP v5 / RFC 9980 split remains unresolved.

3. **The NIPs repository is still active (June 16, 2026 push)** — protocol-level WoT refinement continues.

4. **Invite-only-WoT-access relays are a real pattern.** fiatjaf/pyramid, Bitvora wot-relay, and PlebOne relay.pleb.one all implement the same architectural idea through independent implementations.

5. **The activity gap between Rust/Python SDKs and the experimental WoT projects is widening.** The protocol-layer projects (GnuPG, OpenPGP.js, rust-nostr, nips, Amber, ContextVM SDK) are pushed within the last 48 hours; the WoT-specific tooling (Chronicle, wot-relay, wot-scoring, nostr-wot) is at April-May activity. This is consistent with the WoT layer being stable infrastructure rather than actively evolving primitives.

### June 18 OpenPGP Schism Status

The LibrePGP v5 vs RFC 9580 split flagged in the June 11 update has not progressed toward resolution. No new GnuPG 2.5.x release has appeared between May 13 and June 18, 2026. The [gnupg.org home page](https://www.gnupg.org) still describes GnuPG as implementing "RFC 4880," and the LWN article [Fedora and GPG 2.5](https://lwn.net/Articles/1055053) (covering the distribution packaging debate) confirms that **GnuPG 2.4 reaches end-of-life in June 2026** — meaning distributions must move to GnuPG 2.5 (LibrePGP v5, not RFC 9580) or fork. The practical implications for the OpenPGP WoT are unchanged from the June 11 update: two certificate universes, no resolution path visible.

### Updated References

New primary sources added this week:

- [ContextVM](https://opensats.org/projects/contextvm) — OpenSats project page for MCP-over-Nostr protocol
- [ContextVM/relatr](https://github.com/ContextVM/relatr) — personalized trust scoring service
- [ContextVM/wotrlay](https://github.com/ContextVM/wotrlay) — WoT-aware relay
- [ContextVM/sdk](https://github.com/ContextVM/sdk) — TypeScript/Rust MCP-over-Nostr SDKs
- [OpenSats Fourteenth Wave of Nostr Grants](https://opensats.org/blog/fourteenth-wave-of-nostr-grants) — YakiHonne, Quartz, Nostr Feedz
- [YakiHonne/web-app](https://github.com/YakiHonne/web-app) and [YakiHonne/mobile-app](https://github.com/YakiHonne/mobile-app) — client repos
- [PlebOne/Nostr-Feedz](https://github.com/PlebOne/Nostr-Feedz) — RSS+Nostr feed app with WoT-gated relay
- [PlebOne/relay.pleb.one](https://github.com/PlebOne/relay.pleb.one) — invite-only WoT relay
- [KotlinGeekDev/quartz](https://github.com/KotlinGeekDev/quartz) — KMP Nostr library, Amethyst parent
- [bitvora/haven](https://github.com/bitvora/haven) — personal relay, multi-npub WoT in v1.2.0
- [draft-ietf-openpgp-replacementkey-08](https://datatracker.ietf.org/doc/draft-ietf-openpgp-replacementkey/) — OpenPGP key replacement draft, May 29, 2026
- [draft-ietf-openpgp-hkp-01](https://datatracker.ietf.org/doc/draft-ietf-openpgp-hkp/) — OpenPGP HTTP Keyserver Protocol, June 5, 2026
- [draft-ietf-openpgp-nist-bp-comp-03](https://datatracker.ietf.org/doc/draft-ietf-openpgp-nist-bp-comp/) — composite NIST+Brainpool PQ/T schemes, January 8, 2026
- [draft-gallagher-openpgp-certificates-00](https://datatracker.ietf.org/doc/draft-gallagher-openpgp-certificates/) — OpenPGP Certificate Grammar, June 4, 2026
- [draft-gallagher-openpgp-messages-00](https://datatracker.ietf.org/doc/draft-gallagher-openpgp-messages/) — OpenPGP Message Grammar, June 4, 2026
- [draft-gallagher-openpgp-signatures-03](https://datatracker.ietf.org/doc/draft-gallagher-openpgp-signatures/) — OpenPGP Signatures v03, June 4, 2026
- [OpenPGP Standard page](https://www.openpgp.org/about/standard) — confirms RFC 9580 + RFC 9980
- [IANA 2026 IETF Draft Status](https://www.iana.org/performance/ietf-draft-status/2026) — confirms RFC-Ed-ACK state
- [Bitcoin 2026 Protocol vs Platform panel](https://www.youtube.com/watch?v=wrlE0DMoTSc) — WoT reputation coverage
- [LWN: Fedora and GPG 2.5](https://lwn.net/Articles/1055053) — distribution packaging implications

## Primary sources

- [NIPs README: NIP-26 status](https://github.com/nostr-protocol/nips)
- [NIP-46 remote signing](https://github.com/nostr-protocol/nips/blob/master/46.md)

### Standards and specs

- [RFC 9580 — OpenPGP](https://www.rfc-editor.org/rfc/rfc9580.html) — current OpenPGP standard, July 2024.
- [OpenPGP Key Replacement — draft-ietf-openpgp-replacementkey-07](https://datatracker.ietf.org/doc/draft-ietf-openpgp-replacementkey/) — IETF draft for machine-readable key migration signalling.
- [First-Party Approved Third-Party Certifications in OpenPGP](https://www.ietf.org/archive/id/draft-dkg-openpgp-1pa3pc-02.html) — IETF draft for consentful third-party certification distribution.
- [A Protocol for Solving Certificate Poisoning for the OpenPGP Keyserver Network](https://journals-sol.sbc.org.br/index.php/jisa/article/view/3810) — 2024 JISA article on first-party attested third-party certification.
- [OpenPGP ID Specification (u4/u5)](https://foopgp.org/blog/2026-04-28-openpgp-id-spec/) — foopgp.org draft for universal privacy-respecting identifiers.
- [NIP-51 — Lists](https://nips.nostr.com/51) — Nostr follow, mute, relay, bookmark, community, and curation lists.
- [NIP-85 — Trusted Assertions](https://nips.nostr.com/85) — signed computed metrics and trust assertions for users, events, addresses, and identifiers.
- [Nostr Protocol NIPs](https://github.com/nostr-protocol/nips) — canonical Nostr improvement proposals.

### Projects and implementations

- [nostr-wot/nostr-wot](https://github.com/nostr-wot/nostr-wot) — Nostr Web of Trust toolkit, SDK, oracle, and docs.
- [nostr-wot/nostr-wot-oracle](https://github.com/nostr-wot/nostr-wot-oracle) — global follow-graph indexer for pairwise distance queries.
- [nostr-wot/nostr-wot-extension](https://github.com/nostr-wot/nostr-wot-extension) — browser extension for Nostr signing, wallet, and WoT queries.
- [barrydeen/wot-relay](https://github.com/barrydeen/wot-relay) — relay that archives notes from a user's web of trust.
- [joelklabo/wot-scoring](https://github.com/joelklabo/wot-scoring) — PageRank-based Nostr scoring with NIP-85 event publication; live at wot.klabo.world.
- [CodyTseng/nostr-relay-plugin](https://github.com/CodyTseng/nostr-relay-plugin) — relay plugin monorepo including WoT Guard concepts.
- [dtonon/chronicle](https://github.com/dtonon/chronicle) — personal relay with Outbox model and WoT spam protection.
- [GnuPG](https://www.gnupg.org/) / [gpg/gnupg mirror](https://github.com/gpg/gnupg) — GNU Privacy Guard.
- [OpenPGP.js](https://github.com/openpgpjs/openpgpjs) — JavaScript OpenPGP implementation.
- [Mailvelope](https://github.com/mailvelope/mailvelope) — OpenPGP browser extension for webmail.
- [Sequoia-PGP](https://sequoia-pgp.org/) — Rust OpenPGP implementation.
- [Sequoia WoT specification](https://sequoia-pgp.gitlab.io/sequoia-wot/) — formal OpenPGP WoT specification and Rust reference implementation.
- [PGPainless](https://pgpainless.org/) / [pgpainless-wot](https://github.com/pgpainless/pgpainless-wot) — Java/Kotlin OpenPGP library with NLnet-funded WoT implementation.
- [keys.openpgp.org FAQ](https://keys.openpgp.org/about/faq/) — modern abuse-resistant keyserver design notes.
- [Keyoxide](https://keyoxide.org/) and [Keyoxide docs](https://docs.keyoxide.org/) — decentralized identity proof verification.

### Background reading

- [The Evolution of PGP's Web of Trust](https://www.mit.edu/~prz/docs/Beautiful_Security%20Chap7.pdf) — historical account by Phil Zimmermann and PGP context.
- [Linux Foundation: PGP Web of Trust, delegated trust and keyservers](https://www.linuxfoundation.org/blog/blog/pgp-web-of-trust-delegated-trust-and-keyservers) — practical explanation of trust signatures and delegation.
- [Webs of Trust: Choosing Who to Trust on the Internet](https://www.nortonlifelock.com/content/dam/nortonlifelock/pdfs/research-papers/2020-research-papers/webs-of-trust-choosing-who-to-trust-on-the-internet.pdf) — survey-style discussion of reputation, decentralization, privacy, and scalability trade-offs.
