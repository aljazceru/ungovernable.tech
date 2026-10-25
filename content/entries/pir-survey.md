---
title: "Private Information Retrieval: The Long Survey"
slug: pir-survey
type: reference
pillars: ["cryptography"]
description: "A long survey of private information retrieval: fetching a record from a database without the server learning which one, from theory to practice."
dek: "Fetching item `i` from a public database without the database server learning which item was fetched."
updated: 2026-06-17
created: 2026-04-17
origin: vault
source: "02-Cryptography/Overview - Private Information Retrieval.md"
aliases: ["PIR", "Private Information Retrieval", "Computational PIR", "CPIR"]
tags: ["pir", "private-information-retrieval", "cryptography", "privacy", "homomorphic-encryption", "metadata-privacy"]
---

## Summary

End-to-end encryption hides message contents, but it does not hide *what public data you asked for*. A DNS resolver learns the domain. A certificate-transparency monitor learns the certificate. A keyserver learns the public key. A model-serving stack learns which embedding shard, document, or reputation record was retrieved.

Private Information Retrieval (PIR) addresses that access-pattern leak. A client retrieves one or more records from a server-held database while the server learns nothing about the selected index, except metadata that the protocol does not cover: query timing, database identity, record size class, and the fact that a query happened.

PIR matters for freedom tech because public databases are everywhere:

- safety lists and blocklists: Safe Browsing, malware domains, adult-content filters;
- public-key infrastructure: Certificate Transparency, revocation, key directories;
- decentralized systems: DNS records, Nostr relay indexes, blockchain state, reputation graphs;
- AI retrieval: RAG over public corpora, vector search, model-weight or expert routing;
- contact discovery: checking a phone number, username, or public key without revealing the social graph.

The field has moved from elegant theory to near-deployable systems. Single-server computational PIR built on LWE / RLWE and homomorphic encryption is no longer a toy: SimplePIR and YPIR approach memory-bandwidth throughput; Spiral and SealPIR cover FHE-style high-rate trade-offs; Brave's FrodoPIR and Apple's Swift Homomorphic Encryption show product-oriented PIR libraries; Google has released experimental private-retrieval and hintless PIR code. The 2025 frontier is about specialization: distribution-aware PIR for skewed access patterns, tiny-query protocols for bandwidth-constrained clients, sharded PIR for Ethereum state, and two-server information-theoretic PIR with sublinear server work.

The catch: PIR is not magic anonymity. The server still must touch a large part of the database, so server cost scales with database size. PIR hides *which record*, not *who asked*, *when*, or *how often*. In practice it composes with [Overview - Mix Networks](/kb/mix-networks/), [Overview - Confidential Computing](/kb/confidential-computing/), [Overview - Fully Homomorphic Encryption](/kb/fully-homomorphic-encryption/), and padding.

## Historical context

### 1995–1998: PIR as a theoretical primitive

Chor, Goldreich, Kushilevitz, and Sudan introduced PIR in the mid-1990s and published the canonical JACM paper in 1998. The original setting used multiple non-colluding replicated servers. A client split the query into shares; any one server saw only randomness, while the combined answers revealed the selected record.

This gave information-theoretic privacy but required an operational assumption that is hard to guarantee in the real world: the servers must not collude.

### 2000s–2010s: computational PIR and homomorphic encryption

Computational PIR (CPIR) asks for privacy with one server. Privacy now rests on computational hardness rather than non-collusion. Early schemes were too slow for production, but they established the central pattern:

1. Client encrypts a selection vector or query token.
2. Server homomorphically evaluates a lookup over the database.
3. Server returns an encrypted answer.
4. Client decrypts the selected record.

XPIR (Aguilar-Melchor and Gaborit, 2015) and SealPIR (Angel et al., 2018) made lattice / BFV-based CPIR concrete, but still had substantial cost.

### 2020–2023: practical lattice PIR

A wave of systems optimized the algebra and systems engineering:

- **OnionPIR** (CCS 2021) improved response efficiency.
- **Spiral** (IEEE S&P 2023) used FHE composition for high-rate single-server PIR.
- **FrodoPIR** (PoPETS 2023) focused on deployability, amortized server cost, and a simple Rust implementation.
- **SimplePIR / DoublePIR** (USENIX Security 2023) showed single-server LWE PIR at memory-bandwidth-like throughput, with client hints to amortize cost.
- **Tiptoe** (SOSP 2023) applied related homomorphic search techniques to private web search over hundreds of millions of pages.

### 2024–2026: deployment, hintless protocols, and product libraries

Recent work is about removing deployment friction:

- **YPIR** (USENIX Security 2024) introduced silent preprocessing and reported throughput up to 83% of machine memory bandwidth.
- **Google HintlessPIR** implements the 2023 ePrint "Hintless Single-Server Private Information Retrieval", eliminating database-dependent client state and avoiding an interactive setup phase.
- **Apple Swift Homomorphic Encryption** is a product-grade Swift package with PIR and private nearest-neighbor search examples; Apple describes PIR use cases in Mail business-logo lookup, caller ID, and parental web filtering.
- **PIR for Ethereum data** has become a live research area for hiding wallet state reads, contract storage reads, and RPC access patterns.
- **PETS / Eurocrypt 2025 work** is pushing client-efficient, committed, and HE-revisited variants; the theme is no longer "can PIR work?" but "which PIR variant matches this database, update rate, and trust model?"
- **Distributional PIR** (USENIX Security 2025, Lehmkuhl / Henzinger / Corrigan-Gibbs) exploits heavily skewed popularity distributions without weakening cryptographic privacy; the price is relaxed correctness for out-of-distribution queries.
- **Pirouette** (ePrint 2025/680) targets extremely small client queries: 36 bytes for `2^25` records in the paper's headline setting, without a database-specific hint.
- **VIA** (ePrint 2025/2074) attacks online communication for single-server PIR, reporting 690 KB online communication for a 32 GB database without offline communication, and 2.1 KB online communication in a variant with offline communication.
- **Finite-differences two-server PIR** (ePrint 2025/2008 / EUROCRYPT 2026) revives information-theoretic multi-server PIR with sublinear server probes and quasilinear storage, at the cost of a two-server non-collusion assumption and large communication constants.
- **GPIR** (ICS 2026, Ji, Yu et al.) brings GPU acceleration to single-server PIR, rethinking kernel design, data layout, and execution scheduling; reports substantial throughput gains over CPU-bound baselines and is accepted at IEEE ICS 2026.
- **iSimplePIR** (ePrint 2026/030) introduces the first formal definition of single-server incremental PIR, enabling entry-level real-time updates without full reprocessing; for a 1% column-major update in a 1 GB database it achieves 224× reduction in preprocessing overhead versus prior row-level approaches, and is compatible with DoublePIR, YPIR, Authenticated PIR, VeriSimplePIR.
- **HarmonyPIR** (ePrint 2026/437) constructs a new single-server stateful PIR scheme using a single random permutation instantiated via AES or FF1 Format-Preserving Encryption; achieves up to two orders of magnitude better amortized computation and up to five times better amortized communication than prior state-of-the-art.
- **BALANCED-PIR** (ePrint 2025/1055, Wang & Ren) balances client storage against computation for stateful PIR, with Verifiable BALANCED-PIR adding only modest costs while achieving 100× smaller client storage, 15× less amortized computation, and 2.5× better amortized communication than prior verifiable schemes.
- **PIRacle** (IEEE TC 2026) is a published journal article system targeting practical scalability for single-server PIR deployments.
- **Improved TensorPIR** (ePrint 2026/912) reduces communication cost to 45.5% of the original TensorPIR via a new framework that rethinks encryption strategy for the index, using fewer CRT moduli; reports 36.9% query size and 22.2% answer size versus TensorPIR for large N, and 28.9%–56.1% of HintlessPIR's online time across 16–128 GB databases.
- **Zeal** (ePrint 2026/684) is the first non-cooperative PIR scheme: requires no cooperation from the database operator, assumes a strong adversary controlling the database and all third parties, and uses differential privacy for security proofs; reports ~3–4 minutes latency for 1M records, a 50× improvement over a naive solution.
- **Doubly-Efficient PIR Practical** (ePrint 2026/243) advances DEPIR — sublinear per-query work for both client and server with no client state — from impractical to near-feasible: for N=2^23, reduces server state from 733 TB to 171 GB (4 orders of magnitude) and query time by 6 orders of magnitude; batch querying 5,461 elements takes 112s total with 21ms amortized per query.
- **Secret-Key PIR** (ePrint 2026/865) constructs PIR from one-way functions, where the client processes the database using a short secret key in an offline phase; theoretically interesting as an alternative to lattice-based approaches.

## What PIR does and does not hide

A PIR protocol normally hides the **index** of the record requested from the PIR server. It does not automatically hide:

- the client's IP address;
- query timing and frequency;
- the database being queried;
- the approximate response size if record classes vary;
- whether the client later acts on the returned data;
- correctness of the answer, unless verifiability or commitment is added;
- data confidentiality against the client. Standard PIR is asymmetric: the client may learn more than one record depending on packing. Symmetric PIR / SPIR adds constraints so the client learns only the requested item.

For a freedom-tech deployment, PIR is best treated as an *access-pattern privacy component*. It needs network anonymity, rate limiting, padding, and usually auditable database commitments around it.

## Taxonomy

### Information-theoretic PIR (IT-PIR)

The database is replicated across `k` non-colluding servers. The client sends each server a random-looking share of the query. Combining the answers reveals the record.

- **Privacy basis:** information-theoretic, assuming no collusion.
- **Strength:** fast server operations; no heavy lattice crypto.
- **Weakness:** non-collusion is an institutional / operational assumption.
- **Representative systems:** Chor et al.; Percy++; distributed point-function systems.

### Computational PIR (CPIR)

One server holds the database. The client sends an encrypted query, and the server computes over it.

- **Privacy basis:** hardness assumptions such as LWE / RLWE or assumptions underlying the HE scheme.
- **Strength:** no non-collusion requirement; realistic for one public service.
- **Weakness:** the server generally scans or preprocesses the database; costs scale with database size.
- **Representative systems:** SealPIR, Spiral, FrodoPIR, SimplePIR, DoublePIR, YPIR, HintlessPIR.

### Preprocessing / stateful PIR

Some modern PIR schemes split work into an expensive offline phase and a cheap online query phase. The client downloads or derives a database-dependent "hint" and reuses it for many queries.

- **Strength:** excellent online latency and communication after setup.
- **Weakness:** hints can be large; database updates complicate correctness; first-run cost is visible.
- **Examples:** SimplePIR, DoublePIR, YPIR, FrodoPIR variants.

### Hintless / stateless PIR

Hintless protocols avoid database-dependent client state and interactive setup. This is attractive when databases update frequently or clients make only a few queries.

- **Strength:** easier client UX, database updates are simpler.
- **Weakness:** can shift work back to the server and may lose the best online constants.
- **Examples:** Google `hintless_pir`, based on Li, Micciancio, Raykova, Schultz-Wu (ePrint 2023/1733).

### Keyword PIR

Index PIR assumes the client knows the numeric record index. Many applications need lookup by domain, phone number, public key, or hash. Keyword PIR maps keywords to index PIR via hashing, cuckoo tables, bucketization, or encrypted equality tests.

- **Useful for:** DNS, key directories, revocation lists, Safe Browsing, contact discovery.
- **Trade-off:** bucket design can leak distributional information if not padded carefully.

### Symmetric PIR / SPIR and committed PIR

Plain PIR protects the client's query but not necessarily the server's database. A malicious or over-curious client may learn extra records depending on packing. SPIR protects server privacy. Committed PIR adds database commitments so clients can detect equivocation or wrong answers.

- **Useful for:** paid databases, signed transparency logs, replicated datasets where a server might lie.
- **Recent work:** `PIR-PIXR/CPIR` implements Committed Private Information Retrieval variants.

### Distributional PIR

Classic PIR treats every record as equally likely. Real systems do not: social feeds, software update metadata, Safe Browsing entries, package names, Nostr events, and popular token contracts follow skewed distributions. Distributional PIR keeps the same cryptographic privacy for the query but relaxes correctness: in-distribution queries succeed with high probability, while rare out-of-distribution queries may fail more often.

- **Strength:** large server-cost reductions when popularity is highly skewed.
- **Weakness:** clients must not let past success or failure change whether they query, or the success/failure side channel can leak information.
- **Example:** Lehmkuhl, Henzinger, and Corrigan-Gibbs, *Distributional Private Information Retrieval* (USENIX Security 2025), plus the CrowdSurf system for privately fetching tweets.

### Communication-efficient PIR

Some deployments care more about client upload / download than server CPU. Mobile wallets, browsers, IoT clients, and low-bandwidth networks cannot afford tens of kilobytes or megabytes per lookup even if the server can scan memory quickly.

- **Pirouette** minimizes query size, reporting a 36-byte query for `2^25` records in its headline benchmark without a database-specific hint.
- **VIA / VIA-C / VIA-B** target online communication for single-server offline/online PIR. VIA removes offline communication and reports 690 KB online communication for a 32 GB database; VIA-C permits offline communication and reports 2.1 KB online communication for the same size.
- **Design tension:** query-size reductions often increase server computation, require new LWE/RLWE conversion machinery, or assume an offline phase that is awkward for frequently changing databases.

### Multi-server PIR revival

The original PIR model used multiple non-colluding servers. Single-server CPIR became attractive because the trust model was simpler, but two-server IT-PIR still matters for deployments where two independent operators are realistic: public-interest infrastructure, federated transparency logs, open-source package registries, and [Overview - Decentralized DNS](/kb/decentralized-dns/) mirrors.

The finite-differences PIR work by Henzinger and Ragavan shows a new point in the design space: two-server information-theoretic PIR with quasilinear storage and sublinear server probes. It is not a drop-in production system — it expands an 11 GB one-byte-record database into a 1 TB data structure and still has large communication — but it weakens the assumption that information-theoretic PIR must be linear-time at the server.

### Keyword PIR for practical key-value databases

Most freedom-tech lookups are by key, not by numeric index. ChalametPIR is a useful concrete example: it builds a stateful single-server keyword PIR scheme by combining FrodoPIR with Binary Fuse Filters. The project reports browser/WASM client support and GPU-assisted server setup; this makes it closer to real application shape than pure index-PIR references, while still being a young implementation.

## How single-server CPIR works

A simplified LWE / HE PIR flow:

```text
Client knows desired index i
        │
        ▼
Encode i as encrypted selector vector q
        │       server sees q but cannot decrypt it
        ▼
Server evaluates: encrypted_answer = DB · q
        │       often scans/preprocesses whole DB
        ▼
Client decrypts encrypted_answer → record_i
```

If the server skipped most of the database, its memory accesses would reveal which record was requested. Good PIR systems either touch the database uniformly or use preprocessing that makes the online phase independent of the selected index.

The engineering problem is therefore brutal and simple: make "touch a lot of database" cheap enough.

## Major implementations

| Project | Type | Maturity | Development signal | Notes |
|---|---|---:|---|---|
| [Apple Swift Homomorphic Encryption](https://github.com/apple/swift-homomorphic-encryption) | BFV HE library with PIR / PNNS | Production-oriented library | 637 stars; pushed 2026-05-26 | Swift package from Apple; includes PIR and private nearest-neighbor search applications; docs update #314 merged May 26 2026. |
| [SimplePIR / DoublePIR](https://github.com/ahenzinger/simplepir) | LWE CPIR with client hint | Research reference, influential | 100 stars; last push 2023-01-13 | USENIX Security 2023; 10 GB/s/core SimplePIR, 7.4 GB/s/core DoublePIR in paper. |
| [YPIR](https://www.usenix.org/conference/usenixsecurity24/presentation/menon) | Silent-preprocessing CPIR | Research artifact, state of the art | USENIX Security 2024 | Reports up to 83% of memory bandwidth; optimized for high-throughput single-server use. |
| [Spiral](https://github.com/menonsamir/spiral) / [spiral-rs](https://github.com/menonsamir/spiral-rs) | FHE-composition CPIR | Research; Rust implementation active | `spiral-rs` 15 stars; pushed 2026-03-19 | High-rate single-server PIR; original C++ repo preserved for reproducibility. |
| [Brave FrodoPIR](https://github.com/brave-experiments/frodo-pir) | Stateful single-server LWE PIR | Research / deployment-oriented | 76 stars; pushed 2024-01-10 | Designed for Safe Browsing, password breach, certificate revocation, streaming use cases. |
| [Microsoft SealPIR](https://github.com/microsoft/SealPIR) | BFV / Microsoft SEAL CPIR | Research library | 156 stars; pushed 2024-11-19 | Classic practical PIR implementation; README warns not for production. |
| [Google HintlessPIR](https://github.com/google/hintless_pir) | Hintless LWE / RLWE PIR | Experimental research code | 24 stars; pushed 2026-03-27 | Implements HintlessPIR / LinPIR from ePrint 2023/1733; PR #14 merged March 2026. |
| [Google Private Retrieval](https://github.com/google/private-retrieval) | SHELL-based PIR | Archived research library | 48 stars; archived; last push 2021-10-19 | Useful historical code, not active. |
| [OpenMined PIR](https://github.com/OpenMined/PIR) | Private retrieval protocol | Stale / educational | last push 2021-04-03 | Useful for reading but not active production base. |
| [valargroup/vote-nullifier-pir](https://github.com/valargroup/vote-nullifier-pir) | Zcash nullifier non-membership PIR | Research prototype; Zcash ZIP proposed | 2 stars; pushed 2026-05-22; Rust | PIR system for proving a Zcash nullifier is not in the on-chain nullifier set without revealing which nullifier; proposes ZIP specification; Cargo workspace with IMT-tree, YPIR server/client. |
| [PIREX](https://github.com/vt-asaplab/pirex) | Client-efficient PIR | Research prototype | 3 stars; pushed 2026-02-27 | PETS 2025 artifact focused on online/offline client efficiency. |
| [PIR-PIXR/CPIR](https://github.com/PIR-PIXR/CPIR) | Committed PIR / SPIR | Research prototype, active | GitHub appeared June 2026; implements CPIR with database commitment; notes extra client-protection costs |
| [ChalametPIR](https://github.com/itzmeanjan/ChalametPIR) | Keyword PIR over key-value database | Young Rust implementation | 15 stars; pushed 2025-07-11 | Combines FrodoPIR with Binary Fuse Filters; includes WASM client and GPU-assisted server setup paths. |
| [finite-diffs-pir](https://github.com/ahenzinger/finite-diffs-pir) | Two-server IT-PIR with preprocessing | Research prototype | 0 stars; pushed 2026-05-01 | EUROCRYPT 2026 reference implementation; sublinear server probes with quasilinear storage, but high communication and non-collusion assumption. |
| [wuwuz/Piano-PIR-new](https://github.com/wuwuz/Piano-PIR-new) | PIANO (sublinear server PIR) | Research reference, active | Tutorial + server Go implementations; updated 2026; IEEE S&P 2024 | Sublinear server computation; used in RAGtime-PIANO. |
| [RAGtime-PIANO](https://eprint.iacr.org/2026/231) | FHE + PIR for secure RAG | Research prototype, strong results | ePrint 2026/231; Python CKKS + PIANO implementation | 323× lower communication, 40× lower latency vs prior work; quantum-secure; fully secure RAG. |
| [PIR-DSN](https://github.com/BDS-SDU/PIR-DSN) | DSN + PIR (Filecoin-based) | INFOCOM 2026; active | Go + Rust; multi-node testnet scripts; SealPIR + BRPIR backends | First DSN protocol with PIR for both single/multi-server settings; privacy in decentralized storage retrieval. |
| [nd-dsp-lab/Piano-PIR-RAG-MODIFIED](https://github.com/nd-dsp-lab/Piano-PIR-RAG-MODIFIED) | PIANO variant for RAGtime-PIANO | Research artifact | Go; mod of PIANO for RAGtime-PIANO integration | PIANO backend tuned for RAG retrieval workloads. |
| [inspire-rs](https://github.com/igor53627/inspire-rs) | Server-side preprocessing PIR | Research Rust implementation | pushed 2026-02-15 | Targets large databases such as Ethereum state. |
| [GPIR](https://arxiv.org/abs/2604.04696) | GPU-accelerated single-server PIR | Research; ICS 2026 | Accepted at IEEE ICS 2026; code expected | Rethinks kernel design, data layout, and scheduling for GPU throughput. |
| [iSimplePIR](https://eprint.iacr.org/2026/030) | Incremental single-server LWE PIR | Research prototype | ePrint 2026/030 | Compatible with DoublePIR, YPIR, AuthPIR, VeriSimplePIR; 224× less preprocessing overhead for 1% updates. |
| [HarmonyPIR](https://eprint.iacr.org/2026/437) | Stateful single-server PIR with FPE | Research prototype | ePrint 2026/437 | FF1 or AES permutation; up to 2 orders of magnitude amortized compute improvement. |
| [BALANCED-PIR](https://eprint.iacr.org/2025/1055) | Balanced stateful PIR with verifiability | Research prototype | ePrint 2025/1055 | 100× smaller client storage than prior verifiable schemes; Verifiable variant. |

Repository signals above were checked through GitHub metadata on 2026-05-27. Star counts are weak maturity indicators; cryptographic audit status and deployment evidence matter more.

## Key papers and results

| Paper / system | Year | Main contribution | Practical reading |
|---|---:|---|---|
| Chor, Goldreich, Kushilevitz, Sudan, *Private Information Retrieval* | 1995 / 1998 | Introduced PIR; multi-server IT-PIR | The conceptual root. |
| Aguilar-Melchor & Gaborit, *Lattice-based PIR* / XPIR | 2015 | Early lattice CPIR implementation | Pre-modern but historically important. |
| Angel et al., *PIR with Compressed Queries and Amortized Query Processing* / SealPIR | 2018 | BFV-based practical PIR | First widely referenced modern implementation. |
| Mughees, Chen, Ren, *OnionPIR* | 2021 | Response-efficient single-server PIR | Important communication trade-offs. |
| Menon & Wu, *Spiral* | 2022 / 2023 | FHE composition, high-rate PIR | Good for large records / streaming. |
| Davidson, Pestana, Celi et al., *FrodoPIR* | 2022 / 2023 | Simple scalable stateful PIR with low amortized cost | Deployment-motivated design. |
| Henzinger et al., *One Server for the Price of Two* | 2022 / 2023 | SimplePIR and DoublePIR; near memory-bandwidth throughput | Baseline for fast LWE CPIR. |
| Henzinger et al., *Private Web Search with Tiptoe* | 2023 | Private search over hundreds of millions of pages | PIR-style retrieval beyond exact record lookup. |
| Li, Micciancio, Raykova, Schultz-Wu, *Hintless Single-Server PIR* | 2023 | Eliminates database-dependent client state | Strong fit for frequently updated databases. |
| Menon & Wu, *YPIR* | 2024 | Silent preprocessing and high throughput | Current high-performance baseline. |
| Shriram, Chen, Ren, *RAGtime-PIANO: Efficient Secure Remote RAG* | 2026 | FHE+PIR for fully secure RAG; 323× lower communication, 40× lower latency; first to achieve all four security properties simultaneously | ePrint 2026/231; IACR News Feb 2026; quantum-secure retrieval via FHE/PIANO composition. |
| Zhang et al., *PIR-DSN: A Decentralized Storage Network Supporting PIR* | 2026 | First DSN protocol integrating PIR for both single and multi-server settings; Filecoin/Lotus-based; INFOCOM 2026 | arXiv 2025/07189; INFOCOM 2026; Go/Rust implementation. |
| Wu et al., *Piano: Extremely Simple, Single-Server PIR with Sublinear Server Computation* (updated impl) | 2024 / 2026 | Updated Go implementation via wuwuz/Piano-PIR-new; sublinear server-side computation | IEEE S&P 2024; github.com/wuwuz/Piano-PIR-new; used as PIANO backend in RAGtime-PIANO. |
| Lehmkuhl, Henzinger, Corrigan-Gibbs, *Distributional Private Information Retrieval* | 2025 | Faster PIR under skewed popularity distributions with relaxed correctness | Good fit for social feeds and popular public objects; watch success/failure leakage. |
| *Pirouette: Query Efficient Single-Server PIR* | 2025 | 36-byte query headline for `2^25` records without database-specific hint | Useful for mobile / low-bandwidth clients. |
| *Private Information Retrieval based on Homomorphic Encryption, Revisited* | 2025 | Practical comparison of HE-PIR structures | Useful for choosing deployment architecture; reports large gains from less-used designs. |
| *VIA: Communication-Efficient Single-Server Private Information Retrieval* | 2025 | Low online communication with and without offline phase | Relevant for bandwidth-constrained deployments. |
| Henzinger & Ragavan, *Two-Server Private Information Retrieval in Sublinear Time and Quasilinear Space* | 2025 / 2026 | IT-PIR with quasilinear storage and sublinear server probes | Theoretical/practical bridge for two independent operators. |
| GPIR, *Enabling Practical Private Information Retrieval with GPUs* | 2026 | GPU kernel design, data layout, and scheduling for PIR throughput | ICS 2026 accepted; first major GPU-specific PIR systems work. |
| Shriram, Arunachalaramanan & Ren, *iSimplePIR: Incremental Single-Server PIR* | 2026 | First formal definition of single-server incremental PIR; entry-level updates with 224× preprocessing overhead reduction | Extends SimplePIR compatibly with DoublePIR, YPIR, VeriSimplePIR. |
| Wang & Ren, *BALANCED-PIR: Single-Server Stateful PIR with Balanced Efficiency* | 2025 | Balances client storage and computation; verifiable variant with 100× smaller client storage | Substantial improvement over prior verifiable stateful PIR. |
| Wang & Ren, *HarmonyPIR: Efficient Single-Server Stateful PIR Using FPE* | 2026 | FF1/AES permutation; up to 2 orders of magnitude amortized compute and 5× better amortized communication | ePrint 2026/437; new hint organization for stateful PIR. |
| *Improved TensorPIR: Single-Server PIR with Lower Communication Cost* | 2026 | Rethinks index encryption; reduces communication to 45.5% of original TensorPIR; fewer CRT moduli | ePrint 2026/912; 36.9% query size vs TensorPIR for large N. |
| *Zeal: PIR for Non-Cooperative Databases* | 2026 | First non-cooperative PIR; no database cooperation required; differential privacy security proof | ePrint 2026/684; ~3–4 min latency for 1M records; 50× vs naive. |
| *Towards Making Doubly-Efficient PIR Practical* | 2026 | DEPIR sublinear server/client work; reduces server state 4 orders of magnitude and query time 6 orders | ePrint 2026/243; 171 GB server state for N=2^23 vs 733 TB; 21ms amortized per query. |
|| *Secret-Key PIR from One-Way Functions* | 2026 | PIR from generic one-way functions; offline client preprocessing with short secret key | ePrint 2026/865; theoretically interesting alternative to lattice PIR. ||
|| *Streamlined Symmetric PIR via Rényi Divergence* | 2026 | First single-server SPIR derived directly from LWE PIR via Rényi noise flooding; 8 MB online communication, 302 ms server compute for 1M × 1 kB records | ePrint 2026/1051; post-quantum; notes that hint-based preprocessing schemes need extra database-privacy protections. ||
|| *Private Information Retrieval: A Tutorial and Survey* | 2026 | Comprehensive tutorial covering all major PIR paradigms; characterizes concrete efficiency; provides deployment guidance and application survey | ePrint 2026/1135; CC BY; targets readers without prior PIR knowledge. ||

## Late-June 2026 Developments

## Late-June 2026 Developments

### RAGtime-PIANO — FHE + PIR for Fully Secure Remote RAG (ePrint 2026/231)

A first-of-its-kind secure RAG protocol appeared at ePrint 2026/231, combining **FHE (CKKS)** with **PIR (PIANO)** through a novel two-stage IVF-Flat clustering approach:

- **Stage 1**: FHE-encrypted query embedding sent to server; server performs k-means centroid scoring and returns top-N clusters via FHE — query embedding never exposed to server.
- **Stage 2**: PIR queries privately retrieve centroid-associated embeddings and top-ranked documents — document indices never exposed.
- **Result**: End-to-end security where neither query, distances, nor retrieval information is known to the database server.
- **Performance**: Up to **323× lower communication costs** and **40× lower latency** versus prior work, with superior accuracy on FEVER and Natural Questions datasets.
- **Python implementation** using CKKS (FHE) and PIANO (PIR) — benchmarks confirm practical latency for real-world RaaS deployments.

This is the first fully secure RAG protocol achieving all four properties simultaneously: no embedding DB download, no DB modification, complete security, and quantum-secure retrieval. Links to [Confidential-AI-Inference](/kb/confidential-ai-inference/) and [Private-LLM-Inference-Patterns](/kb/private-llm-inference-patterns/) directly — private RAG is the concrete missing piece for confidential AI inference over public corpora.

Source: [ePrint 2026/231](https://eprint.iacr.org/2026/231), [IACR News Feb 2026](https://iacr.org/news/item/27672), [modification repo](https://github.com/nd-dsp-lab/Piano-PIR-RAG-MODIFIED)

### PIR-DSN: PIR for Decentralized Storage Networks (INFOCOM 2026)

PIR-DSN ([INFOCOM 2026](https://arxiv.org/abs/2512.07189), SDU Blockchain and Distributed Security Lab) is the first DSN protocol to integrate PIR for both single and multi-server settings, protecting user privacy during retrieval from decentralized storage without revealing which specific data is being fetched.

- **Built on Filecoin/Lotus**: Uses lotus-miner, lotus-gateway, and lotus-wallet as building blocks.
- **PIR backends**: Includes both SealPIR and BRPIR (distributed PIR) implementations within the project.
- **Multi-node testnet support**: Genesis node + worker node architecture with scripted deployment.
- **Privacy guarantee**: Other nodes in the network cannot infer which specific data the user intends to retrieve.
- **Go-based**: Full implementation at [github.com/BDS-SDU/PIR-DSN](https://github.com/BDS-SDU/PIR-DSN).

For [Overview - Decentralized Storage](/kb/decentralized-storage/) integrations (IPFS/Filecoin/Arweave/Sia/Storj), PIR-DSN shows the concrete path: attach a PIR layer to a DSN's retrieval protocol and you get private fetching over decentralized storage. This is directly relevant to the privacy architecture for decentralized AI model weights, dataset shards, or archival content.

Source: [GitHub BDS-SDU/PIR-DSN](https://github.com/BDS-SDU/PIR-DSN), [arXiv](https://arxiv.org/abs/2512.07189), [Moonlight review](https://www.themoonlight.io/tw/review/pir-dsn-a-decentralized-storage-network-supporting-private-information-retrieval)

### PIANO Implementation Updates — wuwuz/Piano-PIR-new

PIANO (*Extremely Simple, Single-server PIR with Sublinear Server Computation*, IEEE S&P 2024) received a notable implementation update. The original repository has been archived in favor of [wuwuz/Piano-PIR-new](https://github.com/wuwuz/Piano-PIR-new), which:

- Implements the **updated version** of PIANO as described in the main paper body.
- Contains both the original version (in `client/client.go`) and the new version (in `tutorial_new/tutorial_new.go`).
- Includes a clean **tutorial implementation**: `go run tutorial_new/tutorial_new.go` (client) + `go run server/server.go -port 50051` (server).
- PIANO's key property: **sublinear server computation** — the server does not need to read every database element during query processing, a significant efficiency improvement over naive PIR.

PIANO is used as the PIR backend in RAGtime-PIANO (above), demonstrating its suitability for practical privacy-preserving AI workloads.

Source: [github.com/wuwuz/Piano-PIR-new](https://github.com/wuwuz/Piano-PIR-new)

### Vitalik June 14, 2026 — Ethereum Privacy Blitz: ORAM and PIR for Wallet Privacy

Vitalik Buterin published a major post on June 14, 2026 declaring 2026 "the year that we take back lost ground in terms of self-sovereignty and trustlessness" and explicitly calling out **ORAM and PIR** as the primitives for hiding wallet queries from RPC providers:

> *"Helios: actually verify the data you're receiving from RPCs instead of blindly trusting it. ORAM, PIR: ask for data from RPCs without revealing what."*

The concrete privacy stack for Ethereum wallet reads is now:
1. **Helios** (a16z crypto): trustless light client — verifies RPC data without trusting the provider.
2. **PIR**: hides which state record is being fetched from the PIR server.
3. **ORAM**: prevents access pattern analysis when the RPC provider is the same as the data provider.
4. **Kohaku** (Ethereum Foundation): privacy-service abstraction as first-phase deliverable, making this stack consumable by non-technical users.

This is the clearest real-world deployment signal PIR has ever received from a protocol founder. Ethereum's privacy roadmap treats PIR not as an academic curiosity but as **infrastructure** for mainstream wallet privacy.

Sources: [Vitalik X June 14 2026](https://x.com/VitalikButerin/status/2012231445809435134), [The Block June 14 2026](https://www.theblock.co/post/386043/vitalik-buterin-declares-2026-the-year-ethereum-reverses-backsliding-of-self-sovereignty-and-trustlessness), [CryptoSlate](https://cryptoslate.com/ethereum-may-finally-kill-trust-me-wallets-in-2026-and-vitalik-says-the-fix-is-already-shipping)

### IACR News June 4, 2026 — PIR Tutorial Published

The IACR news item for June 4, 2026 highlighted the publication of *"Private Information Retrieval: A Tutorial and Survey"* (ePrint 2026/1135) by Shriram, Arunachalaramanan, Chen, and Ren. The paper is described as accessible to readers without prior PIR knowledge, covering:

- Information-theoretic and computational PIR.
- Single-server and multi-server non-colluding settings.
- PIR with and without preprocessing.
- Keyword queries and batch queries.
- Concrete efficiency characterization and deployment guidance.
- Practical applications survey.

This paper serves as the canonical onboarding reference for teams evaluating PIR for the first time — more applied than the original papers, more rigorous than a blog post.

Source: [IACR News June 4 2026](https://www.iacr.org/news/item/28679), [ePrint 2026/1135](https://eprint.iacr.org/2026/1135)

### PSE Ethereum Privacy PIR — Active Project

The Privacy and Scaling Explorations (PSE) team has an active project page for "Private Information Retrieval for Ethereum Data" at [pse.dev/projects/pir-ethereum-data](https://pse.dev/projects/pir-ethereum-data). This is the Ethereum Foundation-backed effort to turn PIR from research into wallet infrastructure. Combined with the Helios verified RPC and the Kohaku privacy toolkit, PSE's PIR project is the implementation arm of Vitalik's June 2026 privacy roadmap call.

Source: [pse.dev](https://pse.dev/projects/pir-ethereum-data)

### PIR-PIXR/CPIR — Committed PIR Implementation (June 2026)

GitHub appeared at [github.com/PIR-PIXR/CPIR](https://github.com/PIR-PIXR/CPIR) implementing Committed Private Information Retrieval — a scheme where the PIR server commits to its database state so clients can detect equivocation or wrong answers. The implementation results show that schemes with extra protection for the client increase practical time on both servers and the client. This fills a gap the overview noted: standard CPIR protects the client query but not the server's answer. Committed PIR is relevant for paid databases, signed transparency logs, or any setting where a PIR server might return wrong data opportunistically.

### SPIR via Rényi Divergence (ePrint 2026/1051)

The paper *"Streamlined Symmetric Private Information Retrieval via Rényi Divergence"* (ePrint 2026/1051) achieves a notable first: a single-server SPIR constructed directly from standard LWE PIR using Rényi divergence arguments for the database-privacy noise flooding, instead of the statistical distance analysis that leads to impractical parameters in prior approaches. Result: post-quantum, round-optimal SPIR with 8 MB online communication and 302 ms server computation for a 1-million-record, 1 kB-per-element database. This is still large for consumer mobile but represents a concrete step toward practical SPIR without multi-server assumptions.

The paper also raises an important note for deployments: practical LWE-PIR schemes that use client-downloaded offline hints require additional protections for the database, because the hint can encode information about the database. This directly affects deployments using SimplePIR, DoublePIR, or YPIR hint patterns.

### PIR Tutorial and Survey (ePrint 2026/1135)

A comprehensive tutorial-and-survey paper appeared at ePrint 2026/1135 covering all major PIR paradigms (IT-PIR, CPIR, preprocessing, hintless, keyword, batch), characterizing concrete efficiency, providing guidance on selecting a paradigm for a given deployment, and surveying applications. CC BY licensed. This is a strong onboarding resource for teams evaluating PIR for the first time — more applied than a survey, more accessible than the original papers.

## Evidence at a glance

| Claim | Evidence | Confidence |
|---|---|---:|
| Single-server PIR can be fast enough for selected production workloads | SimplePIR reports 10 GB/s/core; YPIR reports up to 83% of memory bandwidth; FrodoPIR reports sub-second response for 1M × 1KB database. | High for benchmarks; medium for production. |
| PIR is entering product libraries | Apple `swift-homomorphic-encryption` includes PIR and PNNS, with active development through 2026-04-27. | High. |
| PIR has plausible real-world use cases | Brave lists Safe Browsing, breached-password checks, certificate revocation, streaming; Apple describes Mail logos, caller ID, adult-content URL filtering. | High. |
| Hints and database updates remain hard | SimplePIR / DoublePIR use client hints; HintlessPIR exists specifically to remove database-dependent client state. | High. |
| PIR alone does not provide anonymity | Protocol hides selected record from PIR server, not IP, timing, or query frequency. | High. |
| Ethereum / Web3 PIR is active but immature | PSE project page and Ethereum research discussion exist; small Rust prototypes such as `inspire-rs` are active. | Medium. |
| Committed / verifiable PIR is still research-grade | `PIR-PIXR/CPIR` exists but has small adoption and prototype signals. | Medium. |
| Skewed access distributions can materially reduce PIR cost | Distributional PIR reports 5–77× compute-cost reductions on two real-world popularity distributions and 8× end-to-end cost reduction in CrowdSurf. | Medium-high for research benchmarks. |
| Tiny-query PIR is an active 2025 research axis | Pirouette reports a 36-byte query for `2^25` records; VIA-C reports 2.1 KB online communication for a 32 GB database with offline communication. | Medium; implementation maturity varies. |
| GPU acceleration is becoming practical for PIR | GPIR (ICS 2026) reports substantial throughput gains via kernel/data-layout co-design; first major GPU-specific PIR paper. | Medium; GPIR is newly published. |
| Incremental PIR for updateable databases is now formally defined | iSimplePIR (ePrint 2026/030) provides first formal definition and achieves 224× preprocessing overhead reduction for 1% updates. | Medium-high for research benchmarks; implementation availability TBD. |
| State-of-the-art stateful PIR is improving rapidly | HarmonyPIR (2× compute, 5× communication) and BALANCED-PIR (100× smaller client storage) are simultaneous 2026 improvements, suggesting the design space is actively explored. | Medium; both are new results. |
| Multi-server IT-PIR is not dead | Finite-differences PIR claims the first constant-server IT-PIR with quasilinear storage and polynomially sublinear server time, with a Go reference implementation. | Medium; still research-grade and communication-heavy. |
| Non-cooperative PIR is a new frontier | Zeal (ePrint 2026/684) removes the need for database cooperation, enabling PIR against arbitrary public databases; differential privacy security proof; 50× improvement over naive baseline. | Medium; newly defined model; implementation stage. |
| Doubly-Efficient PIR is becoming practical | DEPIR reduced server state from 733 TB to 171 GB for N=2^23; query time reduced 6 orders of magnitude; 21ms amortized per query for batch retrieval. | Medium; still requires substantial server resources. |
| Communication-efficient single-server PIR continues to improve | Improved TensorPIR (ePrint 2026/912) reduces communication to 45.5% of original TensorPIR via fewer CRT moduli; 36.9% query size vs TensorPIR for large N. | Medium; paper-stage, implementation TBD. |
| Committed PIR / SPIR now has a GitHub implementation | PIR-PIXR/CPIR GitHub appeared June 2026; implements committed CPIR variants; extra client protections add practical time costs | Medium; newly active. |
| Single-server SPIR derived from LWE PIR via Rényi divergence | ePrint 2026/1051 achieves 8 MB online communication, 302 ms server compute for 1M × 1 kB records; post-quantum; notes hint-based schemes need extra DB privacy protections | Medium; new theoretical result, implementation stage. |
| **Fully secure remote RAG is now practical via FHE+PIR** | RAGtime-PIANO (ePrint 2026/231) achieves all four security properties simultaneously: no embedding DB download, no DB modification, complete security, quantum-secure retrieval; 323× lower communication, 40× lower latency vs prior work | Medium-high; first-of-its-kind result; Python implementation exists; links directly to Confidential AI and Private LLM inference patterns. |
| **PIR-DSN: decentralized storage + PIR** | INFOCOM 2026; first DSN protocol integrating PIR for both single/multi-server; built on Filecoin/Lotus; Go+Rust implementation with multi-node testnet scripts | Medium; INFOCOM 2026 publication; active GitHub; concrete integration path for IPFS/Filecoin privacy. |
| **PIANO sublinear server PIR has active updated implementation** | wuwuz/Piano-PIR-new (2026) provides clean tutorial + server Go implementations; PIANO used as backend for RAGtime-PIANO, demonstrating production relevance | Medium; IEEE S&P 2024 paper with active 2026 implementation maintenance. |
| **Vitalik June 2026 explicitly calls out ORAM + PIR for wallet privacy** | June 14 post: "ORAM, PIR: ask for data from RPCs without revealing what"; Helios + PIR + ORAM + Kohaku stack for mainstream Ethereum wallet privacy | High; clearest real-world deployment signal PIR has received from a protocol founder. |
| **PSE has active Ethereum Privacy PIR project** | pse.dev/projects/pir-ethereum-data is the Ethereum Foundation-backed implementation arm for Vitalik's privacy roadmap; combines with Helios and Kohaku | High; active EF project; concrete deployment path. |
| **PIR Tutorial published via IACR June 2026** | ePrint 2026/1135 accessible tutorial covering all major PIR paradigms with deployment guidance and application survey; CC BY licensed | High; canonical onboarding resource for teams new to PIR. |

## Use cases

### Private DNS and naming

DNS queries are intent beacons. DoH hides queries from the local ISP but centralizes them at the resolver. ODoH hides the client's IP from the resolver but the resolver still sees the domain. PIR can hide the queried name from a resolver or from a cached public DNS database.

A PIR-backed [Overview - Decentralized DNS](/kb/decentralized-dns/) resolver could expose public zones through a fixed-size keyword PIR table. The open design questions are update cadence, record-size padding, negative answers, and abuse resistance.

### Certificate Transparency and revocation

SimplePIR / DoublePIR were applied to private auditing in Certificate Transparency. The paper reports a stronger privacy notion than Chrome's then-current approach with modest communication overhead: a monthly download plus small per-connection cost. This fits the PIR model well because CT data is public but the client's visited sites are sensitive.

Revocation checks have a similar shape: the revocation database is public; the certificate a user is checking is private.

### Safe Browsing and content filtering

Safe Browsing, malware-domain checks, and parental filters all ask whether a private URL or hash prefix appears in a public or semi-public database. Brave's FrodoPIR blog explicitly names Safe Browsing, breached-password checks, certificate revocation, and streaming as target applications. Apple's HE / PIR write-up describes adult-content URL filtering under parental restrictions as a PIR-style use case.

### Contact discovery and key directories

Contact discovery asks: "Which of my contacts are users?" Sending the address book to the server is unacceptable. Signal's production private contact discovery historically relied on enclaves; PIR / PSI designs reduce or remove the hardware trust assumption. See [Private Set Intersection](/kb/private-set-intersection/) for the neighboring primitive.

Key directories have the same problem: checking whether a key, username, phone number, or Nostr pubkey exists reveals relationships and intent.

### Private AI retrieval and RAG

Confidential LLM inference is incomplete if retrieval leaks the query. A TEE-hosted model with an ordinary vector database still leaks document IDs to the vector DB. PIR can hide which public chunks were retrieved; private nearest-neighbor search can hide embedding queries; TEEs can then handle the generation step.

This links directly to [Confidential-AI-Inference](/kb/confidential-ai-inference/) and [Private-LLM-Inference-Patterns](/kb/private-llm-inference-patterns/).

### Ethereum and public blockchain state

Wallets leak addresses and contracts through RPC reads. PIR over Ethereum state could let a wallet fetch balances, nonces, storage slots, or transaction data without revealing which account it cares about to the RPC provider. PSE's "Private Information Retrieval for Ethereum Data" and Ethereum research discussions are early-stage attempts to make this concrete.

The hard part is database shape: Ethereum state is large, hot, mutable, and heterogeneous. A practical deployment may shard by data type and use decoy queries across shards.

### Streaming, media catalogs, and social feeds

PIR can hide which public object a client streams. Spiral's streaming variants and FrodoPIR both discuss this setting. The economics only work when the server can amortize preprocessing across many clients or when records are large enough that response overhead is acceptable.

Distributional PIR is particularly relevant when a catalog has a long tail and a few very popular objects: tweets, Nostr events, software releases, package metadata, app-store objects, or media manifests. The CrowdSurf prototype in the Distributional PIR paper privately fetched tweets and reported an 8× end-to-end server-cost reduction. The trade-off is operational: a client's retry behavior and reaction to failed rare-object queries must not become a new side channel.

## Trade-offs

### Strengths

- **Cryptographic access-pattern privacy.** No need to trust the database operator not to log selected records.
- **Single-server deployability.** CPIR avoids the multi-server non-collusion assumption.
- **Composability.** PIR can be paired with mixnets, TEEs, FHE, ZK commitments, and signed transparency logs.
- **Public-database fit.** Many freedom-tech datasets are public but query-sensitive.
- **Post-quantum-friendly assumptions.** Many leading schemes use LWE / RLWE.

### Limitations

- **Server work scales with database size.** If the server only touched the selected row, privacy would fail.
- **Bandwidth and hints.** The best online performance often requires large client hints or preprocessing.
- **Database updates.** Static public tables are easy; fast-changing databases complicate hints, commitments, and cache invalidation.
- **Metadata remains.** PIR does not hide IP address, timing, or frequency.
- **Correctness / equivocation.** A malicious server can return the wrong encrypted answer unless the database is committed, replicated, or externally auditable.
- **Client privacy vs server privacy.** Standard PIR protects the client's query, not the server's database. Use SPIR when the server must reveal only one record.
- **Cryptographic implementation risk.** Lattice parameters, noise margins, serialization, side channels, and malformed ciphertext handling are non-trivial.

### When PIR is a bad fit

PIR is usually a poor fit when:

- the database is private to the server and cannot be leaked to clients;
- records are huge and clients could just download a coarse bucket;
- the database changes every second and clients query rarely;
- the adversary's main signal is network-level identity rather than selected record;
- the server cannot afford a database-scale scan or preprocessing pipeline.

## Design checklist for deployments

1. **Define the leakage goal.** What exactly must the server not learn: index, keyword, bucket, response size, or query frequency?
2. **Choose database shape.** Fixed-size records and stable ordering make PIR much easier.
3. **Pick a scheme by update cadence.** Static / slow updates favor preprocessing; frequent updates favor hintless or smaller buckets.
4. **Pad aggressively.** Normalize query and response sizes across record classes.
5. **Authenticate the database.** Use Merkle roots, signed epochs, CT-style logs, or committed PIR.
6. **Add network privacy.** Use OHTTP, Tor, mixnets, or proxying if IP-to-query linkage matters.
7. **Rate-limit without identity.** Blind tokens or privacy-pass-style credentials can prevent abuse without re-identifying clients.
8. **Plan failure modes.** Decryption errors, malformed answers, stale hints, and database epoch mismatch must be explicit.
9. **Benchmark on real data.** PIR constants are database-shape dependent; benchmark record size, batch size, cache behavior, and update rate.
10. **Do not roll your own crypto.** Start from audited or widely reviewed libraries where possible.

## Real-world maturity

| Domain | Maturity | Notes |
|---|---:|---|
| Apple ecosystem PIR / PNNS | Emerging production | Apple has public docs, an actively maintained Swift HE library, and named feature areas. |
| CT / revocation auditing | Prototype / research | Strong fit; SimplePIR paper gives concrete costs; production integration remains specialized. |
| Safe Browsing / URL checks | Emerging | Brave and Apple both describe this as a target; details vary by product. |
| Contact discovery | Production adjacent | Signal deployed TEE-based private contact discovery; cryptographic PIR / PSI variants are research-to-deployment. |
| Private web search | Research prototype | Tiptoe demonstrates feasibility over large corpora but not a public search product. |
| Ethereum state reads | Early research | Active discussions and prototypes, but no widely deployed wallet default. |
| General-purpose PIR-as-a-service | Early commercial | Blyss and similar efforts show demand; integration remains application-specific. |

## Late-May / June 2026 Developments

### Vitalik Ethereum Privacy Roadmap (April 2026)

Vitalik Buterin published a short-term privacy roadmap in April 2026 proposing a nine-step plan to make privacy a native feature of Ethereum rather than a third-party bolt-on. The core thesis: "a large portion of sends are private, and private sends are default in many cases," with activity inside individual applications remaining public but cross-application links private.

Key elements relevant to PIR:
- **Privacy pools** as an initial step: incorporating privacy tools into existing wallets (not separate apps) with an option to "send from shielded balance."
- **FOCIL (Fork-inclusive Optimistic Lists)**: a committee of validators proposes transaction lists that builders are required to include, removing the public mempool as a visibility vector for private transactions.
- **Account abstraction + keyed nonces**: enabling privacy-native account models without consensus changes.
- **Kohaku roadmap (Ethereum Foundation)**: explicitly includes privacy-service abstraction as a first-phase deliverable, moving wallet-side tooling for private reads from theory to implementation.

The connection to PIR is direct: private reads from Ethereum state (balances, nonces, storage slots, token positions) without revealing which account to the RPC provider is the missing piece in Vitalik's privacy architecture. Helios (a16z crypto's light client) + a PIR layer over Ethereum state is the reference design for the wallet-side implementation path.

Source: [Vitalik privacy roadmap](https://x.com/VitalikButerin/status/1910506160349921667), [The Defiant](https://thedefiant.io/news/blockchains/vitalik-buterin-unveils-roadmap-for-improving-privacy-on-ethereum), [CryptoSlate](https://cryptoslate.com/ethereum-may-finally-kill-trust-me-wallets-in-2026-and-vitalik-says-the-fix-is-already-shipping)

### Helios Light Client — Trustless RPC Verification

Helios (a16z crypto) is a Rust-based Ethereum light client that converts data from an untrusted centralized RPC provider into a verifiably safe local RPC. The client syncs in ~2 seconds, requires no storage, and runs on mobile and browser extensions.

The Helios model matters for PIR because the privacy gap starts at the RPC layer: even with PIR hiding which record is fetched from the database, if the client uses a standard RPC provider to query the PIR server, the RPC provider sees the query. Helios provides verified RPC data without trusting the provider. Combined with PIR over the data layer, this gives a full-stack privacy guarantee: the RPC provider sees nothing about which state is being read, the PIR server sees nothing about which record is being queried.

For the Kohaku reference wallet (Ambire fork), the combination of Helios + privacy-service abstraction is the first-phase deliverable. This positions PIR not as an academic tool but as infrastructure plumbing for mainstream Ethereum privacy.

Source: [a16z crypto blog](https://a16zcrypto.com/posts/article/building-helios-ethereum-light-client), [GitHub](https://github.com/a16z/helios)

### Apple Swift Homomorphic Encryption — Live Caller ID Deployment

Apple's Live Caller ID Lookup feature (iOS 18) uses homomorphic encryption for caller ID and spam blocking. The system encrypts the phone number query server-side and evaluates it against an encrypted database without learning the specific number. This is the same PIR-adjacent HE primitive Apple has shipped in production.

The swift-homomorphic-encryption GitHub repository (Apache 2.0) shows ongoing development: recent commits reference the 2024-2026 copyright period, documentation is actively maintained, and the whitepaper (Issue #39) asks about the differences between `aclsPir` and `mulPir` versus SimplePIR and HintlessPIR — confirming active implementation work.

The broader Apple research paper on combining ML and HE in the Apple ecosystem (Apple ML Research) documents the production stack: HE + PIR + private nearest-neighbor search for Enhanced Visual Search for Photos, and Live Caller ID Lookup. This represents the most visible large-scale deployment of HE/PIR technology.

Sources: [Swift Homomorphic Encryption](https://github.com/apple/swift-homomorphic-encryption), [Apple ML Research](https://machinelearning.apple.com/research/homomorphic-encryption)

### Browser-based PIR — WASM State

Browser-based PIR (clients running PIR protocols in the browser via WASM) is maturing. ChalametPIR explicitly ships a WASM client feature alongside its Rust implementation, enabling browser-integrated private lookups. The 2026 WASM ecosystem (Wasmtime LTS, Wasmer 6.0 at 95% native speed, WASI 1.0 in progress, Wasm Component Model maturing) provides the substrate for running PIR clients in-browser without native code.

This maps directly onto the privacy architecture: a browser extension containing a PIR client + Helios for verified state reads + NIP-07 signing for Nostr identity gives users privacy-preserving access to Ethereum state, public databases, and decentralized social without trusting the provider.

### GPU-Accelerated Batch PIR (Springer 2026)

A February 2026 paper published in Frontiers in Computer Science demonstrates GPU-accelerated batch PIR with lower communication overheads. This extends the GPIR (ICS 2026) direction: server-side PIR throughput is a GPU problem because the dominant cost is memory-bandwidth-bound homomorphic computation, which maps well to GPU parallelism.

The practical implication for decentralized compute: a GPU provider (Akash, Render, io.net, Aethir) can host a high-throughput PIR service in front of a public database, offering privacy-preserving queries as a service. Clients don't need GPUs; the server does.

## Primary sources

### Papers and talks

- Chor, Goldreich, Kushilevitz, Sudan, *Private Information Retrieval*, JACM 1998.
- Angel et al., *PIR with Compressed Queries and Amortized Query Processing*, IEEE S&P 2018 / SealPIR — https://eprint.iacr.org/2017/1142.pdf
- Mughees, Chen, Ren, *OnionPIR: Response-Efficient Single-Server PIR*, ACM CCS 2021.
- Menon & Wu, *Spiral: Fast, High-Rate Single-Server PIR via FHE Composition*, ePrint 2022/368 — https://eprint.iacr.org/2022/368
- Davidson, Pestana, Celi et al., *FrodoPIR: Simple, Scalable, Single-Server Private Information Retrieval*, ePrint 2022/981 — https://eprint.iacr.org/2022/981
- Henzinger, Hong, Corrigan-Gibbs, Meiklejohn, Vaikuntanathan, *One Server for the Price of Two: Simple and Fast Single-Server PIR*, ePrint 2022/949 / USENIX Security 2023 — https://eprint.iacr.org/2022/949
- Henzinger et al., *Private Web Search with Tiptoe*, SOSP 2023 / ePrint 2023/1438 — https://eprint.iacr.org/2023/1438
- Li, Micciancio, Raykova, Schultz-Wu, *Hintless Single-Server Private Information Retrieval*, ePrint 2023/1733 — https://eprint.iacr.org/2023/1733
- Menon & Wu, *YPIR: High-Throughput Single-Server PIR with Silent Preprocessing*, USENIX Security 2024 — https://www.usenix.org/conference/usenixsecurity24/presentation/menon
- Lehmkuhl, Henzinger, Corrigan-Gibbs, *Distributional Private Information Retrieval*, USENIX Security 2025 / ePrint 2025/132 — https://eprint.iacr.org/2025/132
- *Pirouette: Query Efficient Single-Server PIR*, ePrint 2025/680 — https://eprint.iacr.org/2025/680
- *Private Information Retrieval based on Homomorphic Encryption, Revisited*, ePrint 2025/729 — https://eprint.iacr.org/2025/729
- Henzinger & Ragavan, *Two-Server Private Information Retrieval in Sublinear Time and Quasilinear Space*, ePrint 2025/2008 / EUROCRYPT 2026 — https://eprint.iacr.org/2025/2008
- *VIA: Communication-Efficient Single-Server Private Information Retrieval*, ePrint 2025/2074 — https://eprint.iacr.org/2025/2074
- *Towards Making Doubly-Efficient PIR Practical*, ePrint 2026/243 — https://eprint.iacr.org/2026/243
- *Improved TensorPIR: Single-Server PIR with Lower Communication Cost*, ePrint 2026/912 — https://eprint.iacr.org/2026/912
- *Zeal: PIR for Non-Cooperative Databases*, ePrint 2026/684 — https://eprint.iacr.org/2026/684
- *Secret-Key PIR from One-Way Functions*, ePrint 2026/865 — https://eprint.iacr.org/2026/865
- *Streamlined Symmetric Private Information Retrieval via Rényi Divergence*, ePrint 2026/1051 — https://eprint.iacr.org/2026/1051
- *Private Information Retrieval: A Tutorial and Survey*, ePrint 2026/1135 — https://eprint.iacr.org/2026/1135

### Implementations and docs

- Apple Swift Homomorphic Encryption — https://github.com/apple/swift-homomorphic-encryption
- Apple ML Research, *Combining Machine Learning and Homomorphic Encryption in the Apple Ecosystem* — https://machinelearning.apple.com/research/homomorphic-encryption
- SimplePIR / DoublePIR reference implementation — https://github.com/ahenzinger/simplepir
- Spiral original implementation — https://github.com/menonsamir/spiral
- Spiral Rust implementation — https://github.com/menonsamir/spiral-rs
- Brave FrodoPIR — https://github.com/brave-experiments/frodo-pir
- Brave blog, *FrodoPIR: a new privacy-preserving approach for retrieving data* — https://brave.com/blog/frodopir/
- Microsoft SealPIR — https://github.com/microsoft/SealPIR
- Google HintlessPIR — https://github.com/google/hintless_pir
- Google Private Retrieval — https://github.com/google/private-retrieval
- PIR-PIXR Committed PIR — https://github.com/PIR-PIXR/CPIR
- PIREX — https://github.com/vt-asaplab/pirex
- ChalametPIR keyword PIR — https://github.com/itzmeanjan/ChalametPIR
- finite-diffs-pir two-server PIR reference implementation — https://github.com/ahenzinger/finite-diffs-pir
- InsPIRe Rust implementation — https://github.com/igor53627/inspire-rs
- PSE, *Private Information Retrieval for Ethereum Data* — https://pse.dev/projects/pir-ethereum-data
- Ethereum Research, *Sharded PIR Design for the Ethereum State* — https://ethresear.ch/t/sharded-pir-design-for-the-ethereum-state/24552
