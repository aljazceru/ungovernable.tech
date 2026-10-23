---
title: "Bitcoin Self-Custody, Step by Step"
slug: bitcoin-self-custody
type: guide
pillars: [money, endpoint]
description: "How to hold bitcoin that nobody can freeze: a hardware signer, your own node, a tested seed backup, multisig for larger amounts, and habits that protect privacy."
dek: "Not your keys, not your coins. Holding your own keys is simple; holding them safely, privately and recoverably takes a plan."
updated: 2026-10-17
created: 2026-10-17
origin: original
level: intermediate
time: "2-4 hours"
related: [hardware-wallets, financial-sovereignty, coinjoin, lightning-network, cashu-ecash, threshold-signatures, monero]
---

Money held by an exchange or bank can be frozen, seized, inflated away or lost when the custodian fails. Bitcoin lets you hold value as a secret only you know. The cost of that freedom is responsibility: there is no support desk, and a lost or stolen key is final. This guide walks through a setup that balances security, privacy and recoverability. For the background, read [Financial Sovereignty](/kb/financial-sovereignty/) and [Hardware Wallets](/kb/hardware-wallets/).

## 1. Decide how much security you need

| Amount at stake | Reasonable setup |
|---|---|
| Spending money | A reputable open-source mobile wallet, or Lightning ([Lightning Network](/kb/lightning-network/)) |
| Savings you would hate to lose | A hardware signer with a metal seed backup and a passphrase, used with your own node |
| Savings that would change your life | Multisig: 2-of-3 keys on different hardware, stored in different places |

## 2. Get a hardware signer

A hardware signer (hardware wallet) keeps the private keys on a dedicated device and shows you what you are signing on its own screen, so malware on your computer cannot steal keys or silently change the destination. Prefer devices with open-source firmware and a good security track record; buy directly from the manufacturer; check the tamper evidence; and set it up yourself, never with a seed someone else gave you. Air-gapped devices that sign via QR code or microSD (including the DIY SeedSigner) avoid USB connections entirely. The trade-offs are covered in [Hardware Wallets](/kb/hardware-wallets/).

## 3. Back up the seed properly

The device generates a 12- or 24-word recovery phrase (BIP-39). Anyone with those words has your money.

- Write it down **on paper first, then on metal** (stamped or engraved steel survives fire and water). Never photograph it, type it into a computer or store it in the cloud.
- Consider a **passphrase** (sometimes called the 25th word). It creates a different wallet from the same seed, so a found seed alone is useless. The passphrase must be backed up separately; lose it and the funds are gone.
- **Test recovery** before sending real money: wipe the device (or use a second one), restore from your backup, and check that you get the same addresses.
- Plan for **inheritance**: write instructions someone you trust could follow, without giving them access today.

## 4. Run your own node

A wallet that queries someone else's server tells that server which addresses are yours. Running your own full node means you verify the rules yourself and keep your balance private.

- **Bitcoin Core** (<https://bitcoincore.org/>) is the reference implementation.
- Packaged node systems such as Umbrel, Start9 (StartOS) and RaspiBlitz bundle a node with an Electrum server and a web interface on a small dedicated computer.
- Connect your node over **Tor** so your IP address is not linked to it.

Pair it with desktop wallet software such as **Sparrow** (<https://sparrowwallet.com/>), which works with hardware signers, supports coin control and multisig, and can connect to your own node.

## 5. For larger amounts, use multisig

In a 2-of-3 multisig wallet, any two of three keys can spend. One key can be lost, stolen or destroyed without losing funds, and a single seized or coerced key is not enough. Use signers from **different manufacturers** and store them in **different places**. Back up the **wallet descriptor** (the description of which keys make up the wallet) as well as each seed: without it, recovery is much harder. Partially signed Bitcoin transactions (PSBT, BIP-174) let the signers co-sign without ever being connected to each other.

## 6. Protect your privacy

The Bitcoin blockchain is public and permanent. Chain analysis companies link addresses into clusters and clusters to identities, often starting from exchange KYC records.

- **Never reuse addresses.** Your wallet generates a new one for each payment.
- **Use coin control and labels.** Know where each coin came from; do not merge coins from a KYC exchange with coins from private sources in one transaction.
- **Payjoin** (BIP-78, and asynchronous BIP-77) breaks the common assumption that all inputs belong to the sender. **Silent Payments** (BIP-352) give you a reusable static address without address reuse on-chain.
- **CoinJoin** combines many users' transactions; see [CoinJoin and Payjoin](/kb/coinjoin/). The legal environment changed sharply in 2024: the Samourai Wallet founders were arrested on US charges (they pleaded guilty in 2025 to operating an unlicensed money-transmitting business), and the zkSNACKs coordinator used by Wasabi Wallet shut down. JoinMarket, which has no central coordinator, continues.
- Buying without KYC (peer-to-peer markets such as Bisq, RoboSats and Hodl Hodl, or in person) avoids creating the link in the first place.

For stronger on-chain privacy by default, see [Monero](/kb/monero/); for private everyday payments, see [Cashu and Chaumian Ecash](/kb/cashu-ecash/).

## 7. Physical security

The "$5 wrench attack" (someone threatening you until you hand over keys) is real and increasing. Do not talk about your holdings. Multisig with geographically separated keys, a decoy passphrase wallet, and time-delayed setups all reduce what an attacker can force you to do on the spot.

## Sources

- Bitcoin Core: <https://bitcoincore.org/>
- BIP-39, *Mnemonic code for generating deterministic keys*: <https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki>
- BIP-174, *Partially Signed Bitcoin Transaction Format*: <https://github.com/bitcoin/bips/blob/master/bip-0174.mediawiki>
- BIP-78, *Payjoin*: <https://github.com/bitcoin/bips/blob/master/bip-0078.mediawiki>; BIP-352, *Silent Payments*: <https://github.com/bitcoin/bips/blob/master/bip-0352.mediawiki>
- Sparrow Wallet documentation: <https://sparrowwallet.com/docs/>
- Bitcoin Wiki, *Privacy*: <https://en.bitcoin.it/wiki/Privacy>
- US Attorney's Office SDNY, *Founders of Samourai Wallet cryptocurrency mixing service plead guilty* (August 2025): <https://www.justice.gov/usao-sdny/pr/founders-samourai-wallet-cryptocurrency-mixing-service-plead-guilty>
