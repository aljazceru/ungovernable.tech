---
title: "DID Methods"
tags:
  - "did"
  - "did-key"
  - "did-web"
  - "did-plc"
  - "did-ion"
  - "w3c"
  - "deep-dive"
  - "identity"
---
*A concrete look at the DID methods worth taking seriously in 2026: what each one trades off, who uses it in production, and which to pick for which threat model.*

---

## The method-resolver architecture

A DID looks like `did:method:identifier`. The W3C DID Core spec leaves the **method** open. A method is a small protocol that defines:

- How a DID gets created.
- How the DID Document (containing public keys, service endpoints, etc.) is **resolved** from the identifier.
- How the DID can be updated, deactivated, or rotated.

There are dozens of registered methods. Most are dead, demonstrative, or vendor lock-ins. The handful below are the ones worth knowing.

---

## did:key — self-contained

**Mechanics**: the identifier *is* the public key (multibase-encoded). Resolution is a local operation, with no registry and no network call:

```
did:key:z6MkpTHR8VNsBxYAAWHut2Geadd9jSrUEZD4kV9NjYRjjEpW
                ↑
                Ed25519 pubkey (multibase z6Mk prefix)
```

**Properties**:

- No registry. Pure cryptography.
- No update path. A `did:key` is permanent. You cannot rotate the key. Lose it, identity gone.
- Trivial resolution. Library function, no network.
- Universal. Anyone can mint one.

**Use cases**: ephemeral identifiers, single-purpose authentication, verifier-side recipient public keys for issuing credentials. Not for long-term primary identity.

---

## did:web — the pragmatic option

**Mechanics**: the identifier resolves to an HTTPS URL. The DID Document is served from that URL.

```
did:web:example.com         → https://example.com/.well-known/did.json
did:web:example.com:user:alice → https://example.com/user/alice/did.json
```

**Properties**:

- Resolution requires DNS plus HTTPS, with the same trust as the legacy web.
- Updating is just editing a file.
- Recovery means owning the domain.
- Centralized in the DNS / CA chain.

**Use cases**: enterprise or government identity where DNS ownership is the authoritative anchor. Microsoft's **Entra Verified ID** has effectively shifted production to did:web. Government-issued credentials (health, education) where the issuer's DNS identity is the right trust anchor.

**Limitations**: DNS-bound. The name disappears if the domain does. For sovereignty users this is a non-starter; for most enterprise and government use, it is the right pragma.

---

## did:plc — Bluesky's choice

**Mechanics**: a public, append-only log of DID operations, hosted by a small set of operators. Each DID has a chain of signed operations forming its history; the latest valid state is the current DID Document.

```
did:plc:ewvi7nxzyoun6zhxrhs64oiz
        ↑
        Random identifier (24 chars, base32)
```

**Properties**:

- Centralized log. Bluesky operates the canonical PLC log.
- Portable. DIDs migrate between hosting providers via signed operations.
- Auditable. Full operation history is public.
- Recoverable. Recovery keys can override compromised primary keys.

**Use cases**: Bluesky and ATProto identity at scale. In production with millions of users. The pragmatic compromise: more decentralized than did:web (data is portable, the log is auditable), less so than blockchain methods (one operator runs the log).

**Caveat**: did:plc is run by one entity (Bluesky). The data model lets you migrate to a different log operator, but as of 2026 there is only one operator.

---

## did:ion — Bitcoin-anchored

**Mechanics**: DIDs anchored on Bitcoin via the **Sidetree** protocol. Operations batch into trees; tree roots are anchored as Bitcoin transactions.

```
did:ion:EiClkZMDxPKqC9c-umQfTkR8IyVbn3v0gd2nHSjE0WrM3w
```

**Properties**:

- Bitcoin finality for the operation log.
- Self-managed. You run a Sidetree node or use a public one.
- Permissionless. Anyone can issue a DID.
- Stewardship: DIF (Decentralized Identity Foundation) maintains the protocol; original Microsoft sponsorship has receded as Microsoft shifted to did:web for production.

**Use cases**: high-stakes identity where Bitcoin's finality is the goal. Niche compared with did:web operationally and did:plc on UX.

---

## did:peer — pairwise private DIDs

**Mechanics**: an ephemeral DID created for a single relationship. Both parties exchange `did:peer` identifiers and DID Documents directly, with no resolver and no registry. Used in DIDComm-style messaging.

```
did:peer:0z6MkkGDx38SHMNJEdKcMxSBoLGMvjBLmKDpQUHycqpRkbDXJ
```

**Properties**:

- Pairwise. A distinct DID per relationship.
- No global resolution. Only the parties involved can resolve.
- Privacy. Different relationships cannot be correlated by DID.
- Throwaway. Deactivate by deleting the local state.

**Use cases**: privacy-preserving messaging (DIDComm, Hyperledger Aries). Not for public identity.

---

## did:ens — Ethereum-anchored

**Mechanics**: DIDs whose underlying name is registered on **ENS**. Resolution goes through ENS records.

```
did:ens:vitalik.eth
```

**Properties**:

- Tied to Ethereum L1 finality.
- Same threat model as ENS, where the registry is Ethereum smart contracts.
- CCIP-Read allows off-chain backing for many subnames.
- Composable with the rest of the EVM ecosystem.

**Use cases**: crypto-native identity. Lightning Address records on the same name. SIWE login flows.

---

## did:btc, did:cosmos, others

A long tail of method registrations. Most are demonstrations or vendor-specific. The five above are what production systems converge on.

---

## Comparison

| Method | Decentralization | Update path | Privacy | Maturity | Best for |
|--------|------------------|-------------|---------|----------|----------|
| **did:key** | Pure crypto | None (key is permanent) | Public | Mature | Ephemeral, verifier keys |
| **did:web** | DNS-trusted | File edit | Public | Mature | Enterprise, government |
| **did:plc** | One log operator (BSky) | Signed log entry | Public | Production | Social / ATProto |
| **did:ion** | Bitcoin + DIF | Sidetree operation | Public | Stable, niche | High-stakes Bitcoin-anchored |
| **did:peer** | Pairwise | Pairwise rotation | **Private** | Mature | Encrypted messaging |
| **did:ens** | Ethereum L1 | ENS-managed | Public | Production | Crypto-native, identity-as-name |

---

## Method selection by threat model

| Threat | Method |
|--------|--------|
| Issuer / verifier loss of trust | did:web (issuer's DNS proves identity) |
| Decentralization required | did:ion or did:ens |
| User wants portable social identity | did:plc |
| Per-relationship unlinkability | did:peer |
| Single-use / ephemeral | did:key |
| Government / regulated credential | did:web (most likely) or did:ion |

---

## Multi-DID identity

A user often has several DIDs:

- A **stable identity** DID (did:ens or did:plc) for long-term reputation.
- **Per-relationship pairwise** DIDs (did:peer) for messaging.
- **Verifier keys** as did:key for credential presentation.
- **Service-specific** DIDs (did:web hosted on a service domain).

The W3C DID model accommodates this naturally. Wallet implementations (Spruce ID's Kepler, Indicio, MATTR, Microsoft Authenticator, Apple Wallet) manage multiple DIDs and present the right one for the right context.

---

## DIDs vs pure-key identity

[Nostr](/identity/nostr) and [Pubky](/identity/pubky) argue for pure-key identity and skip the DID layer entirely. Their argument is "DID Documents are over-engineered; the public key is enough." For many use cases that is true.

DIDs add value when:

- You need **rotation** (did:key explicitly does not, but most others do).
- You need **service endpoint discovery** via DID Doc service endpoints.
- You need to **bind multiple key types** (signing, encryption, capability) to one identifier.
- You are integrating with W3C VC issuers and verifiers.

Otherwise, plain pubkey-as-identity (Nostr, Tor v3, PKARR) is simpler.

---

## Trade-offs

### Strengths

- Standardized: W3C DID Core 1.0 (2022).
- Method-pluggable: choose the trust anchor that fits.
- Composable with VCs, OIDC4VP, SIWE, etc.
- Production deployments (Bluesky's millions, Microsoft Entra, EU Digital Wallet).

### Limitations

- Method proliferation, confusing for newcomers.
- Resolver complexity. Every method needs its own resolver code path.
- Centralization risks vary by method, so each use case needs auditing.
- Wallet UX has caught up but is not on par with consumer messengers.

---

## Related files

- [Overview - Decentralized Identity](/identity/overview-decentralized-identity)
- [Overview - Identity & Pseudonymity](/identity)
- [Verifiable Credentials](/identity/verifiable-credentials)
- [ENS as Identity](/identity/ens-as-identity)
- [Nostr](/identity/nostr)
- [Pubky](/identity/pubky)
- [Glossary](/meta/glossary) — DID, did:key, did:web, did:plc, did:ion, did:peer

---

## Primary sources

- W3C, *DID Core 1.0*, recommendation 2022. [w3.org/TR/did-core](https://www.w3.org/TR/did-core).
- DIF, *Sidetree Protocol*. [github.com/decentralized-identity/sidetree](https://github.com/decentralized-identity/sidetree).
- Bluesky / ATProto, *did:plc method spec*. [github.com/did-method-plc/did-method-plc](https://github.com/did-method-plc/did-method-plc).
- DID method registry — [w3c.github.io/did-spec-registries/](https://w3c.github.io/did-spec-registries/).
- DIDComm Messaging — [identity.foundation/didcomm-messaging](https://identity.foundation/didcomm-messaging).
- Microsoft Entra Verified ID — [learn.microsoft.com/en-us/entra/verified-id](https://learn.microsoft.com/en-us/entra/verified-id).

