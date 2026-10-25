---
title: "BitVM"
slug: bitvm
type: deep-dive
pillars: ["zk", "money"]
readiness: experimental
description: "BitVM lets Bitcoin verify arbitrary computation through fraud proofs, without a soft fork: how it works, what it enables for bridges, and its costs."
dek: "A way to express and verify arbitrary computation on Bitcoin without consensus changes. Robin Linus's October 2023 white paper \"BitVM: Compute Anything on Bitcoin\" showed that existing Bitcoin Script primitives — bit commitments, hash locks, and the limited operators in Tapscript — are enough to build a fraud-proof game where an off-chain prover and verifier interactively challenge each other and Bitcoin only adjudicates the disputed step. Subsequent designs (BitVM2, BitVM-X, ZK-BitVM) compress the interaction down to single-round dispute and integrate SNARK verifiers, making trust-minimized BTC bridges and expressive smart contracts plausibly buildable on Bitcoin without a soft fork."
updated: 2026-04-26
created: 2026-04-26
origin: vault
source: "09-Zero-Knowledge/BitVM.md"
aliases: ["BitVM2", "BitVM-X", "Bitcoin VM"]
tags: ["zk", "bitcoin", "bitvm", "fraud-proofs", "bridges", "deep-dive"]
---

## The problem BitVM addresses

Bitcoin Script is intentionally restricted: no loops, no recursion, no stateful storage, and historically disabled arithmetic operators (`OP_MUL`, `OP_DIV`, `OP_CAT`). Building expressive smart contracts (a SNARK verifier, a state-machine commitment, a bridge contract) requires either:

1. A consensus change (a soft fork to add operators) — politically slow, has happened rarely.
2. An off-chain construction that uses Bitcoin only for adjudication — the BitVM approach.

BitVM picks option 2. The insight is that Bitcoin doesn't need to *execute* the computation — it only needs to be able to *punish* a party who lies about the result. If you can build a fraud-proof game where the loser's coins are forfeited, you've made off-chain computation enforceable on Bitcoin.

## Original BitVM (October 2023)

Robin Linus, "BitVM: Compute Anything on Bitcoin," white paper, October 2023.

### Bit commitments

The primitive: Alice commits to a bit `b` by publishing two hash preimages `P0`, `P1` such that revealing `P0` claims `b=0` and revealing `P1` claims `b=1`. Revealing both burns Alice's stake (the contract is constructed so that double-revealing means anyone can claim a punishment payout).

This gives Bitcoin Script *committed boolean values* — a building block it didn't have natively.

### Logic gates from bit commitments

Combining bit commitments with hash-lock conditions, Linus showed how to encode NAND gates (and therefore arbitrary boolean circuits) into Tapscript leaves. A circuit's evaluation becomes a sequence of gate evaluations, each of which can be challenged.

### The interactive fraud-proof game

The construction:

1. **Setup.** Alice (the prover) and Bob (the verifier) co-fund a Taproot output containing many tapscript leaves, each encoding a possible challenge.
2. **Off-chain assertion.** Alice asserts off-chain: "I executed program `P` on input `x`, and got output `y`."
3. **Off-chain challenge.** Bob can disagree. The protocol proceeds via a binary search over the execution trace ("disagree at step 0 to N/2 or N/2 to N?") until a single disputed gate is identified.
4. **On-chain dispute resolution.** Alice spends the relevant tapscript leaf, revealing her bit-commitment preimages for that gate's inputs and output. The script checks the gate's logic. If Alice lied (output is inconsistent with inputs), Bob spends a punishment branch. If Alice told the truth, the dispute resolves in her favor.

Number of on-chain transactions in the worst case: log of the trace length, plus the final adjudication. Each transaction is small (few hundred bytes); the total is manageable.

### What original BitVM proved

- It's possible to do fraud-proof-based off-chain computation on Bitcoin today, with no soft fork.
- The construction is impractical for production at the original parameter sizes (Taproot output trees blow up combinatorially with circuit size; setup is heavy; multi-round disputes are slow).
- But it's a proof of concept that the *abstract* primitive — verifiable off-chain computation — exists on Bitcoin.

The white paper triggered an explosion of follow-up work in 2024.

## BitVM2 (2024)

Linus, Aumayr, Zamyatin, et al., "BitVM2: Bridging Bitcoin to Second Layers," 2024.

The major improvements:

### Single-round disputes

Instead of binary-searching over the trace via multiple on-chain rounds, BitVM2 commits to the entire execution trace once (in a Merkle-root-style structure embedded in Taproot leaves) and lets the challenger expose a single disputed step in one transaction. This reduces worst-case dispute latency from `O(log n)` rounds to a single round.

### Permissionless challenges

BitVM2 changes the trust model: in original BitVM, only a designated verifier could challenge. BitVM2 lets *any* party challenge a faulty assertion (with a bond). This is the property needed for trust-minimized bridges: the bridge operator can be challenged by anyone watching the chain, not just by a pre-committed counterparty.

### SNARK verifier circuits

BitVM2 expresses a Groth16 verifier as a circuit suitable for the BitVM gate model. With this in place, an off-chain SNARK proof of a complex computation (rollup state transition, ZK light client) can be verified via the BitVM2 game on Bitcoin.

The proof is generated off-chain by a prover; the BitVM operator asserts "this proof verifies"; if anyone disputes, the BitVM game adjudicates the disputed gate of the SNARK verifier circuit. This is the construction that makes ZK-rollup-style bridges to Bitcoin possible.

## Subsequent designs

### BitVM3 / BitVM-X

Multiple research teams (StarkWare, Citrea, others) have published BitVM-family designs through 2024-2025, optimizing for: smaller setup, fewer Taproot leaves, lower per-dispute cost, more general circuit support, and integration with specific zkVMs (Risc0, SP1, Cairo).

The naming has been informal — "BitVM3" appears in some materials, "BitVM-X" in others. The space is a moving target.

### ZK-BitVM

A line of work that fully integrates a SNARK verifier into the BitVM game. The off-chain prover generates a SNARK; the on-chain dispute, if it happens, falls back to verifying a single arithmetic constraint of the SNARK verifier on-chain. Most production BitVM-bridge designs in 2025 are this style.

## Applications

### Trust-minimized Bitcoin-bridged BTC

The headline application. A BitVM bridge holds BTC in a multi-sig (or Taproot) output on Bitcoin and mints wrapped BTC on a second layer (a sidechain, an L2, or another chain). Withdrawals from the second layer trigger BitVM-mediated unlock on Bitcoin.

The bridge operator asserts "this withdrawal is valid per the L2's state"; anyone can challenge; if the operator lies, they're slashed and the bridge state recovers.

Compared to existing bridge designs:

| Bridge type | Trust |
|-------------|-------|
| Multi-sig federation (e.g. WBTC, RSK federation) | Trust the federation members |
| Optimistic with watchtowers | Trust at least one watchtower is online |
| BitVM | Trust at least one challenger is online + the off-chain proof system |
| Native (with consensus change) | Trustless |

BitVM gets close to native — the trust assumption reduces to "at least one honest party watches the bridge during the challenge window."

Production projects targeting BitVM bridges include Citrea, BitlayerLabs's BitVM-bridge work, and several others. As of the cutoff, no BitVM bridge is in full production with material BTC volume; demos and testnets exist.

### Expressive smart contracts on Bitcoin

Beyond bridges: any application that can be expressed as a fraud-proof game can run via BitVM. Examples: DLC-style oracles where the oracle's signature is verified via BitVM, complex multi-party state channels, Bitcoin-native rollups.

### Bitcoin-native ZK light clients

A chain (Ethereum, Solana, Cosmos, Bitcoin itself) can have its consensus verified inside a BitVM game on Bitcoin. The output is a Bitcoin contract that releases funds based on another chain's state, without trusting an oracle.

## Trade-offs

### Strengths

- No consensus change needed. Works on Bitcoin today.
- Trust-minimized in the limit: requires only one honest challenger.
- Composes with mature ZK proof systems (Groth16, STARKs via wrappers — see [SNARKs](/kb/snarks/) and [STARKs](/kb/starks/)).
- Generalizable: applications beyond bridges are conceivable.

### Limitations

- **Liveness assumption.** The fraud-proof game requires at least one honest challenger to be online during the challenge window. If a faulty assertion goes unchallenged, it stands.
- **Challenge windows are long.** Days to weeks, depending on parameters. Withdrawals are slow.
- **Setup cost is high.** Each BitVM instance requires a sizable Taproot setup; not amortizable across multiple disputes cheaply.
- **Capital efficiency.** Bridge operators must lock collateral for the challenge window; high-volume bridges need a lot of collateral.
- **Tooling immaturity.** The compiler stack from circuits to BitVM Taproot leaves is research-grade as of early 2026.
- **Bitcoin transaction cost.** A worst-case dispute walk can run several transactions; in a high-fee environment, this is real cost.
- **No production deployment with material volume yet.** All deployments at the cutoff are demos, testnets, or early-mainnet with small volume.

## Honest scope (early 2026)

- The cryptographic construction is sound and the demonstrated demos work.
- Engineering work on production-grade BitVM bridges is ongoing across multiple teams.
- Liveness assumptions and challenge windows are real constraints; users withdrawing from a BitVM bridge will wait days, not seconds.
- Capital efficiency for bridge operators is a real economic constraint.
- BitVM is *not* a generic Bitcoin smart-contract platform that competes with Ethereum. It is an enforcement layer for off-chain computation, with bridges as the dominant near-term application.

If a production BitVM bridge to Bitcoin ships with material BTC volume during 2026, the trust-minimized cross-chain BTC story changes substantially. Until that happens, it remains a watch-this-space technology.

## Comparison with related approaches

| Approach | Bitcoin consensus change? | Trust model | Maturity |
|----------|--------------------------|-------------|----------|
| **BitVM family** | None | One-honest-challenger + ZK proofs | Demos / early mainnet |
| **Drivechains (BIP 300/301)** | Soft fork required | Miner federation | Proposed; not adopted |
| **OP_CAT / OP_CTV-based covenants** | Soft fork required | None (consensus-enforced) | Proposed; not adopted |
| **Multi-sig federation bridges** | None | Trust federation | Mature (WBTC, etc.) |
| **Liquid Network sidechain** | None (sidechain) | Trust Liquid federation | Live |
| **Lightning** | None | Channel partners + watchtowers | Mature |

BitVM uniquely sits in the "no consensus change AND trust-minimized" cell. The trade-off is the liveness assumption and the long challenge window.

## Cross-cutting

- BitVM doesn't need a new ZK system; it composes with existing ones (Groth16 verifier circuits expressed as Tapscript leaves).
- The fraud-proof game pattern — interactive dispute over a committed trace — is parallel to optimistic rollups (Arbitrum, Optimism). BitVM is the Bitcoin analogue. See [ZK Rollups](/kb/zk-rollups/) for the ZK-side comparison.
- Once a BitVM bridge exists, [Lightning Network Deep Dive](/kb/lightning-network/) can be re-thought with BitVM-bridged BTC on faster L2s.

## Primary sources

- Linus, *BitVM: Compute Anything on Bitcoin*, white paper, October 2023 — [bitvm.org](https://bitvm.org).
- Linus, Aumayr, Zamyatin, et al., *BitVM2: Bridging Bitcoin to Second Layers*, 2024 — [bitvm.org/bitvm2.pdf](https://bitvm.org/bitvm2.pdf).
- BitVM source repositories — [github.com/BitVM](https://github.com/BitVM).
- Citrea — [citrea.xyz](https://citrea.xyz) (Bitcoin rollup using BitVM-style bridge).
- StarkWare BitVM-related research — [starkware.co](https://starkware.co).
- Robin Linus blog — [robinlinus.com](https://robinlinus.com).
