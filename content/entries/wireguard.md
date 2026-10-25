---
title: "WireGuard"
slug: wireguard
type: deep-dive
pillars: [circumvention]
readiness: battle-tested
description: "WireGuard encrypts IP traffic between peers with a small, fixed protocol. Its routing, operator trust and lack of built-in obfuscation explained."
dek: "A dependable encrypted tunnel to a server you choose, with no built-in disguise against network censorship."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [outline, psiphon, pluggable-transports, ooni, nostr-vpn, self-hosted-circumvention-server, censorship-circumvention]
tags: [wireguard, vpn, cryptokey-routing, censorship]
---

## Summary

WireGuard is an encrypted IP tunnel carried over UDP. Each peer has a private key, knows its peers' public keys, and associates those peers with allowed tunnel addresses. You can run it on your own server or use it through a VPN provider. It protects traffic on the path to that server; it does not make the server untrusted or make the connection look like ordinary web browsing.

## How it works

**A fixed cryptographic protocol.** WireGuard uses a Noise IK handshake, specifically `Noise_IKpsk2_25519_ChaChaPoly_BLAKE2s`: Curve25519 for key agreement, ChaCha20-Poly1305 for authenticated encryption, and BLAKE2s for hashing. Handshakes establish rotating session keys with forward secrecy for data packets. The [protocol description](https://www.wireguard.com/protocol/) and [whitepaper](https://www.wireguard.com/papers/wireguard.pdf) describe the construction.

**Cryptokey routing.** `AllowedIPs` associates each public key with IP prefixes. On send, the destination address selects the peer; on receive, the source address must be allowed for the authenticated peer. This is both a routing decision and an access check. The server learns a peer's current public endpoint from authenticated packets, allowing peers to move between networks. The [project overview](https://www.wireguard.com/) walks through both directions.

**Configuration stays outside the protocol.** WireGuard does not distribute keys or provision accounts. The operator handles key exchange, address allocation, routing, DNS and revocation. The supplied `wg` and `wg-quick` tools configure and bring up interfaces; a working handshake alone does not establish that all internet traffic uses the tunnel.

## Trust model / threat model

For packets routed through it, WireGuard encrypts the inner IP traffic between the device and its peer. A local network observer can still see the outer endpoints and packet timing and size. Traffic excluded by routing rules gets no protection from that tunnel.

**The VPN operator is the other end of the encryption.** It knows the peer's public key, assigned tunnel addresses and current public IP endpoint. The [administration tool](https://git.zx2c4.com/wireguard-tools/about/src/man/wg.8) exposes endpoints, latest handshake times and transfer counters. These are live operational metadata; the protocol does not promise that an operator deletes them or refrains from logging.

When that peer forwards your traffic to the internet, it can observe destination addresses and any traffic without separate application encryption. HTTPS remains encrypted between the browser and website. Self-hosting changes who administers this point of trust; it still leaves the hosting provider and the server's network in the path. The [Ubuntu gateway guide](https://documentation.ubuntu.com/server/how-to/wireguard-vpn/vpn-as-the-default-gateway/) explains forwarding and the separate DNS decision.

## Use under censorship

WireGuard's own [limitations page](https://www.wireguard.com/known-limitations/) explicitly leaves obfuscation to another layer. Its distinctive packet signatures can be recognised by deep packet inspection (DPI); encryption does not stop a censor identifying and blocking the protocol or the server address.

[AmneziaWG](https://github.com/amnezia-vpn/amneziawg-go) is a documented fork of WireGuard-Go that adds obfuscation to address those signatures. It is a separate implementation, not a switch in standard WireGuard. An obfuscation layer or variant can help against protocol detection, but should not be treated as a promise of reachability. Compare [Outline](/kb/outline/), [Psiphon](/kb/psiphon/) and [Tor's pluggable transports](/kb/pluggable-transports/) for other approaches.

## Readiness

**Battle-tested as a VPN protocol.** WireGuard entered mainline Linux in **5.6**, confirmed by the maintainer's [release announcement](https://lists.zx2c4.com/pipermail/wireguard/2020-March/005206.html). Official clients and installation instructions cover desktop and mobile platforms. This rating concerns encrypted tunnelling, not its ability to survive censorship.

## Limits

- **No built-in obfuscation.** A private server address does not hide a recognisable protocol.
- **No anonymity from the endpoint operator.** Keys and addresses identify peers to that operator; logging into a website still identifies you to that website.
- **Routing and DNS need deliberate configuration.** A split tunnel protects only its selected routes. Check IPv6 and DNS separately; the [wg-quick manual](https://git.zx2c4.com/wireguard-tools/about/src/man/wg-quick.8) documents default routes, DNS configuration and an optional firewall-based kill switch.
- **Key compromise has different consequences for content and identity.** The project documents forward secrecy for data, but not for the identity hidden in recorded handshakes if the responder's private key is later compromised.

For an operator checklist, follow [Run a private circumvention server for people you know](/guides/self-hosted-circumvention-server/). Use [OONI](/kb/ooni/) to understand published measurements before deciding whether to run tests yourself.

## Primary sources

- [WireGuard overview and cryptokey routing](https://www.wireguard.com/).
- [Protocol and cryptography](https://www.wireguard.com/protocol/) and [technical whitepaper](https://www.wireguard.com/papers/wireguard.pdf).
- [Known limitations](https://www.wireguard.com/known-limitations/).
- [Linux 5.6 release announcement](https://lists.zx2c4.com/pipermail/wireguard/2020-March/005206.html).
- [Installation](https://www.wireguard.com/install/) and [quick start](https://www.wireguard.com/quickstart/).
- [wg manual](https://git.zx2c4.com/wireguard-tools/about/src/man/wg.8) and [wg-quick manual](https://git.zx2c4.com/wireguard-tools/about/src/man/wg-quick.8).
- [AmneziaWG implementation and configuration](https://github.com/amnezia-vpn/amneziawg-go).
- [Ubuntu: using WireGuard as the default gateway](https://documentation.ubuntu.com/server/how-to/wireguard-vpn/vpn-as-the-default-gateway/).

Continue with [DNSCrypt and dnscrypt-proxy](/kb/dnscrypt/) and [Mullvad VPN](/kb/mullvad-vpn/).
