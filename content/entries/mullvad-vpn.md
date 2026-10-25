---
title: "Mullvad VPN"
slug: mullvad-vpn
type: deep-dive
pillars: ["circumvention", "anonymity"]
readiness: usable
description: "Mullvad uses numbered accounts and WireGuard tunnels. Examine payment records, published audits, multihop routing and DAITA limitations."
dek: "A managed VPN with a minimal account identifier still depends on its operator, software and payment path."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: ["wireguard", "cover-traffic", "using-tor-safely", "browser-and-network-privacy"]
---

## Summary

Mullvad is a commercial VPN service. Its account system generates a number without asking for an email address, username or password. That reduces required registration data; it does not make every payment method anonymous or remove the VPN operator from the trust model.

## How it works

Mullvad documents WireGuard tunnels and a multihop mode that routes a connection through two of its servers. Its current multihop modes can always use two servers, use them when a selected feature requires it, or disable multihop.

DAITA adds padding and background traffic and varies traffic patterns to make analysis harder. It changes observable traffic characteristics; it should not be read as a guarantee of anonymity. See [cover traffic](/kb/cover-traffic/) for the broader design question.

## Trust model / threat model

Mullvad's published policy says it does not keep activity logs. Treat that as the operator's stated policy. The same page explains payment data handling and lists cash, Monero, Bitcoin, Bitcoin Cash, bank wire, card, PayPal and Swish. Cash uses a payment token; bank and payment-provider routes can introduce identifying records. Follow the current instructions for the chosen payment method.

Two hops operated by one company do not create two independent administrative trust domains. The account number also remains a credential worth protecting. Compare the protocol-level trust model in [WireGuard](/kb/wireguard/) with [using Tor safely](/guides/using-tor-safely/).

## Readiness

**Usable.** Mullvad publishes client and service documentation and links external assessments. Its account/payment-services audit announcement names X41 D-Sec and describes the reviewed backend scope. Its GotaTun announcement names Assured Security Consultants and explicitly excludes DAITA, the command-line interface and external dependencies from that review. An audit of one component is not an audit of every service claim.

## Limits

Choose a VPN according to the adversary and network restrictions you face. Keep website encryption, account privacy and device security in the plan; see [browser and network privacy](/guides/browser-and-network-privacy/). This entry does not rank providers or promise that a VPN will work through a particular block.

## Primary sources

- [Numbered accounts, payment handling and logging policy](https://mullvad.net/en/help/no-logging-data-policy)
- [WireGuard multihop](https://mullvad.net/en/help/multihop-wireguard)
- [Current multihop modes](https://mullvad.net/en/blog/introducing-multihop-modes)
- [DAITA design](https://mullvad.net/en/vpn/daita)
- [Account and payment services audit scope](https://mullvad.net/en/blog/new-security-audit-of-account-and-payment-services)
- [GotaTun audit scope and exclusions](https://mullvad.net/en/blog/a-security-audit-of-gotatun-is-now-available)
