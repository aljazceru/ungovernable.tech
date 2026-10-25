---
title: "Silent Payments (BIP 352)"
slug: silent-payments
type: explainer
pillars: [money]
readiness: usable
description: "Silent Payments give Bitcoin a reusable payment address without on-chain address reuse. BIP 352's privacy, scanning costs and confirmed wallet support."
dek: "Publish one address, receive to fresh Taproot outputs, and pay for that convenience with wallet scanning."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [bitcoin-self-custody, coinjoin, btcpay-server, zcash, hardware-wallets]
tags: [bitcoin, silent-payments, bip352, privacy, wallets]
---

## Summary

Silent Payments, specified in **BIP 352**, let a recipient publish a static Bitcoin payment address while receiving each payment at a different on-chain output. Sender and receiver do not need to interact to exchange a fresh address, and there is no separate notification transaction. The trade-off is that the receiving wallet must scan for its payments.

## How it works

A Silent Payment address contains a public **scan key** and a public **spend key**. The sender combines its eligible transaction-input keys with the recipient's scan key to derive a shared secret, then derives a fresh Taproot output using the spend key. Transaction-specific input data prevents repeated use of the same sender key from producing the same destination.

The receiver repeats the calculation using its private scan key and public input data. When the derived output matches an output in the transaction, it has found a payment. The private spend key is needed to spend that output; scanning and spending can be separated.

An observer cannot derive the link from the published Silent Payment address to its on-chain outputs. The outputs have the normal Taproot form, without a dedicated on-chain notification identifying the payment scheme.

## Trust model / threat model

This addresses public address reuse. It does not conceal Bitcoin transaction amounts, hide the sender's existing input history or prevent a sender from knowing the payment it made. Labels derived from the same scan key are linkable as published addresses, so BIP 352 explicitly warns against treating them as separate identities.

The wallet must implement both the output derivation and scanning correctly. BIP 352 also cautions that there is no formal security proof for collaborative input construction and recommends that the input keys belong to the same entity. Do not assume every [CoinJoin](/kb/coinjoin/) or multisignature workflow composes safely with it.

## Scanning and recovery

The recipient checks eligible transactions rather than querying one fixed receiving address. This costs computation and data. BIP 352 discusses indexes and filters for lighter clients, while describing light-client support as an area of ongoing research.

A backup can recover payments by rescanning; a wallet's creation date and saved label information help constrain that work. An old wallet that has not implemented BIP 352 cannot send to the new address format.

## Readiness

**Usable with compatible software.** [Cake Wallet's documentation](https://docs.cakewallet.com/features/privacy-and-security/silent-payments) confirms both sending and receiving, with scanning enabled for receipt. It also documents a practical privacy boundary: scanning uses the selected node only if it serves the required tweak data; otherwise it falls back to Cake Wallet's server without changing the wallet's node setting.

## Limits

Scanning takes time, data and battery. A payment may remain undiscovered until scanning catches up. Receiving support, sending support and the data source used for scanning are separate things to check before relying on a wallet.

For an invoice-based payment setup, see [BTCPay Server](/kb/btcpay-server/). For key management and recovery, start with [Bitcoin self-custody](/guides/bitcoin-self-custody/).

## Primary sources

- [BIP 352: protocol, privacy goals, scanning, backups and compatibility](https://github.com/bitcoin/bips/blob/master/bip-0352.mediawiki).
- [BIP 352 reference implementation](https://github.com/bitcoin/bips/blob/master/bip-0352/reference.py).
- [Cake Wallet: sending, receiving, scanning and server fallback](https://docs.cakewallet.com/features/privacy-and-security/silent-payments).
