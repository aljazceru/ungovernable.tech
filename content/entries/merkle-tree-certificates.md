---
title: "Merkle Tree Certificates"
slug: merkle-tree-certificates
type: deep-dive
pillars: ["pqc"]
readiness: experimental
description: "Merkle Tree Certificates batch many TLS certificates into one signed tree, keeping certificates small enough for post-quantum signatures."
dek: "A new certificate format that batches many certificates into a single Merkle tree, signing only the root — making post-quantum web authentication practical without the signature-size explosion."
updated: 2026-09-05
created: 2026-08-01
origin: vault
source: "10-Post-Quantum/Merkle Tree Certificates.md"
aliases: ["MTC", "MTCs", "Merkle Tree Certs", "PLANTS certificates"]
tags: ["pqc", "post-quantum", "mtc", "merkle-tree", "web-pki", "tls", "lets-encrypt", "plants", "authentication", "ietf"]
---

## Why MTCs Exist

Post-quantum signatures are dramatically larger than classical ones:

| Algorithm | Signature Size |
|-----------|---------------|
| ECDSA P-256 | ~72 bytes |
| Ed25519 | 64 bytes |
| **ML-DSA-65** | **3,309 bytes** |
| SLH-DSA-128s | 7,856 bytes |
| SLH-DSA-128f | 17,088 bytes |

A TLS certificate chain (root → intermediate → leaf) with ML-DSA signatures at every level adds **~10 KB** to every TLS handshake. For a high-traffic web server, this is a meaningful cost in bandwidth, latency (especially on mobile/satellite links), and TCP window sizing. It also breaks existing X.509 size assumptions in middleware, load balancers, and TLS terminators.

**Merkle Tree Certificates solve this** by changing the signing model: instead of each certificate getting its own large PQ signature, certificates are batched into a Merkle tree, and only the tree's root is signed. Each certificate carries a compact inclusion proof (logarithmic in batch size) rather than a full signature.

## How MTCs Work

```
                    ┌─────────────┐
                    │  Root Hash   │  ← Signed once per batch with ML-DSA
                    └──────┬───────┘
                    ┌──────┴───────┐
               ┌────┴────┐    ┌────┴────┐
               │  Hash A  │    │  Hash B  │
               └────┬─────┘    └────┬─────┘
              ┌─────┴──┐       ┌────┴───┐
           ┌──┴──┐ ┌───┴─┐  ┌──┴──┐ ┌───┴──┐
           │Cert1│ │Cert2│  │Cert3│ │Cert4│
           └─────┘ └─────┘  └─────┘ └─────┘
```

1. **Batching**: A CA collects certificates into a batch (e.g., all certificates issued in a ~1-second window).
2. **Tree construction**: Certificates are hashed into leaf nodes; internal nodes hash their children.
3. **Root signing**: Only the Merkle root is signed — once — using ML-DSA (or any PQ signature).
4. **Inclusion proof**: Each certificate carries its authentication path (the sibling hashes from leaf to root). The client verifies the proof against the signed root.
5. **Transparency**: The tree structure is append-only and publicly logged, similar to Certificate Transparency (CT) logs. Cosignatures from independent parties verify correct CA operation.

**Size math**: For a batch of 4,096 certificates (12 levels), the inclusion proof is ~12 × 32 bytes = 384 bytes — much smaller than a single ML-DSA signature (3,309 bytes). The signed root (one ML-DSA signature per batch) is amortized across thousands of certificates.

## Key Properties

- **Post-quantum secure**: The only signature is the root's ML-DSA signature; inclusion proofs are hash-based (quantum-resistant under Grover, which only quadratically speeds up hash inversion).
- **Compact**: Per-certificate overhead is O(log n) hashes, not a full PQ signature.
- **Transparent**: Built-in logging (like CT) means the CA's issuance activity is publicly auditable.
- **Batch-latency**: Certificates are issued in batches (target: ~1 per second), adding a small delay similar to waiting for CT log inclusion today.
- **Revocation**: Requires rethinking — traditional CRL/OCSP assume individual signatures. MTC revocation likely involves short-lived certificates or a separate revocation tree.

## Standardization

| Entity | Role | Status (August 2026) |
|--------|------|---------------------|
| **IETF PLANTS WG** | Standardization of MTC format | `draft-ietf-plants-merkle-tree-certs-05` — **WG Document / I-D Exists** (no shepherd, no AD, no intended RFC status; last revision 2026-07-06). *Corrected 2026-09-05: earlier entries said WG Last Call.* |
| **Let's Encrypt / ISRG** | Certificate authority (700M+ sites) | Committed to MTCs; staging late 2026, production 2027 |
| **Chrome** | Browser client | Identified MTCs as preferred approach for PQ certificates |
| **Cloudflare** | CDN / edge | Testing MTCs on live internet traffic with Chrome |
| **IETF LAMPS WG** | Composite ML-DSA X.509 certs (alternative) | `draft-ietf-lamps-pq-composite-sigs-19` — **RFC Editor queue** (RFC-Ed-Ack, First Edit, Proposed Standard) as of 2026-08-26 |

**The PLANTS WG** (Post-quantum usE of oLder Protocol Number TerminalS — a backronym) was chartered specifically to develop the Merkle Tree Certificate standard. The draft defines:
- The MTC format (how certificates and inclusion proofs are encoded)
- The issuance protocol (how a CA creates batches and signs roots)
- The verification protocol (how a TLS client validates an MTC)
- Integration with TLS 1.3 (how MTCs are negotiated in the handshake)

**Composite ML-DSA** (`draft-ietf-lamps-pq-composite-sigs`) is the alternative approach: put a combined ML-DSA + ECDSA signature directly into X.509. This is simpler (no batching, no new certificate format) but doesn't solve the size problem. It's the path for enterprise/private PKI where certificate chains are short and bandwidth isn't constrained. MTCs are the path for the public Web PKI at scale.

## Let's Encrypt's MTC Roadmap

Let's Encrypt (the nonprofit CA operated by ISRG, securing 700M+ websites) published its PQ roadmap on June 3, 2026:

- **Late 2026**: Staging environment that issues MTCs (for testing).
- **2027**: Production-ready MTC issuance.
- **User experience**: No change — certificates remain free, automated, and available via ACME.
- **Coexistence**: Current RSA/ECDSA certificates continue to be issued and renewed as always.
- **Transition**: MTCs will be issued alongside traditional certificates during a multi-year migration.

Let's Encrypt has operated Certificate Transparency logs since 2019 — the same append-only Merkle tree data structure that underlies MTCs. This gives them operational experience with the core technology.

**Quote** (Josh Aas, Let's Encrypt / ISRG head): *"Let's Encrypt is committed to a post-quantum-safe Web PKI. The path we're planning to take is Merkle Tree Certificates."*

## Enterprise Concerns (from IETF 126 MAPRG, July 2026)

The IETF 126 MAPRG session raised critical enterprise adoption questions:

1. **Certificate fields**: Can relying parties still access Subject DN, SAN, EKU, Certificate Policies, Name Constraints, and enterprise-specific extensions? The MTC format must preserve X.509 semantics or provide a migration path.
2. **Private PKI**: How should private/internal CAs deploy and operate MTCs? Enterprise PKI has different requirements (no public transparency logs, custom naming, longer lifetimes).
3. **CDN/proxy interaction**: What happens when a browser expects MTC but a CDN terminates TLS with a traditional certificate? The "split world" problem.
4. **Compliance forensics**: What should enterprises archive for audit, compliance, and evidentiary purposes? MTCs change what a "certificate" looks like.
5. **Middleware compatibility**: Load balancers, TLS inspectors, API gateways, and DLP systems that parse certificates may not understand MTCs.

These are unresolved — the PLANTS WG must address them before broad enterprise adoption.

## Internet-Scale Deployment Measurement (IETF 126)

The IETF 126 MAPRG presentation included a measurement study of the top 27 websites:

| Algorithm Set | % of Sites | Count |
|---------------|----------|-------|
| RSA only | 51.9% | 14 |
| EC only | 33.3% | 9 |
| EC + RSA | 14.8% | 4 |

**Key finding**: Over half of top sites still use RSA-only certificate chains. Zero use PQ signatures. The migration to PQ authentication is at the very beginning — the standardization work (ML-DSA in TLS, MTCs) is the prerequisite for any deployment.

A separate arXiv study (*Measurement Study of Post-Quantum Readiness of Internet: 2026*, arXiv:2606.16473) found that while TLS 1.3 is at 52.4% adoption and QUIC at 31.9%, 15.7% of domains (especially banking and government) still rely on TLS 1.2 — the protocol layer beneath the PQ migration.

## Trade-offs: MTCs vs. Composite ML-DSA Certificates

| Dimension | Merkle Tree Certificates | Composite ML-DSA X.509 |
|-----------|------------------------|----------------------|
| **Per-cert overhead** | O(log n) hash proof (~384 B) | Full ML-DSA sig (~3.3 KB) |
| **Standardization** | PLANTS: WG Document (I-D Exists, -05 dated 2026-07-06) | LAMPS: **RFC Ed Queue** (2026-08-26) |
| **CA complexity** | Batching infrastructure needed | Minimal change to issuance |
| **Client complexity** | New verification logic | Existing X.509 path (extended) |
| **Transparency** | Built-in (CT-like logging) | Separate CT logs as today |
| **Revocation** | Requires new model | Traditional CRL/OCSP works |
| **Best for** | Public Web PKI at scale | Enterprise/private PKI |
| **Timeline** | Staging 2026, prod 2027 | RFC Q4 2026 |

**Likely outcome**: Both standards coexist. Public CAs (Let's Encrypt, DigiCert, Sectigo) deploy MTCs for the public web. Enterprises deploy composite ML-DSA certificates for internal PKI. Browsers eventually support both.

## Relevance to Freedom Tech / Decentralized Systems

MTCs are architecturally significant beyond Web PKI:

1. **Decentralized identity**: The Merkle tree model — a compact commitment to a set of identities, verifiable without trusting each individual assertion — is philosophically aligned with decentralized identity. A Nostr relay could issue MTC-style batch proofs for its users. An ENS subdomain registrar could batch registrations into a Merkle root.

2. **Mesh network node registries**: A mesh network (Meshtastic, Reticulum, cjdns) that needs to authenticate member nodes could use MTC-style batch proofs instead of individual certificates — reducing overhead on low-bandwidth links.

3. **Crypto-agility**: MTCs separate the signing algorithm (at the root) from the certificate format. If ML-DSA is later found weak, only the root signing algorithm changes — the certificate and proof infrastructure remains.

4. **Anti-censorship**: The built-in transparency logging means CAs cannot silently issue certificates — every issuance is publicly auditable. This aligns with the ungovernable principle of transparency over authority.

5. **Compact proofs for constrained environments**: The O(log n) proof size is valuable for satellite IoT, off-grid messaging ([Overview - Off-Grid Networks](/kb/off-grid-networks/)), and any bandwidth-constrained system that needs authentication.

## Open Questions

- **Will browsers support both MTCs and ML-DSA X.509 simultaneously?** Chrome prefers MTCs; Firefox and Safari haven't committed publicly.
- **How does revocation work?** Short-lived certificates (hours/days) may replace traditional revocation, but this requires automated renewal (already common via ACME).
- **What about code signing?** MTCs are designed for TLS server authentication. Code signing, email signing, and document signing have different requirements (offline verification, long lifetimes) that may not fit the MTC model.
- **HSM integration**: Can MTC root signing keys be protected in HSMs? The batching model changes the signing cadence from per-certificate to per-batch.
- **Cross-CA chains**: Can an MTC from one CA chain to another (cross-certification)? The Merkle tree model may not compose the way traditional X.509 chains do.

## Update — August 15 2026: First External CA Files for Chrome's MTC Test Root

**TrustAsia Technologies** (Shanghai; Chrome-qualified CT log operator since 2021, operates log2026a/b) has filed what appears to be the **first certificate-authority application to Chrome's MTC test root store** — Chromium Issue 538260165, flagged by PKI standards expert Corey Bonnell (early August). Three data points in five months: Google+Cloudflare experiment (spring) → Let's Encrypt commitment (June) → independent third-party CA implementing against draft-stage specs. The PLANTS draft is provably implementable outside its originating collaboration.

What the filing implements:
- **RFC 9925 unsigned CA cosigner certificates** (Feb 2026, David Benjamin): the MTC CA cosigns Merkle subtrees rather than signing individual certs; RFC 9925's placeholder signature algorithm lets X.509 represent this safely — legacy relying parties reject rather than mis-trust.
- **The critical `MTCCertificationAuthority` extension** (PLANTS draft §5.5): marks the subject as an MTC-issuing CA; carries issuance-log hash algorithm, cosigner signature algorithm, and serial-number range. The critical marking forces non-MTC X.509 stacks to reject rather than misinterpret as a conventional CA — a deliberate transition-period safety mechanism.

Rollout confirmation: Phase 1 live (~1,000 certs via Cloudflare mock-MTCA); **Phase 2 targeted Q1 2027** (open to CT log operators with pre-Feb-2026 "usable" logs — exactly TrustAsia's credential); **Phase 3 / Chrome Quantum-resistant Root Store (CQRS) Q3 2027**, MTC-only, alongside the existing root program. PLANTS draft at v03 (April 2026; Benjamin/Google, O'Brien/Apple, Westerbaan & Valenta/Cloudflare, Valsorda/Geomys), ~12–18 months from Proposed Standard.

**Strategic read**: MTC is the rare PQ story that *decentralizes* — batched Merkle roots plus transparency logs replace per-certificate CA signatures as the trust chokepoint, and every independent CA implementing it pushes toward an open standard rather than proprietary infrastructure. For freedom-tech: watch whether issuance-log operation (the CT-operator → MTCA pipeline) becomes something a non-institutional actor can realistically run.

See [Post-Quantum Saturday — August 15 2026 Weekly Update](/briefings/post-quantum/2026-08-15/) §5 for full analysis.

## Update — August 22 2026: Google Cloud Dates Its MTC Support (2028)

Google Cloud's PQC roadmap (Haridas & Bachman, Aug 11, 2026) adds an independent timeline data point: **Google Trust Services support for Merkle Tree Certificates is dated 2028**, with PQC certificates rolling out across Google Cloud products and infrastructure through 2027–2028 (ML-DSA certificates intended, SLH-DSA "where meaningful"). Google attributes the later signature dates partly to unfinished standards work — it is contributing to the **IETF PLANTS working group**, whose Merkle Tree Certificate spec reached **working-group draft revision 05 on July 6, 2026** (v03 was the April snapshot; the draft remains an Internet-Draft). Chrome and Cloudflare have been testing MTC against live traffic since February 2026.

The full Google signature timeline (Domain 2, target end-2028): Binary Authorization + Access Approval 2026; Assured OSS 2027; Certificate Authority Service 2027; Cloud IAM 2028; GTS MTC 2028. Signatures trail confidentiality (end-2027) by one year across every line — the same one-year signature lag Cloudflare documented (see the [August 01 update](/briefings/post-quantum/2026-08-01/)).

**Strategic read**: GTS at 2028 + Chrome Phase 2 at Q1 2027 + CQRS at Q3 2027 means MTC's first full production cycle spans 2027–2028 across the two biggest browser/CDN ecosystems. For self-operated CA dreams: the 2027–28 window is when third-party issuance-log tooling either matures or doesn't.

See [Post-Quantum Saturday — August 22 2026 Weekly Update](/briefings/post-quantum/2026-08-22/) §7 for the full roadmap analysis.

## Primary Sources

- Let's Encrypt blog (June 3, 2026): *A Post-Quantum Future for Let's Encrypt* — `letsencrypt.org/2026/06/03/pq-certs/`
- IETF PLANTS WG: `datatracker.ietf.org/wg/plants/`
- MTC draft: `datatracker.ietf.org/doc/draft-ietf-plants-merkle-tree-certs/`
- LAMPS composite sigs: `lamps-wg.github.io/draft-composite-sigs/`
- Chrome MTC experiment: `blog.chromium.org/` (search "Merkle Tree Certificates")
- Cloudflare PQ authentication: `blog.cloudflare.com/ml-dsa-will-have-to-do/`
- IETF 126 MAPRG slides: `datatracker.ietf.org/meeting/126/materials/slides-126-maprg-`
- Help Net Security coverage (June 5, 2026): `helpnetsecurity.com/2026/06/05/lets-encrypt-mcts-web-post-quantum-authentication/`
