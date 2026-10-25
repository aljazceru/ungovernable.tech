---
title: "Stablecoins and sovereignty"
slug: stablecoins-and-sovereignty
type: explainer
pillars: ["money"]
readiness: usable
description: "Holding stablecoin keys does not remove issuer control. Examine USDC and Tether freezing powers, redemption rules, chain choice and privacy."
dek: "Self-custody controls a signing key; an issuer-backed token also depends on contract administration and redemption terms."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: ["financial-sovereignty", "bitcoin-self-custody", "monero", "zcash"]
---

## Summary

Holding the private key to a stablecoin address and controlling the token's rules are different things. Circle's USDC contract documentation includes privileged pause, blacklist and upgrade functions. Tether's terms reserve powers to freeze tokens and restrict services. A self-custodied wallet does not remove these issuer controls.

## How it works

Circle's EVM implementation distinguishes several administrative roles. A pauser can stop transfers, a blacklister can prevent specified addresses from sending or receiving, and a proxy owner can change the implementation. These are properties of the documented contract family; check the exact deployed contract and network before generalizing to another token implementation.

Tether's terms describe circumstances in which it may freeze tokens, suspend services or restrict redemption. Read the applicable terms directly: control of a blockchain address does not by itself establish eligibility to redeem through the issuer.

## Trust model / threat model

| Layer | What to verify |
|---|---|
| Wallet | Who controls signing and recovery material? |
| Token contract | Who can pause, blacklist or upgrade this implementation? |
| Issuer | What redemption rights, identity checks and restrictions apply to you? |
| Network | Is this the issuer-supported token on the intended chain? |
| Bridge or wrapper | Is there another custodian or contract between you and the issuer-backed asset? |

Circle's cited USDC terms apply outside the European Economic Area and direct EEA holders to separate documentation. They also distinguish issuer-supported USDC from third-party copies and wrappers. Tether's integration page identifies supported protocols and flags legacy networks where issuance or redemption support has ended. Do not treat a familiar ticker as proof of a supported redemption path.

## Privacy

Do not infer transaction privacy from self-custody or a stable price. Review the ledger visibility, wallet disclosures and exchange or redemption records involved in your actual route. Circle's terms require identity verification for direct redemption. Compare [Monero](/kb/monero/) and [Zcash](/kb/zcash/) when privacy is a requirement, and assess the distinct custody model in [Bitcoin self-custody](/guides/bitcoin-self-custody/).

## Readiness

**Usable with issuer dependence.** The contracts and issuer services are documented. Their controls are part of the asset's trust model, not a wallet setting that can be disabled.

## Limits

This comparison addresses control boundaries, not reserve quality, investment returns or a guaranteed peg. Use it with [financial sovereignty](/kb/financial-sovereignty/) to decide which dependencies you are willing to accept.

## Primary sources

- [Circle EVM token contract roles and features](https://github.com/circlefin/stablecoin-evm)
- [Circle USDC terms, scope, redemption and wrappers](https://www.circle.com/legal/usdc-terms)
- [Tether terms and freezing powers](https://tether.to/en/legal/)
- [Tether supported and legacy protocols](https://tether.to/en/supported-protocols/)
