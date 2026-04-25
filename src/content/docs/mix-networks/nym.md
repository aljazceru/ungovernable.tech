---
title: "Nym"
tags:
  - "nym"
  - "mixnet"
  - "loopix"
  - "anonymity"
  - "mix-networks"
  - "sphinx"
  - "deep-dive"
---
*A production Loopix-based mixnet. The first system designed for the strongest threat model (a global passive adversary) actually deployed at scale, with economic incentives via the NYM token.*

---

## How Nym differs from Tor

Tor and I2P optimize for low-latency anonymity. Both fail against an adversary watching the global network. They leak via timing correlation between entry and exit. Nym takes the opposite design choice: add deliberate latency and cover traffic so that an observer can't link ingress to egress flows even with full visibility.

The base design is **Loopix** (Piotrowska et al., 2017). Loopix introduces:

- Continuous-time Poisson mixing. Each mix node delays each packet by a random exponential interval. The aggregate effect: packets arriving close together can leave widely separated.
- Cover traffic. Each user generates dummies; each mix generates loop traffic. The result: traffic patterns at every link have constant or near-constant entropy.
- Sphinx packet format. Fixed-size, layered-encrypted packets with no length leakage.

Nym productizes this with a stake-weighted node selection, anonymous credentials for service authorization (zk-nyms), and integrations for everything from VPN-replacement (NymVPN) to wallet RPC privacy.

---

## Sphinx packets

A Sphinx packet (Danezis & Goldberg, 2009) is a fixed-size mixnet payload with these properties at every hop:

- Bitwise indistinguishability of packets across the network. No traffic-analysis fingerprint from size.
- Replay protection via per-mix bloom filters.
- No revealable next-hop info to anyone but the current mix.
- Single-use reply blocks (SURBs). A sender can include encrypted return-path information so the recipient can reply without learning the sender's identity.

```
Sender ── Mix1 (decrypt outer layer, delay) ── Mix2 ── Mix3 ── Recipient
                ↑ each layer reveals only "next hop"
```

Layered encryption: each mix peels one layer; the inner ciphertext is opaque to it.

---

## Topology

Three layers of mixes, each containing many nodes. Packets traverse one mix per layer. Stake-weighted random selection keeps the topology balanced. Higher stake gives a node higher selection probability, within bounds that prevent centralization.

```
   Layer 1 mixes      Layer 2 mixes      Layer 3 mixes
   ┌──┐ ┌──┐ ┌──┐    ┌──┐ ┌──┐ ┌──┐    ┌──┐ ┌──┐ ┌──┐
   │M1│ │M2│ │M3│    │M4│ │M5│ │M6│    │M7│ │M8│ │M9│
   └──┘ └──┘ └──┘    └──┘ └──┘ └──┘    └──┘ └──┘ └──┘
        gateway nodes ↗                     ↘ exit / service
```

**Gateway nodes** at the edges accept packets from clients (via WebSocket or similar) and inject them into the mixnet. Gateways are also stake-weighted.

---

## Operating modes

Nym supports several deployment patterns layered on the same mixnet:

### Anonymous transport

A generic SOCKS-like proxy through the mixnet. Apps that speak SOCKS5 can route through Nym for the strongest anonymity guarantees deployed today, at the cost of seconds of latency per message.

### NymVPN

A consumer-facing VPN-style application built on the mixnet, with two modes:

- Mixnet mode. Full Loopix mixing, maximum anonymity, low throughput.
- Wireguard mode. Two-hop wireguard relay. Faster, weaker anonymity (similar threat model to Tor without traffic-analysis defense).

### Anonymous credentials

zk-nyms are Coconut-based blind signature credentials. They let a user prove "I paid for service" without revealing which payment maps to which user. Used internally for paid mixnet bandwidth and externally for zero-knowledge access tokens.

---

## Token economics

Nym uses the NYM token (Cosmos-based chain) for:

- Stake on mix nodes. Operators stake to participate; selection probability is proportional to stake (within bounds).
- Slashing for bad behavior (downtime, misbehavior provable from the mixnet's measurements).
- Bandwidth credentials paid via NYM, redeemed via zk-nym credentials so the spending is unlinkable to the user.

Tokenomics is a design choice, not a fundamental requirement of mixnets, but it is how Nym creates a permissionless market for mix capacity rather than relying on volunteers (Tor's model).

---

## What Nym doesn't solve

- End-to-end encryption. Use a real protocol (Signal, MLS, Marmot). Nym anonymizes transport.
- Real-time interactive protocols. The latency budget is too high for most VoIP/video.
- Endpoint compromise. Same as everywhere.
- Bandwidth-heavy workloads. Mix bandwidth is metered and substantially less than Tor's already-modest throughput.

For interactive use, layer Tor for low-latency anonymity and use Nym for high-stakes or async traffic where seconds-scale latency is acceptable.

---

## Threat model

| Adversary | Status |
|-----------|--------|
| Local observer | Defeated. The local link sees only constant-rate Sphinx packets |
| ISP / on-path observer | Defeated |
| Compromised gateway | Defeated for downstream. The gateway sees only encrypted Sphinx |
| Compromised mix node (subset) | Defeated by 3-layer plus cover traffic |
| Global passive observer | Defeated under Loopix assumptions. The headline property |
| Global active adversary modifying packets | Replay protection plus integrity bound; some research-stage attacks exist |
| Endpoint malware | Out of scope |

The "defeated under Loopix assumptions" is the central Nym claim. Validity rests on:

- Sufficient cover traffic.
- Sufficient honest-mix density (3-layer protection).
- Correct cipher implementation.
- No covert channels in the deployed software.

Empirical validation of those assumptions for a real network the size of Nym is an open research area.

---

## Trade-offs

### Strengths

- Strongest deployed anonymity. Loopix-based, production network operating since 2021.
- Defends against a global passive adversary, the canonical "uncatchable" threat for low-latency systems.
- zk-nym credentials decouple payment from access.
- Stake-weighted, decentralized topology. No directory authorities.
- Active development with academic involvement.

### Limitations

- High latency. Seconds per round trip baseline.
- Limited bandwidth. Every Sphinx hop is metered.
- Newer than Tor. Smaller anonymity set, less analyzed in deployment.
- Token model introduces speculative-economic attack surface.
- Fewer apps integrated than Tor; ecosystem is younger.

---

## Comparison

| Dimension | Tor | I2P | Nym | Katzenpost |
|-----------|-----|-----|-----|------------|
| Mixing | None (low-latency) | None (variable) | Continuous-time Poisson | Continuous-time Poisson |
| Cover traffic | Limited (padding) | Garlic-natural | Loops + dummies | Loops + dummies |
| GPA defense | No | No | **Yes** | **Yes** |
| Latency | seconds | seconds | seconds (with mixing) | seconds-tens |
| Hidden services | Yes | Yes | Service Providers | Service Providers |
| Decentralization | Authorities | NetDB | Stake-weighted | Operators |
| Post-quantum | Roadmap | Roadmap | Roadmap | Built-in |
| Maturity | High | Medium | Medium | Research-grade |

---

## Operational patterns

### Wallet RPC privacy

Nym's mixnet is a natural fit for blockchain RPC calls. Sending a transaction through Nym hides "wallet sends transaction at time T from IP X" from anyone observing the user's connection, a much weaker threat model than even Tor satisfies for RPC.

### NymVPN for general browsing

Use NymVPN's mixnet mode for high-stakes browsing, Wireguard mode for everyday VPN replacement.

### Service operators

Apps offer Nym-aware ingress. Examples deployed: monero-related services, blockchain RPC gateways, messaging gateways.

---

## Recent developments (2024-2026)

- NymVPN consumer launch with mixnet and wireguard modes.
- zk-nym credentials stabilized.
- Network growth. Hundreds of mix nodes, multiple gateways.
- Service Provider ecosystem maturing. Nym-aware service discovery.
- Performance work. Better cover-traffic optimization, latency reduction in low-load conditions.

---

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Mix-node Sybil | Stake-weighted selection bounds influence |
| Adversarial cover traffic | Per-user dummies plus per-mix loops |
| Replay | Sphinx replay tags plus bloom filters per mix |
| Long-term flow correlation | Loopix Poisson-mix breaks per-flow timing |
| Token-economic attacks | Slashing on misbehavior; stake bounds |
| Gateway compromise | Gateway sees only opaque Sphinx |
| Endpoint compromise | Out of scope |

---

## Related files

- [Overview - Mix Networks](/mix-networks)
- [Tor](/mix-networks/tor)
- [I2P](/mix-networks/i2p)
- [Katzenpost](/mix-networks/katzenpost)
- [MOC - Metadata Privacy](/meta/moc-metadata-privacy)
- [Glossary](/meta/glossary) — Loopix, Sphinx, SURB

---

## Primary sources

- Piotrowska et al., *The Loopix Anonymity System*, USENIX Security 2017. [usenix.org/conference/usenixsecurity17/technical-sessions/presentation/piotrowska](https://www.usenix.org/conference/usenixsecurity17/technical-sessions/presentation/piotrowska)
- Danezis & Goldberg, *Sphinx: A Compact and Provably Secure Mix Format*, IEEE S&P 2009.
- Nym Technologies — [nymtech.net](https://nymtech.net)
- Nym Whitepaper — [nymtech.net/nym-whitepaper.pdf](https://nymtech.net/nym-whitepaper.pdf)
- Sonnino et al., *Coconut: Threshold Issuance Selective Disclosure Credentials with Applications to Distributed Ledgers*, NDSS 2019 (zk-nym basis).

