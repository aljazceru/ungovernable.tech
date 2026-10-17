---
title: "Nym Mixnet"
slug: nym
type: deep-dive
pillars: ["anonymity"]
readiness: usable
description: "Nym, a deployed mixnet based on Loopix with cover traffic and incentivised nodes, designed to resist a global passive adversary. Design and status."
dek: "A production Loopix-based mixnet: the first system designed for the strongest threat model (a global passive adversary) actually deployed at scale, with economic incentives via the NYM token. This is this library's pillar reference — architecture, Nyx blockchain and the Directory Contract evolution, node economics and their documented weaknesses (including the January 2026 Cao & Green reputation-attack paper), the 2026 integration wave, and operational guidance."
updated: 2026-09-04
created: 2026-04-25
origin: vault
source: "08-Mix-Networks/Nym.md"
aliases: ["Nym Mixnet", "NYM", "NymVPN", "Noise Generating Mixnet"]
tags: ["nym", "mix-networks", "loopix", "sphinx", "anonymity", "nyx-blockchain", "mixnode-economics", "reputation", "censorship-resistance", "deep-dive"]
---

## Definitional

Nym is a decentralized anonymity network that combines:

1. A **packet mixnet** descended from [Loopix](/kb/loopix/) — stratified layers of mixnodes, Sphinx-format packets ([Sphinx Packet Format](/kb/sphinx-packet-format/)), Poisson delays, and continuous cover traffic ("noise") on every link;
2. A **layer-1 blockchain (Nyx)** providing node registration, staking, delegation, and mixmining rewards, with CosmWasm smart contracts;
3. A **credential system** (coconut-style zk-credentials, "zk-nyms") for anonymous access without identity linkage;
4. A consumer product (**NymVPN**) exposing the network as both a WireGuard-style fast VPN and the full five-hop mixnet.

Primary references:

- Piotrowska, A., Hayes, J., Elahi, T., Meiser, S., Danezis, G. *The Loopix Anonymity System*. USENIX Security 2017. https://www.usenix.org/conference/usenixsecurity17/technical-sessions/presentation/piotrowska
- Danezis, G., Hapgood, H., Isaakidis, M., et al. *Nym: Next-Generation Digital Infrastructure for Privacy* (whitepaper, rev. 2021). https://nymtech.net/whitepapers/
- Sonnino, A., Al-Bassam, M., Bano, S., Meiklejohn, S., Danezis, G. *Coconut: Threshold Issuance Selective Disclosure Credentials with Applications to Distributed Ledgers*. NDSS 2019 (zk-nym basis).
- Rial, Piotrowska, Halpin. *Outfox* (PQ packet format). ACM 2025.
- Cao, X.A., Green, M. *Analysis and Attacks on the Reputation System of Nym*. IACR ePrint 2026/101.
- Nym documentation: https://nymtech.net/docs/ · Blog: https://nym.com/blog

Project status (Aug 2026): production network + consumer VPN; core repo `nymtech/nym` (~1.9k stars, Rust, actively pushed); binaries **v2026.16-como** (Aug 19, 2026); NymVPN client v2026.12.1-beta (Aug 20).

## Architecture

### The mixnet (Anonymous mode)

```
 Client ──▶ Gateway ──▶ [ Mix Layer 1 ] ──▶ [ Mix Layer 2 ] ──▶ [ Mix Layer 3 ] ──▶ Exit Gateway ──▶ Internet
            (entry)        Poisson delay       Poisson delay       Poisson delay      (exit,
            auth           + cover noise        + cover noise        + cover noise       geo-selectable)
```

The base design is **Loopix**:

- **Continuous-time Poisson mixing.** Each mixnode independently samples an exponential delay per packet; packets arriving close together leave widely separated. Aggregate effect: input/output ordering is statistically decoupled.
- **Cover traffic.** Each user generates loop/dummy traffic; each mix generates loop traffic. Every link carries real+dummy flows at near-constant rate, so silence never distinguishes activity.
- **Sphinx packet format.** Fixed-size, layered-encrypted packets with no length leakage; SURBs provide anonymous replies.
- **Stratified topology.** Three mix layers; every packet traverses one node per layer; the **active set** (nodes carrying traffic) is selected from registered mixnodes by stake and performance score.

**Anonymous vs Fast mode** — the distinction that matters analytically (do not conflate them when evaluating NymVPN claims):

| Property | Anonymous mode | Fast mode |
|----------|---------------|-----------|
| Mixnet | Yes (Loopix-style, 5-hop) | No (2-hop WireGuard-like) |
| Cover traffic | Yes | No |
| Latency | Seconds (Poisson mixing) | ~100 ms |
| PQ key exchange | Not yet (roadmap; directionally Outfox) | Yes — Lewes Protocol (ML-KEM-based) |
| Threat model | Global passive adversary | Decentralized VPN |

### The Nyx blockchain and directory

- Nodes self-register on **Nyx** (Cosmos SDK chain) bonding NYM tokens; delegators stake behind nodes; a mixing reward pool ("mixmining") distributes NYM to the active set by performance.
- **Directory Contract (merged Aug 21, 2026)**: node-info distribution moves from per-node HTTP pulls to an **on-chain push model** — each nym-node pushes ed25519-signed configuration (keyed by `(node_id, label)`) to a CosmWasm contract, with an **incremental on-chain LtHash digest** over all entries making whole-directory retrieval verifiable. The `nym-lthash` crate (LtHash16, 2 KB BLAKE3-XOF accumulator) shipped in v2026.16-como. The full 8-PR stack merged 2026-08-21: #6933 (contract), #6936 (verifiable retrieval), #6941 (TM Light Client anchor), #6948 (attested anchor), #6949 (nym-api keys + proof-of-possession), #6954 (attestation provider), #7004 (checkpoint bootstrapping), #7013 (node publishing). This is the architectural response to the corporate-gating critique (below) — now shipped, not proposed.
- **Credential issuance** (coconut zk-credentials) remains company-operated as of 2026 — the residual centralization point.

### Token economics

The NYM token (Nyx/Cosmos-based) is used for:

- **Stake on mixnodes.** Operators stake to participate; selection probability is proportional to stake (within bounds).
- **Slashing** for provable misbehavior (downtime, misconduct detectable from network measurements).
- **Bandwidth credentials** paid via NYM, redeemed via zk-nym credentials so spending is unlinkable to the user.

Tokenomics is a design choice, not a requirement of mixnets — it is how Nym creates a permissionless market for mix capacity rather than relying on volunteers (Tor's altruism model, per Dingledine's DEF CON 34 briefing). The cost: economic gravity concentrates infrastructure and the measurement mechanism becomes an attack target (below).

### Censorship resistance stack

Per the 2026 censorship-resistance roadmap (and shipped items): AmneziaWG obfuscation for Fast mode, QUIC pluggable transport, Stealth API hardening, Outfox PQ packet-format design; 2026 targets add resilient bootstrapping, context-aware config delivery, and countermeasures against AI-adaptive censorship (the roadmap explicitly acknowledges static defenses are now attacked with near-real-time adaptive blocking).

## Node economics — and the documented attack surface

Nym's differentiator versus Tor is **paid infrastructure**: mixnodes stake, get measured, and earn. This buys uptime and capacity but creates a new class of attack: **the measurement and selection mechanism itself becomes the target.**

### The Cao & Green reputation analysis (ePrint 2026/101, Jan 2026)

Xinmu Alexis Cao and Matthew Green (Johns Hopkins) analyzed Nym's reputation mechanism using source-code analysis, mainnet data collection, and a custom simulator:

- **Framing attack**: node-performance measurement is manipulable — a small number of **low-stake nodes can damage the score of high-reputation active-set nodes**, because measurement trusts interactions with cheap-to-enter nodes.
- **Active-set capture**: a moderately resourced adversary (explicitly not nation-state budget) can thereby capture a **fraction of the active set**, a condition enabling **connection de-anonymization** — defeating the network's core purpose.
- **The survivability dilemma**: open entry is required (new operators must join for network survivability) but grants attackers a platform to attack the scoring system itself. Mitigations discussed; the tension is structural.

Nym continues to modify the scoring subsystem (PR #7073, Aug 2026 — config-score penalty for nodes incapable of sending Nyx transactions), so the measurement layer is under active development *and* documented active-attack pressure.

### Stark Industries incident (2026)

The **Stark Industries** case (see [Mix Networks Friday — August 07 2026 Weekly Update](/briefings/mix-networks/2026-08-07/)) documented bulk-hosting concentration: large volumes of mixnode capacity on one commercial host, mirroring Tor's Hetzner problem — economic gravity concentrates infrastructure, eroding jurisdictional diversity.

### Privacy Guides "privacy theater" thread (ongoing through Aug 2026)

Community critique: a single corporation (Nym Technologies SA) can gate the entire network via credential issuance; "684+ community-run nodes become useless overnight" if the company is compelled. The Directory Contract is the architectural counter; credential decentralization remains open.

### Synthesis: three failure modes, three different layers

| Failure mode | Layer | Status (Aug 2026) |
|---|---|---|
| Corporate gating (directory/credentials) | Governance/directory | Being addressed — Directory Contract + LtHash (on-chain, verifiable); credential issuance still company-operated |
| Infrastructure concentration (Stark, Hetzner-analog) | Economics/hosting | Unresolved — economic gravity; no provider-diversity incentives |
| Reputation manipulation (framing attacks) | Measurement/selection | **Unresolved** — Cao & Green paper; scoring under active modification |

## Threat model

| Adversary | Status |
|-----------|--------|
| Local observer | Defeated. The local link sees only constant-rate Sphinx packets |
| ISP / on-path observer | Defeated |
| Compromised gateway | Defeated for downstream. The gateway sees only encrypted Sphinx |
| Compromised mix node (subset) | Defeated by 3-layer plus cover traffic |
| Global passive observer | Defeated **under Loopix assumptions**. The headline property |
| Global active adversary modifying packets | Replay protection plus integrity bound; some research-stage attacks exist |
| Adversary capturing the active set via reputation manipulation | **Weak point** — Cao & Green framing attacks |
| Endpoint malware | Out of scope |

The "defeated under Loopix assumptions" claim rests on: sufficient cover traffic, sufficient honest-mix density, correct implementations, and no covert channels in deployed software. Empirical validation at Nym's real scale is an open research area — and the Cao & Green result shows the *incentive layer* can undermine the *cryptographic layer* from below.

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Mix-node Sybil | Stake-weighted selection bounds influence — but see framing attacks |
| Reputation framing (low-stake nodes defaming honest nodes) | **Open problem** (ePrint 2026/101) |
| Adversarial cover traffic | Per-user dummies plus per-mix loops |
| Replay | Sphinx replay tags plus bloom filters per mix |
| Long-term flow correlation | Loopix Poisson-mix breaks per-flow timing |
| Token-economic attacks | Slashing on misbehavior; stake bounds; concentration unmitigated |
| Gateway compromise | Gateway sees only opaque Sphinx |
| Endpoint compromise | Out of scope |

## What Nym doesn't solve

- **End-to-end encryption.** Use a real protocol (Signal, MLS). Nym anonymizes transport.
- **Real-time interactive protocols.** The Anonymous-mode latency budget is too high for most VoIP/video.
- **Endpoint compromise.** Same as everywhere.
- **Bandwidth-heavy workloads.** Mix bandwidth is metered and substantially less than Tor's already-modest throughput.
- **Hidden services.** Unlike Tor (.onion) and I2P (eepsites), Nym has no addressable internal services (Service Providers provide ingress/egress, not an overlay web). Nym is a transit network.

For interactive use, layer Tor for low-latency anonymity and use Nym for high-stakes or async traffic where seconds-scale latency is acceptable.

## Use cases and operational patterns

| Use case | Fit | Notes |
|---|---|---|
| Wallet/marketplace metadata privacy | **Strong fit — production** | Edge Wallet (Jul 2026), **Peach Bitcoin (Aug 17, 2026 — first P2P BTC marketplace with native mixnet)**, Zcash Ironwood free tier; async traffic is the mixnet's sweet spot |
| Async messaging / dead drops | Strong fit | Loop cover traffic + SURB replies match store-and-forward |
| Wallet RPC privacy | Strong fit | Hides "wallet sends transaction at time T from IP X" from network observers |
| Interactive browsing | Partial | Anonymous mode adds seconds of latency; Fast mode is a VPN, not a mixnet — do not conflate |
| Censorship circumvention (censored markets) | Growing | AmneziaWG + QUIC transports; Geo Exclusion (Aug 2026) solves local-app breakage via an external SOCKS5 proxy for excluded regions (China first) |
| VoIP / video | Not viable | Latency |
| Hidden services / internal overlay | Not supported | Use Tor or I2P |

Operational patterns: apps offer Nym-aware ingress via the Service Provider framework (deployed examples include blockchain RPC gateways and messaging gateways); NymVPN Fast mode serves as an everyday WireGuard replacement with PQ handshakes while Anonymous mode is reserved for metadata-critical sessions.

## Comparison

| Dimension | Tor | I2P | Nym | Katzenpost |
|-----------|-----|-----|-----|------------|
| Mixing | None (low-latency) | None (variable) | Continuous-time Poisson | Continuous-time Poisson |
| Cover traffic | Limited (padding) | Garlic-natural | Loops + dummies | Loops + dummies |
| GPA defense | No | No | **Yes** (under assumptions) | **Yes** (under assumptions) |
| Latency | seconds | seconds | seconds (with mixing) | seconds-tens |
| Internal services | Yes (.onion) | Yes (eepsites) | Service Providers (ingress) | Service Providers |
| Decentralization | 9 dirauths | NetDB (P2P) | Stake-weighted + on-chain directory | Federated authorities |
| Post-quantum | Roadmap (CGO era) | Ratchet-layer PQ default | Fast-mode PQ shipped; mixnet PQ roadmap | Built-in (hybrid) |
| Incentives | Altruism | None (peers) | Token staking + mixmining | None (federated) |
| Maturity | High | Medium | Medium (production + consumer) | Research-grade |

## 2026 roadmap and integration wave

Nym's 2026 roadmap frames the year as a shift from technically functional mixnet to consumer-scale privacy product: faster Anonymous mode without dropping the Loopix threat model; NymVPN adoption; **browser and wallet integrations** (the two places metadata privacy produces immediate user value); merged payment flows with zk-credentials; token utility tied to actual usage; decentralization of remaining centralized services.

The integration wave, in order:

1. **Edge Wallet** (mid-July 2026) — first major multi-asset wallet with native mixnet routing.
2. **Zcash** — Ironwood free tier for NymVPN (Jul 27), long-running ecosystem engagement.
3. **Peach Bitcoin** (Aug 17, 2026) — first P2P Bitcoin marketplace with native mixnet integration; free for all users; verifiable exit country ("Test current country"); user-selectable exit jurisdictions.

Nym's framing — "plug-and-play Layer 0 anonymity network" — is becoming testable: each integration grows the anonymity set with the integrator's user base, the only sustainable path for cover-traffic economics. The counterweight is the reputation-attack surface: each integration concentrates de-anonymization value in the active set, making node-selection integrity proportionally more critical.

Recent product signals: NymVPN v2026.11 Mixnet Tuning (user-controlled cover traffic 0.7–2 Mbps, delay 0–200 ms), Server Families, Geo-exclusion beta; v2026.12.1-beta clients (Aug 19–20); core v2026.16-como with Directory Contract components (Aug 18–19).

## Evidence at a glance

| Dimension | Evidence | Date | Source |
|---|---|---|---|
| Core release | v2026.16-como (nym-lthash, Como v2 endpoints) | Aug 18–19, 2026 | github.com/nymtech/nym/releases |
| Flagship integration | Peach Bitcoin — first P2P BTC marketplace with native mixnet | Aug 17, 2026 | nym.com/blog/peach-bitcoin-mixnet-integration |
| Directory decentralization | Directory Contract (LtHash digest, on-chain push) | Aug 2026 (**merged 08-21**) | github.com/nymtech/nym/pull/6933 |
| Reputation attackability | Cao & Green framing attacks; active-set capture | Jan 21, 2026 | eprint.iacr.org/2026/101 |
| Fast-mode PQ shipped | Lewes Protocol (ML-KEM) in NymVPN Fast mode | 2026 | nym.com/blog/lewes-protocol-post-quantum |
| Mixnet tuning | v2026.11: cover-traffic 0.7–2 Mbps and 0–200 ms delay sliders | Jul 14, 2026 | nym.com/blog/mixnet-tuning |
| Geo Exclusion beta | External SOCKS5 proxy for excluded regions (China first) | Aug 19, 2026 | nym.com/blog/geo-exclusion-split-tunneling |
| Censorship roadmap | AmneziaWG, QUIC, Outfox; AI-adaptive adversary acknowledgment | 2026 | nym.com/blog/nym-censorship-resistance-2026 |
| Community critique | "privacy theater" thread — corporate gating critique | ongoing (Aug 8, 2026 update) | discuss.privacyguides.net/t/38335 |
| Infrastructure concentration | Stark Industries bulk-hosting case | Aug 2026 | Aug 7 weekly update |

## Open questions

1. **Can performance measurement be made Sybil-resistant?** The framing attack exploits cheap entry into the measurement protocol; mitigations (stake-weighted measurement, committees, TEE-attested monitors) are open design problems the Cao & Green paper frames but does not close.
2. **Does on-chain directory + decentralized credentials fully remove corporate gating?** Directory Contract addresses storage/verification; coconut credential issuance remains company-operated.
3. **Do integrations compound anonymity?** Only if traffic shapes across integrations are similar enough to mix; cross-application mixing effectiveness is publicly unmeasured.
4. **Can token incentives buy honest mixing without stake concentration?** Long-running tracker question; Stark Industries and delegation concentration are live counterexamples.
5. **When does Anonymous mode get PQ?** Outfox gives the architectural path; Sphinx geometry changes (PQ KEM ciphertext sizes) risk packet-class distinguishability until fully deployed.

## September 04, 2026 Update — Djibouti Release; Outfox Removed; LP-Data Split

Three concrete shifts this week, all in the same release: **Nym Binaries v2026.17-djibouti (Sep 2)** is the first tagged release to ship the full Directory Contract stack that was merged Aug 21 — eight PRs now reach operators as one numbered update. With it comes:

- **Outfox packet removal (#7048)** — *breaking change*. SOCKS5 and WASM clients are now Mix-packet only; Outfox creation/decoding/routing/ACKs return explicit "not supported" errors. Outfox options and public exports removed or deprecated. This is the second PQ-packet-format retirement in the mixnet ecosystem in 2026 (after [Katzenpost](/kb/katzenpost/)'s non-PQ Sphinx retirement) and runs without user pushback because Mix packets have been the default for ≥12 months.
- **Geolocator service + CosmWasm contract (#7055)** — on-chain attested digests replace the cached `geoip` JSONB that previously caused "empty country code silently drops a gateway from the dVPN directory." Now any consumer can verify a node's reported geolocation by recomputing the digest against the on-chain state, rather than trusting whoever served the cached value.
- **Network Details v2 endpoint type fix (#7051)** — the v2 endpoint was actually serving the v1 struct (since #6901); corrected + minimal validator-client function added.
- **Config-score penalty for nodes incapable of sending nyx transactions (#7073)** — operational lever: nodes that can't pay the on-chain tx fee get a downward score adjustment, making the active-set selection more honest about node capability.
- **WireGuard startup robustness (#7065)** — don't crash node startup over one corrupted peer record.
- **Reject packets to unknown clients (#7061)** — gateway-probe hardening.

Three post-release follow-ups the same week:

- **#7117 (Sep 1)** — *directory submission default-on*. The operational complement to the Directory Contract: nodes that can submit to the on-chain directory *do so by default* going forward, accelerating network participation.
- **#7112 (Sep 2)** — **LP-Data separation**. Refactor that extracts the LP (Lounge Pass) gateway channel into a new crate `nym-lp-gateway-client`, leaving only dVPN registration in `nym-registration-client`. The LP-side dependency list drops to `bincode, bytes, rand, thiserror, tokio, tracing, nym-lp, nym-lp-data` — verified via `cargo tree -p nym-lp-gateway-client --depth 1 -e normal`. **Lounge Pass / LP is becoming a real product surface**, not just a marketing label — the new crate exists so third-party clients can take the LP data channel without dragging in Nym's registration machinery.
- **re-DKG robustness vols 2–5 (#7082/#7088/#7096/#7107)** — four batches of "make future re-DKG smoother" bugfixes, all merged Sep 3. After four months of incremental work, the re-DKG ceremony is no longer a fragile operation.

**NymVPN v2026.12.4-beta.1 (Sep 3)** — PR **#6272** *"Make pinned gateways respect the blacklist"* fixes a **pinned-gateway bypass-of-blacklist**: a pinned entry/exit gateway identity was using an unfiltered lookup that skipped `NotBlacklisted`/`MinScore`/`Residential` checks, so a user who pinned a gateway the GFW was actively blackholing retried the same doomed gateway on every connection attempt forever, with no cooldown and no useful error. The fix routes pinned-gateway lookups through the same filter pipeline as random selection. This is the textbook failure mode of user-trust features silently defeating adversary-defence features.

**Evidence at a Glance (Sep 4 update)**:

| Item | PR / source | Date |
|---|---|---|
| v2026.17-djibouti release | `nym-binaries-v2026.17-djibouti` tag | 2026-09-02 |
| Outfox packet removal | #7048 | merged 2026-08-11, ships in djibouti |
| Geolocator service + contract | #7055 | merged 2026-08-18 |
| Network Details v2 endpoint fix | #7051 | merged 2026-08-12 |
| Directory submission default-on | #7117 | merged 2026-09-01 |
| LP-Data separation | #7112 | merged 2026-09-02 |
| re-DKG robustness vol2–5 | #7082/#7088/#7096/#7107 | all merged 2026-09-03 |
| NymVPN pinned-gateway blacklist fix | #6272 | merged 2026-09-03 |
| NymVPN v2026.12.4-beta.1 release | `nym-vpn-v2026.12.4-beta.1` tag | 2026-09-03 |

See [Mix Networks Friday — September 04 2026 Weekly Update](/briefings/mix-networks/2026-09-04/) for the full weekly delta.
