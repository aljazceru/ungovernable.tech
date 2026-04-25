---
title: "Private Information Retrieval (PIR)"
tags:
  - "pir"
  - "cryptography"
  - "privacy"
  - "homomorphic"
  - "confidential-inference"
---
*Fetching item `i` from a public database without the database (or anyone watching it) learning `i`.*

---

## The problem

Searching public data leaks intent. "Symptoms of X disease" tells the server who is worried about X. Wikipedia article fetches, DNS lookups, CRL checks, certificate transparency queries, key-server lookups, and LLM retrieval over a public corpus all leak which record was accessed, often more sensitive than the record's contents.

PIR lets a client retrieve record `i` from an `n`-record database while the server(s) learn nothing about `i` beyond its length.

---

## Taxonomy

### Information-theoretic PIR (IT-PIR)

The database is replicated across `k` non-colluding servers. The client splits its query into `k` shares; each share alone reveals nothing in the Shannon sense. Servers cannot cheat without colluding.

- Pro: unconditional privacy, fast, no heavy crypto.
- Con: requires multiple non-colluding servers, a strong trust assumption.
- Representative systems: Chor-Goldreich-Kushilevitz-Sudan (1995, original), Percy++.

### Computational PIR (CPIR)

Single server. Privacy rests on a hardness assumption, usually LWE or another lattice problem.

- Pro: single server, no collusion assumption.
- Con: historically very expensive. The server has to process the entire database for every query, otherwise the access pattern leaks.
- Breakthroughs (2020 onward): SealPIR, FrodoPIR, Spiral, SimplePIR, DoublePIR, YPIR. Practical single-server PIR now exists at hundreds of MB/s server throughput with modest client compute, via LWE and careful offline/online splits.

### Hybrid and batch

- Batch PIR amortizes cost across many queries (Angel-Setty, MulRound).
- Keyword PIR extends index lookup to keyword lookup; SimplePIR has a keyword variant.
- Stateful PIR (DoublePIR, YPIR) has the client cache a large "hint" from a one-shot offline phase, so online queries become tiny.

---

## Why it matters for this vault

### Confidential inference (primary link)

- **RAG without access-pattern leaks.** A confidential LLM behind a TEE still reveals which document it retrieved. Memory controllers see HBM accesses, and any external vector-DB call obviously leaks the index. PIR-based retrieval keeps the document identity hidden from the retrieval server. Pair with a TEE for the generation step.
- **Private model-weight streaming.** Large models exceed HBM; swapping tiles from object store leaks which experts activate. PIR over model shards closes that leak.

### Encrypted messaging and contact discovery

Finding whether a contact uses a service without revealing the query. Signal's contact discovery is a TEE-based PIR analogue; cryptographic PIR (FrodoPIR-style) removes the TEE dependency.

### DNS, CT, revocation

- Private DNS lookups (ObliviousDoH plus PIR on recursive caches).
- Private certificate revocation checks (CRLite plus PIR).
- Private Safe Browsing lookups (Google's design uses a close cousin of PIR).

### Wikipedia, search, package managers

Every `apt-get`, every `pip install`, every Wikipedia read leaks what you're building or researching. PIR-backed mirrors are an active research track.

---

## Systems and libraries

### Production-grade single-server CPIR

| System | Flavor | Throughput | Status |
|--------|--------|------------|--------|
| **YPIR** (Menon-Wu, 2024) | CPIR (LWE) | 12.1 GB/s/core (32GB DB) | Best single-server |
| **SimplePIR / DoublePIR** (Henzinger et al., 2023) | CPIR (LWE) | 10.3 GB/s/core | Active, widely cited |
| **FrodoPIR** (Brave, 2023) | CPIR (LWE) | ~1.2 GB/s | Production at Brave |
| **Spiral / SpiralStream** (Menon-Wu, 2022) | CPIR (FHE) | 1.9 GB/s (streaming) | High-rate design |
| **SealPIR** (Microsoft Research, 2018) | CPIR (BFV) | 97 MB/s | Early practical |

### Specialized implementations

| System | Domain | Notes |
|--------|--------|-------|
| **Tiptoe** (MIT, 2023) | Private search | Private web search over 360M pages |
| **GPIR** (2026) | GPU acceleration | arxiv:2604.04696, stage-aware kernels |
| **PIRonGPU** (2025) | GPU PIR | GitHub: Alisah-Ozcan/PIRonGPU |
| **GPU-DPF** (Meta, 2025) | Distributed Point Functions | On-device ML inference |
| **Percy++** | IT-PIR | Multi-server, mature |
| **Blyss** | Managed service | Commercial confidential-AI platform |

### Research-grade and recent (2025-2026)

| Paper | Venue | Contribution |
|-------|-------|--------------|
| **Incremental Single-Server PIR** (2026) | ePrint 2026/030 | Reduces preprocessing costs |
| **Batch PIR with GPU Lower Communication** (2025) | Springer | Cuckoo hash batch PIR |
| **Distributional PIR** (2025) | ePrint 2025/132 | Optimizes for popularity distributions |
| **LightPIR** (2024) | ACM ASIACCS | FHE without Gaussian noise |

---

## Trade-offs

### Strengths

- Cryptographic, not hardware-based. No TCB to trust.
- Composes cleanly with TEEs, FHE, and MPC.
- Throughput is now production-grade for many workloads.

### Limitations

- Server cost scales with DB size per query. A 1GB database needs tens of milliseconds of server compute per query in the best systems; not free.
- Bandwidth. Offline-hint schemes move hundreds of MB to the client once.
- Updates. Static-DB PIR is easy; updatable PIR is an active research area, and most production deployments rebuild hints periodically.
- Metadata. PIR hides what you queried, not that you queried or how often. Combine with mix networks or padding.

### 2025-2026 developments

The field continues to advance on several fronts:

1. GPU acceleration. GPIR (arxiv:2604.04696) reports significant speedups via stage-aware kernel design on CUDA GPUs, optimizing data layout and execution scheduling for batch queries.

2. Lower communication. Cuckoo hash-based batch PIR cuts bandwidth by about 3x over prior art, per a Springer 2025 paper.

3. Distributional PIR. A new paradigm that optimizes for query popularity distributions, giving faster expected query times for realistic workloads.

4. Incremental preprocessing. The 2026 ePrint paper reduces preprocessing overhead when the database updates incrementally.

5. Production deployment. Brave continues to use FrodoPIR; Blyss offers managed PIR services for confidential AI inference.

---

## Attack surface

- Query-size leakage. Variable query sizes give away classes of records.
- Timing. Server compute variations can leak information.
- Collusion (IT-PIR only).
- Side channels on the client-side hint. If the hint is used insecurely, it can leak prior queries.
- Implementation bugs. LWE-based libraries are cryptographically dense; audits matter.

---

## Related files

- [Overview - Fully Homomorphic Encryption](/cryptography/overview-fully-homomorphic-encryption)
- [Confidential-AI-Inference](/confidential-computing/confidential-ai-inference)
- [Private-LLM-Inference-Patterns](/confidential-computing/private-llm-inference-patterns)
- [Overview - Encrypted Messaging](/encrypted-messaging)

## Primary sources

### Academic papers

- Chor et al., *Private Information Retrieval*, JACM 1998
- Henzinger et al., *One Server for the Price of Two: Simple and Fast Single-Server PIR*, USENIX Security 2023
- Menon & Wu, *YPIR: High-Throughput Single-Server PIR*, USENIX Security 2024
- Davidson et al., *FrodoPIR*, PoPETS 2023
- Henzinger et al., *Private Web Search with Tiptoe*, SOSP 2023
- Menon & Wu, *SPIRAL: Fast, High-Rate Single-Server PIR via FHE Composition*, IEEE S&P 2023
- *GPIR: Enabling Practical Private Information Retrieval with GPUs*, arxiv:2604.04696 (2026)
- *GPU-accelerated Batch Private Information Retrieval with Lower Communication*, Springer (2025)
- *Distributional Private Information Retrieval*, ePrint 2025/132
- *Incremental Single-Server Private Information Retrieval*, ePrint 2026/030
- *LightPIR: Single-Server PIR via FHE without Gaussian Noise*, ACM ASIACCS 2024

### Implementations

- [simplepir](https://github.com/ahenzinger/simplepir) — SimplePIR/DoublePIR reference implementation
- [frodo-pir](https://github.com/brave-experiments/frodo-pir) — Brave's FrodoPIR
- [tiptoe](https://github.com/ahenzinger/tiptoe) — Tiptoe private search
- [YPIR](https://zenodo.org/records/13117988) — YPIR implementation
- [PIRonGPU](https://github.com/Alisah-Ozcan/PIRonGPU) — GPU-accelerated PIR
- [GPU-DPF](https://github.com/facebookresearch/GPU-DPF) — Meta's GPU DPF for PIR
- [blyss/sdk](https://github.com/blyssprivacy/sdk) — Blyss homomorphic encryption SDK

