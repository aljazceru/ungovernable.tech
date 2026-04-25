---
title: "ZK Rollups"
tags:
  - "zk"
  - "rollups"
  - "layer-2"
  - "ethereum"
  - "starknet"
  - "zksync"
  - "deep-dive"
---
*Layer-2 scaling for Ethereum (and increasingly other L1s) where transactions execute off-chain and a single succinct proof of correctness gets posted on-chain. The most-deployed real-world application of zero-knowledge cryptography.*

---

## The problem ZK rollups solve

Ethereum L1 processes 20-50 transactions per second. ZK rollups push that to thousands per second by:

1. Executing transactions off-chain.
2. Generating a succinct proof that the executed state transition is correct.
3. Posting the proof plus minimal data to L1.
4. Having the L1 contract verify the proof in milliseconds and update the rollup's canonical state.

The user gets:

- Inherited L1 security. Once the proof verifies, the state transition is final on L1.
- No fraud-proof window (unlike optimistic rollups). Finality is immediate.
- Cheap fees, typically 1-100x cheaper than L1.

The trade-off: prover infrastructure is heavyweight, and proving general EVM execution is hard. The 2020-2025 era was about closing the gap between "ZK rollup" and "fully Ethereum-equivalent ZK rollup."

---

## Architectural choices

### Type-1 to Type-4 zkEVMs

Vitalik's classification (2022):

- **Type-1**: Fully Ethereum-equivalent. Re-executes Ethereum without changes. Hardest to prove. Examples: Taiko (close), Polygon zkEVM (close).
- **Type-2**: EVM-equivalent. Slight differences in storage layout but bytecode-level compatible. Most production zkEVMs (Scroll, Polygon zkEVM, Linea).
- **Type-2.5**: EVM-equivalent at consensus but with gas-cost adjustments to make ZK proving cheaper.
- **Type-3**: Almost EVM-equivalent. Some opcodes adjusted or unsupported.
- **Type-4**: Compile Solidity to a custom ZK-friendly VM. Highest performance, lowest compatibility. Examples: zkSync Era, StarkNet (Cairo).

Trade-off: developer experience vs prover performance. The 2024-2026 industry has converged on Type-2 / Type-2.5 as the production sweet spot.

### Validium vs volition vs rollup

- **Rollup**: full transaction data on L1 (data availability via L1).
- **Validium**: ZK proof on L1, transaction data off-chain (data availability via committee or DA layer).
- **Volition**: per-transaction choice between rollup mode and validium mode.

Validiums are cheaper but have an additional trust assumption: the data-availability committee must not censor or hide data. EigenDA, Celestia, and Avail provide more decentralized DA than committee-based options.

---

## Major ZK rollups (early 2026)

### Type-2 zkEVMs

| Project | Approach | Status |
|---------|----------|--------|
| **Polygon zkEVM** | Plonkish + Plonky2 | Live since 2023 |
| **Scroll** | Halo2 + KZG | Live since 2023 |
| **Linea** | Custom proving system | Live since 2023 |
| **Taiko** | Type-1 / Type-2 | Live; closest to true Ethereum-equivalent |

### Type-4 zkVMs

| Project | VM | Status |
|---------|-----|--------|
| **StarkNet** | Cairo VM (Cairo language) | Live since 2020 |
| **zkSync Era** | EraVM (Solidity-via-LLVM) | Live since 2023 |

### Specialized

| Project | Focus |
|---------|-------|
| **Aztec** | Privacy-by-default with ZK + encrypted state |
| **Polygon Miden** | High-throughput STARK-based VM |
| **Risc0 / SP1 / Jolt** | RISC-V zkVMs as L2 alt |
| **Aleo** | Privacy-focused L1 with ZK execution |

---

## How a transaction flows

```
User signs transaction
  ↓
Submitted to rollup sequencer (off-chain)
  ↓
Sequencer batches transactions, executes them
  ↓
Prover generates succinct proof of state-transition validity
  ↓
Sequencer posts to L1:
  - State root after batch
  - Proof
  - Transaction data (if rollup) or DA-blob commitment (if validium)
  ↓
L1 verifier contract checks proof, updates rollup canonical state
  ↓
User can withdraw to L1 at any time after batch is finalized
```

Latency:
- Soft confirmation (sequencer accepted): seconds.
- Hard confirmation (L1 batch posted plus proven): minutes to hours.
- Withdrawal latency to L1: minutes (vs around 7 days for optimistic rollups).

---

## Sequencer centralization

A practical concern: most ZK rollups today have a single sequencer (Polygon Foundation, Matter Labs, StarkWare). The sequencer can:

- Refuse transactions (censorship).
- Reorder transactions (MEV extraction).
- Halt the chain (liveness failure).

Mitigations:

- Force-include via L1. Users can post transactions directly to L1 to force inclusion.
- Decentralized sequencers (rolling out 2025-2026): Espresso, Astria, native sequencer markets.
- Shared sequencers: multiple rollups share decentralized sequencer infrastructure.

The 2026 trajectory is toward decentralized sequencers as a baseline expectation.

---

## DA (data availability) and the modular stack

The other critical layer: data availability.

- **L1 (Ethereum)**: most expensive DA. Blob (EIP-4844) reduced cost substantially since 2024.
- **Celestia**: sovereign rollups; modular DA layer.
- **EigenDA**: Ethereum-staked DA via restaking.
- **Avail**: DA-focused L1.
- **Validium committees**: centralized but cheap.

Modular thesis: separate execution (rollup), settlement (L1), consensus, and DA. Each layer specializes; rollups assemble them.

---

## ZK rollups beyond Ethereum

- **Bitcoin via BitVM**: optimistic verification of ZK proofs on Bitcoin. Long-term direction, complex.
- **Cosmos via Sovereign / SDK**: ZK rollups as Cosmos SDK chains.
- **Solana via Light**: privacy-focused ZK on Solana.
- **L1 with ZK at consensus**: Aleo, Aztec — privacy-first.

The ZK rollup pattern is escaping its Ethereum-specific origin.

---

## Privacy in ZK rollups

Most production ZK rollups are **not privacy-preserving**. They prove correctness, not privacy. State and transactions are public on L1 (in rollup mode) or visible to the operator (in validium mode).

Privacy-preserving ZK chains differ:

- **Aztec**: encrypted state with ZK execution. Transactions and balances private.
- **Aleo**: ZK execution with privacy as default, public toggle.
- **Zcash**: shielded pool on a non-rollup L1.
- **Railgun**: privacy layer over EVM rollups.

For sovereignty users: a generic zkSync transaction is no more private than an L1 transaction. For privacy, choose privacy-by-design protocols.

---

## Trade-offs

### Strengths

- Inherited L1 security with fast finality.
- Cheaper than L1, often by 10-100x.
- No fraud-proof delay (vs optimistic).
- Mature. Deployed for years with billions in TVL.
- Composable. Apps work across rollups via bridges.

### Limitations

- Sequencer centralization (improving).
- Proving cost is significant; passed through to gas pricing.
- No privacy by default.
- Cross-rollup interop is still rough. Bridges are the largest attack surface in DeFi.
- Trusted setup for some constructions (KZG-based).

---

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Sequencer censorship | Force-include from L1; decentralized sequencer |
| MEV extraction by sequencer | Decentralized sequencer auctions |
| Bridge exploit | Audit bridges; native account abstraction; ZK light clients |
| Prover bug | Formal verification of proving system; independent provers |
| L1 reorg | Wait for L1 finality |
| DA layer compromise (validium) | Use rollup mode for high-stakes; verify DA committee |
| Soundness break in proof system | Defense in depth: multiple proof systems |

---

## Recent developments (2024-2026)

- Pectra hard fork (2025) on Ethereum optimizes for L2 throughput.
- Decentralized sequencers (Espresso, native sequencer markets) reach production.
- EigenDA / Celestia / Avail mature as DA layers.
- Type-1 zkEVMs (Taiko et al.) approach full equivalence.
- Folding-based provers ([Folding Schemes](/zero-knowledge/folding-schemes)) reduce proving costs.
- GPU / FPGA prover acceleration by Cysic, Ingonyama, ZPrize winners.
- Aztec mainnet rollout for privacy-by-default L2.

---

## Related files

- [Overview - Zero-Knowledge Proofs](/zero-knowledge)
- [SNARKs](/zero-knowledge/snarks)
- [STARKs](/zero-knowledge/starks)
- [Folding Schemes](/zero-knowledge/folding-schemes)
- [ZKML](/zero-knowledge/zkml)
- [Overview - Financial Sovereignty](/financial-sovereignty)
- [Glossary](/meta/glossary) — ZK rollup, validium, volition, zkEVM types

---

## Primary sources

- Vitalik Buterin, *The different types of zk-EVMs*, 2022.
- StarkWare, *Cairo Whitepaper*. [starkware.co](https://starkware.co).
- Matter Labs, *zkSync Era documentation*. [docs.zksync.io](https://docs.zksync.io).
- Polygon zkEVM — [polygon.technology/polygon-zkevm](https://polygon.technology/polygon-zkevm).
- Scroll — [scroll.io](https://scroll.io).
- Linea — [linea.build](https://linea.build).
- Aztec Network — [aztec.network](https://aztec.network).
- Celestia — [celestia.org](https://celestia.org).
- L2Beat — [l2beat.com](https://l2beat.com) (rollup data).

