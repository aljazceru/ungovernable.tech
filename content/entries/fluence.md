---
title: "Fluence"
slug: fluence
type: deep-dive
pillars: ["compute"]
readiness: usable
description: "Fluence, a decentralized marketplace for virtual servers and GPU containers run by independent providers: how it works and what you trust."
dek: "The \"cloudless\" compute platform. DePIN marketplace for virtual servers and GPU containers, built on an Arbitrum Orbit L2 anchored to Ethereum, with a Rust-based composition language (Aqua) and WASM execution model. The 2026 Vision plan focuses on tokenizing compute as RWAs to meet AI's exponential demand."
updated: 2026-06-08
created: 2026-06-08
origin: vault
source: "04-Decentralized-Compute/Fluence.md"
aliases: ["Fluence Network", "FLT"]
tags: ["fluence", "flt", "decentralized-compute", "depin", "serverless", "aqua", "marine", "rust", "deep-dive"]
---

## Position

Fluence is a decentralized serverless computing platform — the model where you deploy functions or services without managing infrastructure — running on independently operated nodes coordinated through an Arbitrum Orbit L2 (InterPlanetary Consensus / IPC) appchain anchored to Ethereum.

Compared to the rest of this library's compute coverage:

| Dimension | Fluence | Akash | Phala | Golem |
|-----------|---------|-------|-------|-------|
| Model | Serverless VMs + containers | K8s-style containers | TEE-attested CVMs | Task-based batch |
| Confidential | TEE roadmap (2026) | No | Yes (TEE native) | No |
| Language | Aqua/Rust/WASM | Docker | Docker | Generic |
| Chain | Arbitrum Orbit L2 (IPC) | Cosmos | Substrate/ETH L2 | ETH/Polygon |
| Token | FLT (ERC-20 on ETH) | AKT | PHA | GLM |
| GPU | Coming 2026 | H100s (live) | H100 CC (production) | Limited |

Fluence's differentiation is its Rust-first, WASM-centric developer experience and its "cloudless" positioning — the network itself provides the orchestration, discovery, and payment layer without hyperscaler intermediaries.

## Architecture

### InterPlanetary Consensus (IPC) — the L2 foundation

Fluence is built on IPC, a Filecoin-launched framework for deploying app-specific L2 blockchains anchored to Ethereum. IPC provides:

- Low transaction fees (Arbitrum Orbit stack).
- Custom appchain with your own validators.
- Ethereum L1 finality via the parent chain's security.
- Native Filecoin storage integration for state.

Fluence runs its compute coordination and payment settlement on this L2. Providers run nodes that participate in the IPC chain; the chain tracks capacity commitments, compute deals, and staking collateral.

### Aqua — the composition language

Aqua is Fluence's domain-specific language for composing distributed services. It compiles to WASM and runs inside Marine, Fluence's WASM runtime. Aqua is designed for the specific challenges of distributed compute:

- **Service graphs**: describe which service calls which, with retry policies, timeouts, and fallbacks.
- **Peer discovery**: finds nodes with the right capacity in the network.
- **Secret injection**: credentials and keys are injected from the Fluence key store, not hardcoded.
- **Type-safe**: strong typing across the service boundary, no JSON guessing.

```rust
// Aqua example: call a service with a fallback
service MyService("my-service-id");
service BackupService("backup-service-id");

pub fn call_with_fallback(arg: u64) -> u64 {
    MyService.compute(arg)!
    || BackupService.compute(arg)
}
```

Marine is the runtime. A "marine" is a WASM module deployed to the Fluence network; it can be composed with other marines via Aqua.

### Compute providers

Providers run the Fluence node software and offer capacity (CPU, RAM, GPU when available) to the network. They:

1. Post a **Capacity Commitment** to the IPC chain: "I offer X cores, Y GB RAM, Z GPU for period P."
2. Receive compute deals from requestors.
3. Execute workloads inside isolated environments (WASM sandbox initially; TEE later).
4. Get paid in USDC (stablecoin settlements on Fluence's payment layer).

### FLT token

- **Total supply**: 1,000,000,000 FLT.
- **Allocation**:
  - Community rewards: ~50M FLT (5%) to ~110,000 developers.
  - Team + investors: locked until Feb 2025, then daily unlocks through Feb 2026.
  - Ecosystem: the remainder.
- **Utility**: staking (provider collateral), governance (Fluence DAO), and protocol-level functions.

Stakers (delegators) contribute FLT as collateral to secure the network and earn FLT rewards. Providers must meet a minimum staking threshold proportional to their capacity commitments.

### Payment model

- Compute is paid in **USDC** (stablecoin), not FLT.
- FLT is used for staking and governance, not direct payment.
- This separates token speculation from compute costs — a design choice that makes it easier for enterprises to adopt without crypto price volatility affecting their bills.

## Fluence Vision 2026

The May 2025 "Vision 2026" plan outlined scaling to meet AI's exponential compute demand through **RWA-tokenized compute** — representing physical GPU and CPU capacity as tradeable digital assets backed by real infrastructure.

Key elements:

- Tokenized compute capacity (FLT representing real hardware).
- GPU expansion (H100/GPU nodes on the roadmap).
- TEE confidential computing (2026 target).
- Enterprise adoption focus.

## Aqua and Marine — the WASM stack

### Marine

Marine is the WASM runtime that executes deployed services ("marines"). Each marine is a WASM module with a typed interface defined via the `#[marine]` proc macro in Rust:

```rust
use fluence::marine;

#[marine]
pub fn add(a: f64, b: f64) -> f64 {
    a + b
}
```

Marines can be composed: one marine can call another marine deployed on a different node, with Aqua handling the serialization, peer resolution, and error propagation.

### Aqua

Aqua is the language for writing distributed application logic that coordinates multiple marines and network resources. It runs on the Fluence network and compiles to WASM. Key features:

- **peerify**: makes a function callable across the network, advertising it as a service.
- **service ability**: typed service interfaces.
- **retry/timeout**: built-in fault tolerance.
- **secret store**: inject keys at invocation time, not at compile time.

### Aquamarine

The broader Aquamarine project encompasses the Aqua language, Marine runtime, and the IPFS integration layer. The stack lets you:

1. Write a service in Rust, compile to WASM via Marine.
2. Compose multiple services with Aqua.
3. Deploy to the Fluence network (backed by IPC).
4. Store state on Filecoin via the IPC integration.

## Comparison

|| Dimension | Fluence | Akash | Phala | Golem |
||-----------|---------|-------|-------|-------|
|| Model | Serverless (WASM) | K8s containers | TEE VMs | Task batch |
| Confidential | TEE (roadmap) | No | Yes (TDX/H100 CC) | No |
| Language | Aqua/Rust/WASM | Docker | Docker | Generic |
| Payment | USDC (stable) | AKT (burns to ACT) | PHA | GLM |
| Chain | Arbitrum Orbit L2 | Cosmos SDK | Substrate/ETH L2 | ETH/Polygon |
| GPU support | Coming | H100 (live) | H100 CC (prod) | Limited |
| FLT status | ERC-20 on ETH | Cosmos coin | Substrate coin | ERC-20 |

## Trade-offs

### Strengths

- **WASM-native**: strong isolation, fast cold starts, language-agnostic (Rust, Go, C++, etc. compile to WASM).
- **Stablecoin payments**: enterprises can pay in USDC without touching FLT.
- **IPC integration**: native Filecoin storage for state, Ethereum security for settlement.
- **Rust/Aqua stack**: modern developer experience with strong typing across distributed service boundaries.
- **Cloudless pitch**: no hyperscaler lock-in, transparent pricing, community-governed.
- **DePIN economics**: real hardware providing real compute, with FLT aligning incentives.

### Limitations

- **Younger than Akash/Golem**: less production battle-testing than the older networks.
- **GPU inventory**: behind Phala and Akash on GPU availability; GPU nodes are 2026.
- **TEE**: not yet live; Phala is the mature production option for confidential compute today.
- **Adoption**: smaller provider network than hyperscalers; reliability depends on network density.
- **WASM learning curve**: Aqua/Marine is a different mental model than Docker/K8s.

## Attack surface

|| Attack | Mitigation |
||--------|-----------|
| Dishonest provider | Staking collateral; reputation system; compute verification |
| Computation integrity | WASM sandbox; result verification by requestor |
| IPC chain compromise | Ethereum L1 anchoring; Arbitrum Orbit security |
| Key theft | Secret store injection; key management |
| Sybil provider | Staking threshold; capacity commitment on-chain |
| FLT governance capture | DAO governance; token distribution spread |

## Primary sources

- Fluence website — [fluence.network](https://fluence.network)
- Documentation — [fluence.dev](https://fluence.dev)
- API — [api.fluence.dev](https://api.fluence.dev)
- Explorer — [explorer.fluence.dev](https://explorer.fluence.dev)
- GitHub — [github.com/fluencelabs](https://github.com/fluencelabs)
- FLT tokenomics — [fluence.network/blog/fluence-tokenomics](https://www.fluence.network/blog/fluence-tokenomics)
- Vision 2026 — [fluence.network/blog/fluence-vision-2026](https://www.fluence.network/blog/fluence-vision-2026)
- IPC launch — [cryptoslate.com/press-releases/fluence-launches-cloudless-computing-platform](https://cryptoslate.com/press-releases/fluence-launches-cloudless-computing-platform-a-permissionless-answer-to-centralized-cloud-providers)
- Aqua/Marine docs — [fluence.dev/docs/aqua-book](https://fluence.dev/docs/aqua-book)
