---
title: "RoboSats"
slug: robosats
type: deep-dive
pillars: [money, anonymity]
readiness: usable
description: "RoboSats trades bitcoin over Lightning and Tor using hold invoices and temporary identities. Understand coordinator custody, bonds and fiat privacy."
dek: "Lightning-based peer-to-peer exchange with temporary robot identities and a coordinator whose trust boundary still matters."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [lightning-network, bisq, compare-p2p-bitcoin-acquisition, bitcoin-self-custody, tor]
tags: [robosats, lightning, bitcoin, tor, peer-to-peer]
---

## Summary

RoboSats matches people buying and selling bitcoin for national currencies. Traders connect over Tor, use temporary **robot identities**, and lock Lightning hold invoices as bonds and trade escrow. The fiat payment moves directly between the traders. A coordinator handles the order, invoices, payout and disputes.

## How it works

**Identity.** A private random token generates a robot avatar and lets its owner recover an ongoing trade. No email or phone registration is needed. Save the token until the trade and any dispute are complete, then use a fresh identity for the next trade. Reusing a robot links its orders.

**Bonds.** Both traders lock small hold invoices. These can be charged for breaking the trade rules or losing a dispute; otherwise they are released.

**Trade escrow.** The seller locks the traded bitcoin in a separate hold invoice. Unlike a normal invoice, a hold invoice can remain pending until its receiver settles or cancels it. The sender cannot revoke that pending payment at will. Once the seller confirms receipt of fiat, the coordinator settles the escrow and pays the buyer's Lightning invoice.

**Chat.** The trading conversation uses end-to-end PGP encryption. The payment method still determines which personal details the counterparty needs to see.

## Trust model / threat model

Hold invoices reduce the time spent in custody. They do **not** make settlement between seller, coordinator and buyer an atomic exchange. The [escrow documentation](https://learn.robosats.org/docs/escrow/) explicitly says the coordinator holds the funds while trying to pay the buyer after settling the seller's invoice. A dishonest coordinator can therefore harm users; a failed payout can also leave funds awaiting resolution.

The coordinator decides disputes and controls invoice settlement. Tor and encrypted chat do not remove this trust or identity disclosure from the fiat rail.

## What the federation means

RoboSats documents a federation of independent coordinators and a shared client that combines their order listings. Each coordinator runs its own backend and Lightning infrastructure and resolves its own users' disputes. This is a choice of service operators, not the threshold custody of a [Fedimint](/kb/fedimint/) federation. Choosing a coordinator is a custody and availability decision for that trade.

## Readiness

**Usable, with coordinator risk.** The project publishes clients and coordinator software and documents the trading flow. A working trade needs compatible Lightning invoice handling, payment liquidity and a responsive coordinator. Test the wallet and coordinator with an amount whose temporary loss of access you can tolerate.

## Limits

Robot tokens must be kept secret and recoverable. Orders, bonds and pending invoices have deadlines; a trading session needs attention. Fresh identities help separate trades inside RoboSats, but reusing the same bank account can reconnect them outside it.

Compare [Bisq](/kb/bisq/) and [other P2P acquisition routes](/kb/compare-p2p-bitcoin-acquisition/). For the payment layer underneath, see [Lightning Network](/kb/lightning-network/).

## Primary sources

- [RoboSats repository: trade flow, tokens, bonds and clients](https://github.com/RoboSats/robosats).
- [RoboSats privacy model: Tor, identities and encrypted chat](https://learn.robosats.org/docs/private/).
- [Trade escrow and hold-invoice custody](https://learn.robosats.org/docs/escrow/).
- [Federation specification: coordinator roles and trust](https://github.com/RoboSats/robosats/blob/main/federation.md).
