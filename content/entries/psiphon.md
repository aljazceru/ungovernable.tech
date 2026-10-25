---
title: "Psiphon"
slug: psiphon
type: deep-dive
pillars: [circumvention]
readiness: usable
description: "Psiphon tries multiple transports to reach its proxy network through censorship. Its open core, operator trust and privacy limits explained."
dek: "A managed route around blocking, with transport selection handled by the client and infrastructure operated by Psiphon."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [outline, wireguard, pluggable-transports, ooni, tor, censorship-circumvention, internet-shutdown-preparedness]
tags: [psiphon, censorship, proxies, obfuscation]
---

## Summary

Psiphon is a circumvention system operated by Psiphon Inc. Its client tries different servers and connection methods to reach the internet through filtering. You rely on that operator's infrastructure and software distribution instead of administering a server yourself. Psiphon's own [FAQ](https://psiphon.ca/en/faq.html) says that, like any VPN, it protects the privacy of your traffic but is not a full anonymity tool.

## How it works

**An encrypted core with changing transports.** The [open-source tunnel core](https://github.com/Psiphon-Labs/psiphon-tunnel-core) documents SSH as the authenticated, encrypted channel between client and proxy. Obfuscation layers wrap that channel to change what the network sees. The code's [protocol definitions](https://github.com/Psiphon-Labs/psiphon-tunnel-core/blob/master/psiphon/common/protocol/protocol.go) include obfuscated SSH, fronted and unfronted meek variants, and QUIC-based obfuscated SSH. These are implemented options, not a promise that every app or connection uses every transport.

**Discovery and selection.** Clients receive server entries containing addresses, public keys and connection parameters. The core can try several servers and obfuscation methods concurrently, remember successful choices, and receive remotely supplied configuration called *tactics*. This lets the operator adapt connection strategies without requiring users to pick a protocol by hand.

**Traffic routing.** The core supports local proxy forwarding and a packet-tunnel mode. Check the mode and platform you actually use: an app configured to use a local proxy is a different scope from routing a device's traffic through a VPN interface.

## Trust model / threat model

The tunnel protects traffic between the device and Psiphon's server. Psiphon controls the server network, discovery information and operational configuration. Open source makes the implementation inspectable; it does not remove this central point of trust.

The [FAQ's data-handling section](https://psiphon.ca/en/faq.html) distinguishes visibility from retention: HTTPS remains encrypted between the device and destination, while ordinary HTTP passes through the proxy in cleartext. Psiphon says it does not inspect or store that HTTP traffic. Treat those retention statements as the operator's policy, not as a cryptographic restriction on what a server could observe.

## Privacy policy

The current [privacy policy](https://psiphon.ca/en/privacy.html) says Psiphon does not persist users' IP addresses, record the services they access or store traffic content. It does describe collecting connection metadata: approximate country and city, network provider, connection duration, transferred data, performance, protocol, platform, client version and the Psiphon server used.

The accompanying FAQ specifies a rolling **90-day** deletion schedule for raw operational connection data, with exceptions for filtered data retained to study significant censorship events. Aggregated statistics and optional diagnostic reports may be retained indefinitely. The policy also describes third-party services, including advertising through Google AdMob in the free app. Read the policy and data-handling details for the app you intend to use; “no browsing history” does not mean “no metadata”.

## Readiness

**Usable.** Psiphon provides client downloads, a deployed service and a documented open-source client/server core. It is an access option to test alongside [Outline](/kb/outline/) and [Tor bridges](/kb/pluggable-transports/). No local success rate is implied by this rating.

## Limits

- **Access is not anonymity.** Psiphon's own documentation draws that boundary. For an anonymity network and its separate limitations, read [Tor](/kb/tor/) and [Using Tor Safely](/guides/using-tor-safely/).
- **A working route can stop working.** Transport diversity helps adaptation; it does not guarantee that a censor leaves a path available.
- **The operator remains central.** Server discovery, updates, capacity and collection practices depend on Psiphon. [Self-hosting](/guides/self-hosted-circumvention-server/) changes that responsibility and introduces its own maintenance burden.
- **Measurement is separate.** [OONI](/kb/ooni/) has a Psiphon reachability test, but running it has risks, and a result concerns the tested network and time.

## Primary sources

- [Psiphon project and downloads](https://psiphon.ca/).
- [FAQ: connection methods, anonymity limits and data handling](https://psiphon.ca/en/faq.html).
- [Privacy policy](https://psiphon.ca/en/privacy.html).
- [Psiphon tunnel core](https://github.com/Psiphon-Labs/psiphon-tunnel-core).
- [Implemented transport identifiers](https://github.com/Psiphon-Labs/psiphon-tunnel-core/blob/master/psiphon/common/protocol/protocol.go).
