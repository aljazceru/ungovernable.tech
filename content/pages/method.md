---
title: "How We Evaluate Technology"
description: "The questions every ungovernable.tech entry answers, how readiness ratings are assigned, how sources are ranked, and the claims we treat with suspicion."
---

## The questions every entry answers

1. **What problem does it solve?** Against which adversary, for which asset.
2. **What does it trust?** Hardware vendors, operators, a majority of validators, at least one honest relay, a trusted setup, your own endpoint. Every system trusts something.
3. **How does it fail?** Side channels, implementation bugs, operational mistakes, protocol downgrades, metadata leaks, coercion of the vendor, lost keys.
4. **How hard is it to use?** Security that people abandon protects nobody.
5. **What is the legal and political exposure?** For users, operators and developers.

## Readiness

Technology entries carry one of six readiness labels. The rating describes the technology's maturity in the hands of people with real adversaries, not the quality of its idea.

- **Battle-tested** — years of production use by people with real adversaries; audited and well understood.
- **Usable** — in production and usable today, but younger, smaller or with known caveats.
- **Experimental** — working software, but early: small user base, unaudited or changing fast.
- **Research** — papers and prototypes; not something to rely on yet.
- **Historical** — discontinued or superseded; kept for the lessons.
- **Cautionary** — works, but its trust model, governance or legal exposure undermines what it claims.

Ratings are editorial judgements and change as projects mature, get audited, are broken or are abandoned. If you think one is wrong, tell us why.

## Sources, in order of weight

1. Peer-reviewed cryptography and security research (IACR, USENIX, PETS, IEEE S&P, ACM CCS).
2. Specifications and standards (RFCs, NIST FIPS, BIPs, NIPs) and audited open-source implementations.
3. Production deployments with a track record, and public audit reports.
4. Project documentation, release notes and repositories.
5. Announcements, roadmaps and claims that have not yet been demonstrated.

Entries link to primary sources wherever possible. Volatile facts (versions, release dates, deployment numbers) belong in dated briefings; explainers and deep dives are revised when those facts change.

## Claims we treat with suspicion

- "Decentralized," but someone must approve who joins.
- "Private," but metadata leaks.
- "Uncensorable," but there are admin keys.
- "Trustless," but there is a trusted setup or a single attestation service.
- "Anonymous," but identity verification is required.
- "Military-grade encryption," and other phrases that mean nothing.

## Editorial rules

- Every factual claim should be traceable to a source; numbers and statistics are cited or left out.
- Experimental and production-ready are always distinguished.
- Directory links are checked for dead ends; links to discontinued or seized projects are labelled, not silently kept.
- No affiliate links, no sponsored placements, no tracking.

## Corrections

Open an issue at <https://github.com/aljazceru/ungovernable.tech/issues> with the page and what is wrong. Corrections are applied and the page's updated date changes.
