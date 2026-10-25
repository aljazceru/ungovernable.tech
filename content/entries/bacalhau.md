---
title: "Bacalhau and Compute-over-Data"
slug: bacalhau
type: deep-dive
pillars: ["compute"]
readiness: usable
description: "Bacalhau and compute-over-data: moving jobs to where data lives instead of moving data to the compute, and how it underpins decentralized networks."
dek: "Distributed compute orchestration for the data-gravity problem: instead of pulling terabytes out of S3, Filecoin, IPFS, edge boxes, or regional data stores, ship the job to the machine that already has the data and publish only the result."
updated: 2026-05-12
created: 2026-05-05
origin: vault
source: "04-Decentralized-Compute/Bacalhau and Compute-over-Data.md"
aliases: ["Bacalhau", "Compute-over-Data", "CoD", "Distributed Compute Orchestration"]
tags: ["bacalhau", "compute-over-data", "ipfs", "filecoin", "distributed-compute", "edge-computing", "duckdb", "deep-dive"]
---

## Summary

**Bacalhau** is an open-source distributed compute orchestration framework built around **Compute-over-Data (CoD)**. Its core claim is simple: large datasets are slow, expensive, and often legally awkward to move, so computation should be scheduled near the data rather than the other way around. In the [Overview - Decentralized Compute](/kb/decentralized-compute/) landscape, Bacalhau is not a token-first GPU marketplace like [Akash](/kb/akash/), [Render Network](/kb/render-network/), [io.net](/kb/io-net/), or [Aethir](/kb/aethir/). It is closer to an orchestration layer for *federated infrastructure*: one binary can act as client, orchestrator, or compute node; jobs can run as Docker containers or WebAssembly; inputs can come from S3, HTTP, local volumes, and IPFS CIDs; outputs can be published back to storage.

For ungovernable infrastructure, Bacalhau matters because it attacks a different bottleneck than most DePIN compute projects. The practical question is not always “where can I buy the cheapest GPU?” but “how do I process data that is already scattered across homes, edge devices, Filecoin/IPFS, observability pipelines, or jurisdictionally constrained regions without centralizing it first?” That makes Bacalhau a natural companion to [IPFS and Filecoin](/kb/ipfs-and-filecoin/), [Overview - Decentralized Storage](/kb/decentralized-storage/), [Private-LLM-Inference-Patterns](/kb/private-llm-inference-patterns/), [Confidential-AI-Inference](/kb/confidential-ai-inference/), and [MOC - Composing Primitives](/kb/map-composing-primitives/).

Current maturity is **active but infrastructure-layer**. The GitHub repository `bacalhau-project/bacalhau` is Apache-2.0, written in Go, not archived, with 858 stars / 100 forks and a fresh push on 2026-04-29 (GitHub API check, 2026-05-05). Documentation describes Bacalhau as a single-binary orchestrator with modular execution engines, storage integrations, multiple job types, declarative YAML job specs, and a data-centric scheduler. It is useful today for controlled distributed fleets and compute-over-data workflows; it is not yet a fully permissionless, cryptoeconomic, adversarial marketplace in the same sense as Akash or Golem.

## Historical context

### From distributed computing to data gravity

Classic volunteer computing — SETI@home, Folding@home, BOINC — proved that loosely coordinated machines can perform useful work. But those systems generally assume the dataset is small enough to broadcast or that work units can be prepackaged centrally. Modern data is different: observability logs, genomic datasets, sensor streams, model artifacts, blockchain archives, and media corpora can be many terabytes or petabytes. The bottleneck becomes **data movement**, not CPU cycles.

Cloud vendors solved this by co-locating data and compute inside one provider boundary: keep data in S3, run EMR / Athena / Lambda / Batch / SageMaker near it, pay egress if you leave. That works operationally but deepens lock-in and surveillance risk. Compute-over-data generalizes the useful part — run close to the data — without requiring a single hyperscaler trust domain.

### IPFS / Filecoin roots

Bacalhau emerged from the Filecoin/IPFS orbit. IPFS documentation frames CoD as processing near content-addressed data, especially where moving large volumes over networks is inefficient. The IPFS CoD page names Bacalhau and IPVM as the two relevant pieces: Bacalhau as a practical platform that runs Docker or WASM jobs where data is generated and stored, and IPVM/Homestar as a more capability-oriented specification/runtime for content-addressed compute.

This lineage matters because content addressing gives a stronger primitive than location addressing. A job can refer to an IPFS CID and know what bytes it is supposed to process, independent of which node supplies them. Bacalhau's IPFS input source lets a job mount a CID into the task environment via YAML or CLI, making CIDs feel like ordinary input directories.

### Shift from public Filecoin demos to enterprise/fleet orchestration

The current docs emphasize Bacalhau as a general distributed compute orchestration framework rather than only a Filecoin compute market. Expanso, Inc. produces commercial Bacalhau offerings from the open-source software, while the repository remains Apache-2.0 with trademark caveats. The product framing is now broader: process logs at the source, query regional datasets, manage distributed nodes, run ML workloads across a fleet, and support edge/low-connectivity environments.

That evolution is important for maturity analysis. Bacalhau's strongest near-term use case may be not “anonymous strangers run jobs over arbitrary decentralized data” but “an organization, DAO, research consortium, or sovereign cloud operator controls many heterogeneous locations and needs a common job plane.”

## Architecture

### Single binary, multiple roles

Bacalhau's architecture is built around a single self-contained binary that can serve multiple roles:

- **Client / CLI** — submits jobs imperatively (`bacalhau docker run ...`) or declaratively (`bacalhau job run <job-spec>`).
- **Orchestrator** — schedules work onto suitable compute nodes based on locality, availability, constraints, and job policy.
- **Compute node** — runs the actual task, fetches/mounts inputs, executes the container or WASM module, and publishes outputs.

This is operationally valuable because decentralized deployments tend to fail at packaging complexity. A one-binary design lowers the cost of running nodes in labs, homes, ships, field deployments, or small data centers.

### Execution engines

The docs and README emphasize modular execution:

| Engine | Role | Notes |
|---|---|---|
| Docker containers | General workload compatibility | Most existing batch jobs, data pipelines, ML scripts, and CLI tools can be containerized. |
| WebAssembly (WASM) | Sandboxed / portable execution | Better fit for deterministic, constrained, capability-style tasks; aligns with IPVM direction. |
| Custom engines | Extension point | The architecture exposes interfaces so new runtimes can be added without rewriting the scheduler. |

Docker gives immediate pragmatism. WASM points toward a more verifiable/capability-oriented future, especially when combined with content-addressed inputs and outputs.

### Input and output model

Bacalhau jobs can consume data from multiple sources:

- **IPFS** — mount an IPFS CID into the task environment, e.g. `ipfs://<CID>:/data`.
- **S3 / object storage** — practical for enterprise and regional data lakes.
- **HTTP/HTTPS** — simple remote fetches.
- **Local mounted data** — the most important edge/fleet pattern: data already on a node does not need to move.

Outputs can be written to local storage, object stores, or other publishers. The important pattern is that outputs should usually be **smaller than inputs**: summaries, aggregates, model checkpoints, indexes, Merkle roots, signatures, or reports.

### Job types

The GitHub README and docs list several job shapes:

| Job type | Fit |
|---|---|
| Batch | One-off analytics, transforms, rendering, ETL, scientific jobs. |
| Ops | Fleet operations and maintenance tasks run across nodes. |
| Daemon | Long-lived agents or local services. |
| Service | Network-facing workloads; less central than batch CoD but useful for edge services. |

Compared with [Akash](/kb/akash/), which exposes a Kubernetes-flavored deployment abstraction, Bacalhau feels closer to a distributed batch/fleet orchestrator optimized around data locality.

### Scheduling principle: locality first

The scheduler's conceptual job is to answer: *which node can run this job with the least unnecessary data movement?* Relevant constraints include:

- where the input data already exists;
- whether the node has required CPU/GPU/memory/runtime capabilities;
- whether the data can legally leave a region;
- whether a network partition is expected;
- whether outputs need to be published to a particular sink.

This is the central difference from raw compute markets. A GPU marketplace asks “who has an H100 at the best price?” Compute-over-data asks “who already has the data, and can they run this code safely enough?”

## Evidence at a glance

| Claim | Evidence | Maturity / caveat |
|---|---|---|
| Bacalhau is actively developed open-source infrastructure | `bacalhau-project/bacalhau`, Go, Apache-2.0, not archived, 858 stars / 100 forks, pushed 2026-04-29, updated 2026-05-01. | Active small-to-mid infrastructure project; not as visible as tokenized DePIN networks. |
| CoD reduces bandwidth and egress costs | Bacalhau docs claim log processing can reduce bandwidth usage up to 93%; IPFS docs explain CoD avoids moving large volumes. | Plausible and workload-dependent; verify with local benchmarks before production budgeting. |
| IPFS integration is first-class | Bacalhau IPFS input source mounts CIDs into tasks via YAML or CLI. | Useful for content-addressed pipelines; availability still depends on pinning / retrieval. |
| DuckDB integration supports distributed analytics | Bacalhau docs describe DuckDB partition UDFs, distributed query execution, and stateless SQL jobs. | Practical for partitionable datasets; not a replacement for a full distributed database. |
| Filecoin ecosystem recognizes Bacalhau | Filecoin Foundation ecosystem page describes Bacalhau as fast, cost-efficient computation for Filecoin data and says compute providers can participate even without hosting Filecoin data. | Ecosystem listing, not proof of large independent demand. |
| Security model is not inherently confidential | Docs emphasize private clusters and data locality, not TEE-by-default confidentiality. | For sensitive workloads, compose with [Confidential-Containers](/kb/confidential-containers/), [Confidential-AI-Inference](/kb/confidential-ai-inference/), or trusted internal nodes. |
| Strongest real-world fit is federated/fleet compute | Docs emphasize logs, multi-region queries, edge nodes, ML fleets, and low-connectivity environments. | Better near-term fit than anonymous adversarial open markets. |

## Major implementations and related projects

### Bacalhau

- **Website:** [bacalhau.org](https://bacalhau.org/)
- **Docs:** [bacalhau.org/docs](https://bacalhau.org/docs/)
- **GitHub:** [bacalhau-project/bacalhau](https://github.com/bacalhau-project/bacalhau)
- **License:** Apache-2.0 with trademark/logo caveats.
- **Language:** Go.
- **Status:** active, usable, infrastructure-layer.

Bacalhau is the implementation this note is about: a distributed compute orchestrator for running jobs near data. It is not primarily a blockchain; it can be used with decentralized storage and decentralized infrastructure, but the core abstraction is job orchestration.

### IPFS Compute-over-Data

- **Docs:** [Compute-over-Data with content-addressed data](https://docs.ipfs.tech/concepts/cod/)

IPFS provides the content-addressed data substrate. Bacalhau jobs can mount CIDs, run Docker/WASM tasks, and publish compact outputs. The key win is reproducibility: if a job says it processed CID `X`, the input bytes are cryptographically named.

### IPVM / Homestar

- **Homestar GitHub:** [ipvm-wg/homestar](https://github.com/ipvm-wg/homestar/)
- **IPVM spec:** [ipvm-wg/spec](https://github.com/ipvm-wg/spec)
- **Workflow spec:** [ipvm-wg/workflow](https://github.com/ipvm-wg/workflow)

IPVM is the more explicitly content-addressed, capability-oriented compute specification. IPFS docs describe it as an open, decentralized, local-first competitor to AWS Lambda using WASM, content addressing, SPKI, and object capabilities. Bacalhau is the practical orchestrator; IPVM/Homestar is the architectural direction for open-world compute.

### DuckDB + Bacalhau

- **Integration docs:** [Bacalhau DuckDB integration](https://bacalhau.org/integrations/duckdb/)

DuckDB is an in-process analytical database. Bacalhau extends it by partitioning datasets across nodes and running SQL jobs near storage. The docs list partitioning UDFs for hash, regex, and date-based splits, enabling workloads like distributed log analysis over Parquet.

### Filecoin integration

- **Filecoin ecosystem page:** [Bacalhau — Filecoin Foundation](https://fil.org/ecosystem-explorer/bacalhau)

Filecoin's page describes Bacalhau as supporting large-scale parallel compute of Filecoin data, with compute providers able to run Bacalhau nodes regardless of whether they host Filecoin data. This is useful because Filecoin's hard problem is not only storing data but making stored data computationally useful without extracting everything to a centralized cloud.

## Use cases

### 1. Log processing at the edge

A network of nodes generates logs locally: relays, gateways, LoRa base stations, IPFS gateways, Nostr relays, Bitcoin nodes, or application servers. Shipping raw logs to a central analytics cluster is expensive and privacy-invasive. With Bacalhau, each node can run a container that extracts aggregates, anomaly summaries, or compressed features locally, then publish only the result.

This pairs naturally with [MOC - Metadata Privacy](/kb/map-metadata-privacy/): do not centralize unnecessary metadata if local aggregation is enough.

### 2. Multi-region analytics without data export

Organizations often keep datasets in specific jurisdictions for compliance. Bacalhau can run the same DuckDB or Python job in each region and combine only aggregate outputs. This is not cryptographic privacy by itself, but it reduces the blast radius of data movement and can be composed with [Multi-Party Computation](/kb/multi-party-computation/), [Overview - Private Information Retrieval](/kb/private-information-retrieval/), or TEEs when stronger guarantees are required.

### 3. IPFS/Filecoin batch processing

A dataset pinned to IPFS or stored through Filecoin can be processed by CID. This is useful for:

- generating indexes over archived content;
- transcoding or thumbnailing media;
- extracting embeddings from open datasets;
- verifying datasets before retrieval deals;
- running scientific transforms where the input should remain content-addressed.

The output can be another CID plus a signed manifest, giving a reproducible pipeline.

### 4. Distributed ML preprocessing

Training pipelines often spend huge time on preprocessing: deduplication, tokenization, filtering, embedding extraction, feature generation. These jobs are embarrassingly parallel and data-heavy, so they fit CoD well. Bacalhau is less about all-reduce training than about preparing data where it lives, then feeding a later [Decentralized Training](/kb/decentralized-training/) run.

### 5. Sovereign research consortia

A consortium of universities, hospitals, or civic labs may not be allowed to pool raw data. Bacalhau can coordinate jobs across members' machines and return aggregate statistics or model updates. On its own, this is a governance/trust pattern; with [Overview - Confidential Computing](/kb/confidential-computing/), [Multi-Party Computation](/kb/multi-party-computation/), or [Overview - Fully Homomorphic Encryption](/kb/fully-homomorphic-encryption/), it becomes a stronger privacy-preserving computation stack.

### 6. Off-grid and intermittently connected environments

Because the architecture emphasizes network resilience and local execution, Bacalhau is conceptually useful for [Overview - Off-Grid Networks](/kb/off-grid-networks/) scenarios: ships, field labs, disaster zones, local-first mesh clusters. Jobs can execute when links are up, continue locally through disruption, and publish outputs later.

## Trade-offs

### Strengths

- **Attacks the right bottleneck for big data:** bandwidth, egress, and jurisdictional movement often dominate compute cost.
- **Works with existing tooling:** Docker, YAML job specs, S3, HTTP, IPFS, local mounts, and DuckDB are pragmatic choices.
- **Single-binary deployment:** lowers operational friction for edge/fleet deployments.
- **Content-addressed compatibility:** IPFS CIDs provide verifiable input references.
- **Composable:** can sit underneath privacy layers (TEE/MPC/FHE) or above decentralized storage.
- **No token dependency for core utility:** easier to adopt inside institutions that cannot touch crypto payment rails.

### Limitations

- **Not a trustless marketplace by default:** if a compute node is malicious, Bacalhau alone does not magically prove correct execution.
- **No confidentiality by default:** the node running the job can usually see input data and code unless additional isolation is used.
- **Data availability remains hard:** IPFS CIDs are only useful if someone pins/serves the data reliably.
- **Result verification is application-specific:** deterministic jobs can be rerun; ML and floating-point jobs need tolerances; adversarial jobs may need TEEs or proofs.
- **Less direct GPU marketplace liquidity:** for raw H100 rental, [Akash](/kb/akash/), [io.net](/kb/io-net/), [Render Network](/kb/render-network/), [Aethir](/kb/aethir/), or centralized clouds are more direct.
- **Enterprise/fleet bias:** the current strongest use cases are controlled fleets and consortia, not anonymous open compute.

## Attack surface and mitigations

| Attack / failure mode | Why it matters | Mitigation |
|---|---|---|
| Compute node lies about output | A malicious node can skip work or alter results. | Deterministic replay, redundant execution on multiple nodes, signed outputs, application-level checks, TEEs. |
| Compute node reads sensitive data | Bacalhau moves code to data, but the local node still sees the data. | Use trusted nodes, private clusters, [Confidential-Containers](/kb/confidential-containers/), [Attestation-Architecture](/kb/remote-attestation/), [Multi-Party Computation](/kb/multi-party-computation/). |
| Malicious job attacks provider | Running arbitrary containers is dangerous for node operators. | Sandboxing, least privilege, WASM where possible, cgroups/seccomp, no host mounts unless needed. |
| CID unavailable or slow | Content addressing does not guarantee retrieval. | Pinning, Filecoin deals, multiple gateways, local caching. |
| Output tampering during publication | Results can be modified if publisher/storage is compromised. | Hash outputs, sign manifests, publish CIDs, append audit logs. |
| Scheduler centralization | Orchestrator becomes a policy chokepoint. | Federated orchestrators, local queues, open specs, run your own control plane. |
| Compliance theater | Data “stays local” but outputs may leak sensitive aggregates. | Differential privacy, query review, aggregation thresholds, red-team output channels. |

## Maturity assessment

| Dimension | Assessment |
|---|---|
| Development activity | Active. GitHub API on 2026-05-05: pushed 2026-04-29, updated 2026-05-01, 858 stars, 100 forks, not archived. |
| Open-source posture | Strong. Apache-2.0 core repository; commercial product/trademark caveats from Expanso. |
| Production readiness | Good for controlled fleets, edge jobs, and batch pipelines. Evaluate carefully for adversarial open networks. |
| Ecosystem fit | Strong with IPFS/Filecoin, DuckDB, edge analytics, and decentralized storage. |
| Privacy guarantees | Weak by default; strong only when composed with TEEs/MPC/FHE or trusted local operators. |
| Decentralization | Medium. Distributed execution is real; trustless economic settlement and adversarial verification are not the main product focus. |
| Best current use | Compute-over-data orchestration for logs, analytics, ML preprocessing, and regional/federated datasets. |

## How Bacalhau compares to other compute notes

| System | Primary abstraction | Best fit | Trust model |
|---|---|---|---|
| [Bacalhau and Compute-over-Data](/kb/bacalhau/) | Job near data | Distributed analytics, IPFS/Filecoin jobs, edge/fleet compute | Trust node / replay / add TEE |
| [Akash](/kb/akash/) | Kubernetes-style lease marketplace | General containers, web services, GPUs | Trust provider unless adding attestation |
| [Golem](/kb/golem/) | Requestor/provider task market | Generic batch CPU jobs | Trust provider + sandbox |
| [Render Network](/kb/render-network/) | GPU rendering / GPU jobs | Rendering, creator workloads, some AI | Trust render service/provider network |
| [io.net](/kb/io-net/) | Aggregated GPU cloud | AI inference/training on distributed GPUs | Provider verification + staking; no confidentiality |
| [Phala and 0G](/kb/phala-and-0g/) | TEE-attested workloads | Confidential AI / verifiable off-chain compute | Trust TEE vendor + attestation chain |
| [Decentralized Training](/kb/decentralized-training/) | Distributed model optimization | Open model training / RL swarms | Algorithmic verification, TEEs, reputation |

The dividing line: Bacalhau is **data-local orchestration**, not just compute rental.

## Practical patterns

### Content-addressed transform

1. Pin dataset to IPFS and record CID.
2. Submit Bacalhau job that mounts the CID into `/data`.
3. Run deterministic container/WASM transform.
4. Publish output directory to IPFS/S3.
5. Sign manifest containing input CID, container digest, output CID, parameters, and timestamp.

This creates a reproducible provenance chain. It is especially useful for public archives and research datasets.

### Regional aggregate query

1. Deploy Bacalhau compute nodes in each region.
2. Keep raw data local.
3. Run DuckDB query partitions locally.
4. Return aggregate rows only.
5. Combine aggregates centrally.
6. Apply differential privacy or thresholding if outputs are sensitive.

This pattern is weaker than cryptographic privacy but much easier to deploy.

### Confidential CoD composition

1. Run Bacalhau on nodes with TEE support.
2. Schedule jobs only onto attested nodes.
3. Verify quote binds the expected container/WASM digest.
4. Encrypt inputs to enclave-held keys.
5. Publish signed outputs.

This is the bridge between Bacalhau and [Overview - Confidential Computing](/kb/confidential-computing/). It is not “Bacalhau by default”; it is a composed architecture.

## Open questions

- Will Bacalhau grow into a permissionless public marketplace, or remain mostly a fleet/enterprise orchestration layer?
- How should result verification be standardized for deterministic CoD jobs?
- Can IPVM/Homestar-style object capabilities give a cleaner security model than Docker containers?
- What is the right payment/settlement layer when jobs are run across mutually distrustful organizations?
- How should data-local jobs express privacy budgets, output restrictions, and compliance constraints?
- Can Bacalhau become a standard preprocessing plane for [Decentralized Training](/kb/decentralized-training/) datasets?

## Primary sources

- Bacalhau docs — [What is Bacalhau?](https://bacalhau.org/docs/)
- Bacalhau architecture — [bacalhau.org/docs/overview/architecture](https://bacalhau.org/docs/overview/architecture/)
- Bacalhau GitHub — [github.com/bacalhau-project/bacalhau](https://github.com/bacalhau-project/bacalhau)
- Bacalhau IPFS input source — [bacalhau.org/docs/sources/ipfs](https://bacalhau.org/docs/sources/ipfs/)
- Bacalhau DuckDB integration — [bacalhau.org/integrations/duckdb](https://bacalhau.org/integrations/duckdb/)
- IPFS docs — [Compute-over-Data with content-addressed data](https://docs.ipfs.tech/concepts/cod/)
- Filecoin Foundation ecosystem page — [Bacalhau](https://fil.org/ecosystem-explorer/bacalhau)
- IPVM / Homestar — [github.com/ipvm-wg/homestar](https://github.com/ipvm-wg/homestar/)
- IPVM specification — [github.com/ipvm-wg/spec](https://github.com/ipvm-wg/spec)

Continue with [Compare decentralized compute platforms](/kb/compare-decentralized-compute/).
