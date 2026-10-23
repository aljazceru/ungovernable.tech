---
title: "HORNET"
slug: hornet
type: deep-dive
pillars: ["anonymity"]
readiness: research
description: "HORNET, a research design for high-speed onion routing at the network layer: how it reaches line-rate anonymity, and why it was never deployed."
dek: "HORNET (High-speed Onion Routing at the Network Layer) is a 2015 research design for line-rate, network-layer onion routing. It is not a deployed public anonymity network like Tor, I2P, Nym, or Katzenpost, but it is important because it explores the opposite end of the design space: very high throughput with low per-router state, intended to be built into future Internet routing architectures such as SCION-like path-aware networks."
updated: 2026-05-01
created: 2026-05-01
origin: vault
source: "08-Mix-Networks/HORNET.md"
aliases: ["High-speed Onion Routing at the Network Layer"]
tags: ["hornet", "onion-routing", "mix-networks", "anonymity", "scion", "network-layer-privacy"]
---

## Summary

Most anonymity systems pay for privacy with latency, relay state, and bandwidth overhead. [Tor](/kb/tor/) is low latency but still overlay-based: volunteer relays terminate TLS, maintain circuit state, and forward fixed-size cells in user space. Stronger packet-mix networks such as [Nym](/kb/nym/), [Katzenpost](/kb/katzenpost/), and [Loopix](/kb/loopix/) add intentional delays and cover traffic to resist global traffic analysis. HORNET asks a different question: could onion routing be moved closer to the network layer and forwarded at near-router speed?

The HORNET paper was published at ACM CCS 2015 by Chen Chen, Daniele E. Asoni, David Barrera, George Danezis, and Adrian Perrig. Its central idea is **stateless forwarding**: relay state is carried inside packet headers instead of stored in routers. Intermediate nodes use symmetric crypto to validate and transform headers, avoiding per-flow tables and allowing very high packet processing rates.

In ungovernable-tech terms, HORNET is useful as a design reference rather than a tool to run today. It shows what anonymous routing might look like if the underlying network exposed explicit paths, efficient packet-carried forwarding state, and router-level deployment hooks.

## Historical context

### Onion routing before HORNET

Early onion routing systems, including the work that became [Tor](/kb/tor/), were built as overlays on top of the existing Internet. That made deployment possible without ISP cooperation, but it came with costs:

- Circuits are maintained by overlay relays, not routers.
- Paths are long and indirect compared with native network routes.
- Throughput depends on volunteer relay capacity.
- Relays perform significant cryptographic and state-management work.

[Tor](/kb/tor/) solved the deployability problem: anyone can run the client and volunteers can run relays. HORNET did **not** try to solve immediate deployment. It assumed a more programmable, path-aware network substrate.

### The SCION / path-aware-networking influence

HORNET came out of the same research ecosystem as SCION, a clean-slate Internet architecture emphasizing path control, isolation domains, and packet-carried forwarding information. This matters because HORNET's design is much more natural in a network where senders can select paths and routers can process compact cryptographic forwarding headers.

That makes HORNET less like "a Tor competitor" and more like "an anonymity layer for a future Internet architecture." Its relevance to present-day freedom tech is architectural: if the Internet ever evolves toward path-aware routing, anonymity should be built into the forwarding layer rather than retrofitted as an overlay.

## How HORNET works

HORNET separates communication into two phases:

1. **Setup phase** — establishes anonymous session state between source and destination. The sender constructs an anonymous header path through selected nodes.
2. **Data transmission phase** — forwards packets using packet-carried forwarding segments, without per-session state stored at intermediate routers.

The key packet concept is the **anonymous header (AHDR)**. Instead of each relay keeping a circuit table entry like `circuit_id -> next_hop, keys`, HORNET puts encrypted forwarding state in the packet itself. Each relay can open only the part intended for it, verify integrity, derive the next transformation, and forward.

```text
Sender
  │  AHDR carries encrypted forwarding segments
  ▼
Node 1 ── validates/updates header ──► Node 2 ──► Node 3 ──► Destination
  ▲                                   ▲           ▲
  │ sees predecessor + successor only │           │
  └ no per-flow state table required ─┴───────────┘
```

Important properties:

- **Source-selected path**: the sender chooses the forwarding path, rather than relying on each hop to independently choose the next hop.
- **Symmetric crypto in data phase**: expensive public-key operations are kept out of the hot packet-forwarding path.
- **Packet-carried state**: routers do not store per-session circuit state.
- **Replay / integrity checks**: each hop can verify that its forwarding segment has not been modified.
- **Bidirectional channel support**: after setup, data can flow through the established anonymous channel.

## Threat model

HORNET is still a **low-latency onion-routing** design. That means it inherits the core limitation of [Tor](/kb/tor/): it does not aim to defeat a global passive adversary that can observe both ends of a flow and correlate timing and volume.

| Adversary | HORNET posture |
|---|---|
| Local observer near client | Hides destination if path entry is honest |
| Single compromised intermediate router | Sees predecessor/successor only, not full path |
| Compromised destination-side observer | Can observe destination traffic but not source if path remains honest |
| Global passive adversary | Not solved; timing/volume correlation remains possible |
| Malicious router modifying packets | Header integrity checks detect tampering |
| Endpoint compromise | Out of scope |

This places HORNET in the same broad anonymity family as [Tor](/kb/tor/) and [I2P](/kb/i2p/), not the stronger packet-mix family represented by [Nym](/kb/nym/), [Katzenpost](/kb/katzenpost/), and [Loopix](/kb/loopix/). Its novelty is performance and router-level statelessness, not global-observer resistance.

## Comparison with Tor, I2P, and mixnets

| Property | HORNET | [Tor](/kb/tor/) | [I2P](/kb/i2p/) | [Nym](/kb/nym/) / [Katzenpost](/kb/katzenpost/) |
|---|---|---|---|---|
| Primary goal | High-speed onion routing | Deployable low-latency anonymity | Anonymous internal overlay | Traffic-analysis resistance |
| Deployment | Research / future network layer | Production overlay | Production overlay | Production / research mixnets |
| Relay state | Packet-carried, stateless forwarding | Per-circuit relay state | Tunnel/router state | Mix queues, cover traffic, provider state |
| Latency | Designed low | Low to moderate | Low to moderate | Deliberately higher |
| Global passive adversary | Vulnerable | Vulnerable | Vulnerable / limited | Core threat model |
| Cover traffic | Not central | Limited padding | Some garlic/tunnel effects | Central design element |
| Best use case | Future router-level anonymity | Browsing, onion services | Anonymous in-network apps | Async messaging, wallet RPC, high-stakes metadata privacy |

HORNET is most compelling where throughput is the binding constraint and the adversary is not global. For dissidents, journalists, or wallets facing nation-state traffic analysis, the stronger trade-off is usually [Nym](/kb/nym/) or [Katzenpost](/kb/katzenpost/), accepting latency for cover traffic.

## Real-world status and maturity

HORNET is a **research design**, not a widely deployed network.

- **Paper maturity**: strong academic artifact; published at ACM CCS and widely cited in anonymity-network literature.
- **Implementation maturity**: no mainstream public HORNET network; code and prototypes have not become a user-facing ecosystem.
- **Operational maturity**: not production; no public relay set, browser integration, or package-manager install path comparable to [Tor](/kb/tor/) or [I2P](/kb/i2p/).
- **Architectural maturity**: valuable reference for SCION/path-aware-network researchers and for protocol designers thinking about stateless anonymous forwarding.

A useful way to remember it: HORNET is to anonymity routing what many clean-slate Internet proposals are to networking — technically clarifying, not immediately deployable.

## Use cases

Potential use cases if the required network substrate existed:

- **Router-level anonymous channels** for high-throughput traffic where Tor-style overlays are too slow.
- **Private path-aware networking** in SCION-like environments, especially within federated or institutional networks.
- **Anonymous service access** where the client needs low latency but does not require global passive adversary resistance.
- **Censorship-resistant routing research** exploring alternatives to overlay-only deployment.
- **Defense-in-depth for decentralized infrastructure**: private access to [Overview - Decentralized Compute](/kb/decentralized-compute/) or [Overview - Decentralized DNS](/kb/decentralized-dns/) services if path-aware routing becomes practical.

Near-term freedom-tech use is mostly educational: learn from the packet-carried-state design, then apply those ideas where the deployment assumptions are realistic.

## Trade-offs

### Strengths

- Very high performance target compared with overlay onion routing.
- Stateless forwarding reduces router memory pressure and per-flow state attacks.
- Clean separation between setup and fast data forwarding.
- Fits future path-aware routing architectures better than retrofitted overlays.
- Clarifies the distinction between anonymity from relay compromise and anonymity from traffic analysis.

### Limitations

- Not deployable on today's Internet without new network-layer support or specialized overlays.
- Does not solve global passive traffic correlation.
- Requires path selection and forwarding assumptions outside the reach of ordinary users.
- Less relevant for consumer privacy today than [Tor](/kb/tor/), [I2P](/kb/i2p/), [Nym](/kb/nym/), or [Katzenpost](/kb/katzenpost/).
- No mature public ecosystem of clients, relays, bridges, or operational docs.

## Evidence at a glance

| Item | Assessment |
|---|---|
| Core source | Chen et al., "HORNET: High-speed Onion Routing at the Network Layer," ACM CCS 2015 / arXiv:1507.05724 |
| Implementation status | Research prototypes only; no public production network |
| Development status | Conceptually important, not an active user-facing project |
| Threat model | Low-latency onion routing; not global passive adversary resistant |
| Main contribution | Packet-carried forwarding state enabling stateless high-speed onion routing |
| Best current role | Architecture reference for future Internet / SCION-style anonymity |

## Primary sources

- Chen, C., Asoni, D. E., Barrera, D., Danezis, G., and Perrig, A. (2015). "HORNET: High-speed Onion Routing at the Network Layer." ACM CCS 2015. https://dl.acm.org/doi/10.1145/2810103.2813628
- arXiv preprint: https://arxiv.org/abs/1507.05724
- SCION architecture context: https://www.scion-architecture.net/
- Tor comparison baseline: Dingledine, Mathewson, Syverson (2004), "Tor: The Second-Generation Onion Router." https://www.ndss-symposium.org/ndss2004/symposium-programme/tor-second-generation-onion-router/
