---
title: "Zero-Knowledge Privacy Applications"
slug: zk-privacy-applications
type: explainer
pillars: ["zk"]
description: "Chains and protocols that use zero-knowledge proofs for shielded transactions, private smart contracts and shielded pools, compared by design."
dek: "Six chains and protocols that use zero-knowledge proofs to deliver shielded transactions, private smart contracts, or shielded pools on top of public chains. Each picks a different point on the shielded-UTXO vs. shielded-account axis, a different proof system, and a different deployment surface (own L1, Cosmos zone, EVM L2, smart-contract overlay). The result is a fragmented landscape: each project has real users, none has won."
updated: 2026-04-27
created: 2026-04-26
origin: vault
source: "09-Zero-Knowledge/ZK Privacy Applications.md"
aliases: ["Privacy L1s", "Privacy L2s", "Shielded Chains"]
tags: ["zk", "privacy", "aztec", "penumbra", "aleo", "iron-fish", "namada", "railgun", "deep-dive"]
---

## The design space

A privacy application on a public chain has to answer five questions:

1. **State model.** Shielded UTXOs (Zcash-style notes) or shielded accounts (encrypted balances per address)?
2. **Proof system.** Groth16, PLONK, Halo2, or custom? See [SNARKs](/kb/snarks/) for the trade-offs.
3. **Deployment surface.** Own L1, Cosmos zone, EVM L2, or smart-contract pool on existing chains?
4. **Shielded asset support.** Single native asset only, or multi-asset shielded pool?
5. **Programmability.** Payments only, or full private smart contracts?

The six projects below sit at different points across these axes.

## Aztec — privacy-by-default L2

Aztec is the longest-running attempt at a private-by-default Ethereum L2. Founded 2018 (Aztec Protocol), it shipped Aztec Connect in 2022 (a shielded pool overlay on Ethereum, sunset 2024) and then pivoted to Aztec Network — a full L2 with hybrid public/private state.

**State model.** Hybrid. Each contract has a public state component (Merkle tree of slots, like Ethereum) and a private state component (encrypted notes, Zcash-style). A function call can read and write both, with private reads/writes proven inside a SNARK and public ones executed by the sequencer.

**Proof system.** Recursive Halo2 derivative (UltraHonk, then Honk). Each user produces a client-side proof of their private function call; the sequencer recursively aggregates these into a rollup proof. See [SNARKs](/kb/snarks/) for Halo2 specifics.

**Language.** Noir, a Rust-flavored DSL designed by the Aztec team for writing both private and public functions. Compiles to ACIR (Abstract Circuit Intermediate Representation), which the proving stack consumes.

**Status (early 2026).** Public testnet running since mid-2024. Mainnet launch has been "imminent" multiple times across 2024-2025 and was targeted for late 2025 / early 2026 with phased rollout. As of the cutoff, the network is in a public-launch phase with sequencer decentralization and full programmability still maturing. The Noir language and ACIR toolchain are mature and used by other projects independently of the L2.

**Real adoption.** Significant developer interest pre-mainnet (Noir is used outside Aztec for general SNARK app development). On-chain user adoption depends on mainnet stability. Honest read: Aztec has shipped less than its timeline promised, but the technology stack — particularly the hybrid private/public state model and the Noir tooling — is among the most ambitious in this list.

## Penumbra — Cosmos shielded zone

Penumbra is a Cosmos SDK chain focused on shielded multi-asset transactions and a shielded DEX. Built by Penumbra Labs starting 2021, mainnet launched mid-2024.

**State model.** Shielded UTXO (notes), Sapling-derived. Each note commits to (asset, amount, address). Spent notes produce nullifiers; the chain tracks a nullifier set to prevent double-spends.

**Proof system.** Groth16 over BLS12-377 (Penumbra's "decree" circuits). Per-circuit trusted setup ran in 2023. The team chose Groth16 for proof size and verifier efficiency given the constrained set of action types (spend, output, swap, delegate).

**Distinctive features.**

- **ZSwap.** A shielded DEX where individual user swaps are batched into a single per-block clearing price. Front-running and MEV are mitigated because individual orders are only revealed in aggregate. The mechanism is closer to a sealed-bid batch auction than to a CFMM.
- **Shielded staking.** Delegations and undelegations stay private; only the validator's total stake is public.
- **Shielded IBC.** Tokens bridged from other Cosmos chains via IBC become shielded notes in Penumbra, with unshielding back.

**Status.** Mainnet live since 2024, validator set decentralized, IBC connections to Cosmos Hub and other zones. Niche but real usage.

**Honest read.** Penumbra is the most cryptographically distinctive project in this list — the shielded-DEX construction is genuinely novel work. Adoption is small relative to Cosmos as a whole; positioning as "the shielded zone" depends on bridging interest from other Cosmos chains, which is slow.

## Aleo — Snarky-program L1

Aleo is an L1 designed by the team that built ZEXE (the Decentralized Private Computation primitive, Bowe et al. 2018). Mainnet launched in 2024 after extended testnet phases.

**State model.** Records (shielded UTXOs) plus public state for programs. A "transition" consumes input records and produces output records with a SNARK proof; programs (Leo or Aleo Instructions) define the transition logic.

**Proof system.** snarkVM, with a Halo2-derivative arithmetization (Marlin originally, then their own variant). Aleo invested heavily in custom proving infrastructure, including hardware acceleration via the snarkOS prover network.

**Language.** Leo, a Rust-inspired DSL for writing private programs that compile to AVM (Aleo Virtual Machine) bytecode and snarkVM circuits. Aleo Instructions is the lower-level bytecode.

**Tokenomics.** ARC tokens stake into the consensus; provers earn rewards via a coinbase puzzle (a SNARK-friendly proof-of-work-ish mechanism). The puzzle has been re-tuned multiple times across 2024-2025 because of ASIC and GPU concentration concerns.

**Status.** Mainnet live since early 2024. Programmatic activity has been slower than initial targets; the prover network is heavily concentrated in specialized hardware operators.

**Honest read.** The cryptographic engineering is serious (snarkVM is one of the more capable production zkVMs), but the deployment has been bumpy: token launch issues, prover concentration, and an ecosystem that hasn't yet produced a flagship application. The "snarky programs as L1 primitives" thesis has not been validated at scale.

## Iron Fish — Sapling-derived shielded chain

Iron Fish is an L1 launched April 2023, targeting a Zcash-like shielded payment system with a different chain and a different incentive model.

**State model.** Sapling-derived shielded UTXO. Notes commit to (asset, amount, viewing key); spends produce nullifiers. The construction is close to Zcash Sapling (Groth16 over BLS12-381), with multi-asset support added.

**Proof system.** Groth16 with the Sapling circuits, lightly modified for multi-asset. Per-circuit trusted setup completed in 2022 with a 1000+ participant ceremony.

**Multi-asset.** A single shielded pool holds multiple assets (custom asset issuance plus bridged assets); transactions reveal asset type only inside the encrypted note.

**View keys.** Iron Fish foregrounds *viewing keys* — selective-disclosure keys that let an auditor or counterparty see specified incoming/outgoing transactions. This is positioned as a compliance feature.

**Status.** Mainnet live since 2023. Trading volume and active addresses are small compared to Zcash or Monero. The team has emphasized regulatory dialog (viewing keys) over feature growth.

**Honest read.** Technically conservative — basically Sapling-on-its-own-chain — and small in adoption. The viewing-key compliance angle is interesting as a design choice but hasn't visibly broadened the user base.

## Namada — multi-asset shielded pool for Cosmos

Namada is a Cosmos SDK chain built by Heliax (the Anoma team's privacy-focused offshoot). Mainnet phased launch began late 2023.

**State model.** Multi-Asset Shielded Pool (MASP), a Sapling derivative supporting multiple asset types in one shielded set. MASP was first prototyped for Zcash and productionized by Namada.

**Proof system.** Groth16 with the MASP circuits.

**Distinctive features.**

- **Shielded actions for IBC.** Assets bridged in via IBC can be shielded into the MASP and unshielded back, providing privacy as a service to the wider Cosmos ecosystem.
- **Shielded rewards.** A shielding incentive program rewarded users for keeping balances in the MASP, growing the anonymity set during early mainnet. The program has been periodically re-tuned.
- **Cubic proof-of-stake slashing.** Unrelated to privacy but distinctive economically.

**NAM token.** Used for staking, governance, and shielded rewards. Genesis distribution was complex and phased.

**Status.** Mainnet live; MASP shielded pool is functional; IBC privacy bridge is the headline use case.

**Honest read.** Namada's MASP work is real cryptographic engineering and the IBC privacy story is a genuine niche. Adoption is bounded by Cosmos overall and by the operational complexity of using shielded balances.

## RailGun — privacy on existing EVMs

RailGun is the outlier in this list: not a new chain, but a smart-contract privacy system deployed on Ethereum, Polygon PoS, and BNB Chain. Deployed since 2021, with significant protocol upgrades through 2023-2024.

**State model.** Shielded UTXOs implemented as contract state. Each shielded balance is a note (encrypted commitment) tracked in a Merkle tree inside the RailGun contract. To shield, deposit ERC-20s and produce a note. To transfer privately, prove ownership of input notes and produce output notes with a SNARK. To unshield, prove a note's destruction and withdraw the underlying ERC-20.

**Proof system.** Groth16 over BN254 (Ethereum-friendly pairing curve). Per-circuit trusted setup; circuits are fixed (transfer, shield, unshield).

**No L2 required.** RailGun runs as a contract on each chain it deploys to. Withdrawals and deposits go to/from the host chain's account model. The trade-off is that gas costs are paid in the host chain's native token, which is significantly higher than in a dedicated shielded chain.

**RAIL token.** Governance and fee-relay incentives. Relayers process transactions on behalf of users to break the link between shielded operations and the user's gas-paying address.

**Status.** Live and used. The 0xPARC and RailGun communities have shipped wallet integrations (Railway Wallet) and have a small but real user base of EVM users wanting privacy without bridging to a new chain.

**Honest read.** The on-existing-EVMs design is the pragmatic choice: no bridge, no new validator set, no token launch friction. The trade-off is the OFAC-pressure surface — see [Tornado and Privacy Pools](/kb/tornado-and-privacy-pools/) for what happens when sanctions land on a smart-contract privacy pool. RailGun has tried to differentiate via private-balance abstractions but operates in the same regulatory shadow.

## Comparison

| Project | Layer | State model | Proof system | Setup | Asset model | Status (Q1 2026) |
|---------|-------|-------------|--------------|-------|-------------|------------------|
| **Aztec** | Ethereum L2 | Hybrid public + private | Halo2 / Honk | Universal/none | Multi-asset | Mainnet rollout |
| **Penumbra** | Cosmos L1 | Shielded UTXO + ZSwap | Groth16 (BLS12-377) | Per-circuit | Multi-asset | Mainnet (2024) |
| **Aleo** | Own L1 | Records + programs | snarkVM (Marlin/Halo2) | Universal | Multi-asset | Mainnet (2024) |
| **Iron Fish** | Own L1 | Sapling shielded UTXO | Groth16 (BLS12-381) | Per-circuit | Multi-asset + view keys | Mainnet (2023) |
| **Namada** | Cosmos L1 | MASP shielded UTXO | Groth16 | Per-circuit | Multi-asset (IBC) | Mainnet (2023) |
| **RailGun** | EVM contracts | Shielded UTXOs in contract | Groth16 (BN254) | Per-circuit | ERC-20s shielded | Live since 2021 |

## Cross-cutting notes

### Proof system choice

Five of six pick Groth16. The exception is Aztec, which needs a universal/recursion-friendly system because of its programmable model. Groth16 wins for fixed-circuit shielded payments on size and verifier cost; Halo2 wins when you need recursion or a wider circuit space. See [SNARKs](/kb/snarks/) for the trade-off in detail.

### Per-circuit trusted setup

Penumbra, Iron Fish, Namada, and RailGun all rely on per-circuit MPC ceremonies. Aztec uses a universal setup (powers-of-tau) for its Halo2 stack. Aleo's snarkVM uses a universal setup as well. The operational pain of per-circuit setups is one reason newer designs lean toward universal or transparent proof systems.

### Anonymity-set economics

A shielded pool is only as private as its anonymity set. RailGun on Ethereum competes with the legacy Tornado Cash anonymity sets (now sanctioned, see [Tornado and Privacy Pools](/kb/tornado-and-privacy-pools/)); Penumbra and Namada's anonymity sets are bounded by their own user counts. The shielding-incentive programs (Namada) try to grow the set artificially. This is a coordination problem more than a cryptographic one.

### Compliance posture

Iron Fish (viewing keys) and the Privacy Pools design (see [Tornado and Privacy Pools](/kb/tornado-and-privacy-pools/)) are two attempts at "privacy with selective disclosure". Penumbra and Aztec are largely silent on compliance; RailGun has tried to engineer relay-based privacy that doesn't require chain-level cooperation. None of these has produced a clean regulatory equilibrium yet.

## Where each fits

| If you want… | Use |
|--------------|-----|
| Programmable private contracts on Ethereum | Aztec when mainnet stabilizes |
| Shielded DEX with batch-clearing privacy | Penumbra |
| Custom shielded programs with dedicated infra | Aleo |
| Conservative Sapling-style shielded payments + view keys | Iron Fish |
| Privacy as an IBC service for Cosmos | Namada |
| Shielded balances on existing EVMs without bridging | RailGun |

## Trade-offs

### Strengths (across the field)

- Shielded UTXO + nullifier set is a battle-tested construction (Zcash since 2016).
- Multiple proof systems give designers real choice based on circuit shape.
- Some genuinely novel designs (ZSwap, Aztec hybrid state, MASP-on-IBC).

### Limitations (across the field)

- Each project's anonymity set is bounded by its own user count — fragmentation hurts privacy.
- Per-circuit trusted setups are operational debt.
- Compliance pressure is real (see [Tornado and Privacy Pools](/kb/tornado-and-privacy-pools/)); no project has produced an equilibrium.
- Wallet UX for shielded chains lags transparent chains by years.
- Multi-chain support means users have to pick which privacy island to live on.

## Primary sources

- Bowe, Chiesa, Green, Miers, Mishra, Wu, *ZEXE: Enabling Decentralized Private Computation*, IEEE S&P 2020.
- Hopwood, Bowe, Hornby, Wilcox, *Zcash Protocol Specification* (Sapling) — [zips.z.cash](https://zips.z.cash).
- Penumbra protocol docs — [protocol.penumbra.zone](https://protocol.penumbra.zone).
- Aleo Developer Docs — [developer.aleo.org](https://developer.aleo.org).
- Iron Fish whitepaper — [ironfish.network](https://ironfish.network).
- Namada specs — [specs.namada.net](https://specs.namada.net).
- Aztec Network docs — [docs.aztec.network](https://docs.aztec.network).
- Noir language docs — [noir-lang.org](https://noir-lang.org).
- RailGun docs — [docs.railgun.org](https://docs.railgun.org).
- MASP specification — [github.com/anoma/masp](https://github.com/anoma/masp).
