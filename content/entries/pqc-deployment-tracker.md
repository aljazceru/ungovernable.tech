---
title: "PQC Deployment and Libraries Tracker"
slug: pqc-deployment-tracker
type: reference
pillars: ["pqc"]
description: "A tracker of where post-quantum cryptography is actually shipping: TLS, SSH, messaging, libraries, hardware and government migration deadlines."
dek: "Operational tracker for where post-quantum cryptography is actually shipping: protocol stacks, operating systems, libraries, messaging systems, VPNs, and compliance roadmaps. This complements Overview - Post-Quantum Cryptography, ML-KEM, ML-DSA, SLH-DSA, HQC, FN-DSA Falcon, and Hybrid KEM Migration."
updated: 2026-10-17
created: 2026-05-02
origin: vault
source: "10-Post-Quantum/PQC Deployment and Libraries Tracker.md"
aliases: ["Post-Quantum Deployment Tracker", "PQC Library Tracker", "Quantum-Safe Deployment Tracker"]
tags: ["pqc", "post-quantum", "ml-kem", "ml-dsa", "tls", "ssh", "libraries", "migration", "mtcs", "mtc-draft-06", "openssl-4-1-beta2", "dtls-1-3", "ches-2026", "lightsec-2026", "sealsq", "ilwe", "omb-m-26-15", "gsa-ficam", "wolfssl"]
---

## Summary

Post-quantum cryptography has moved from research competition to production deployment. The decisive shift was NIST's 2024 publication of FIPS 203, 204, and 205, which standardized [ML-KEM](/kb/ml-kem/), [ML-DSA](/kb/ml-dsa/), and [SLH-DSA](/kb/slh-dsa/). By 2026, the practical state is uneven but no longer hypothetical:

- **Key exchange is real in production.** TLS 1.3 hybrid key exchange, especially `X25519MLKEM768`, is deployed by Cloudflare, Google-facing stacks, Go 1.24+ programs, OpenSSL 3.5-based stacks, and modern browsers / CDNs. OpenSSH has shipped PQ hybrid KEX by default since 9.0, first with `sntrup761x25519-sha512`, then with `mlkem768x25519-sha256` in OpenSSH 10.x. **RFC 10024 (PQ/T hybrid key agreement for TLS 1.3, ex-draft-ietf-tls-ecdhe-mlkem) published August 2026 as Proposed Standard** (Kwiatkowski / Kampanakis / Westerbaan / Stebila; AD Paul Wouters) — cite this, not the draft, in migration docs.
- **Messaging led early.** Signal deployed PQXDH in 2023; Apple deployed iMessage PQ3 in 2024. Both use hybrid designs rather than pure PQ trust.
- **Signatures are the laggard.** PQ signatures are standardized, but public Web PKI, code signing, package repositories, hardware attestation, blockchain signatures, and long-lived identity keys remain mostly classical. This matters because authentication failures are not only future risks; they affect whether a recorded handshake or signed artifact can be trusted later.
- **Libraries are mature enough for integration, not for complacency.** `liboqs`, `oqs-provider`, PQClean, CIRCL, RustCrypto KEMs, Go's standard library, Bouncy Castle, OpenSSL 3.5, and AWS s2n-tls provide usable building blocks. The risk is choosing obsolete pre-standard Kyber/Dilithium parameter names, non-constant-time code, or a stack that quietly falls back to classical crypto.
- **The migration pattern is hybrid + crypto-agility.** For 2026 deployments, hybrid KEMs are the safest default: combine X25519 or another classical primitive with ML-KEM, feed both secrets into a transcript-bound KDF, and keep algorithm negotiation upgradeable.

For ungovernable infrastructure, the immediate priorities are: enable hybrid TLS and SSH where available; inventory long-secrecy data stores; migrate encrypted backups and source-protection workflows; avoid exposing blockchain public keys before spend; and pressure wallet, mesh, attestation, and decentralized identity systems to publish explicit PQ roadmaps.

## Historical context

### 1994-2015: the warning phase

Shor's algorithm showed that a large fault-tolerant quantum computer would break RSA, finite-field Diffie-Hellman, DSA, and elliptic-curve cryptography. For years the problem was academically obvious but operationally distant. Symmetric primitives such as AES and hash functions were less threatened: Grover's algorithm changes security margins, but AES-256 and SHA-256-family choices are broadly viable.

### 2016-2024: NIST standardization

NIST launched its post-quantum standardization project in 2016. The competition created a public cryptanalytic gauntlet: lattice KEMs, lattice signatures, code-based schemes, hash-based signatures, multivariate signatures, isogeny systems, and MPC-in-the-head designs were proposed, attacked, optimized, and culled.

The cautionary story is SIKE: an isogeny-based finalist was dramatically broken in 2022. The lesson is not "PQC is unsafe" but "hybrid deployment is prudent while cryptanalytic confidence matures." This is why production systems generally combine classical and PQ primitives.

On August 13, 2024, NIST approved three FIPS standards:

| FIPS | Algorithm | Function | Origin | Practical role |
|---|---|---|---|---|
| FIPS 203 | [ML-KEM](/kb/ml-kem/) | Key encapsulation | CRYSTALS-Kyber | Default PQ KEM for TLS, SSH, KMS, file encryption wrappers |
| FIPS 204 | [ML-DSA](/kb/ml-dsa/) | Signature | CRYSTALS-Dilithium | General-purpose PQ signature for code signing, certs, identities |
| FIPS 205 | [SLH-DSA](/kb/slh-dsa/) | Signature | SPHINCS+ | Conservative hash-based backup; larger/slower but minimal algebraic assumptions |

NIST is also standardizing [FN-DSA Falcon](/kb/fn-dsa-falcon/) for compact signatures and selected [HQC](/kb/hqc/) in 2025 as a code-based backup KEM to diversify away from a single ML-KEM family.

### 2024-2026: deployment phase

The deployment phase is defined by libraries and defaults rather than papers. Go 1.24 introduced standard-library `crypto/mlkem` and made hybrid TLS key exchange part of the default curve preferences. OpenSSL 3.5 added ML-KEM, ML-DSA, and SLH-DSA. Ubuntu 25.10 / 26.04-era systems expose those capabilities to ordinary applications such as `curl`, `nginx`, OpenSSH, wolfSSL, rustls, and Libgcrypt. Cloudflare reports large-scale hybrid TLS use and targets full PQ security, including authentication, by 2029.

## Evidence at a glance

| Area | Current maturity | Evidence / primary source | Notes for ungovernable systems |
|---|---:|---|---|
| NIST standards | Mature | FIPS 203/204/205 approved Aug 2024; FN-DSA FIPS 206 IPD Aug 2025, final expected 2026; HQC selected Mar 2025 | Use standardized names and parameters, not pre-final Kyber/Dilithium labels in new systems. |
| **TLS 1.3** | Hybrid in production | Chrome, Firefox, Safari-derived stacks (iOS 26+), Cloudflare, Google, AWS KMS/SecretsManager/ACM (April 2026), and Go 1.24+ support X25519MLKEM768; Cloudflare >65% of human traffic using PQ as of April 2026. **Now RFC 10024 (Aug 2026, Proposed Standard).** Google Cloud LB hybrid TLS: default-on after Oct 2026, always-on after Oct 2027. | Highest-leverage easy win for websites, APIs, RPC, relays, and control planes. |
| **SSH** | Hybrid KEX in production | OpenSSH PQ page; OpenSSH 9.0+ and 10.x changes | Admin channels can often get PQ KEX by upgrading OpenSSH. Host/user signatures remain classical unless separately migrated. |
| **End-to-end messaging** | Production in leaders | Signal PQXDH spec; Apple PQ3 blog/formal analysis | Initial key agreement and ratcheting are much further along than most infrastructure stacks. iOS 26 extends ML-KEM to TLS system-wide via URLSession. |
| **iOS / Apple TLS** | GA since WWDC 2025 | iOS 26, macOS Tahoe 26, visionOS 26 ship ML-KEM-768/1024 in CryptoKit; hybrid X25519MLKEM768 default for URLSession and Network.framework. |
| **Public Web PKI signatures** | Early | CA/B Forum + browser discussions; Cloudflare roadmap | Certificates and CAs remain a hard migration problem because PQ signatures increase size and compatibility risk. |
| **Code/package signing** | Early | distro and Sigstore discussions; NIST signature standards | High priority for long-lived firmware, operating systems, and reproducible-build ecosystems. |
| **Cloudflare IPsec** | GA since April 2026 | RFC 9370 + draft-ietf-ipsecme-ikev2-mlkem; Cisco and Fortinet interoperability confirmed. |
| **AWS ML-KEM** | GA since April 2026 | KMS, Secrets Manager, ACM, Payment Cryptography, S3 hybrid TLS by default for SDK clients | Dominant cloud provider now PQ-capable at scale. |
| **Libraries** | Active | liboqs, oqs-provider, PQClean, CIRCL, RustCrypto KEMs, Go, Bouncy Castle, OpenSSL 3.5 (March 2026) | OpenSSL 3.5 is the mainstream inflection point — ML-KEM/ML-DSA/SLH-DSA available via distro packages. |
| Decentralized identity / WoT | Mostly pre-PQ | Nostr, DID, PGP ecosystems | Long-lived identity keys are a weak point. Hybrid or hash-based identity migration needs design work. |
| Blockchains | Mostly pre-PQ | [Bitcoin PQ Migration](/kb/bitcoin-post-quantum-migration/); Ethereum research | Public keys revealed on-chain are future targets. Migration is social consensus + wallet UX, not only crypto. |
| Mesh / off-grid networks | Mostly pre-PQ | [Overview - Off-Grid Networks](/kb/off-grid-networks/), [Yggdrasil](/kb/yggdrasil/), Reticulum/FIPS notes | Bandwidth and packet-size constraints make PQ harder; hybrid overlays may be simpler than native migration. |
- **Kyber Ransomware** | Active since Sep 2025 | Rapid7 analysis confirmed April 2026; Ars Technica reporting | First criminal use of ML-KEM-1024. PQC is now in both attacker and defender toolkits. |
| **FN-DSA (FIPS 206)** | IPD / finalizing | NIST 6th PQC Conference 2025; draft-ietf-cose-falcon-04 (Jan 2026 milestone); expected late 2026 / early 2027 | Final standard resolution of SUF-CMA, hedged variants, key/message-recovery mode, fixed-point signing. HSM vendors awaiting final FIPS before production support. |
| **SLH-DSA (FIPS 205)** | Mature | FIPS 205 final Aug 2024; ePrint 2026/632 security analysis; draft-ietf-cose-sphincs-plus-07 (Jan 2026 milestone) | Tight security analysis confirms SPHINCS+ framework. IETF COSE integration progressing. |
| **AWS Private CA — ML-DSA** | GA since Q2 2026 | AWS Private CA documentation; AWS blog Q2 2026 | Extends PQ signatures to private PKI hierarchies. ML-DSA-backed certificates from AWS PCA for internal CAs. Public Web PKI still pending. |
| **wolfSSL CVE-2026-5194** | Critical patched | GHSA-f5h9-5q52-qrx7; wolfSSL v5.9.1 patch | Critical ML-DSA (and ECDSA/EdDSA) signature verification bug: missing hash/digest size and OID checks allowed undersized digests. Any wolfSSL build with ECC+ML-DSA doing cert verification should update immediately. |

## Major implementations and libraries

### Open Quantum Safe: liboqs and oqs-provider

- Repository: https://github.com/open-quantum-safe/liboqs
- OpenSSL provider: https://github.com/open-quantum-safe/oqs-provider
- Maturity check, 2026-05-02 via GitHub API: `open-quantum-safe/liboqs` was active, not archived, ~2.9k stars, C, pushed 2026-05-01. `oqs-provider` was active, not archived, ~470 stars, pushed 2026-04-30.

`liboqs` remains the central prototyping and interoperability library for many PQ experiments. It is not simply a "use in production blindly" library; its value is breadth, test vectors, benchmarking, bindings, and integration with TLS/OpenSSL experiments. The older `open-quantum-safe/openssl` fork is deprecated/archived; new work should use OpenSSL 3's provider model through `oqs-provider` or native OpenSSL 3.5+ support where available.

**Use when:** testing algorithm support, benchmarking, building prototypes, integrating non-default PQ algorithms, or tracking NIST round candidates.

**Avoid when:** a system already has a well-maintained native implementation in its language runtime or TLS library. Prefer the platform default when it is current and audited.

### OpenSSL 3.5+ (GA March 2026)

- Release planning / announcement: https://openssl-library.org/post/2025-02-04-release-announcement-3.5/
- Core support: ML-KEM (FIPS 203), ML-DSA (FIPS 204), SLH-DSA (FIPS 205).
- Practical impact: any OpenSSL-backed program can negotiate or use PQ algorithms once built against 3.5+ and configured correctly. Ubuntu 26.04 LTS and derivative distributions expose PQ through the standard OpenSSL interface — `curl`, `nginx`, `haproxy`, and any linked program inherit PQ capability without application-level changes.
- Signature API: `EVP_SIGNATURE-SLH-DSA` man page documents the SLH-DSA signing interface.
- `EVP_SIGNATURE-ML-DSA` and `EVP_KEM-MLKEM` similarly for the other standards.

OpenSSL 3.5 is the inflection point for mainstream server administrators. Before OpenSSL 3.5, PQ TLS often meant BoringSSL, Cloudflare-specific stacks, patched forks, or OQS experiments. With 3.5, distributions can expose NIST-standard algorithms through ordinary package lifecycles.

**Trade-off:** support in the library does not guarantee end-to-end PQ security. You still need protocol support, group configuration, client support, and no middlebox breakage.

### Go standard library and CIRCL

- CIRCL repository: https://github.com/cloudflare/circl
- Go TLS issue / implementation discussion: https://github.com/golang/go/issues/69985
- Go source defaults: https://go.dev/src/crypto/tls/defaults.go

Go is unusually important because so much cloud-native infrastructure, Kubernetes tooling, relays, agents, reverse proxies, and decentralized infrastructure are written in Go. Go 1.24 added ML-KEM support and default hybrid TLS preferences around `X25519MLKEM768`. That means many services inherit PQ-capable TLS merely by rebuilding on a recent toolchain, provided their TLS configuration does not override curve preferences.

CIRCL is Cloudflare's Go cryptographic library and has been a key implementation bed for PQ experiments, including KEMs, signatures, HPKE-related work, and pairing/zk primitives.

**Operational caveat:** Go services that explicitly set `CurvePreferences` can accidentally disable the default hybrid group. Audit custom TLS configs.

### Meta's PQC migration framework (April 2026)

Meta's engineering blog published the most detailed hyperscaler PQC migration account to date in April 2026:

- **PQC Migration Levels**: a 5-level maturity ladder (PQ-Unaware → PQ-Aware → PQ-Ready → PQ-Hardened → PQ-Enabled). Most organizations are PQ-Aware or below.
- **Six-step methodology**: Prioritization (offline HNDL vs online Shor's attack); cryptographic inventory (automated discovery + developer reporting); external dependency mapping (standards, hardware, library maturity); PQC-secure component design; phased rollout; guardrails and monitoring.
- **Key insight**: Meta classifies applications by susceptibility to *offline* attacks (key exchange, where harvest-now-decrypt-later applies) versus *online* attacks (digital signatures, requiring a working CRQC). This distinction drives prioritization.
- **Meta reports** reaching PQ-Enabled for portions of internal traffic, demonstrating production-scale deployment is operationally tractable.
- **Meta cryptographers are co-authors of HQC**, signalling that assumption diversity (lattice + code-based) is part of serious migration strategy, not just academic interest.

### PQClean and generated bindings

- Repository: https://github.com/PQClean/PQClean
- Maturity check, 2026-05-02: active, not archived, ~900 stars, C, pushed 2026-01-09.

PQClean provides clean, portable C implementations with a consistent API and test discipline. Many language bindings and packages derive from PQClean metadata and source trees. It is valuable as a bridge from academic implementations to auditable, portable code.

**Use when:** comparing implementations, generating bindings, or needing simple C implementations for embedded experimentation.

**Caveat:** clean portability is not the same as hardened side-channel resistance on every target. Hardware leakage analysis is workload- and architecture-specific.

### Rust ecosystem

- RustCrypto KEMs: https://github.com/RustCrypto/KEMs
- `ml-kem` crate: https://lib.rs/crates/ml-kem
- rustpq/pqcrypto: https://github.com/rustpq/pqcrypto

Rust now has multiple PQ paths. RustCrypto's KEM work provides pure-Rust implementations aligned with the wider RustCrypto traits. `rustpq/pqcrypto` wraps/generates from PQClean. Which one to use depends on whether the project values pure Rust/no-std integration, compatibility with PQClean, audit status, or ecosystem fit.

**Operational caveat:** Rust cryptography projects move quickly. Pin versions, read changelogs for parameter-name changes, and avoid stale pre-standard Kyber crates when building new systems.

### BoringSSL, AWS s2n-tls, rustls, wolfSSL, Bouncy Castle

- BoringSSL is the browser/Google deployment path for hybrid TLS.
- AWS `s2n-tls` is actively maintained and used in AWS infrastructure: https://github.com/aws/s2n-tls
- rustls has PQ support paths influenced by provider and backend choices.
- wolfSSL and Libgcrypt are appearing in distribution PQ support matrices.
- **wolfSSL CVE-2026-5194 (critical, April 2026):** wolfSSL v5.9.1 patched a critical vulnerability in ML-DSA (and ECDSA/EdDSA) signature verification: missing hash/digest size and OID checks allowed undersized digests to be accepted. Reported by Nicholas Carlini (Anthropic). Affects any wolfSSL build with both ECC and ML-DSA enabled doing certificate verification. Deployments using wolfSSL for PQ certificate validation should update immediately. See: https://github.com/advisories/GHSA-f5h9-5q52-qrx7
- Bouncy Castle provides broad Java PQ algorithm coverage and is relevant for enterprise and Android-adjacent systems.

For decentralized infrastructure projects, the key question is not "does a PQ algorithm exist?" but "does the exact runtime and TLS library used by my relay, node, gateway, or wallet negotiate a hybrid group by default?"

## Protocol and platform deployments

### TLS 1.3

TLS is the most mature high-volume PQ deployment surface. `X25519MLKEM768` is the dominant hybrid group because it composes a classical X25519 secret with an ML-KEM-768 shared secret. The system remains safe if either side of the hybrid remains secure.

Cloudflare's public docs describe PQ support for TLS 1.3 and HTTP/3, note that PQ key agreements are disabled for websites in FIPS mode, and state a target of full PQ security across its product suite by 2029. Its docs also distinguish visitor-to-Cloudflare, internal Cloudflare traffic, and Cloudflare-to-origin traffic. This distinction matters: a site can be PQ-secure from browser to CDN but classical from CDN to origin unless origin connectivity is upgraded.

**Ungovernable use cases:** public relays, Nostr relays, coordination servers, package mirrors, gateways, WebRTC signaling servers, LLM inference APIs, self-hosted dashboards, and federation endpoints.

**Verification pattern:** use a recent client and check negotiated groups, e.g. OpenSSL 3.5 `s_client`, recent `curl -v`, Cloudflare's PQ test endpoint, or browser security instrumentation. Do not assume support from version strings alone.

### SSH

OpenSSH has been ahead of most infrastructure. Its PQ page says OpenSSH has offered PQ key agreement by default since 9.0 in April 2022, initially via `sntrup761x25519-sha512`. OpenSSH 10.x moves toward the standardized `mlkem768x25519-sha256` hybrid. This protects against store-now-decrypt-later for SSH session key establishment.

**Important limitation:** SSH KEX migration does not automatically migrate host keys or user authentication keys. Ed25519/RSA host keys are still quantum-vulnerable signatures. For most users, confidentiality of captured sessions improves before authentication becomes PQ.

### End-to-end messaging

Signal's PQXDH specification extends X3DH with a post-quantum KEM component. The security goal is hybrid initial key agreement: compromising only the classical curve side or only the PQ side should not reveal the shared secret. Formal analyses have examined PQXDH using tools such as ProVerif and CryptoVerif.

Apple's PQ3 for iMessage goes further than one-time initial PQ key agreement by adding post-quantum ratcheting. The IACR ePrint formal analysis of PQ3 is a useful primary research artifact for evaluating its claims.

**Ungovernable relevance:** messaging systems show that PQ migration can be hidden under product UX. Protocols like [Overview - Encrypted Messaging](/kb/encrypted-messaging/), Nostr DMs, Matrix, SimpleX, Cwtch, and off-grid messengers need similar migration strategies but must balance packet sizes, asynchronous delivery, and identity persistence.

### VPNs, IPsec, WireGuard, and overlays

VPN migration is mixed. IPsec/IKEv2 has RFC and draft work for post-quantum shared keys / KEMs. Cloudflare documents PQ IPsec and Cloudflare One Appliance deployment paths. WireGuard's base protocol remains Curve25519-centric; product-specific approaches either layer PQ in control planes or use out-of-band pre-shared secrets.

**Pragmatic pattern:** for high-stakes overlays, use hybrid TLS control channels and regularly rotated symmetric PSKs while native PQ WireGuard remains unsettled. For [Overview - Off-Grid Networks](/kb/off-grid-networks/), packet-size and bandwidth constraints make ML-KEM feasible for setup but not free.

### Operating systems and distributions

Ubuntu 25.10 and the 26.04 LTS line are a visible example of PQ becoming a distribution default: OpenSSL 3.5, OpenSSH 10.0+, and libraries such as wolfSSL/rustls/Libgcrypt expose PQ-capable paths. The Ubuntu Discourse article demonstrates `curl` negotiating `TLSv1.3 / ... / X25519MLKEM768` against a Cloudflare PQ test endpoint on a modern stack. This matters because most self-hosters do not hand-compile cryptographic libraries. PQ adoption accelerates once distro defaults carry it into normal package management.

### Criminal adoption: Kyber ransomware

The Kyber ransomware family (active since September 2025, confirmed by Rapid7 in April 2026, Ars Technica reporting April 23, 2026) is the first confirmed criminal use of NIST-standardized post-quantum cryptography. It deploys ML-KEM-1024 alongside X25519 (classical) and AES-256-CTR for bulk encryption — a hybrid scheme similar to production defender deployments. The dual-layer approach means even a future quantum computer would need to break both layers. Rapid7's Anna Širokova noted the ML-KEM implementation required "relatively little work" given liboqs availability. The operational implication: PQ is no longer a theoretical concern exclusive to defenders — it is in the adversary toolkit, making attribution harder and underscoring that PQ is operationally neutral technology.

## Migration priorities by system type

| System | First PQ step | Hard part | Recommended stance |
|---|---|---|---|
| Public HTTPS service | Enable TLS 1.3 hybrid group | Client/middlebox compatibility; origin path | Do now if stack supports it; monitor negotiated groups. |
| SSH admin access | Upgrade OpenSSH | PQ signatures for host/user auth | Do now; treat KEX and auth as separate migrations. |
| Encrypted backups | PQ-wrap archive keys | Tool maturity and recovery UX | Pilot on non-critical backups; keep classical recovery path. |
| Code signing | Hybrid signatures | Verifier compatibility and artifact bloat | Start inventory and test now; production rollout needs ecosystem coordination. |
| Hardware attestation / TEEs | PQ attestation roots | Vendor hardware cycles | Track [Overview - Confidential Computing](/kb/confidential-computing/) dependencies; ask vendors for roadmap. |
| Nostr / DIDs / WoT | Hybrid identity keys or hash-based migration | Social recovery, reputation continuity, key discovery | Research now; do not wait until identity keys are exposed long-term. |
| Blockchains | Avoid public-key reuse; PQ address migration | Consensus, wallets, UX, inactive coins | See [Bitcoin PQ Migration](/kb/bitcoin-post-quantum-migration/); migration is governance-heavy. |
| Mesh/off-grid | Hybrid session setup | Message size, energy, intermittent links | Use PQ where setup bandwidth exists; avoid bloating every packet. |
| Apple iOS / macOS apps | Default is now PQ via URLSession | None — iOS 26 ships this as the default | If targeting iOS 26+, no action needed for TLS; audit any custom TLS code that overrides default behavior. |
| AWS-based workloads | Enable hybrid TLS in SDK / service config | SDK version requirements | AWS KMS/SecretsManager/ACM now default to PQ TLS since April 2026 — no action needed for new workloads using latest SDKs. |

## Trade-offs and failure modes

### Larger handshakes and signatures

ML-KEM is compact by PQ standards but still much larger than X25519. ML-DSA signatures are measured in kilobytes, and SLH-DSA can be much larger/slower. This affects TLS ClientHello size, certificate chains, DNS records, QR-code key exchange, LoRa/mesh links, blockchain transactions, package metadata, and firmware update channels.

### Silent downgrade and false confidence

Many stacks advertise PQ capability but negotiate classical crypto because of old peers, FIPS mode, custom curve preferences, TLS termination at a CDN, or middleboxes. A system is not PQ-secure because a library supports ML-KEM; it is PQ-secure only if the actual connection negotiated a hybrid or PQ group on every relevant segment.

### Pre-standard algorithm names

Old code often refers to Kyber and Dilithium rather than ML-KEM and ML-DSA. Some pre-final parameters or encodings differ from the FIPS standards. New systems should prefer final FIPS names and implementations unless compatibility with a specific older deployment is required.

### Side channels and constant-time behavior

PQC does not remove implementation risk. Lattice schemes have decapsulation, rejection, sampling, and arithmetic paths that must avoid secret-dependent timing and memory access. Embedded and hardware-backed implementations need separate leakage evaluation.

### Authentication is harder than encryption

Hybrid KEMs can be added to a handshake without changing human-visible identities. PQ signatures are harder: certificates, public keys, fingerprints, package signatures, blockchain addresses, and WoT identities are all socially embedded. That is why key exchange is ahead and signatures lag.

### August 2026 update: IETF 126 standardization milestones

| Draft | WG | Status (Aug 2026) | Impact |
|-------|-----|-------------------|--------|
| `draft-ietf-tls-mlkem` | TLS | **IESG Processing** | Hybrid X25519MLKEM768 formally standardized |
| `draft-ietf-tls-mldsa` | TLS | Active WG Draft | ML-DSA authentication in TLS; RFC expected Aug 2026 |
| `draft-ietf-lamps-pq-composite-sigs` | LAMPS | **WG Last Call** | Composite ECDSA+ML-DSA X.509 certs; RFC Q4 2026 |
| `draft-ietf-plants-merkle-tree-certs` | PLANTS | **WG Last Call** | Merkle Tree Certificates — PQ Web PKI path |
| `draft-yusef-tls-pqt-dual-certs` | TLS (individual) | Active I-D (Jul 3, 2026) | PQ/T hybrid dual certificates |
| `draft-ietf-uta-pqc-app` | UTA | Active I-D (expires Aug 2026) | PQC recommendations for TLS applications |
| RFC 9958 | PQUIP | **Published RFC** (June 2026) | PQC for Engineers — reference document |

Additional August 2026 milestones:
- **Go 1.27**: ML-DSA added to standard library (`crypto/mldsa`).
- **CISA PQC Product Categories** (July 23, 2026): Operationalizes EO 14412 procurement requirements.
- **Cloudflare ML-DSA timeline**: hybrid ML-DSA cert standard July 2026; ML-DSA-in-TLS RFC August 2026; first WebPKI certs early 2027.
- **GRI Threat Survey**: 28–49% CRQC probability within 10 years (record high).

See [Merkle Tree Certificates](/kb/merkle-tree-certificates/) and [Post-Quantum Saturday — August 01 2026 Weekly Update](/briefings/post-quantum/2026-08-01/) for full details.

## Primary sources and documentation

- NIST FIPS approval announcement: https://csrc.nist.gov/news/2024/postquantum-cryptography-fips-approved
- NIST PQC project: https://csrc.nist.gov/projects/post-quantum-cryptography
- FIPS 203 ML-KEM: https://csrc.nist.gov/pubs/fips/203/final
- FIPS 204 ML-DSA: https://csrc.nist.gov/pubs/fips/204/final
- FIPS 205 SLH-DSA: https://csrc.nist.gov/pubs/fips/205/final
- FIPS 206 FN-DSA (Falcon) IPD: https://csrc.nist.gov/pubs/fips/206/ipd
- Open Quantum Safe liboqs: https://github.com/open-quantum-safe/liboqs
- OQS OpenSSL provider: https://github.com/open-quantum-safe/oqs-provider
- PQClean: https://github.com/PQClean/PQClean
- CIRCL: https://github.com/cloudflare/circl
- RustCrypto KEMs: https://github.com/RustCrypto/KEMs
- rustpq/pqcrypto: https://github.com/rustpq/pqcrypto
- OpenSSL 3.5 release announcement: https://openssl-library.org/post/2025-02-04-release-announcement-3.5/
- OpenSSL PQC integration (ICMC 2026): https://openssl-corporation.org/files/ICMC2026-PQC.pdf
- Cloudflare PQC docs: https://developers.cloudflare.com/ssl/post-quantum-cryptography/
- Cloudflare 2029 roadmap: https://blog.cloudflare.com/post-quantum-roadmap/
- Cloudflare Radar (live stats): https://radar.cloudflare.com/post-quantum
- OpenSSH PQ page: https://www.openssh.com/pq.html
- Go TLS ML-KEM issue: https://github.com/golang/go/issues/69985
- Signal PQXDH specification: https://signal.org/docs/specifications/pqxdh/
- Apple iMessage PQ3: https://security.apple.com/blog/imessage-pq3/
- PQ3 formal analysis: https://eprint.iacr.org/2024/1395
- Meta PQC Migration Framework: https://engineering.fb.com/2026/04/16/security/post-quantum-cryptography-migration-at-meta-framework-lessons-and-takeaways/
- Ars Technica — Kyber ransomware: https://arstechnica.com/security/2026/04/now-even-ransomware-is-using-post-quantum-cryptography/
- AWS Secrets Manager PQ TLS: https://aws.amazon.com/about-aws/whats-new/2026/04/aws-secrets-manager-post-quantum-tls/
- AWS PQC migration page: https://aws.amazon.com/security/post-quantum-cryptography/migrating-to-post-quantum-cryptography/
- PQCC international requirements: https://pqcc.org/international-pqc-requirements/
- Ubuntu PQ support in 26.04-era stack: https://discourse.ubuntu.com/t/post-quantum-support-in-the-upcoming-26-04-lts/76840
- NIST IR 8528 (HQC selection): https://vlpubs.nist.gov/nistpubs/ir/2025/NIST.IR.8528.pdf

## Open questions

- ~~When will Web PKI deploy PQ or hybrid certificate chains without unacceptable size and compatibility costs?~~ **Partially answered (August 2026):** Merkle Tree Certificates (Let's Encrypt staging late 2026, production 2027; Chrome preferred approach; PLANTS WG Last Call) provide the PQ Web PKI path. Composite ML-DSA certs (LAMPS WG Last Call, RFC Q4 2026) provide the enterprise PKI path. See [Merkle Tree Certificates](/kb/merkle-tree-certificates/). Open question becomes: will browsers support both simultaneously?
- Which decentralized identity systems will define key-transition proofs that preserve pseudonymous reputation without making users deanonymize?
- Will blockchain ecosystems converge on hash-based, lattice-based, or STARK/account-abstraction migration paths?
- How should off-grid and low-bandwidth systems amortize PQ handshakes across intermittent links?
- Will major TEE vendors publish PQ attestation timelines before CRQC risk becomes operationally urgent?
- How will CISA's PQC Product Categories (July 23, 2026) reshape vendor roadmaps for networking hardware, HSMs, and email systems in the "transitioning" category?

## Standardization state, verified 2026-09-26

| Document | WG | State | Last revision |
|----------|----|-------|---------------|
| `draft-ietf-tls-mlkem` (pure ML-KEM KEX) | TLS | **Blocked under appeal 2026-09-24** (Deb Cooley, complaint/appeals review); was "Approved-announcement sent" Sept 3 → "RFC Ed Queue" Sept 8 → Blocked Sept 24. IANA "RFC-Ed-Ack" on -10 since Sept 10; -11 uploaded Sept 16 with IANA "IANA OK - Actions Needed". Informational, Recommended=N | -11, 2026-09-16 |
| RFC 10024 (hybrid ECDHE+ML-KEM) | TLS | **Published**, Proposed Standard, Aug 2026 — the endorsed default | — |
| `draft-ietf-tls-mldsa` (ML-DSA auth) | TLS | **Blocked under appeal 2026-09-24** (Deb Cooley, same cause as mlkem); was cleared from 65-day appeal Sept 11, then re-blocked 13 days later. IANA "Waiting on Authors" since Sept 18 | -06, 2026-09-11 |
| `draft-ietf-lamps-pq-composite-sigs` | LAMPS | **RFC Ed Queue** / "Awaiting Second editor" from "In Progress (First Edit)" 2026-09-23 — first forward motion in 63 days; ~2–6 weeks further to publication. Proposed Standard | -19, 2026-08-26 |
| `draft-ietf-plants-merkle-tree-certs` | PLANTS | **WG Document / I-D Exists** — **-05 still current as of Oct 10 (no -06 in datatracker)**. The previously-reported "Sept 21 -06 upload" did not appear in datatracker during the W41 cycle. Companion `draft-gray-plants-mtc-deploy-use-cases-01` (last updated 2026-09-18, revision 2026-09-02) — no -02 in W41 either. Chrome Q2 update (post W41) commits "more MTC details to be published this month" — W43 trigger for Chrome MTC disclosure | -05, 2026-07-06 |
| RFC 9958 (PQC for Engineers) | PQUIP | Published, Informational | — |
| RFC 9980 (OpenPGP PQC) | OpenPGP | Published 2026-06-30, hybrid-only | — |
| `draft-ietf-jose-pq-composite-sigs` | JOSE | **WG Document / I-D Exists** — no shepherd, no AD. ~14 days in queue | -04, 2026-09-11 |

### Library state, 2026-09-26

| Project | Version | Notes |
|---------|---------|-------|
| liboqs | **0.16.0** (2026-07-09) | main updated with AES-192 support (commit b196b57, Sept 24), XMSS code-scan fixes (#2577 Sept 21), and security fix for OOB access in `xmss_core_sign` on secret-key OID mismatch (#2511 Sept 21) |
| oqs-provider | 0.12.0-rc2 (2026-09-16) | commit 36cafae0 (Sept 19) updated MAYO, MQOM, SNOVA to NIST Round 3 variants |
| mlkem-native | **v2.0.0** (2026-08-07) | SUPERCOP aliases removed, `MLK_ERR_FAIL` split; v1.3 LTS bugfix-only through Feb 2027 |
| mldsa-native | **v2.0.0** (2026-08-07) | **first stable release**; C90; SLOTHY Neon/AVX2; memory/type-safety proofs |
| AWS-LC | **v5.10.0** (2026-09-23) | fifth release of September; hardening sweep; OpenSSL-compatible rehash -compat; `ca`-command failure-mode fix |
| OpenSSL | **4.1.0-beta1** (2026-09-23) — feature line | PQ-capable-branch security: 4.0.3 / 3.6.5 / 3.5.9 (Sept 9) — no fresh security release in this window |

### Cryptanalysis ePrints (Sept 19–25 window)

| ePrint | Title | Significance | Primitives affected |
|--------|-------|-------------|---------------------|
| 2026/2137 (Sept 21) | Too Small to Hide: Single-Trace Key Recovery from ML-KEM Key Generation | CBD sampler vulnerable to single-trace side-channel; q-randomization countermeasure restores ~4 bits loss instead of >140 | ML-KEM (implementation only) |
| 2026/2131 (Sept 20) | Forging 1024-bit RSA signatures in nearly SNFS time | Even RSA-4096 below 128-bit under signing-oracle model | RSA (signing keys specifically) |
| 2026/2149 (Sept 22) | Identify PQC Algorithms for Automotive Security | Secure Boot / OTA / V2X guidance — performance-driven | Multiple (deployment guidance) |
| 2026/974 (Sept 21) | LoTRS: Practical PQ Structured Threshold Ring Signatures from Lattices | Threshold ring signatures | New construction |

### Federal clock

| Date | Requirement |
|------|-------------|
| 2026-09-21 | FIPS 140-2 certificates → **Historical** (5 days ago); FIPS 140-3 only for new procurement |
| 2026-10-09 → 2026-10-12 | Ethereum Foundation 2nd Annual PQ Research Retreat, Cambridge UK |
| 2026-10-22 | OMB **M-26-15**: agency PQC Migration Plans due to OMB + ONCD (**26 days out**) |
| 2026-11-14 → 2026-11-20 | IETF-127 San Francisco (**49 days out**) |
| 2026-12-07 → 2026-12-11 | ASIACRYPT 2026 Hong Kong |
| 2027-01-01 | CNSA 2.0 first enforcement (**97 days out**) |
| 2028–2030 | M-26-15 Phase 3 — PQC key establishment for HVAs / high-impact systems |
| **2031** | M-26-15 Phase 4 — **signature** migration |
| 2035 | M-26-15 Phase 5 — full migration |

See [Post-Quantum Saturday — September 26 2026 Weekly Update](/briefings/post-quantum/2026-09-26/) for sourcing and analysis.

## Library state, 2026-10-10 (status check)

| Project | Version | Notes |
|---------|---------|-------|
| liboqs | **0.16.0** (2026-07-09) | **93 days as current tagged release** — longest 2026 gap; the mldsa-native integration from 0.16.0 is the production-credible default; pin to known SHA rather than rely on the tag |
| oqs-provider | 0.12.0-rc2 (2026-09-16); stable **0.10.0** (2025-07-28) | **470 days as stable tag**, no fresh tag; main-branch last commit `36cafae0` Sept 19 (MAYO/MQOM/SNOVA Round 3) — no new commits in W41 |
| mlkem-native | **v2.0.0** (2026-08-07) | unchanged from W36; v1.3 LTS bugfix-only through Feb 2027 |
| mldsa-native | **v2.0.0** (2026-08-07) | unchanged from W36; first stable release; C90; SLOTHY Neon/AVX2; memory/type-safety proofs |
| AWS-LC | **v5.11.0** (2026-10-01) | **9 days as current**; September weekly cadence broken into October; PR #3601 (Oct 6) carries ML-DSA prehash mutual-exclusion fix toward v5.12.0 (~Oct 17-31) |
| OpenSSL | **4.1.0-beta1** (2026-09-23) | final October 2026 target; 4.0.3/3.6.5/3.5.9/3.4.8 multi-branch triplet (Sept 29) current; **OpenSSL 3.4 EOL 2026-10-22 (same date as M-26-15 deadline, 12 days out)** |
| Chrome MTC | n/a (Chromium browser code) | Q2 2026 update commitment: "more MTC details to be published this month [Oct 2026]" — W43 cycle is the operative trigger; Chromium issues-tracker P1/P2 cluster: [#452986180](https://issues.chromium.org/issues/452986180) cert verifier, [#482083310](https://issues.chromium.org/issues/482083310) experiment metrics, [#452983502](https://issues.chromium.org/issues/452983502) signatureful MTC, [#462227032](https://issues.chromium.org/issues/462227032) UX, [#458113212](https://issues.chromium.org/issues/458113212) server roots |

### Cryptanalysis ePrints (Sept 26 – Oct 10 window)

| ePrint | Title | Significance | Primitives affected |
|--------|-------|-------------|---------------------|
| 2026/2113 (Sept 25) | Post-Quantum PKE and More from a Noisy Unstructured Linear Algebraic Assumption: Beyond LWE and LPN | NLA-based PKE that resists LPN-broken oracle but plausibly LWE-broken; diversification track | New construction |
| 2026/1992 (Sept 23) | Bridging the Cryptographic Transition: A Unified Framework for Post-Quantum Key Exchange | Google 2029 internal PQC deadline formalized; unified hybrid-PQ-KEX framework | Hybrid KEX |
| 2026/2195 (Sept 30) | MKFHE Almost as Fast as SK-FHE | multi-client PIR trajectory | MKFHE / PIR |
| 2026/2120 (prior-week) | MKFHE Strikes Back | multi-client PIR trajectory | MKFHE / PIR |
| 2026/2401 (Oct 7) *if published in window* | (research-scan continuation) | carried forward | (TBA) |

No first-line PQC cryptanalysis paper published in the Oct 3 → Oct 10 IACR ePrint window that breaks or weakens ML-KEM / ML-DSA / SLH-DSA / Falcon deployments. The week is a **"between-cycles" week** for cryptanalysis — the [IACR ePrint Archive](https://eprint.iacr.org) shows fresh papers but none with direct PQC-primitive cryptanalytic impact.

### Hardware-PQC (CHES 2026 anchors)

- [Electronics 2026, 15(2), 475](https://www.mdpi.com/2079-9292/15/2/475) "Lattice-Based Cryptographic Accelerators for the Post-Quantum Era" — survey of FPGA/ASIC implementations; **18.7× energy-efficiency gain** at >50,000-unit volumes for ASIC lattice-PQ vs general-purpose CPU; cites both mlkem-native v2.0.0 (Aug 7) and mldsa-native v2.0.0 (Aug 7) as the canonical software anchors. Most current hardware-PQC survey.
- **IACR CHES 2026** (Oct 11-15, Antalya) opens **1 day after this update** — hardware-PQC primary venue; side-channel mitigations for ML-KEM / ML-DSA on FPGAs and ASICs.

### Federal clock (refreshed 2026-10-10)

| Date | Requirement |
|------|-------------|
| 2026-10-07 | GSA FICAM PQC WG **5th meeting** (per bi-weekly cadence, 3 days back). Per Zscaler PQC analysis citing post-meeting summary: Aug 12 kickoff with 17 federal agencies |
| 2026-10-11 → 2026-10-15 | IACR CHES 2026, Antalya (**1-5 days out**) |
| 2026-10-21 | GSA FICAM PQC WG **6th meeting** (per bi-weekly cadence, 11 days out, 2 days before deadline) |
| **2026-10-22** | **OMB M-26-15** agency PQC Migration Plans due to OMB + ONCD (**12 days out, same date as OpenSSL 3.4 EOL**) |
| 2026-10-23 | IETF-127 final-agenda publication (1 day after M-26-15 deadline) |
| 2026-10-26 → 2026-10-27 | FIPS 'n' Chips FNC2026, Austin TX (16-17 days out) |
| 2026-10-26 → 2026-10-29 | NIST WPEC 2026 (Privacy-Enhancing Cryptography workshop), virtual (16-19 days out) |
| 2026-11-14 → 2026-11-20 | IETF-127 San Francisco (**35 days out**) |
| 2026-12-07 → 2026-12-11 | ASIACRYPT 2026 Hong Kong |
| 2027-01-01 | CNSA 2.0 first enforcement (**83 days out**) |
| 2030-12-31 | DoW: CRQC-vulnerable-with-larger-keys phased out; PQC required for cryptographic uses by **2031-12-31** |
| 2028–2030 | M-26-15 Phase 3 — PQC key establishment for HVAs / high-impact systems |
| **2031** | M-26-15 Phase 4 — **signature** migration |
| 2035 | M-26-15 Phase 5 — full migration |

### Sept 26 → Oct 10 deltas (week-over-week deltas vs. the Sept 26 base)

- AWS-LC v5.10.0 → **v5.11.0** (Oct 1) — ML-KEM BMI2+AVX2 gate (correctness), FIPS 3.x EOS to Feb 2030, KEM EVP_PKEY_check APIs (PR #2709)
- OpenSSL 4.1.0-beta1 (Sept 23) — **unchanged** through W41; final October 2026 target remains
- liboqs 0.16.0 — **unchanged** through W41
- oqs-provider — **unchanged** through W41
- `draft-ietf-tls-mlkem-11` and `draft-ietf-tls-mldsa-06` — **unchanged** (Blocked under Sept 24 appeal); +16 days blocked
- `draft-ietf-lamps-pq-composite-sigs` — **unchanged** (Awaiting Second editor from Sept 23); +17 days in state
- `draft-ietf-plants-merkle-tree-certs-05` — **unchanged**; no -06 visible in W41
- `draft-ietf-cose-falcon-04` — **unchanged** (expired Sept 16); no -05
- FIPS 206 — **unchanged** (NIST silence); +36 days since last Perlner post

See [Post-Quantum Saturday — October 10 2026 Weekly Update](/briefings/post-quantum/2026-10-10/) for the W41 detailed analysis and [Post-Quantum Saturday — October 03 2026 Weekly Update](/briefings/post-quantum/2026-10-03/) for the W40 cycle (the prior week).

## Library state, 2026-10-17 (status check, refreshed)

| Project | Version | Notes |
|---------|---------|-------|
| liboqs | **0.16.0** (2026-07-09) | **100 days as current tagged release** — longest 2026 gap (the prior 0.15.0 → 0.14.0 gap was 94 days between Jul 10 2025 and Nov 14 2025); 0.17.0 expected November or December 2026 if cadence holds; pin to known SHA rather than rely on the tag |
| oqs-provider | stable **0.10.0** (2025-07-28) | **477 days as stable tag**, no fresh tag; main-branch last commit `36cafae0` Sept 19 (MAYO/MQOM/SNOVA Round 3) |
| mlkem-native | **v2.0.0** (2026-08-07) | unchanged from W36; v1.3 LTS bugfix-only through Feb 2027 |
| mldsa-native | **v2.0.0** (2026-08-07) | unchanged from W36; first stable release; C90; SLOTHY Neon/AVX2; memory/type-safety proofs |
| AWS-LC | **v5.11.0** (2026-10-01) | **16 days as current**; September weekly cadence broken into October; no `Prepare v5.12.0` PR open; the W41 PR cluster (#3600, #3601, #3602, #3604, #3609) is the candidate set for v5.12.0; AWS Security Blog "Quantum-resistant signing on AWS" Part 1 published in window — first end-to-end cloud-provider ML-DSA supply-chain guide; AWS CloudHSM ML-DSA in FIPS mode for hsm2m.medium GA since 2026-09-01 |
| OpenSSL | **4.1.0-beta2** (2026-10-09) | DTLS 1.3 (RFC 9147), ppc64le ML-DSA/ML-KEM NTT, AVX-512 SHAKE x4 for ML-DSA, AVX-512/VAES for AES-CBC; **2 known DTLS 1.3 security issues (#33172, #33173) force beta2 not final**; **4.1.0 final pushed beyond October 2026**; 4.0.3/3.6.5/3.5.9/3.4.8 multi-branch triplet (Sept 29) current; **OpenSSL 3.4 EOL 2026-10-22 (5 days out, same date as M-26-15 deadline)**; OpenSSL 3.6 EOL 2026-11-01 (15 days out); 4.2 master-branch adds `MLKEM512X25519` + `SecP256r1MLKEM512` hybrid TLS KEMs (draft-rosomakho) + `fips-indicator` gettable context parameter for the 4.x FIPS 140-3 module + ASCON-AEAD128 per NIST SP 800-232 |
| wolfSSL | **5.9.1** (late Aug / early Sept 2026) | **ML-KEM (FIPS 203) enabled by default**; **context-aware FIPS 204 ML-DSA (Dilithium) API now default** (legacy gated behind `WOLFSSL_DILITHIUM_NO_CTX`); sensitive memory buffers zeroized; private key validation for Ed25519/Ed448/ML-DSA/ML-KEM; **22 CVEs** including ECDSA cert verification with EdDSA or ML-DSA enabled, DTLS 1.3, ECH, ECCSI; DTLS 1.3 / TLS 1.3 write-dup; Brainpool curve support |
| Chrome MTC | n/a (Chromium browser code) | Q2 2026 update commitment: "more MTC details to be published this month [Oct 2026]" — W43 trigger |
| Apple MTC | n/a (Apple Root Program policy) | **Apple commits to MTCs — draft MTC policy end of October 2026** (apple/apple-root-program); 3 cosignatures (ML-DSA-44 + ECDSA-P256 from issuer, ML-DSA-44 from mirror Operator) + 7-day validity + FIPS 140-3 L3 / CC EAL 4+ HSMs + IANA PENs as Trust Anchor IDs; applications late summer 2027; S/MIME goes composite ML-DSA + ECDSA/RSA in traditional X.509; MTC institutional backing now complete: Chrome + Cloudflare + Let's Encrypt + Apple (Mozilla pending) |

### Cryptanalysis ePrints (Oct 10 – Oct 17 window)

| ePrint | Title | Significance | Primitives affected |
|--------|-------|-------------|---------------------|
| **2026/2480** | Post-Quantum Certificate-Based PSK Provisioning for WireGuard via Mutual TLS, DTLS, and QUIC: Design and Performance Study | First Tamarin-verified hybrid PQ + ML-DSA-authenticated WireGuard; external TLS 1.3 control channel + PSK injection; classical / pure PQ / hybrid key establishment + classical / ML-DSA certs + 3 transports evaluated | WireGuard + ML-KEM + ML-DSA |
| **2026/2474** | Software-Pipelining The Number Theoretic Transform on Neural Processing Units: A Loop-Fission Methodology | First NTT acceleration on AMD AI Engine NPUs; radix-2/4/8; 14-bit / 30-bit moduli; polynomial degree 4096/2048; TCHES 2027 | ML-KEM / ML-DSA / FHE NTT |
| **2026/2402** | Revisiting Lattice-based Blind Signatures Again | Breaks a Crypto'20 lattice-based blind signature scheme; bug in blindness security proof + attack exploiting tree-leaf correlations; repair discussed | Lattice-based blind signatures |
| **2026/2091** (W41 carry) | Keep Track of Your Errors: Solving ILWE and Improving Attacks on ML-DSA | **ML-DSA secret recovery from 139M → 2.25M signatures** (factor 62) via belief-propagation soft-analytic ILWE solver; reveals recently discovered timing leakage in ML-DSA | ML-DSA |
| 2026/974 (carry) | LoTRS: Practical Post-Quantum Structured Threshold Ring Signatures from Lattices | First practical lattice threshold ring signature; **ACM CCS 2026**; t-out-of-N selection-hiding + 2-round aggregated signing | Lattice ring signatures |

**The week's cryptanalysis headline** is **the lattice-standardization side-channel reality check** — the **ePrint 2026/2091 ILWE soft-analytic paper** (139M → 2.25M signatures) and the **SEALSQ LightSec 2026 paper** on ML-KEM key-generation encoding side-channel together establish that **both lattice-based NIST standards (ML-KEM and ML-DSA) carry side-channel fragility comparable to classical ECC in adversary cost**, an order-of-magnitude change from pre-2026 expectations. **For freedom-tech deployers**: constant-time + masked implementations are required for both ML-KEM and ML-DSA in production, not only in HSM contexts.

### IACR CHES 2026 + LightSec 2026 anchors (Oct 11-15 Antalya)

- **SEALSQ "Cross-information lattice attack on ML-KEM" at LightSec 2026** (Oct 11, affiliated event of CHES 2026) — peer-reviewed paper; combines profiling-based techniques with lattice reduction against the **ML-KEM key-generation encoding step**; recovers sensitive information under realistic conditions; pairs the attack with practical countermeasures; complements SEALSQ's QS7001 secure element (Common Criteria EAL5+ in progress). **First third-party confirmation of lattice-standardization side-channel fragility for ML-KEM**.
- **[Electronics 2026, 15(2), 475](https://www.mdpi.com/2079-9292/15/2/475)** "Lattice-Based Cryptographic Accelerators for the Post-Quantum Era" — W41 carry survey of FPGA/ASIC implementations; **18.7× energy-efficiency gain** at >50,000-unit volumes for ASIC lattice-PQ vs general-purpose CPU; cites both mlkem-native v2.0.0 and mldsa-native v2.0.0 as canonical software anchors. Most current hardware-PQC survey.
- **ePrint 2026/2474** (TCHES 2027) — first NTT acceleration on AMD AI Engine NPUs.

### Federal clock (refreshed 2026-10-17)

| Date | Requirement |
|------|-------------|
| 2026-10-11 → 2026-10-15 | IACR CHES 2026, Antalya (**in window**) |
| 2026-10-11 | LightSec 2026 affiliated event at CHES 2026 (Antalya, **in window**); SEALSQ ML-KEM paper |
| **2026-10-21** | **GSA FICAM PQC WG 5th meeting** (presumed, per bi-weekly cadence from Aug 12 kickoff: Aug 12 → Aug 26 → Sep 9 → Sep 23 → Oct 7 → **Oct 21**) — **1 day before M-26-15 deadline**; agenda not public |
| **2026-10-22** | **OMB M-26-15** agency PQC Migration Plans due to OMB + ONCD (**5 days out, same date as OpenSSL 3.4 EOL**); 17 federal agencies participated in Aug 12 kickoff per Zscaler / MeriTalk analyses |
| 2026-10-23 | IETF-127 final-agenda publication (1 day after M-26-15 deadline) |
| 2026-10-26 → 2026-10-29 | NIST WPEC 2026 (Privacy-Enhancing Cryptography workshop), virtual |
| 2026-10-26 → 2026-10-27 | FIPS 'n' Chips FNC2026, Austin TX |
| 2026-10-22 → 2026-10-31 (presumed) | **Apple draft MTC policy** publication (apple/apple-root-program), per the [Sept 21 Apple announcement](https://groups.google.com/a/chromium.org/g/ct-policy/c/QGZw2ADMXvk/m/pR3A5uRZCAAJ) |
| **2026-11-01** | **OpenSSL 3.6 EOL** (15 days out) |
| 2026-11-04 | GSA FICAM PQC WG 6th meeting (presumed) |
| 2026-11-14 → 2026-11-20 | **IETF-127 San Francisco** (**28 days out**); PLANTS WG session on MTCs the most consequential in cycle |
| 2027-01-01 | CNSA 2.0 first enforcement (**76 days out**) |
| 2028–2030 | M-26-15 Phase 3 — PQC key establishment for HVAs / high-impact systems |
| **2031** | M-26-15 Phase 4 — **signature** migration |
| 2031-12-31 | DoW: PQC required for all cryptographic uses |
| 2035 | M-26-15 Phase 5 — full migration |
| 2035 | NSM-10 PQC risk-mitigation |

### Oct 10 → Oct 17 deltas (week-over-week vs. the W41 base)

- AWS-LC v5.11.0 — **unchanged** through W42 (16 days current, +7d from W41)
- OpenSSL 4.1.0-beta1 → **4.1.0-beta2** (Oct 9, in-window) — **first pre-release with DTLS 1.3 (RFC 9147) + ppc64le ML-DSA/ML-KEM NTT + AVX-512 SHAKE x4 + AVX-512/VAES AES-CBC**; 2 known DTLS 1.3 security issues force beta2 not final; **4.1.0 final pushed beyond October 2026**
- OpenSSL 4.2 master — `MLKEM512X25519` + `SecP256r1MLKEM512` hybrid TLS KEMs (draft-rosomakho) + `fips-indicator` gettable context parameter for the 4.x FIPS 140-3 module + ASCON-AEAD128 (NIST SP 800-232) added
- liboqs 0.16.0 — **unchanged** through W42 (100 days current, +7d from W41)
- oqs-provider — **unchanged** through W42 (477 days as stable tag, +7d from W41)
- wolfSSL — **5.9.1** ships (W41 release, in window) — ML-KEM default-on + context-aware ML-DSA API default + 22 CVEs
- `draft-ietf-tls-mlkem-11` and `draft-ietf-tls-mldsa-06` — **unchanged** (Blocked under Sept 24 appeal); +23 days blocked
- `draft-ietf-lamps-pq-composite-sigs-19` (Ounsworth et al, April 2026) — **expires 23 October 2026** (6 days out); still in RFC Editor "Awaiting Second editor" state from Sept 23; +24 days in state; companion `draft-ietf-lamps-cms-composite-sigs` expires 23 November 2026
- `draft-ietf-plants-merkle-tree-certs-05` → **-06** (Sept 21, 2026) — **correction**: the prior W41 "MTC -05" note was itself wrong; the datatracker page now shows -06 as the current document; still in WG Document state, no shepherd, no AD, no IANA review
- `draft-gray-plants-mtc-deploy-use-cases-01` — **unchanged** (revision 2026-09-02; last updated 2026-09-18); expires 6 March 2027
- `draft-ietf-cose-falcon-04` — **unchanged** (expired Sept 16); no -05
- FIPS 206 — **unchanged** (NIST silence); +43 days since last Perlner post
- **Apple MTC commitment** (Sept 21, in scope) — draft MTC policy end of October 2026; 3 cosignatures + 7-day validity + FIPS 140-3 L3 HSMs
- **AWS Security Blog "Quantum-resistant signing on AWS" Part 1** — first end-to-end cloud-provider ML-DSA supply-chain guide
- **IACR CHES 2026** (Oct 11-15 Antalya) + **LightSec 2026** (Oct 11) — SEALSQ "Cross-information lattice attack on ML-KEM" peer-reviewed paper

See [Post-Quantum Saturday — October 17 2026 Weekly Update](/briefings/post-quantum/2026-10-17/) for the W42 detailed analysis and [Post-Quantum Saturday — October 10 2026 Weekly Update](/briefings/post-quantum/2026-10-10/) for the W41 cycle (the prior week).
