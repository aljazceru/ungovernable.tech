---
title: "Monero"
slug: monero
type: deep-dive
pillars: [money, cryptography]
readiness: battle-tested
description: "How Monero hides senders, receivers and amounts by default with ring signatures, stealth addresses and RingCT, where its privacy has limits, and how to use it well."
dek: "A cryptocurrency where privacy is the default for every transaction, not an option a few users turn on."
updated: 2026-10-17
created: 2026-10-17
origin: original
aliases: [XMR]
tags: [monero, privacy, ring-signatures, ringct]
related: [financial-sovereignty, bitcoin-self-custody, coinjoin, zero-knowledge-proofs, tornado-and-privacy-pools]
---

On Bitcoin, every transaction's sender address, receiver address and amount are public forever, and privacy has to be added by careful users. Monero (XMR), launched in 2014, takes the opposite approach: every transaction hides all three by default. Because everyone's transactions look alike, privacy does not depend on a few careful users hiding in a crowd of careless ones.

## How it hides what

| What is hidden | Mechanism | In short |
|---|---|---|
| **Sender** | Ring signatures (CLSAG) | Each input is signed on behalf of a "ring" of 16 possible outputs; observers cannot tell which one is really being spent. A *key image* prevents the same output being spent twice without revealing which it is. |
| **Receiver** | Stealth (one-time) addresses | The sender derives a fresh one-time address for every payment from the recipient's public address, so payments to the same person are unlinkable on-chain. |
| **Amount** | RingCT with Bulletproofs+ | Amounts are hidden in Pedersen commitments; short zero-knowledge range proofs (Bulletproofs+) show they are valid without revealing them. |
| **Network origin** | Dandelion++ | Transactions are passed along a random path before being broadcast, making it harder to link a transaction to the IP address that first sent it. |

Monero uses the **RandomX** proof-of-work algorithm (since 2019), designed to favour general-purpose CPUs over specialised mining hardware. Since mid-2022 a permanent **tail emission** of 0.6 XMR per block funds miners after the main emission ended.

A planned upgrade, **FCMP++** (full-chain membership proofs), would replace rings of 16 decoys with a zero-knowledge proof that the spent output is one of *all* outputs on the chain, removing the main statistical weakness described below.

## Where its privacy has limits

- **Decoy analysis.** With rings of 16, statistical techniques (for example, guessing that the newest output is the real one, or tracing outputs created by a known party) can sometimes raise the probability of identifying the real spend. Researchers have published such attacks against earlier, smaller rings; the protocol has repeatedly increased ring size and improved decoy selection in response.
- **Exchange records.** If you buy XMR on an exchange with identity verification, the exchange knows you bought it and where you withdrew it.
- **Timing and amounts at the edges.** Converting a precise amount into Monero and out again shortly after can be linked by the services at each end, even if the chain reveals nothing.
- **Network metadata.** Connecting to a remote node tells the node operator your IP address and when you transact. Run your own node, or connect over Tor or I2P.
- **Legal and market pressure.** Several large exchanges have delisted Monero or restricted it in some jurisdictions. Peer-to-peer markets and atomic swaps fill the gap.

## Using it well

1. **Wallets:** the official Monero GUI and CLI wallets (<https://www.getmonero.org/downloads/>); Feather Wallet for desktop; Cake Wallet and Monerujo for mobile. Verify downloads.
2. **Run your own node** if you can, or use a trusted node over Tor. The GUI wallet can run a node for you; a pruned node needs considerably less disk space.
3. **Back up the 25-word seed** offline, as with Bitcoin ([Bitcoin Self-Custody](/guides/bitcoin-self-custody/)).
4. **Acquire it privately:** peer-to-peer exchanges such as Haveno, in-person trades, or Bitcoin-to-Monero atomic swaps (for example eigenwallet, formerly UnstoppableSwap) avoid exchange KYC records.
5. **Use subaddresses** to give each counterparty a different receiving address.
6. **Do not rush round trips.** Moving funds in and out quickly with identical amounts undoes much of the benefit.

## Monero compared with other approaches

- **Bitcoin with CoinJoin or Payjoin** gives privacy that is optional, depends on coordination and on other users, and is visible as such on-chain ([CoinJoin and Payjoin](/kb/coinjoin/)).
- **Zcash** uses zk-SNARKs and offers a larger anonymity set for shielded transactions, but shielding is optional and many transactions remain transparent.
- **Ecash** (Cashu, Fedimint) gives strong payment privacy against the mint, but you trust the mint with custody ([Cashu and Chaumian Ecash](/kb/cashu-ecash/)).

## Sources

- The Monero Project: <https://www.getmonero.org/>; *Moneropedia* (ring signatures, stealth addresses, RingCT, Dandelion++, tail emission): <https://www.getmonero.org/resources/moneropedia/>
- Goodell, Noether and RandomRun, *Concise Linkable Ring Signatures and Forgery Against Adversarial Keys* (CLSAG), IACR ePrint 2019/654: <https://eprint.iacr.org/2019/654>
- Chung et al., *Bulletproofs+: Shorter Proofs for a Privacy-Enhanced Distributed Ledger*, IACR ePrint 2020/735: <https://eprint.iacr.org/2020/735>
- Fanti et al., *Dandelion++: Lightweight Cryptocurrency Networking with Formal Anonymity Guarantees* (2018): <https://arxiv.org/abs/1805.11060>
- Möser et al., *An Empirical Analysis of Traceability in the Monero Blockchain* (PETS 2018): <https://arxiv.org/abs/1704.04299>
- RandomX: <https://github.com/tevador/RandomX>
- FCMP++ research and development: <https://www.getmonero.org/2024/04/27/fcmps.html>

Continue with [Stablecoins and sovereignty](/kb/stablecoins-and-sovereignty/).
