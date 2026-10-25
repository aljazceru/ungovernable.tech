---
title: "Pluggable transports and bridges"
slug: pluggable-transports
type: explainer
pillars: [circumvention, anonymity]
readiness: usable
description: "Tor bridges provide alternative entry points; pluggable transports disguise the connection. Compare obfs4, Snowflake, meek and WebTunnel."
dek: "An unlisted address and a different-looking connection solve different parts of the blocking problem."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [tor, using-tor-safely, psiphon, outline, wireguard, ooni, self-hosted-circumvention-server, censorship-circumvention]
tags: [tor, bridges, pluggable-transports, obfs4, snowflake, meek, webtunnel]
---

## Summary

A **bridge** is a Tor relay whose address is not listed in the public relay directory. It supplies an alternative entry point when known Tor relays are blocked. A **pluggable transport** changes how the connection to Tor looks on the network, making protocol-based detection harder. An unlisted address alone does not provide that disguise.

The [Tor Browser manual](https://tb-manual.torproject.org/circumvention/) leads to the current [unblocking guide](https://support.torproject.org/tor-browser/circumvention/unblocking-tor/), which documents obfs4, meek, Snowflake and WebTunnel. They address different blocking conditions; none is a universal answer.

## How it works

The transport carries the connection into Tor while Tor provides the onward circuit. The [relay guide](https://community.torproject.org/relay/types-of-relays/) distinguishes a bridge at the entry from an exit relay connecting to the destination.

| Transport | What changes on the network | Practical dependency |
|---|---|---|
| **obfs4** | Makes the traffic look random and resists discovery of bridges by scanning. | You need a reachable bridge and its complete connection details. Its address can still be blocked. |
| **Snowflake** | Uses WebRTC connections through volunteer proxies, resembling the technology used for calls. | Requires reachable volunteers and Snowflake infrastructure; users do not need to obtain a private bridge address. |
| **meek** | Makes the connection appear to reach a major website through a CDN or cloud provider. | Depends on that service path remaining available; users do not need a separately obtained bridge address. |
| **WebTunnel** | Makes the Tor connection look like HTTPS web traffic. | Operators need a domain, a valid certificate and a web server; a secret URL path directs connections to the bridge. |

The [Snowflake project](https://snowflake.torproject.org/) explains its WebRTC design. The [WebTunnel operator guide](https://community.torproject.org/relay/setup/webtunnel/) documents the website, certificate and reverse-proxy setup. Looking like a common protocol raises the difficulty of selective blocking; it does not prevent a censor blocking the endpoint or the surrounding service.

**Conjure is experimental here.** Tor's [Conjure testing announcement](https://forum.torproject.org/t/call-for-testers-help-the-tor-project-to-test-conjure-on-tor-browser-alpha/7815) describes refraction networking: participating network infrastructure turns otherwise unused IP addresses into proxy endpoints. A later [Tor developer response](https://forum.torproject.org/t/what-happened-to-conjure-bridges/17884) says the bridge is for testing and expected to fail. Treat it as research to follow, not a fallback to promise to people who need access.

## Getting and using bridges

1. Install Tor Browser while you can reach the official download channel. In its connection settings, try a built-in transport appropriate to your network.
2. If you need additional bridges, request them inside Tor Browser or through [Tor's bridge distributor](https://bridges.torproject.org/). The [getting-bridges guide](https://support.torproject.org/tor-browser/circumvention/getting-bridges/) lists the supported distribution methods.
3. Copy the **complete bridge line**, not just the IP address, into the bridge settings. Follow the [desktop or Android instructions](https://support.torproject.org/tor-browser/circumvention/using-bridges/) for your client.
4. If it fails, try another bridge or transport. Preserve a working configuration privately and keep an alternative; avoid publishing the bridge details you depend on.

For ordinary browsing precautions after connecting, continue with [Using Tor Safely](/guides/using-tor-safely/).

## Trust model / threat model

Bridges change the entry to the Tor circuit. They are not exits and do not replace the rest of Tor's design. Their address is absent from the public relay directory, not guaranteed secret from anyone who receives or discovers it. Tor's own relay guide documents that bridges can be detected and blocked.

Transport disguise should not be read as a guarantee that Tor use is undetectable. Choose based on the connection you can actually establish. A VPN such as [WireGuard](/kb/wireguard/) or a proxy such as [Outline](/kb/outline/) has a different trust model from a Tor circuit; transport encryption alone does not make them interchangeable.

## Readiness

**Usable for the transports documented in Tor Browser.** obfs4, Snowflake, meek and WebTunnel have user-facing connection instructions. Which one works depends on local filtering. Conjure is described separately because its documented testing status is a different readiness level.

## Limits

- An unpublished bridge can be learned and blocked. Transport disguise does not solve every form of address blocking.
- Bridges and transports can slow connections. Reachability and performance need local testing, with attention to the risks of measurement described in [OONI](/kb/ooni/).
- The Snowflake browser extension **helps other people** connect. To use Snowflake for your own access, select it in a supported Tor application; installing the extension does not unblock your own browsing.
- These are internet transports. Pair them with [shutdown preparedness](/guides/internet-shutdown-preparedness/) for loss of connectivity and with the [server guide](/guides/self-hosted-circumvention-server/) if you want to contribute capacity.

## Primary sources

- [Tor Browser manual: circumvention](https://tb-manual.torproject.org/circumvention/) and [current unblocking guide](https://support.torproject.org/tor-browser/circumvention/unblocking-tor/).
- [Getting bridges](https://support.torproject.org/tor-browser/circumvention/getting-bridges/), [using bridges](https://support.torproject.org/tor-browser/circumvention/using-bridges/) and [bridge distribution](https://bridges.torproject.org/).
- [Types of Tor relays](https://community.torproject.org/relay/types-of-relays/).
- [Snowflake](https://snowflake.torproject.org/) and [WebTunnel setup](https://community.torproject.org/relay/setup/webtunnel/).
- [Conjure testing announcement](https://forum.torproject.org/t/call-for-testers-help-the-tor-project-to-test-conjure-on-tor-browser-alpha/7815) and [developer guidance on experimental status](https://forum.torproject.org/t/what-happened-to-conjure-bridges/17884).
