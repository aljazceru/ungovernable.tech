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
*Identifiers, credentials, and reputation that belong to the user, not to platforms, governments, or the issuer after the fact.*

---

## Core primitives

### DIDs (Decentralized Identifiers)

A W3C standard. A URI of the form `did:method:...` resolves through a method-specific resolver to a DID Document containing public keys and service endpoints.

- `did:key` — no registry, self-contained.
- `did:web` — resolves via HTTPS (pragmatic, with trust centralized in DNS). Microsoft's Entra Verified ID has effectively shifted to this method.
- `did:ion` — anchored on Bitcoin via Sidetree (DIF; original Microsoft sponsorship). Largely community-maintained today.
- `did:plc` — Bluesky's model: centralized log, portable.
- `did:ens` — Ethereum Name Service.
- `did:peer` — ephemeral, pairwise DIDs for private connections.

### Verifiable Credentials (VCs)

W3C **VC Data Model 2.0** (W3C Recommendation, May 2025): signed JSON-LD or JWT structures where an **issuer** (for example, a university) attests claims about a **subject** that the subject can present to a **verifier** with cryptographic integrity.

### Selective disclosure / ZK credentials

Instead of handing over a whole credential, prove only what is needed:

- **BBS+ signatures** — redact attributes; pairing-based.
- **SD-JWT (RFC 9901, November 2025)** — JWT with salted hashes of individual claims; the holder reveals chosen claims by disclosing salt and value.
- **ZK-based** — Anon Aadhaar, zkPassport, Rarimo, Semaphore: prove "I have a credential from X saying my age > 18" without revealing name or ID number.
- **mDL (ISO 18013-5)** — mobile driver's license with selective disclosure, deployed in several US states and the EU Digital Wallet.

---

## The stack

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

## Relation to confidential computing

- **Attestation-backed credentials.** A TEE can issue credentials claiming "this attestation happened", binding an off-chain fact to a decentralized identifier. This is used for attested AI oracles (Oasis ROFL, Phala) and for proof-of-humanity via device attestation (Apple DeviceCheck, Google Play Integrity producing pseudonymous VCs).
- **Confidential inference identity.** A private LLM endpoint's identity, which users want to pin across sessions, can be a DID whose keys live inside a TEE and rotate via attestation on each deployment.
- **Proof of personhood.** Worldcoin's Orb (Secure Enclave + iris), Idena, BrightID, and Proof of Humanity each trade off biometric invasiveness against Sybil resistance. Confidential-computing approaches such as attested iris hashing inside SGX or Secure Enclave try to split the difference.

---

## Representative projects

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

- User-owned identity survives platform failure, account bans, and political coercion.
- Selective disclosure and ZK reduce over-sharing in everyday identity checks.
- Splitting issuer, subject, and verifier breaks the surveillance-capitalism loop.

### Limitations

- **Issuer power remains.** If a government issuer revokes your credential, you are back where you started.
- **Recovery is hard.** Losing your wallet means losing your identity. Social recovery and Shamir-style schemes are immature.
- **Adoption chicken-and-egg.** Most services do not accept VCs, and most users do not have wallets.
- **Correlation attacks.** Pseudonymous DIDs correlate easily across sessions without careful use. Pairwise DIDs help but add UX complexity.
- **Standards churn.** The VC, OIDC4VC, mDL, and ZK-cred landscape is still settling.

---

## Attack surface

- Wallet compromise equals total identity compromise.
- Issuer key compromise taints every credential they signed.
- Replay or linkage across verifiers without nullifiers or pairwise identifiers.
- ZK circuit bugs can quietly break unlinkability.
- Social engineering around recovery is the dominant threat in practice.

---

## Related files

- [Overview - Zero-Knowledge Proofs](/zero-knowledge)
- [Overview - Post-Quantum Cryptography](/post-quantum)
- [Attestation-Architecture](/confidential-computing/attestation-architecture)
- [Overview - Encrypted Messaging](/encrypted-messaging)

## Primary sources

- W3C: *Decentralized Identifiers (DIDs) v1.0*
- W3C: *Verifiable Credentials Data Model v2.0*
- IETF: *SD-JWT* drafts
- ISO 18013-5 (mDL)
- DIF specifications — `identity.foundation`

