---
title: "Tornado Cash and Privacy Pools"
slug: tornado-and-privacy-pools
type: deep-dive
pillars: ["zk", "money"]
readiness: cautionary
description: "Tornado Cash, Ethereum's zero-knowledge mixer, its sanctions and prosecutions, and Privacy Pools, the design that tries to separate illicit funds."
dek: "Tornado Cash was the canonical ZK mixer on Ethereum: fixed-denomination pools, deposit and withdraw decoupled by a Merkle inclusion proof. It was sanctioned by OFAC in August 2022 — the first time the U.S. Treasury sanctioned an autonomous smart contract — and its developers were criminally charged. Privacy Pools is the response: a 2023 Buterin-Soleimani-Chainalysis-coauthored proposal that adds opt-in association sets so honest users can prove they aren't drawing from sanctioned deposits while keeping their individual deposits private. The two together define the \"privacy with compliance\" debate."
updated: 2026-04-26
created: 2026-04-26
origin: vault
source: "09-Zero-Knowledge/Tornado and Privacy Pools.md"
aliases: ["Tornado Cash", "Privacy Pools", "0xbow"]
tags: ["zk", "privacy", "tornado-cash", "privacy-pools", "compliance", "sanctions", "deep-dive"]
---

## Tornado Cash — architecture

Tornado Cash was a smart-contract mixer on Ethereum (and later Polygon, BSC, Arbitrum, and others). Each *pool* held a single asset at a single denomination — for example, "100 DAI" or "10 ETH". A user:

1. **Deposits.** Picks a fresh secret + nullifier, computes a commitment `H(secret || nullifier)`, sends the deposit transaction with the commitment as input. The contract appends the commitment to a Merkle tree.
2. **Waits.** The longer between deposit and withdrawal, the larger the anonymity set (more commitments added in between).
3. **Withdraws.** Generates a Groth16 proof that "I know `secret`, `nullifier` such that `H(secret || nullifier)` is in the Merkle tree, and the nullifier hasn't been spent". Submits the withdrawal to a fresh address. The contract publishes the nullifier to prevent double-withdraw.

The deposit address and withdrawal address are unlinkable on-chain. The anonymity set is "everyone who deposited the same denomination and hasn't withdrawn yet".

Key implementation details:

- **Fixed denominations.** Required because variable amounts would leak the link.
- **Groth16 proof system** on BN254. See [SNARKs](/kb/snarks/) for the proof-system context.
- **Relayers.** A withdrawer who paid gas from their own address would burn the privacy. Relayers submitted withdrawals on the user's behalf and were paid out of the withdrawn amount.
- **Trusted setup.** Tornado Cash ran a multi-party setup ceremony in 2019.

Code repository: `tornadocash/tornado-core` (now archived, with multiple community forks).

## Sanctions and prosecutions

### August 2022 — OFAC SDN listing

On 8 August 2022, the U.S. Treasury Office of Foreign Assets Control added Tornado Cash to the Specially Designated Nationals (SDN) list, citing use by the Lazarus Group (DPRK-linked) to launder proceeds of cross-chain hacks. The novelty was that the listing covered specific Ethereum *contract addresses* — autonomous code, not a person or entity. U.S. persons were prohibited from interacting with the listed addresses.

Immediate effects:

- Circle froze USDC held by listed addresses.
- Infura, Alchemy, GitHub, and other infrastructure providers blocked or delisted Tornado Cash code and front ends.
- Some validators began censoring Tornado-Cash-related transactions.

### Roman Storm and Roman Semenov — criminal charges

In August 2023, the U.S. Department of Justice indicted Roman Storm and Roman Semenov on conspiracy to commit money laundering, sanctions violations, and operating an unlicensed money-transmitting business. Alexey Pertsev had been arrested in the Netherlands a year earlier and was convicted by a Dutch court in May 2024 (sentenced to 64 months; under appeal as of the cutoff).

Roman Storm's U.S. trial began in mid-2025; the case turned on whether a contract deployer remains responsible for autonomous code after deployment, and whether the front-end UI constitutes a money-transmitting business. The verdict and any sentencing are part of the live legal record at the cutoff and should be cross-checked against current reporting.

### November 2024 — Fifth Circuit ruling

In *Van Loon v. Department of the Treasury* (Fifth Circuit, November 2024), the court ruled that immutable smart contracts are not "property" within the meaning of the IEEPA statute that authorizes OFAC to sanction property of foreign persons. The Treasury subsequently rescinded the SDN designations against the specific contract addresses in March 2025, while continuing to assert sanctions authority over individuals associated with the project. The ruling did not legalize use of the contracts retroactively for prior periods and did not absolve the developers.

Net effect: the autonomous-contract sanction precedent is weakened; the developer-criminal-liability question is ongoing.

## What Tornado got right and wrong

### Right

- Crisp construction. Fixed-denomination pools + Merkle inclusion + nullifier is the textbook ZK mixer.
- Real anonymity-set growth. By 2022, the 100 ETH and 10 ETH pools held tens of thousands of deposits.
- Open source, audited, immutable post-deployment.

### Wrong (or at least: didn't account for)

- **No compliance hooks.** Mixed deposits indiscriminately — there was no way for an honest user to demonstrate "I'm not withdrawing Lazarus's deposit."
- **Front-end as a single point of compliance failure.** The dApp UI was operated centrally; once it went down, users had to interact directly with the contract.
- **Relayers as a compliance choke point.** Relayers needed to know they weren't proxying sanctioned deposits, but had no cryptographic way to check.
- **Token + governance + fee structure created an "operating an enterprise" surface** that prosecutors could use against developers.

These gaps motivated the Privacy Pools design.

## Privacy Pools — the proposal

In September 2023, Vitalik Buterin, Jacob Illum (Chainalysis), Matthias Nadler (University of Basel), Fabian Schär (University of Basel), and Ameen Soleimani co-authored *"Blockchain Privacy and Regulatory Compliance: Towards a Practical Equilibrium"* (SSRN, 2023). The paper proposes adding an *association set proof* on top of a Tornado-style shielded pool.

### Construction

- Same shielded pool as Tornado: deposits make commitments, withdrawals prove Merkle membership + nullifier.
- **Additional public statement.** The withdrawer also proves that their deposit is in some *association set* — a publicly defined subset of the deposit set.
- **Association sets are user-chosen.** A user picks the association set that fits their use case: "deposits not flagged by any major chain analytics provider," "deposits known to be from KYC'd exchanges," etc.
- The proof is symmetric — a user can equivalently prove *non-membership* in a "bad" set (sanctioned deposits, known-stolen funds).

The cryptographic addition is small: an extra Merkle inclusion proof, with a different root, in the same SNARK.

### Game-theoretic argument

The paper's central claim is a separating equilibrium:

- **Honest users** pick the strictest reasonable association set (proves their deposit is not flagged) and accept a slightly smaller anonymity set in exchange for clear compliance.
- **Illicit users** can only join association sets that don't filter them out, and these sets become small and obviously suspicious.

The result is a pool where the anonymity set is large enough for honest users while bad actors cluster into visibly small subsets. Whether this works in practice depends on how association set providers (ASPs) operate, what data they use, and how they govern membership.

### Association Set Providers

ASPs are the trust assumption. An ASP publishes a Merkle root (or roots) committing to a list of "approved" deposits, often based on chain-analytics screening. Users prove membership in an ASP's set when withdrawing. ASPs themselves can be public, multiple, and competing — a user picks the one whose policy they accept.

ASPs are a centralization vector. The cryptographic privacy holds, but an ASP that screens too aggressively (excluding legitimate users) or too laxly (admitting sanctioned funds) breaks the equilibrium.

## Privacy Pools v1 — deployment

### 0xbow — the first production deployment

0xbow.io launched a Privacy Pools deployment on Ethereum mainnet in early 2024 (with the Privacy Pools contract code at `privacy-pools-core/contracts`). Features:

- ETH-denominated pools (initially), later additional asset support.
- Default ASP screening based on multiple chain-analytics signals.
- Public ratification process for the ASP root.
- Open-source contracts and circuits.

User experience: similar to Tornado — fixed-denomination shielded deposits — but withdrawal includes the ASP membership proof. Front end and ASP governance are operated by 0xbow with community ratification of association set updates.

### Status (early 2026)

Privacy Pools deployments are live but adoption is small relative to Tornado at its 2022 peak. The compliance-aware design has not (so far) attracted large-scale honest-user demand at the level of pre-sanctions Tornado, in part because:

- Anonymity set is bounded by the pool's own usage.
- The compliance ratification process adds operational complexity.
- Many former Tornado users migrated to other privacy strategies (CEX off-ramps, alternative L2s, [ZK Privacy Applications](/kb/zk-privacy-applications/) like RailGun or Aztec).

## Trade-offs

### Tornado-style mixers

| Strength | Weakness |
|----------|----------|
| Maximally simple cryptography | No compliance hook |
| Large anonymity sets at scale | Mixes good and bad indiscriminately |
| Fully autonomous | Developers in legal jeopardy |

### Privacy Pools (Buterin et al.)

| Strength | Weakness |
|----------|----------|
| Compliance-friendly via ASP proofs | ASP is a centralization point |
| User picks their own association set | Smaller anonymity set than indiscriminate pool |
| Cryptography is a small addition to Tornado-style design | Game-theoretic separation depends on ASP behavior |
| Reduces developer legal exposure (arguably) | Has not (yet) achieved Tornado-scale adoption |

## What this means for designers

A privacy-pool designer in 2026 picks among:

1. **Tornado-style indiscriminate pool.** Maximum simplicity, maximum legal exposure.
2. **Privacy Pools with ASP.** Adds an ASP layer; reduces legal exposure but introduces an oracle.
3. **Built-in selective disclosure** (Iron Fish viewing keys, see [ZK Privacy Applications](/kb/zk-privacy-applications/)).
4. **Privacy at a different layer entirely** (shielded chain like Penumbra; [Confidential-AI-Inference](/kb/confidential-ai-inference/) for compute; CoinJoin for Bitcoin).

There is no "right" answer; the trade-off is between privacy maximalism and the operational reality of running a smart contract that U.S. persons can use without breaking laws.

## Anonymity-set economics

A privacy pool's privacy is its anonymity set size. The math:

- If `n` deposits are in the pool when you withdraw, your withdrawal is unlinkable to one of `n` deposits.
- Adding an association-set constraint reduces the *effective* anonymity set to those deposits also in your chosen ASP.
- An aggressive ASP that admits 90% of deposits leaves 0.9n; a strict ASP at 50% leaves n/2; at 10%, n/10.

For Privacy Pools to deliver real privacy, the pool needs both *volume* (large `n`) and a *reasonable ASP* (large surviving fraction). Both scale together with adoption — a chicken-and-egg problem.

## Cross-cutting

- **Mixers vs. shielded chains.** A mixer (Tornado, Privacy Pools, RailGun) sits on top of a transparent chain; a shielded chain (Zcash, Penumbra, Iron Fish, Namada) makes privacy the default. Different anonymity-set economics, different compliance surfaces.
- **CoinJoin vs. ZK mixers.** CoinJoin (see [CoinJoin Implementation](/kb/coinjoin/)) provides Bitcoin-side mixing without ZK proofs; the trust and unlinkability properties differ.
- **Selective disclosure.** Viewing keys (Iron Fish, Zcash) and ASP proofs (Privacy Pools) are two structurally different solutions to "prove I'm not the bad actor."

## Primary sources

- Pertsev, Storm, Semenov, *Tornado Cash whitepaper*, 2019 — [github.com/tornadocash/docs](https://github.com/tornadocash/docs).
- U.S. Treasury OFAC press release, "U.S. Treasury Sanctions Notorious Virtual Currency Mixer Tornado Cash", 8 August 2022.
- Buterin, Illum, Nadler, Schär, Soleimani, *Blockchain Privacy and Regulatory Compliance: Towards a Practical Equilibrium*, SSRN 4563364, September 2023.
- *Van Loon v. Department of the Treasury*, U.S. Court of Appeals for the Fifth Circuit, No. 23-50669, 26 November 2024.
- 0xbow Privacy Pools — [0xbow.io](https://0xbow.io); contracts at [github.com/0xbow-io](https://github.com/0xbow-io).
- DOJ indictment, *United States v. Roman Storm and Roman Semenov*, S.D.N.Y., August 2023.
- Dutch court ruling, *State v. Pertsev*, 's-Hertogenbosch, May 2024.
