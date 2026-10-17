---
title: "Tor"
slug: tor
type: deep-dive
pillars: ["anonymity", "circumvention"]
readiness: battle-tested
description: "Tor, the most widely used anonymity network: three-hop onion routing, onion services, bridges and pluggable transports, and what it does not protect."
dek: "The reference low-latency anonymity network. Three-hop onion-routed circuits, around 7000 relays, used by millions every day for browsing, hidden services, and as transport for many of the other systems in this library."
updated: 2026-09-04
created: 2026-04-25
origin: vault
source: "08-Mix-Networks/Tor.md"
aliases: ["Tor Project", "Onion Routing"]
tags: ["tor", "onion-routing", "anonymity", "mix-networks", "hidden-services", "deep-dive"]
---

## What Tor provides

Tor sits between VPNs and mixnets. Slower than a VPN, faster than a mixnet, and usable enough that millions of people actually run it daily. The design choices:

- Three-hop onion routing. Each relay only knows its predecessor and successor. The entry node knows the user, the exit node knows the destination, no single node sees both.
- TLS to relays. Public-key directory authorities sign the consensus that lists relay identities and bandwidth weights.
- v3 hidden services. A server with no IP address, addressable through a 56-character base32 of an Ed25519 public key.
- Pluggable transports. Obfs4, meek, snowflake, all aimed at deep-packet-inspection in censoring countries.
- Bridges. Unpublished relay IPs for users in countries that block the public Tor network.

What Tor is not:

- A defense against a global passive adversary. Timing correlation between entry and exit is possible in principle.
- A high-bandwidth network. Typical 1-10 Mbps, latency in the seconds.
- A complete metadata-protection answer. Size and timing patterns leak under analysis.

For traffic-analysis defense beyond Tor's threat model, see [Nym](/kb/nym/) and [Katzenpost](/kb/katzenpost/).

## Circuit construction

```
Client ── TLS ── Guard ── ─── Middle ── ─── Exit ── ─── Destination
                  ↑           ↑          ↑
             knows client   knows nothing  knows destination
                            of either
```

Each hop is a layered TLS-over-AES tunnel. The client picks circuits from the consensus, builds them lazily as needed, and rotates them roughly every 10 minutes (or per-stream).

### Guards

The first hop in a circuit is a *guard*. To resist long-term Sybil-based deanonymization, clients pin a small set of guards (usually one) for months. If the guard is honest, attackers above the guard never see your traffic. If the guard is malicious, correlation is possible, but the attack is bounded to one node.

### Exit policies

Exits voluntarily declare which destination ports they will forward. Most allow web traffic, some only specific ports. Operating an exit relay carries legal exposure in many jurisdictions, so the exit set is smaller than the relay set.

## v3 hidden services

A v3 onion service is a server reachable only via Tor:

- The server generates an Ed25519 keypair.
- The address is `base32(Ed25519-pubkey ‖ checksum ‖ version) + ".onion"`, 56 characters before `.onion`.
- The server publishes *introduction points* in the Tor directory (short-lived).
- The client picks a *rendezvous point* and tells the introduction point to ask the service to meet there.
- Both sides connect to the rendezvous through three-hop circuits, six hops end-to-end inside Tor.

Properties:

- Self-authenticating. The address proves the key.
- No CA, no DNS. Trust binds to the Ed25519 public key.
- Hidden by default. The server's IP is not revealed to clients or to the network.
- Client authorization. v3 supports an explicit allowlist of authorized client keys.

Common uses: SecureDrop, the Tor Project's own services, Briar's transport, ricochet-refresh, Nym's clearnet ingress, Cwtch peers.

## Pluggable transports and bridges

When a network blocks Tor (China, Iran, others), pluggable transports disguise Tor traffic:

| Transport | What it looks like |
|-----------|--------------------|
| **obfs4** | Random-looking bytes; defeats simple DPI |
| **meek** | TLS to a CDN (Azure, Fastly), with the real Tor request hidden in HTTPS |
| **snowflake** | WebRTC peer-to-peer; volunteers run Snowflake proxies in browsers |
| **WebTunnel** | HTTPS-resembling websocket flow, plausibly deniable |

Bridges are non-public Tor relays whose IP isn't in the consensus. They are distributed via BridgeDB (email, web, Telegram). Censors who learn a bridge's IP can block it; new bridges are issued.

## Protocol-level details

- Cell size: fixed 514-byte cells defeat trivial size-based traffic analysis.
- Padding: Tor v3 padding negotiation reduces visible inactive-period inference.
- TLS 1.3 between relays.
- Directory authorities: about 10 trusted operators that vote on consensus hourly.
- Bandwidth weighting: clients prefer higher-bandwidth relays, with weighting derived from authority measurements.

## Trust model

| Trust assumption | Required? |
|------------------|-----------|
| At least one of three hops not adversarial | Yes, for unlinkability |
| Directory authorities do not collude | Yes |
| Crypto primitives unbroken | Yes (Ed25519, Curve25519, AES-128) |
| Network not globally observable end-to-end | Implicit in the low-latency model. Tor is **not** safe against an adversary observing both ends with traffic analysis |

For threat models that include a global passive adversary, see [Nym](/kb/nym/), [Katzenpost](/kb/katzenpost/), and the [MOC - Metadata Privacy](/kb/map-metadata-privacy/) discussion of cover-traffic defenses.

## 2026 maintenance status

Tor Browser 15.0.13 (2026-05-08) is the latest stable release, an emergency update following 15.0.12 and 15.0.11 in rapid succession. The 15.0.x series tracks Firefox ESR 140.x; 15.0.13 backports security fixes from Firefox and addresses a Tor Browser-specific vulnerability. The release cadence (three emergency patches in one week) reflects ongoing pressure on the browser attack surface rather than a systemic crisis.

Arti 2.3.0 (2026-05-07) continues the relay/directory/RPC development trajectory. New in 2.3.0: `syslog` logging support, a `logging.protocol_warnings` option to surface protocol violations, RPC API additions for tunnel-path inspection, and ongoing work toward Arti-as-relay and Arti-as-directory-authority. The minimum macOS version bumped to 10.14. A breaking change is flagged for the next release: `TorClient` will explicitly require `Arc` wrapping instead of implicit `Arc`-like semantics — downstream `arti-client` crate users should monitor [#2469](https://gitlab.torproject.org/tpo/core/arti/-/work_items/2469).

Tor remains actively maintained rather than "finished infrastructure." The pattern is clear: Rust rewrite (Arti) absorbs new protocol features (CGO, relay mode, directory authority) while Tor Browser keeps pace with Firefox security updates and emergency patches. The Tor Project's 2026 release cadence — particularly the Tails 7.7.x emergency series in April-May and the Tor Browser 15.0.11/12/13 rapid-response updates — reflects a live, responsive security posture under active attack.

Arti, the Rust implementation of Tor, is the strategic integration path for wallets, messengers, and embedded apps. It matters because many freedom-tech tools want Tor as a library instead of requiring users to manage a separate daemon. Maturity assessment: C Tor remains the production network implementation; Arti is increasingly important for embedding and future codebase safety.

## Operational patterns

### Tor Browser

The reference client. Standardized fingerprint to reduce browser-fingerprinting differentiation across users. Uses HTTPS-Everywhere by default and NoScript on the Safer/Safest security levels.

### System-wide Tor

`SocksPort 9050` exposed locally; configure individual apps to use SOCKS5 to that. Pair with proxychains for CLI tools.

### Whonix and Tails

OS-level Tor enforcement. Whonix has two VMs (a gateway that routes everything via Tor, a workstation with no direct internet). Tails is an amnesic Live USB.

### onion-only services

Services bound to a `.onion` only, with no clearnet listener. Pair with [Overview - Decentralized DNS](/kb/decentralized-dns/) alternatives for double-resistance.

### Tor + attested LLM endpoint

Confidential-AI inference reachable only at a `.onion`, with attested TLS pinned in the enclave. The pattern is documented in [MOC - Composing Primitives](/kb/map-composing-primitives/).

## Trade-offs

### Strengths

- Mature. Over 20 years; the largest anonymity network ever deployed.
- Wide app support. SOCKS5 makes integration trivial.
- Hidden services. Server-side anonymity, not just client-side.
- Robust against censorship with bridges plus pluggable transports.
- Open, auditable, transparent.

### Limitations

- Low latency is a feature for usability, a weakness for traffic analysis.
- Exit-policy bottleneck. Fewer exits than entry relays creates congestion and exposure.
- A compromised exit can MITM unencrypted traffic. Use HTTPS or authenticated protocols.
- State-sponsored attacks. Tor is in scope for major SIGINT agencies, so it is not the right tool for targets of sustained nation-state attention without additional layering.
- Bandwidth. A typical Tor circuit isn't suitable for video, large transfers, or low-latency real-time work.

## Attack surface

| Attack | Description | Mitigation |
|--------|-------------|------------|
| Traffic confirmation | Adversary observes ingress and egress | Layer with mixnet (Loopix-style) for cover-traffic defense |
| Compromised guard | Long-term observation by adversary's guard | Guard pinning limits scope; use bridges for an additional layer |
| Compromised exit | MITM of unencrypted traffic | Always use TLS or authenticated channels at the app layer |
| Sybil consensus voting | Authorities compromised | Multi-authority threshold; geographic diversity |
| DoS | Resource exhaustion attacks on relays | Rate limiting, priority classes (research and production) |
| Browser fingerprint | Differentiation across users | Tor Browser standardization; Safer security level |
| Side-channel via app | DNS leaks, WebRTC, etc. | Tor Browser plus system-wide Tor; avoid leaking apps |

## Recent developments (2024-2026)

- Arti, the Rust rewrite of the Tor client, is on a production roadmap. Lighter and more embeddable.
- Onion-balancing improvements for high-traffic hidden services.
- WebTunnel, a newer pluggable transport for HTTPS-like camouflage.
- Snowflake, broadly adopted by NGOs. WebRTC-based circumvention in browsers.
- PoW for hidden-service DoS, which works around resource-exhaustion attacks during high-demand periods.
- Vanguards-Lite, a second-layer guard discipline for hidden services.

## September 04, 2026 Update — Arti 2.6.0; Tor Browser 15.0.21; 0.4.8 EOL; Tails 2-week cadence

Three Tor Project releases land within four days (Sep 1–3), all interlocking:

- **Arti 2.6.0 (Sep 1)** — *Counter Galois Onion* and *Congestion Control* now **always-on** in `arti`. Both were opt-in/experimental in 2.5.x; promoting both in the same release is the prerequisite for using Arti as a relay — a relay that only understood CGO traffic and a client that only understood pre-CGO traffic would silently drop each other's cells. Other 2.6.0 work: document parsing, directory mirror support, DNS stream handling, RPC-based configuration. The relay + dirauth build-out continues.
- **Tor Browser 15.0.21 (Sep 1)** — rebases stable onto **Firefox 140.15.0esr**, OpenSSL 3.5.8, NoScript 13.6.32.1984, Go 1.25.14, GeckoView 140.15.0esr; backports Firefox 155 security fixes; parent-process TorConnect redirection fix; 32-bit Linux retirement message adjusted.
- **Tor Browser 16.0a11 (Sep 2)** — alpha that will become 16.0 stable; with the new cadence, 15.0.21 and 16.0a11 land in the same week.
- **Tails 7.12 (Sep 3)** — *first release on Firefox's new 2-week release cadence*. Electrum 4.8.1, Tor Browser 15.0.21 inside. **Tails, Tor Browser, and Firefox now ship on the same clock**, so the lag from "Firefox security release" to "Tails users get the patch" drops from ~4–6 weeks to ~2 weeks.
- **Tor 0.4.8 deprecation cut-off (Sep 1)** — un-upgraded relays, onion services, and Tor-embedded apps lose connectivity to the network once the deprecated directory fields are removed. Tor Project guidance is "upgrade to Tor 0.4.9 series or later before September 1, 2026." Tor Browser users are unaffected directly.

**Network metrics (Sep 1)**: 10,137 relays (Exit 3,268 / Fast 9,987 / Guard 6,155 / HSDir 3,015 / Stable 9,059). Aug 31 dipped to 10,060 — likely the 0.4.8 EOL taking its first tranche — with Sep 1 partial recovery to 10,137. The network has absorbed the cut without drama.

See [Mix Networks Friday — September 04 2026 Weekly Update](/briefings/mix-networks/2026-09-04/) for the full weekly delta.

## Primary sources

- Dingledine, Mathewson, Syverson, *Tor: The Second-Generation Onion Router*, USENIX Security 2004. [svn-archive.torproject.org/svn/projects/design-paper/tor-design.pdf](https://svn.torproject.org/svn/projects/design-paper/tor-design.pdf)
- Tor Specification — [spec.torproject.org](https://spec.torproject.org)
- *Onion Service v3 Specification* — same site.
- The Tor Project — [torproject.org](https://www.torproject.org)
- Arti — [gitlab.torproject.org/tpo/core/arti](https://gitlab.torproject.org/tpo/core/arti)
