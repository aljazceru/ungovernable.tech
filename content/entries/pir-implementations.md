---
title: "PIR Implementations and Libraries"
slug: pir-implementations
type: reference
pillars: ["cryptography"]
description: "A tracker of private information retrieval implementations and libraries: single-server and multi-server schemes, performance and maturity."
dek: "Comprehensive tracker of all known PIR implementations, libraries, and codebases. Organized by era, maturity, and access method."
updated: 2026-10-14
created: 2026-08-05
origin: vault
source: "13-Private-Information-Retrieval/PIR Implementations and Libraries.md"
aliases: ["PIR Tracker", "PIR Libraries"]
tags: ["pir", "implementations", "libraries", "sealpir", "simplepir", "frodopir", "ypir", "thorpir", "whispir", "chalamet", "hintless", "onionpir", "gpu-pir", "keyword-pir", "tracker"]
---

## Foundational Implementations (Pre-2023)

### SealPIR
| Field | Value |
|-------|-------|
| **Source** | Microsoft Research |
| **Year** | 2018 |
| **Paper** | Angel, Chen, Laine, Setty, "PIR with Compressed Queries and Amortized Query Processing," IEEE S&P 2018 |
| **ePrint** | https://eprint.iacr.org/2017/1142.pdf |
| **Repo** | https://github.com/microsoft/SealPIR |
| **Language** | C++ (using Microsoft SEAL) |
| **License** | MIT |
| **Scheme** | RLWE-based CPIR |
| **Key feature** | Compressed queries + amortized server work |
| **Throughput** | ~MB/s range |
| **Status** | Research library; widely referenced, not production |

SealPIR was the first practical PIR library that researchers could reasonably experiment with. It compresses client queries to reduce communication and amortizes server-side computation across multiple database entries. While superseded in throughput by SimplePIR-class schemes, it remains important for understanding the FHE-based PIR approach.

### XPIR
| Field | Value |
|-------|-------|
| **Source** | Academic (Aguilar Melchor et al.) |
| **Year** | 2014/2016 |
| **Paper** | "XPIR: Private Information Retrieval for Everyone," PETS 2016 |
| **Scheme** | Lattice-based CPIR |
| **Status** | Historical; superseded |

### FastPIR (2021)
| Field | Value |
|-------|-------|
| **Year** | 2021 |
| **Scheme** | RLWE-based |
| **Note** | Improved SealPIR-class performance |

### Spiral (2022)
| Field | Value |
|-------|-------|
| **Source** | Stanford (Menon & Wu) |
| **Year** | 2022 |
| **Paper** | "Spiral: Fast, High-Rate Single-Server PIR via FHE Composition," IEEE S&P 2022 |
| **ePrint** | https://eprint.iacr.org/2022/368 |
| **Scheme** | FHE composition |
| **Note** | Reduced latency but still limited by expensive online homomorphic operations |

## The SimplePIR Family (2023–2026)

### SimplePIR / DoublePIR
| Field | Value |
|-------|-------|
| **Repo** | https://github.com/ahenzinger/simplepir |
| **Stars** | 100 |
| **Language** | Go (~1,400 LOC) |
| **License** | MIT |
| **Throughput** | SimplePIR: 10 GB/s/core; DoublePIR: 7.4 GB/s/core |
| **Paper** | USENIX Security 2023 |
| **Deep dive** | [SimplePIR and DoublePIR](/kb/simplepir-doublepir/) |

### YPIR
| Field | Value |
|-------|-------|
| **Source** | Blyss / UT Austin (Menon & Wu) |
| **Year** | 2024 |
| **Venue** | USENIX Security 2024 |
| **ePrint** | https://eprint.iacr.org/2024/270 |
| **Key innovation** | Silent preprocessing — eliminates hint download entirely |
| **Throughput** | 12 GB/s/core (83% of memory bandwidth) |
| **Preprocessing speedup** | 10–15× faster than SimplePIR family |
| **CT log auditing** | 48× cost reduction vs prior art |
| **Repos** | https://github.com/ahenzinger/tiptoe (Tiptoe uses YPIR concepts) |

YPIR is the current throughput champion. By removing the hint requirement through silent preprocessing, it removes the primary deployment barrier of the SimplePIR family while maintaining or exceeding throughput. The 48× cost reduction for CT log auditing makes private CT auditing economically viable for the first time.

### ThorPIR
| Field | Value |
|-------|-------|
| **Source** | Yale (Fisch, Lazzaretti, Liu, Papamanthou) |
| **Year** | 2024 |
| **Venue** | CCS 2024 |
| **ePrint** | https://eprint.iacr.org/2024/482 |
| **Key innovation** | Sublinear server time AND sublinear offline communication via homomorphic Thorp shuffles |
| **Note** | Addresses the "impractical homomorphic computation" problem of prior CP-PIR schemes |

### WhisPIR
| Field | Value |
|-------|-------|
| **Source** | de Castro, Lewi, Suh |
| **Year** | 2024 |
| **ePrint** | https://eprint.iacr.org/2024/266 |
| **Key innovation** | Fully stateless PIR — ephemeral clients, no stored state |
| **Communication** | Low per-query |
| **Throughput** | ~1 GB/s (1 GB DB), ~1.15 GB/s (8 GB DB) |
| **Implementation** | Not publicly available |
| **Citations** | 17 |

### VeriSimplePIR
| Field | Value |
|-------|-------|
| **Source** | de Castro et al. |
| **Year** | 2024 |
| **Venue** | USENIX Security 2024 |
| **Key innovation** | Verifiability at no online cost — guarantees consistency with a fixed database |
| **Client storage** | >1 GiB for 8 GB DB (addressed by follow-up) |
| **Follow-up** | "Verifiable PIR with Small Client Storage" (IEEE S&P 2026) — reduces client state by orders of magnitude; introduces covert vPIR for stateless clients |
| **Citations** | 27 |

### Respire
| Field | Value |
|-------|-------|
| **Source** | Burton, Menon, Wu |
| **Year** | 2024 |
| **Venue** | CCS 2024 |
| **Key innovation** | Optimized for databases with small records (~256 bytes) |
| **Relevance** | Blockchain Merkle tree leaf queries |

## Hintless / Stateless PIR

### hintless_pir (Google)
| Field | Value |
|-------|-------|
| **Repo** | https://github.com/google/hintless_pir |
| **Language** | C++ |
| **Build** | Bazel |
| **Paper** | Li, Micciancio, Raykova, Schultz-Wu, "Hintless Single-Server PIR," CRYPTO 2024 |
| **Components** | `hintless_simplepir`, `linpir`, `lwe`, `private_inference` |
| **Key innovation** | No client hints, no client-dependent server state, no interactive setup |
| **DB update** | Client doesn't need to be involved in processing DB updates |

This is Google's implementation of the hintless PIR paradigm. The `private_inference` directory suggests applications in privacy-preserving ML inference.

### FrodoPIR (Brave)
| Field | Value |
|-------|-------|
| **Repo** | https://github.com/brave-experiments/frodo-pir |
| **Source** | Brave Browser experiments |
| **Scheme** | Stateful single-server with offline phase |
| **Features** | Highly configurable; suitable for experimentation |

### OnionPIR / OnionPIRv2
| Field | Value |
|-------|-------|
| **Repo (v2)** | https://github.com/chenyue42/OnionPIRv2 |
| **Paper (v2)** | https://eprint.iacr.org/2025/1142 |
| **Scheme** | SHE-based single-server PIR |
| **Key innovation (v2)** | Optimized implementation incorporating standard orthogonal techniques and engineering improvements |
| **Citations** | 4 |

## 2025–2026 Frontier Implementations

### Keyword PIR

#### ChalametPIR
| Field | Value |
|-------|-------|
| **ePrint** | https://eprint.iacr.org/2024/092 |
| **Language** | Rust |
| **Scheme** | Keyword PIR |
| **WASM** | Browser-compatible client available |

#### KPIR (USENIX Security 2025)
| Field | Value |
|-------|-------|
| **Paper** | "Practical Keyword Private Information Retrieval from Key-to-Index Mappings" |
| **Source** | USENIX Security 2025 |
| **PDF** | https://www.usenix.org/system/files/conference/usenixsecurity25/sec25cycle1-prepub-1224-hao.pdf |
| **Variants** | KPIRkvs (sparse KVS), KPIRhash (hash-based), KPIRindex (index-based) |
| **Key innovation** | Generic transformation from keyword PIR to any standard (index) PIR using sparse key-value stores |
| **Comparison** | Outperforms ChalametPIR for 2^20 entries with 32-byte records |

#### Conflux (HPCA 2026)
| Field | Value |
|-------|-------|
| **Source** | Shandong University (Chen et al.) |
| **Venue** | HPCA 2026 |
| **URL** | https://2026.hpca-conf.org/details/hpca-2026-main-conference/28/ |
| **Key innovation** | Keyword PIR for dynamic datasets via protocol-architecture co-design with computational storage devices (CSDs) |
| **Focus** | Reducing data movement through specialized hardware support |

#### PIRacle (IEEE TC 2026)
| Field | Value |
|-------|-------|
| **Source** | Shandong University (Chen et al.) |
| **Venue** | IEEE Transactions on Computers, 2026 |
| **URL** | https://www.computer.org/csdl/journal/tc/2026/04/11359596/2dsHojHBHUs |
| **Key innovation** | High-performance PIR for key-value stores |

### Hardware-Accelerated PIR

> **Aug 19 2026 update**: the new published GPU ceiling is the TCHES 2026(3) DPF-PIR paper (Tan, Zeng, Feng, Peng, Wang, He — Wuhan/Shandong): 8.20–9.39× throughput over Lam et al. (ASPLOS 2024) on RTX 4090 for 2^19–2^24 databases; pipelined variant 1.14–1.87× with up to 99% lower memory; ≥2.27× over preprocessing-PIR baselines. Techniques: GPU-oriented DPF tree expansion, distribution-aware access with thread-level coalescing, CUDA reduction primitives. DOI: 10.46586/tches.v2026.i3.933-957. See [PIR Wednesday — August 19 2026 Weekly Update](/briefings/pir/2026-08-19/).

#### GPIR (GPU)
| Field | Value |
|-------|-------|
| **Source** | arXiv 2604.04696 |
| **Key innovation** | GPU-accelerated PIR, up to 305× throughput over prior GPU implementations |
| **Compatibility** | Applicable to SimplePIR-family, Spiral, OnionPIRv2, and others with minimal modification |

#### SmartPIR (MICRO 2025)
| Field | Value |
|-------|-------|
| **Source** | Shandong University (Chen et al.) |
| **Venue** | MICRO 2025 (CCF-A) |
| **Key innovation** | PIR on computational storage devices (CSDs) — processing data near storage |
| **Focus** | Reducing data movement bottleneck |

#### IM-PIR (Processing-in-Memory)
| Field | Value |
|-------|-------|
| **Source** | arXiv 2509.06514 |
| **Key innovation** | PIR using processing-in-memory (PIM) via DPUs |
| **Focus** | Eliminating processor-memory data transfer bottleneck |

### Communication-Optimized PIR

#### FlashPIR
| Field | Value |
|-------|-------|
| **Source** | Cybersecurity journal (Springer Nature) |
| **Year** | 2026 (published May 21, 2026) |
| **DOI** | 10.1186/s42400-026-00601-7 |
| **Authors** | Dai, Xiang, Qin, Deng, Zhang |
| **Key innovation** | Low-latency FHE-based PIR with low client overhead; 2.6× over WhisPIR for 1 GB DB, 3.0× for 8 GB |

#### ZipPIR
| Field | Value |
|-------|-------|
| **Source** | arXiv 2603.09190 (March 2026) |
| **Key innovation** | High-throughput without client storage AND without per-client server state |
| **Note** | Addresses the resource constraints of limited client devices |

#### VIA
| Field | Value |
|-------|-------|
| **ePrint** | https://eprint.iacr.org/2025/2074 |
| **Venue** | To appear in IEEE S&P 2026 |
| **Authors** | Liu, Wang, Zhang |
| **Key innovation** | Communication-efficient single-server PIR |

#### InsPIRe
| Field | Value |
|-------|-------|
| **ePrint** | https://eprint.iacr.org/2025/1352 |
| **Authors** | Mahdavi, Patel, Seo, Yeo |
| **Key innovation** | Server-side preprocessing for communication-efficient PIR |

#### Pirouette
| Field | Value |
|-------|-------|
| **Venue** | FHE.org Conference 2026 (poster) |
| **Authors** | Kang, Schild (COSIC, KU Leuven) |
| **Key innovation** | Novel alternative to transciphering for reducing client-to-server communication |

#### Improved TensorPIR
| Field | Value |
|-------|-------|
| **ePrint** | https://eprint.iacr.org/2026/912 |
| **Authors** | Lv, Pan, Wang |
| **Key innovation** | 45.5% communication reduction over original TensorPIR |

### Preprocessing-Optimized PIR

#### RotPIR
| Field | Value |
|-------|-------|
| **ePrint** | https://eprint.iacr.org/2026/1336 |
| **Authors** | Zhang, Bian, Guan, Persiano |
| **Key innovation** | 1000× preprocessing speedup via oblivious homomorphic rotation |
| **Note** | Addresses the preprocessing bottleneck of CP-PIR (preprocessing PIR) schemes |

#### iSimplePIR
| Field | Value |
|-------|-------|
| **ePrint** | https://eprint.iacr.org/2026/030 |
| **Authors** | Lu, Xu, Li, Wang, Cui |
| **Key innovation** | First formal definition of single-server incremental PIR |
| **Variants** | Entry-level (real-time individual entry updates) and Row-level |
| **Use case** | Password breach detection with frequently updated databases |

### PIRCOR / RECPIR
| Field | Value |
|-------|-------|
| **ePrint** | https://eprint.iacr.org/2025/756 |
| **Title** | "RECPIR: Communication-Optimal Hintless Single-Server PIR via Homomorphic Rotation" |
| **Key innovation** | Rotation-optimized query expansion; highly parallel operation |

## Information-Theoretic & Foundational (2025–2026)

### Henzinger & Ragavan Two-Server IT-PIR (EUROCRYPT 2026)
| Field | Value |
|-------|-------|
| **ePrint** | https://eprint.iacr.org/2025/2008 |
| **Venue** | EUROCRYPT 2026 (DOI: 10.1007/978-3-032-25330-9_3) |
| **Authors** | Alexandra Henzinger, Seyoon Ragavan (MIT) |
| **Servers** | 2 (non-colluding) |
| **Security** | Information-theoretic (no crypto assumptions) |
| **Key innovation** | First IT-PIR with quasilinear storage n^{1+o(1)} AND polynomially sublinear server time n^{1-Ω(1)} |
| **Server storage** | 1.5·√(log₂ n)·n bits |
| **Server time** | 12·n^0.82 bits probed per query |
| **Improvement** | 4,500,000× smaller data structure than prior IT-PIR (BIM 2000) |
| **Memory accesses** | 2,560× fewer than linear-time PIR |
| **Communication** | 4.4 MB on 11 GB DB (reducible to n^0.31·poly(λ) with LHE) |
| **DB tested** | 11 GB with 1-byte records |
| **Technique** | Compact data structure for multivariate polynomial evaluation + Hasse derivatives via finite differences |
| **Extends** | Also improves 3+ server PIR (building on Ghoshal et al. TCC 2025) |

### Bitansky & Mazor Secret-Key PIR from OWFs
| Field | Value |
|-------|-------|
| **ePrint** | https://eprint.iacr.org/2026/865 |
| **Authors** | Nir Bitansky, Noam Mazor (NYU) |
| **Category** | Foundations |
| **Key innovation** | SK-PIR with Õ(√N) online communication from one-way functions alone |
| **Assumption** | One-way functions (minimal) |
| **Trade-off** | Client comm. Õ(N_c) × Server comm. Õ(N_s) where N_c · N_s ≥ N |
| **Construction** | Garbled circuits with uncorrelated input encoding |
| **Significance** | SK-PIR is fundamentally easier than public-key PIR — does not require lattice/DDH |
| **Related** | Chen, Ishai, Mour, Rosen (STOC 2026) — SK-PIR from high-noise LPN with N^ε communication |

### Döttling Minicrypt Batch PIR
| Field | Value |
|-------|-------|
| **ePrint** | https://eprint.iacr.org/2025/1406 |
| **Authors** | Nils Döttling |
| **Servers** | 2 (non-colluding) |
| **Setting** | Offline/online batch retrieval |
| **Key innovation** | Two-server batch PIR from Minicrypt assumptions (no public-key crypto) |
| **Citations** | 3 |

### Doubly-Efficient Secret-Key PIR with Low Storage Overhead (Aug 2026)
| Field | Value |
|-------|-------|
| **ePrint** | https://eprint.iacr.org/2026/1480 |
| **Authors** | Caicai Chen (Bocconi/Bending Spoons), Yuval Ishai (Technion/AWS), Aayush Jain (CMU), Tamer Mour (IIAI), Alon Rosen (Bocconi), Chaoping Xing (SJTU) |
| **Model** | Single server, secret-key preprocessing (stateless alternative to ORAM; SSE without access-pattern leakage) |
| **Key innovation** | First doubly-efficient SK-PIR with constant storage overhead (asymptotically →1×); k^{o(1)} communication and online server work |
| **Technique** | Permuted-code blueprint (BIPW/CHR TCC 2017) instantiated with new t-smooth LDCs — concatenated-curve Reed–Muller local decoder + curve-lifted codes |
| **Benchmark** | 37 GB DB of 18-bit records at 4.2× storage overhead; server reads <600 KB per query |
| **Significance** | First SK-PIR with concrete benchmarks; moves the SK-PIR line (Bitansky–Mazor 2026/865, Chen et al. STOC'26) from existence proof to engineering artifact |
| **Deployment angle** | SK-PIR model maps onto wallet ↔ RPC-provider relationships (one-time preprocessing, then private queries) |

### SkrrtPIR — Doubly-Stateless Batch PIR (Oct 2026)
| Field | Value |
|-------|-------|
| **ePrint** | https://eprint.iacr.org/2026/2385 |
| **IACR news** | https://iacr.org/news/item/30019 (Oct 8) |
| **Authors** | Keewoo Lee (Ethereum Foundation) + Yongha Son (Sungshin Women's University) |
| **History** | 2026-10-08 approved, 2026-10-06 received |
| **Category** | Cryptographic protocols |
| **Model** | Doubly-stateless Batch PIR — server stores no per-client state, client maintains no DB-dependent hint |
| **Key innovation** | First doubly-stateless Batch PIR (prior concretely-efficient schemes required per-client server state, making queries linkable across sessions). **Core technical ingredient: single-key RLWE unpacking** that replaces the traditional tree-based approach (which requires logarithmically many Galois keys) with a **linear walk over a cyclic Galois subgroup requiring only a single Galois key** |
| **Comparison point** | Natural baseline of "send fresh evaluation keys with each batch query" (the pre-SkrrtPIR status quo) |
| **Significance** | The Ethereum Foundation PIR research line is now publishing at one paper per week (2026/1959 Sep 13 → 2026/2412 Oct 8 → 2026/2385 Oct 6). Composes with RisePIR's incremental-keyword-PIR (2026/2082 Sep 18) for stateless-batch-private Ethereum RPC. Maps directly to wallet-deployment constraints (no per-client server state, no client-side DB hint) |
| **Code** | None published as of Oct 14 |

### Barely Sublinear RAM-FHE from Plain LWE (Oct 2026)
| Field | Value |
|-------|-------|
| **ePrint** | https://eprint.iacr.org/2026/2412 |
| **Author** | Keewoo Lee (Ethereum Foundation) — sole author |
| **History** | 2026-10-11 approved, 2026-10-08 received |
| **Category** | Foundations |
| **Key innovation** | First RAM-FHE from **plain (unstructured) LWE**; per-step o(N/log N) time. Prior Lin–Mook–Wichs STOC 2023 used Ring-LWE. Built by extending a DEPIR-from-plain-LWE-in-the-standard-model — the 4th DEPIR (after YPIR USENIX Sec'24, LMW STOC'23, Lee's CRYPTO 2026). The CRS-removal is the primary technical contribution |
| **Significance** | Plain LWE is the conservative post-quantum assumption (Ring-LWE has a known history of subfield attacks; plain LWE has held up to the longest sustained cryptanalytic effort). A RAM-FHE from plain LWE is the most conservatively post-quantum-secure RAM-FHE to date. **The DEPIR-from-plain-LWE in the standard model may be of independent interest** |
| **Code** | None published as of Oct 14 |

### Arithmetic PIR: Why Code-Based PIR (Usually) Fails — CRYPTO 2026
| Field | Value |
|-------|-------|
| **ePrint** | https://eprint.iacr.org/2026/1224 |
| **Venue** | CRYPTO 2026 (Santa Barbara, Aug 17–20 2026); presented by Shahar Shechter |
| **Authors** | Benny Applebaum (TAU), Yuval Ishai (Technion/AWS), Shahar Shechter (TAU) |
| **Main result** | Negative: no single-server arithmetic PIR (APIR) achieves non-trivial download < n field elements |
| **Attack** | Breaks Holzbaur et al. (ISIT'20) and Verma–Hollanti (ISIT'24) code-based PIR "within a few minutes on a standard workstation" for all suggested parameters |
| **Positive results** | Two-server APIR from DPF arithmetization (Boyle et al. CCS'16); SK-preprocessing APIR via Chen et al. STOC'26; IT two-server APIR at O(n^{1/3}) communication |
| **Impact** | Closes the code-based single-server PIR direction; PQ-friendly PIR must go lattice-CPIR or DPF-arithmetized |

### UC-Secure Verifiable & Updatable PIR (Aug 2026)
| Field | Value |
|-------|-------|
| **ePrint** | https://eprint.iacr.org/2026/1651 |
| **Key innovation** | First universally composable definition of single-server verifiable PIR (ideal VPIR functionality); proves game-based VPIR fails under composition |
| **UVPIR** | Updatable VPIR: updates authorized by permissioned clients; responses bound to a specific database version; black-box from any VPIR |
| **Realizations** | Trivial PIR and VeriSimplePIR (de Castro & Lee, USENIX Security 2024) |
| **Significance** | Merges verifiability + updates + composable security — the formalism needed to embed PIR in wallets/agent stacks as a building block |

### Updatable OKVS + PIR Multi-Key Searchable Encryption (Aug 2026)
| Field | Value |
|-------|-------|
| **ePrint** | https://eprint.iacr.org/2026/1590 |
| **Key innovation** | UOKVS: updatable oblivious key-value store with fine-grained access control; first oblivious-insertion analysis for Cuckoo hashing |
| **Application** | Multi-key searchable encryption without data replication across users — 0.6 s WAN queries (100-doc keywords) on 24M-entry Enron dataset at 3.1× storage |
| **PIR backend** | FrodoPIR — rare production-oriented benchmark of Brave's deployment-oriented scheme |

### McEliece Distinguisher from Failed PIR Research (Aug 2026)
| Field | Value |
|-------|-------|
| **ePrint** | https://eprint.iacr.org/2026/1630 |
| **Authors** | Ashrujit Ghoshal (IIT Madras), Yuval Ishai, Aayush Jain (CMU), Nuozhou Sun (CMU) |
| **Result** | Classical quasipolynomial (n^{O(log n)}) distinguisher for Goppa–McEliece public keys; applies to all Classic McEliece NIST parameter sets; extends heuristically to message recovery |
| **PIR connection** | Attack originated from a failed attempt to build doubly-efficient PIR from algebraic locally decodable codes; "can be intuitively explained from the PIR perspective" |
| **Cross-links** | [HQC](/kb/hqc/), PQC migration files — code-based PQC inherits the scrutiny |

### Fewer-Server PIR & Quantum Ceiling (Jul 2026)
| Field | Value |
|-------|-------|
| **ePrint** | https://eprint.iacr.org/2026/1515 (Gupta et al.) — s-server PIR with exp(O((log n)^{1/s} (log log n)^{1-1/s})) communication using only s servers (was 2^{O(s)}); unconditional for s ≤ 15; main result discovered in a GPT-5.5 Pro conversation |
| **QPIR** | https://eprint.iacr.org/2026/1524 (Ananth et al.) — single-server quantum PIR with polylog communication from post-quantum one-way functions (Kerenidis–Wolf ⨯ Gilboa–Ishai DPF) |
| **SoK** | https://eprint.iacr.org/2026/1544 — first systematization of confidential transformer inference + RAG covering the retrieval layer; no family dominates; private graph-RAG least served |

### UIUC PIR Survey
| Field | Value |
|-------|-------|
| **ePrint** | https://eprint.iacr.org/2026/1135 |
| **Authors** | Pranav Shriram Arunachalaramanan, Yue Chen, Ling Ren (UIUC) |
| **Type** | Tutorial and survey |
| **Coverage** | IT-PIR, CPIR, preprocessing, stateful, keyword PIR, batch PIR, concrete efficiency, paradigm selection |
| **Value** | Best newcomer entry point as of August 2026 |

### IVE Custom PIR Accelerator (Kim et al. 2026)
| Field | Value |
|-------|-------|
| **Authors** | Kim et al. |
| **Year** | 2026 |
| **Key innovation** | Custom accelerator architecture for single-server HE-based PIR with multi-client batching |
| **Features** | Large on-chip scratchpads, tightly scheduled execution |
| **Note** | Referenced in GPIR paper as baseline. Implementation not publicly available. |

### Dynamic MKFHE PIR (MDPI Electronics 2025)
| Field | Value |
|-------|-------|
| **Journal** | Electronics (MDPI), 2025 |
| **URL** | https://www.mdpi.com/2079-9292/14/17/3441 |
| **Key innovation** | PIR via Multi-Key FHE (MKFHE) supporting multiple data owners |
| **Features** | Dynamic database updates; polynomial ring encoding with automorphism transforms |
| **Focus** | Collaborative multi-party computation scenarios |

## Multi-Server / Specialized

### mpc4j (Alibaba)
| Field | Value |
|-------|-------|
| **Repo** | https://github.com/alibaba-edu/mpc4j |
| **Contents** | Incremental/offline-online PIR, MPC primitives |
| **Note** | Comprehensive MPC library with PIR components |

### hybridpir
| Field | Value |
|-------|-------|
| **Repo** | https://github.com/KoffeinFlummi/hybridpir |
| **Key innovation** | Combines multi-server IT-PIR (CIP-PIR) with single-server CPIR (SealPIR) |

### Piano
| Field | Value |
|-------|-------|
| **Venue** | IEEE S&P 2024 |
| **Authors** | Zhou, Park, Shi, Zheng |
| **Key innovation** | Extremely simple single-server PIR with sublinear server computation |
| **Note** | Requires streaming entire database to client during preprocessing |

### Tiptoe
| Field | Value |
|-------|-------|
| **Repo** | https://github.com/ahenzinger/tiptoe |
| **Stars** | 56 |
| **Venue** | SOSP 2023 |
| **Application** | Private web search using PIR |
| **Architecture** | Two non-colluding servers (ranking + URL services) |
| **Client state** | ~57 MiB |

## Survey and Reference Resources

| Resource | URL |
|----------|-----|
| **UIUC PIR Tutorial and Survey** (NEW Aug 2026) | https://eprint.iacr.org/2026/1135 |
| Stanford PIR Library | https://crypto.stanford.edu/pir-library/ |
| UT Austin PIR Tutorial (Wu 2024) | https://www.cs.utexas.edu/~dwu4/talks/PIRGeneral0624.pdf |
| IACR ePrint PIR category | https://eprint.iacr.org/complete/ (filter "private information retrieval") |
| PSE Ethereum PIR project | https://pse.dev/blog/ethereum-privacy-pir |
| Sharded PIR for Ethereum (ethresear.ch) | https://ethresear.ch/t/sharded-pir-design-for-the-ethereum-state/24552 |
| Kohaku roadmap | https://notes.ethereum.org/@niard/KohakuRoadmap |
| EF Q1 2026 Allocations | https://blog.ethereum.org/2026/04/29/allocation-q1-26 |

## Repo Watch Snapshot (verified 2026-10-14)

| Repo | Stars | Last Push | Note |
|------|------:|-----------|------|
| ethereum/kohaku | 402 | 2026-10-07 | W42 cycle: only new PR is **#316 (Oct 7) "feat(privacy-pools): account history"**; open PRs: #316 + #312 (Oct 3 zipcoin deployment) + #258 (Sep 17 PP v2 SDK); 7 PRs/commits in W42 window, none PIR-tagged |
| apple/swift-homomorphic-encryption | 655+ | 2026-10-12 | **5-PR merge cluster on main Sep 25 → Oct 12 (largest of 2026)**: #332 Sep 25 + #335 + #337 + #333 Oct 7 + #334 + #336 Oct 12. All 4 substantive W41 PRs by `@deadcaf3` (Karl Tarbe, GPG `9AAD1BD8BE87E79A` = same engineer as `@karulont`). **No v1.0.8 release tag yet (day 133 since v1.0.7 Jun 3)** |
| google/hintless_pir | 23 | 2026-07-23 | steady maintenance |
| menonsamir/spiral-rs | 18 | 2026-03-19 | dormant since March |
| itzmeanjan/ChalametPIR | 16 | 2025-07-11 | dormant 13+ months |
| brave-experiments/frodo-pir | 78 | 2024-01-10 | deployment reference, frozen |
| ahenzinger/simplepir | 101 | 2023-01-13 | research reference |
| ahenzinger/finite-diffs-pir | 0 | 2026-05-01 | EUROCRYPT 2026 IT-PIR reference |
| a16z/helios | 2,175+ | 2026-06-26 | Kohaku reference wallet's verified-reads client |
| **orochi-network/orochimaru** | 80 | **2026-07-10** | **95 days silent** as of Oct 14; last commit `95f95bd` "constraints/permutation_circuit.rs: PermutationCircuit::new_with_seeds" by `bao-ninh-orochi` + `on-unknown-fish`; **RisePIR source code still not publicly auditable** (the orochimaru release that Sep 23 / Sep 30 / Oct 7 sweeps predicted has not materialized) |
| **orochi-network/cuckoo-filter-rs** | — | — | **404 (no public repo)** as of Oct 14 — the RisePIR paper's primary artifact |
| **sidsabh/sandwichpir** | 2 | 2026-08-28 | **47 days silent since reference implementation**; 2 stars / 0 forks / 0 issues / 0 PRs; v0.1.0 tag Aug 25 the only release; hardware moat (CUDA 12.4 + L40S + CUTLASS 3.5.1 + saturating-int8 patch) unchanged |
