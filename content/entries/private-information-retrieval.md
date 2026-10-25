---
title: "Private Information Retrieval"
slug: private-information-retrieval
type: explainer
pillars: ["cryptography"]
description: "Private information retrieval lets you fetch a record from a database without the server learning which record you asked for. How it works."
dek: "Allowing clients to retrieve specific database records without revealing the queried index or item to the server(s). A core primitive for privacy-preserving search, metadata-hiding systems, and decentralized applications."
updated: 2026-08-26
created: 2026-07-08
origin: vault
source: "13-Private-Information-Retrieval/Overview - Private Information Retrieval.md"
aliases: ["PIR", "Private Information Retrieval"]
tags: ["pir", "private-information-retrieval", "sealpir", "simplepir", "doublepir", "frodopir", "ypir", "thorpir", "fhe", "lwe", "privacy", "cryptography", "ethereum", "kohaku", "arithmetic-pir", "sk-pir", "gpu-pir", "lpn", "okvs", "share-conversion"]
---

## Why PIR Matters

Traditional database queries leak the client's interest to the server. PIR protocols cryptographically hide the query while still returning the correct record. This enables:

- Private web search / Wikipedia browsing
- Private DNS lookups
- Private contact discovery and blocklist checks
- Certificate Transparency auditing without leaking watched domains
- Private blockchain state queries (balances, UTXOs)
- Metadata-hiding messaging and media consumption
- Password breach checking without revealing passwords

PIR has seen major practical advances since ~2022, moving from theoretical curiosity to deployable systems with multi-GB/s throughput on commodity hardware. The field is now in a phase of rapid diversification: incremental preprocessing, GPU acceleration, hardware-coupled designs, keyword PIR, and verifiable variants are all active frontiers as of August 2026.

## Historical Context and Evolution

**Information-theoretic PIR (IT-PIR)**: Introduced in 1995 (Chor et al.). Requires multiple non-colluding servers; communication and computation scale with database size. Early schemes (CGKS 1998, etc.) were impractical for large DBs.

**Computational PIR (CPIR)**: Single-server, relies on cryptographic hardness (e.g., LWE, DDH). Early schemes (Kushilevitz & Ostrovsky 1997) had prohibitive computation.

**Modern era (2010s–2020s)**:
- XPIR (2014): First practical CPIR using lattice crypto.
- SealPIR (2018, Microsoft): Optimized query compression + amortized computation using Microsoft SEAL FHE. ~36ms per query on modest hardware.
- SimplePIR / DoublePIR (USENIX Security 2023, Henzinger et al.): Breakthrough single-server schemes achieving near-memory-bandwidth throughput (10 GB/s/core for SimplePIR) under LWE. Hint-based preprocessing enables unbounded queries after initial download.
- YPIR (USENIX Security 2024, Menon & Wu): Eliminates hints entirely via silent preprocessing; 12 GB/s/core throughput (83% of memory bandwidth); 10–15× faster preprocessing than SimplePIR family.
- ThorPIR (CCS 2024, Fisch et al.): First sublinear server-time scheme with sublinear offline communication via homomorphic Thorp shuffles.
- WhisPIR (ePrint 2024/266, de Castro et al.): Stateless PIR with low communication; ephemeral clients.
- VeriSimplePIR (USENIX Security 2024, de Castro et al.): Verifiability added to SimplePIR at no online cost.
- Respire (CCS 2024, Burton et al.): Optimized for small records (~256 B) — relevant for blockchain Merkle trees.

**2025–2026 wave**:
- FlashPIR (Cybersecurity journal, May 2026): Low-latency FHE-based PIR with low client overhead; 2.6× throughput over WhisPIR.
- ZipPIR (arXiv, March 2026): High-throughput without client preprocessing or server-side per-client state.
- RotPIR (ePrint 2026/1336): Up to 1000× preprocessing speedup via oblivious homomorphic rotation.
- iSimplePIR (ePrint 2026/030): First formal single-server incremental PIR — real-time entry-level database updates without full re-preprocessing.
- OnionPIRv2 (ePrint 2025/1142): Optimized single-server PIR using SHE advances.
- PIRCOR/RECPIR (ePrint 2025/756): Communication-optimal hintless PIR via homomorphic rotation.
- VIA (ePrint 2025/2074, to appear S&P 2026): Communication-efficient single-server PIR.
- Improved TensorPIR (ePrint 2026/912): 45.5% communication reduction over original TensorPIR.
- InsPIRe (ePrint 2025/1352): Server-side preprocessing for communication-efficient PIR.
- Pirouette (FHE.org 2026): Query-efficient PIR, novel alternative to transciphering for query compression.
- Conflux (HPCA 2026): Keyword PIR for dynamic datasets via protocol-architecture co-design with computational storage devices.
- PIRacle (IEEE TC 2026): Fast scalable PIR for key-value stores.
- GPIR (arXiv 2604.04696): GPU-accelerated, up to 305× throughput over prior GPU PIR.
- SmartPIR (MICRO 2025): PIR on computational storage devices (CSDs) — reducing data movement.
- KPIR (USENIX Security 2025): Practical keyword PIR from key-to-index mappings (KPIRkvs, KPIRhash, KPIRindex).
- IM-PIR (arXiv 2509.06514): Processing-in-memory PIR using DPUs.
- Conflux (HPCA 2026, Chen et al.): High-performance keyword PIR for dynamic datasets.
- Applebaum–Ishai–Shechter arithmetic PIR (CRYPTO 2026): single-server code-based PIR provably cannot beat n download; breaks ISIT'20/'24 code-based schemes in minutes. See [PIR Wednesday — August 19 2026 Weekly Update](/briefings/pir/2026-08-19/).
- Chen–Ishai–Jain–Mour–Rosen–Xing doubly-efficient SK-PIR (ePrint 2026/1480): first benchmarked SK-PIR — 4.2× storage overhead on 37 GB DB, <600 KB server reads per query.
- UC VPIR / UVPIR (ePrint 2026/1651): first universally-composable verifiable PIR, with authorized database updates.
- GPU DPF-PIR (TCHES 2026(3), Tan et al.): 8.2–9.4× throughput over prior GPU SOTA on RTX 4090; pipelined variant uses 99% less memory.

Key shift: From "impractical" to "practical for medium databases" with acceptable bandwidth and server throughput approaching raw memory speed. The 2025–2026 frontier focuses on: (1) removing preprocessing/hint dependencies, (2) keyword (not just index) PIR, (3) verifiable PIR against malicious servers, (4) GPU/CSD/PIM hardware acceleration, (5) incremental updates for dynamic databases, (6) real-world deployment in Ethereum privacy infrastructure, and (7) **information-theoretic PIR resurgence** — Henzinger & Ragavan (EUROCRYPT 2026) achieved the first IT-PIR with quasilinear storage and polynomially sublinear time, while Bitansky & Mazor (2026) proved SK-PIR needs only one-way functions.

## Major Implementations and Libraries

### Reference / Foundational

- **SealPIR** (Microsoft Research, 2018)
  - https://github.com/microsoft/SealPIR
  - Uses Microsoft SEAL for RLWE-based CPIR. Compressed queries, amortized server work.
  - Still widely referenced; research library (not production).

- **SimplePIR & DoublePIR** (2023)
  - https://github.com/ahenzinger/simplepir — 100 stars, MIT license, Go implementation.
  - Fastest known single-server throughput: SimplePIR ~10 GB/s/core; DoublePIR trades some speed for smaller hints (~16 MB fixed hint).
  - Paper: https://eprint.iacr.org/2022/949
  - See [SimplePIR and DoublePIR](/kb/simplepir-doublepir/) for the deep dive.

- **FrodoPIR** (Brave)
  - https://github.com/brave-experiments/frodo-pir
  - Stateful single-server scheme with offline phase. Highly configurable.

- **hintless_pir** (Google)
  - https://github.com/google/hintless_pir
  - Implements Li & Micciancio et al. (CRYPTO 2024) protocols. No client hints, no client-dependent server state.

- **YPIR** (Blyss / UT Austin)
  - https://eprint.iacr.org/2024/270
  - Silent preprocessing (no hint download); 12 GB/s/core; reduces CT log auditing cost by 48× vs prior art.

- **ThorPIR** (Yale)
  - https://eprint.iacr.org/2024/482 — CCS 2024.
  - Sublinear server time + sublinear offline communication via homomorphic Thorp shuffles.

- **WhisPIR** (de Castro, Lewi, Suh)
  - https://eprint.iacr.org/2024/266
  - Stateless, ephemeral clients, low communication. Implementation not publicly available.

- **VeriSimplePIR** (de Castro et al.)
  - https://www.usenix.org/conference/usenixsecurity24/presentation/de-castro — USENIX Security 2024.
  - Verifiable PIR: guarantees consistency with a fixed database at no online overhead.
  - Follow-up: "Verifiable PIR with Small Client Storage" (IEEE S&P 2026) — reduces client state from >1 GiB by orders of magnitude.

- **OnionPIRv2** (Chen & Ren)
  - https://github.com/chenyue42/OnionPIRv2
  - https://eprint.iacr.org/2025/1142 — optimized single-server PIR using SHE.

- **mpc4j** (Alibaba)
  - https://github.com/alibaba-edu/mpc4j
  - Contains incremental/offline-online PIR and other MPC primitives.

- **hybridpir**
  - https://github.com/KoffeinFlummi/hybridpir
  - Combines CIP-PIR (multi-server) and SealPIR (single-server).

### Recent / Specialized (2025–2026)

| Scheme | Venue / Source | Key Innovation | Repo |
|--------|---------------|----------------|------|
| FlashPIR | Cybersecurity journal, May 2026 | Low-latency FHE PIR, 2.6× over WhisPIR | — |
| ZipPIR | arXiv 2603.09190, Mar 2026 | High-throughput without client storage | — |
| RotPIR | ePrint 2026/1336 | 1000× preprocessing speedup via homomorphic rotation | — |
| iSimplePIR | ePrint 2026/030 | First single-server incremental PIR (entry-level updates) | — |
| GPIR (GPU) | arXiv 2604.04696 | GPU-accelerated, 305× over prior GPU PIR | — |
| SmartPIR | MICRO 2025 | PIR on computational storage devices (CSDs) | — |
| Conflux | HPCA 2026 | Keyword PIR for dynamic datasets (CSD co-design) | — |
| PIRacle | IEEE TC 2026 | Fast scalable PIR for key-value stores | — |
| KPIR | USENIX Security 2025 | Practical keyword PIR (kvs/hash/index) | — |
| Respire | CCS 2024 | Optimized for small records (~256 B) | — |
| VIA | ePrint 2025/2074 (S&P 2026) | Communication-efficient single-server PIR | — |
| Improved TensorPIR | ePrint 2026/912 | 45.5% communication reduction | — |
| InsPIRe | ePrint 2025/1352 | Server-side preprocessing, communication-efficient | — |
| Pirouette | FHE.org 2026 | Query-efficient, transciphering alternative | — |
| IM-PIR | arXiv 2509.06514 | Processing-in-memory PIR using DPUs | — |
| ChalametPIR | ePrint 2024/092 | Rust impl, keyword PIR | available |

**Stanford PIR Library** (survey & pointers): https://crypto.stanford.edu/pir-library/

**UT Austin PIR tutorial** (Wu, June 2024): https://www.cs.utexas.edu/~dwu4/talks/PIRGeneral0624.pdf — comprehensive overview slide deck covering 25 years of PIR research with throughput evolution.

## Use Cases and Trade-offs

### High-value use cases

- **Certificate Transparency**: Private SCT auditing. YPIR specifically reduces server costs for private CT log auditing by 48×. This is the most concrete near-term deployment vector.
- **Private search**: Tiptoe (SOSP 2023) demonstrates fully private web search using two non-colluding servers and PIR; ~57 MiB client state.
- **Apple / device features**: Logo lookup, caller ID lookup, content filtering via HE + PIR (iOS 18 Live Caller ID).
- **Password breach checking**: Checking credentials against breach databases without revealing the password. iSimplePIR explicitly targets this use case.
- **Ethereum / blockchain**: Private RPC reads so nodes don't learn what state the user queries. PSE project "PIR for Ethereum Data"; Vitalik's Kohaku privacy toolkit (2025); the sharded PIR design (ethresear.ch, Ali Atiia & Keewoo Lee) proposes sharding Ethereum state across multiple PIR schemes. See [PIR Use Cases and Deployments](/kb/pir-use-cases/).
- **Decentralized apps**: Private smart contract state queries, private contact discovery (Signal-style).
- **Ad / analytics**: Privacy-preserving measurement without leaking user interests.

### Trade-offs

- **Single-server vs multi-server**: Single-server (most practical) requires computational assumptions (LWE); multi-server offers information-theoretic security but deployment friction (non-collusion).
- **Hint size vs query cost**: SimplePIR has large per-client hints (~4N KB for N-byte DB) but tiny queries. DoublePIR shrinks hints at modest query cost increase. YPIR eliminates hints entirely via silent preprocessing. ZipPIR eliminates both hints and per-client server state.
- **Preprocessing / incremental updates**: Most schemes assume static DB. iSimplePIR (2026) is the first formal single-server incremental scheme — entry-level updates without full re-preprocessing. Conflux targets dynamic datasets for keyword PIR.
- **Throughput vs bandwidth**: Modern schemes achieve near-memory-bandwidth server throughput; client bandwidth is the remaining bottleneck for very large DBs.
- **GPU / hardware acceleration**: GPIR (GPU, 305×), SmartPIR (CSDs), IM-PIR (processing-in-memory) — emerging for high-scale deployments.
- **Security model**: Semi-honest servers assumed in most practical schemes. VeriSimplePIR adds verifiability (detects malicious server cheating) at no online cost. "Verifiable PIR with Small Client Storage" (S&P 2026) extends this with covert security for stateless clients.
- **Keyword vs index PIR**: Index PIR (retrieve by position) is the classical formulation. Keyword PIR (retrieve by key) is the practical need. KPIR (USENIX Security 2025) and Conflux (HPCA 2026) bridge this gap via key-to-index mappings.

**Maturity (August 2026)**: Research-to-early-production. The performance frontier has shifted from raw throughput (SimplePIR-class) to practical deployment concerns: incremental updates, keyword lookups, verifiability, and hardware acceleration. Production use is growing in Ethereum privacy layers (Kohaku, PSE PIR), Apple device features, and CT log auditing. Tiptoe demonstrates private web search is architecturally feasible but requires non-colluding server operators.

## Evidence at a Glance

| Scheme | Servers | Throughput (approx) | Hint Size | Query Comm. | DB Size Tested | Year | Notes / Link |
|--------|---------|---------------------|-----------|-------------|----------------|------|--------------|
| SealPIR | 1 | ~MB/s range | Small | Low | Medium | 2018 | Microsoft SEAL-based |
| SimplePIR | 1 | 10 GB/s/core | ~4N KB | ~242 KB | 1 GB | 2023 | https://github.com/ahenzinger/simplepir |
| DoublePIR | 1 | 7.4 GB/s/core | ~16 MB fixed | ~345 KB | 1 GB | 2023 | Same repo |
| FrodoPIR | 1 | Configurable | Stateful | Varies | Varies | ~2023 | Brave experiments |
| YPIR | 1 | 12 GB/s/core | Silent (no hint) | ~2.5 MB | 32 GB | 2024 | USENIX Sec '24, silent preprocessing |
| ThorPIR | 1 | Sublinear server time | Sublinear offline | Sublinear | Large | 2024 | CCS '24, Thorp shuffles |
| WhisPIR | 1 | ~1 GB/s | Stateless | Low | 1–8 GB | 2024 | Stateless, ephemeral clients |
| VeriSimplePIR | 1 | Same as SimplePIR | Same as SimplePIR + digest | Same | 8 GB | 2024 | USENIX Sec '24, verifiable |
| Respire | 1 | High for small records | Configurable | Low | Medium | 2024 | CCS '24, optimized for ~256 B records |
| GPIR (GPU) | 1 | 305× prior GPU | — | — | Large | 2026 | arXiv 2604.04696 |
| Pirex (OO) | 2 | High (client opt) | Low client | Very low | 1 TB | 2025 | 55 ms for 4 KB entry |
| NPiR | 1 | High-rate | Optimized | Moderate | Medium | 2026 | eprint 2025/2257 |
| Distributional PIR | 1 | Faster under skew | Varies | Lower | Large | 2025 | USENIX Sec '25 |
| FlashPIR | 1 | 2.6× WhisPIR | Low | Low | 1–8 GB | 2026 | Cybersecurity journal |
| ZipPIR | 1 | High | None | Low | Large | 2026 | arXiv 2603.09190, no client storage |
| RotPIR | 1 | Sublinear online | 1000× faster preprocessing | Sublinear | Large | 2026 | ePrint 2026/1336 |
| iSimplePIR | 1 | Same as SimplePIR | Incremental updates | Same | Medium | 2026 | ePrint 2026/030, entry-level updates |
| VIA | 1 | High | Optimized | Low | Large | 2026 | S&P 2026, ePrint 2025/2074 |
| Improved TensorPIR | 1 | High | Optimized | 45.5% of original | Large | 2026 | ePrint 2026/912 |
| KPIR | 1 | High (keyword) | Varies | Low | 2^20 entries | 2025 | USENIX Sec '25, keyword PIR |
| Conflux | 1 | High (keyword) | Dynamic | Low | Dynamic | 2026 | HPCA '26, CSD co-design |
| Henzinger & Ragavan IT-PIR | 2 | Sublinear: 12·n^0.63 | 1.5·√(log n)·n | 4.4 MB (11 GB DB) | 11 GB | 2026 | EUROCRYPT '26, first sublinear-time IT-PIR |
| Bitansky & Mazor SK-PIR | 1 (SK) | Sublinear | Secret key offline | Õ(√N) | Theoretical | 2026 | ePrint 2026/865, from OWFs |
| Döttling Minicrypt Batch | 2 | Batch-amortized | — | Batch-efficient | Large | 2025 | ePrint 2025/1406, Minicrypt |

## Research Frontier (August 2026)

The field is in an explosive diversification phase. Key open problems being actively addressed:

1. **Incremental / dynamic databases**: iSimplePIR (entry-level updates), Conflux (keyword PIR for dynamic data), PIRacle (key-value stores). The static-DB assumption is being dismantled.
2. **Keyword PIR**: KPIR, Conflux, ChalametPIR. Practical systems need keyword lookup, not just index-based retrieval.
3. **Verifiability**: VeriSimplePIR, "Verifiable PIR with Small Client Storage" (S&P 2026), covert vPIR. Detecting malicious servers that return wrong results.
4. **Hardware acceleration**: GPIR (GPU), SmartPIR (CSDs), IM-PIR (processing-in-memory), IVE (custom ASIC, Kim et al. 2026). PIR's memory-bound nature makes it ideal for near-data processing.
5. **Communication reduction**: FlashPIR, ZipPIR, VIA, Pirouette, InsPIRe, Improved TensorPIR. Reducing client-to-server communication remains the primary deployment bottleneck.
6. **Preprocessing elimination**: YPIR (silent), WhisPIR (stateless), ZipPIR (no client storage). Removing the hint download barrier.
7. **Ethereum integration**: Sharded PIR design (ethresear.ch), Kohaku privacy toolkit, PSE PIR project, Oblivious Labs → Kohaku pipeline (EF Q1 2026 funded). The first major platform-level deployment target.
8. **Information-theoretic PIR resurgence** (NEW Aug 2026): Henzinger & Ragavan (EUROCRYPT 2026) achieved first IT-PIR with quasilinear storage n^{1+o(1)} and polynomially sublinear server time n^{1-Ω(1)} using just 2 servers — 4.5M× smaller data structure than prior IT-PIR. Reopens two-server deployment paradigm.
9. **Foundational cryptographic requirements** (NEW Aug 2026): Bitansky & Mazor proved SK-PIR needs only one-way functions (ePrint 2026/865). Chen et al. (STOC 2026) construct SK-PIR from LPN. Evidence mounting that secret-key PIR is fundamentally easier than public-key PIR.
10. **Batch PIR from Minicrypt** (NEW Aug 2026): Döttling's batch two-server PIR from Minicrypt assumptions (ePrint 2025/1406). Amortized batch retrieval without public-key crypto.
11. **Negative results & arithmetic PIR** (NEW Aug 19 2026): Applebaum–Ishai–Shechter (CRYPTO 2026, ePrint 2026/1224) prove no single-server arithmetic PIR beats n download — killing code-based single-server PIR (ISIT'20/'24 schemes broken in minutes). Meanwhile PIR research *exported* a quasipolynomial McEliece distinguisher (ePrint 2026/1630), born from a failed PIR-from-LDC attempt.
12. **Benchmarked secret-key PIR** (NEW Aug 19 2026): ePrint 2026/1480 gives the first doubly-efficient SK-PIR with constant (→1×) storage overhead and concrete benchmarks — 37 GB DB at 4.2× overhead, <600 KB server reads/query — from new t-smooth LDCs (concatenated-curve Reed–Muller, curve-lifted codes).
13. **Composable verifiable PIR** (NEW Aug 19 2026): UC-secure VPIR + Updatable VPIR (ePrint 2026/1651); Updatable OKVS with access control powering PIR-based multi-key searchable encryption (ePrint 2026/1590, FrodoPIR backend).
14. **Fewer-server IT-PIR** (NEW Aug 19 2026): ePrint 2026/1515 achieves prior communication with exponentially fewer servers (2^{O(s)} → s), unconditional for s ≤ 15; quantum ceiling set by QPIR-from-OWFs note (ePrint 2026/1524).
15. **t-private wall + LPN consolidation** (NEW Aug 26 2026): Alon (ePrint 2026/1780) proves no t-private Z_m→F_q share conversion for t≥2 — the matching-vector framework cannot yield t-private PIR. On the positive side, RC-PIR (ePrint 2026/1372, Applebaum–Shechter) grounds two-server non-collusion in a retrieval-only static host under ternary LPN, and the SK-PIR secret-dual-code toolbox exports to encrypted matrix-vector products at <2× plaintext cost (ePrint 2025/858). LPN now carries SK-PIR, batch PIR, EMVP, and RC-PIR simultaneously.
16. **OKVS goes dynamic** (NEW Aug 26 2026): Multi-PGBF (ePrint 2026/1774, encode 65–78% faster than RR; decode ~90–96% faster than RB-OKVS) and updatable one-pass multi-party PSI (ePrint 2026/1772), joining UOKVS (2026/1590) — three updatable/fast OKVS results in 14 days.

For privacy across storage reads and writes, see [oblivious RAM](/kb/oblivious-ram/).
