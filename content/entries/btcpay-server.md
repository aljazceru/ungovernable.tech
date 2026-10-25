---
title: "BTCPay Server"
slug: btcpay-server
type: deep-dive
pillars: [money]
readiness: usable
description: "BTCPay Server accepts Bitcoin payments into your wallet. Learn how xpub invoices, self-hosting and Lightning change custody and operational trust."
dek: "Run your own payment processor, generate invoices and receive bitcoin directly into the wallet you choose."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [bitcoin-self-custody, lightning-network, silent-payments, coinjoin, fedimint]
tags: [btcpay-server, bitcoin, payments, self-hosting, lightning]
---

## Summary

BTCPay Server is an open-source payment processor that you can host yourself. It generates invoices and receives payments directly into a connected wallet. With your own server, node and wallet, there is no separate payment-processing company holding the incoming bitcoin or approving the payment. Running that infrastructure becomes your responsibility.

## How it works

**On-chain invoices.** Connect a wallet through an extended public key, or **xpub**, and its derivation scheme. BTCPay can generate receiving addresses without obtaining the wallet's spending keys. It generates a fresh address for each invoice and tracks the corresponding payments using its node infrastructure.

**Spending.** Receiving through an xpub does not require keeping private keys on the server. An external wallet or hardware signer can retain spending authority. BTCPay also offers hot-wallet configurations; those put different responsibilities on the server.

**Lightning.** BTCPay can use an internal or external Lightning node, including LND or Core Lightning. Operating your own node means managing channels and receiving liquidity. Custodial Lightning integrations are also documented, but their custody belongs to the selected service.

**Applications.** Invoicing, point-of-sale, donation and crowdfunding interfaces give the processor practical uses without building a checkout from scratch.

## Trust model / threat model

An xpub separates receiving from spending. It does not make a compromised payment server harmless. The [hosting documentation](https://docs.btcpayserver.org/Deployment/ThirdPartyHosting/) describes an attacker replacing the configured xpub and redirecting future payments. Protect the server and check that invoices pay addresses belonging to your wallet.

Hosting on someone else's BTCPay instance also introduces that operator. A malicious host can observe activity or change the software. A hot wallet on their server, or payments to their shared Lightning node, additionally introduces custody. The claim of no payment intermediary applies to the infrastructure and wallet you actually control.

## Readiness

**Usable.** BTCPay provides documented wallet connections, Lightning integrations and payment applications. It suits merchants and organisations prepared to operate a server and maintain their payment setup. Start with [Bitcoin self-custody](/guides/bitcoin-self-custody/) if wallet backups and signing are still unfamiliar.

## Limits

- **Public-chain privacy.** Self-hosting does not hide on-chain payment amounts or history.
- **Address discovery.** An external wallet's address gap limit can make payments appear missing after many unpaid invoices. BTCPay's wallet FAQ explains the recovery and configuration issue.
- **Lightning operations.** Receiving capacity, channel management and the selected wallet's custody model still matter.
- **Deployment trust.** A hosted instance and a server under your control have different security boundaries.

For a reusable donation address without an invoice server, compare [Silent Payments](/kb/silent-payments/), including its scanning cost. For transaction privacy, see [CoinJoin and Payjoin](/kb/coinjoin/).

## Primary sources

- [BTCPay Server: payment processor and built-in applications](https://btcpayserver.org/).
- [Wallet FAQ: xpubs, derivation schemes, invoice addresses and gap limits](https://docs.btcpayserver.org/FAQ/Wallet/).
- [Lightning integration: node choices, custody and liquidity](https://docs.btcpayserver.org/LightningNetwork/).
- [Hosting security: xpub replacement, hot wallets and operator trust](https://docs.btcpayserver.org/Deployment/ThirdPartyHosting/).
