---
title: "MLS (RFC 9420) and Wire"
slug: mls-wire
type: deep-dive
pillars: ["messaging"]
readiness: usable
description: "Messaging Layer Security (RFC 9420) brings efficient end-to-end encryption to large groups. How MLS works and how Wire deploys it in production."
dek: "Wire is a Swiss / German enterprise messenger that has, alongside Cisco Webex, served as the canonical reference deployment of MLS (Messaging Layer Security, RFC 9420). Founded 2012 by ex-Skype engineers, Wire shipped MLS in production starting 2022, ahead of the RFC's final publication in July 2023. The interesting object here is less Wire-the-company and more Wire-the-MLS-implementation: the place where MLS first met real-world enterprise scale."
updated: 2026-04-26
created: 2026-04-26
origin: vault
source: "07-Encrypted-Messaging/Wire MLS.md"
aliases: ["Wire", "Wire Swiss", "Wire MLS deployment"]
tags: ["wire", "mls", "rfc-9420", "treekem", "e2ee", "group-messaging", "enterprise", "deep-dive"]
---

## Why this file

Wire matters in this knowledge base for two reasons distinct from Wire-the-product:

1. **It is a working production deployment of MLS.** The RFC is abstract; Wire is the practical compass — the place to look when wondering "what does MLS actually look like with millions of group members across hundreds of organizations?"
2. **It demonstrates a different design lineage from Signal.** Wire was built independently of the Signal Protocol family. Its cryptography (Proteus, Wire's adapted Axolotl-style protocol) ran in parallel for a decade; the MLS migration is the convergence point.

For users picking a messenger, Wire is a credible enterprise option in EU regulatory environments. For protocol designers, Wire is the early-canon MLS reference.

## Brief company history

- **2012**: Wire Swiss GmbH founded in Zurich by Jonathan Christensen, Alan Duric, and Priidu Zilmer (former Skype). Initial focus: HD voice + chat for consumers.
- **2014-2017**: Consumer focus; E2EE rolled out (2016); apps for iOS, Android, web, desktop.
- **2018**: Pivot to enterprise / government. The Berlin office became the engineering center of gravity.
- **2018-2020**: ISO 27001, BSI C5, EU GDPR-compliant deployments. Customers in EU government, healthcare, defense.
- **2022**: First MLS production rollout. Wire publishes details in their CoreCrypto open-source library.
- **2023**: RFC 9420 final, July 2023. Wire's MLS implementation is one of the cited reference deployments.
- **2024-2026**: MLS is the default for new groups; legacy Proteus is deprecated (still supported for old conversations).

The honest framing: Wire is a commercial company with a focused enterprise market, not a privacy-NGO product. Its threat model is "EU regulator-friendly secure communications for organizations that don't want to use US-jurisdictional cloud," not "activists evading nation-state adversaries."

## What MLS is, briefly

MLS (Messaging Layer Security, RFC 9420) is the IETF standard for end-to-end encrypted group messaging. It generalizes Signal's per-pair Sender Keys to a group key agreement that scales **logarithmically in group size** rather than linearly.

Core MLS primitives:

- **Group state**: a tree of public keys (the **TreeKEM** ratchet tree) where each leaf is a group member's KeyPackage and internal nodes hold derived keys.
- **Commits**: a member proposes changes (add, remove, update) and produces a Commit message; group state advances atomically.
- **Welcome messages**: when a new member is added, they receive a Welcome containing the group state encrypted to their KeyPackage.
- **Application messages**: ordinary chat encrypted under the current epoch's key.

Properties:

- **Forward secrecy**: past group keys cannot be derived from current state.
- **Post-compromise security**: a compromised member key is recovered by the group's next ratchet update (Commit with an Update proposal).
- **Logarithmic add/remove cost**: O(log N) work per membership change instead of Signal's O(N).
- **Asynchronous**: members do not need to be online when changes happen.

For a primer on MLS layered over Nostr instead of an enterprise stack, see [Marmot Protocol](/kb/marmot-protocol/).

## Wire's MLS implementation

Wire's open-source CoreCrypto library ([github.com/wireapp/core-crypto](https://github.com/wireapp/core-crypto)) implements MLS in Rust, with bindings for Wire's mobile and desktop clients. It is distinct from OpenMLS ([github.com/openmls/openmls](https://github.com/openmls/openmls), the other major Rust MLS library), though there is significant cross-pollination of designs.

Key choices Wire made:

- **Credential type**: BasicCredentials with **X.509 certificate chains**. This integrates with enterprise PKI: the Credential identity is verified against a corporate CA. For consumer accounts it falls back to a BasicCredential with Ed25519 directly.
- **Ciphersuite**: MLS_128_DHKEMX25519_AES128GCM_SHA256_Ed25519 as default. Hybrid post-quantum ciphersuites being added 2024-2026 in line with the RFC's PQ work.
- **Server role**: the Wire backend is a **Delivery Service** that fans out Commits and application messages. It cannot read content. It enforces ordering and basic anti-replay.
- **Authentication Service**: Wire-operated CA for BasicCredentials in consumer use; client-supplied X.509 for enterprise.

The cryptographic model is RFC-compliant; Wire participated in the IETF MLS working group and contributed to drafts.

## Real-world MLS deployment lessons

The published Wire engineering writeups (and conference talks at Real World Crypto, IETF, and elsewhere) surface practical issues that the RFC alone leaves abstract:

- **KeyPackage management is operationally heavy.** Each device publishes prekey-style KeyPackages, which expire, need renewal, and must be available at any moment for asynchronous Adds. Mobile clients with intermittent connectivity stress this.
- **Group epoch contention.** When two members attempt simultaneous Commits, only one wins; the other has to retry. At scale (large groups, many concurrent admins) this causes ordering issues. Wire learned to optimize for low-contention groups.
- **Welcome message size.** Adding a member to a 1,000-person group requires a Welcome with significant state; clients must download and process it. Large enterprise groups exposed scaling issues that pure-protocol modeling didn't predict.
- **Federation across MLS domains** is, as of 2026, still being standardized. Wire to-Wire works; Wire-to-Webex doesn't yet. The RFC anticipates federation; the operational tooling lags.
- **Backwards compatibility** with Wire's earlier Proteus protocol. Old groups remain on Proteus until migrated; new groups default to MLS. Migration is not transparent for users.

These lessons are valuable to anyone planning an MLS deployment; they are why Wire and Cisco Webex matter as canonical references rather than just product placements.

## How Wire differs from Signal lineage

| Property | Wire (Proteus then MLS) | Signal |
|----------|--------------------------|--------|
| Initial protocol | Proteus (Axolotl-derived; 2014) | Signal Protocol / Double Ratchet (2014) |
| Group encryption (originally) | Per-pair Proteus | Sender Keys |
| Group encryption (current) | MLS (RFC 9420) | Sender Keys still primary; MLS exploration |
| Identity | Email address (consumer), X.509 (enterprise) | Phone number; usernames (2024+) |
| Multi-device | First-class from launch | Linked devices via Sesame |
| Voice/video | First-class (Skype lineage) | Via Signal calling stack |
| Hosting model | EU clouds (Frankfurt, mostly) | Signal Foundation infrastructure |
| Federation | None (Wire is a single network) | None (Signal is a single network) |
| Open-source | Server and clients open-source (AGPL/GPL) | Server open, network closed |

The shared part: both are Signal-quality E2EE messengers with multi-device support and forward secrecy. The differences are jurisdictional posture (EU enterprise vs US foundation), funding (commercial vs nonprofit), and protocol family (MLS-first vs Sender-Keys-first).

For protocol designers, Wire's MLS work is a parallel reference to Signal's PQXDH work — both are how to extend a 2014-era E2EE design into the 2025+ era.

## Threat model

What Wire MLS provides:

- **Group E2EE with logarithmic membership-change cost.** Useful for organizations with hundreds of members in some channels.
- **Forward secrecy and post-compromise security at group level.**
- **Server cannot read content.** The Delivery Service sees ciphertext + envelope metadata.
- **EU-data-residency by default.** Wire's enterprise tier offers Frankfurt and German cloud regions; for some customers Wire is on-premise.

What it doesn't:

- **Wire is a centralized network.** No federation, no self-host of the network at the protocol layer (enterprise on-prem deployments exist but are isolated networks).
- **Server-side metadata.** Like Signal, Wire's server sees who-talks-to-whom for Delivery Service routing. MLS does not standardize sealed-sender-style metadata reduction.
- **Endpoint compromise.** Same as everywhere.
- **Jurisdictional pressure.** Wire is a Swiss / German company subject to EU and Swiss law. The legal regime is friendly to E2EE compared to many alternatives, but Wire is not a no-jurisdiction project.

The honest enterprise threat model: Wire is the right answer if you're a European hospital, government agency, or NGO that wants better than Microsoft Teams without the operational nightmare of self-hosting Matrix. It is not the right answer for activists in repressive states (use [Briar](/kb/briar/), [SimpleX](/kb/simplex/), [Cwtch](/kb/cwtch/)).

## Deployment scale

Wire's published numbers are commercial and somewhat opaque:

- Estimated **500K-1M paid seats** in 2025-2026 across enterprise and government customers.
- Notable customers: German federal IT (BWI, "Bundeswehr-IT"), various EU institutions, healthcare networks.
- Public free tier exists but has been deprioritized over time; consumer use is much smaller.

These numbers put Wire well below Signal in absolute users but well above niche messengers in revenue per user and in deployment scale within the enterprise category.

## Place in the MLS ecosystem

As of 2026 the MLS production deployments include:

- **Wire** — first major rollout, 2022.
- **Cisco Webex** — large-scale rollout, 2023-2024 (Webex was a major contributor to RFC 9420).
- **Google** — RCS / Messages have been planning MLS migration; partial rollout in 2024-2025.
- **Discord** — investigating MLS for E2EE DMs (announcements 2024).
- **Matrix** — MLS profile under development and pre-scale; see [Matrix and E2EE](/kb/matrix/).
- **Marmot** — MLS over Nostr ([Marmot Protocol](/kb/marmot-protocol/)).
- **Session** — MLS-style group migration in progress ([Session](/kb/session-messenger/)).

Wire is "the place where MLS first ran in anger" and is the implementation other adopters compare against.

## Primary sources

- RFC 9420, "The Messaging Layer Security (MLS) Protocol" (Barnes, Beurdouche, Robert, Millican, Omara, Cohn-Gordon; July 2023). [datatracker.ietf.org/doc/rfc9420](https://datatracker.ietf.org/doc/rfc9420).
- RFC 9419, "Architecture for MLS" (March 2024).
- Wire CoreCrypto — [github.com/wireapp/core-crypto](https://github.com/wireapp/core-crypto).
- Wire server source — [github.com/wireapp/wire-server](https://github.com/wireapp/wire-server).
- Wire whitepaper, "Wire Security Whitepaper" — [wire.com/en/security](https://wire.com/en/security).
- Beurdouche et al., "TreeKEM: Asynchronous Decentralized Key Management for Large Dynamic Groups" — the academic basis for MLS group key agreement.
- Cohn-Gordon et al., "On Ends-to-Ends Encryption: Asynchronous Group Messaging with Strong Security Guarantees" (CCS 2018) — foundational paper.
- OpenMLS (alternative implementation) — [github.com/openmls/openmls](https://github.com/openmls/openmls).
- Real World Crypto talks (2022-2024) by Wire and Cisco engineers on production MLS deployment lessons.
