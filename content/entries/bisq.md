---
title: "Bisq"
slug: bisq
type: deep-dive
pillars: [money, anonymity]
readiness: usable
description: "Bisq exchanges bitcoin peer to peer over Tor. Compare its multisig escrow and dispute process with the seller-reputation model of Bisq Easy."
dek: "A peer-to-peer market over Tor, with different security assumptions for multisig trades and Bisq Easy."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [compare-p2p-bitcoin-acquisition, robosats, bitcoin-self-custody, tor, coinjoin]
tags: [bisq, bitcoin, peer-to-peer, multisig, tor]
---

## Summary

Bisq is software for exchanging bitcoin directly with other people over Tor. Its established multisig trading protocol locks bitcoin and security deposits while the buyer pays the seller through an agreed external payment method. It has no central exchange account or centralized identity-verification requirement. The fiat payment still takes place outside the protocol and can identify the traders to each other and their payment providers.

## How it works

**Peer-to-peer discovery.** Bisq applications communicate through Tor onion services. Users choose offers themselves; Bisq coordinates the trade without integrating directly with the banks moving the fiat payment.

**Multisig escrow.** In the Bisq multisig protocol, the seller's bitcoin and both traders' security deposits are locked in a **two-of-two multisignature output**. After the buyer sends the agreed payment and the seller confirms receipt, the traders cooperate to settle the bitcoin and return deposits.

**Disputes.** Trader chat is the first step, followed by mediation and then arbitration. A mediator proposes a settlement but has no escrow key, so both traders must accept the proposal. Arbitration is a separate escalation and reimbursement process involving the trade's delayed payout transaction; an arbitrator cannot simply sign the original two-of-two escrow to either trader. The [trading rules](https://docs.bisq.network/trading-rules.html) describe the process and the payment evidence it can require.

## Bisq 2 and Bisq Easy

The [Bisq 2 repository](https://github.com/bisq-network/bisq2) documents **Bisq Easy**, a chat-based trading protocol aimed at people who do not already hold bitcoin. Its security rests on the seller's reputation. Do not assume that a Bisq Easy trade has the multisig escrow and bitcoin security deposits described above: it is a different trade protocol.

## Trust model / threat model

Multisig prevents either trader from spending the escrow alone. Deposits discourage misconduct, but cannot cryptographically prove that a bank transfer arrived or will remain final. Disputed fiat payments depend on evidence, human decisions and the reimbursement process.

Tor protects the network connection; it does not hide names or account details carried by a payment rail. Disputes can require disclosure of payment records. Face-to-face cash removes the bank transfer but introduces physical risk and payment disputes that can be difficult to prove.

Bisq Easy adds a direct trust decision about the seller's reputation. Evaluate that separately from the security of the Tor connection or the Bisq software itself.

## Readiness

**Usable.** Bisq provides downloadable desktop software, and Bisq 2 has its own software and trading model. Choose the protocol deliberately. Multisig trading requires bitcoin for deposits and fees; Bisq Easy is designed to remove that initial-bitcoin requirement for buyers.

## Limits

Trades depend on a matching counterparty, the agreed payment method and completion of the dispute process when something goes wrong. They are not instant exchange-account purchases. No platform identity check does not mean no identity disclosure.

Compare [RoboSats](/kb/robosats/) and the wider [P2P acquisition comparison](/kb/compare-p2p-bitcoin-acquisition/), then follow [Bitcoin self-custody](/guides/bitcoin-self-custody/) for holding the result.

## Primary sources

- [Bisq project and downloads](https://bisq.network/).
- [Bisq introduction: Tor, multisig, deposits and privacy](https://docs.bisq.network/intro.html).
- [Bisq trading rules: mediation, arbitration and payment risks](https://docs.bisq.network/trading-rules.html).
- [Bisq 2 repository: Bisq Easy and seller reputation](https://github.com/bisq-network/bisq2).
