---
title: "Verifiable Credentials"
tags:
  - "vc"
  - "w3c"
  - "sd-jwt"
  - "bbs"
  - "mdl"
  - "deep-dive"
  - "identity"
---
*Cryptographically signed claims about a subject, in the issuer-holder-verifier model. The formal stack for digital credentials, deployed in mobile driver's licenses, EU Digital Wallets, vaccine passes, and increasingly enterprise login.*

---

## The three-party model

```
ISSUER ──► HOLDER ──► VERIFIER

Issuer:   issues a signed credential to the holder
Holder:   stores it; controls when and to whom it's presented
Verifier: receives a presentation; checks the issuer's signature; trusts the claims
```

The pattern decouples *issuance* from *verification*. The DMV issues a driver's license once; the holder presents it to the bouncer, the rental car company, and the police, each verifying independently without contacting the DMV.

What VCs add: standard formats, cryptographic integrity, **selective disclosure** (reveal only some claims), and **issuer-not-online verification**.

---

## W3C VC Data Model 2.0 (2025)

The W3C VC Data Model became a Recommendation in **May 2025**. The 2.0 update brought:

- Cleaner JSON-LD context handling.
- Updated proof formats.
- Better support for selective disclosure.
- Explicit ZKP-friendly variants.

A credential is a JSON-LD or JWT structure:

```json
{
  "@context": ["https://www.w3.org/ns/credentials/v2"],
  "type": ["VerifiableCredential", "DriversLicenseCredential"],
  "issuer": "did:web:dmv.example.gov",
  "validFrom": "2026-04-25T00:00:00Z",
  "credentialSubject": {
    "id": "did:key:z6Mk...",
    "name": "Alice",
    "dateOfBirth": "1990-01-01",
    "licenseClass": "B"
  },
  "proof": {
    "type": "DataIntegrityProof",
    "cryptosuite": "ecdsa-rdfc-2019",
    "verificationMethod": "did:web:dmv.example.gov#key-1",
    "proofValue": "..."
  }
}
```

The proof is what the verifier checks. The issuer's public key (from their DID Document) verifies the signature. If the cryptosuite supports selective disclosure (BBS+), the holder can reveal subsets.

---

## Credential formats

### JSON-LD VCs

The W3C-canonical form. Rich semantic types via JSON-LD `@context`. Verbose but expressive. Used by enterprise and government wallets that want strict semantic validation.

### JWT VCs

JOSE-compatible. Compact, familiar to OIDC integrators. Less semantic-rich than JSON-LD; common in SSO-adjacent integrations.

### **SD-JWT** (RFC 9901, November 2025)

The breakout format of 2024-2025. JWT-compatible with selective disclosure via **salted hash claims**:

```
SD-JWT structure:
  header.payload.signature ~ disclosure_1 ~ disclosure_2 ~ ...

Each disclosure: salt + claim_name + claim_value
The payload contains hashes of disclosures, not the values.
```

Properties:

- Selective disclosure by revealing chosen disclosures.
- Unlinkability across presentations with key-binding salt rotation.
- JWT-compatible: most JWT libraries can validate the base.
- No fancy crypto, just SHA-256 plus the underlying JWT signature.

SD-JWT is what the EU Digital Wallet, mDL deployments, and most production VC systems use today. Simpler than ZK-based selective disclosure with most of the privacy benefit.

### **BBS+ signatures**

Pairing-based signatures with native selective disclosure and zero-knowledge proofs of possession. The holder can:

- Prove ownership of a credential without revealing the signature.
- Selectively reveal a subset of claims.
- Generate a fresh, unlinkable presentation each time.

More cryptographic horsepower than SD-JWT, with more complex implementations. Used in Hyperledger AnonCreds, some EU experimental wallets, and ZK-friendly credential designs.

### **mDL (ISO 18013-5)**

ISO standard for mobile driver's licenses. Uses CBOR encoding (not JSON), MSO (mobile security object) for issuer signing, and supports selective disclosure of attributes (age, address, license class).

Deployed in several US states, the EU Digital Wallet ecosystem, and increasingly cross-border.

The mDL data model is **adjacent** to W3C VC: different encoding, same conceptual model. Bridges between the two are emerging.

---

## Selective disclosure in practice

A real flow: a bar checks age on entry.

```
Holder: presents mDL via NFC / QR
Bar:    requests age_over_21 only
Holder: SD-JWT discloses only the age_over_21 attribute
        (not name, not date of birth, not address, not license number)
Bar:    verifies issuer signature, accepts proof
```

The holder reveals one bit. The verifier trusts the issuer chain. Privacy is meaningfully better than presenting a physical ID, though still not anonymous since the issuer signature still ties to the issuer.

For full unlinkability across presentations, BBS+ or ZK proofs are needed.

---

## ZK-powered credentials

When selective disclosure is not enough, when the goal is to prove things derived from but not in the credential, ZK proofs come in:

- **Anon Aadhaar** (India): prove "I have a valid Aadhaar credential issued to a person born before X" without revealing identity.
- **zkPassport**: prove ePassport possession plus age, nationality, etc., without revealing the passport.
- **Worldcoin / World ID**: prove uniqueness via an iris-derived nullifier without revealing biometrics.
- **Rarimo / Semaphore**: generic ZK identity primitives.

These compose with VCs: an issuer issues a standard VC, and a ZK circuit proves derivative claims about it.

---

## OIDC4VP / OpenID4VC

The standards that bridge VC presentation to the OIDC and OAuth ecosystem:

- **OIDC4VP** (OpenID for Verifiable Presentations): how a verifier requests presentations from a holder wallet via OIDC-shaped flows.
- **OIDC4VCI** (OpenID for Verifiable Credential Issuance): how an issuer issues credentials via OIDC-shaped flows.

These are the protocols you hit when a website says "Sign in with your wallet". The wallet receives an OIDC-style presentation request, the holder picks credentials, and the presentation goes back via an OIDC-style response.

Production: EU Digital Wallet ecosystem, Microsoft Entra Verified ID, MATTR, and Spruce ID's stack.

---

## EU Digital Identity Wallet (EUDI)

The EU regulatory mandate (eIDAS 2.0) requires every member state to provide a digital identity wallet to citizens by **2026**. The wallet:

- Holds government-issued credentials (national ID, driver's license, qualifications).
- Supports SD-JWT and mDL formats.
- Must be interoperable across the EU.
- Provides strong privacy: holder controls disclosure, and issuers cannot track verifier-side use.

This is the largest production VC deployment in the world by 2026. Whatever format the EU mandates becomes a de facto global default for cross-border credential interop.

---

## Comparison

| Format | Selective disclosure | Unlinkability | Maturity | Adoption |
|--------|---------------------|---------------|----------|----------|
| **JSON-LD VC** | Limited | Limited | Mature | Some enterprise |
| **JWT VC** | No | No | Mature | OIDC integrations |
| **SD-JWT** | Yes (salted hash) | Limited (improves with key binding) | RFC 9901 (2025) | Production EU, mDL bridges |
| **BBS+** | Yes (ZK) | Strong | Stable | AnonCreds, EU pilots |
| **mDL (ISO 18013-5)** | Yes (CBOR-based) | Limited | Production | US states, EU |
| **Anon Aadhaar / Worldcoin / zkPassport** | Yes (ZK) | Strong | Production | India, Worldcoin users |

---

## Trade-offs

### Strengths

- Standardized: W3C VC 2.0 Recommendation 2025; SD-JWT RFC 9901.
- Real production deployment at large scale (EU Digital Wallet, mDL).
- Issuer / holder / verifier decoupling is operationally clean.
- Selective disclosure ships in production formats.
- Composable with DIDs, OIDC, and ZK proofs.

### Limitations

- Format proliferation: SD-JWT vs JSON-LD vs JWT vs BBS+ vs mDL means operational complexity.
- Wallet UX is improving but not consumer-grade for crypto-native users.
- Issuer trust assumptions are inherited; VCs are only as trusted as the issuer's reputation.
- Revocation lists are clunky; checking if a credential is revoked at scale is an operational headache (status lists, etc.).
- Key binding is subtle. Different formats have different mechanisms for making sure the holder presenting the credential really controls it.

---

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Issuer key compromise | Revocation lists; rotate issuer keys |
| Holder credential theft | Hardware-bound holder keys (Secure Enclave) |
| Replay across verifiers | Per-presentation nonces; verifier-specific challenges |
| Linkable presentations | BBS+ or ZK selective disclosure |
| Verifier-side data exfiltration | Holder consent UX; data-minimization defaults |
| Issuer-verifier collusion | Holder doesn't trust either fully — uses unlinkable formats |

---

## Operational patterns

### Mobile mDL deployment

```
DMV issues mDL via NFC / QR to holder phone
Holder phone stores in OS-managed wallet (Apple Wallet, Google Wallet)
Bar / TSA / police requests subset of attributes
Holder approves
mDL presents only requested attributes via ISO 18013-5 protocol
```

### Login with VC

```
Site presents OIDC4VP request: "Need a verified-identity VC"
Wallet selects matching VC
Holder approves disclosure
Site verifies signature, OIDC-style session begins
```

### EU Digital Wallet abroad

A French citizen presents EU-Digital-Wallet credentials in Germany at a hotel. Both wallets implement the EUDI ARF (Architecture and Reference Framework). Cross-border interop works because the protocols and formats are mandated.

---

## Recent developments (2024-2026)

- VC Data Model 2.0 (W3C Rec, May 2025).
- SD-JWT (RFC 9901, November 2025).
- EU Digital Wallet rollout per member state.
- mDL adoption in US states and TSA (PreCheck integration).
- OIDC4VP finalization in OpenID Foundation.
- Anon Aadhaar and zkPassport in production use for proof-of-personhood.

---

## Related files

- [Overview - Decentralized Identity](/identity/overview-decentralized-identity)
- [Overview - Identity & Pseudonymity](/identity)
- [DID Methods](/identity/did-methods)
- [ENS as Identity](/identity/ens-as-identity)
- [ZKML](/zero-knowledge/zkml) — composable proofs over credential data
- [Glossary](/meta/glossary) — VC, BBS+, SD-JWT, mDL, OIDC4VP

---

## Primary sources

- W3C, *Verifiable Credentials Data Model 2.0*, May 2025. [w3.org/TR/vc-data-model-2.0](https://www.w3.org/TR/vc-data-model-2.0/).
- IETF, *RFC 9901: Selective Disclosure for JWTs (SD-JWT)*, November 2025.
- ISO 18013-5, *Mobile driving licence (mDL) — Application*.
- EU Digital Identity Wallet Architecture and Reference Framework (ARF) — [digital-strategy.ec.europa.eu](https://digital-strategy.ec.europa.eu).
- OpenID for Verifiable Presentations / Issuance — [openid.net/specs](https://openid.net/specs).
- Hyperledger AnonCreds — [hyperledger.github.io/anoncreds-spec](https://hyperledger.github.io/anoncreds-spec).
- Anon Aadhaar — [anon-aadhaar.pse.dev](https://anon-aadhaar.pse.dev).

