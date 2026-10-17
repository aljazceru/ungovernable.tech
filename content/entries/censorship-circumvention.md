---
title: "Getting Around Internet Censorship"
slug: censorship-circumvention
type: guide
pillars: [circumvention, anonymity]
description: "How censors block the internet, and how Tor bridges, Psiphon, Outline, Xray with REALITY, AmneziaWG and similar tools get around each kind of blocking."
dek: "Censorship is an arms race between detection and disguise. Knowing which technique a censor is using tells you which tool will work."
updated: 2026-10-17
created: 2026-10-17
origin: original
level: intermediate
time: "30 minutes"
related: [using-tor-safely, tor, internet-shutdown-preparedness, map-censorship-resistance, decentralized-dns]
---

There is no single best circumvention tool. Each one is a disguise, and a disguise works only until the censor learns to see through it. The useful question is not "which app is best?" but "how is my network being censored right now, and what does that rule out?"

## How networks are censored

Censors combine several techniques, roughly in order of cost and sophistication:

| Technique | What happens | What gets around it |
|---|---|---|
| **DNS tampering** | The resolver returns a fake address or nothing for blocked domains | Encrypted DNS (DNS over HTTPS or TLS) to a resolver outside the censor's control; any proxy or VPN |
| **IP blocking** | Connections to known addresses of a service, VPN or Tor relay are dropped | Unlisted servers: private bridges, your own server, frequently rotating proxies |
| **SNI filtering** | The domain name visible in the TLS handshake is matched against a blocklist | Encrypted Client Hello where supported; tunnels that present an innocuous name |
| **Protocol fingerprinting (DPI)** | Deep packet inspection recognises OpenVPN, WireGuard, Tor or other tunnel protocols by their shape | Obfuscated transports: obfs4, WebTunnel, Shadowsocks variants, VLESS with REALITY, AmneziaWG |
| **Active probing** | The censor connects to a suspected proxy itself to see whether it answers like one | Transports designed to resist probing (obfs4, REALITY) and servers that behave like normal websites to strangers |
| **Throttling** | Traffic to a service or of a certain shape is slowed until it is unusable | Disguised transports; sometimes simply a different protocol |
| **Allowlisting** | Only approved domains or protocols work; everything else is blocked | Very little; domain fronting through allowed infrastructure, or going offline (see below) |
| **Shutdown** | Mobile data or the whole network is turned off, sometimes regionally | Nothing on the internet. Mesh radios, Bluetooth meshes, satellite, sneakernet ([Internet Shutdown Preparedness](/guides/internet-shutdown-preparedness/)) |

Research from GFW Report and others has documented these techniques in detail, including how China's Great Firewall detected Shadowsocks servers through active probing and, from 2021, began blocking "fully encrypted" traffic that looks like random bytes. The same arms race plays out in Iran, Russia, Turkmenistan and elsewhere.

## The main tool families

### Tor with pluggable transports
Tor plus a bridge is the most studied option and gives you anonymity, not just access. Built-in bridges are easy for censors to list, so request private bridges in advance. Snowflake and WebTunnel are often the transports that survive longest. Step by step: [Using Tor Safely](/guides/using-tor-safely/).

### Psiphon and Lantern
Psiphon (<https://psiphon.ca/>) and Lantern (<https://lantern.io/>) are free apps run by organisations that operate large, constantly changing server networks and switch transports automatically. They are often the easiest thing that works for non-technical users. The trade-off is trust: the operator can see your traffic metadata, and these tools are built for access, not anonymity.

### Your own server: Outline, Xray, AmneziaWG
Running your own proxy on a rented server outside the censored country gives you an address no blocklist has seen yet, and lets you share it with a small, trusted group.

- **Outline** (<https://getoutline.org/>), from Google's Jigsaw, installs a Shadowsocks-based server with a manager app and shareable access keys. It is one of the simplest options to deploy.
- **Xray-core** (<https://github.com/XTLS/Xray-core>) implements VLESS with **REALITY**, which makes the server impersonate the TLS handshake of a real, popular website, so that an active probe sees a normal site. This family of tools is widely used where other tunnels are blocked, notably in Iran, Russia and China.
- **AmneziaWG** (<https://docs.amnezia.org/>) is a fork of WireGuard that adds junk packets and randomised headers so that DPI cannot match WireGuard's fixed handshake pattern. The Amnezia VPN app can deploy it, and Xray, to a server you control.
- **Hysteria 2** (<https://v2.hysteria.network/>) is a QUIC-based proxy designed for lossy, throttled networks.

Your own server gives you access, not anonymity: the hosting company and anyone watching the server can see the traffic leaving it. If you need anonymity too, run Tor over the tunnel.

### Commercial VPNs
A VPN moves trust from your ISP to the VPN company. Standard OpenVPN and WireGuard are easy to fingerprint, and well-known VPN providers' IP ranges are routinely blocked. Some providers offer obfuscation modes; test them before you depend on them. Choose a provider whose ownership, jurisdiction and logging claims you have checked, preferably one that accepts anonymous payment.

## Choosing, in practice

1. **Find out what is blocked and how.** OONI Probe (<https://ooni.org/install/>) tests websites, messaging apps and circumvention tools from your connection and publishes the results, so you can see what others in your country are seeing.
2. **Keep more than one option installed.** Censors change tactics during protests and elections. A second and third tool, set up in advance, are worth more than a perfect first one.
3. **Get your bridges and keys before you need them.** Distribution channels are the first thing to be blocked.
4. **Match the tool to the need.** For reading news, anything that works is fine. For organising or communicating with sources, use Tor or tunnel Tor through your proxy.
5. **Mind the legal risk.** In some countries using circumvention tools is itself an offence, and police check phones at checkpoints. Consider how visible the apps on your device are.

## Publishing so that it cannot be blocked

Circumvention also works the other way: make your own content hard to censor. Publish an onion service, mirror on several hosts and jurisdictions, use content-addressed storage, and avoid depending on a single domain name. See [Publishing an Uncensorable Website](/guides/uncensorable-website/) and [Map: Censorship Resistance](/kb/map-censorship-resistance/).

## Sources

- GFW Report, *How China Detects and Blocks Shadowsocks* (ACM IMC 2020): <https://gfw.report/publications/imc20/en/>
- Wu et al., *How the Great Firewall of China Detects and Blocks Fully Encrypted Traffic* (USENIX Security 2023): <https://gfw.report/publications/usenixsecurity23/en/>
- Tor Project, *Circumvention* (Tor Browser manual): <https://tb-manual.torproject.org/circumvention/>
- OONI, Open Observatory of Network Interference: <https://ooni.org/>
- Project REALITY documentation (Xray-core): <https://github.com/XTLS/REALITY>
- Amnezia, *AmneziaWG*: <https://docs.amnezia.org/documentation/amnezia-wg/>
- IETF TLS Working Group, *TLS Encrypted Client Hello*: <https://datatracker.ietf.org/doc/draft-ietf-tls-esni/>
