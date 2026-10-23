---
title: "Mix Networks Research and Deployment Tracker"
slug: mix-networks-tracker
type: reference
pillars: ["anonymity"]
description: "A tracker of deployed and near-deployed anonymity networks and mixnet research: Tor, I2P, Nym, Katzenpost, HOPR and the papers behind them."
dek: "A current-state tracker for the deployed and near-deployed anonymity-routing ecosystem: Tor, I2P, Nym, Katzenpost, HORNET, HOPR, and adjacent anonymity-network research. The point is not to crown one winner; it is to map which systems are usable today, which threat models they actually satisfy, and where freedom-tech builders should integrate next."
updated: 2026-06-12
created: 2026-05-08
origin: vault
source: "08-Mix-Networks/Mix Networks 2026 Research and Deployment Tracker.md"
aliases: ["Mixnet 2026 Tracker", "Anonymous Routing 2026 Tracker", "Mix Network Deployment Tracker"]
tags: ["mix-networks", "tor", "i2p", "nym", "katzenpost", "hopr", "anonymity", "censorship-resistance", "post-quantum"]
---

## Summary

The 2026 mix-network landscape has split into three practical tracks:

1. **Tor as the default anonymity substrate.** Tor remains the only anonymity network with mass adoption, broad censorship-evasion tooling, mature hidden services, reproducible metrics, and a hardened browser. The most important 2025–2026 development is not a new user-facing feature but the Rust rewrite, **Arti**, moving from client-only toward RPC, HTTP CONNECT, relay, directory-server, and onion-service work.
2. **I2P as a peer-to-peer private network under real Sybil pressure.** I2P continues to ship rapidly, including post-quantum work at the ratchet layer and fixes for SAMv3 clients such as Bitcoin and BitTorrent applications. The 2026 spam/Sybil episodes make I2P an important live laboratory for open-membership anonymity-network defense.
3. **Packet-mix systems trying to make global-passive-adversary defense usable.** [Nym](/kb/nym/) is pushing NymVPN, zk-credentials, decentralized payment, split tunneling, and post-quantum key-exchange experiments. [Katzenpost](/kb/katzenpost/) remains the strongest architecture reference for post-quantum federated mixnets. HOPR is the most visible incentivized RPC/data-exchange mixnet outside Nym.

The key freedom-tech conclusion: **low latency and strong traffic-analysis resistance are still in tension**. Tor/I2P are deployable defaults for censorship resistance and hidden services. Nym/Katzenpost are the right research and integration targets when the adversary can observe the network globally and metadata is the main asset being protected.

## Historical context and evolution

### Chaum to remailers

David Chaum's 1981 "Untraceable Communications" introduced the core idea: public-key encrypted messages are batched and transformed by mixes so observers cannot link input messages to output messages. The early practical descendants were remailers such as Mixmaster: high-latency, email-oriented, strong against simple traffic analysis, but too slow and specialized for general internet use.

### Onion routing becomes the usable compromise

Tor's 2004 design optimized for interactive traffic. It deliberately accepted a weaker traffic-analysis model so ordinary users could browse the web and developers could host reachable onion services. That compromise made Tor the most important deployed anonymity network, but also left a permanent warning label: a global passive adversary observing entry and exit traffic can correlate flows.

### Continuous-time packet mixing reopens the stronger threat model

Loopix (USENIX Security 2017) revived the mixnet path with Poisson delays, loop cover traffic, and Sphinx packets. Its influence is visible in [Nym](/kb/nym/) and [Katzenpost](/kb/katzenpost/): fixed-size packets, per-hop delay distributions, SURB-like reply mechanisms, and deliberate dummy traffic. These systems are slower and more expensive than Tor, but they target the threat Tor explicitly does not solve.

### 2025–2026: implementation hardening and productization

Recent developments are less about inventing brand-new primitives and more about hardening implementations:

- Tor is modernizing relay encryption with **Counter Galois Onion (CGO)** and moving toward embeddable Rust infrastructure via Arti.
- I2P is testing post-quantum ratchet-layer changes while dealing with hostile network conditions.
- Nym is converting a research-grade mixnet into a consumer product with NymVPN, custom DNS, split tunneling, ad blocking, decentralized pay-as-you-go access, zk-credentials, and post-quantum key exchange.
- Katzenpost is maintaining a research-first, post-quantum, federated model with detailed threat-model and literature documents.

## Evidence at a glance

| System | 2026 maturity | Main implementation signal | Threat model | Development signal observed 2026-05-08 | Best fit |
|---|---:|---|---|---|---|
| [Tor](/kb/tor/) / Arti | Production network; Arti 2.3.0 relay/directory/RPC in May 2026 | Tor Browser 15.0.13 (May 8, 2026 emergency), Arti 2.3.0 (May 7), Tails 7.7.3 emergency (May 12) | Local/partial observer; not global passive | Rapid emergency release cadence (15.0.11/12/13 within 10 days); Arti 2.3.0 syslog, protocol_warnings, tunnel-path RPC; CGO relay encryption in development | Censorship evasion, onion services, universal SOCKS/HTTP proxy |
| [I2P](/kb/i2p/) | Production P2P private network | Java I2P, i2pd, SAMv3 app APIs | Peer-to-peer internal anonymity; vulnerable to large Sybil/spam pressure | `i2p/i2p.i2p`: ~2.5k GitHub stars, non-archived, pushed 2026-05-07; I2P 2.12.0 released April 2026 | Anonymous in-network services, BitTorrent, Bitcoin app transport experiments |
| [Nym](/kb/nym/) | Production network + consumer VPN | Nym mixnet, NymVPN, zk-nyms | Global passive adversary under Loopix/cover-traffic assumptions | `nymtech/nym`: ~1.7k stars, non-archived Rust repo, pushed 2026-05-08; NymVPN v2026.7 shipped PQ key-exchange testing | Metadata-private RPC, async apps, high-stakes browsing, VPN-like UX |
| [Katzenpost](/kb/katzenpost/) | Research-grade / federated alpha | Go mixnet stack, hpqc, threat-model docs | Global passive + harvest-now-decrypt-later emphasis | `katzenpost/katzenpost`: active Go repo, pushed 2026-05-07; 2024 threat model/literature/hpqc docs remain primary references | Federated deployments, PQ mixnet research, app-specific privacy systems |
| [HORNET](/kb/hornet/) | Research design | arXiv / academic prototype | Low-latency network-layer onion routing, not deployed | No major deployment signal; remains architecture reference | Future path-aware network design, SCION-like anonymity layer thinking |
| HOPR | Active incentivized mixnet niche | `hoprnet/hoprnet`, node staking/cover traffic | Metadata-private point-to-point data exchange | `hoprnet/hoprnet`: active Rust repo, pushed 2026-05-07; roadmap and newsletter emphasize incentivized mixnet | RPC/data-exchange privacy experiments |

## 2026 deployment notes

### Tor and Arti

Tor's 2026 story is the **rapid-response release cadence**, not any single feature. Tor Browser 15.0.11 (April 28), 15.0.12 (May 7), and 15.0.13 (May 8) followed each other within 10 days — the latter two explicitly labeled emergency patches. The Tails 7.7.x series (7.7, 7.7.1, 7.7.2, 7.7.3 — April-May 2026) similarly reflects emergency kernel and Tor Browser/client fixes. This is not evidence of systemic failure; it reflects an active attacker environment with a responsive security team.

Arti 2.3.0 (May 7, 2026) continues the relay/directory/RPC development arc:
- `syslog` logging support when the `syslog` feature is enabled.
- `logging.protocol_warnings` config option to surface protocol violations.
- RPC API for tunnel-path inspection.
- Ongoing: Arti as relay, Arti as directory authority.
- **Flagged breaking change in next release**: `TorClient` will require explicit `Arc` wrapping. Downstream `arti-client` crate users should monitor [#2469](https://gitlab.torproject.org/tpo/core/arti/-/work_items/2469).

Counter Galois Onion (CGO) remains in development: when deployed, replaces legacy AES-CTR/SHA-1-derived 4-byte digest relay-cell encryption with a 16-byte authenticator, adding immediate forward secrecy and closing the tagging-attack vector. This is the most significant Tor protocol-level change since v3 onion services.

Practical interpretation:

- Use Tor today for browser anonymity, onion services, bridge/pluggable-transport censorship resistance, and default wallet/RPC hygiene.
- Track Arti for embedded applications, mobile apps, Rust stacks, and projects that need programmatic Tor control.
- Do not claim Tor defeats a global passive adversary; the traffic-correlation limitation is structural.

### I2P

I2P's 2026 releases are notable for two reasons: post-quantum experimentation and real-world hostile-network pressure. I2P 2.11.0 enabled post-quantum crypto at the ratchet layer by default and added mitigations for spam/Sybil conditions. I2P 2.12.0 continued PQ implementation work, improved interoperability, and fixed a SAMv3 lookup bug affecting applications such as Bitcoin and BitTorrent clients.

This makes I2P particularly relevant for [Overview - Decentralized DNS](/kb/decentralized-dns/), [Overview - Decentralized Compute](/kb/decentralized-compute/), and [Overview - Private Information Retrieval](/kb/private-information-retrieval/) use cases where the application is naturally internal to the anonymity network. I2P is not a clearnet-exit network in the Tor sense; its design center is private services inside the overlay.

Practical interpretation:

- Use I2P for eepsites, anonymous file sharing, and applications that can live entirely inside the overlay.
- Treat Sybil/spam resilience as a live operational question, not a solved property.
- Track SAMv3 because wallet, BitTorrent, and other application integrations often rely on it.

### Nym

Nym is the most productized attempt to bring Loopix-style mix networking to ordinary users. The 2026 update stream shows a clear product push:

- NymVPN v2026.7 shipped split tunneling beta for Windows, optional post-quantum key exchange in Fast mode via the **Lewes Protocol**, and secure authentication improvements on macOS following Cure53 audit recommendations.
- Nym's March/April 2026 update highlights split tunneling, ad blocking beta, custom DNS, decentralized pay-as-you-go access with zk-credentials, and a broader go-to-market campaign aimed partly at crypto users and censorship-affected countries.
- The post-quantum roadmap says Nym wants PQ key exchange across client-to-entry-node links, mixnode-to-mixnode links, NymVPN modes, and eventually the Sphinx packet layer.

The important distinction: NymVPN has both **Anonymous mode** and **Fast mode**. Anonymous mode is where the noise-generating mixnet matters. Fast mode is closer to a decentralized VPN / WireGuard-like model and now receives post-quantum handshake work first. These modes should not be conflated when reasoning about anonymity guarantees.

Practical interpretation:

- Use Nym for wallet RPC, sensitive asynchronous queries, and applications where seconds of latency are acceptable.
- Be careful when writing about NymVPN: Fast mode and mixnet mode are different threat models.
- Watch whether Nym can turn decentralized pay-as-you-go credentials into a real usage market rather than only token-staking infrastructure.

### Katzenpost

Katzenpost remains smaller than Nym but technically important. It is a federated, post-quantum-oriented mixnet stack with explicit threat modeling, Sphinx-based packet design, directory authorities, service connectors, and a Go implementation. The 2024 Katzenpost blog produced three durable primary-source anchors still relevant in 2026:

- A living **mixnet threat model** document.
- A **mixnet literature overview** with critical analysis of the academic design space.
- **hpqc**, a Go library for hybrid post-quantum cryptographic constructions such as hybrid KEMs and NIKEs.

Practical interpretation:

- Use Katzenpost as the architecture reference when post-quantum metadata privacy matters.
- Treat it as research-grade/federated infrastructure, not a mass-market consumer network.
- Study its docs before designing new mixnet messaging, voting, whistleblowing, or human-rights applications.

### HOPR and adjacent systems

HOPR positions itself as a decentralized, incentivized mixnet for privacy-preserving point-to-point data exchange. It is especially relevant to Web3 RPC, node-to-node messaging, and incentive-market experiments. At last review, `hoprnet/hoprnet` is active, non-archived, Rust-based, and recently pushed.

HOPR is not as central to this library as Tor, I2P, Nym, or Katzenpost, but it is worth tracking because economic incentives and cover traffic are one of the unresolved problems in open-membership mixnets.

## June 2026 update notes

### Nym: PQ key exchange in Fast mode, zk-credential progress

Nym's development through June 2026 continues the productization arc. The Lewes Protocol — Nym's post-quantum key exchange — is active in NymVPN Fast mode, making Nym one of the few deployed consumer VPN products with PQ handshakes in any form. The mixnet (Anonymous mode) PQ roadmap remains longer-term: adding PQ to Sphinx packet layer and mixnode-to-mixnode links is not yet shipped. The distinction between Fast mode ( WireGuard-like, PQ handshakes) and Anonymous mode (Loopix-style packet mixing, no PQ yet) remains the critical analytical line when evaluating NymVPN claims.

Nym's zk-credential system for decentralized pay-as-you-go access is advancing toward beta. The use case is anonymous subscription credentials that prove payment without revealing identity — relevant to privacy-preserving VPN access, anonymous messaging tier, and metadata-private service access. This is worth watching as a practical instantiation of anonymous credentials outside the academic literature.

### Katzenpost: built-in hybrid PQ as architectural differentiator

Katzenpost's most durable technical differentiator from Nym is its **built-in hybrid post-quantum stance** from the ground up. The `hpqc` Go library implements hybrid KEMs and NIKE constructions combining classical and post-quantum primitives, and the Katzenpost threat model explicitly factors in harvest-now-decrypt-later adversaries. By contrast, Nym's PQ roadmap is add-on and experimental; Katzenpost's PQ is structural.

For ungovernable system design, this means: if the primary threat is a state-level adversary that records all traffic today for future decryption, Katzenpost's architecture is more conservative by design. If the primary threat is metadata correlation by commercial surveillance, Nym's consumer productization and larger user base may be more relevant. Neither is universally superior; the choice depends on the specific threat model documented in the system design.

### Tor: Arti relay milestone approaching

Arti's path to relay-level deployment continues. The2.3.x series is adding RPC interfaces for tunnel-path inspection, syslog support, and protocol warning surfacing — infrastructure that makes Arti viable as a Rust-native Tor relay rather than only a client library. The next major milestone is Arti as directory authority, which would make the Rust rewrite functionally complete for all Tor roles. This matters for the ungovernable stack because Rust-based Tor infrastructure enables embedded, mobile, and programmatic use cases that the legacy C implementation does not easily support.

### I2P: SAMv3 fixes and persistent Sybil pressure

I2P 2.12.0's SAMv3 lookup bug fix (affecting Bitcoin and BitTorrent application integrations) is a reminder that I2P's application-layer APIs are as important as its network-layer anonymity properties. The ongoing Sybil/spam pressure on I2P continues to make it a live laboratory for open-membership anonymity-network defense. The project is active and responsive, but the fundamental challenge — that peer-to-peer networks with open membership are structurally vulnerable to Sybil attacks unless economic or social barriers exist — remains unsolved in production.

## June 12, 2026 — Friday Mixnet Research Update

### Tor: CGO deployment approaching, Arti relay milestone in sight

The most significant Tor development is the approach of Counter Galois Onion (CGO) deployment. The CGO replaces the legacy AES-CTR/SHA-1-derived 4-byte digest relay-cell encryption with a 16-byte authenticator and adds immediate forward secrecy. This is the most significant Tor protocol change since v3 onion services, and the design discussion on the tor-dev mailing list indicates implementors are working through the final edge cases before a network-wide flag day.

Arti's trajectory toward relay-level deployment continues. The 2.3.x series added RPC interfaces for tunnel-path inspection, syslog support, and protocol warning surfacing — infrastructure that makes Arti viable as a Rust-native Tor relay rather than only a client library. The next milestone is Arti as directory authority, which would complete the Rust rewrite for all Tor roles. For the ungovernable stack, this matters because Rust-based Tor infrastructure enables embedded, mobile, and programmatic use cases that the legacy C implementation does not support.

### I2P: continued active releases, Kimwolf afterglow

I2P continues its rapid release cadence. I2P 2.12.0 (April 2026) addressed performance and security issues with improved PQ interoperability and SAMv3 fixes. The post-quantum ratchet layer is now enabled by default since 2.11.0 (February 2026). The Kimwolf botnet incident in February — 700,000 hostile nodes — remains the most instructive recent case study in anonymity-network Sybil economics. I2P's response demonstrated that open-membership networks can recover from massive Sybil flooding, but the recovery required coordinated filtering and reputation adjustments that are themselves a target for manipulation.

### Nym: zk-credential beta, Lewes Protocol PQ in Fast mode, Anonymous mode still research

Nym's June 2026 development continues the productization arc. The Lewes Protocol — Nym's post-quantum key exchange — remains active in NymVPN Fast mode, making NymVPN one of the few consumer VPN products with PQ handshakes in any form. The distinction between Fast mode (WireGuard-like, PQ handshakes) and Anonymous mode (Loopix-style packet mixing, no PQ yet) remains the critical analytical line when evaluating NymVPN claims. Nym's zk-credential system for decentralized pay-as-you-go access is advancing toward beta, targeting anonymous subscription credentials that prove payment without revealing identity.

The mixnet layer (Anonymous mode) PQ roadmap remains longer-term. Adding PQ to the Sphinx packet layer and mixnode-to-mixnode links is not yet shipped. The core challenge is that the Sphinx packet geometry changes if PQ primitives replace X25519 for the per-hop key encapsulation — larger keys and different ciphertext sizes create distinguishable packet classes that could degrade anonymity. Outfox (ACM SIGCOMM 2025) addresses exactly this problem with a simplified PQ packet format for fixed-route layered mixnets, and Nym's PQ work will likely converge on similar architecture.

### Mixnet WoT: trust score visibility crosses into UI

A notable development since the last tracker update: multiple Nostr clients — Amethyst (Android), Primal, Coracle — now display WoT-based trust scores as user-visible metadata in Q1–Q2 2026. This is significant because WoT trust scoring is transitioning from developer-facing library features to end-user-visible product features. The practical implication: ordinary users see trust metadata surfaced by their clients, creating both better spam filtering and new design questions about trust presentation. Coracle's explicit message — "If you can't tell the difference between me and a scammer, use a nostr client with web of trust support" — signals that WoT visibility is becoming a product differentiator.

For mixnet operators, this has a parallel: if Nym or Katzenpost develop analogous trust scoring for mixnode operators, it could serve a similar anti-Sybil function. A trusted-mixnode list, weighted by stake or reputation, could provide users with stronger anonymity guarantees than arbitrary node selection — at the cost of introducing a new kind of centralization risk.

### Research frontier: MOCHA client anonymity, Outfox PQ packet format, Nox performance benchmarks

Three research developments from 2026 remain the reference points for mixnet advancement:

**MOCHA** (ePrint 2026/861, IH&MMSEC 2025): The key insight is that optimizing mixnet parameters for message anonymity alone can produce configurations where client anonymity is dangerously low. The paper provides an algorithm to simulate client anonymity for Loopix mixnets. For Nym and Katzenpost operators, MOCHA's finding means that Poisson rate μ, cover traffic ratio, and layer count tuning requires measuring both message and client anonymity — a more complex optimization than the Loopix paper implied.

**Outfox** (ACM SIGCOMM 2025): A simplified Sphinx variant for post-quantum layered mixnets, using a PQ KEM at the key encapsulation layer while preserving Sphinx's provable security properties (bitwise indistinguishability, per-hop unlinkability, tagging-attack resistance). Outfox is the architectural direction for any new mixnet design that wants PQ from scratch without the compatibility burden of the original Sphinx spec. Nym's PQ roadmap will likely converge on this approach.

**Nox** (2024-2025): Real performance benchmarking for a working Sphinx mixnet — 58.6µs per-hop processing mean, 100.1ms median end-to-end latency under Poisson mixing, 372.3 packets/second sustained throughput. These numbers establish the realistic performance envelope for Sphinx-based packet-mix networks.

### NymVPN Anonymous mode vs Fast mode: clarifying the threat model

The most common confusion in the Nym ecosystem remains the conflation of NymVPN's two modes:

| Property | Anonymous mode | Fast mode |
|----------|---------------|-----------|
| Mixnet | Yes (Loopix-style) | No |
| Cover traffic | Yes (noise-generating) | No |
| Latency | Seconds (Poisson mixing) | ~100ms |
| PQ key exchange | No (classical X25519) | Yes (Lewes Protocol, ML-KEM) |
| Threat model | Global passive adversary | Decentralized VPN |

NymVPN Anonymous mode is the strong mixnet — it defends against timing correlation from a global passive adversary. Fast mode is closer to a decentralized WireGuard with post-quantum handshakes. Claiming Fast mode provides mixnet-grade anonymity is wrong. Conversely, dismissing NymVPN because one mode doesn't have PQ is also wrong if the Anonymous mode's threat model is what you need.

For the ungovernable stack: use Anonymous mode for wallet RPC privacy, sensitive browsing, and metadata-critical applications where seconds of latency are acceptable. Use Fast mode for general VPN-like protection with PQ handshakes. Do not conflate them when writing about Nym's threat model.

### HOPR: Sphinx + probabilistic payments, RPC/data-exchange focus

HOPR (https://github.com/hoprnet/hoprnet) remains active as the most visible incentivized RPC/data-exchange mixnet outside Nym. It uses Sphinx packets with probabilistic payments — nodes earn HOPR tokens for relaying traffic, which creates economic incentives for honest participation. The model is different from Nym's stake-weighted mixnode selection: HOPR pays per-packet rather than per-stake. The operational challenge for both is the same: economic incentives can be gamed by adversaries with sufficient capital, and the cover traffic requirement means both networks need enough real traffic to make dummy traffic indistinguishable. Watch whether either network achieves sustainable traffic levels without token subsidies.

## Use cases and trade-offs

| Use case | Best current option | Why | Trade-off |
|---|---|---|---|
| Anonymous web browsing | [Tor](/kb/tor/) Browser | Mature browser fingerprinting defenses, bridges, pluggable transports | Vulnerable to global timing correlation; blocked in some jurisdictions |
| Hidden services | [Tor](/kb/tor/) onion services or [I2P](/kb/i2p/) eepsites | Mature service-discovery models and internal routing | Operational security still matters; server misconfiguration deanonymizes |
| Wallet/RPC privacy | [Tor](/kb/tor/) today; [Nym](/kb/nym/) where supported | Hides wallet IP from RPC provider and network observer | Tor is low latency but weaker against global observers; Nym is stronger but slower |
| Async messaging / dead drops | [Nym](/kb/nym/) or [Katzenpost](/kb/katzenpost/) | Packet mixing and cover traffic fit async traffic | Latency, scarce bandwidth, smaller anonymity sets |
| Anonymous BitTorrent / internal services | [I2P](/kb/i2p/) | Designed for in-network services and file sharing | Smaller ecosystem and persistent Sybil/spam risk |
| Post-quantum metadata privacy | [Katzenpost](/kb/katzenpost/) today; Nym roadmap to watch | Katzenpost built around hybrid PQ assumptions; Nym adding PQ layers | PQ does not solve timing/endpoint leaks; careful threat-modeling required |
| Censorship resistance at scale | [Tor](/kb/tor/) bridges, Snowflake, WebTunnel | Largest deployed circumvention ecosystem | Bridge discovery/blocking is an arms race |

## Open research questions

1. **How much cover traffic is enough?** Loopix-style guarantees depend on real cover-traffic distributions and enough honest participants. Production networks need empirical anonymity-set measurement, not only protocol proofs.
2. **Can token incentives buy honest mixing without centralizing stake?** Nym and HOPR both test economic designs. The risk is that stake weighting or delegation creates a small de facto operator set.
3. **How should mixnets expose APIs to apps?** SOCKS is universal but semantically weak. RPC, HTTP CONNECT, service-provider APIs, and embedded libraries may give applications better privacy defaults.
4. **Can post-quantum upgrades be deployed without new fingerprinting?** PQ handshakes, larger keys, and optional toggles can create distinguishable client classes if rollout is uneven.
5. **What is the right user experience for strong anonymity?** If mixnet mode is too slow, users switch to fast modes. The product challenge is making the safe path tolerable for realistic workflows.

## Primary sources

### Project documentation and release notes

- Tor Project — Arti 2.3.0 release: https://blog.torproject.org/arti_2_3_0_released/
- Tor Project — Tor Browser 15.0.13: https://blog.torproject.org/new-release-tor-browser-15013/
- Tor Project — Tor Browser 15.0.12: https://blog.torproject.org/new-release-tor-browser-15012/
- Tor Project — Tails 7.7.3 emergency: https://blog.torproject.org/new-release-tails-7_7_3/
- Tor Project — Counter Galois Onion announcement: https://blog.torproject.org/introducing-cgo/
- Tor announcements index: https://blog.torproject.org/category/announcements/
- I2P 2.11.0 release: https://i2p.net/en/blog/2026/02/09/i2p-2.11.0-release/
- I2P 2.12.0 release: https://i2p.net/en/blog/2026/04/20/i2p-2.12.0-release/
- NymVPN v2026.7 release: https://nym.com/blog/nymvpn.v2026.7
- Nym March/April 2026 update: https://nym.com/blog/nym-in-march-april-2026
- Nym post-quantum roadmap: https://nym.com/blog/nym-post-quantum-roadmap
- Nym Lewes Protocol post-quantum key exchange: https://nym.com/blog/lewes-protocol-post-quantum
- Katzenpost website and docs: https://katzenpost.network/
- Katzenpost blog index: https://katzenpost.network/blog/
- HOPR roadmap: https://hoprnet.org/roadmap

### Repositories checked for activity

- Nym: https://github.com/nymtech/nym
- I2P Java implementation: https://github.com/i2p/i2p.i2p
- i2pd C++ implementation: https://github.com/PurpleI2P/i2pd
- Katzenpost: https://github.com/katzenpost/katzenpost
- HOPR: https://github.com/hoprnet/hoprnet

### Foundational papers

- Chaum, David. "Untraceable Communications." Communications of the ACM, 1981. https://dl.acm.org/doi/10.1145/1008908.1008920
- Dingledine, Roger; Mathewson, Nick; Syverson, Paul. "Tor: The Second-Generation Onion Router." USENIX Security 2004. https://www.usenix.org/legacyurl/13th-usenix-security-symposium-151-technical-paper
- Danezis, George; Goldberg, Ian. "Sphinx: A Compact and Provably Secure Mix Format." IEEE S&P 2009.
- Piotrowska et al. "The Loopix Anonymity System." USENIX Security 2017. https://www.usenix.org/conference/usenixsecurity17/technical-sessions/presentation/piotrowska
- Chen et al. "HORNET: High-speed Onion Routing at the Network Layer." 2015. https://arxiv.org/abs/1507.05724
