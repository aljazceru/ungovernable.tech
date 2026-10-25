---
title: "DNSCrypt and dnscrypt-proxy"
slug: dnscrypt
type: deep-dive
pillars: ["circumvention", "anonymity"]
readiness: usable
description: "DNSCrypt encrypts DNS queries to a resolver. Compare direct resolution, anonymized relays and the DoH and ODoH support in dnscrypt-proxy."
dek: "Encrypted DNS protects a lookup on its way to a resolver; relay separation changes who can associate it with your IP address."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: ["censorship-circumvention", "wireguard", "metadata-resistance", "browser-and-network-privacy"]
---

## Summary

DNSCrypt is a protocol for authenticating and encrypting DNS traffic between a client and a resolver. `dnscrypt-proxy` is a client proxy supporting DNSCrypt, DNS over HTTPS (DoH), Anonymized DNSCrypt and Oblivious DoH (ODoH). These are distinct connection modes, not interchangeable names for the same protection.

## How it works

| Mode | Query path | Trust boundary |
|---|---|---|
| Direct DNSCrypt or DoH | Client to resolver over an encrypted connection | The resolver receives the query and the connecting client's IP address. |
| Anonymized DNSCrypt | Client encrypts for the resolver, then sends through a relay | The relay forwards ciphertext; the resolver sees the relay's address. |
| ODoH | Client encrypts for an ODoH target and uses an ODoH relay | Both target and relay must support ODoH; an arbitrary DoH server is insufficient. |

DNSCrypt's protocol specification defines resolver certificates and authenticated query/response encryption. The proxy's anonymization configuration selects relay/resolver routes. Its ODoH documentation separately describes enabling ODoH servers and loading the relevant server and relay lists.

## Trust model / threat model

A direct encrypted resolver still sees the questions it answers. With a relay, choose operators independently: the Anonymized DNS documentation explicitly warns against having the same entity run both ends. This separation is a privacy assumption, not protection against collusion or an observer correlating both connections.

## Readiness

**Usable.** The maintained proxy documents all four modes. Verify the selected mode and resolver in your own configuration; enabling encrypted DNS alone does not select an anonymizing relay.

## Limits

This protects DNS exchanges. It is not a tunnel for the subsequent website connection, and DNSCrypt is not DNSSEC: the former protects transport to a resolver, while DNSSEC authenticates DNS data. Do not treat successful resolution as proof that a blocked destination is reachable. Continue with [WireGuard](/kb/wireguard/), [censorship circumvention](/guides/censorship-circumvention/) and [browser and network privacy](/guides/browser-and-network-privacy/).

## Primary sources

- [DNSCrypt protocol specification](https://dnscrypt.info/protocol/)
- [dnscrypt-proxy supported protocols](https://github.com/DNSCrypt/dnscrypt-proxy)
- [Anonymized DNS configuration and operator separation](https://github.com/DNSCrypt/dnscrypt-proxy/wiki/Anonymized-DNS)
- [Oblivious DoH support and requirements](https://github.com/DNSCrypt/dnscrypt-proxy/wiki/Oblivious-DoH)
- [RFC 4033: DNSSEC data authentication](https://www.rfc-editor.org/rfc/rfc4033.html)
