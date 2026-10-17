---
title: "Reducing Tracking: Browsers, DNS and Fingerprinting"
slug: browser-and-network-privacy
type: guide
pillars: [endpoint, anonymity]
description: "Practical steps against everyday tracking: choosing and hardening a browser, blocking trackers, encrypted DNS, private search and testing your fingerprint."
dek: "Most surveillance is commercial and automatic. A few changes to your browser and network remove most of it."
updated: 2026-10-17
created: 2026-10-17
origin: original
level: beginner
time: "30 minutes"
related: [using-tor-safely, threat-modeling, tor, decentralized-dns]
---

Advertisers, data brokers and platforms track people across the web with cookies, tracking scripts, link decoration, and browser fingerprinting: the combination of fonts, screen size, graphics hardware and settings that makes your browser recognisable even with cookies cleared. Much of this data is later sold or handed over. You cannot opt out of all of it, but you can opt out of most of it.

## 1. Choose the browser for the job

| Browser | Use for | Why |
|---|---|---|
| **Tor Browser** | Anything that must not be linked to you | Routes through Tor; designed so that all users look identical ([Using Tor Safely](/guides/using-tor-safely/)) |
| **Mullvad Browser** | Private everyday browsing, with a VPN or on its own | Built by the Tor Project and Mullvad: Tor Browser's anti-fingerprinting, without the Tor network |
| **Firefox, hardened** | Daily browsing where you need extensions | Enable strict Enhanced Tracking Protection; consider the arkenfox user.js for stronger defaults |
| **Brave** | Daily browsing, Chromium compatibility | Built-in tracker blocking and fingerprint randomisation; disable the crypto and AI features you do not use |

Use different browsers, or at least different profiles, for identities you want to keep apart.

## 2. Block trackers

**uBlock Origin** is the most effective content blocker for Firefox. It blocks ads, trackers and many malicious domains. On Chromium-based browsers, Google's Manifest V3 changes have limited what extensions can do; Brave's built-in blocking is not affected. Avoid installing many privacy extensions: each one makes your browser more unique.

## 3. Encrypt your DNS

Every site you visit starts with a DNS lookup that, by default, your ISP (or whoever runs the network) can see and alter. Encrypted DNS (DNS over HTTPS or DNS over TLS) hides these lookups from the local network.

- Turn it on in the browser (Firefox and Chromium-based browsers support DNS over HTTPS) or system-wide (Android's *Private DNS* setting supports DNS over TLS).
- Choose a resolver whose logging policy you trust, such as Quad9, or run your own.
- Encrypted DNS moves trust to the resolver; it does not hide which IP addresses you connect to. A VPN or Tor does.

## 4. Search without being profiled

Use search engines that do not build profiles, such as DuckDuckGo, Startpage or Brave Search, or run your own **SearXNG** instance, an open-source metasearch engine that queries others on your behalf.

## 5. Strip tracking from links

Many links carry identifiers (for example `utm_`, `fbclid` and `gclid` parameters) that tell the destination where you came from. Firefox's *Copy Link Without Site Tracking* and uBlock Origin's filter lists remove many of them. Remove them by hand before sharing links.

## 6. Test your browser

EFF's **Cover Your Tracks** (<https://coveryourtracks.eff.org/>) shows whether your browser blocks trackers and how unique your fingerprint is. The goal is not zero tracking (impossible) but blending in or randomising.

## 7. Phones

On phones, apps track far more than websites. Reduce the number of apps, prefer websites to apps for services you rarely use, revoke location and contact permissions, reset or delete the advertising ID, and consider a hardened OS ([Hardening a Phone with GrapheneOS](/guides/grapheneos/)).

## Sources

- EFF, *Cover Your Tracks*: <https://coveryourtracks.eff.org/>
- Tor Project and Mullvad, *Mullvad Browser*: <https://mullvad.net/en/browser>
- uBlock Origin: <https://github.com/gorhill/uBlock>
- arkenfox user.js: <https://github.com/arkenfox/user.js>
- Mozilla, *DNS over HTTPS in Firefox*: <https://support.mozilla.org/kb/firefox-dns-over-https>
- SearXNG: <https://docs.searxng.org/>
- Privacy Guides, *Desktop browsers*: <https://www.privacyguides.org/en/desktop-browsers/>
