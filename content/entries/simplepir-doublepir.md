---
title: "SimplePIR and DoublePIR"
slug: simplepir-doublepir
type: deep-dive
pillars: ["cryptography"]
readiness: research
description: "SimplePIR and DoublePIR, single-server private information retrieval schemes that run close to memory bandwidth: how they work and their costs."
dek: "The breakthrough single-server PIR schemes (USENIX Security 2023) that brought server throughput to near-memory-bandwidth limits, establishing the performance baseline that all subsequent PIR research measures against."
updated: 2026-10-25
created: 2026-08-05
origin: vault
source: "13-Private-Information-Retrieval/SimplePIR and DoublePIR.md"
aliases: ["SimplePIR", "DoublePIR"]
tags: ["pir", "simplepir", "doublepir", "lwe", "lattice", "single-server", "preprocessing", "regev-encryption", "usenix-sec23"]
---

**Paper**: "One Server for the Price of Two: Simple and Fast Single-Server Private Information Retrieval" — Alexandra Henzinger, Jason Hennessey, Matthew Hong, Yuval Ishai, Eyal Kushilevitz, Robin Li, Ananth Raghunathan, Vinod Vaikuntanathan, Tudor Dimitriou (MIT, Technion, Boston University). USENIX Security 2023.

**ePrint**: https://eprint.iacr.org/2022/949
**Repo**: https://github.com/ahenzinger/simplepir (100 stars, MIT license, Go)
**Slides**: https://people.eecs.berkeley.edu/~henrycg/files/academic/pres/simplepir-slides.pdf

## Core Idea

SimplePIR and DoublePIR are single-server PIR schemes built on the Learning With Errors (LWE) assumption. They demonstrate that a single server can achieve the throughput of a two-server scheme — hence "one server for the price of two."

The key insight is that the "square-root" communication PIR scheme of Kushilevitz and Ostrovsky (1997) can be instantiated with Regev encryption (LWE-based), and **99.9% of the server's work** can be moved into a one-time preprocessing phase that produces a database-dependent "hint." The online phase then reduces to a matrix-vector product that runs at memory-bandwidth speed.

### SimplePIR: High Throughput

On a database of N bytes:

| Property | Value |
|----------|-------|
| Client hint (one-time download) | 4096 · √N bytes |
| Per-query communication | 8 · √N bytes |
| Server work per query | 2N 32-bit operations |
| Server throughput | ~10 GB/s/core |
| Security assumption | LWE |
| Max DB tested | 1 GB (extends further) |

SimplePIR's hint is proportional to the database size (4096 · √N). For a 1 GB database, the hint is ~128 MB. This is the scheme's main drawback — the client must download and store a large hint.

### DoublePIR: Less Communication

DoublePIR adds a second dimension of processing to shrink the hint to a fixed ~16 MB regardless of database size (for 1-byte records). This comes at a modest throughput cost (7.4 GB/s/core vs SimplePIR's 10 GB/s/core).

| Property | SimplePIR | DoublePIR |
|----------|-----------|-----------|
| Throughput | 10 GB/s/core | 7.4 GB/s/core |
| Hint size | ~4√N KB (large) | ~16 MB (fixed) |
| Query communication | 8√N bytes | ~8√N bytes (slightly larger) |
| Matrix dimensions | √N × √N | Two-level: √(√N) × √(√N) per level |
| Best for | Max throughput, small DBs | Large DBs where hint size matters |

## How It Works

### Setup (Preprocessing)

1. The database D is reshaped into a √N × √N matrix over ℤ_q (integers modulo q).
2. A random public matrix A ∈ ℤ_q^{√N × √N} is generated.
3. The hint H = A · D (mod q) is computed. This is the expensive one-time step.
4. The client downloads H and stores it locally.

### Online Query

1. The client wants record at index i, corresponding to column c of D.
2. The client encrypts the query: it generates a Regev ciphertext e = A^T · s + μ · e_c + noise, where s is a secret key, e_c is a column selector vector, μ is a scaling factor, and noise ensures LWE security.
3. The server computes the answer: ans = e^T · D (mod q). Due to the structure, ans = s^T · (A · D) + μ · D[c] + noise = s^T · H + μ · D[c] + noise.
4. The client subtracts s^T · H (using its stored hint) to recover D[c].

The server's online computation is just a matrix-vector multiplication: O(√N · √N) = O(N) operations. Since this is memory-bandwidth-bound (streaming D once), throughput approaches the machine's memory bandwidth limit.

### DoublePIR's Two-Level Optimization

DoublePIR processes the query in two stages:
1. **First level**: Reduce from N items to √N candidates.
2. **Second level**: Reduce from √N candidates to 1 item.

This "square-root of square-root" approach means the hint only needs to cover the second level's matrix, dramatically reducing its size. The first level is computed without a hint because it reduces to a manageable intermediate result.

## Extensions

### Long Records

The SimplePIR/DoublePIR paper uses LWE dimension **n = 1024**. This is the lattice security parameter, distinct from database dimensions or record size.

### Batch Queries

Both schemes support batch queries — retrieving multiple records simultaneously. Batching amortizes the query setup cost and improves overall throughput. For SimplePIR, batching has minimal effect on throughput (it's already memory-bandwidth-limited). For DoublePIR, batching significantly improves throughput because the first-level computation dominates and can be shared across queries.

## The SimplePIR Family

SimplePIR became the foundational scheme that subsequent research extends. The "SimplePIR family" now includes:

| Variant | Innovation | Year |
|---------|-----------|------|
| SimplePIR | Baseline: 10 GB/s/core, LWE-based | 2023 |
| DoublePIR | Fixed ~16 MB hint via two-level processing | 2023 |
| YPIR | Silent preprocessing (no hint download) | 2024 |
| VeriSimplePIR | Verifiability at no online cost | 2024 |
| ThorPIR | Sublinear server time via Thorp shuffles | 2024 |
| iSimplePIR | Incremental entry-level updates | 2026 |
| RotPIR | 1000× faster preprocessing via homomorphic rotation | 2026 |
| ZipPIR | No client storage, no per-client server state | 2026 |
| FlashPIR | Low-latency, 2.6× over WhisPIR | 2026 |

The iSimplePIR paper (ePrint 2026/030) explicitly constructs entry-level and row-level incremental variants based on SimplePIR, with communication optimization for different update cycles.

## Performance Context

From the UT Austin PIR tutorial (Wu, June 2024), SimplePIR/DoublePIR sit at the top of the throughput evolution curve:

```
Server throughput (GB/s/core) over time:

1999 (KO97): ~0.001
2016 (XPIR):  ~0.01
2018 (SealPIR): ~0.1
2021 (FastPIR): ~1
2022 (Spiral):  ~5
2023 (SimplePIR): ~10  ← near memory bandwidth
2024 (YPIR):    ~12   ← 83% of memory bandwidth
```

The key takeaway: lattice-based cryptography (specifically LWE) provided the tool that made practical PIR possible. SimplePIR demonstrated that the theoretical "square-root" PIR communication bound is achievable at near-hardware-speed throughput.

## Code and Reproduction

The reference implementation is in Go (~1,400 LOC):

```bash
# Clone and test
git clone https://github.com/ahenzinger/simplepir.git
cd simplepir
go test  # ~2.5 minutes for correctness tests

# Benchmark on 1 GB database
go run main.go -LOG_N=33 -D=1  # ~10 minutes
```

Key files:
- `pir/pir.go`: Core SimplePIR and DoublePIR implementations
- `pir/client.go`: Client-side operations
- `pir/server.go`: Server-side operations
- `eval/`: Benchmark and plotting scripts

To call from Go code:
```go
import "github.com/ahenzinger/simplepir/pir"
// See RunPIR and RunPIRCompressed in pir/pir.go
```

## Limitations and Open Problems

1. **Hint size**: SimplePIR's hint (~4√N KB) is impractical for very large databases. DoublePIR mitigates this but doesn't eliminate it. YPIR and WhisPIR address this directly.

2. **Static database assumption**: The original schemes assume the database never changes. If D changes, the hint H must be recomputed. iSimplePIR (2026) addresses this with incremental preprocessing.

3. **Semi-honest security**: The server is assumed to follow the protocol honestly. VeriSimplePIR adds malicious-server detection.

4. **Index-only**: The schemes retrieve by index, not by keyword. KPIR (2025) bridges this gap.

5. **Single dimension**: SimplePIR uses a 2D matrix layout. Multi-dimensional approaches (TensorPIR, DoublePIR's two-level scheme) explore different dimensionality trade-offs.

## Primary sources

- [Henzinger et al.: One Server for the Price of Two, USENIX Security 2023](https://www.usenix.org/system/files/usenixsecurity23-henzinger.pdf)
