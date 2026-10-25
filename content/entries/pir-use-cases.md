---
title: "PIR Use Cases and Deployments"
slug: pir-use-cases
type: explainer
pillars: ["cryptography"]
description: "Where private information retrieval is used, tested or planned: private contact discovery, password checks, certificate transparency and more."
dek: "Where private information retrieval is actually being used, tested, or planned for production. From Certificate Transparency auditing to Ethereum privacy to Apple device features."
updated: 2026-10-25
created: 2026-08-05
origin: vault
source: "13-Private-Information-Retrieval/PIR Use Cases and Deployments.md"
aliases: ["PIR Use Cases", "PIR Deployments"]
tags: ["pir", "use-cases", "deployments", "certificate-transparency", "ethereum", "kohaku", "private-search", "apple", "password-breach", "blockchain", "contact-discovery"]
---

## 1. Certificate Transparency (CT) Log Auditing

### The Problem

Certificate Transparency logs record every TLS certificate issued by a CA. Monitoring these logs is essential for detecting misissued certificates. But monitoring also means querying the log for specific domains — which reveals exactly which domains an auditor is watching. A surveillance adversary who observes the queries learns what domains security teams consider sensitive.

### PIR Solution

PIR enables querying CT logs without revealing which entries are being checked. The auditor retrieves entries by index/position, and the log server cannot determine which certificate is being audited.

### Key Work

- **YPIR** (USENIX Security 2024): Specifically demonstrates **48× cost reduction** for private CT log auditing compared to prior schemes. This makes private CT auditing economically viable for the first time. At AWS compute rates, the prior scheme would cost 48× more than YPIR.
- **SimplePIR/DoublePIR** (USENIX Security 2023): The original paper demonstrates CT log auditing as a primary application. The hint-based approach works well for CT logs because they are append-only Merkle trees.
- **Respire** (CCS 2024): Optimized for small records (~256 bytes), which matches the size of CT log entries (certificate fingerprints, timestamps).

### Deployment Status

CT log auditing with PIR is at the **research-to-pilot** stage. The cost reductions from YPIR make it practical, but no public deployment is confirmed. The CT ecosystem (Google, Cloudflare, Apple, DigiCert) is the natural operator, as they already run CT logs and have the infrastructure for non-colluding server setups.

### Relevance to Freedom Tech

Private CT auditing protects organizations that monitor for certificate abuse targeting their infrastructure. Without PIR, an adversary who controls or observes the CT log can learn which domains a privacy-focused organization is protecting, potentially preempting defensive actions.

## 2. Ethereum Privacy — Private RPC Reads

### The Problem

When an Ethereum user checks their balance, simulates a transaction, or queries contract state via an RPC provider (Infura, Alchemy, etc.), the provider learns exactly which addresses and contracts the user is interacting with. This enables:

- **Identity correlation**: Linking on-chain addresses to off-chain identities (IP address, API key).
- **MEV extraction**: Frontrunning transactions based on observed query patterns.
- **Surveillance**: Monitoring which dApps, tokens, or contracts a user is interested in.

Even if transactions themselves are private (via privacy pools, ZK proofs, etc.), the **read path** remains fully observable. This is analogous to making a private phone call where the telecom knows who you called and when.

### Key Developments

#### Kohaku Privacy Toolkit (2025–2026)
Kohaku is an open-source Ethereum privacy toolkit developed by the Ethereum Foundation's Privacy Cluster (announced October 2025, 47-member team). It consists of:
- **Kohaku SDK**: Modular plugin system for wallet developers
- **Kohaku Reference Wallet**: Browser extension forked from Ambire, targeted at power users

Referenced in Vitalik Buterin's May 2026 privacy roadmap alongside FOCIL (Fork-Choice Inclusion Lists), privacy pools, and account abstraction.

**Private State Reading Architecture** (confirmed August 2026):
- Kohaku embeds a minimal execution client in the browser for private `eth_call`
- **Phase 1 (current)**: Uses an oblivious server combining TEE + ORAM (Oblivious Labs, EF-funded Q1 2026)
- **Long-term**: Replace with purely cryptographic PIR
- Privacy-service abstraction is a Phase 1 deliverable

**EF Q1 2026 Allocation** confirms funded grant: "Builds an Oblivious server to handle requests from the Kohaku extension's embedded execution client, enabling private state reading." — First concrete pipeline from PIR/ORAM research to wallet deployment.

#### Kohaku SDK Shipping (May–August 2026)
The SDK moved from announcement to shipping alpha artifacts (GitHub-verified Aug 19 2026):

| Component | Latest alpha | Released |
|-----------|--------------|----------|
| `@kohaku-eth/railgun` | 0.0.1-alpha.30 | Aug 21 2026 |
| `@kohaku-eth/tornado-cash` | 0.0.2-alpha.21 | Aug 21 2026 |
| `@kohaku-eth/privacy-pools` | 0.0.2-alpha.16 | Aug 21 2026 |
| `@kohaku-eth/plugins` | 0.0.1-alpha.13 | Aug 21 2026 |
| `@kohaku-eth/provider` | 0.1.0-alpha.9 | Aug 21 2026 (NEW — wallet↫network abstraction; 0.1.0 major.minor ahead of plugins) |
| `@kohaku-eth/pq-account` | listed | Post-quantum ERC-4337 account implementation |

- Repo: https://github.com/ethereum/kohaku — 399 stars, created Aug 1 2025, active weekly releases.
- **Railgun integration has operational ERC-4337 mempool relaying** — private transactions route through the 4337 mempool instead of protocol-specific relayers, removing a centralized-relayer dependency (The Defiant). SDK announced May 25 2026; Ambire integrating in production; breadcoop collaboration on an experimental browser-extension wallet; CLI reference wallet from `kassandraoftroy/kohaku-cli`.
- **Scope**: shielded-pool writes (Railgun, Tornado Cash, Privacy Pools) plus post-quantum accounts, multisig, hardware-wallet support. Berlin Blockchain Week showcase planned.
- **The private-*reads* (PIR) side is NOT yet in the SDK** — it remains the Phase-1-then-endgame architecture above. The Kohaku testnet roadmap (`ethereum/wallet-poc`) schedules "v1: Abstraction Core with Privacy by Design" across January–August 2026, making H2 2026 the watch window for the first PIR-backed wallet feature.

#### Sharded PIR Design for Ethereum State
Ali Atiia and Keewoo Lee published a comprehensive design for sharding Ethereum state across multiple PIR schemes on ethresear.ch (2025). Key proposals:

- **Data sharding**: Split Ethereum state into slices (hot state, receipts, blocks, transactions, archival) and pair each with the optimal PIR scheme for its characteristics.
- **Decoy queries**: Users query the PIR engine of interest **but simultaneously submit decoy queries to all other engines**. This is privacy-equivalent to querying one monolithic PIR engine for all Ethereum data.
- **Scheme selection decision tree**: Different PIR schemes are optimal for different data types (e.g., SimplePIR for static archival data, FrodoPIR for mutable hot state).

The design also references **RisePIR**, a keyword-PIR variant optimized for key-value stores (based on Segmented Cuckoo Filters), which maps directly to the `(address → balance)` lookup pattern for private `eth_getBalance` calls.

#### PSE PIR for Ethereum Data
The Privacy & Scaling Explorations (PSE) team at the Ethereum Foundation has an active project: "PIR for Ethereum Data." Published a blog post on June 18 2025 at pse.dev/blog/ethereum-privacy-pir. **August 2026 update**: PSE rebranded to **"Privacy Stewards of Ethereum"** with a mandate to "methodically study ORAM and PIR state-of-the-art techniques while translating research into practical wallet and browser experiences." The old `privacy-scaling-explorations/pir-ethereum-data` GitHub repo no longer resolves (404) — the effort now lives under pse.dev project pages. ethereum.org's official privacy roadmap page (updated Jul 27 2026) states "PIR research is progressing with active implementations being tested by infrastructure teams," positioning PIR at the access layer between wallet software and node providers. Separately, the EF's Institutional Privacy Task Force spun out as **EthSystems** (for-profit, July 2026) to build institutional privacy infrastructure — adding demand-side pull for PIR/ORAM serving.

#### TEE+ORAM Alternative
Flashbots and others have explored TEE+ORAM (Trusted Execution Environment + Oblivious RAM) for private blockchain data access. This achieves obliviousness via hardware isolation and access-pattern hiding. TEE+ORAM is orders of magnitude faster than PIR in practice, but relies on trust in hardware (TEE integrity). PIR relies on cryptographic guarantees alone.

### Deployment Status

Ethereum private reads via PIR are at the **design and prototyping** stage. No production wallet currently uses PIR for RPC reads. However:
- The Kohaku SDK is shipping (alpha, Aug 2026) for private *writes*; the private-reads PIR/ORAM phase is scheduled in the Jan–Aug 2026 "Abstraction Core" window.
- The sharded PIR design provides a concrete architecture.
- RisePIR demonstrates that key-value PIR can handle the `(address → balance)` workload at useful throughput (1,500–24,000 ops/s for 32-byte values on a single-threaded, no-SIMD prototype).
- Vitalik's explicit endorsement makes this the **highest-signal deployment target** for PIR in the freedom-tech space.

### Relevance to Freedom Tech

Private RPC reads are a prerequisite for a fully private Ethereum experience. Without them, even users of privacy-preserving transaction layers (Aztec, private pools) leak their interests and activity patterns to RPC providers. This is the most direct path to PIR deployment in a censorship-resistant stack.

## 3. Private Web Search — Tiptoe

### The Problem

Search engines (Google, Bing, DuckDuckGo) see every query you make. Even "privacy-focused" engines like DuckDuckGo still receive plaintext queries — they simply promise not to track them. True privacy requires the search provider to **not know what you're searching for**.

### PIR Solution — Tiptoe (SOSP 2023)

Tiptoe is a system for fully private web search built by Alexandra Henzinger et al. (MIT, Google). It was published at SOSP 2023 and demonstrates that private web search is architecturally feasible.

**Architecture**:
- Two non-colluding servers: a **ranking service** and a **URL service**.
- Documents are pre-processed: embedded into vectors, clustered, and organized into cryptographic data structures.
- The client encrypts its query using Regev encryption (LWE).
- The ranking service computes on encrypted data to find the relevant document cluster.
- The URL service retrieves the actual URLs without learning which cluster was selected.
- Client downloads ~57 MiB of state for query encoding.

**Key properties**:
- The search provider learns nothing about what the user searches for.
- Supports both keyword and semantic (embedding-based) search.
- Compatible with transformer embedding models.
- Query latency is practical on a cluster of tens of machines.

**Repo**: https://github.com/ahenzinger/tiptoe (56 stars)

**Funded by**: Capital One, Facebook, Google, Mozilla, NASDAQ, MIT FinTech@CSAIL, NSF.

### Deployment Status

Tiptoe is a **research prototype** that demonstrates feasibility. It is not deployed as a product. The non-collusion requirement (two independent server operators) is the main deployment barrier. Mozilla's involvement is notable as they could potentially operate one of the two servers.

### Relevance to Freedom Tech

Private search is one of the highest-impact privacy primitives. If search queries are truly hidden, the largest surveillance vector in everyday internet use is closed. Tiptoe's architecture (two non-colluding servers) maps naturally to organizations like Mozilla + Tor Project, or EFF + a university.

## 4. Apple Device Features

### Live Caller ID Lookup (iOS 18+)

Apple uses a combination of homomorphic encryption (HE) and PIR for features like:
- **Live Caller ID**: Looking up caller information without Apple learning who is calling you.
- **Logo lookup**: Retrieving business logos without revealing which business.
- **Content filtering**: Checking message/email content against blocklists without revealing the content.

The system uses a combination of HE for server-side computation on encrypted data and techniques related to PIR for retrieving specific records without revealing which ones.

### Deployment Status

**Production**. These features shipped in iOS 18 (2024) and are live on consumer devices. Apple's deployment is the largest-scale production use of HE+PIR techniques in consumer hardware.

### Relevance to Freedom Tech

Apple publishes the Swift Homomorphic Encryption library, including PIR, and a PIR service example. These repositories make the library and example backend available for inspection. The example supports Live Caller ID Lookup and URL filtering; its README explicitly says it should not be run in production. Public example code does not establish that every component of Apple’s deployed services is open source.

## 5. Password Breach Checking

### The Problem

Checking whether a password has appeared in a known breach requires sending the password (or a hash of it) to a breach database server. Even with k-anonymity (used by Google Password Checkup and HaveIBeenPwned), the server learns partial information about the password being checked.

### PIR Solution

PIR enables checking a password against a breach database without revealing which password is being checked. The server returns whether the queried entry exists in the breach DB without learning the query.

### Key Work

- **iSimplePIR** (ePrint 2026/030): Explicitly targets password breach detection as a primary use case. The incremental update feature is critical because breach databases are constantly updated with new entries. iSimplePIR's entry-level update support means new breached passwords can be added without re-processing the entire database.
- **Hintless PIR** (Google, CRYPTO 2024): The `private_inference` component of Google's hintless_pir repo suggests applications in private credential checking.
- **VeriSimplePIR**: Verifiability ensures the breach-checking server cannot lie about whether a password is in the breach DB.

### Deployment Status

**Research**. No production password-checking service is known to use PIR. Google Password Checkup uses k-anonymity (range queries), which is less private than PIR but more practical at current performance levels. iSimplePIR's incremental update support makes PIR-based breach checking more viable for frequently-updated breach databases.

## 6. Private Contact Discovery

### The Problem

When a messaging app (Signal, WhatsApp) checks which of your contacts are also on the service, it must send your contact list to the server. The server learns your entire social graph.

### PIR Solution

PIR enables checking whether each phone number / identifier is registered without revealing which numbers are being checked. The client queries by index, and the server cannot determine which contacts are being looked up.

### Key Work

- Signal has explored PIR-based contact discovery but has not deployed it. The primary challenge is the database size (billions of registered users) and the query volume (every new user checks their entire contact list).
- **Respire** (CCS 2024): Optimized for small records, which matches the contact-discovery workload (each record is a phone number hash + registration flag).
- **FrodoPIR**: Brave's experiments include contact-discovery-style workloads.

### Deployment Status

**Research**. Signal currently uses SGX-based trusted hardware for contact discovery (Signal SGX contact discovery service). This is faster than PIR but relies on Intel hardware trust. PIR would eliminate the hardware trust assumption entirely.

## 7. Private DNS Lookups

### The Problem

DNS resolvers see every domain a user queries. Even encrypted DNS (DoH, DoT) only encrypts the transport — the resolver still learns the domain name.

### PIR Solution

PIR can make DNS lookups private: the resolver serves DNS records without learning which domain was queried. This requires the DNS zone to be structured as a PIR-queriable database.

### Compositions

- PIR + [PKARR](/kb/pkarr/): PKARR records on the Mainline DHT are already self-authenticating. PIR could make the DHT lookup private.
- PIR + CT: Private CT auditing (described above) ensures domain monitoring privacy.
- PIR + Decentralized DNS: ENS, Handshake, or GNS records could be served via PIR, making resolution fully private.

### Deployment Status

**Research**. No production DNS resolver uses PIR. The database size (hundreds of millions of DNS records) and latency requirements (sub-100ms) are challenging for current PIR schemes. However, DNS-over-PIR is a natural composition that would close the last metadata leak in encrypted DNS.

## Use Case Maturity Matrix

| Use Case | Status | Key Scheme | Barrier |
|----------|--------|-----------|---------|
| CT Log Auditing | Research→Pilot | YPIR (48× cost reduction) | Operator adoption |
| Ethereum Private Reads | Design→Prototype | Sharded PIR, Kohaku, RisePIR | Performance at ETH state size |
| Private Web Search | Prototype | Tiptoe (two-server) | Non-collusion requirement |
| Apple Device Features | **Production** | HE+PIR; public Swift library and service example | Public code can be inspected; example backend is not for production |
| Password Breach Check | Research | iSimplePIR | Incremental update performance |
| Contact Discovery | Research | Respire, FrodoPIR | DB size (billions of entries) |
| Private DNS | Research | Various | Latency (<100ms) + DB size |

## Deployment Architecture Patterns

### Pattern 1: Single-Server PIR
- Client downloads hint → client queries → server computes on encrypted query → client decrypts.
- No non-collusion assumption needed.
- Requires LWE (or similar) hardness assumption.
- Best for: CT auditing, password breach checking, Apple device features.

### Pattern 2: Two Non-Colluding Servers
- Client queries both servers, neither learns the query alone.
- Information-theoretic security possible.
- Best for: Private web search (Tiptoe), high-security applications.
- Deployment barrier: Finding two independent operators.

### Pattern 3: Hardware-Assisted (TEE+ORAM)
- PIR computation runs inside a TEE (SGX, SEV-SNP, TDX).
- ORAM hides access patterns from the TEE host.
- Orders of magnitude faster than pure PIR.
- Best for: Contact discovery (Signal), latency-sensitive applications.
- Trade-off: Trust in hardware manufacturer.

### Pattern 4: Sharded PIR (Ethereum design)
- Database split into shards by data type.
- Each shard served by the optimal PIR scheme.
- User submits real query to one shard + decoy queries to all others.
- Best for: Complex, multi-type databases (Ethereum state).

## Primary sources

- [Apple Swift Homomorphic Encryption, including PIR](https://github.com/apple/swift-homomorphic-encryption)
- [Apple PIR Service Example and deployment limits](https://github.com/apple/pir-service-example)
