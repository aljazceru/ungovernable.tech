---
title: "HOPR"
slug: hopr
type: deep-dive
pillars: ["anonymity"]
readiness: experimental
description: "HOPR, an incentivised mix network that pays relays per packet: Sphinx onion routing, proof of relay, cover traffic and its deployment status."
dek: "An incentivized mix network for Web3 traffic — Sphinx-packet onion routing with per-hop probabilistic micropayments. Pitched as the privacy layer for RPC calls and dApp queries, built by the HOPR Association in Switzerland since 2020."
updated: 2026-09-04
created: 2026-04-26
origin: vault
source: "08-Mix-Networks/HOPR.md"
aliases: ["HOPR Network", "HOPR Protocol"]
tags: ["hopr", "mixnet", "sphinx", "web3", "payment-channels", "anonymity", "deep-dive"]
---

## Position in the mixnet landscape

HOPR sits between [Tor](/kb/tor/)'s volunteer model and [Nym](/kb/nym/)'s stake-weighted economy. Both Nym and HOPR pay node operators, but the payment models differ:

- **Nym**: stake-weighted selection, NYM token, bandwidth credentials redeemed via zk-nym blind signatures.
- **HOPR**: per-packet probabilistic payments via the HOPR token, settled through off-chain payment channels on Gnosis Chain.

The HOPR thesis is that *every relayed packet carries its own payment proof*, so node operators are compensated for actual work rather than for stake-weighted selection. The trade-off is heavier on-chain machinery (payment channels, ticket verification) and a smaller network than either Tor or Nym.

## Architecture

The HOPR data path is Sphinx-format onion routing over libp2p, with a payment channel layer in parallel.

```
Client → Hop 1 → Hop 2 → Hop 3 → Hop 4 → Recipient
         ↓       ↓       ↓       ↓
         v       v       v       v
        ticket  ticket  ticket  ticket
        (probabilistic micropayment per packet)
```

### Mix layer

- Sphinx packets (see [Sphinx Packet Format](/kb/sphinx-packet-format/)). Fixed-size, layered ECDH + symmetric encryption, replay-protected via per-hop tags.
- Multi-hop routing, default 3 forward hops plus 1 return hop for SURBs (single-use reply blocks).
- Cover traffic. Each node generates dummy packets to maintain link-level entropy.
- libp2p transport. Nodes discover each other via Kademlia DHT and gossipsub.

### Payment layer

Each hop produces a *ticket* — a probabilistic payment commitment. A ticket pays out only with probability `p` (typically `p = 1`, but the design supports lower win-rate tickets for amortized settlement). Tickets are aggregated and redeemed against a payment channel on Gnosis Chain (formerly xDai).

`HoprChannels` is the Solidity contract that manages bilateral payment channels between nodes. Settlement is off-chain except for channel open, channel close, and ticket aggregation events. The economic model resembles a Lightning-style channel network restricted to mixnet payments.

The probabilistic-payment scheme draws on Rivest's "PayWord and MicroMint" lineage and on more recent work on probabilistic channels in [Lightning Network Deep Dive](/kb/lightning-network/).

## HOPR token economics

The HOPR token (ERC-20 on Gnosis Chain, bridged to Ethereum) is used for:

- Funding payment channels between nodes.
- Paying senders for relay capacity.
- Staking by node operators (the "Cover Traffic" program rewards stake committed to running nodes that generate cover traffic).

The token went live in 2020 via a Genesis DAO sale; the HOPR Association is the Swiss non-profit steward. Total supply roughly 1 billion tokens, with treasury allocations for development, ecosystem grants, and node-operator incentives.

The honest critique: a substantial portion of node-operator revenue has come from token issuance ("Cover Traffic" rewards) rather than from end-user demand for the privacy product. This is structurally similar to many Web3-incentivized infrastructure projects and remains the central sustainability question.

## RPC privacy use case

The flagship application is RPC privacy. When a wallet queries an Ethereum node, the RPC provider (Infura, Alchemy, public node) sees:

- The querying IP.
- The request pattern (which addresses, contracts, balances).
- Timing of transaction broadcasts.

This metadata trivially links wallet activity to network identity and is widely held by a small handful of RPC operators. HOPR routes RPC calls through its mixnet so the provider sees only an exit-node IP and the user sees no degradation other than added latency.

This is exactly the niche Nym targets too. The differentiator HOPR claims: per-packet payment, so users pay for what they use rather than committing stake.

## Threat model

| Adversary | Status |
|-----------|--------|
| Local / ISP observer | Defeated. Sees only encrypted Sphinx packets to the entry hop |
| Compromised hop | Defeated. Sphinx layered encryption hides the path beyond the immediate next hop |
| Compromised RPC endpoint | Sees aggregated mixnet egress, not user IP |
| Sybil attack on the mixnet | Partially mitigated by stake requirements; smaller network is more vulnerable than Tor |
| Global passive adversary | Limited defense. HOPR has cover traffic but the small network size makes empirical anonymity sets thin |
| Endpoint compromise | Out of scope |

The "global passive adversary" line is the honest weak point. HOPR's design includes Loopix-inspired cover traffic, but the deployed network has historically operated at a few hundred nodes — far below the anonymity-set scale of Tor (~7,000 relays) or even Nym's mainnet. A global observer with knowledge of the full node set would have a much narrower correlation problem on HOPR than on Tor.

## Trade-offs

### Strengths

- Per-packet incentive aligns payment with work performed.
- Sphinx-format onion routing inherits well-studied anonymity properties.
- Gnosis Chain settlement is cheap, making micropayment economics viable.
- Open source, Rust implementation, Swiss non-profit governance.
- Targets a real underserved niche (Web3 RPC privacy).

### Limitations

- Small node count. Adoption has stalled compared to Tor and Nym.
- Token-funded sustainability. Cover-traffic rewards have been a major revenue source for operators, raising questions about long-term equilibrium when issuance ends.
- Documentation and tooling are less polished than Tor; client SDKs (RPCh) target a narrow developer audience.
- Marketing-heavy positioning at times outpaced deployment realities.
- Overlap with Nym for the wallet-RPC use case, with Nym having more momentum in 2024-2026.

## Deployment status (2024-2026)

- **RPCh** (RPC over HOPR) is the consumer-facing product, packaged as a client SDK and a public RPC endpoint provider.
- Node count has fluctuated in the low hundreds to low thousands depending on incentive cycles.
- Integrations with Web3 wallets and dApps remain limited; most users connect via the RPCh proxy rather than running native HOPR clients.
- The 2025-2026 roadmap emphasizes performance optimization and cover-traffic efficiency over network expansion.

## Comparison vs Nym

| Aspect | HOPR | Nym |
|--------|------|-----|
| Mixing | Sphinx onion routing, cover traffic | Loopix Poisson mixing, cover traffic |
| Incentive model | Per-packet probabilistic payment | Stake-weighted selection plus zk-nym credentials |
| Settlement | Payment channels on Gnosis Chain | NYM token on Cosmos chain |
| Node count | Hundreds | Hundreds to low thousands |
| Flagship app | RPCh (Web3 RPC) | NymVPN (consumer VPN) |
| GPA defense claim | Partial (small network limits anonymity set) | Loopix-grade under stated assumptions |
| Maturity | Production but small | Production with growing ecosystem |

The two projects have largely converged on the wallet-RPC use case from different starting points. The market has not obviously chosen between them; each has a small but committed user base.

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Sphinx replay | Per-mix bloom filters and replay tags |
| Sybil hop selection | Stake bonding for node registration |
| Payment-channel griefing | On-chain dispute resolution; channel-close timeouts |
| Ticket forgery | Cryptographic commitments verified before settlement |
| Adversarial flow correlation | Cover traffic; weak relative to Loopix bounds at deployed scale |
| Token-economic attacks | Treasury and slashing mechanisms |
| Endpoint compromise | Out of scope |

## September 04, 2026 Update — PIX Supervision Track Surfaces

HOPR's PIX (Payment-In-channel eXchange) protocol is the payment channel that makes the hop-by-hop mixnet economically viable. The week's commits show PIX supervision graduating from deposit plumbing to admission policy:

- **#8362 (Aug 27, merged)** — `feat(pix): per-SSA deposit data in SsaRequest, sourced from the deposit pool`. The per-Session-Source-Account deposit lookup, prerequisite for parameterized admission decisions.
- **#8355 (Aug 22, merged)** — `fix(session): stop ERROR-spam on inbound packets to torn-down sessions`. Operator log hygiene.
- **#8364 (Aug 28, merged)** — `chore: bump hopr-types to v4.0.0`. Major version bump; signals API surface changes.
- **#8373 (Sep 1, merged)** — `chore(deps): unify on hopr-chain-connector 0.26.0`. Single-version policy across the workspace.
- **#8237 (Sep 2, merged)** — **`feat: add session PIX supervisor`**. The supervisor that tracks PIX state per session and decides whether to admit new packets.
- **#8336 (Sep 3, merged)** — `fix(tests): scale cluster convergence waits with the test timeout`. CI reliability on long-running integration tests.
- **#8377 (Sep 3, merged)** — **`feat(session): parameterize PIX admission by Session target`**. The admission policy is now keyed by *which session* the packet is for, not just by deposit balance. Meaningful step toward "PIX per application / per use-case" pricing.

The PIX supervision track is now visible in the public commit stream as a coordinated effort: deposit plumbing (#8362) → test reliability (#8336) → supervisor (#8237) → parameterized admission (#8377). Expect a HOPR blog post or release-notes announcement when the supervisor lands in a numbered release.

See [Mix Networks Friday — September 04 2026 Weekly Update](/briefings/mix-networks/2026-09-04/) for the full weekly delta.

## Primary sources

- HOPR Association — [hoprnet.org](https://hoprnet.org)
- HOPR protocol specification — [github.com/hoprnet/hoprnet](https://github.com/hoprnet/hoprnet)
- HOPR yellowpaper — [hoprnet.org/papers](https://hoprnet.org/papers)
- Danezis & Goldberg, *Sphinx: A Compact and Provably Secure Mix Format*, IEEE S&P 2009.
- Piotrowska et al., *The Loopix Anonymity System*, USENIX Security 2017 (Sphinx + cover-traffic foundations).
- HoprChannels Solidity contracts — [github.com/hoprnet/hoprnet/tree/master/packages/ethereum](https://github.com/hoprnet/hoprnet/tree/master/packages/ethereum).
- RPCh — [rpch.net](https://rpch.net).
