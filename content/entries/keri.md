---
title: "KERI (Key Event Receipt Infrastructure)"
slug: keri
type: deep-dive
pillars: ["identity"]
readiness: experimental
description: "KERI builds self-certifying identifiers with pre-rotated keys, so a stolen signing key does not mean a stolen identity. How it works and where it is used."
dek: "Self-certifying identifiers built on cryptographic prefixes, with pre-rotated keys so a stolen signing key doesn't mean a stolen identity. Sam Smith's design from 2019, picked up by GLEIF and the Trust over IP Foundation. Niche but technically distinctive."
updated: 2026-10-25
created: 2026-04-26
origin: vault
source: "11-Identity/KERI.md"
aliases: ["Key Event Receipt Infrastructure", "did:keri", "did:webs"]
tags: ["keri", "identity", "did-keri", "did-webs", "acdc", "pre-rotation", "trust-over-ip", "deep-dive"]
---

## What KERI is

KERI is an identity protocol where the identifier is **self-certifying**: it's a cryptographic prefix (typically a hash of the inception public key plus parameters), and ownership of the corresponding private key is what proves control of the identifier. There is no registry, no blockchain, and no DNS in the trust path.

The headline distinguishing feature is **pre-rotation**: at every key rotation event, the controller commits in advance to the *next* key by including its hash in the signed event. The next signing key is therefore not exposed until it is actually used, and an adversary who steals the current signing key cannot rotate to a key they control — only the controller has the pre-image of the committed next-key hash.

KERI was designed by **Samuel M. Smith** starting around 2019 and published as a sequence of technical reports on [Smith: Key Event Receipt Infrastructure](https://arxiv.org/abs/1907.02143) and at `keri.one`. It has been adopted as the technical foundation of the **Trust over IP Foundation** layer-1 spec and used by **GLEIF** (Global Legal Entity Identifier Foundation) for vLEI (verifiable LEI) credentials.

## Core concepts

### Self-certifying identifiers (AID)

An **Autonomic Identifier (AID)** is a cryptographic prefix:

```
EAtNcDOg-pQzPg5QyYQpNCD3lFQ7hRgIzJsjlEByuwk
↑
Self-addressing identifier: hash of inception event
```

The prefix is the hash of the **inception event** (which contains the initial signing key, the pre-rotation commitment, and parameters). Ownership of the inception key proves control of the AID.

This makes the AID immune to issuer takedowns, registry deletions, or DNS attacks. The identifier is a function of the cryptographic state, not a name allocated by anyone.

### Key Event Log (KEL)

Each AID has a hash-chained log of **key events**:

```
inception → rotation → rotation → interaction → rotation → ...
```

Each event is signed by the current controller and references the previous event by hash. The log is the authoritative history of the identifier.

Events are:

- **icp** (inception): create the AID, set initial signing key, commit pre-rotated next key.
- **rot** (rotation): rotate to the previously-committed next key, and commit a new pre-rotated next key.
- **ixn** (interaction): bind data to the AID without rotating (e.g., issuing credentials, anchoring documents).
- **dip / drt** (delegated inception / rotation): for delegated identifiers.

### Pre-rotation

The defining innovation. At every signing key, the controller commits to the **next** key's hash:

```
At rotation event K:
    signed by:  current_key_K
    contains:   next_key_hash = HASH(K+1_pubkey)
```

The next signing key (`K+1`) is held offline or in a secure location until needed. When rotation happens (event `K+1`), the controller reveals `K+1_pubkey`, the verifier checks that `HASH(K+1_pubkey) == next_key_hash` from event `K`, and the rotation is valid.

If an adversary steals `K`, they **cannot rotate**: they don't have `K+1`'s pre-image. The legitimate controller can rotate to `K+1` (which they hold offline), invalidating the stolen `K`. The window of vulnerability is the time between key compromise detection and rotation.

KERI pre-rotation commits to future keys. In did:plc, repository signing keys and DID rotation keys have distinct authority; compromise of a repository key alone does not authorize DID rotation.

### Witnesses and watchers

KERI's logs are not anchored on a blockchain. Instead, **witnesses** (designated by the controller) publish receipts attesting to each key event. **Watchers** observe witnesses and detect inconsistencies.

- A controller designates `n` witnesses and requires `m`-of-`n` to sign each event.
- Witnesses publish their receipts on any available transport (HTTP, gossip, DHT).
- Verifiers consult witnesses (or watchers cached from witnesses) to confirm event validity.
- A "duplicity" detection: if witnesses publish conflicting events for the same sequence number, the AID is compromised and watchers raise the alarm.

This is a **witness-based BFT** consensus — lighter than blockchain, heavier than pure-key identity.

### Direct vs. indirect mode

- **Direct mode**: controller and verifier exchange events peer-to-peer. No witnesses needed. Suitable for closed bilateral relationships.
- **Indirect mode**: events are published to witnesses; anyone can verify by consulting witnesses. Required for public-facing identity.

## DID methods built on KERI

### did:keri

A DID method where the identifier is a KERI AID. The DID Document is derived from the latest key event log state. Resolution involves replaying the KEL.

```
did:keri:EAtNcDOg-pQzPg5QyYQpNCD3lFQ7hRgIzJsjlEByuwk
```

### did:webs

A hybrid: DIDs hosted at HTTPS URLs (like did:web) but **with a KEL appended** so the underlying KERI identifier is verifiable independently of DNS. Designed to give the operational simplicity of did:web with KERI's self-certifying assurance.

```
did:webs:example.com%3a3000:users:alice:EKYGGh-FtAphGmSZbsuBs_t4qpsjYJ2ZqvMKluq9OxmP
↓
HTTPS fetches DID Doc + KEL
KEL is verifiable cryptographically; HTTPS is just a transport
```

did:webs is the method GLEIF uses for vLEI credentials. The interest is that even if the website disappears or DNS is hijacked, the KEL (cached anywhere) still proves identifier history.

## ACDC — Authentic Chained Data Containers

KERI's alternative to W3C Verifiable Credentials. ACDCs are credential-like structures with these distinguishing features:

- **Chained**: a credential can reference and be cryptographically chained to its issuer's prior credentials, building provenance trees.
- **Schema-bound**: each ACDC commits to a schema hash; schemas are also self-addressing.
- **Issuer-AID-rooted**: the issuer is a KERI AID, not a DID with arbitrary key material.
- **Edge-and-rule constrained**: ACDC graphs can encode authorization policies, delegation, and revocation in a structured way.

ACDCs underlie the GLEIF vLEI ecosystem: a chain from the GLEIF root, to qualified vLEI issuers, to legal entities, to officers and roles within those entities. Each link is an ACDC.

vLEI in production has been issued to thousands of organizations as of 2025. It's the largest production deployment of KERI.

## Comparison with other DID approaches

| Property | KERI / did:keri | did:plc | did:ion | did:web | did:key |
|----------|----------------|---------|---------|---------|---------|
| **Identifier root** | Self-certifying prefix | PLC log entry | Sidetree on Bitcoin | DNS | Public key |
| **Pre-rotation** | **Yes** (built-in) | No | No | No | N/A |
| **Recovery** | Pre-rotated key + witnesses | Recovery keys | Sidetree operations | Domain ownership | None |
| **Decentralization** | Witness-based BFT | One log operator (BSky) | Bitcoin + DIF | DNS-trusted | None needed |
| **Update path** | Signed event log | Signed PLC entry | Sidetree operation | File edit | None |
| **Operational complexity** | High | Medium | High | Low | Trivial |
| **Production scale** | GLEIF (~thousands) | Millions (Bluesky) | Niche | Enterprise | Ephemeral |
| **Spec maturity** | Internet-Draft + ToIP | DID method spec | DIF spec | W3C method | W3C method |

KERI's distinguishing feature is **pre-rotation**: nothing else on this list has it. The cost is operational complexity.

## Where KERI fits

| Use case | Why KERI |
|----------|----------|
| **Legal entity identity (GLEIF vLEI)** | Long-lived organizational identity, pre-rotation gives strong recovery story |
| **Government / regulated identity** | Self-certifying prefix avoids registrar lock-in |
| **Supply-chain provenance** | Chained ACDCs encode multi-step custody |
| **Long-lived credential issuance** | Issuer's KEL outlives any web presence |
| **Witness-redundant identity** | Where blockchain is too heavy and DNS is too fragile |

When **not** to use KERI:

- Consumer social identity (use Nostr, Pubky, or did:plc).
- Ephemeral identifiers (use did:key).
- Where the ecosystem already runs on W3C VCs and OIDC4VP (use did:web + VCs).
- Where the operational team can't run witnesses.

## Honest scope and adoption

KERI has a **niche** in identity. As of early 2026:

- The spec is sprawling. The KERI suite spans key event protocol, witness protocol, ACDC, CESR (Composable Event Streaming Representation), SAID (Self-Addressing Identifier), and more. The full stack is hundreds of pages of technical reports.
- Implementations exist (`keripy`, `keri-rs`, `keria`, `signify-ts`) but are research-grade compared to the W3C DID/VC ecosystem.
- **GLEIF vLEI** is the biggest production deployment. Government and enterprise pilots are the active use cases.
- Bluesky, Nostr, and the broader sovereign-identity space have not adopted KERI. The simplicity argument from pure-key systems beats KERI's pre-rotation in most cypherpunk contexts.

KERI is technically excellent for what it does. It is also operationally heavy in a way that limits its adoption to organizations with dedicated identity infrastructure teams.

## Trade-offs

### Strengths

- **Pre-rotation**: a stolen signing key cannot take over the identity.
- Self-certifying. No registry, no DNS, no blockchain in the trust path.
- Witness-based recovery is lighter than blockchain anchoring.
- Chained ACDCs give rich provenance structures.
- GLEIF production deployment proves the model at scale for legal entities.

### Limitations

- Operationally complex (witnesses, watchers, KEL maintenance).
- Spec sprawl. KERI, ACDC, CESR, SAID together are a substantial learning investment.
- Niche tooling. Wallets, libraries, and SDKs are far behind W3C DID/VC.
- Witnesses are a trust anchor that has to be selected and maintained.
- No consumer-facing wallet adoption.
- Pre-rotation requires storing a future key offline — operational burden.

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Current signing key compromise | Pre-rotation; rotate to committed next key before adversary acts |
| Witness collusion | Multiple independent witnesses; watchers detect duplicity |
| Pre-rotation key compromise (before reveal) | Multi-sig on the next-key commitment |
| Hash function break (changes AID semantics) | Migration via interaction event referencing new hash family |
| KEL availability (witnesses go offline) | Distribute witnesses; self-host backup witnesses |
| Quantum attack on signing keys | KERI is signature-agnostic; can use ML-DSA / SLH-DSA as the signature suite |

## Primary sources

- [Smith: Key Event Receipt Infrastructure](https://arxiv.org/abs/1907.02143)
- [KERI specification](https://weboftrust.github.io/ietf-keri/draft-ssmith-keri.html)
- [CESR specification](https://weboftrust.github.io/ietf-cesr/draft-ssmith-cesr.html)
- [GLEIF vLEI Ecosystem Governance Framework](https://www.gleif.org/en/vlei/introducing-the-vlei-ecosystem-governance-framework)
- [KERI reference implementation](https://github.com/WebOfTrust/keripy)
- [KERIA implementation](https://github.com/WebOfTrust/keria)
- [Signify TypeScript implementation](https://github.com/WebOfTrust/signify-ts)
- [Trust over IP KERI specification](https://trustoverip.github.io/kswg-keri-specification/)
- [The did:webs method](https://trustoverip.github.io/kswg-did-method-webs-specification/)
- [ACDC specification](https://trustoverip.github.io/kswg-acdc-specification/)
- [did:plc specification and directory implementation](https://github.com/did-method-plc/did-method-plc)
