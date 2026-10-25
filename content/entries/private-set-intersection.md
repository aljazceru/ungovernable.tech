---
title: "Private Set Intersection"
slug: private-set-intersection
type: explainer
pillars: ["cryptography"]
description: "Private set intersection lets two parties learn which items they have in common and nothing else: protocols, performance and real deployments."
dek: "A two-party (or multi-party) protocol where each party holds a private set and the parties learn only the intersection. Items not in the intersection stay private. Variants exist for cardinality-only, threshold-PSI, and circuit-PSI (compute on the intersection without revealing it)."
updated: 2026-04-26
created: 2026-04-26
origin: vault
source: "02-Cryptography/Private Set Intersection.md"
aliases: ["PSI", "Private Set Intersection"]
tags: ["psi", "mpc", "oprf", "cryptography", "deep-dive"]
---

## Threat model

Two parties, client `C` with set `X = {x_1, …, x_n}` and server `S` with set `Y = {y_1, …, y_m}`. Goal: client learns `X ∩ Y`, server learns nothing (or also learns the intersection in symmetric variants).

What's hidden:

- Server's elements in `Y \ X` stay hidden from client.
- Client's elements in `X \ Y` stay hidden from server.
- Sometimes the size `|X \ Y|` and `|Y \ X|` are themselves sensitive; padding and bucketing address this.

What may leak (depending on variant):

- The intersection itself (intentional in standard PSI).
- The sizes `|X|`, `|Y|`.
- Whether a particular query was made (in repeated-PSI scenarios, traffic patterns).

PSI sits at the boundary of MPC: it is a specific function `f(X, Y) = X ∩ Y`. Generic MPC can solve it, but specialized constructions are orders of magnitude faster.

## Variants

| Variant | Output to client | Output to server | Use case |
|---------|------------------|------------------|----------|
| Plain PSI | `X ∩ Y` | nothing | contact discovery |
| PSI cardinality | `|X ∩ Y|` | nothing | breach checking |
| PSI sum | `Σ values associated with intersection` | aggregate | ad measurement |
| Threshold PSI | reveal `X ∩ Y` only if `|X ∩ Y| ≥ t` | nothing | matchmaking |
| Circuit PSI | output of a circuit applied to intersection | depends | compute on shared records |
| Unbalanced PSI | small `|X|`, huge `|Y|` | nothing | client-vs-server-database |

## Construction families

### OPRF-based (KKRT16 and successors)

Kolesnikov, Kumaresan, Rosulek and Trieu, *Efficient Batched Oblivious PRF with Applications to Private Set Intersection*, CCS 2016 (KKRT16). The classical recipe:

```
server: pick OPRF key k
both:   for each x_i client computes F_k(x_i) via OPRF (server learns nothing)
server: send Y' = {F_k(y_j) for y_j in Y}
client: compare {F_k(x_i)} against Y'; intersection elements collide
```

OPRF + OT extension makes this very fast. Successors (PaXoS, SpOT-light, VOLE-PSI by Rindal et al.) bring billion-element PSI to seconds on commodity hardware. Used by Signal contact discovery (with TEE assist) and by various ad-measurement vendors.

### Diffie-Hellman PSI

Older, simpler:

```
client: blind X with secret a:  X' = {H(x_i)^a}
server: blind Y with secret b:  Y' = {H(y_j)^b}
both exchange and re-blind:     X'' = X'^b, Y'' = Y'^a
intersection: x_i ↔ y_j when H(x_i)^(ab) = H(y_j)^(ab)
```

Folklore construction; appears in Apple's PSI proposal for iCloud Photos CSAM scanning (Bellare et al., *The Apple PSI System*, 2021). Apple **retracted the deployment in late 2022** after researcher pushback on collisions and broader civil-liberties concerns, despite the underlying PSI math being sound. The retraction is a useful case study: cryptographic correctness is necessary but not sufficient for legitimacy.

### FHE-based PSI

Use somewhat-homomorphic or fully homomorphic encryption (typically BFV or CKKS — see [Overview - Fully Homomorphic Encryption](/kb/fully-homomorphic-encryption/)) to evaluate set membership under encryption. Chen, Laine, Rindal, *Fast Private Set Intersection from Homomorphic Encryption*, CCS 2017 (a.k.a. *APSI*) and *PSI from Homomorphic Encryption with Reduced Communication and Computation*, CCS 2018 are the canonical references; Microsoft's APSI library implements them. Strength: very low communication for unbalanced PSI (small client set, huge server set). Weakness: server compute is heavy.

### MPC-based / circuit PSI

Run a circuit-PSI protocol that produces secret shares of the intersection rather than the intersection itself; then evaluate further MPC on the shares. Pinkas, Schneider and Zohner, *Faster Private Set Intersection Based on OT Extension*, USENIX Security 2014; later extended by Pinkas, Rosulek, Trieu, Yanai (2019) and others.

### VOLE-PSI (modern, 2022+)

Rindal and Schoppmann, *VOLE-PSI: Fast OPRF and Circuit-PSI from Vector-OLE*, EUROCRYPT 2021. Closest to state-of-the-art for billion-scale balanced PSI as of 2026.

## Applications

### Contact discovery

A messenger needs to tell a user which of their phone contacts are also users without uploading the address book in cleartext. Production deployments:

- **Signal** uses an SGX-attested service combined with a hash-prefix bucket scheme. Strictly speaking this is *trusted-hardware-assisted* private contact discovery, not a pure cryptographic PSI; the trust model is the SGX attestation. Background: *Private Contact Discovery* (Moxie Marlinspike, 2017 blog) and the open-source `ContactDiscoveryService`.
- **Apple Messages** uses iCloud-stored hashed numbers with similar tradeoffs.
- **Google Messages** has experimented with PSI-style protocols in newer rollouts.

### Have-I-Been-Pwned-style breach checking

Hunt's *PwnedPasswords* API uses a *k-anonymity hash prefix* scheme: client sends the first 5 hex chars of `SHA-1(password)`, server returns all matching suffixes. This is a privacy-preserving lookup but not technically PSI; it's a one-sided range query. Cloudflare partnered on the prefix protocol. Real PSI variants (Google Password Checkup) use OPRF-based PSI to harden the same idea.

### Apple PSI for CSAM scanning (retracted)

Apple announced in August 2021 a PSI-based on-device matching of iCloud Photos against a hashed CSAM database. The cryptographic design (Bhowmick, Boneh, Myers, Shen and others) used DH-PSI plus threshold secret sharing so the server learned nothing unless a per-account match count crossed a threshold. After researcher and civil-society pushback (collision attacks against the perceptual hash, scope-creep concerns), Apple **abandoned the deployment in December 2022**.

Reference: *Apple PSI System Threat Model and Cryptographic Specification*, July 2021 (now archived).

### Ad measurement

- **Google PAIR** (Publisher Advertiser Identity Reconciliation): PSI between advertiser and publisher first-party identities so both sides learn the overlap audience without exchanging raw user lists.
- **Meta Private Lift** / **Private Computation Framework**: MPC + PSI to measure ad campaign lift over a control group without exposing per-user attribution.
- **IAB Tech Lab PAIR specification** (2023+): standards-track effort.

### Joint research / health records

Hospitals or genomic consortia with overlapping patient cohorts use PSI to identify which records they both hold (for joint analysis) without exchanging full patient lists. Typically threshold PSI to avoid revealing single-record overlaps.

## Trade-offs by family

| Family | Comm. | Server compute | Client compute | Unbalanced-friendly | Trust |
|--------|-------|---------------|----------------|---------------------|-------|
| OPRF + OT (KKRT, VOLE-PSI) | linear in `|X|+|Y|` | fast | fast | moderate | semi-honest standard, malicious variants exist |
| DH-PSI | linear, EC ops | medium | medium | yes | semi-honest |
| FHE-PSI (APSI) | sublinear in server set | heavy | medium | excellent | semi-honest |
| MPC circuit PSI | linear | medium | medium | weak | semi-honest, malicious variants |
| TEE-assisted (Signal-style) | small | very fast | very fast | excellent | hardware vendor |

Choose based on: which side can spend compute, whether unbalanced sizes are common, whether malicious-security is required, and whether a trusted enclave is acceptable.

## Security models

- **Semi-honest:** both parties follow the protocol but may try to learn extra. Most production deployments target this — adequate when both parties are services with reputational stakes.
- **Malicious:** parties may deviate arbitrarily. Required when one side might lie about its set membership; cost is typically 2–5x semi-honest.
- **Covert:** cheating is detected with non-trivial probability.

## Pitfalls

- **Hash-only "PSI" is not PSI.** Sending `SHA-256(x_i)` of phone numbers to a server is a dictionary-attackable hash. Real PSI requires keyed PRFs, OPRF, or oblivious primitives.
- **Set-size leakage.** Both sides see the order of magnitude; pad to a power-of-two bucket if size is sensitive.
- **Re-running PSI iteratively** can leak the full set via differential queries. Bound the number of runs and rotate keys.
- **Linkability across queries.** OPRF-based PSI with a static server key allows a client to detect across-session collisions in its own set. Add session-binding nonces if undesired.

## Primary sources

- Pinkas, Schneider, Zohner, *Faster Private Set Intersection Based on OT Extension*, USENIX Security 2014.
- Kolesnikov, Kumaresan, Rosulek, Trieu, *Efficient Batched Oblivious PRF with Applications to Private Set Intersection* (KKRT16), CCS 2016.
- Chen, Laine, Rindal, *Fast Private Set Intersection from Homomorphic Encryption*, CCS 2017.
- Chen, Huang, Laine, Rindal, *Labeled PSI from Fully Homomorphic Encryption with Malicious Security*, CCS 2018.
- Pinkas, Rosulek, Trieu, Yanai, *SpOT-light: Lightweight Private Set Intersection from Sparse OT Extension*, CRYPTO 2019.
- Rindal, Schoppmann, *VOLE-PSI: Fast OPRF and Circuit-PSI from Vector-OLE*, EUROCRYPT 2021.
- Bhowmick, Boneh, Myers, Shen et al., *Apple PSI System Threat Model and Cryptographic Specification*, 2021 (archived).
- Microsoft APSI: [github.com/microsoft/APSI](https://github.com/microsoft/APSI).
- Signal Contact Discovery: [github.com/signalapp/ContactDiscoveryService](https://github.com/signalapp/ContactDiscoveryService).
- VOLE-PSI: [github.com/Visa-Research/volepsi](https://github.com/Visa-Research/volepsi).
