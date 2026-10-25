---
title: "Lightning Network"
slug: lightning-network
type: deep-dive
pillars: ["money"]
readiness: battle-tested
description: "The Lightning Network makes Bitcoin payments instant and cheap through payment channels and onion-routed HTLCs: how it works and what it reveals."
dek: "Bitcoin's instant, low-fee, censorship-resistant payment layer. Built from bidirectional payment channels, HTLCs, and onion routing."
updated: 2026-10-25
created: 2026-04-25
origin: vault
source: "06-Financial-Sovereignty/Lightning Network Deep Dive.md"
aliases: ["Lightning", "LN", "BOLT"]
tags: ["lightning", "bitcoin", "layer-2", "payment-channels", "htlc", "financial", "deep-dive"]
related: ["fedimint", "robosats", "btcpay-server", "cashu-ecash"]
---

## Why Lightning matters

Bitcoin base-layer transactions are *settlement*, not *payments*. Block intervals (~10 min) and per-byte fees price out micropayments and high-frequency commerce. Lightning solves this without a custodian or a separate token: peers open a 2-of-2 multisig channel, exchange off-chain state updates, and settle on-chain only when they close. While the channel is open, payments are atomic, route through a network of intermediaries, and clear in seconds for sub-cent fees.

The censorship-resistance story compounds. Payments are onion-routed (Sphinx), so intermediaries see their incoming peer and outgoing hop, and modern features (route blinding, BOLT12 offers, async payments) progressively close the metadata gaps that early Lightning still leaked.

## Core mechanics

### Payment channels

A channel is a 2-of-2 multisig UTXO with an off-chain ledger maintained by both parties via signed *commitment transactions*. Each new payment produces a new commitment that supersedes the prior one. If either party broadcasts an old commitment, the counterparty can use a *justice transaction* to claim the entire channel balance during a dispute window.

```
Funding tx (on-chain) → 2-of-2 multisig output
   │
   ├── Commitment tx N (off-chain, ratcheted)
   │      ├── Output: Alice balance
   │      └── Output: Bob balance + revocation key
   │
   └── On close: cooperative or unilateral
```

### HTLCs (Hash-Time-Locked Contracts)

A multi-hop payment is a chain of *HTLCs*. Each hop locks funds against a hash preimage `R` and a timeout. The receiver knows the preimage `R`; the payment hash is `SHA256(R)`; revealing `R` upstream collects the payment. If `R` isn't revealed before the timeout, funds return.

This makes routed payments atomic: either the whole route settles or none of it does.

```
A → B → C → D    (each hop holds an HTLC)
              ↓
              D releases R to claim from C
              ↓
A ← B ← C ← D    (preimage propagates back, settling each HTLC)
```

### Onion routing (Sphinx)

Each payment carries a Sphinx packet: layered encryption such that each hop sees only the previous and next hops, the payment amount at this hop, and the timeout. Constant size at every hop, so no information leaks from packet length.

## BOLT specifications

The protocol is defined by the BOLT (Basis of Lightning Technology) specs:

| BOLT | Topic |
|------|-------|
| BOLT 1 | Base protocol, message framing |
| BOLT 2 | Channel state machine |
| BOLT 3 | Transaction format |
| BOLT 4 | Onion routing protocol |
| BOLT 5 | On-chain transactions |
| BOLT 7 | Gossip and channel discovery |
| BOLT 11 | Payment requests (legacy invoices) |
| BOLT 12 | Offers: reusable payment requests specified in the canonical BOLT 12 document |

Onion messages were folded into the existing BOLT 4/7 surface (feature bits 38/39, message type 513) rather than getting a separate BOLT.

[github.com/lightning/bolts](https://github.com/lightning/bolts)

## Implementations

| Implementation | Language | Notes |
|----------------|----------|-------|
| LND (Lightning Labs) | Go | Most-deployed; integrates with Loop, Pool |
| Core Lightning (CLN) | C | Modular plugin architecture; spec-implementing reference |
| Eclair (ACINQ) | Scala | Powers Phoenix mobile wallet |
| LDK (Lightning Dev Kit) | Rust | Library for embedding LN in custom apps |
| Sensei, Electrum LN | Various | Niche / desktop |

## Privacy properties

| Property | Status (early 2026) |
|----------|---------------------|
| Sender privacy | Reasonable. Onion routing, but timing analysis is still possible at the destination |
| Receiver privacy | Improving. Route blinding (BOLT12), blinded paths, async payments |
| Amount privacy | Visible to each hop; trampoline mitigates partially |
| Channel topology | Public. The gossip layer leaks channel sizes (mitigated by private channels) |

Practical patterns:

- Private channels: don't gossip; receiver embeds routing hints in invoices.
- Hold invoices: for refundable or streaming payments without revealing intent up front.
- Trampoline routing: outsource pathfinding to a trusted-but-blind node, hides destination from earlier hops.
- PTLCs (Point-Time-Locked Contracts): Schnorr/Taproot-based replacement for HTLCs that breaks payment correlation across hops. Spec stabilizing.

## Liquidity markets

Channels need balance on the right side to forward and receive. The 2024-2026 market matured around:

- Lightning Pool (Lightning Labs): non-custodial market for channel leases.
- Magma (Amboss): open marketplace for channel leases and liquidity.
- Liquidity Ads (BOLT12-adjacent): protocol-native channel ads.
- Splicing: re-balance or resize channels on-chain without closing them. Activated mid-2024 across CLN/Eclair, LND landing.

## Trade-offs

### Strengths

- No custodian. Keys remain with you; channel state is enforceable on-chain.
- Sub-second settlement, and routing failures fail open by returning funds.
- Onion routing built in. Sender privacy by default.
- Bitcoin-native. Uses Bitcoin's security, not a separate token or PoS chain.

### Limitations

- Liquidity management. Incoming liquidity is the recurring footgun; running a node well is a side hobby.
- Online requirement. A watchtower is needed if you go offline (otherwise risk of stale-commitment theft).
- Channel jamming. Pathological attackers can lock liquidity in unresolvable HTLCs. Mitigations: anchor outputs, package relay, jamming-resistant fee schedules in flight.
- Routing privacy is partial. Timing correlation, channel-size correlation, and payment-amount inference remain.
- Onboarding cost. Opening a channel is an on-chain tx; mempool spikes price out small users.

## Attack surface

| Attack | Description | Mitigation |
|--------|-------------|------------|
| Stale-commitment broadcast | Counterparty publishes old state | Watchtower, justice tx during dispute window |
| Channel jamming | Attacker locks HTLCs without settling | Anchor outputs, reputation-based fee tiers, PTLCs |
| Eclipse attack | Isolate node from honest peers | Multiple gossip peers, Tor circuits |
| Route probing | Send micropayments to map liquidity | Private channels, route blinding |
| Mempool flooding at force-close | RBF/CPFP exploitation | Anchor outputs, package relay |
| Custodial nodes (Wallet of Satoshi etc.) | KYC and takedown risk | Self-custody; check the wallet’s current support and custody model |

## Recent developments (2024-2026)

- Splicing: resize without closing.
- BOLT12 Offers: reusable invoices, no static metadata leak.
- Async payments: offline receivers buffer payments via a routing peer, end-to-end encrypted.
- PTLC adoption: Schnorr-only Lightning targeting late 2026.
- LSPs (Lightning Service Providers): non-custodial liquidity providers; standardized via LSPS.

## Primary sources

- [The Bitcoin Lightning Network](https://lightning.network/lightning-network-paper.pdf)
- [BOLT specifications](https://github.com/lightning/bolts)
- [BOLT 4: Onion Routing Protocol](https://github.com/lightning/bolts/blob/master/04-onion-routing.md)
- [BOLT 2: peer protocol and HTLC handling](https://github.com/lightning/bolts/blob/master/02-peer-protocol.md)
- [BOLT 12: Offers](https://github.com/lightning/bolts/blob/master/12-offer-encoding.md)
- [Lightning Labs: LND documentation](https://docs.lightning.engineering/lightning-network-tools/lnd)
- [ACINQ: Eclair](https://github.com/ACINQ/eclair)
- [Core Lightning documentation](https://docs.corelightning.org/)
- [Mutiny Wallet shutdown announcement](https://blog.mutinywallet.com/mutiny-wallet-is-shutting-down/)

For applications of Lightning, see [Fedimint](/kb/fedimint/) for federated ecash and gateway contracts, [RoboSats](/kb/robosats/) for peer-to-peer acquisition using hold invoices, and [BTCPay Server](/kb/btcpay-server/) for accepting payments. Their entries distinguish guardian, coordinator and wallet custody.
