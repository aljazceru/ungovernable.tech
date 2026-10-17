---
title: "PIR Research Frontier"
slug: pir-research-frontier
type: deep-dive
pillars: ["cryptography"]
readiness: research
description: "The research frontier of private information retrieval: recent schemes, performance breakthroughs, open problems and what is close to deployment."
dek: "This note tracks the 2025–2026 edge of Overview - Private Information Retrieval: the work that is pushing PIR from \"fast enough in special cases\" toward deployable infrastructure for wallets, browsers, public-key directories, package metadata, and decentralized systems."
updated: 2026-06-17
created: 2026-05-06
origin: vault
source: "02-Cryptography/PIR 2025 Research Frontier.md"
aliases: ["PIR 2025", "Distributional PIR", "Query Efficient PIR", "Communication Efficient PIR"]
tags: ["pir", "private-information-retrieval", "cryptography", "privacy", "metadata-privacy", "research-tracker"]
---

This note tracks the 2025–2026 edge of [Overview - Private Information Retrieval](/kb/private-information-retrieval/): the work that is pushing PIR from "fast enough in special cases" toward deployable infrastructure for wallets, browsers, public-key directories, package metadata, and decentralized systems.

The short version: PIR research is no longer only about making one generic single-server construction faster. The frontier is splitting into **workload-specific PIR**:

- popularity-aware PIR for skewed public datasets;
- communication-minimal PIR for mobile and low-bandwidth clients;
- two-server information-theoretic PIR when independent operators are plausible;
- keyword/key-value PIR for application databases rather than abstract numeric arrays;
- sharded PIR for heterogeneous public state such as Ethereum.

## Why this matters for freedom tech

Freedom-tech systems often publish public data while making queries sensitive:

- a wallet checks an address, balance, note commitment, nullifier, contract storage slot, or token position;
- a browser checks a phishing, malware, adult-content, revocation, or certificate-transparency database;
- a Nostr client looks up a pubkey, relay index, event, social graph edge, or reputation record;
- a package manager checks update metadata or vulnerability information;
- a decentralized naming client checks a name record in [Overview - Decentralized DNS](/kb/decentralized-dns/).

Without PIR, the operator of the public database learns the user's intent. DoH, TLS, and authenticated APIs do not fix this; they simply move the leak to a different operator. PIR is one of the few primitives that directly hides the selected database record from the database holder.

The remaining question is cost. If every private lookup forces a server to scan a multi-gigabyte database, PIR stays niche. The 2025 papers below all attack that cost from different angles.

## Evidence at a glance

| Development | Primary source | Claim | Maturity |
|---|---|---|---|
| Distributional PIR | [ePrint 2025/132](https://eprint.iacr.org/2025/132), [USENIX page](https://people.eecs.berkeley.edu/~henrycg/pubs/distpir/) | 5–77× compute-cost reduction on two real-world popularity distributions; 8× end-to-end cost reduction in CrowdSurf. | USENIX Security 2025 research; compelling for skewed workloads. |
| Pirouette | [ePrint 2025/680](https://eprint.iacr.org/2025/680) | 36-byte query for `2^25` records; 420× smaller than Respire and 9.3× smaller than T-Respire in the paper's setting. | Paper-stage; implementation maturity still needs tracking. |
| HE-PIR revisited | [ePrint 2025/729](https://eprint.iacr.org/2025/729) | Reclassifies HE-PIR structures; reports 90% communication reduction and 8× computational reduction from a less-explored design. | Useful deployment-analysis paper. |
| Finite-differences two-server PIR | [ePrint 2025/2008](https://eprint.iacr.org/2025/2008), [GitHub](https://github.com/ahenzinger/finite-diffs-pir) | Two-server IT-PIR with quasilinear storage and polynomially sublinear server time; 11 GB DB becomes 1 TB encoded structure. | EUROCRYPT 2026 reference implementation; research prototype. |
| VIA | [ePrint 2025/2074](https://eprint.iacr.org/2025/2074) | 690 KB online communication for 32 GB DB without offline communication; 2.1 KB online communication with offline communication. | Paper-stage; source URL reportedly updated in ePrint metadata. |
| ChalametPIR | [GitHub](https://github.com/itzmeanjan/ChalametPIR) | Keyword PIR over key-value databases using FrodoPIR + Binary Fuse Filters; WASM client and GPU-assisted setup paths. | Young Rust implementation; 15 GitHub stars; pushed 2025-07-11. |
| Ethereum sharded PIR | [Ethereum Research](https://ethresear.ch/t/sharded-pir-design-for-the-ethereum-state/24552) | Shard Ethereum data by update profile and query all shards with decoys to preserve privacy. | Architecture proposal; important for wallet/RPC privacy. |

## 1. Distributional PIR

**Source:** Lehmkuhl, Henzinger, Corrigan-Gibbs, *Distributional Private Information Retrieval*, USENIX Security 2025 / ePrint 2025/132.

Classic PIR gives every record the same treatment. That is elegant but wasteful for real systems where a few records are extremely popular and most are rare. Distributional PIR keeps cryptographic query privacy but relaxes correctness: if the user's request follows the expected popularity distribution, the lookup succeeds with high probability; out-of-distribution lookups may fail more often.

This is not weaker query privacy in the usual cryptographic sense. The server still should not learn which item was requested. The new leak to manage is **success/failure behavior**: if a client only retries or changes behavior after failures, those reactions can reveal that the query landed outside the expected distribution.

### Best-fit deployments

- Nostr / social event retrieval where some events or profiles are hot.
- Package and software update metadata where popular packages dominate traffic.
- Public media catalogs and manifests.
- Safe Browsing or threat-intelligence lists with skewed access.
- App-store metadata or business-logo / caller-ID style directories.

### Trade-offs

- Great when popularity distributions are stable and skewed.
- Dangerous when correctness failures change client behavior in observable ways.
- Less compelling for uniformly accessed datasets or security-critical lookups where every record must succeed equally.

## 2. Query-efficient and communication-efficient PIR

Bandwidth is often the binding constraint for client-side privacy. A browser, mobile wallet, mesh node, or low-power device may tolerate server computation better than a huge upload or response. Two 2025 lines are notable:

### Pirouette

Pirouette targets tiny client queries. Its headline result is a **36-byte query** for `2^25` records, compared with 14.8 KB reported for Respire and 336 bytes for T-Respire in the paper's comparison. The paper frames its contribution as an alternative to transciphering: the client sends only one component of a high-precision LWE ciphertext, then the server reconstructs the inputs needed for later homomorphic computation.

Why this matters: if PIR is to live inside wallets, browsers, and intermittent networks, client-to-server communication needs to be boringly small.

### VIA / VIA-C / VIA-B

VIA focuses on online communication for single-server offline/online PIR. The paper reports:

- **VIA:** no offline communication, 690 KB online communication for a 32 GB database, 3.11 GB/s throughput.
- **VIA-C:** allows offline communication, 2.1 KB online communication for a 32 GB database with 14.8 MB offline communication.
- **VIA-B:** batch-query extension with reduced query and response sizes for small-record databases.

This is relevant to public databases that update in epochs: clients can pay an offline cost occasionally, then make cheap online queries.

### Design warning

Communication improvements can hide costs elsewhere: heavier server computation, more complicated parameter choices, brittle offline state, or narrower database shapes. For deployment, benchmark against the exact record size, update cadence, and batch pattern.

## 3. HE-PIR revisited

The 2025 *Private Information Retrieval based on Homomorphic Encryption, Revisited* paper is useful because it is not just another scheme. It asks a deployment question: among existing FHE/PIR structures, which design is actually best for a given database?

The paper reports that a less-explored structure can reduce communication by 90% and computational overhead by 8× compared with the more common approach in its evaluation. The practical lesson is that "use BFV / BGV / RLWE PIR" is not specific enough. Packing layout, query encoding, homomorphic selection algorithm, database dimensions, memory traffic, and response extraction dominate real performance.

Why it matters: treat this as a design-selection reference when evaluating [Overview - Fully Homomorphic Encryption](/kb/fully-homomorphic-encryption/)-based PIR systems.

## 4. Multi-server PIR returns

The original PIR construction assumed multiple non-colluding servers. That assumption is unattractive for centralized products but natural for some ungovernable infrastructure:

- independent civil-society mirrors;
- multiple Nostr indexing services;
- transparency-log mirrors;
- public package registry mirrors;
- blockchain data providers with different operators;
- community-run [Overview - Decentralized DNS](/kb/decentralized-dns/) resolvers.

Henzinger and Ragavan's finite-differences work shows two-server information-theoretic PIR with quasilinear server storage and sublinear server probes. The concrete numbers are not small: an 11 GB database with one-byte records becomes a 1 TB encoded data structure, and the protocol still has large communication. But the direction is important because it weakens the standard assumption that IT-PIR with a constant number of servers must be server-linear.

The reference implementation is `ahenzinger/finite-diffs-pir`, a Go research prototype for the EUROCRYPT 2026 paper.

## 5. Keyword PIR and ChalametPIR

Most real applications are key-value lookups, not numeric-index lookups. ChalametPIR is a practical bridge: it combines FrodoPIR with Binary Fuse Filters to retrieve values by keyword without revealing the queried key.

Notable implementation signals:

- Rust implementation split into client, server, and common crates.
- WASM client feature for browser-like environments.
- GPU-assisted server setup path; the README reports large setup speedups for larger databases in its benchmark environment.
- Benchmarks around `2^20` keys with 32-byte keys and 1 KB values.

This shape maps naturally onto:

- usernames / public keys;
- Nostr pubkeys or event IDs;
- DNS or naming records;
- package names;
- revocation entries;
- address-to-record lookup in wallet infrastructure.

Maturity is still early: as of the 2026-05-06 GitHub metadata check, the repo had 15 stars and last pushed 2025-07-11. Treat it as a useful implementation to study, not an audited production dependency.

## 6. Ethereum and sharded PIR

Ethereum state is not one neat PIR database. It contains hot mutable state, append-only block/receipt data, logs, historical state, account proofs, token balances, contract storage, and application-specific indexes. The Ethereum Research sharded-PIR proposal argues that one monolithic PIR engine is probably the wrong shape.

The proposed architecture:

1. Split Ethereum data into slices by update profile and access pattern.
2. Pair each slice with a PIR scheme suited to that slice.
3. Send decoy queries to all slices in parallel when making a real query to one slice.
4. Use a universal middleware interface so wallets and dapps do not need to know which PIR scheme backs each slice.

This is important because wallets leak enormous metadata to RPC providers: addresses, token holdings, dapp usage, contract interactions, historical portfolio reconstruction, and trading intent. PIR can hide **what** data is read, while [Overview - Mix Networks](/kb/mix-networks/) or proxying is still needed to hide **who** is reading.

## Deployment checklist for 2025-era PIR

1. **Model the database as users see it.** Numeric array, key-value table, sharded state, append-only log, or popularity-skewed catalog?
2. **Choose the privacy model.** Single-server computational privacy, two-server non-collusion, or TEE-assisted privacy?
3. **Define correctness requirements.** Is best-effort retrieval acceptable, or must every rare record succeed?
4. **Separate online and offline costs.** Offline hints may be fine for weekly epochs and impossible for per-block updates.
5. **Pad record sizes and failure behavior.** Response sizes and retry patterns can leak even when the PIR query is cryptographically private.
6. **Authenticate the database epoch.** Use Merkle roots, signatures, commitments, or CT-style logs so a malicious server cannot equivocate.
7. **Protect network metadata.** PIR hides the index, not the IP address or timing. Compose with [Overview - Mix Networks](/kb/mix-networks/), Tor, OHTTP, or relay networks when needed.
8. **Benchmark memory traffic.** Many practical schemes are memory-bandwidth-bound; CPU crypto is not always the bottleneck.
9. **Avoid vague "PIR support" claims.** Name the scheme, record size, DB size, update cadence, setup cost, query size, response size, and adversary model.
10. **Consider GPU acceleration for high-throughput deployments.** GPIR (ICS 2026) demonstrates that GPU-based PIR can substantially outperform CPU-bound baselines for server-side throughput.

## 7. GPU-accelerated PIR: GPIR

**Source:** Ji, Yu et al., *GPIR: Enabling Practical Private Information Retrieval with GPUs*, arXiv:2604.04696, accepted at IEEE ICS 2026.

Single-server CPIR has traditionally been CPU-bound: the bottleneck is homomorphic computation and memory traffic, not network. GPIR (ICS 2026) breaks from this by co-designing PIR for GPU execution, rethinking kernel structure, data layout, and execution scheduling from scratch.

The core observation is that CPU PIR implementations leave GPU-style parallelism untapped. GPIR restructures the query evaluation to expose fine-grained parallelism across database rows and ciphertext slots, using GPU tensor cores for the dominant matrix-vector operations in LWE-based PIR.

Key claims from the paper:
- Substantially higher throughput than CPU baselines in the same database / scheme setting.
- First major GPU-specific PIR systems paper — prior work occasionally used GPUs for FHE bootstrapping but not as the primary PIR execution engine.
- Accepted at IEEE International Conference on Computer Systems (ICS) 2026.

For deployment planning: GPU-accelerated PIR is promising for operator-side throughput but requires the server to have GPU hardware. This maps well to the Akash / Render / io.net GPU provider model: a GPU-accelerated PIR service could sit in front of a public database and offer privacy-preserving queries as a service. The client-side does not need a GPU.

## 8. Incremental single-server PIR: iSimplePIR

**Source:** Shriram, Arunachalaramanan, Ren, *Incremental Single-Server Private Information Retrieval*, ePrint 2026/030.

Stateful PIR schemes like SimplePIR and DoublePIR amortize preprocessing across many queries by deriving a client-specific *hint* from the full database. The catch: any database update invalidates the hint and requires a full reprocessing pass.

iSimplePIR (ePrint 2026/030) is the first paper to formally define single-server incremental PIR. The goal is to update the hint efficiently when individual entries change, rather than recomputing it from scratch. The construction is built on SimplePIR and offers:

- **Entry-level iSimplePIR:** handles individual row insertions, modifications, and deletions with cost proportional to the change, not the full database.
- **Row aggregation mechanism:** for scenarios with predictable update cycles, aggregates multiple changes to reduce communication.
- **Compatibility:** the paper shows iSimplePIR is compatible with DoublePIR, YPIR, Authenticated PIR, and VeriSimplePIR — the incremental update mechanism does not require switching schemes.
- **Concrete numbers:** for a 1% column-major update in a 1 GB database, entry-level iSimplePIR achieves **224× reduction in preprocessing computation overhead** and **4.2× reduction in both communication and monetary costs** versus the prior row-level approach.
- **Password breach detection use case:** for random entry updates (completely random, not skewed), reduces preprocessing time by 86×.

This is a significant practical advance because real-world databases change constantly: blocklists update, certificate transparency logs grow, Nostr event indexes append, Ethereum state mutates. Incremental PIR makes stateful PIR viable for these settings without paying a full-reprocess tax on every update.

## 9. Fast stateful PIR: HarmonyPIR and BALANCED-PIR

**Source (HarmonyPIR):** Wang & Ren, *Efficient Single-Server Stateful PIR Using Format-Preserving Encryption*, ePrint 2026/437.

**Source (BALANCED-PIR):** Wang & Ren, *Single-server Stateful PIR with Verifiability and Balanced Efficiency*, ePrint 2025/1055.

Two simultaneous 2026 papers from the same MIT group attack stateful PIR from complementary angles.

### HarmonyPIR (ePrint 2026/437)

HarmonyPIR introduces a new hint organization using a **single random permutation** — instantiated via either AES or FF1 Format-Preserving Encryption. The key innovation is replacing the multiple-permutation structure of prior schemes with one cheap-to-evaluate permutation, which reduces the hint access pattern complexity and enables better batched execution.

Results: up to **two orders of magnitude better amortized computation** and up to **five times better amortized communication** than the previous state-of-the-art.

### BALANCED-PIR (ePrint 2025/1055)

BALANCED-PIR addresses a different tension in stateful PIR design: the tradeoff between client storage and server computation. Prior schemes either forced large client storage to keep server costs low, or forced the client to do heavy recomputation to keep server costs bounded.

BALANCED-PIR balances these. The Verifiable BALANCED-PIR variant adds commitments so clients can detect equivocation or wrong answers, with modest added costs:

| Metric | Improvement vs prior verifiable stateful PIR |
|---|---|
| Client storage | **100× smaller** |
| Amortized computation | **15× less** |
| Amortized communication | **2.5× better** |

The combination of HarmonyPIR (communication/compute efficiency) and BALANCED-PIR (client-storage efficiency) suggests the stateful PIR design space is maturing rapidly — the gap between research schemes and deployable infrastructure is narrowing.

## 10. New 2026 PIR research: DEPIR practical, non-cooperative PIR, improved TensorPIR, secret-key PIR

Four new ePrint papers appeared in 2026 with distinct contributions:

### Doubly-Efficient PIR becomes practical — ePrint 2026/243

Doubly-efficient PIR (DEPIR) is the holy grail: sublinear per-query work for both client and server with no client state. The problem is concrete: the best prior Eurocrypt 2025 construction required 733 TB of server state and over 2^37 online RAM/disk reads for N=2^23, making it infeasible.

The 2026 paper advances DEPIR toward practicality through a series of algorithmic innovations. For the same database size (N=2^23):

- Server state reduced from **733 TB to 171 GB** (4 orders of magnitude)
- Query time reduced by **6 orders of magnitude**
- Batch querying 5,461 elements: **112s total**, **21ms amortized per query**

This is not yet a drop-in production system — 171 GB is still substantial, and the system targets batch retrieval. But the direction is important: DEPIR, long considered theoretical, is entering the realm of concrete engineering.

**Freedom-tech relevance:** If server state and query time can be reduced this dramatically, DEPIR becomes plausible for privacy-preserving DNS, certificate transparency, and blockchain state retrieval without client-side preprocessing.

### Non-cooperative PIR: Zeal — ePrint 2026/684

All standard PIR schemes assume the database operator cooperates: running special software, performing homomorphic evaluation, or at minimum not interfering with the protocol. This is a fundamental deployment barrier. Zeal removes this assumption.

Zeal is the first **non-cooperative PIR scheme**: it works against an arbitrary public database with no cooperation required from the database operator. The security model assumes a strong adversary controlling not only the database but any third parties in the system.

Key properties:
- **No database cooperation needed:** works against unmodified public databases
- **Differential privacy security proof:** concrete privacy bounds
- **Performance:** ~3–4 minutes latency for 1M records, a **50× improvement** over a naive baseline solution
- **Implemented on AWS:** concrete implementation, not just theoretical

This is a new PIR model. The latency is high for interactive use, but for background private queries — checking a revocation list, fetching a blocklist, looking up a public key — it is within acceptable bounds for non-real-time applications.

**Freedom-tech relevance:** Zeal opens PIR to any public database, without requiring operators to adopt privacy technology. This is a significant deployment unlock. A privacy tool could privately query GitHub, npm, PyPI, or any public dataset without operator consent or participation.

### Improved TensorPIR — ePrint 2026/912

TensorPIR (CRYPTO 2024, Li et al.) lowered asymptotic communication complexity from O(N^1/2) (HintlessPIR) to O(N^1/3), but required larger parameters and more CRT moduli, so practical communication was not significantly smaller than HintlessPIR.

The 2026 improved TensorPIR rethinks the **encryption strategy for the index** and uses fewer CRT moduli. Results across 16 GB, 32 GB, 64 GB, and 128 GB databases:

- **Total communication drops to 45.5% of original TensorPIR**
- Query size reduced to **36.9% of TensorPIR** for large N
- Answer size reduced to **22.2% of TensorPIR** for large N
- Online time reduced to **28.9%–56.1% of HintlessPIR** depending on database size

The key insight is that index encryption was being done inefficiently in the original TensorPIR framework. Rethinking this yields substantial practical gains without changing the asymptotic complexity.

**Freedom-tech relevance:** Better communication efficiency directly benefits bandwidth-constrained clients — mobile wallets, mesh nodes, browsers making many PIR queries. This brings TensorPIR-family schemes closer to practical deployment.

### Secret-Key PIR from one-way functions — ePrint 2026/865

This paper constructs PIR from generic one-way functions, providing an alternative to lattice-based approaches. The model: in an offline phase, the client processes the database using a short secret key, then online queries are stateless for the server.

This is primarily a theoretical result — it demonstrates that lattice hardness assumptions are not necessary for PIR. The construction is of interest for:
- **Foundational understanding:** PIR is weaker than OT, and this work clarifies the exact cryptographic assumptions needed
- **Post-quantum alternative:** if lattice assumptions are broken, this provides a fallback path
- **Theoretical classification:** the relation between PIR, OT, and one-way functions

Practical deployment relevance is currently low, but the result matters for the long-term cryptanalytic landscape.

## 11. Ethereum Privacy Roadmap Integration — Helios, Kohaku, and the PIR Gap

The April 2026 Vitalik Buterin privacy roadmap identifies private state reads as the missing infrastructure piece. Private transactions on Ethereum pass through the public mempool where block builders see them; the roadmap proposes FOCIL to fix that. But the other direction — private *reads* of Ethereum state — hasn't been addressed at the protocol level and is the domain where PIR applies.

### The privacy gap at the RPC layer

When a wallet queries a balance, nonce, storage slot, or token position through a standard RPC provider, the provider learns which account and which data is being accessed. This metadata leak is independent of whether the transaction itself is private. Even with privacy pools and FOCIL, the reads still leak.

The solution stack:

1. **Helios** (a16z crypto): trustless light client. Converts untrusted RPC data into verified local data. No trusting the provider.
2. **PIR over Ethereum state**: the PIR server holds the state database; the client queries it without revealing which record. Even the PIR server doesn't learn which state item was queried.
3. **Privacy-service abstraction** (Kohaku first-phase deliverable): the reference wallet (Ambire fork) exposes private reads as a service layer, hiding the complexity of the Helios + PIR composition.

This is not hypothetical: Helios is production software. PSE (Privacy and Scaling Explorations team) has an active project for "Private Information Retrieval for Ethereum Data." The sharded-PIR architecture for Ethereum state (EthResearch) proposes pairing data slices with optimal PIR schemes, sending decoy queries to all slices in parallel to preserve privacy. The composition of these pieces — Helios for verification, PIR for data confidentiality, privacy pools for transaction privacy — gives a full-stack answer to Vitalik's roadmap.

### Kohaku reference wallet

The Ethereum Foundation's Kohaku roadmap explicitly includes privacy-service abstraction as first-phase deliverable. The reference implementation is a fork of Ambire wallet, designed to demonstrate privacy-by-default and verified-RPC-by-default in practice. This is a consumer-facing product target, not a research prototype.

Why it matters: the Ethereum privacy roadmap positions PIR as the infrastructure layer for mainstream wallet privacy. This is the clearest real-world deployment path for PIR technology — hundreds of thousands of Ethereum users eventually routing state reads through PIR-protected channels.

## June 2026 Developments

### PIR-PIXR/CPIR — Committed PIR Implementation

A GitHub implementation appeared at [github.com/PIR-PIXR/CPIR](https://github.com/PIR-PIXR/CPIR) implementing Committed Private Information Retrieval variants. The core primitive: the PIR server commits to its database state (via a commitment) so clients can detect equivocation — the server returning different answers for the same query — or wrong answers chosen opportunistically.

This fills the gap noted in Section 5: standard CPIR protects the client's query but not the server's answer. A malicious or broken server can return wrong encrypted data and the client cannot detect it without a commitment. Committed PIR matters for:
- **Paid databases**: where the server has financial incentive to cheat.
- **Signed transparency logs**: where the CT log operator might selectively lie about entries.
- **Any production deployment**: where a buggy or adversarial PIR server could return stale, corrupted, or targeted wrong answers with no detection.

Implementation results confirm that schemes with extra client protection increase practical time on both servers and clients — a concrete performance/correctness tradeoff that deployments must account for.

### SPIR via Rényi Divergence (ePrint 2026/1051)

*"Streamlined Symmetric Private Information Retrieval via Rényi Divergence"* (ePrint 2026/1051) achieves a first: a single-server SPIR derived directly from standard LWE PIR using Rényi divergence arguments for the database-privacy noise flooding, replacing the statistical distance analysis that yields impractical parameters in prior approaches.

Key results:
- Post-quantum, round-optimal SPIR.
- Online communication: 8 MB for 1 million records × 1 kB elements.
- Server computation: 302 ms for same workload.
- Concrete parameters using 64-bit ciphertext modulus.

**Important deployment note from the paper**: practical LWE-PIR schemes that use client-downloaded offline hints (SimplePIR, DoublePIR, YPIR) require additional protections for the database, because the hint itself can encode information about the database contents. This is a structural issue for any hint-based deployment: the offline hint is not just client state, it can leak server data. SPIR without multi-server assumptions has to address this.

Why it matters: this is the most concrete single-server SPIR result to date. The 8 MB communication is still large for mobile consumers, but the server-side compute (302 ms) suggests GPU-accelerated PIR servers could handle this in production. The hint-leakage note is important for any deployment considering preprocessing.

### PIR Tutorial and Survey (ePrint 2026/1135)

A comprehensive tutorial-and-survey paper appeared at ePrint 2026/1135 covering all major PIR paradigms — information-theoretic, computational, preprocessing, hintless, keyword, and batch — with concrete efficiency characterization, deployment guidance, and application survey. CC BY licensed.

This is the best onboarding resource for teams evaluating PIR for the first time. It is more applied than a pure research survey and more pedagogical than the original papers. Useful for: security teams evaluating PIR for a product, developers choosing a PIR scheme for a specific database shape, and researchers getting a systematic efficiency map of the field.

## Late-June 2026 Developments

### RAGtime-PIANO — FHE + PIR for Fully Secure Remote RAG (ePrint 2026/231)

A first-of-its-kind secure RAG protocol appeared at ePrint 2026/231, combining **FHE (CKKS)** with **PIR (PIANO)** through a novel two-stage IVF-Flat clustering approach:

- **Stage 1**: FHE-encrypted query embedding sent to server; server performs k-means centroid scoring and returns top-N clusters via FHE — query embedding never exposed to server.
- **Stage 2**: PIR queries privately retrieve centroid-associated embeddings and top-ranked documents — document indices never exposed.
- **Result**: End-to-end security where neither query, distances, nor retrieval information is known to the database server.
- **Performance**: Up to **323× lower communication costs** and **40× lower latency** versus prior work, with superior accuracy on FEVER and Natural Questions datasets.
- **Python implementation** using CKKS (FHE) and PIANO (PIR) — benchmarks confirm practical latency for real-world RaaS deployments.

This is the first fully secure RAG protocol achieving all four properties simultaneously: no embedding DB download, no DB modification, complete security, and quantum-secure retrieval. Links to [Confidential-AI-Inference](/kb/confidential-ai-inference/) and [Private-LLM-Inference-Patterns](/kb/private-llm-inference-patterns/) directly.

Sources: [ePrint 2026/231](https://eprint.iacr.org/2026/231), [IACR News Feb 2026](https://iacr.org/news/item/27672), [modification repo](https://github.com/nd-dsp-lab/Piano-PIR-RAG-MODIFIED)

### PIR-DSN: PIR for Decentralized Storage Networks (INFOCOM 2026)

PIR-DSN ([INFOCOM 2026](https://arxiv.org/abs/2512.07189), SDU Blockchain and Distributed Security Lab) is the first DSN protocol to integrate PIR for both single and multi-server settings, protecting user privacy during retrieval from decentralized storage.

- **Built on Filecoin/Lotus**: Uses lotus-miner, lotus-gateway, and lotus-wallet as building blocks.
- **PIR backends**: Includes both SealPIR and BRPIR (distributed PIR) implementations.
- **Multi-node testnet support**: Genesis node + worker node architecture with scripted deployment.
- **Privacy guarantee**: Other nodes in the network cannot infer which specific data is being fetched.
- **Go-based**: Full implementation at [github.com/BDS-SDU/PIR-DSN](https://github.com/BDS-SDU/PIR-DSN).

For [Overview - Decentralized Storage](/kb/decentralized-storage/) integrations (IPFS/Filecoin/Arweave/Sia/Storj), PIR-DSN shows the concrete path: attach a PIR layer to a DSN's retrieval protocol for private fetching over decentralized storage.

Sources: [GitHub BDS-SDU/PIR-DSN](https://github.com/BDS-SDU/PIR-DSN), [arXiv](https://arxiv.org/abs/2512.07189)

### PIANO Implementation Updates — wuwuz/Piano-PIR-new

PIANO (*Extremely Simple, Single-server PIR with Sublinear Server Computation*, IEEE S&P 2024) received a notable implementation update. The original repository archived in favor of [wuwuz/Piano-PIR-new](https://github.com/wuwuz/Piano-PIR-new):

- Implements the **updated version** of PIANO as described in the main paper body.
- Contains both original version (`client/client.go`) and new version (`tutorial_new/tutorial_new.go`).
- Clean **tutorial implementation**: `go run tutorial_new/tutorial_new.go` (client) + `go run server/server.go -port 50051` (server).
- PIANO's key property: **sublinear server computation** — server does not need to read every database element.

PIANO is used as the PIR backend in RAGtime-PIANO, demonstrating its suitability for practical privacy-preserving AI workloads.

Source: [github.com/wuwuz/Piano-PIR-new](https://github.com/wuwuz/Piano-PIR-new)

### Vitalik June 14, 2026 — Ethereum Privacy Blitz: ORAM and PIR for Wallet Privacy

Vitalik Buterin published a major post on June 14, 2026 declaring 2026 "the year that we take back lost ground in terms of self-sovereignty and trustlessness" and explicitly calling out **ORAM and PIR** as the primitives for hiding wallet queries from RPC providers:

> *"Helios: actually verify the data you're receiving from RPCs instead of blindly trusting it. ORAM, PIR: ask for data from RPCs without revealing what."*

The concrete privacy stack for Ethereum wallet reads:
1. **Helios** (a16z crypto): trustless light client — verifies RPC data without trusting the provider.
2. **PIR**: hides which state record is being fetched from the PIR server.
3. **ORAM**: prevents access pattern analysis when the RPC provider is the same as the data provider.
4. **Kohaku** (Ethereum Foundation): privacy-service abstraction as first-phase deliverable.

This is the clearest real-world deployment signal PIR has ever received from a protocol founder. Ethereum's privacy roadmap treats PIR not as an academic curiosity but as **infrastructure** for mainstream wallet privacy.

Sources: [Vitalik X June 14 2026](https://x.com/VitalikButerin/status/2012231445809435134), [The Block June 14 2026](https://www.theblock.co/post/386043/vitalik-buterin-declares-2026-the-year-ethereum-reverses-backsliding-of-self-sovereignty-and-trustlessness)

### IACR News June 4, 2026 — PIR Tutorial and Survey Published

*"Private Information Retrieval: A Tutorial and Survey"* (ePrint 2026/1135) by Shriram, Arunachalaramanan, Chen, and Ren was highlighted in the IACR June 4, 2026 news item. The paper is accessible to readers without prior PIR knowledge, covering:

- Information-theoretic and computational PIR.
- Single-server and multi-server non-colluding settings.
- PIR with and without preprocessing.
- Keyword queries and batch queries.
- Concrete efficiency characterization and deployment guidance.
- Practical applications survey.

This serves as the canonical onboarding reference for teams evaluating PIR for the first time.

Sources: [IACR News June 4 2026](https://www.iacr.org/news/item/28679), [ePrint 2026/1135](https://eprint.iacr.org/2026/1135)

### PSE Ethereum Privacy PIR — Active Project

The Privacy and Scaling Explorations (PSE) team has an active project page for "Private Information Retrieval for Ethereum Data" at [pse.dev/projects/pir-ethereum-data](https://pse.dev/projects/pir-ethereum-data). This is the Ethereum Foundation-backed effort to turn PIR from research into wallet infrastructure — the implementation arm of Vitalik's June 2026 privacy roadmap call.

Source: [pse.dev](https://pse.dev/projects/pir-ethereum-data)

## Primary sources

- Lehmkuhl, Henzinger, Corrigan-Gibbs, *Distributional Private Information Retrieval* — https://eprint.iacr.org/2025/132
- USENIX materials page for Distributional PIR — https://people.eecs.berkeley.edu/~henrycg/pubs/distpir/
- *Pirouette: Query Efficient Single-Server PIR* — https://eprint.iacr.org/2025/680
- *Private Information Retrieval based on Homomorphic Encryption, Revisited* — https://eprint.iacr.org/2025/729
- Henzinger & Ragavan, *Two-Server Private Information Retrieval in Sublinear Time and Quasilinear Space* — https://eprint.iacr.org/2025/2008
- finite-diffs-pir reference implementation — https://github.com/ahenzinger/finite-diffs-pir
- *VIA: Communication-Efficient Single-Server Private Information Retrieval* — https://eprint.iacr.org/2025/2074
- ChalametPIR — https://github.com/itzmeanjan/ChalametPIR
- Ethereum Research, *Sharded PIR Design for the Ethereum State* — https://ethresear.ch/t/sharded-pir-design-for-the-ethereum-state/24552
- Ji, Yu et al., *GPIR: Enabling Practical Private Information Retrieval with GPUs* — https://arxiv.org/abs/2604.04696
- Shriram, Arunachalaramanan, Ren, *Incremental Single-Server Private Information Retrieval* — https://eprint.iacr.org/2026/030
- Wang & Ren, *BALANCED-PIR: Single-Server Stateful PIR with Verifiability and Balanced Efficiency* — https://eprint.iacr.org/2025/1055
- Wang & Ren, *HarmonyPIR: Efficient Single-Server Stateful PIR Using Format-Preserving Encryption* — https://eprint.iacr.org/2026/437
- *Towards Making Doubly-Efficient PIR Practical* — https://eprint.iacr.org/2026/243
- *Improved TensorPIR: Single-Server PIR with Lower Communication Cost* — https://eprint.iacr.org/2026/912
- *Zeal: PIR for Non-Cooperative Databases* — https://eprint.iacr.org/2026/684
- *Secret-Key PIR from One-Way Functions* — https://eprint.iacr.org/2026/865
- *Streamlined Symmetric PIR via Rényi Divergence* — https://eprint.iacr.org/2026/1051
- *Private Information Retrieval: A Tutorial and Survey* — https://eprint.iacr.org/2026/1135
- PIR-PIXR/CPIR Committed PIR — https://github.com/PIR-PIXR/CPIR
- RAGtime-PIANO (FHE+PIR RAG) — https://eprint.iacr.org/2026/231
- PIANO updated implementation — https://github.com/wuwuz/Piano-PIR-new
- PIANO RAG modification — https://github.com/nd-dsp-lab/Piano-PIR-RAG-MODIFIED
- PIR-DSN (INFOCOM 2026) — https://github.com/BDS-SDU/PIR-DSN
- Helios — https://github.com/a16z/helios
- Helios blog — https://a16zcrypto.com/posts/article/building-helios-ethereum-light-client
- Vitalik June 14 2026 X post — https://x.com/VitalikButerin/status/2012231445809435134
- PSE Ethereum Privacy PIR — https://pse.dev/projects/pir-ethereum-data
- IACR News June 4 2026 — https://www.iacr.org/news/item/28679
- Kohaku roadmap (Ethereum Foundation) — referenced via Ethereum privacy roadmap discussions
