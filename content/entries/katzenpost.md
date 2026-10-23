---
title: "Katzenpost"
slug: katzenpost
type: deep-dive
pillars: ["anonymity"]
readiness: experimental
description: "Katzenpost, a post-quantum mix network based on Loopix with hybrid key exchange built in: design, threat model and deployment status."
dek: "A research-grade, post-quantum-secure mix network. Loopix-based design with hybrid PQ key exchange built in from the start, federated authority structure, and a clear separation between transport (mix) and applications."
updated: 2026-09-04
created: 2026-04-25
origin: vault
source: "08-Mix-Networks/Katzenpost.md"
aliases: ["Katzenpost Mixnet"]
tags: ["katzenpost", "mixnet", "post-quantum", "anonymity", "sphinx", "deep-dive"]
---

## Position vs Nym

Both Katzenpost and [Nym](/kb/nym/) are Loopix-derived mix networks aiming to defeat a global passive adversary. They differ on:

| Aspect | Nym | Katzenpost |
|--------|-----|------------|
| Network type | Permissionless, stake-weighted | Federated; operators run mixes by agreement |
| Token economics | NYM token, on-chain stake | None — operator-funded |
| Post-quantum | Roadmap | Built-in (CTIDH + Kyber hybrid) |
| Maturity | Production network, consumer apps | Research-grade with deployments |
| Sphinx variant | Standard Sphinx | Modified Sphinx with PQ KEM |
| Apps | NymVPN, service providers | Catshadow (messenger), Reunion (key exchange) |

If Nym is "productize Loopix as a market", Katzenpost is "productize Loopix as a federation, with PQ-readiness baked in". Different bets on how anonymity infrastructure should be governed.

## Architecture

Same Loopix substrate as Nym:

- Three-tier mixnet with provider nodes at the edges.
- Continuous-time Poisson mixing per node.
- Sphinx-format packets with cover traffic and decoys.
- PKI managed by mix authorities (federation), with voted consensus per epoch.

Differences:

- Authorities are federated, not consensus-elected via stake. The honesty assumption is "majority of authorities honest in the federation".
- Provider nodes work much like Nym's gateways. They accept user packets and deliver to and from the mix.

## Post-quantum crypto

Katzenpost was designed with quantum-adversary resistance as a first-class concern. The Sphinx-PQ design uses:

- CTIDH (commutative-isogeny-based DH) and/or Kyber/ML-KEM as the asymmetric primitive for layered encryption.
- Hybrid mode. Classical (X25519) plus PQ KEM, so that breaking either independently doesn't compromise the system.

The reason: harvest-now-decrypt-later. Mixnet traffic is interesting to record now; if the cryptography is broken in the future, the historical metadata could be deanonymized retroactively. PQ-from-the-start is the only defense.

## Catshadow messenger

Katzenpost ships a reference messenger, **Catshadow**. Properties:

- E2E encrypted with Signal-like Double Ratchet, ratcheted over the mix transport.
- Per-message routing via separate mix paths. Long-term sender/recipient correlation broken.
- Synchronous and asynchronous delivery via the mixnet's Service Providers.
- Open-source Go implementation.

This is the "Signal but over a mixnet" pattern: Signal-grade content security, mixnet-grade metadata security. The UX is far less polished than Signal. Catshadow is more research artifact than consumer app.

## Reunion protocol

A Katzenpost contribution: **Reunion** is a contact-establishment protocol over the mixnet that doesn't require either party to know the other's address in advance. Useful for resilience scenarios where users want to find each other after a disruption without revealing identifiers to the network.

(The concept echoes [Briar](/kb/briar/)'s contact protocols but executed over a mixnet with stronger anonymity properties.)

## Threat model

Same as Loopix-based systems generally:

| Adversary | Status |
|-----------|--------|
| Global passive observer | Defeated under Loopix assumptions |
| Quantum adversary harvesting traffic | Defeated by hybrid PQ KEM |
| Compromised mix subset | Defeated by 3-layer plus cover traffic |
| Compromised authority | Federated honest-majority assumption |
| Endpoint malware | Out of scope |
| Active adversary modifying packets | Replay protection plus integrity |

The PQ angle is what makes Katzenpost distinctive: traffic recorded today survives the day a CRQC (cryptographically relevant quantum computer) appears.

## 2026 architecture notes

The current Katzenpost documentation describes a deployable federation made of:

- `dirauth` nodes: directory authorities that maintain the mixnet PKI and sign consensus documents.
- `server` nodes: configured as mix nodes, gateway nodes, or service nodes.
- Gateway/client connectors: the boundary between ordinary applications and the mixnet.
- Service nodes: endpoints inside the mixnet for storage, publication, blockchain access, or application-specific services.

Consensus currently operates in epochs; the admin guide describes 20-minute epochs where nodes upload descriptors, directory authorities vote, and clients retrieve signed consensus. Recommended PKI signatures include a hybrid `Ed25519 Sphincs+` option (`sphincs-shake-256f`), aligning the governance layer with the post-quantum design goal.

As of 2026-05-01, GitHub metadata for `katzenpost/katzenpost` showed an active, non-archived Go repository with recent pushes in late April 2026. Maturity assessment: active research/engineering project suitable for pilots and federated deployments, not consumer-scale infrastructure.

## Real-world deployments

- Mix testnet operated by Katzenpost developers and partners.
- OpenDoor (Hashcloak) provided mix capacity.
- Specific NGO and research deployments for journalism and activist scenarios.

Catshadow has been used in workshops and pilot deployments. Less consumer-visible than Nym's NymVPN, but technically interesting for the threat model and PQ readiness.

## Trade-offs

### Strengths

- Post-quantum from day one. The only deployed mixnet with this property.
- Federated authority model, which is different governance than stake-weighted.
- Includes a reference messenger (Catshadow) for the full E2E story.
- Reunion protocol for anonymous contact establishment.
- Clean separation between mix transport and applications.

### Limitations

- Research-grade. Smaller deployments, less polished tooling than Tor or Nym.
- Federation requires bootstrap trust. Permissioned set of operators.
- Catshadow UX is barebones.
- Documentation is academic-style, with fewer consumer guides.
- No token economics. Relies on operator funding for sustainability.

## Operational patterns

### Threat-model-extreme messaging

For a journalist with a multi-decade secrecy horizon (think nuclear or state-secret leaks), Catshadow's combination of mixnet anonymity plus PQ-secure key agreement is closer to "future-proof" than Signal-over-Tor today.

### Research benchmarking

Katzenpost is the de-facto reference implementation for mixnet research papers. It is the comparison baseline for Loopix variants, PQ Sphinx, and traffic-analysis attacks.

### Hybrid deployments

Katzenpost-style mix transport with custom application protocols on top, an emerging research pattern combining the best parts of MLS / Marmot with mixnet metadata defense.

## Recent developments (2024-2026)

- CTIDH integration for compact PQ key exchange in Sphinx.
- Kyber/ML-KEM hybrid completed; running in testnets.
- Catshadow updates: improved key management, multi-device exploration.
- Reunion protocol stabilized.
- Performance work for higher-throughput mixes under cover-traffic load.

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Long-term traffic correlation (GPA) | Loopix Poisson plus cover traffic |
| Compromised mix subset | 3-layer architecture |
| Compromised authority majority | Federation diversity is the assumption |
| Quantum cryptanalysis (future) | Hybrid PQ KEM in Sphinx |
| Endpoint compromise | Out of scope |
| Implementation bugs | Open source, ongoing audit |

## Comparison summary

| Dimension | Tor | I2P | Nym | Katzenpost |
|-----------|-----|-----|-----|------------|
| Threat: GPA | No | No | Yes | Yes |
| Threat: Quantum harvest | No | No | Roadmap | **Yes** |
| Latency | Sec | Sec | Sec | Sec-tens |
| Token model | None | None | NYM stake | None (federation) |
| Default messenger | None | None | None | Catshadow |
| Maturity | High | Medium | Medium | Research-deployed |

## September 04, 2026 Update — Replica Epic Closes; PKI Epoch Negotiation; Ping Loss Attribution

The 7-part replica-proxy congestion umbrella (#1091) that opened with the Aug 28 update **closes** this week:

- **#1099 (Sep 2, merged)** — `replica: document the proxy path as self-tuning (7 of 7)`. The replica proxy is now *self-tuning by design*: sweep budget = one `ProxyRequestTimeout`, read-repair gated on box-not-found, load-driven scheduling.
- **#1102 (Sep 2, merged)** — `replica: gate read-repair on box-not-found and fix shutdown ordering (5 of 7)`.
- **#1103 (Sep 2, merged)** — `replica: size the proxy sweep to one ProxyRequestTimeout (6 of 7)`.

Beyond the replica epic:

- **#1107 (Aug 29, merged)** — `docker: simplify port architecture and fix collision issues`. The local-dev docker mixnet had colliding ports across services; operator-facing fix.
- **#1105 (Sep 1, merged)** — **`client: agree on a PKI epoch instead of pinning one`**. Clients previously pinned a single PKI document, which left them out of sync on clock skew or missed round-trips. Now clients negotiate an *epoch* with the dirauth — more resilient to clock skew and network lag.
- **#1112 (Sep 2, merged)** — `client/transport: harden the websocket listener` (6-commit series): explicit `ws://host:port` listen required, Origin enforcement, close-bound-port-on-Close, `InsecureSkipVerify` opt-in flag, default loopback host, Accept/Close race + Origin coverage.
- **#1114 (Sep 3, merged)** — `server: instrument seven silent packet drop sites`. The first step toward *attribution*: before per-node loss estimation, count the drops per drop-site.
- **#1120 (Sep 3, merged)** — **Ping probabilistic packet loss attribution**. The payoff: compare service nodes too (not only mix layers), fix two ways the loss estimate was wrong (sample bias, CI), explain the attribution maths, attribute loss to nodes *with uncertainty stated*, and `client: report the route a message took to the thin client`. The combination of #1114 + #1120 is **a network-wide attribution layer for Katzenpost packet loss** — thin clients get probabilistic per-node loss estimates with stated confidence. This is the kind of measurement primitive mixnets need to defend against *selective-loss attacks* (a node dropping only specific senders/recipients to deanonymize them), where aggregate counts are insufficient.

See [Mix Networks Friday — September 04 2026 Weekly Update](/briefings/mix-networks/2026-09-04/) for the full weekly delta.

## Primary sources

- Katzenpost — [katzenpost.network](https://katzenpost.network)
- Source — [github.com/katzenpost/katzenpost](https://github.com/katzenpost/katzenpost)
- Piotrowska et al., *Loopix*, USENIX 2017.
- Hashcloak / Katzenpost developers, *Post-Quantum Sphinx*, technical reports.
- Reunion protocol specification — Katzenpost docs.
- *CTIDH: Faster Constant-Time CSIDH*, IACR 2021/633.
