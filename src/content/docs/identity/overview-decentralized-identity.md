---
title: "Decentralized Identity"
tags:
  - "did"
  - "ssi"
  - "verifiable-credentials"
  - "identity"
  - "zk"
  - "privacy"
---
*Identifiers, credentials, and reputation that belong to the user — not to platforms, not to governments, not to the issuer after the fact.*

---

## Core Primitives

### DIDs (Decentralized Identifiers)

W3C standard. A URI (`did:method:...`) that resolves via a method-specific resolver to a DID Document containing public keys and service endpoints.

- `did:key` — no registry, self-contained.
- `did:web` — resolves via HTTPS (pragmatic, centralizes trust in DNS).
- `did:ion` — anchored on Bitcoin via Sidetree (Microsoft / DIF).
- `did:plc` — Bluesky's model: centralized log, portable.
- `did:ens` — Ethereum Name Service.
- `did:peer` — ephemeral, pairwise DIDs for private connections.

### Verifiable Credentials (VCs)

W3C VC Data Model: signed JSON-LD / JWT structures where an **issuer** (e.g., a university) attests claims about a **subject** that the subject can present to a **verifier** with cryptographic integrity.

### Selective Disclosure / ZK Credentials

Instead of handing over a whole credential, prove just what's needed:

- **BBS+ signatures** (draft standard) — redact attributes.
- **SD-JWT** (IETF) — selective disclosure via hashed-claim trees.
- **ZK-based** — Anon Aadhaar, zkPassport, Rarimo, Semaphore: prove "I have a credential from X saying my age > 18" without revealing name or ID number.
- **mDL (ISO 18013-5)** — mobile driver's license with selective disclosure, now deployed in several US states and the EU Digital Wallet.

---

## The Stack

```
Application   (login, age-gate, payroll, KYC)
      │
Wallet         (holds DIDs + VCs; user-owned)
      │
Protocols      (DIDComm, OpenID4VP, OpenID4VCI, CHAPI)
      │
Primitives     (DIDs, VCs, BBS+, SD-JWT, ZK circuits)
      │
Trust anchors  (Issuer registries, KYC providers, governments)
      │
Ledger / Infra (Bitcoin/ION, Ethereum/ENS, Sovrin, centralized PKI)
```

---

## Relation to Confidential Computing

- **Attestation-backed credentials.** A TEE can issue credentials claiming "this attestation happened" — binding an off-chain fact to a decentralized identifier. Used for attested AI oracles (Oasis ROFL, Phala) and for "proof of humanity" via device attestation (Apple DeviceCheck, Google Play Integrity → pseudonymous VCs).
- **Confidential inference identity.** A private LLM endpoint's identity (for users to pin across sessions) can be a DID whose keys live inside a TEE, rotated via attestation on each deployment.
- **Proof of personhood.** Worldcoin's Orb (Secure Enclave + iris), Idena, BrightID, Proof of Humanity — each has trade-offs between biometric invasiveness and Sybil resistance. Confidential-computing-based approaches (e.g., attested iris hashing inside SGX/Secure Enclave) try to split the difference.

---

## Representative Projects

| Project | Model | Notes |
|---|---|---|
| **Bluesky / AT Protocol** | `did:plc` | Portable identifiers backed by signed history logs |
| **ENS** | `did:ens` | Human-readable, Ethereum-anchored |
| **Nostr** | npub (just a pubkey) | Minimalist; no DID machinery |
| **EU Digital Identity Wallet (EUDI)** | mDL + ISO standards | Mandated by eIDAS 2.0 (2024); all EU member states by 2026 |
| **Polygon ID / Iden3** | ZK-based VC verification | On-chain and off-chain |
| **Rarimo, zkPassport** | ZK over government eIDs | Privacy-preserving passport verification |
| **Worldcoin / World ID** | Biometric proof of personhood | Controversial; Orb hardware does attested iris hashing |
| **Sovrin / Hyperledger Indy** | Permissioned ledger + BBS+ | Enterprise SSI |
| **Veramo, Credo, Affinidi** | SDKs | Implementation libraries |

---

## Trade-offs

### Strengths

- User-owned identity survives platform failure, account bans, political coercion.
- Selective disclosure + ZK dramatically reduce over-sharing in everyday identity checks.
- Issuer/subject/verifier separation breaks the surveillance capitalism loop.

### Limitations

- **Issuer power remains.** If the issuer is a government that revokes your credential, you're back where you started.
- **Recovery is hard.** Losing your wallet = losing your identity; social recovery and Shamir-style schemes are immature.
- **Adoption chicken-and-egg.** Most services don't accept VCs; most users don't have wallets.
- **Correlation attacks.** Pseudonymous DIDs correlate easily across sessions without careful use (pairwise DIDs help but add UX complexity).
- **Standards churn.** The VC / OIDC4VC / mDL / ZK-cred landscape is still settling.

---

## Attack Surface

- **Wallet compromise = total identity compromise.**
- **Issuer key compromise** taints every credential they signed.
- **Replay / linkage** across verifiers without nullifiers or pairwise identifiers.
- **ZK circuit bugs** can quietly break unlinkability.
- **Social engineering** around recovery is the dominant threat in practice.

---

## Related Files

- [Overview - Zero-Knowledge Proofs](/zero-knowledge)
- [Overview - Post-Quantum Cryptography](/post-quantum)
- [Attestation-Architecture](/confidential-computing/attestation-architecture)
- [Overview - Encrypted Messaging](/encrypted-messaging)

## Primary Sources

- W3C: *Decentralized Identifiers (DIDs) v1.0*
- W3C: *Verifiable Credentials Data Model v2.0*
- IETF: *SD-JWT* drafts
- ISO 18013-5 (mDL)
- DIF specifications — `identity.foundation`

