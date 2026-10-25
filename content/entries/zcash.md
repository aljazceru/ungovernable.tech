---
title: "Zcash"
slug: zcash
type: deep-dive
pillars: [money, zk]
readiness: usable
description: "Zcash supports transparent and shielded payments. Understand its privacy pools, Orchard's Halo 2 proofs, viewing keys and wallet limits."
dek: "Shielded payments hide financial details on the chain, but transparent transfers and movement between pools still reveal information."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [monero, zero-knowledge-proofs, coinjoin, silent-payments, financial-sovereignty]
tags: [zcash, shielded-payments, orchard, halo2, financial-privacy]
---

## Summary

Zcash supports both public and shielded transfers of ZEC. In a fully shielded transfer within one pool, observers cannot read the sender, recipient or payment amount from the chain. Zero-knowledge proofs establish that the spend is valid without publishing those details. Transparent transfers expose financial information much like Bitcoin transactions. Privacy depends on the transaction actually being shielded, not just on using Zcash.

## How it works

Shielded value is represented by **notes**. The chain records commitments to notes, and a spend reveals a **nullifier** that prevents the same note being spent twice. The proof connects a valid note to its spend without exposing which earlier commitment it belongs to.

The [protocol specification](https://zips.z.cash/protocol/protocol.pdf) defines three shielded pools. They hold the same currency, but have separate notes and transaction rules.

| Pool | Construction | Setup assumption |
|---|---|---|
| Sprout | The original shielded protocol, using JoinSplit transfers | Trusted parameters; its proving system was subsequently changed to Groth16 |
| Sapling | Separate shielded spend and output descriptions, proved with Groth16 | Trusted parameters |
| Orchard | Actions combine a spend and an output; Halo 2 proves the bundle | No trusted setup |

[ZIP 224](https://zips.z.cash/zip-0224) explains the distinction: Sprout and Sapling rely on parameter ceremonies whose hidden secrets must not survive. Orchard's Halo 2 construction removes that requirement. It does not remove the need for correct cryptography, wallet software and consensus validation.

**Addresses.** Transparent addresses expose their activity publicly. Shielded addresses receive encrypted notes. A **Unified Address**, defined by [ZIP 316](https://zips.z.cash/zip-0316), can package Orchard, Sapling and transparent receivers together. The sender chooses the most preferred receiver it supports from that address. Check which receiver the wallet actually uses; a Unified Address does not make every possible payment fully shielded.

**Viewing keys.** An incoming viewing key reveals incoming payments within its scope. A full viewing key can reveal incoming and outgoing notes without granting spending authority. Unified viewing keys package the corresponding capabilities across supported receiver types. Sharing one is a financial disclosure, even though it does not hand over the spending key.

## Trust model / threat model

Shielding protects against observers reading payment details directly from the public ledger. The protocol still depends on proof soundness, consensus and the security of the spending keys. A counterparty knows the payment it participates in; a viewing-key holder can see the information that key exposes.

The important boundary is the **pool**. Moving value into or out of a shielded pool reveals the transferred amount, including movement between shielded pools. The protocol specification also cautions that public transaction structure and timing can support probabilistic links. Shielding is not a promise that every surrounding interaction is anonymous.

## Readiness

**Usable.** The shielded protocols are deployed, and wallet support exists. The official ecosystem lists [Zodl, formerly Zashi](https://z.cash/ecosystem/zodl-wallet/), as a self-custodial wallet with shielding by default. Wallet selection still matters: verify the destination's supported receiver and the pool used for each payment.

## Limits

- **Transparent activity stays public.** A shielded leg does not conceal a transparent input or output in the same transaction.
- **Pool boundaries expose amounts.** Sapling-to-Orchard movement is not equivalent to a payment entirely inside Orchard.
- **Some transaction data remains public.** Fees, commitments, nullifiers and transaction structure are not hidden balances or addresses, but they are observable data.
- **Disclosure has consequences.** Protect viewing keys as well as spending keys; they grant different powers.

Compare [Monero](/kb/monero/) and [CoinJoin](/kb/coinjoin/) for other payment-privacy designs, and [Silent Payments](/kb/silent-payments/) for reusable Bitcoin addresses.

## Primary sources

- [Zcash: shielded and transparent payments](https://z.cash/learn/what-is-the-difference-between-shielded-and-transparent-zcash/).
- [Zcash protocol specification: pools, notes, proofs, viewing keys and transaction fields](https://zips.z.cash/protocol/protocol.pdf).
- [ZIP 224: Orchard shielded protocol and setup assumptions](https://zips.z.cash/zip-0224).
- [ZIP 316: Unified Addresses and viewing keys](https://zips.z.cash/zip-0316).
- [Zodl, formerly Zashi: official ecosystem listing](https://z.cash/ecosystem/zodl-wallet/).
