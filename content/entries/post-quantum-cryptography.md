---
title: "Post-Quantum Cryptography"
slug: post-quantum-cryptography
type: explainer
pillars: ["pqc"]
description: "Replacing RSA and elliptic-curve cryptography with algorithms that survive quantum computers: the NIST standards, migration and harvest-now risk."
dek: "Replacing RSA and elliptic-curve cryptography with algorithms that survive a cryptographically relevant quantum computer."
updated: 2026-09-26
created: 2026-04-17
origin: vault
source: "10-Post-Quantum/Overview - Post-Quantum Cryptography.md"
aliases: ["PQC", "Post-Quantum"]
tags: ["pqc", "post-quantum", "ml-kem", "ml-dsa", "slh-dsa", "nist", "liboqs", "mldsa-native", "openssl-4"]
---

## Why now

Shor's algorithm breaks RSA, Diffie-Hellman, and ECC in polynomial time on a sufficiently large quantum computer. Such a machine does not exist today and may not exist for a decade or longer, but:

- "Harvest now, decrypt later." Adversaries record encrypted traffic today; any record will be readable the day a quantum computer comes online. Anything with a secrecy horizon beyond ~2030 must migrate now.
- **Google tightened the Q-Day estimate in March 2026**: the company now targets completing PQC migration for authentication services by 2029, citing advances in quantum hardware (Willow chip), quantum error correction, and updated factoring resource estimates (estimated ~500,000 qubits for cryptographically relevant work). This is a meaningful acceleration from prior estimates of 2030+.
- Symmetric crypto (AES-256, SHA-3) is largely unaffected; key length doubling (Grover) is enough.

## NIST standards (2024-2025)

After a multi-year competition, NIST finalized:

| Standard | Purpose | Based on | Replaces | Status |
|---|---|---|---|---|
| **FIPS 203 — ML-KEM** (Kyber) | Key encapsulation | Module-LWE | ECDH, RSA-KEM | Final (2024) |
| **FIPS 204 — ML-DSA** (Dilithium) | Digital signatures | Module-LWE / SIS | ECDSA, RSA-PSS | Final (2024) |
| **FIPS 205 — SLH-DSA** (SPHINCS+) | Hash-based signatures | Hash functions only | Conservative backup for ML-DSA | Final (2024) |
| **FIPS 206 — FN-DSA** (Falcon) | Compact signatures | NTRU lattices | Size-sensitive ECDSA uses | **IPD published Aug 2025; final expected late 2026 / early 2027**; SUF-CMA, key-recovery, fixed-point signing under discussion at NIST 6th PQC Conference |
| **HQC** | Alternate KEM | Code-based | Backup for ML-KEM | **Selected March 2025; FIPS document in drafting; expected 2026-2027** |

STARK-based signatures, isogeny-based KEMs (SIKE was broken in 2022, a cautionary tale), and MPC-in-the-head signatures remain research-active.

## Deployment status (August 2026)

- TLS 1.3 hybrid KEMs (X25519+ML-KEM-768) shipped: Chrome, Firefox, Cloudflare, Google edge, AWS KMS. **RFC 10024 (PQ/T hybrid key agreement for TLS 1.3) published August 2026 as Proposed Standard** — the endorsed default is now citeable as an RFC.
- **Pure ML-KEM for TLS**: IETF-wide Last Call closed **August 13, 2026**; IESG decision pending as of Aug 22. Code points would be `Recommended=N` in an Informational RFC. Most contentious PQC standards decision in IETF history — Bernstein's final filing documents 75 non-withdrawn objections and alleges the last-call list blocked it. See [Post-Quantum Saturday — August 22 2026 Weekly Update](/briefings/post-quantum/2026-08-22/) §3.
- SSH (OpenSSH ≥ 9.0) offers `sntrup761x25519-sha512` hybrid; ML-KEM hybrids landing. Forescout data (July 2026): ~90% of SSH servers still not quantum-safe; IoT 28%, OT 16%, IoMT 6% PQC-capable.
- Signal Protocol: PQXDH in production since 2023, hybrid X3DH plus ML-KEM-1024 for initial keys.
- iMessage PQ3 (Apple, 2024): post-quantum ratcheting.
- **OpenPGP: RFC 9980 published June 30, 2026**. Hybrid-only (composite ML-DSA-65+Ed25519). But GnuPG has no PQ signature support — divergent LibrePGP track. Implementation gap is the blocker.
- Email / PGP: RFC 9980 standard exists but real-world adoption depends on GnuPG/LibrePGP reconciliation.
- Blockchain: hash-based signatures (Lamport / XMSS / SLH-DSA) for quantum-safe wallets under active proposal; Ethereum has a long roadmap.
- **NIST Additional Signatures Round 3** (May 14, 2026): 9 candidates from 4 mathematical families (FAEST, HAWK, MAYO, MQOM, QR-UOV, SDitH, SNOVA, SQIsign, UOV). ~2-year evaluation. **HAWK took a ring-specific key-recovery hit in July 2026** (see below).
- **Bernstein "Exploiting ML-DSA bugs" paper** (June 2026): Demonstrates sub-second key recovery from software bugs that pass all standard tests. Estimates 25% of ML-DSA libraries will ship with severe vulnerabilities. Quantitative case for hybrid Ed25519+ML-DSA.
- **Google Cloud dated PQC roadmap** (Aug 11, 2026): SNDL mitigation end-2027 (LB hybrid TLS default-on Oct 2026), signatures + KMS foundations end-2028, Google Trust Services MTC support 2028 — signatures trail confidentiality by one year. See [Post-Quantum Saturday — August 22 2026 Weekly Update](/briefings/post-quantum/2026-08-22/) §7.

## Relevance to confidential computing / inference

- Attestation keys. Intel / AMD / NVIDIA attestation signatures are ECDSA today, which is quantum-vulnerable. Pre-recorded quotes could be forged post-Q, weakening any past proof of confidentiality. Migration path: new hardware with ML-DSA or SLH-DSA attestation keys; vendors had not published concrete attestation-key migration plans as of early 2026.
- Sealing / wrapping keys. Long-lived sealed secrets and key-wrap ciphertexts must be PQ-secure to resist harvest-now-decrypt-later.
- TLS to TEE. Use hybrid KEM in any RA-TLS today; pure-PQ once counterparts support ML-KEM.
- KMS-gated key release. Rotate to PQ wrap keys on the release side.

## Trade-offs

- Key and signature sizes are larger. ML-KEM-768 pubkey = 1184 B; ML-DSA signature ~2.4 KB. Matters on constrained links and chained certs.
- New code means new bugs. Lattice math is trickier than RSA; constant-time implementations are essential and not trivial.
- Hybrid is safer. Composing a classical and PQ KEM means the system is secure as long as either remains unbroken. Until we're sure about PQ algorithms, hybrid is the right default.
- Performance impact is minimal. Modern hybrid implementations add 15-20ms to connection establishment (WireGuard: 15-20ms extra; TLS: negligible on modern hardware); throughput unchanged.

## Attack surface

- Implementation side channels. Constant-time Kyber / Dilithium are active research; several early libraries had timing leaks. KyberSlash (TCHES 2025) demonstrated secret-dependent division timings.
- Parameter selection mistakes. Insecure parameter sets lurking in old demos.
- Fault attacks on signing. Reuse of randomness or poor decoders can leak secret keys.
- "PQ-washing." Products claim "post-quantum" by bolting PQ onto one layer while classical crypto still gates the overall system.
- **AI-assisted cryptanalysis (July 2026).** Anthropic's Claude Mythos Preview recovered signing-equivalent keys from two HAWK-256 challenge public keys (tier-2, ring-specific: Galois involution ζ→−ζ in the power-of-two cyclotomic ring); a separate team hit HAWK independently with GPT-5.6; Mythos also improved the 13-year-old best attack on 7-round AES-128. No deployed standard touched. Economics: a publishable cryptanalytic result now costs ~$100K and a week of model time — the argument for crypto-agility is now an AI-cadence argument. See [Post-Quantum Saturday — August 22 2026 Weekly Update](/briefings/post-quantum/2026-08-22/) §5.
- **Criminal adoption.** The Kyber ransomware (active since September 2025, confirmed April 2026) uses ML-KEM-1024 for key exchange — meaning the PQ toolkit is in the attacker arsenal alongside defenders. This makes attribution harder and underscores that PQ is operationally neutral.

## Implementation libraries

### liboqs (C / Open Quantum Safe)

The reference implementation library for NIST algorithms. Actively maintained by PQCA.

- Repository: https://github.com/open-quantum-safe/liboqs
- Latest checked: v0.15.0 (November 2025)
- Algorithms: ML-KEM (Kyber), ML-DSA (Dilithium), SLH-DSA (SPHINCS+), HQC, SNOVA
- Security fix: CVE-2025-52473 patched in v0.14.0
- Note: v0.14.0 was the transition release with both Dilithium (Round 3) and ML-DSA (standardized); current deployments should use standardized names and parameter sets.
- Upcoming: SQIsign (additional signature), SLH-DSA (FIPS 205), NTRU support

### Rust

- **pqcrypto** (https://crates.io/crates/pqcrypto): NIST algorithm implementations with hybrid mode support
- **ring**: considering PQ integration; no stable PQ release at this writing
- **rustpq/pqcrypto**: Rust-native implementations from the PQC research community

### Go

- **crypto/mlkem**: Go standard-library ML-KEM package, introduced with Go 1.24.
- **filippo.io/mlkem**: standalone ML-KEM implementation (Filippo Valsorda)
- Go's TLS stack supports X25519MLKEM768 by default when curve preferences are not overridden.

### Other languages

| Language | Library | Status |
|---|---|---|
| JavaScript | `node-forge` + PQ extensions | Experimental |
| Java | `bouncycastle` | PQ algorithms in progress |
| .NET | `libsodium` bindings, `System.Security.Cryptography` | Early |

## Government migration timelines

### Germany (BSI)

- Critical infrastructure deadline: full migration to quantum-safe cryptography by 2030
- Guidance: BSI position paper (2025) recommends hybrid deployment during transition
- Reference: https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Crypto/PQC-joint-statement-2025.pdf

### UK (NCSC)

- Timeline: https://www.ncsc.gov.uk/guidance/pqc-migration-timelines
- Guidance: recommends "start planning now" for systems with long data protection requirements
- Focus: inventory crypto assets first, enable crypto-agility, then migrate

### United States

- NSM-10 (2022): federal agencies must plan for PQC migration
- NIST SP 800-175B: federal standards for cryptography
- CISA: "Harvest now, decrypt later" alerts to critical infrastructure operators

### EU

- eIDAS 2.0: digital identity wallet includes quantum-safe signatures
- ETSI QSC: European standards body working on PQC specifications

## Updated deployment status (June 2026)

### Google: Q-Day moved to 2029 — authentication migration priority

Google's March 2026 blog post "Quantum frontiers may be closer than they appear" tightened the corporate Q-Day estimate: Google now targets completing PQC migration for **authentication services** by 2029. This is the first major hyperscaler to issue a specific near-term deadline for PQ authentication, distinct from the prior 2030+ estimates. The stated rationale includes Google Willow quantum chip progress, quantum error correction advances, and updated factoring resource estimates (~500K qubits for cryptographically relevant work). Google explicitly recommends that engineering teams prioritize PQC migration for authentication — digital signatures and certificates — ahead of key exchange. This is a meaningful signal: it shifts the urgency from "key exchange is urgent" to "authentication is also urgent" and aligns with NCSC/BSI guidance already in this library.

**Relevance to ungovernable systems**: Any system with long-lived identity keys, code-signing chains, or certificate-based trust should treat Google's 2029 authentication deadline as a forcing function for PQ signature planning. This applies to Nostr npubs, ENS names, PGP key chains, and any decentralized identity system whose trust model depends on ECDSA/Ed25519 signatures.

### Kyber ransomware: variant activity through June 2026

The Kyber ransomware family (first confirmed April 2026 by Rapid7, using ML-KEM-1024 alongside X25519 and AES-256) continues to circulate. Threat intelligence reporting through May-June 2026 indicates secondary compromised deployments using modified variants with altered ML-KEM parameter sets. The operational pattern — hybrid KEM in criminal malware — is no longer novel; defenders should treat any ransomware sample negotiating PQ key exchange as expected terrain. The implication: PQ is operationally neutral infrastructure.

### FN-DSA (FIPS 206): IPD process advancing

The FIPS 206 initial public draft (IPD) remains in the NIST comment-resolution pipeline as of early June 2026. The IETF `draft-ietf-cose-falcon-04` (current as of this writing, expires April 2026) tracks FIPS 206 alignment for COSE/JOSE integration. Open questions at the NIST 6th PQC Conference included SUF-CMA requirements, hedged variants, key/message-recovery mode, and fixed-point signing. These are being resolved in the IPD period before final publication. HSM vendors (Utimaco, AWS CloudHSM, YubiHSM) have not yet shipped production FN-DSA support; the likely inflection point is 12-18 months after final FIPS publication, consistent with the late 2026 / early 2027 target.

### liboqs v0.16.0 milestone: FIPS alignment

liboqs development continues toward v0.16.0, which targets full FIPS alignment for ML-KEM (FIPS 203), ML-DSA (FIPS 204), and SLH-DSA (FIPS 205) implementations. This includes updated test vectors from the finalized standards and alignment of parameter names with FIPS nomenclature. The v0.14.0 release (July 2025) was the transition release with both Dilithium (Round 3) and ML-DSA (FIPS 204); v0.15.0 (November 2025) refined; v0.16.0 should consolidate FIPS alignment across all three primary standards.

### AWS Private CA: ML-DSA support added

AWS Private Certificate Authority added ML-DSA (FIPS 204) as a supported signing algorithm in Q2 2026, following the April 2026 AWS ML-KEM announcement for KMS and Secrets Manager. This extends PQ signatures to private PKI hierarchies — enterprise CAs issuing internal certificates can now request ML-DSA-backed certificates from AWS PCA. For self-hosted PKI, OpenSSL 3.5 provides the underlying primitives. The practical constraint remains: ML-DSA certificates are not yet widely understood by enterprise TLS clients, so private CA deployments are the immediate use case rather than public Web PKI.

## Updated deployment status (May 2026)

### The Kyber ransomware: PQC goes dark

In a first for criminal malware, the **Kyber ransomware family** (active since September 2025, confirmed by Rapid7 in April 2026) uses **ML-KEM-1024** for key exchange, combined with X25519 (classical) and AES-256-CTR (bulk encryption). The dual-layer scheme means that even a future quantum computer capable of breaking one layer would still face the other. Ars Technica reported this as "branding" (Rapid7's Anna Širokova noted it required relatively little work given liboqs availability), but the operational reality is the same: adversaries are deploying NIST-standardized PQ crypto in weaponized malware. The implication for defenders: PQ is no longer a theoretical concern — it is in the attacker toolkit.

### Cloudflare: >65% of human traffic post-quantum

Cloudflare reported in April 2026 that **>65% of human traffic** through its network negotiates a PQ key exchange — up from >60% in February 2026 and >50% in October 2025. The inflection point happened when Apple iOS 26 shipped ML-KEM as a default in URLSession and Network.framework (WWDC 2025, production late 2025), which automatically pushed hundreds of millions of devices into the PQ-capable client base. Cloudflare's 2029 target for full PQ security (including authentication) remains the reference roadmap for the industry.

### AWS ML-KEM: production since April 2026

AWS turned on **ML-KEM hybrid TLS** by default across KMS, Secrets Manager, ACM (Amazon Certificate Manager), Payment Cryptography, and S3 in April 2026 — a milestone for enterprise cloud. The AWS Secrets Manager clients gained hybrid PQ TLS support in April 2026, extending the service-side ML-KEM support launched in 2025. This means the dominant cloud provider's key management, certificate, secret storage, and object storage services are all PQ-capable for the first time, with the clients automatically negotiating hybrid key exchange. AWS also offers ML-DSA key pair generation in KMS.

### OpenSSL 3.5: GA shipped March 2026

OpenSSL 3.5 shipped in March 2026 with native support for **ML-KEM** (FIPS 203), **ML-DSA** (FIPS 204), and **SLH-DSA** (FIPS 205). This is the inflection point for Linux distributions and self-hosted infrastructure: Ubuntu 26.04 LTS and derivative distributions expose PQ algorithms through the standard OpenSSL interface, making them available to `curl`, `nginx`, `haproxy`, and any program linked against the system OpenSSL without application-level changes. The `EVP_SIGNATURE-SLH-DSA` man page documents the API surface.

### Meta's PQC migration framework (April 2026)

Meta published its PQC migration playbook in April 2026 — the most detailed hyperscaler account published to date. Key contributions:

- **PQC Migration Levels**: a 5-level maturity ladder (PQ-Unaware → PQ-Aware → PQ-Ready → PQ-Hardened → PQ-Enabled) that gives organizations a structured self-assessment.
- **Six-step methodology**: Prioritization (by attack type: offline HNDL vs online Shor's), cryptographic inventory (automated discovery + developer reporting), external dependency mapping, PQC-secure component design, phased rollout, and guardrails.
- **Meta reports** it has reached PQ-Enabled for portions of internal traffic, showing that production-scale PQ deployment is operationally tractable at internet company scale.
- **Meta cryptographers are co-authors of HQC** (NIST's fifth selected algorithm), underscoring that assumption diversity (lattice + code-based) is part of the serious migration strategy.

### SLH-DSA security analysis (ePrint 2026/632)

A May 2026 ePrint paper, *"A tight security analysis of the FIPS-205 standard (SLH-DSA)"*, provides the first comprehensive formal security treatment of the finalized SPHINCS+ / SLH-DSA specification. The paper examines the HORST and hypertree layers, the FORS signing scheme, and the SHA-256/384/512 and SHAKE-256 variants across all parameter sets. The analysis confirms the security properties assumed in the FIPS 205 standardization, providing additional cryptanalytic confidence for deployments using SLH-DSA as the conservative backup for ML-DSA in long-lived archival signatures.

### OpenPGP PQC exploration begins

DidiSoft reported in October 2024 that the OpenPGP / LibrePGP specification effort is exploring ML-KEM keys and SHA-3-based signatures — a necessary step if email encryption, code signing, and key certificates are to survive a quantum computer. The RFC 9580 (July 2024) baseline does not yet include PQ algorithms; the next OpenPGP message format update is the likely vehicle for formalizing ML-KEM key packets and PQ signature packets. Adoption depends on HSM support, key-size budget in certificate chains, and GnuPG / Sequoia-PGP / OpenPGP.js library updates. This is early research, not production — but the trajectory is established.

### wolfSSL critical ML-DSA defect (CVE-2026-5194, April 2026)

wolfSSL v5.9.1 (April 8, 2026) patched **CVE-2026-5194**, a critical vulnerability in ML-DSA (and ECDSA/EdDSA) signature verification: missing hash/digest size and OID checks allowed digests smaller than the algorithm permits to be accepted. The flaw was reported by **Nicholas Carlini of Anthropic** and affects any wolfSSL build with both ECC and ML-DSA enabled doing certificate verification. This underscores that PQ signature verification is not automatically safe by virtue of being standardized — the verification logic must also enforce algorithm-specific constraints correctly, and this class of bug is subtle enough to evade existing test vectors (KAT tests). Deployments using wolfSSL for PQ certificate validation should update immediately.

### liboqs: ML-DSA native v1.0.0-beta2, SHA3-512 fix (May 2026)

liboqs activity on `main` in late May 2026 confirms active maintenance:

- **2026-05-27**: `mldsa-native` updated to `v1.0.0-beta2` with full and extended test suites enabled. This is the native (non-hydrogen) ML-DSA implementation, now approaching a stable v1.0.0 release.
- **2026-05-27**: Patched an **AVX512VL implementation bug in SHA3-512** (`#2442`) — incorrect incremental absorption that would produce wrong hashes when processing data in multiple steps. The AVX512 code path is critical for high-throughput applications; any code using liboqs's SHA3-512 for incremental hashing should verify its version.
- **2026-05-22**: Added NIST LMS signature verification KATs (`#2435`), expanding hash-based signature coverage in the test suite.

These commits postdate the May 23 vault state and indicate the PQ reference library is actively hardening after the v0.15.0 (November 2025) release.

### Production ML-DSA implementations: ePrint audit findings (ePrint 2026/1032)

A formal academic paper published in 2026, *"When Removing Reductions Goes Wrong: Auditing Reduction Placement in Production ML-DSA Implementations"* (ePrint 2026/1032), presents a **certificate-backed audit methodology** for ML-DSA reduction placement across eight libraries. Key findings:

- The audit uncovered a **previously unreported defect in wolfSSL's `WOLFSSL-DILITHIUM-SMALL` memory-optimized path**: omitted post-matrix-multiplication Montgomery reductions cause integer overflow, non-conformant arithmetic, and signing failure. Critically, the defect **survives the existing KAT (Known Answer Test) vectors**, meaning standard compliance testing alone did not catch it.
- The root cause is that reduction omissions for performance look locally correct but are **inter-procedurally load-bearing**: a site that appears redundant in isolation is required for correctness at a later `InvNTT` stage.
- The audit methodology uses SMT-LIB2 certificates with core integer-bound lemmas cross-checked in Coq, establishing a replicable framework for other libraries.

This is the first systematic post-standardization audit of ML-DSA production code, and it shows that deployment quality assurance requires formal methods — KAT vectors are necessary but not sufficient.

### Lattice cryptanalysis advances: CoNAN and dual attacks (ePrint 2026/1041, 2026/1048)

Two 2026 ePrint papers advance the understanding of ML-KEM/ML-DSA security:

- **ePrint 2026/1041 — CoNAN**: Introduces a structure-aware framework for lattice security estimation, showing that algebraic structure in NTRU-like and structured LWE schemes can enable **algebra-induced homomorphisms** that yield lower-dimensional lattice representations and more realistic (sometimes 60+ bits lower) security estimates than generic lattice estimators. Specifically identifies LWE over noncommutative group rings and semidirect products as potentially degrading concrete security. This is relevant for evaluating whether parameterized variants of Kyber/Dilithium maintain their stated security levels.
- **ePrint 2026/1048 — Unified Dual Attack Analyses**: Provides a rigorous covariance-based framework for estimating the score distribution in LWE dual attacks, finding that prior variance estimates (including Bashiri and Wiemers, JMC 2025) perform poorly in medium-to-high dimensions. The paper establishes that the independence assumptions underlying many dual attack analyses are flawed, which may tighten attack complexity estimates. While no claim is made that ML-KEM or ML-DSA parameters are broken, this line of work reinforces that security levels should not be treated as static — cryptanalytic confidence continues to evolve.

### PQ e-voting and unified FPGA Kyber/Dilithium (ePrint 2026/1008, 2026/984)

- **ePrint 2026/1008**: *PQKryvos* — a post-quantum e-voting system using lattice-based commitments and hash-based GPZKPs, achieving public verifiability and public tally-hiding simultaneously. The design is PQ-secure (lattice assumptions) and demonstrates that privacy elections over encrypted ballots are compatible with quantum safety.
- **ePrint 2026/984**: A quantum algorithm for **discrete Gaussian sampling** on lattices that is asymptotically quadratically faster than its classical counterpart, with applications to both lattice-based signatures (speeding up signing or key generation) and to solving hard lattice problems (SVP, SIS). The dual-use nature — improving both attack and defense — is notable for long-term PQC planning.

### NIST additional signature schemes: SQIsign, MPC-itH developments

NIST's ongoing competition for **additional post-quantum digital signature schemes** (the "on-ramp" or "round 2" process) continues to evaluate submissions including:

- **SQIsign** (isogeny-based, ePrint 2026/1031): Compact quaternion algorithms for SQIsign are being optimized, reducing signature and public key sizes further. SQIsign's isogeny-based construction provides diversity from lattice assumptions — important if lattice problems turn out to be weaker than assumed.
- **MPC-in-the-Head (MPCitH)** schemes: A unified framework for **TCitH** (Ternary Contentious PoW / Threshold Computation) on embedded Cortex-M4 devices (ePrint 2026/1029) demonstrates that MPCitH-based signatures are viable on constrained hardware with 99% stack usage reduction versus baseline. VOLE-itH variants offer shorter signatures but more memory; TCitH wins on embedded.
- **Miraidon** (MinRank-based, ePrint 2026/997): A new family of MinRank-based PQ signatures built from a novel ZK proof system, with competitive key sizes and the first linkable ring signature from MinRank.

| Protocol | Status | Details |
|---|---|---|
| **TLS 1.3** | Hybrid in production | Chrome, Firefox, Safari-derived stacks (iOS 26+), Cloudflare (>65% traffic), Google edge, AWS KMS/SecretsManager/ACM/S3 (April 2026), and Go 1.24+ support X25519MLKEM768; Apple iOS 26 defaults to PQ TLS via URLSession. |
| **SSH** | Hybrid KEX in production | OpenSSH 9.0+ supports `sntrup761x25519-sha512`; OpenSSH 9.9+/10.x supports `mlkem768x25519-sha256`. Host/user authentication is still classical by default. |
| **Signal (PQXDH)** | Production since 2023 | Hybrid X3DH + ML-KEM-1024 for initial keys. |
| **Apple iMessage (PQ3)** | Production since 2024 | Post-quantum ratcheting. iOS 26 extends ML-KEM to TLS via URLSession and Network.framework (default-on since late 2025). |
| **Apple iOS 26 TLS** | Production since WWDC 2025 | ML-KEM-768 and ML-KEM-1024 available in CryptoKit; hybrid X25519MLKEM768 default for URLSession and Network.framework on iOS 26, macOS Tahoe 26, visionOS 26. |
| **GnuPG / OpenPGP** | Early | PQC support is emerging; not a default mainstream deployment path. |
| **Cloudflare IPsec** | GA since Apr 2026 | TLS 1.3 with hybrid ML-KEM in control plane, IPsec ESP via RFC 9370 / draft-ietf-ipsecme-ikev2-mlkem; Cisco and Fortinet interoperability confirmed. |
| **Cloudflare Magic Transit IPsec / IKEv2** | Closed beta → GA | ML-KEM-768 or ML-KEM-1024 with DH group 20; now generally available per April 2026 changelog. |
| **AWS ML-KEM** | GA since Apr 2026 | KMS, Secrets Manager, ACM, Payment Cryptography, S3 — hybrid TLS by default for SDK clients. |
| **WireGuard / VPNs** | Product-specific | Native WireGuard PQ is still in progress; some VPN products layer ML-KEM in their own clients or control planes. |
| **Kyber Ransomware** | Active since Sep 2025 | First confirmed criminal use of NIST-standardized ML-KEM-1024; dual-layer with X25519 + AES-256. Detected April 2026 by Rapid7. |
| **wolfSSL ML-DSA** | Patched Apr 2026 | CVE-2026-5194: missing OID/digest-size checks in ML-DSA verification (critical); also affects ECDSA/EdDSA. Reported by Nicholas Carlini (Anthropic). |

## Quantum threat timeline

| Year | Expected Milestone |
|---|---|
| ~2030 | Cryptographically relevant quantum computer (CRQC) possible |
| ~2028-2030 | Grover's algorithm makes AES-256 brute-force feasible (with significant quantum resources) |
| Now | "Harvest now, decrypt later" active — adversaries recording encrypted traffic |
| 2024-2026 | Migration window — upgrade before CRQC exists |

The "harvest now, decrypt later" threat is immediate. Any data with secrecy requirements beyond ~2030 should use hybrid classical+PQ encryption now.

## Updated deployment status (June 2026)

### Bernstein's "Exploiting ML-DSA bugs" — the 2026 implementation-maturity event

Daniel J. Bernstein (cryptographer behind Ed25519, Curve25519) published a 59-page paper on **2026-06-01** providing two open-source attack demonstrations against ML-DSA (FIPS 204) signature implementations. **Both attacks recover the secret key in under one second on a single laptop core**, then forge arbitrary signatures passing standard verification. Key findings:

- **Two attack classes**: AABBCC coefficient-repetition (Dilithium 1.0 bug class, 2018) and nonce repetition (PS3 ECDSA disaster analog, 2010).
- Both attacks pass standard functionality tests including KATs — the only catching method is **cross-implementation checksum comparisons using derandomized RNGs**, applied inconsistently.
- Bernstein projects **~25% of ML-DSA libraries will ship with severe vulnerabilities** at initial release. ~18% of 2027 ML-DSA keys will be on vulnerable software (vs ~2% for Ed25519).
- **Solo ML-DSA produces ~10× more breakable keys than hybrid Ed25519+ML-DSA** for the first 5-10 years after quantum computers arrive.
- Directly challenges the April 2026 position of Filippo Valsorda that hybrid ECC+ML-DSA signatures are unnecessary.

**Implication for ungovernable systems**: any high-value signing key — Nostr npubs, ENS names, code-signing chains, certificate authority keys, blockchain validator keys — should use **hybrid Ed25519+ML-DSA** until ML-DSA implementations have a multi-year production track record. See [Post-Quantum Saturday — June 20 2026 Weekly Update](/briefings/post-quantum/2026-06-20/) for full analysis.

### NIST IR 8610 — Round 3 selection for additional signatures

On **2026-05-14**, NIST announced **9 third-round candidates** for additional post-quantum digital signature schemes, down from 14 second-round: **FAEST, HAWK, MAYO, MQOM, QR-UOV, SDitH, SNOVA, SQIsign, UOV**. Five were eliminated. Round 3 is expected to last ~2 years; the 7th NIST PQC Standardization Conference is targeted for late spring/early summer 2027. The four families (lattice, isogeny, multivariate, MPCitH) provide deliberate diversity against any single cryptanalytic breakthrough.

**Operational relevance**: Round 3 finalists that could displace FN-DSA / ML-DSA for specific use cases:
- **SQIsign (148 byte cat-1 signature)** — isogeny-based; smallest combined pubkey+signature of any PQC candidate
- **UOV (96 byte cat-1 signature)** — multivariate; competing with ECDSA on signature size
- **HAWK** — lattice; backup if standard lattice problems weaken

**No Round 3 candidate is production-ready in 2026** — they are research-track for the 2027-2028 standardization window.

### liboqs CVE cluster — XMSS / XMSS^MT

A cluster of three related advisories for stateful hash-based signatures (XMSS and XMSS^MT) was published on **2026-05-29**, all fixed in the upcoming liboqs v0.16.0:
- **CVE-2026-44518** — unvalidated caller-supplied `signature_len` in wrapper layer (5.3 Medium)
- **CVE-2026-46344** — OOB read via OID-controlled parameter mismatch in `xmss_sign_open` (5.3 Medium)
- The original 2025 disclosure (related underlying issue in `xmss_commons.c:194`)

**Reachable from any caller of `OQS_SIG_STFL_verify`** that accepts a public key from an untrusted source (firmware updates, TUF metadata, certificate stores). The primary observable effect is a process crash (DoS); no mechanism exists for OOB data to influence verification or leak. Apply the patch from `main` branch or pin to a vendor-patched fork until v0.16.0 ships.

### RustCrypto `ml-dsa` signature malleability (CVE-2026-24850)

A **regression bug** in the RustCrypto `ml-dsa` crate (since v0.1.0-rc.2) accepted ML-DSA signatures with **duplicate hint indices**, breaking SUF-CMA. Root cause: a non-strict monotonic check (`<=` instead of `<`) in `ml-dsa/src/hint.rs`. Reported by Oren Yomtov (Fireblocks). Fixed in v0.1.0-rc.4 with a one-character change.

**This is the textbook example of the "passes KAT, fails spec" bug class** that Bernstein's paper generalizes. A one-character code change produces an implementation that passes all standard tests but violates FIPS 204. The lesson: **spec compliance is not implementation correctness**.

### OpenSSL 4.0.0 + 4.0.1 — TLS-only, FIPS 140-3, PQC extensions

- **OpenSSL 4.0.0** (2026-04-14) — first major OpenSSL release since 3.0 (2021). **First TLS-only architecture** (SSLv2/SSLv3 removed). **FIPS 140-3 module** validated. New PQC primitives: **`curveSM2MLKEM768`** (hybrid KEM with SM2 for Chinese compliance), **`ML-DSA-MU`** (multi-user digest algorithm), cSHAKE updates. Engine support removed; `ASN1_STRING` made opaque; `c_rehash` removed (use `openssl rehash`).
- **OpenSSL 4.0.1** (2026-06-09) — coordinated security patch day across **5 branches** (4.0.1, 3.6.3, 3.5.7, 3.4.6, 3.0.21). 17 CVEs fixed in 4.0.1 alone. None are PQ-specific, but the platform is now the reference FIPS 140-3 + PQC stack.

### mldsa-native v1.0.0-beta2 (2026-05-27)

The PQCA-maintained, **formally verified ML-DSA implementation** reached its second beta:
- **C backend**: production-ready, **formally verified with CBMC** for memory safety, type safety, absence of (certain types of) undefined behavior.
- **AArch64 and x86_64 backends**: growing HOL Light proofs of functional correctness, memory safety, secret-independent execution.
- Tested against all official NIST ACVP ML-DSA test vectors.
- **AWS adopted mldsa-native in production** during May 2026.

This is the **most stringently verified open-source ML-DSA implementation** as of June 2026. v1.0.0 stable is expected within 2-4 weeks.

### Cloudflare PQ traffic holding >65%

Cloudflare Radar data through June 2026 shows PQ-encrypted HTTPS traffic in the **65-70% range** across major countries (India 70.6%, France 67.1%, Malaysia 62.0%, Saudi Arabia 60.1%). The **iOS 26 inflection point** of late September 2025 (where a single iOS update moved global share from 29% to 52% in about a week) is now a steady state. Cloudflare's **2029 target for full PQ including authentication** (announced April 7, 2026) remains the reference roadmap.

## Updated deployment status (August 2026)

### IETF 126: ML-KEM in TLS reaches IESG; ML-DSA in TLS advancing

At IETF 126 (Vienna, July 20–24, 2026), the TLS working group confirmed the standardization status of PQ algorithms in TLS 1.3:

- **ML-KEM key exchange** (`draft-ietf-tls-mlkem`): **IESG Processing** — the final editorial/approval stage before RFC publication. This formalizes the hybrid X25519MLKEM768 key exchange already deployed by Chrome, Cloudflare, AWS, and Apple.
- **ML-DSA authentication** (`draft-ietf-tls-mldsa`): **Active WG draft**. RFC expected August 2026 per Cloudflare's timeline.
- **Composite ML-DSA signatures** (`draft-ietf-lamps-pq-composite-sigs`, LAMPS WG): **WG Last Call** since March 2026; RFC target Q4 2026. Defines how to combine ECDSA + ML-DSA into a single X.509 certificate.
- **Merkle Tree Certificates** (`draft-ietf-plants-merkle-tree-certs`, PLANTS WG): **WG Last Call**. See [Merkle Tree Certificates](/kb/merkle-tree-certificates/) for the full deep dive.
- **RFC 9958** (June 2026): *Post-Quantum Cryptography for Engineers* — published as an informational RFC by the PQUIP WG. Reference document for engineers new to PQC.

**Implication**: The ML-KEM key-exchange standardization is essentially complete. The next frontier is PQ authentication — ML-DSA in X.509 certificates and the Merkle Tree Certificate alternative. First ML-DSA certificates in the public Web PKI are expected early 2027.

### Merkle Tree Certificates: the PQ Web PKI path

Let's Encrypt (June 3, 2026) committed to **Merkle Tree Certificates (MTCs)** as its path to PQ web authentication — staging late 2026, production 2027. Chrome identified MTCs as its preferred approach. Cloudflare and Chrome are testing MTCs on live internet traffic.

MTCs solve the PQ signature-size problem by batching certificates into a Merkle tree and signing only the root. Each certificate carries a compact inclusion proof (O(log n) hashes, ~384 bytes) instead of a full ML-DSA signature (~3.3 KB). This dramatically reduces per-certificate overhead while maintaining PQ security.

See [Merkle Tree Certificates](/kb/merkle-tree-certificates/) for the complete analysis.

### CISA PQC Product Categories (July 23, 2026)

CISA published operational guidance for EO 14412 procurement requirements, categorizing technologies by PQC readiness:

- **"Widely Available" PQC** (procure PQC-only): cloud platforms, web browsers/servers, chat/messaging, endpoint security.
- **"Transitioning" PQC**: networking hardware (routers, firewalls), HSMs/CAs/IdPs, email servers/clients, databases.

This creates a vendor checklist: federal procurement will demand PQC-only products in "widely available" categories immediately.

### Cloudflare's "ML-DSA will have to do"

Cloudflare (Westerbaan & Patton, July 2026) argued that despite ML-DSA's larger signatures (2.4–4.6 KB vs. 64 bytes for Ed25519), it is the only PQ signature ready for the first migration. Better alternatives (SQIsign 148-byte sigs, UOV 96-byte sigs, HAWK 555-byte sigs) are all NIST Round 3 candidates, years from standardization. ML-DSA certificates' path: hybrid ML-DSA cert standard expected July 2026, ML-DSA-in-TLS RFC expected August 2026, first WebPKI certs early 2027.

### Go 1.27: ML-DSA in standard library

Go 1.27 adds `crypto/mldsa` to the standard library, following Go 1.24's `crypto/mlkem`. This brings PQ signatures to the entire Go cloud-native ecosystem (Kubernetes, Terraform, Docker, Consul) without external dependencies.

### Global Risk Institute: 28–49% CRQC probability in 10 years

The GRI / evolutionQ Quantum Threat Timeline Report 2025 (published April 2026) puts expert-estimated CRQC probability at **28–49% within 10 years** (record high) and **51–70% within 15 years**. This is the survey cited in EO 14412's rationale and Google's 2029 timeline.

### EO 14412 milestones

The July 2026 deadline for federal agencies to identify PQC migration leads has passed. Next milestones: September 2026 OMB guidance on migration plans; September 21, 2026 FIPS 140-2 sunset; December 2030 key establishment deadline; December 2031 signature deadline.

### G7 coordinated PQC roadmap

The G7 Cyber Expert Group issued a coordinated PQC transition statement (January 13, 2026), establishing 2030 as the de facto global deadline for critical infrastructure PQ migration across G7 nations.

## Updated deployment status (September 2026)

### Pure ML-KEM for TLS approved; ML-DSA-in-TLS frozen under appeal

On **September 3, 2026** the IESG approved `draft-ietf-tls-mlkem-10` (pure ML-KEM-512/768/1024 NamedGroups for TLS 1.3, Informational, registry marking **Recommended=N**); IANA action moved to In Progress. Hybrid ECDHE+ML-KEM was already published as **RFC 10024** (Proposed Standard, August 2026). Both options now exist as citeable documents; **operational guidance is unchanged — deploy hybrid**. Bernstein's four-part Last Call filing (75 sourced, non-withdrawn objections) and the unpublished rough-consensus weighting remain the substance of a signalled RFC 2026 complaint, which approval does not answer.

By contrast, `draft-ietf-tls-mldsa-05` was approved and announced **July 8, 2026** and held the same day on receipt of an appeal request (IESG state reverted to *Approved-announcement to be sent::AD Followup*, IANA action **On Hold**, action holder Deb Cooley). It has not moved since — the PQ *authentication* RFC track is procedurally stuck while the key-exchange track finished.

### Corrected status: Merkle Tree Certificates are earlier-stage than previously recorded

`draft-ietf-plants-merkle-tree-certs-05` is **WG Document / I-D Exists** — no shepherd, no responsible AD, no intended RFC status, last revision 2026-07-06. Earlier vault entries recorded "WG Last Call," which overstated its position. Let's Encrypt's staging-late-2026 / production-2027 commitment is unchanged. See [Merkle Tree Certificates](/kb/merkle-tree-certificates/).

Meanwhile `draft-ietf-lamps-pq-composite-sigs-19` (composite ECDSA+ML-DSA in one X.509 certificate) reached the **RFC Editor queue** (RFC-Ed-Ack, First Edit, Proposed Standard) as of 2026-08-26 — the enterprise/private-PKI path will likely publish before any public-web PQ authentication document.

### Cryptanalysis: the results that bit landed on FHE, not ML-KEM

- **SVP in 2^(0.73134n+o(n)) classical time**, 2^(n/2) space (ePrint 2026/1587, Gao–Feng–Hu), beating the ADRS 2^(n+o(n)) classical bound *and* the best worst-case quantum bounds (2^0.9497n / 2^0.8345n with QRAM). Asymptotic worst-case exact SVP; no effect on deployed ML-KEM parameters, which are set by Core-SVP against sieving at practical block sizes.
- **Enhanced hybrid decoding against Module/Ring-LWE** (ePrint 2026/366, Hou–Jiang, CRYPTO 2026) exploits the Z_q[x]/(x^N+1) ring structure for a linear-in-N improvement in the sparse-secret setting, 17×–114× faster than prior art on broken benchmarks, and drops **12 of 16 published FHE sparse Ring-LWE parameter sets below their targeted 128-bit level** (up to 13 bits). ML-KEM does not use sparse secrets and is out of scope — but this is the counterexample to "algebraic structure has never been exploited to accelerate attacks."
- **Classic McEliece** got a costing companion to August's quasipolynomial distinguisher: Saarinen's Holdout key-recovery arithmetic model (ePrint 2026/1786) finds a 2^114.35 supplier-complexity floor across 19,338 singleton configurations, explicitly **not a break**, published as a living tracking document.

### Implementation layer: verified backends, line-rate ML-DSA

mldsa-native v2.0.0 (2026-08-07) is that project's first stable release — C90, SLOTHY-optimized Neon/AVX2 backends, memory- and type-safety proofs — and both it and mlkem-native v2.0.0 landed in **liboqs main** (Aug 31 / Sep 3); the current liboqs release is still 0.16.0. WeaveTLS (ePrint 2026/1828) executes ML-DSA authentication across concurrent mTLS connections via a stackless OpenSSL continuation in nginx, giving 2.81–4.31× one-core throughput *and* collapsing the client-visible rejection-timing signal (correlation 0.063 at concurrency 16, 0.008 at 64). OpenSSL shipped a multi-CVE security release across 4.0.2 / 3.6.4 / 3.5.8 on **August 25** — every PQ pilot on 3.5+ needs it.

### Policy clock: three dates inside four weeks

| Date | Event |
|------|-------|
| September 16, 2026 | GSA 2026 Post-Quantum Cryptography Summit (hybrid; .gov/.mil only) |
| September 21, 2026 | FIPS 140-2 certificates → **Historical**; only FIPS 140-3 for new federal procurement (validation backlog averaging 500+ days) |
| October 22, 2026 | **OMB M-26-15** deadline: every civilian agency submits its PQC Migration Plan to OMB and ONCD |

M-26-15's five phases run 2026→2035, with **key establishment by 2030 and signatures by 2031** for HVAs and high-impact systems — the same one-year signatures-trail-confidentiality gap visible in Google Cloud's roadmap and in the IETF document states above. NSS remain under CNSA 2.0.

### Ethereum retired an eight-year hash bet

On **August 13, 2026** EF researcher Justin Drake announced Ethereum L1 is abandoning Poseidon for SHA-2 or BLAKE2s; the $992K Poseidon1 Collision Prize (scheduled to January 2029) had been paused August 1. Nobody broke full-round Poseidon — binary-field proof systems (Binius; Diamond–Posen, EUROCRYPT 2025) made standard bit-oriented hashes cheap enough to prove that an arithmetization-friendly hash was no longer necessary. With lean Ethereum making the hash the single primitive across consensus (leanXMSS aggregate signatures, ~3,000 bytes vs 96 for BLS), data availability, and zkVM, and ~898K active validators implying roughly 374,000 hash verifications/second, the hash choice *is* the roadmap. **The transferable lesson: a primitive chosen to fit the performance constraint of its moment becomes a liability when the constraint moves, and constraints move faster than confidence accumulates around a young design.** See [STARKs](/kb/starks/) and [Bitcoin PQ Migration](/kb/bitcoin-post-quantum-migration/).

Full detail in [Post-Quantum Saturday — September 05 2026 Weekly Update](/briefings/post-quantum/2026-09-05/).

## Updated deployment status (Late September 2026)

### Both pure PQ-TLS documents re-blocked under appeal on the same day

On **September 24, 2026**, Deb Cooley (Security AD) re-blocked both `draft-ietf-tls-mlkem` (pure ML-KEM, had been "Approved-announcement sent" since Sept 3) and `draft-ietf-tls-mldsa` (pure ML-DSA, cleared a 65-day appeal on Sept 11), with the canonical comment: *"The wg chairs and AD have received complaint/appeals on the processing of this document. While the complaints/appeals are being reviewed, the document is being held ..."* This is the **Ken Kubota appeal** (escalated from TLS chairs → Security AD → IESG, each layer declining to process "in its current form") per the [Sept 25 freenode report](https://freenode.net/article/ietf-rejects-appeal-on-ml-kem-tls-consensus-and-nsa-conflict-claims). The substantive unaddressed claim is that the chairs refused to release the detailed tallies behind the "roughly seven in ten" rough-consensus figure.

**Operational impact: zero on cryptographic primitives; one on TLS authentication rail.** ML-KEM-768/1024 and ML-DSA-65/87 are unaffected at every parameter set. Only the IETF-published *wire-level deployment of those primitives in TLS 1.3* is held. Hybrid `X25519MLKEM768` (RFC 10024) remains the citeable, cite-acceptable default. The CNSA 2.0 procurement clock (Jan 1, 2027 = 97 days out) does not require IETF publication of either document; FIPS-validated implementations are sufficient.

A new **mlkem-11** was uploaded Sept 16 by Deirdre Connolly (Selkie Cryptography), with IANA review at "IANA OK - Actions Needed" — the IANA registry step is procedurally complete; only the RFC Editor queue position is gated by the appeal.

### Authentication-side PQ-Web-PKI rail shows first collective forward motion since June

In a 48-hour window (Sept 21–23), two documents that had been static for ~60 days moved:
- **`draft-ietf-plants-merkle-tree-certs-06`** uploaded Sept 21 by David Benjamin (Google) — first revision since -05 in June. Document remains WG Document / I-D Exists. See [Merkle Tree Certificates](/kb/merkle-tree-certificates/).
- **`draft-ietf-lamps-pq-composite-sigs`** moved from "In Progress (First Edit)" to "Awaiting Second editor" on Sept 23 — the first forward motion in 63 days for the composite ML-DSA in X.509 PKI document. ~2–6 weeks further to publication.

The TLS-side rail (pure ML-KEM, pure ML-DSA) is held; the LAMPS / PLANTS / JOSE side is advancing. The institutional dispute on pure PQ-TLS is the gating constraint on the TLS authentication rail specifically.

### Two consequential cryptanalytic ePrints in 7 days

- **ePrint 2026/2137 (Sept 21, Jahandideh, Radboud)**: single-trace key-recovery from ML-KEM key generation. The CBD (centered binomial distribution) sampler produces coefficients with small Hamming weight (k=2 for ML-KEM-512/768, k=3 for ML-KEM-1024) — small domain → high signal-to-noise in a single side-channel trace. The paper provides a countermeasure (**q-randomization**: store `v + r·q` with random nonzero r, raising block size from 129 back to 611 → ~4 bits of security loss instead of >140) at the cost of 937 bytes of firmware. **Not a primitive break — an implementation hardening result.** See [ML-KEM](/kb/ml-kem/) §implementation-hardening.
- **ePrint 2026/2131 (Sept 20, Shea/Haller/Suhl/Heninger/Thomé)**: with a signing oracle, **even RSA-4096 does not appear to meet a 128-bit security level**. The SNFS (special number field sieve) applies to signing-key structure in a way factoring estimates don't capture, yielding 15–30 bits lower attack costs than factoring estimates suggest. The authors frame this as "classical cryptanalytic evidence in favor of moving away from RSA entirely during the current post-quantum transition."

### The pqc-forum McEliece / HAWK synthesis — Mattsson recommends ML-KEM + HQC hybrid

A [Sept 25 freenode synthesis](https://freenode.net/article/pqc-timelines-under-pressure-after-hawk-collapse-and-mceliece-parameter-shocks) of pqc-forum discussion surfaced concrete deployment recommendations:
- **John Mattsson (Ericsson)**: ML-KEM + HQC hybrid for diversification across hardness assumptions and better performance than FrodoKEM alone; FrodoKEM explicitly *not* the conservative default given thinner deployment and scrutiny than ML-KEM.
- **D.J. Bernstein**: challenged naive bit-operation tallies on McEliece attacks as memory-routing-bound, not gate-bound.
- **Demi Marie Obenour**: OpenSSH precedent — Streamlined NTRU Prime shipped before ML-KEM finalized as FIPS 203 — operators who control both endpoints can field research constructions like MIKE hybridized with ECDH.
- **Bas Westerbaan (Cloudflare)**: adoption graphs showing uneven post-quantum uptake across human-driven and automated clients.

The operational upshot: **ML-KEM + HQC hybrid is now the most explicitly-named diversification strategy on the standards track**. For freedom-tech deployers with the freedom to use non-finalized primitives, this is the standards-aligned diversification path. See [HQC](/kb/hqc/).

### Library state at September 26

- **liboqs `main`** added AES-192 support (commit b196b57, Sept 24), fixed XMSS code-scan issues (#2577 Sept 21), and shipped a security fix for OOB access in `xmss_core_sign` on secret-key OID mismatch (#2511 Sept 21). Current tagged release remains **0.16.0** (2026-07-09). 3,071 stars.
- **AWS-LC v5.10.0** (Sept 23) — fifth release of September. Hardening sweep across multiple code paths; OpenSSL-compatible rehash -compat support; `ca`-command failure-mode fix.
- **OpenSSL 4.1.0-beta1** (Sept 23) — first beta of the 4.1 feature line, three weeks after alpha1. PQ-capable-branch security releases (4.0.3 / 3.6.5 / 3.5.9 from Sept 9) had no fresh advisory in this window.
- **oqs-provider** commit 36cafae0 (Sept 19) updated MAYO, MQOM, and SNOVA to NIST Round 3 variants; tagged 0.12.0-rc2 Sept 16.

Full detail in [Post-Quantum Saturday — September 26 2026 Weekly Update](/briefings/post-quantum/2026-09-26/).

## Primary sources

- NIST FIPS 203 / 204 / 205 / 206 — `csrc.nist.gov/projects/post-quantum-cryptography`
- NIST IR 8610 (Additional Signatures Round 2 Status Report, May 2026) — `nvlpubs.nist.gov/nistpubs/ir/2026/NIST.IR.8610.pdf`
- RFC 9980: Post-Quantum Cryptography in OpenPGP (June 2026) — `rfc-editor.org/rfc/rfc9980`
- liboqs: https://github.com/open-quantum-safe/liboqs
- PQCA Blog: https://pqca.org/blog/
- Bernstein & Lange: *Post-quantum cryptography* — Nature 2017 (survey)
- Bernstein: *Exploiting ML-DSA bugs* (June 2026) — `cr.yp.to/papers.html#mldsa`
- Bernstein: *Understanding lattice risks* (June 2026) — `blog.cr.yp.to/20260630-risk.html`
- Ogilvie: *Concrete Hardness Gap Between MLWE and LWE* (Feb 2026) — `eprint.iacr.org/2026/279`
- Kobeissi: *Verification Theatre* (Feb 2026) — `eprint.iacr.org/2026/192`
- *Signal PQXDH* spec — `signal.org/docs/specifications/pqxdh`
- Apple: *iMessage PQ3* — `security.apple.com/blog/imessage-pq3`
- BSI PQC Joint Statement (2025): `bsi.bund.de`
- NCSC PQC Migration Timelines: `ncsc.gov.uk/guidance/pqc-migration-timelines`
- Meta Engineering: *Post-Quantum Cryptography Migration at Meta* — `engineering.fb.com/2026/04/16/security/post-quantum-cryptography-migration-at-meta-framework-lessons-and-takeaways/`
- Ars Technica: *In a first, a ransomware family is confirmed to be quantum-safe* — `arstechnica.com/security/2026/04/now-even-ransomware-is-using-post-quantum-cryptography/`
- Cloudflare PQC roadmap: `blog.cloudflare.com/post-quantum-roadmap/`
- Cloudflare: *Why we cannot wait for better PQ signature algorithms* — `blog.cloudflare.com/ml-dsa-will-have-to-do`
- Cloudflare Radar (live PQ adoption stats): `radar.cloudflare.com/post-quantum`
- Forescout: *PQC Adoption Gaps* (July 2026) — `forescout.com/blog/pqc-adoption-gaps-90-percent-of-systems-are-still-not-quantum-safe`
- PostQuantum.com (Ivezic): ongoing analysis — `postquantum.com/security-pqc/`
- AWS ML-KEM announcement (April 2026): `aws.amazon.com/about-aws/whats-new/2026/04/aws-secrets-manager-post-quantum-tls/`
- OpenSSL 3.5 PQC integration: `openssl-corporation.org/files/ICMC2026-PQC.pdf`
