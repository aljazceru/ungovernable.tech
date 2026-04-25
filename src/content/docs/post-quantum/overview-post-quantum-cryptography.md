---
title: "Overview - Post-Quantum Cryptography"
tags:
  - "pqc"
  - "post-quantum"
  - "ml-kem"
  - "ml-dsa"
  - "slh-dsa"
  - "nist"
sidebar: {"label":"Post-Quantum Cryptography"}
---
*Replacing RSA and elliptic-curve cryptography with algorithms that survive a cryptographically relevant quantum computer.*

---

## Why Now

Shor's algorithm breaks RSA, Diffie-Hellman, and ECC in polynomial time on a sufficiently large quantum computer. Such a machine does not exist today and may not exist for a decade or longer — **but**:

- **"Harvest now, decrypt later."** Adversaries record encrypted traffic today; any record will be readable the day a quantum computer comes online. Anything with a secrecy horizon beyond ~2035 must migrate now.
- Symmetric crypto (AES-256, SHA-3) is largely unaffected; key length doubling (Grover) is enough.

---

## NIST Standards (2024-2025)

After a multi-year competition, NIST finalized:

| Standard | Purpose | Based on | Replaces | Status |
|---|---|---|---|---|
| **FIPS 203 — ML-KEM** (Kyber) | Key encapsulation | Module-LWE | ECDH, RSA-KEM | Final (2024) |
| **FIPS 204 — ML-DSA** (Dilithium) | Digital signatures | Module-LWE / SIS | ECDSA, RSA-PSS | Final (2024) |
| **FIPS 205 — SLH-DSA** (SPHINCS+) | Hash-based signatures | Hash functions only | Conservative backup for ML-DSA | Final (2024) |
| **FIPS 206 — FN-DSA** (Falcon) | Compact signatures | NTRU lattices | Size-sensitive ECDSA uses | **Draft submitted Aug 2025; final expected 2026** |
| **HQC** | Alternate KEM | Code-based | Backup for ML-KEM | **Selected 2025; standard expected 2026** |

STARK-based signatures, isogeny-based KEMs (SIKE was broken 2022 — cautionary tale), and MPC-in-the-head signatures remain research-active.

---

## Deployment Status (early 2026)

- **TLS 1.3 hybrid KEMs** (X25519+ML-KEM-768) shipped: Chrome, Firefox, Cloudflare, Google edge, AWS KMS.
- **SSH** (OpenSSH ≥ 9.0) offers `sntrup761x25519-sha512` hybrid; ML-KEM hybrids landing.
- **Signal Protocol**: PQXDH in production since 2023 — hybrid X3DH + ML-KEM-1024 for initial keys.
- **iMessage PQ3** (Apple, 2024) — post-quantum ratcheting.
- **Email / PGP**: laggard; OpenPGP PQC draft exists, adoption minimal.
- **Blockchain**: hash-based signatures (Lamport / XMSS / SLH-DSA) for quantum-safe wallets under active proposal; Ethereum has a long roadmap.

---

## Relevance to Confidential Computing / Inference

- **Attestation keys.** Intel / AMD / NVIDIA attestation signatures are ECDSA today — quantum-vulnerable. Pre-recorded quotes could be forged post-Q, weakening any past proof of confidentiality. Migration path: new hardware with ML-DSA or SLH-DSA attestation keys; not yet announced by vendors as of early 2026.
- **Sealing / wrapping keys.** Long-lived sealed secrets and key-wrap ciphertexts must be PQ-secure to resist harvest-now-decrypt-later.
- **TLS to TEE.** Use hybrid KEM in any RA-TLS today; pure-PQ once counterparts support ML-KEM.
- **KMS-gated key release.** Rotate to PQ wrap keys on the release side.

---

## Trade-offs

- **Key and signature sizes are larger.** ML-KEM-768 pubkey = 1184 B; ML-DSA signature ~2.4 KB. Matters on constrained links and chained certs.
- **New code = new bugs.** Lattice math is trickier than RSA; constant-time implementations are essential and not trivial.
- **Hybrid is safer.** Composing a classical + PQ KEM means you're secure as long as *either* remains unbroken — until we're sure about PQ algorithms, hybrid is the right default.
- **Performance impact is minimal.** Modern hybrid implementations add 15-20ms to connection establishment (WireGuard: 15-20ms extra; TLS: negligible on modern hardware); throughput unchanged.

---

## Attack Surface

- **Implementation side channels.** Constant-time Kyber / Dilithium are active research; several early libraries had timing leaks.
- **Parameter selection mistakes.** Insecure parameter sets lurking in old demos.
- **Fault attacks on signing.** Reuse of randomness or poor decoders can leak secret keys.
- **"PQ-washing".** Products claim "post-quantum" by bolting PQ onto one layer while classical crypto still gates the overall system.

---

## Implementation Libraries

### liboqs (C / Open Quantum Safe)

The reference implementation library for NIST algorithms. Actively maintained by PQCA.

- **Repository:** https://github.com/open-quantum-safe/liboqs
- **Latest:** v0.14.0 (February 2025)
- **Algorithms:** ML-KEM (Kyber), ML-DSA (Dilithium), SLH-DSA (SPHINCS+), HQC, SNOVA
- **Security fix:** CVE-2025-52473 patched in v0.14.0
- **Note:** v0.14.0 is last release with both Dilithium (Round 3) and ML-DSA (standardized); future releases only ML-DSA
- **Upcoming:** SQIsign (additional signature), SLH-DSA (FIPS 205), NTRU support

### Rust

- **pqcrypto** (https://crates.io/crates/pqcrypto) — NIST algorithm implementations with hybrid mode support
- **ring** — considering PQ integration; not yet shipping
- **rustpq/pqcrypto** — Rust-native implementations from the PQC research community

### Go

- **golang.org/x/crypto/kyber** — ML-KEM implementation in Go standard library's x/crypto module
- **filippo.io/mlkem** — Standalone ML-KEM implementation (Filippo Valsorda)
- Go's standard library is evaluating PQ integration for Go 1.24+

### Other Languages

| Language | Library | Status |
|---|---|---|
| JavaScript | `node-forge` + PQ extensions | Experimental |
| Java | `bouncycastle` | PQ algorithms in progress |
| .NET | `libsodium` bindings, `System.Security.Cryptography` | Early |

---

## Government Migration Timelines

### Germany (BSI)

- **Critical infrastructure deadline:** Full migration to quantum-safe cryptography by 2030
- **Guidance:** BSI position paper (2025) recommends hybrid deployment during transition
- **Reference:** https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Crypto/PQC-joint-statement-2025.pdf

### UK (NCSC)

- **Timeline:** https://www.ncsc.gov.uk/guidance/pqc-migration-timelines
- **Guidance:** Recommends "start planning now" for systems with long data protection requirements
- **Focus:** Inventory crypto assets first, enable crypto-agility, then migrate

### United States

- **NSM-10** (2022): Federal agencies must plan for PQC migration
- **NIST SP 800-175B:** Federal standards for cryptography
- **CISA:** "Harvest now, decrypt later" alerts to critical infrastructure operators

### EU

- **eIDAS 2.0:** Digital identity wallet includes quantum-safe signatures
- **ETSI QSC:** European standards body working on PQC specifications

---

## Updated Deployment Status (April 2026)

|| Protocol | Status | Details |
||---|---|---|
|| **TLS 1.3** | ✅ Hybrid in production | Chrome, Firefox, Safari (iOS 26+) advertise X25519MLKEM768; Cloudflare, Google, AWS backends accept; **>60% of human TLS traffic** uses hybrid ML-KEM (Cloudflare Radar) |
|| **SSH** | 🟡 In progress | OpenSSH 9.0+ supports sntrup761; ML-KEM hybrid in testing |
|| **Signal (PQXDH)** | ✅ Production since 2023 | Hybrid X3DH + ML-KEM-1024 |
|| **Apple iMessage (PQ3)** | ✅ Production since 2024 | Post-quantum ratcheting |
|| **GnuPG** | 🟡 Available since v2.5.1 (Sept 2024) | ML-KEM support, not yet default |
|| **IPsec (Cloudflare)** | ✅ Production March 2026 | First major deployment of hybrid ML-KEM for IPsec/IKEv2; draft-ietf-ipsecme-ikev2-mlkem |
|| **WireGuard** | 🟡 In progress | PQ kernel patches pending; Surfshark offers PQ protection; NordVPN shipped Sept 2024 across all platforms |
|| **OpenVPN** | 🟡 In progress | RFC 8784 (MPK) implementation in progress |
|| **VPN (Enterprise)** | 🟡 In progress | Palo Alto Networks, Mullvad rolling out Quantum Safe VPN |

---

## Quantum Threat Timeline

| Year | Expected Milestone |
|---|---|
| ~2030 | Cryptographically relevant quantum computer (CRQC) possible |
| ~2028-2030 | Grover's algorithm makes AES-256 brute-force feasible (with significant quantum resources) |
| Now | "Harvest now, decrypt later" active — adversaries recording encrypted traffic |
| 2024-2026 | Migration window — upgrade before CRQC exists |

The "harvest now, decrypt later" threat is immediate. Any data with secrecy requirements beyond ~2030 should use hybrid classical+PQ encryption now.

---

## Related Files

- [Overview - Fully Homomorphic Encryption](/cryptography/overview-fully-homomorphic-encryption)
- [Overview - Zero-Knowledge Proofs](/zero-knowledge/overview-zero-knowledge-proofs)
- [Attestation-Architecture](/confidential-computing/attestation-architecture)
- [Overview - Encrypted Messaging](/encrypted-messaging/overview-encrypted-messaging)

## Primary Sources

- NIST FIPS 203 / 204 / 205 / 206 — `csrc.nist.gov/projects/post-quantum-cryptography`
- liboqs: https://github.com/open-quantum-safe/liboqs
- PQCA Blog: https://pqca.org/blog/
- Bernstein & Lange: *Post-quantum cryptography* — Nature 2017 (survey)
- *Signal PQXDH* spec — `signal.org/docs/specifications/pqxdh`
- Apple: *iMessage PQ3* — `security.apple.com/blog/imessage-pq3`
- BSI PQC Joint Statement (2025): `bsi.bund.de`
- NCSC PQC Migration Timelines: `ncsc.gov.uk/guidance/pqc-migration-timelines`

