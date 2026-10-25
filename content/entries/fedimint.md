---
title: "Fedimint"
slug: fedimint
type: deep-dive
pillars: [money, cryptography]
readiness: usable
description: "Fedimint combines federated Bitcoin custody with Chaumian ecash. Learn what guardians control, how Lightning gateways work and what users trust."
dek: "Private ecash backed by bitcoin held by a group of guardians: shared custody, with an explicit trust boundary."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [cashu-ecash, lightning-network, threshold-signatures, bitcoin-self-custody, btcpay-server]
tags: [fedimint, ecash, federation, bitcoin, lightning]
---

## Summary

Fedimint is a federated Chaumian ecash system. Users deposit bitcoin and receive notes that can be transferred and redeemed through a mint operated by **guardians**. Blind signatures prevent the mint from directly linking an issued note to its later redemption. The bitcoin backing those notes is in federation custody: the user's ecash is a claim on that custody, not an independently controlled on-chain output.

## How it works

**Guardians.** The federation runs consensus and jointly operates the mint. Bitcoin reserves sit in a threshold multisignature wallet: enough guardians must cooperate to move them. The documented examples include a three-of-four custody threshold. Ecash uses threshold blind signatures, so issuance is also shared across guardians.

**Notes.** A wallet obtains blinded signatures and holds the resulting ecash. Blinding separates the mint's act of signing from recognition of the resulting note when it returns. This is the same broad privacy idea described in [Cashu and Chaumian Ecash](/kb/cashu-ecash/).

**Lightning gateways.** A gateway exchanges ecash for payments on the [Lightning Network](/kb/lightning-network/). It need not be a guardian, and a federation can have multiple gateways. For an outgoing payment, a contract releases ecash to the gateway when it supplies the payment preimage. Incoming payments use a corresponding contract to exchange the preimage for ecash. The [architecture documentation](https://fedimint.org/guardians/how-federations-work) describes these as atomic payment contracts.

## Trust model / threat model

The guardians are the custodians. A sufficient colluding group can take the bitcoin, and users also trust the federation not to issue unbacked ecash. Too few available guardians can stop service. Threshold custody removes unilateral control by one guardian in a multi-guardian configuration; it does not give users unilateral withdrawal rights.

Gateway contracts constrain payment theft, but a usable gateway still needs connectivity and liquidity to complete payments. Choosing among gateways does not remove the underlying trust in the federation.

Blinding protects the issuance-to-redemption link. It should not be read as a guarantee that deposits, withdrawals, Lightning interactions or network connections reveal nothing. Custody privacy and custody safety are separate properties.

## Fedimint beside Cashu

| Question | Fedimint | Cashu |
|---|---|---|
| What does a user hold? | Ecash redeemable at a federation | Ecash redeemable at the issuing mint |
| What provides payment privacy? | Threshold blind signatures | Blind signatures |
| Where is the custody decision? | The guardian group and its threshold | The chosen mint and its custody arrangements |
| What must be checked? | Guardians, availability, backing and wallet compatibility | Mint operator, availability, backing and wallet compatibility |

Cashu specifies a mint-and-wallet protocol; it does not automatically provide Fedimint's guardian consensus. Neither design turns an ecash balance into [Bitcoin self-custody](/guides/bitcoin-self-custody/).

## Readiness

**Usable.** Fedimint publishes server software and an official wallet directory, including Fedi and other clients. Their supported modules differ, so check compatibility with the chosen federation. Running the federation also requires guardian coordination and recovery planning.

## Limits

Federation selection is part of the security decision. More guardians do not help if they share the same failure or coercion risk. Treat a federation balance as money exposed to that group's custody, and test redemption before relying on it for regular payments.

For accepting payments into your own wallet instead, see [BTCPay Server](/kb/btcpay-server/).

## Primary sources

- [Fedimint project: deposits, ecash and payments](https://fedimint.org/).
- [How federations work: custody, consensus and Lightning gateways](https://fedimint.org/guardians/how-federations-work).
- [Privacy and trust: collusion and unbacked issuance](https://fedimint.org/users/privacy-and-trust).
- [Fedimint source repository and cryptographic documentation](https://github.com/fedimint/fedimint).
- [Official wallet directory and supported modules](https://fedimint.org/wallets).
- [Cashu protocol overview: mint claims, wallets and blind signatures](https://cashu.space/).
