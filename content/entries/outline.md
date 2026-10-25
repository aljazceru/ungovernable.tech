---
title: "Outline"
slug: outline
type: deep-dive
pillars: [circumvention]
readiness: usable
description: "Outline pairs a Shadowsocks server with a manager and shareable access keys. Understand self-hosting, operator visibility and blocking limits."
dek: "Run a proxy for people you know, with an explicit choice of server operator and hosting provider."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [wireguard, psiphon, pluggable-transports, ooni, self-hosted-circumvention-server, censorship-circumvention]
tags: [outline, shadowsocks, self-hosting, censorship]
---

## Summary

Outline is software for creating and sharing a private circumvention server. Launched by Jigsaw, it is now owned by the independent Outline Foundation, according to the [project's FAQ](https://getoutline.org/faq/). You choose the server and hosting provider; Outline does not operate a VPN service for you.

## How it works

**Manager, server, client.** Outline Manager is a desktop application that helps deploy and administer a server on cloud infrastructure or your own Linux system. The server runs a Shadowsocks proxy and exposes a management API. People using it install Outline Client and import an access key. The [server repository](https://github.com/Jigsaw-Code/outline-server) and [applications repository](https://github.com/Jigsaw-Code/outline-apps) provide the code.

**Access keys.** Manager creates separate keys that can be shared, deleted or given data limits. Give each person their own key so access can be revoked individually. Treat the key as a secret that grants use of the server; keep the server's administration credentials separate. Follow the [official setup flow](https://getoutline.org/get-started/) or the [private-server guide](/guides/self-hosted-circumvention-server/).

**Shadowsocks transport.** The documented server uses authenticated encryption, replay protection, probing resistance and variable packet sizes to make detection harder. The project's FAQ describes its handshake-less protocol and private distribution of server access as reasons it can resist blocking. These are mitigations, not a guarantee that the server remains reachable.

## Trust model / threat model

The encrypted proxy connection protects traffic on the path between the client and the chosen server. **The operator of that server remains a trusted party.** By the proxy's design, it accepts client connections and makes outgoing destination connections: an operator with control of the machine can observe connecting IP addresses, destinations, timing and volumes. This follows from the server's [connection handling](https://raw.githubusercontent.com/Jigsaw-Code/outline-ss-server/master/service/tcp.go), rather than from a promise about logging.

Application encryption still matters. HTTPS content remains encrypted between the client and website; ordinary unencrypted traffic is visible after the proxy unwraps it. The hosting provider is also part of the trust boundary. Self-hosting gives you administrative control, not anonymity from the infrastructure that carries the traffic.

**Project telemetry is a separate question.** The [Outline privacy policy](https://getoutline.org/policies/privacy/) says the Foundation does not have access to your server or browsing traffic. It describes automatic crash reports and optional usage metrics, disabled by default, including per-key transferred bytes and originating country and network. It also names Cloudflare and Quad9 as DNS providers used by the client. Do not turn the Foundation's collection policy into a claim that your server operator, host or DNS resolver cannot observe anything.

## Readiness

**Usable.** Outline has a documented deployment flow, client applications, access management and an open server implementation. It is a practical option for a small group with someone willing to maintain the host. Local reachability still needs testing.

## Limits

- **An address can still be blocked.** Outline's own FAQ anticipates recreating a blocked server. Private key distribution reduces exposure but cannot guarantee that an address stays unknown.
- **Obfuscation is not anonymity.** A single proxy is a point where client and destination connections meet. Compare [Tor](/kb/tor/) when separating those observations matters.
- **Keys can spread.** Share them privately, revoke leaked keys, and avoid publishing a group's server access in a public channel.
- **Someone must operate it.** Hosting, account security, updates, bandwidth and recovery remain responsibilities of the person running the server. Keep another route, such as [Psiphon](/kb/psiphon/) or [Tor bridges](/kb/pluggable-transports/), ready to test.

## Primary sources

- [Outline project](https://getoutline.org/) and [FAQ, ownership and blocking resistance](https://getoutline.org/faq/).
- [Get started: Manager, keys and Client](https://getoutline.org/get-started/).
- [Server setup instructions](https://support.getoutline.org/manager/server-setup/setup-server).
- [Outline Server](https://github.com/Jigsaw-Code/outline-server), [Outline applications](https://github.com/Jigsaw-Code/outline-apps) and [Shadowsocks backend](https://github.com/Jigsaw-Code/outline-ss-server).
- [Server TCP connection handling](https://raw.githubusercontent.com/Jigsaw-Code/outline-ss-server/master/service/tcp.go).
- [Outline privacy policy](https://getoutline.org/policies/privacy/).
