---
title: "The OpenPGP Web of Trust"
slug: openpgp-web-of-trust
type: deep-dive
pillars: ["identity", "cryptography"]
readiness: battle-tested
description: "The OpenPGP Web of Trust, the original decentralized trust model: key signing, trust levels, keyservers, and why it struggled at scale."
dek: "The OpenPGP Web of Trust is the classic decentralized trust model: instead of accepting a certificate because a browser-vendor root CA says so, a user accepts a public key because it has a path through people they personally trust as introducers."
updated: 2026-08-06
created: 2026-05-07
origin: vault
source: "02-Cryptography/OpenPGP Web of Trust.md"
aliases: ["GPG Web of Trust", "PGP Web of Trust", "OpenPGP WoT"]
tags: ["openpgp", "gpg", "web-of-trust", "keyserver", "certificate-poisoning", "identity"]
---

## Summary

The OpenPGP Web of Trust is the classic decentralized trust model: instead of accepting a certificate because a browser-vendor root CA says so, a user accepts a public key because it has a path through people they personally trust as introducers. It is the historical ancestor of many modern freedom-tech reputation systems, including [Nostr Web of Trust](/kb/nostr-web-of-trust/), but it solves a narrower problem: **is this OpenPGP certificate valid for this identity?**

OpenPGP WoT separates three ideas that are often conflated:

1. **Certificate validity** — does this key belong to the named user ID?
2. **Ownertrust / introducer trust** — do I trust this certificate holder to certify other people's keys correctly?
3. **Operational trust** — do I trust this person, project, or organization in a broader social sense?

Only the first two are part of the traditional OpenPGP trust computation. A signature on a key is evidence about a key/name binding; it is not a universal moral endorsement. This distinction is essential when importing WoT ideas into [Overview - Identity & Pseudonymity](/kb/identity-and-pseudonymity/), decentralized marketplaces, and Nostr reputation systems.

## Late-May 2026 Developments

### PGPainless WoT Module (NLnet/NGI Assure Funded)

The PGPainless project ([pgpainless.org](https://pgpainless.org/), [github.com/pgpainless/pgpainless-wot](https://github.com/pgpainless/pgpainless-wot)) continues active development of a Java/Kotlin WoT path computation module, funded through NGI Assure / NLnet. The module is based on Sequoia-PGP's published formal WoT specification and includes test vectors from the [wot-test-suite](https://github.com/pgpainless/pgpainless-wot/tree/main/wot-test-suite). For the Android email tool ecosystem and server-side Java workflows, this fills a tooling gap that has existed for years — Java OpenPGP libraries have historically omitted WoT path computation entirely.

### OpenPGP ID u4/u5 Specification (IETF Draft, Djibian OS Production Use)

A new specification from foopgp.org ([blog post April 2026](https://foopgp.org/blog/2026-04-28-openpgp-id-spec/), [Codeberg spec](https://codeberg.org/foopgp/foopgp-hugowebsite/src/branch/public/public/documents/en/draft-foopgp-openpgp-id-00.txt)) introduces two privacy-respecting universal identifiers derived from civil-registry-style data:

- **u4 (human identifier):** derived from last birth surname + first and second given names + date of birth, processed through MD5 and Base64url encoding. Produces a 39-character identifier that fits in an OpenPGP UID comment field. Pseudonymous — without the exact input data, the individual cannot be identified, but the identifier is permanent across marriage, name change, or naturalisation.

- **u5 (universal identifier for anything):** Unix timestamp + geographic coordinates, identifying any entity by its moment and place of origin. Used for AI agents, software components, or humans who prefer not to disclose civil data.

For WoT purposes, u4/u5 represents an attempt to build persistent pseudonymous identity on OpenPGP certificates without a central registry. The spec has been submitted to IETF and is in production use in Djibian OS. The privacy argument rests on the collision difficulty of the derived identifier and the WoT certification fabric as the real verification barrier.

### OpenPGP Key Replacement (draft-ietf-openpgp-replacementkey-07, April 2026)

The IETF active draft specifies a machine-readable mechanism for OpenPGP users to signal that a new key should replace an expired, revoked, or superseded one. The draft (26 pages plus appendices) defines replacement key signalling — when a user publishes a new primary key, they can include a signed signal pointing to the replacement. Users who receive the old key see a machine-readable hint about where to find the successor.

For WoT continuity, this matters: long-lived OpenPGP identities need key rotation paths, and a replacement signal lets the WoT carry trust forward to a new key without requiring re-verification from all prior certifiers. This is not automatic recovery — the user must publish the replacement — but it makes the transition legible to clients and reduces the probability that old-key communications silently fail after rotation. The draft expires October 2026 and is being actively developed.

### draft-gallagher-openpgp-signatures-03 (June 2026)

[draft-gallagher-openpgp-signatures-03](https://datatracker.ietf.org/doc/html/draft-gallagher-openpgp-signatures-03) is an active IETF draft (published June 2026) that specifies several updates and clarifications to the grammar and semantics of OpenPGP signatures. This is a maintenance-level update to RFC 9580, addressing edge cases in signature encoding and semantics that have accumulated since the RFC was published. For WoT implementations, the draft matters because signature validity decisions depend on correct grammar and semantic interpretation — ambiguities in signature processing are exactly the class of bugs that cause valid certifications to be rejected or invalid ones accepted. The draft is in the individual submission track, not yet adopted by a working group.

### OpenPGP message and HKP developments

Two additional IETF drafts deserve tracking:

- [draft-gallagher-openpgp-messages-00](https://datatracker.ietf.org/doc/html/draft-gallagher-openpgp-messages-00) — updates and clarifications to OpenPGP message grammar, complementary to the signatures draft above.
- A new draft on the OpenPGP HTTP Keyserver Protocol (HKP) addressing v6 certificate handling, v2 key lookup, and content-type requirements for ASCII-armored certificate bundles. These HKP changes affect how WoT-compatible key discovery works at the transport layer.

These drafts collectively represent active maintenance of the OpenPGP ecosystem beyond the RFC 9580 baseline, which is notable given that OpenPGP development was relatively quiet after 2020.

## Historical context

### PGP and decentralized certification

Phil Zimmermann released PGP in 1991 as a civil-liberties response to centralized control over strong cryptography. The Web of Trust matched that ethos: each user could verify fingerprints out-of-band, sign keys, and decide which friends were reliable introducers. A certification path might make a key valid if enough trusted introducers signed it.

This model differed sharply from X.509:

| Model | Trust root | User control | Failure mode |
|---|---|---|---|
| X.509 CA | Browser/OS root store | Low; roots are shipped by vendors | Compromised/misbehaving CA can issue for anyone. |
| OpenPGP WoT | User's local trusted keys | High; ownertrust is local | Hard UX, sparse graph, stale signatures. |
| TOFU | First-seen key | Medium; local pinning | First contact can be intercepted. |
| WKD / domain discovery | Domain control | Medium; domain admin controls mapping | Domain/DNS/TLS compromise or central hosting risk. |

OpenPGP standardized message and certificate formats. The current standard is [RFC 9580](https://www.rfc-editor.org/rfc/rfc9580.html), published in July 2024, replacing RFC 4880 and related older OpenPGP RFCs. RFC 9580 modernizes the format with v6 keys, AEAD containers, Argon2 S2K, and mandatory Ed25519/X25519 support, but it does not make WoT usability magically easy.

### Key-signing parties and trust databases

Classic practice involved key-signing parties: people met physically, checked fingerprints and identity documents or known-person context, and later signed each other's certificates. GnuPG maintained a local trust database. Users marked keys as fully trusted, marginally trusted, never trusted, or unknown as introducers.

A relying party could accept a target certificate if, for example, it was signed by one fully trusted introducer or several marginal introducers. Exact thresholds are local policy.

### SKS keyserver collapse and certificate poisoning

The old SKS keyserver pool was append-only and aggressively synchronized. That made key distribution resilient, but it created a fatal abuse surface: anyone could attach arbitrary third-party certifications or identity packets to someone else's certificate, and the network would preserve and redistribute them.

In 2019, certificate poisoning attacks attached huge numbers of signatures to prominent certificates, making them too large or slow for tools to handle. The lesson is bigger than OpenPGP: **decentralized append-only identity objects need consent and garbage collection**. If third parties can permanently mutate your identity record, adversaries will weaponize that capability.

Modern OpenPGP discovery therefore shifted toward narrower and more consentful mechanisms:

- **Web Key Directory (WKD)** — fetch a key from a domain-controlled `.well-known` path associated with an email address.
- **keys.openpgp.org** — centralized, abuse-resistant key discovery; verifies email addresses and does not distribute third-party certifications by default.
- **First-party approved / attested third-party certifications** — distribute third-party certifications only when the certificate holder approves them.
- **Keyoxide / Ariadne proofs** — cross-link cryptographic identities and online accounts through bidirectional proofs.

## Modern standards and protocols

### RFC 9580 — OpenPGP

[RFC 9580](https://www.rfc-editor.org/rfc/rfc9580.html) is the current OpenPGP standard. For WoT purposes, its importance is not that it changes social trust policy, but that it gives modern implementations a cleaner cryptographic substrate: v6 keys, stronger algorithm guidance, AEAD, Argon2, and required modern curves.

### First-party approved third-party certifications

The [IETF draft on First-Party Approved Third-Party Certifications](https://www.ietf.org/archive/id/draft-dkg-openpgp-1pa3pc-02.html) addresses the certificate-bloat / poisoning problem directly. It defines a certification-approval mechanism where the certificate owner explicitly approves selected third-party certifications. Relying parties can prune unapproved certifications rather than accepting all arbitrary additions.

A 2024 Journal of Internet Services and Applications article, ["A Protocol for Solving Certificate Poisoning for the OpenPGP Keyserver Network"](https://journals-sol.sbc.org.br/index.php/jisa/article/view/3810), discusses this pattern as a protocol modification that avoids the worst effects of poisoning without requiring all installed clients to be replaced immediately. Search metadata identifies the authors as Gunnar Wolf and Ortega-Arjona and DOI `10.5753/jisa.2024.3810`.

### keys.openpgp.org

[keys.openpgp.org](https://keys.openpgp.org/about/faq/) is not a pure decentralized keyserver pool. It is a deliberate retreat from SKS-style federation toward abuse resistance:

- email addresses must be verified before they are distributed;
- only one verified key per email address is visible at a time;
- third-party certifications are not distributed by default;
- users can delete their own keys / identities.

From a cypherpunk perspective, this is a compromise: less decentralized, but dramatically more survivable against hostile certificate mutation.

### Web Key Directory and DANE

WKD gives email-like identities a domain-based discovery path. DANE/OpenPGPKEY records (RFC 7929) can bind OpenPGP keys through DNSSEC. These systems lean on [Overview - Decentralized DNS](/kb/decentralized-dns/) questions: who controls the domain, how robust is DNSSEC, and can censorship-resistant naming systems provide equivalent discovery?

### Keyoxide and Ariadne

[Keyoxide](https://keyoxide.org/) and the [Ariadne Identity Specification](https://ariadne.id/core/0/) are adjacent to WoT. They do not decide whether someone is trustworthy. They verify that a cryptographic identity and external accounts point to each other.

Ariadne's draft flow is bidirectional:

1. fetch a cryptographically secured profile or OpenPGP key;
2. read identity claims such as `proof@ariadne.id=https://domain.tld`;
3. fetch the claimed location;
4. verify that the location links back to the cryptographic fingerprint or identifier.

This supports pseudonymous identity bundles: a user can prove control over a website, GitHub account, Fediverse profile, or other service without relying on Keybase-style central hosting or blockchain identity.

## Implementations and ecosystem

| Project | Role | Maturity / activity | Notes |
|---|---|---|---|
| [GnuPG](https://www.gnupg.org/) / [gpg/gnupg mirror](https://github.com/gpg/gnupg) | Reference CLI/agent ecosystem with local trust database | Mature / active; GitHub mirror 919 stars, pushed 2026-05-06; canonical development is not GitHub PRs | Cultural reference implementation for ownertrust, certification, trust signatures, and local validity. |
| [Sequoia-PGP](https://sequoia-pgp.org/) | Rust OpenPGP implementation/toolkit | Mature / active ecosystem | Modern implementation used for tooling and libraries; useful when building new OpenPGP workflows. |
| [OpenPGP.js](https://github.com/openpgpjs/openpgpjs) | JavaScript OpenPGP library | Mature / active; 5,949 stars, 821 forks, pushed 2026-05-02 | Browser and Node.js OpenPGP implementation; library-level building block more than full WoT UX. |
| [Mailvelope](https://github.com/mailvelope/mailvelope) | Browser extension for webmail OpenPGP | Mature / active; 1,825 stars, 222 forks, pushed 2026-05-05 | Practical OpenPGP deployment in webmail; trust UX remains hard for mainstream users. |
| [PGPainless](https://pgpainless.org/) | Java OpenPGP library | Active | Developer-friendly OpenPGP tooling. |
| [keys.openpgp.org](https://keys.openpgp.org/about/faq/) | Abuse-resistant key discovery | Production | Central service designed to avoid SKS poisoning dynamics. |
| [Keyoxide](https://keyoxide.org/) / [docs](https://docs.keyoxide.org/) | Decentralized identity proof verification | Active community / open source | Bidirectional account-control proofs; privacy-friendly, non-blockchain. |
| [Ariadne Identity](https://ariadne.id/core/0/) | Specification behind Keyoxide-style proofs | Draft; v0 says not recommended for implementations | Useful conceptual model: cryptographic profile + identity claims + public proofs. |

## Use cases

### Encrypting email or files to the right key

The core OpenPGP problem is binary: should I encrypt this message to this certificate? WoT can help when the target key has a path through trusted introducers. In practice, many users now combine fingerprint pinning, WKD, keys.openpgp.org, and TOFU because full WoT management is too complex.

### Software release verification

Open-source maintainers sign releases. Distributions and users pin maintainer keys. A WoT path can provide additional evidence that a signing key belongs to a maintainer, but it should be combined with reproducible builds, checksums, transparency logs where available, and project-controlled release channels.

### Pseudonymous proof bundles

Keyoxide/Ariadne-style proofs let a pseudonym prove control over accounts and domains. This is not reputation by itself, but it provides stable identity continuity for [Overview - Identity & Pseudonymity](/kb/identity-and-pseudonymity/) without forcing legal-name verification.

### Key transition and continuity

If a key is rotated, the old key can sign the new key, trusted peers can certify the transition, and profiles can update cross-links. WoT does not create a universal recovery desk, but it supplies social evidence around continuity.

## Trade-offs

| Strength | Explanation |
|---|---|
| User-chosen roots | No universal CA decides every trust relationship. |
| Offline/social verification | Fingerprints can be checked in person or out of band. |
| Pseudonym-compatible | Keys and proofs can represent personas without legal identity. |
| Durable cultural model | OpenPGP taught the freedom-tech ecosystem to separate local trust from institutional authority. |

| Limitation | Explanation |
|---|---|
| UX burden | Most users do not want to manage ownertrust, certification paths, and revocations manually. |
| Sparse graph | Many users have no meaningful key-signing paths. |
| Stale signatures | Old certifications may outlive relationships or compromises. |
| Keyserver abuse | SKS showed that append-only third-party mutation is dangerous. |
| Ambiguous semantics | A certification means key/name verification, not broad endorsement. |
| Discovery centralization | Modern abuse-resistant discovery often leans on domains or centralized services. |

## Evidence at a glance

|| Evidence | Source | Strength | What it shows ||
|---|---|---|---|
| OpenPGP standard | [RFC 9580](https://www.rfc-editor.org/rfc/rfc9580.html) | Current IETF standard | Modern OpenPGP format and cryptographic baseline. |
| GnuPG | [gnupg.org](https://www.gnupg.org/) / [GitHub mirror](https://github.com/gpg/gnupg) | Mature production software | Local trust database and OpenPGP operational tooling remain active. |
| Certificate poisoning article | [JISA article](https://journals-sol.sbc.org.br/index.php/jisa/article/view/3810) | 2024 peer-reviewed/academic source | SKS-style poisoning is a real protocol/ecosystem failure; first-party attestation is a proposed mitigation. |
| 1PA3PC draft | [IETF archive draft](https://www.ietf.org/archive/id/draft-dkg-openpgp-1pa3pc-02.html) | Protocol draft | Certificate holders can explicitly approve third-party certifications for pruning. |
| keys.openpgp.org FAQ | [FAQ](https://keys.openpgp.org/about/faq/) | Production operator documentation | Modern key discovery chooses abuse resistance over open keyserver federation. |
| Ariadne spec | [ariadne.id](https://ariadne.id/core/0/) | Draft specification | Bidirectional cryptographic identity proofs for OpenPGP/minisign profiles. |
| Keyoxide docs | [FAQ](https://docs.keyoxide.org/wiki/faq/) | Project documentation | Practical privacy-friendly identity proofs that users can verify manually. |
| OpenPGP Key Replacement | [draft-ietf-openpgp-replacementkey-07](https://datatracker.ietf.org/doc/draft-ietf-openpgp-replacementkey/) | Active IETF draft (April 2026) | Machine-readable key migration signalling for WoT continuity; expires October 2026. |
| OpenPGP ID (u4/u5) | [foopgp.org spec](https://foopgp.org/blog/2026-04-28-openpgp-id-spec/) | Early / in production (Djibian) | Privacy-respecting pseudonymous identifiers derived from civil registry data. |
| OpenPGP Signatures draft | [draft-gallagher-openpgp-signatures-03](https://datatracker.ietf.org/doc/html/draft-gallagher-openpgp-signatures-03) | Active IETF draft (June 2026) | Grammar and semantics clarifications for OpenPGP signatures; maintenance of RFC 9580. |
| OpenPGP Messages draft | [draft-gallagher-openpgp-messages-00](https://datatracker.ietf.org/doc/html/draft-gallagher-openpgp-messages-00) | Early IETF draft | Complementary message grammar updates to RFC 9580. |
| Hermine threshold signatures | [eprint 2026/419](https://eprint.iacr.org/2026/419), [hermine-th.org](https://hermine-th.org) | Research / PQ | Post-quantum FROST-like threshold signatures on standard lattice assumptions; PQ migration path for Frostr. |
| FROST NIST submission | [MPTS 2026 preview](https://csrc.nist.gov/csrc/media/Projects/threshold-cryptography/documents/TCall-1/FROST-PW01.pdf) | Active NIST Threshold Call | FROST submitted for NIST standardization; adaptive security results presented at MPTS 2026. |

## June 11, 2026 — The OpenPGP Schism: LibrePGP v5 vs RFC 9580

The most significant development since the May 24 update is the full crystallization of the OpenPGP standard split. This is not a version-number disagreement — it is a governance fracture that directly fragments the certificate universe on which OpenPGP WoT depends.

### The Two Competing Standards

**RFC 9580 (IETF "v6" OpenPGP)** — the official IETF proposed standard, produced through a multi-year IETF OpenPGP Working Group process. Key implementations:
- Sequoia-PGP v2 (March 2025) — RFC 9580 v6 support
- OpenPGP.js v6 (November 2024) — RFC 9580 v6 support  
- Proton Mail — production email integration

RFC 9580 became a draft standard in March 2025 when two independent interoperable implementations confirmed compliance. It obsoletes RFC 4880/5581/6637, introduces v6 keys, AEAD containers, Argon2 S2K, and mandatory Ed25519/X25519.

**LibrePGP (GnuPG "v5")** — GnuPG maintainer Werner Koch's competing proposal, which critics describe as a fork from a pre-RFC9580 draft. GnuPG's website (as of 2026) still describes itself as implementing "RFC 4880," explicitly avoiding RFC 9580. The IETF OpenPGP Working Group did not adopt LibrePGP.

### GnuPG 2.5.20 (May 13, 2026)

Werner Koch's release announcement for GnuPG 2.5.20 is the key event:

- Introduces Kyber/ML-KEM (FIPS 203) as a post-quantum encryption algorithm in the 2.5 series
- Adds GCM encryption to `gpgsm`
- Warns that the 2.4 series approaches end-of-life
- **Critically: implements LibrePGP v5 features, not RFC 9580 v6**

The release notes do not mention RFC 9580 compatibility. This matters enormously: GnuPG is the dominant OpenPGP implementation in GNU/Linux distributions, package managers (`apt`, `dpkg`, `rpm`), server-side PGP tooling, and Git commit signing. If GnuPG implements a different standard than Sequoia/OpenPGP.js, the two ecosystems can no longer process each other's certificates.

### Why This Fractures the OpenPGP WoT

The OpenPGP Web of Trust requires shared certificate formats and signature semantics. When GnuPG and Sequoia/OpenPGP.js diverge:

1. **Cross-signing breaks** — certifications made by GnuPG keys may not parse correctly by RFC 9580 implementations, and vice versa
2. **Key validation paths break** — WoT path-finding depends on being able to read and verify signatures across the graph
3. **Keyserver responses fragment** — v6 keys returned by keyservers may not be readable by GnuPG
4. **The trust graph literally cannot connect** — keys from the GnuPG/LibrePGP universe cannot certify keys from the RFC 9580 universe

The practical freedom-tech risk: if you sign someone's GnuPG key today using your RFC 9580-compatible implementation, that certification may not be readable or interpretable by GnuPG users in a year.

### Two New Gallagher IETF Drafts (June 2026)

Andrew Gallagher published two complementary OpenPGP maintenance drafts in June 2026:

1. **[draft-gallagher-openpgp-signatures-03](https://datatracker.ietf.org/doc/draft-gallagher-openpgp-signatures/)** — "OpenPGP Signatures." Clarifies grammar and semantics for signature packets, third-party signatures, notary signatures (Type 40 — "a signature of a signature, as a notary seal"), and certification signatures. Expires December 2026.

2. **[draft-gallagher-openpgp-messages-00](https://datatracker.ietf.org/doc/draft-gallagher-openpgp-messages/)** — "OpenPGP Message Grammar." Clarifies One-Pass Signature packet semantics and message structure. Expires December 2026.

3. **OpenPGP HTTP Keyserver Protocol** (draft-gallagher-openpgp-hkp-andrewgdotcom) — specifies v6 key handling for keyservers: v6 certificates MUST NOT be returned for legacy machine-readable requests, but MAY be returned for human-readable requests. Also specifies v2 lookup using `by-keyid` and `by-vfingerprint` categories.

These drafts are IETF-side maintenance of RFC 9580 and independent of the GnuPG/LibrePGP split.

### Mitigation: First-Party Approved Certifications Become More Critical

The certificate poisoning lesson from SKS keyservers (see ) applies even more now. If cross-signing between LibrePGP and RFC 9580 implementations becomes unreliable, the WoT value of third-party certifications degrades. First-party approved third-party certifications (draft-dkg-openpgp-1pa3pc) become the safe path: only certifications explicitly approved by the certificate holder travel with the certificate, reducing attack surface from both poisoning and cross-standard fragmentation.

### What This Means for Freedom-Tech Deployments

For deployments relying on OpenPGP certifications:

1. **Be aware of which standard your keys use.** GnuPG 2.5.x generated keys may be LibrePGP v5 format. OpenPGP.js v6 and Sequoia-PGP v2 generate RFC 9580 v6 keys.
2. **Do not assume cross-compatibility.** Test your certifications against both ecosystems.
3. **Watch for GnuPG 2.6** — Koch's announcement says 2.6 "will not differ a lot from 2.4" except for PQC support and internal library changes, which may indicate continued LibrePGP direction rather than RFC 9580 adoption.
4. **The IETF has one standard (RFC 9580). GnuPG implements another (LibrePGP).** This is not a normal version difference — it is a fork with no obvious merge path.

## Design lessons for newer WoT systems

1. **Do not let third parties permanently mutate identity objects without consent.** SKS poisoning is the canonical failure.
2. **Separate key validity from social reputation.** A person can verify a key correctly while being untrusted in another context.
3. **Expose trust paths and local policy.** Hidden defaults become centralized authority.
4. **Plan revocation and expiry.** Trust edges decay; keys are lost or compromised.
5. **Prefer consentful distribution.** First-party approved certifications and self-published proofs are safer than arbitrary append-only attachments.
6. **Keep manual verification possible.** Keyoxide's strongest claim is that it automates something users can inspect themselves.

## June 18, 2026 Update — RFC 9980 PQC, HKP draft, GnuPG 2.4 EOL

### RFC 9980 — Post-Quantum Cryptography in OpenPGP Assigned

The OpenPGP standard page now lists **RFC 9980: Post-Quantum Cryptography in OpenPGP** alongside RFC 9580. This is the first new RFC number on the OpenPGP standards page since 2024, and the structural answer to the question every WoT operator eventually has to face: what happens to certifications signed with classical algorithms when quantum computers become capable of breaking RSA-2048 and Ed25519?

The IETF datatracker history for [draft-ietf-openpgp-pqc](https://datatracker.ietf.org/doc/draft-ietf-openpgp-pqc/history) shows the document entered the RFC Editor queue on **January 6, 2026** (version 17), and per [IANA's 2026 IETF draft status](https://www.iana.org/performance/ietf-draft-status/2026) is currently in **RFC-Ed-ACK** state. The standard carries forward the existing RFC 9580 format and adds PQ algorithm support — ML-KEM (Kyber, FIPS 203) for encryption, ML-DSA and SLH-DSA for signatures.

**WoT implications:**

- **Long-term cert verifiability.** Certifications and signatures issued today using Ed25519 or RSA can be migrated forward to ML-DSA without breaking the existing trust graph — assuming both signers and verifiers support RFC 9980.
- **Composite signatures during transition.** [draft-ietf-openpgp-nist-bp-comp-03](https://datatracker.ietf.org/doc/draft-ietf-openpgp-nist-bp-comp/) (93 pages, January 8, 2026) defines composite signatures combining classical (NIST/Brainpool) and post-quantum algorithms, so certifiers can sign in a way that both classical and PQ verifiers can validate.
- **Cross-implementation fracture.** GnuPG 2.5.20 (May 13, 2026) implemented Kyber/ML-KEM as part of LibrePGP v5, **not** RFC 9980. Until GnuPG aligns with the IETF standard, a certifier signing with one tool may produce a signature that the other tool cannot verify — the same WoT fragmentation already flagged in the June 11 update.

### New and Updated IETF Drafts (May–June 2026)

The OpenPGP working group [drafts listing](https://datatracker.ietf.org/wg/openpgp) shows unusually heavy activity in the last month:

- **[draft-ietf-openpgp-replacementkey-08](https://datatracker.ietf.org/doc/draft-ietf-openpgp-replacementkey/)** — May 29, 2026, 31 pages. One month after the -07 covered in the June 11 update. Approaching IETF last call. This is the draft that lets long-lived OpenPGP identities signal key rotation without breaking the existing trust graph.
- **[draft-ietf-openpgp-hkp-01](https://datatracker.ietf.org/doc/draft-ietf-openpgp-hkp/)** — June 5, 2026, 51 pages. New IETF working group document codifying how keyservers handle v6 certificates. Defines v1 (legacy HKP) and v2 (with `by-keyid`, `by-vfingerprint` categories) lookup endpoints, with explicit guidance: v6 keys must NOT be returned for legacy machine-readable requests but MAY be returned for human-readable requests. This is the first IETF-standardized HTTP keyserver protocol since the SKS era, and it codifies the consentful-certification lessons from keys.openpgp.org.
- **[draft-ietf-openpgp-nist-bp-comp-03](https://datatracker.ietf.org/doc/draft-ietf-openpgp-nist-bp-comp/)** — January 8, 2026, 93 pages. Composite NIST + Brainpool PQ/T schemes.
- **Three Andrew Gallagher drafts, all dated June 4, 2026:**
  - [draft-gallagher-openpgp-certificates-00](https://datatracker.ietf.org/doc/draft-gallagher-openpgp-certificates/) — 25 pages, OpenPGP Certificate Grammar
  - [draft-gallagher-openpgp-messages-00](https://datatracker.ietf.org/doc/draft-gallagher-openpgp-messages/) — 9 pages, OpenPGP Message Grammar
  - [draft-gallagher-openpgp-signatures-03](https://datatracker.ietf.org/doc/draft-gallagher-openpgp-signatures/) — 25 pages, OpenPGP Signatures v03

The Gallagher cluster represents foundational maintenance of the certificate, signature, and message grammar. The grammars are the substrate the WoT walks; clarifying them reduces the ambiguity that has historically allowed certificate poisoning to succeed.

### GnuPG 2.4 End-of-Life Warning (June 2026)

Per the LWN article [Fedora and GPG 2.5](https://lwn.net/Articles/1055053), **GnuPG 2.4 reaches end-of-life in June 2026**. This means Linux distributions must move to GnuPG 2.5 (which implements LibrePGP v5, not RFC 9580) or fork the 2.4 series themselves. For the OpenPGP WoT:

- Distributions that adopt GnuPG 2.5 will continue to operate on LibrePGP v5 certificates.
- Distributions that fork 2.4 will retain RFC 9580 interoperability.
- The two camps may diverge further as RFC 9980 ships — GnuPG 2.5 may track LibrePGP rather than RFC 9980, leaving distributions to choose between RFC standardisation and the dominant CLI implementation.

The gnupg.org home page continues to describe GnuPG as implementing "RFC 4880," which is now two RFCs out of date.

### Practical Guidance for OpenPGP WoT Operators (Updated)

Given the RFC 9980 publication path and the LibrePGP fracture:

1. **If you run a high-assurance OpenPGP identity today:** generate keys with classical algorithms (Ed25519/X25519 are fine) but understand that long-term verification will require migration to ML-DSA once GnuPG and Sequoia converge on a unified PQC profile. RFC 9980 + RFC 9580 is the IETF-aligned migration target; LibrePGP v5 is the GnuPG-aligned target.
2. **If you sign third-party certifications:** sign with classical algorithms for now, but consider also issuing composite signatures (NIST-Brainpool PQ/T) when [draft-ietf-openpgp-nist-bp-comp-03](https://datatracker.ietf.org/doc/draft-ietf-openpgp-nist-bp-comp/) stabilises — this gives verifiers on either side of the algorithmic split a usable path.
3. **If you operate a keyserver:** adopt [draft-ietf-openpgp-hkp-01](https://datatracker.ietf.org/doc/draft-ietf-openpgp-hkp/) handling of v6 keys (return only for human-readable requests) and the v2 lookup categories (`by-keyid`, `by-vfingerprint`) to prepare for the post-RFC-9980 era.
4. **If you plan key rotation:** use [draft-ietf-openpgp-replacementkey-08](https://datatracker.ietf.org/doc/draft-ietf-openpgp-replacementkey/) to publish machine-readable replacement signals; clients and keyservers that support the draft can migrate trust paths automatically.
5. **Track the GnuPG vs Sequoia vs OpenPGP.js split.** RFC 9580 is now nearly two years old (July 2024); the existence of two competing implementations after that long suggests the schism is structural rather than transitional.

### Updated GitHub Activity — June 18, 2026

| Project | Stars | Last push | Notes |
|---------|------:|-----------|-------|
| [gpg/gnupg](https://github.com/gpg/gnupg) | 949 | 2026-06-17 | GnuPG 2.5.20 stable, 2.4 EOL warning |
| [openpgpjs/openpgpjs](https://github.com/openpgpjs/openpgpjs) | 5,956 | 2026-06-17 | RFC 9580 production |
| [sequoia-pgp/sequoia](https://gitlab.com/sequoia-pgp/sequoia) | n/a | n/a | Rust OpenPGP, RFC 9580 |
| [pgpainless/pgpainless-wot](https://github.com/pgpainless/pgpainless-wot) | 0 | 2026-04-28 | NLnet-funded WoT module, no recent commits |
| [Sequoia WoT spec](https://sequoia-pgp.gitlab.io/sequoia-wot/) | n/a | n/a | Formal WoT specification |

**Key observation:** PGPainless WoT has not seen new commits since April 28, 2026 — the longest quiet period since the NLnet-funded project began. Worth monitoring; if no further commits appear before July 2026, this may indicate the funded development phase is concluding without a stable 1.0.

## August 6, 2026 Update — RFC 9980 Published, GnuPG 2.5.21, 2.4 EOL, Sequoia sq 1.4.0

### RFC 9980 — Post-Quantum Cryptography in OpenPGP (Published June 2026)

[RFC 9980](https://datatracker.ietf.org/doc/rfc9980) was published as an IETF Proposed Standard in **June 2026** — the most significant OpenPGP WoT event since RFC 9580. Authors: Stavros Kousidis (BSI), Johannes Roth and Falko Strenzke (MTG AG), Aron Wussler (Proton AG). The draft went through 17 working-group revisions.

**Algorithm table**:

| Category | Mandatory | Recommended | Optional |
|----------|-----------|-------------|----------|
| Encryption | ML-KEM-768 + X25519 (composite) | ML-KEM-1024 + X448 (composite) | — |
| Signatures | ML-DSA-65 + Ed25519 (composite) | ML-DSA-87 + Ed448 (composite) | SLH-DSA (SHAKE-128s/128f/256s) standalone |
| Key format | v6 required (one exception) | — | v4 subkeys for ML-KEM-768+X25519 |
| Session key | AES-256 in AEAD | — | — |

**Critical design decisions**:

1. **AND-construction composites**: every ML-KEM encryption and every ML-DSA signature is composite with a classical counterpart. A message decrypts only if *both* components succeed. Eliminates downgrade attacks.

2. **X-Wing key combiner**: composite encryption binds shared secrets via a KDF modeled on [X-Wing KEM](https://eprint.iacr.org/2024/039), preventing cross-message component mixing.

3. **SLH-DSA standalone**: hash-based signatures rest on mature assumptions. Signatures >7 KB but appropriate for 20-year trust anchors.

4. **No RSA composite**: classical component is always Curve25519/Curve448. RSA keys have no RFC 9980 upgrade path — migration means new key material.

5. **v4 carve-out**: ML-KEM-768+X25519 may use v4 encryption subkeys. This is the political compromise letting the GnuPG/LibrePGP installed base participate without v6 migration.

**WoT implications**:
- Certifications signed with Ed25519 can be migrated to ML-DSA composites — assuming both signers and verifiers support RFC 9980.
- Component verification is a hard requirement (not optional) — verifiers must check every component.
- **LibrePGP fracture persists**: GnuPG implemented Kyber/ML-KEM in LibrePGP v5, **not** RFC 9980. Cross-ecosystem PQ certifications may be unreadable.

**Analysis source**: [PostQuantum.com — "Post-Quantum OpenPGP Arrives: RFC 9980, the GnuPG Split, and the Signature Gap"](https://postquantum.com/security-pqc/post-quantum-openpgp-rfc-9980) (June 30, 2026).

### GnuPG 2.5.21 Released (July 2, 2026) — 2.4 Declared End-of-Life

[GnuPG 2.5.21](https://www.gnupg.org) released **July 2, 2026**. On the same date, **GnuPG 2.4 was officially declared end-of-life** — distributions must adopt 2.5 (LibrePGP) or fork 2.4.

**Release history (2026)**:

| Version | Date | Significance |
|---------|------|-------------|
| 2.5.17 | 2026-01-06 | Security fix (2.5.13–2.5.16 severe bug); Debian packages |
| — (T8211) | 2026-04-21 | Libgcrypt DoS advisory; 1.12.2/1.11.3/1.10.4 |
| 2.5.19 | 2026-04-24 | Feature/bugfix |
| 2.5.20 | 2026-05-13 | Kyber/ML-KEM (LibrePGP v5); GCM in gpgsm; 2.4 EOL warning |
| **2.5.21** | **2026-07-02** | **2.4 EOL confirmed**; 2.6 series next |

**Blog posts from Koch**:
- [Why Some Criticisms Matter More Than Others](https://www.gnupg.org/blog/20260320-some-criticism-matter.html) (March 2026) — addresses RFC 9580/LibrePGP criticism.
- [Cleartext Signatures Considered Harmful](https://www.gnupg.org/blog/20251226-cleartext-signatures.html) (December 2025).

**Schism status**: GnuPG 2.5.x implements LibrePGP v5 with ML-KEM, **not** RFC 9580 or RFC 9980. GnuPG 2.6 ("will not differ a lot from 2.4" except PQC) suggests continued LibrePGP direction. gnupg.org still describes itself as "RFC 4880" — two RFCs out of date. The two camps have now coexisted 2+ years post-RFC 9580. The schism is structural, not transitional.

### Sequoia `sq` v1.4.0 (July 6, 2026)

[Sequoia-PGP](https://sequoia-pgp.org/) shipped `sq` v1.4.0:

- **`--cert-store` option**: use an alternate certificate store (OpenPGP certificate directories). Enables isolated WoT testing.
- **WKD improvements**: create Web Key Distribution directory structure (May 28, 2026 blog post).
- **RFC 9580/9980 alignment**: Sequoia v2 (March 2025) was first with full RFC 9580 v6 support. It is the RFC-aligned reference implementation — the path RFC 9980 PQ certifications will follow.
- **WoT engine**: [sequoia-wot](https://crates.io/crates/sequoia-wot) models WoT as a flow network, authentication as maximum flow. Largely compatible with PGP/GnuPG semantics despite differing from both.

### Updated Practical Guidance (August 2026)

Given RFC 9980 publication and permanent LibrePGP fracture:

1. **PQ migration path is now defined but bifurcated.** RFC 9980 (Sequoia, OpenPGP.js, Proton) vs LibrePGP v5 (GnuPG, Gpg4win, RNP). Choose your camp deliberately.
2. **Generate new keys with Ed25519/X25519** as the classical baseline. These have a clear composite upgrade path (ML-DSA-65+Ed25519, ML-KEM-768+X25519) under RFC 9980.
3. **RSA keys have no RFC 9980 upgrade path.** Plan key migration, not algorithm migration, for RSA-dependent WoT nodes.
4. **Test cross-ecosystem certifications.** If your WoT spans GnuPG and Sequoia/OpenPGP.js users, verify that certifications parse in both ecosystems.
5. **For long-lived trust anchors (20+ years)**: consider SLH-DSA standalone once implementations stabilize. Hash-based signatures have the most mature security assumptions.
6. **Track GnuPG 2.6.** If it aligns with neither RFC 9580 nor RFC 9980, the LibrePGP fracture deepens further.

### Updated GitHub Activity — August 6, 2026

| Project | Stars | Last push | Notes |
|---------|------:|-----------|-------|
| [gpg/gnupg](https://github.com/gpg/gnupg) | ~950 | 2026-07-02 | 2.5.21; 2.4 EOL; LibrePGP v5; ML-KEM |
| [openpgpjs/openpgpjs](https://github.com/openpgpjs/openpgpjs) | ~5,950 | active | RFC 9580 v6 production; ~821 forks |
| [sequoia-pgp](https://sequoia-pgp.org/) | n/a | 2026-07-06 | `sq` v1.4.0; `--cert-store`; RFC 9580/9980-aligned |
| [pgpainless/pgpainless-wot](https://github.com/pgpainless/pgpainless-wot) | 0 | 2026-04-28 | NLnet-funded; quiet 3+ months |

**Key observation**: PGPainless WoT has been quiet for 3+ months (last commit April 28). The NLnet-funded development phase may be concluding without a stable 1.0. Meanwhile, Sequoia's WoT engine (`sequoia-wot`) remains the most actively maintained RFC-aligned WoT implementation.

## Primary sources

- [RFC 9580 — OpenPGP](https://www.rfc-editor.org/rfc/rfc9580.html)
- [OpenPGP standard overview](https://www.openpgp.org/about/standard/)
- [GnuPG](https://www.gnupg.org/) and [gpg/gnupg mirror](https://github.com/gpg/gnupg)
- [Sequoia-PGP](https://sequoia-pgp.org/)
- [OpenPGP.js](https://github.com/openpgpjs/openpgpjs)
- [Mailvelope](https://github.com/mailvelope/mailvelope)
- [PGPainless](https://pgpainless.org/)
- [keys.openpgp.org FAQ](https://keys.openpgp.org/about/faq/)
- [First-Party Approved Third-Party Certifications in OpenPGP draft](https://www.ietf.org/archive/id/draft-dkg-openpgp-1pa3pc-02.html)
- [A Protocol for Solving Certificate Poisoning for the OpenPGP Keyserver Network](https://journals-sol.sbc.org.br/index.php/jisa/article/view/3810)
- [The Evolution of PGP's Web of Trust](https://www.mit.edu/~prz/docs/Beautiful_Security%20Chap7.pdf)
- [PGPainless WoT module](https://github.com/pgpainless/pgpainless-wot) — NLnet/NGI Assure funded Java/Kotlin WoT path computation
- [OpenPGP ID u4/u5 spec](https://foopgp.org/blog/2026-04-28-openpgp-id-spec/) — foopgp.org draft universal identifiers
- [draft-ietf-openpgp-replacementkey-07](https://datatracker.ietf.org/doc/draft-ietf-openpgp-replacementkey/) — IETF OpenPGP key replacement signalling (April 2026, active)
- [draft-gallagher-openpgp-signatures-03](https://datatracker.ietf.org/doc/html/draft-gallagher-openpgp-signatures-03) — OpenPGP signature grammar and semantics updates (June 2026)
- [draft-gallagher-openpgp-messages-00](https://datatracker.ietf.org/doc/html/draft-gallagher-openpgp-messages-00) — OpenPGP message grammar updates
- [Ariadne Identity Core Specification](https://ariadne.id/core/0/)
- [Keyoxide](https://keyoxide.org/) and [Keyoxide FAQ](https://docs.keyoxide.org/wiki/faq/)
- [Hermine post-quantum threshold signatures](https://hermine-th.org) and [eprint 2026/419](https://eprint.iacr.org/2026/419)
- [RFC 9980 — Post-Quantum Cryptography in OpenPGP](https://datatracker.ietf.org/doc/rfc9980) — Published June 2026; composite ML-KEM+X25519, ML-DSA+Ed25519; SLH-DSA standalone
- [PostQuantum.com — RFC 9980 analysis](https://postquantum.com/security-pqc/post-quantum-openpgp-rfc-9980) — "Post-Quantum OpenPGP Arrives" (June 30, 2026); GnuPG split and signature gap analysis
- [GnuPG 2.5.21 release announcement](https://lists.gnupg.org/pipermail/gnupg-announce/2026q3/000506.html) — July 2, 2026; 2.4 EOL confirmed
- [GnuPG blog: Why Some Criticisms Matter More Than Others](https://www.gnupg.org/blog/20260320-some-criticism-matter.html) — Koch's response to LibrePGP criticism
- [Sequoia `sq` v1.4.0 release](https://sequoia-pgp.org) — `--cert-store`; WKD improvements; RFC 9580/9980 alignment
