---
title: "Loopix"
slug: loopix
type: deep-dive
pillars: ["anonymity"]
readiness: research
description: "Loopix, the 2017 design that revived mix networks with continuous-time mixing and three kinds of cover traffic, and the basis of Nym and Katzenpost."
dek: "The 2017 academic design that revived high-latency mix networks. Continuous-time Poisson mixing plus three classes of cover traffic gave the first deployable mixnet with provable bounds against a global passive adversary. Loopix itself never shipped as a production system — its descendants did."
updated: 2026-10-25
created: 2026-04-26
origin: vault
source: "08-Mix-Networks/Loopix.md"
aliases: ["Loopix Anonymity System", "Poisson Mix"]
tags: ["loopix", "mix-networks", "poisson-mixing", "anonymity", "sphinx", "deep-dive", "research", "mocha"]
---

## Definitional

Loopix is the anonymity system specified in:

> Piotrowska, A., Hayes, J., Elahi, T., Meiser, S., Danezis, G. *The Loopix Anonymity System*. USENIX Security 2017.

It synthesizes ideas that had circulated in the mixnet research community for decades — Chaum's original mix concept, Stop-and-Go mixes (Kesdogan et al., 1998), [Mixminion and Mixmaster](/kb/mixminion-and-mixmaster/)'s pool mixes, [Sphinx Packet Format](/kb/sphinx-packet-format/) for indistinguishable packets — into a single design with formal anonymity guarantees and reasonable performance.

The combination is what made Loopix tractable: each individual technique was known, but the integrated system delivered (a) low-enough latency for messaging-style use cases (seconds, not hours), (b) tractable bandwidth via per-link constant-rate cover traffic, and (c) provable anonymity bounds against an adversary watching every link in the network.

## Architecture

### Stratified topology

Mix nodes are arranged in a fixed number of layers (the paper uses three). Every packet traverses exactly one node from each layer in order:

```
   Layer 1            Layer 2            Layer 3
   ┌──┐ ┌──┐ ┌──┐    ┌──┐ ┌──┐ ┌──┐    ┌──┐ ┌──┐ ┌──┐
   │M1│ │M2│ │M3│    │M4│ │M5│ │M6│    │M7│ │M8│ │M9│
   └──┘ └──┘ └──┘    └──┘ └──┘ └──┘    └──┘ └──┘ └──┘

Provider →   any L1   →   any L2   →   any L3   → Provider
```

Stratification serves two purposes:

1. **Anonymity-set lower bound**. Each layer contributes its own mixing; even if some layers are partially compromised, the remaining layers preserve anonymity.
2. **Predictable load**. Routing is balanced across the layer, simplifying capacity planning.

Edge **provider nodes** terminate connections from senders and recipients, store messages for offline recipients, and inject/eject packets from the mix layers.

### Continuous-time Poisson mixing

Each mix node, on receiving a Sphinx packet, samples a delay from an exponential distribution with parameter μ and forwards the packet after that delay. This is the *Poisson mix* (or "stop-and-go" with exponential service times).

The key property: at steady state, the order of packets entering and leaving a mix is statistically independent of arrival times. A global observer who sees `n` packets enter and `n` packets leave cannot do better than uniform random matching, asymptotically.

Compared to **batched mixes** (Mixmaster), Poisson mixing provides:

- Lower per-packet latency at moderate traffic (no waiting for batch fill).
- Continuous bandwidth, not bursty.
- Simpler analysis under standard queuing-theory tools.

The trade-off: anonymity bounds depend on having enough simultaneous in-flight packets at each mix. Cover traffic ensures this.

### Three classes of message

Loopix introduces a clean taxonomy of packet types:

- **Real**. The actual user payload.
- **Loop (sender's loop)**. The sender constructs a packet that routes back to themselves. Used both as cover traffic and as an integrity check (the sender notices if loops fail to return, signaling network problems or attacks).
- **Drop (cover traffic)**. The sender constructs a packet that routes to a random destination and is discarded there. Pure cover traffic with no functional payload.

Mix nodes also generate their own **mix loops**: packets that route around the network and return to the originating mix. This keeps every link populated even when end-to-end traffic is sparse.

The three-message design gives Loopix two properties simultaneously:

- **End-to-end indistinguishability**. To an adversary, sender→recipient real traffic looks identical to sender→sender loops or sender→random drops.
- **Continuous link entropy**. Every link carries traffic at all times, so timing patterns at the link level reveal nothing.

## Anonymity guarantees

The Loopix paper proves bounds in the *anonymity trilemma* sense (later formalized by Das et al., 2018):

- **Sender anonymity**. Given a target message at the recipient, the adversary's posterior over possible senders is bounded close to uniform over the active sender set, under stated assumptions.
- **Recipient anonymity**. Symmetric.
- **Sender-recipient unlinkability**. The strongest property: no advantage in linking a known sender to a known recipient.

Stated assumptions:

- The adversary is global passive (sees all links) but does not control mix nodes.
- The user generates cover traffic at the specified rate.
- Sphinx packets are computationally indistinguishable.
- Mix delays are correctly sampled from the exponential distribution.

Active adversaries (controlling some mix nodes, dropping packets, etc.) get weaker but still nontrivial bounds, depending on the fraction of corrupt mixes per layer.

## Bandwidth efficiency vs Mixmaster

Mixmaster batched messages and required minutes-to-hours of latency to accumulate enough cover for meaningful anonymity. The bandwidth cost per delivered message was high (many real-message-equivalents of dummies).

Loopix's continuous design achieves comparable anonymity at:

- **Order-of-seconds end-to-end latency** with three layers and modest μ.
- **Constant-rate cover traffic per user** rather than per-message dummy padding.
- **No batch synchronization** between users.

The paper measures bandwidth-anonymity trade-offs empirically; for plausible parameter choices, Loopix delivers messaging-grade latency with bandwidth costs in the kilobits-per-second range per active client. Far higher than VPN, far lower than Mixmaster's effective overhead.

## MOCHA: Client anonymity vs message anonymity (IH&MMSEC 2025 / ePrint 2025/861)

The Loopix paper proved anonymity bounds for *messages* traversing the mixnet. MOCHA (Mixnet Optimization Considering Honest Client Anonymity, IH&MMSEC 2025) revealed that optimizing for message anonymity alone can produce configurations where *client* anonymity is dangerously low — and the two can diverge significantly.

The core insight: the Loopix anonymity bound measures whether an observed output message can be linked to its input message. It does not directly bound whether a *sender's identity* (the human behind the keyboard) can be distinguished from the set of all possible senders. These are different questions. Message anonymity provides an upper bound on client anonymity, not a tight lower bound.

MOCHA's concrete findings:

- **Client anonymity can be much worse than message anonymity suggests.** In simulations with insufficient client populations, MOCHA found client anonymity entropy dramatically lower than the message anonymity metric would predict. The gap is worst when the number of active senders is small relative to the total anonymity set.
- **MOCHA proposes a multimixing strategy** to address this: mixing varied traffic types with different mixing characteristics together, so that a client's aggregate output pattern is not trivially distinguishable from the background.
- **For Nym and Katzenpost operators**, this means Poisson rate μ, cover traffic ratio, and layer count tuning must jointly optimize for *both* message and client anonymity. Using message-anonymity simulators alone to set parameters is insufficient and potentially dangerous.
- **The implication for parameter design**: Nym's empirical simulator work (see their [empirical privacy study](https://nym.com/blog/empirical-study-of-privacy)) specifically measures end-to-end entropy and sender-receiver unlinkability — metrics closer to client anonymity than message anonymity alone. MOCHA validates that this approach is correct.

MOCHA is the reason the [Mix Networks 2026 Research and Deployment Tracker](/kb/mix-networks-tracker/) flags parameter tuning as a live research question for production mixnets.

**Primary source**: ePrint 2025/861, "MOCHA: Mixnet Optimization Considering Honest Client Anonymity," IH&MMSEC 2025. [eprint.iacr.org/2025/861](https://eprint.iacr.org/2025/861)

## What Loopix does *not* solve

- Endpoint compromise. Out of scope for any anonymous communication system.
- Application-layer fingerprinting. The mixnet anonymizes packets; an app that includes user identifiers in payloads is on its own.
- Long-term intersection attacks. If a sender uses the system from the same identity over months, statistical intersection of who-was-online-when can still narrow the set. Loopix mitigates but does not eliminate this; the cover traffic and continuous nature help substantially.
- Scaling to billions of users. The provable bounds depend on the active sender set; very small populations weaken anonymity regardless of design.
- Latency-sensitive interactive use. Voice, video, or real-time gaming are out of reach.

## Influence and descendants

Loopix has not been deployed as a standalone production system. Its design lives on through:

- [Nym](/kb/nym/) — productized Loopix with stake-weighted node selection and the NYM token. Mainnet since 2022.
- [Katzenpost](/kb/katzenpost/) — Loopix-derived federation with post-quantum Sphinx and the Catshadow messenger.
- [HOPR](/kb/hopr/) — Sphinx + cover traffic with a different incentive layer.
- Research follow-ups: HOPR Project's research output, the Mixim simulator for mixnet topology research, and post-Loopix designs like *SoK: Anonymous Communication* (Shirazi et al., 2018) and Vuvuzela's evolution.

The paper's lineage is Chaum 1981 → Mixmaster 1995 → Mixminion 2003 → Loopix 2017 → Nym/Katzenpost 2018-2026. The 2017 contribution was making the entire pipeline tractable enough for engineers to build on.

## Threat model

| Adversary | Status |
|-----------|--------|
| Local / ISP observer | Defeated. Constant-rate Sphinx traffic |
| Compromised mix subset | Defeated up to threshold; bounds degrade gracefully |
| Global passive observer | Defeated under stated parameters. The headline claim |
| Global active adversary | Partial. Replay protection plus integrity; some attacks remain open research |
| Endpoint compromise | Out of scope |
| Long-term statistical adversary | Mitigated by cover traffic; not eliminated |

## Trade-offs

### Strengths

- Provable anonymity bounds against a global passive adversary, with explicit parameter dependencies.
- Reasonable latency (seconds, not hours).
- Bandwidth-efficient relative to predecessor designs.
- Modular: the topology, delay distribution, and cover-traffic rates are independent design parameters.
- Specified clearly enough to admit multiple production implementations.

### Limitations

- The Loopix system itself is a research artifact; production users go to Nym or Katzenpost.
- Anonymity depends on cover-traffic discipline (clients must send dummies). A client that fails to do so degrades not only its own anonymity but the network's.
- Provider nodes are trusted to deliver messages and store offline mail. Provider compromise is a meaningful attack surface.
- The Poisson-mixing parameter μ is a privacy/latency knob; tuning it for a deployed network is nontrivial and traffic-dependent.

## Comparison with other mix designs

| Property | Mixmaster | Mixminion | Loopix | Nym (production Loopix) |
|----------|-----------|-----------|--------|-------------------------|
| Latency | Minutes-hours | Minutes | Seconds | Seconds |
| Mixing | Batch (pool) | Batch | Continuous (Poisson) | Continuous (Poisson) |
| Cover traffic | Heavy dummies | Heavy dummies | Per-client + per-mix loops | Per-client + per-mix loops |
| GPA defense | Yes | Yes | Yes (with provable bound) | Yes (under assumptions) |
| Reply mechanism | Type-II reply blocks | SURBs | SURBs | SURBs |
| Status | Dead (~2015) | Dead | Research only | Production |

## Primary sources

- [MOCHA: ePrint 2025/861](https://eprint.iacr.org/2025/861)

- Piotrowska, A., Hayes, J., Elahi, T., Meiser, S., Danezis, G. *The Loopix Anonymity System*. USENIX Security 2017. [usenix.org/conference/usenixsecurity17/technical-sessions/presentation/piotrowska](https://www.usenix.org/conference/usenixsecurity17/technical-sessions/presentation/piotrowska)
- Danezis, G., Goldberg, I. *Sphinx: A Compact and Provably Secure Mix Format*. IEEE S&P 2009.
- Kesdogan, D., Egner, J., Büschkes, R. *Stop-and-Go MIXes: Providing Probabilistic Anonymity in an Open System*. Information Hiding 1998 (Poisson-mix precursor).
- Das, D., Meiser, S., Mohammadi, E., Kate, A. *Anonymity Trilemma: Strong Anonymity, Low Bandwidth Overhead, Low Latency — Choose Two*. IEEE S&P 2018.
- Shirazi, F., Simeonovski, M., Asghar, M.R., Backes, M., Diaz, C. *A Survey on Routing in Anonymous Communication Protocols*. ACM Computing Surveys, 2018.
- ePrint 2025/861, *MOCHA: Mixnet Optimization Considering Honest Client Anonymity*, IH&MMSEC 2025. [eprint.iacr.org/2025/861](https://eprint.iacr.org/2025/861)
