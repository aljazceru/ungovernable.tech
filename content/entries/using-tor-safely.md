---
title: "Using Tor Safely"
slug: using-tor-safely
type: guide
pillars: [anonymity, circumvention]
description: "How to install Tor Browser, connect through bridges when Tor is blocked, choose a security level and avoid the habits that deanonymise users."
dek: "Tor hides where you are from the sites you visit and hides what you visit from your network. These are the habits that keep it working."
updated: 2026-10-17
created: 2026-10-17
origin: original
level: beginner
time: "20 minutes"
related: [tor, onion-and-i2p-naming, censorship-circumvention, tails-qubes-whonix, mix-networks]
---

Tor routes your traffic through three volunteer-run relays. The first relay (the guard) sees your IP address but not your destination; the last (the exit) sees your destination but not your IP address; no single relay sees both. Websites see the exit's address instead of yours, and your internet provider sees only that you are using Tor, or, with a bridge, not even that. For how it works underneath, read the [Tor deep dive](/kb/tor/).

Tor is strong against websites, advertisers, your ISP and local network observers. It is **not** designed to defeat an adversary who can watch both your connection and the destination at the same time and correlate the timing. It also cannot protect you from yourself: logging into your personal account over Tor tells the site exactly who you are.

## 1. Get Tor Browser from the source

Download Tor Browser only from <https://www.torproject.org/download/>. On Android, use the official Tor Browser app from the Tor Project (Google Play, F-Droid via the Guardian Project repository, or the download page). On iOS there is no Tor Browser; the Tor Project recommends Onion Browser.

If torproject.org is blocked where you are, the Tor Project keeps official mirrors and a GetTor service that sends download links by email (gettor@torproject.org) or Telegram (@gettor_bot). Verify the signature if you can; the download page explains how.

## 2. Connect, with a bridge if you need one

When Tor Browser starts, it offers to connect. In many countries that just works. If Tor is blocked, use **Connection Assist**, which detects censorship and suggests a bridge, or configure one by hand under *Settings → Connection → Bridges*.

Bridges are Tor relays that are not listed publicly, combined with *pluggable transports* that disguise Tor traffic:

| Transport | How it hides | When to use |
|---|---|---|
| **obfs4** | Makes traffic look like random bytes | Works in many places; ask for private obfs4 bridges if the built-in ones are blocked |
| **Snowflake** | Tunnels through short-lived WebRTC connections to volunteer browsers | Good default when built-in bridges fail; slower |
| **meek** | Tunnels through a large cloud provider (domain fronting style) | Last resort; slow but hard to block without collateral damage |
| **WebTunnel** | Looks like an ordinary HTTPS website connection | Where obfs4 is detected; request from the bridge distributor |

To get private bridges: visit <https://bridges.torproject.org/>, send an email to bridges@torproject.org from a Gmail or Riseup address, or message @GetBridgesBot on Telegram. Get bridges *before* a crisis and keep them somewhere offline.

## 3. Pick a security level

Click the shield icon. **Standard** is the default. **Safer** disables JavaScript on non-HTTPS sites and some fonts and media features. **Safest** disables JavaScript everywhere. If your adversary might use browser exploits against you, use Safest and accept that some sites break.

## 4. Habits that keep you anonymous

- **Do not install add-ons.** Every user should look the same; extensions make you unique and can leak.
- **Do not log into accounts tied to your real identity** in the same session you want to keep anonymous. Use *New Identity* (the broom icon) between unrelated activities.
- **Do not open downloaded documents while online.** PDFs and office files can fetch remote resources outside Tor. Open them offline, in Tails, or in a disposable VM.
- **Do not torrent over Tor.** BitTorrent clients often leak your real IP address and overload the network.
- **Prefer .onion addresses.** Traffic to an onion service never leaves the Tor network, so there is no exit relay to watch it. Many news organisations, SecureDrop instances and services publish onion addresses; Tor Browser shows a ".onion available" button when a site advertises one.
- **Keep it updated.** Tor Browser ships security updates frequently; install them promptly.
- **Using Tor is visible to your ISP** unless you use a bridge. In some places that alone attracts attention; decide whether a bridge should be your default.

## 5. When Tor Browser is not enough

If your adversary could compromise your operating system, or if a single mistake would be catastrophic, use a system that forces everything through Tor: **Tails** (amnesic live USB) or **Whonix** (a gateway VM that routes a workstation VM through Tor), ideally inside **Qubes OS**. See [Tails, Qubes OS and Whonix](/guides/tails-qubes-whonix/).

## Give back

If you live somewhere uncensored, you can help people who do not: run a Snowflake proxy in your browser (<https://snowflake.torproject.org/>) or a bridge. See [Running Infrastructure for Freedom](/guides/running-freedom-infrastructure/).

## Sources

- Tor Project, *Tor Browser User Manual*: <https://tb-manual.torproject.org/>
- Tor Project, *Bridges* and *Circumvention*: <https://tb-manual.torproject.org/bridges/>, <https://tb-manual.torproject.org/circumvention/>
- Tor Project, *Security Settings*: <https://tb-manual.torproject.org/security-settings/>
- Tor Project, *GetTor*: <https://gettor.torproject.org/>
- Tor Project Support, *Can I use Tor with BitTorrent?*: <https://support.torproject.org/>
