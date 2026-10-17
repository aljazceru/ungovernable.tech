---
title: "Nomen"
slug: nomen
type: deep-dive
pillars: ["naming"]
readiness: experimental
description: "Nomen, a small decentralized naming protocol that combines Bitcoin for ownership with Nostr for records: how it works and its experimental status."
dek: "A small but conceptually interesting decentralized DNS protocol that composes two existing sovereign systems: Bitcoin for global ordering of name claims and Nostr for signed record updates. Nomen is not production-scale infrastructure today; its value is as a clean design pattern for globally unique names without launching a new chain or transport network."
updated: 2026-05-04
created: 2026-05-04
origin: vault
source: "03-Decentralized-DNS/Nomen.md"
aliases: ["Bitcoin and Nostr naming", "Nomen DNS"]
tags: ["nomen", "dns", "bitcoin", "nostr", "naming", "decentralized-dns", "deep-dive"]
---

## Summary

Nomen is a decentralized naming protocol by Ursus Camp. It tries to keep the minimum parts needed for DNS-like names:

1. **Global uniqueness** — solved by publishing a name claim on Bitcoin. Bitcoin's block ordering answers "who claimed this name first?"
2. **Owner-authenticated updates** — solved by Nostr events signed by the same key that owns the Bitcoin claim.
3. **Resolution infrastructure** — solved by indexers / name servers that read Bitcoin claims, follow Nostr relays, and answer DNS-like queries.

This makes Nomen a hybrid between [Handshake](/kb/handshake/) and Nostr NIP-05. Like Handshake, it uses a blockchain to order scarce human-readable names. Like NIP-05, it uses Nostr events as a signed record transport. Unlike [ENS](/kb/ens/), there is no smart contract registry; unlike [PKARR](/kb/pkarr/), the human-readable namespace is scarce and globally ordered.

Nomen is experimental and appears lightly maintained: the `ursuscamp/nomen` repository had 17 GitHub stars, 4 forks, 5 releases, and its most recent push was 2023-11-26 when checked on 2026-05-04. The specifications repository `ursuscamp/noms` is even smaller. That does not invalidate the design, but it means Nomen should be treated as a research prototype rather than a dependable name layer.

## Historical context

Decentralized naming repeatedly runs into Zooko's triangle: names that are human-meaningful, decentralized, and secure/global are difficult to combine. Earlier systems chose different points:

| Era | System | Choice |
|-----|--------|--------|
| 2011 | Namecoin | Bitcoin-like chain for `.bit` names |
| 2017 | [ENS](/kb/ens/) | Ethereum smart contracts for `.eth` names |
| 2018 | [Handshake](/kb/handshake/) | New PoW chain for root-zone replacement |
| 2020s | NIP-05 | Human aliases over DNS/HTTPS, mapped to Nostr pubkeys |
| 2023 | [PKARR](/kb/pkarr/) / [Pubky](/kb/pubky/) | Public key as name; no human-readable global name |
| 2023 | Nomen | Bitcoin orders name claims; Nostr transports updates |

Nomen's key historical move is refusing to bootstrap another consensus layer. It asks: if Bitcoin already provides censorship-resistant ordering, and Nostr already provides a relay-based signed-event network, can names be built by composing them?

The answer is technically yes, but with adoption caveats. Every resolver must index Bitcoin transactions and monitor Nostr relays; no major browser, OS resolver, or wallet ships this out of the box.

## Architecture

```text
Name claim:
  Bitcoin transaction commits to name + owner public key
  └─ first valid claim in Bitcoin ordering wins

Record updates:
  owner signs Nostr kind 38300 event
  └─ event contains DNS-like records / name metadata

Resolution:
  Nomen indexer scans Bitcoin for claims
  Nomen indexer subscribes to Nostr relays for updates
  indexer answers queries as a name server / explorer
```

The protocol separates **ownership** from **records**:

- Ownership is slow, final, and globally ordered through Bitcoin.
- Records are faster, mutable, and distributed through Nostr.
- Indexers assemble the view by applying protocol rules.

This is close to an event-sourced registry: Bitcoin establishes the root event, Nostr streams subsequent state transitions, and resolvers materialize the current state.

## Protocol pieces

### Bitcoin claim layer

Nomen claims are published to the Bitcoin blockchain. The repository describes the ownership rule as simple: the first valid claim to a name owns it. Bitcoin provides:

- A globally replicated append-only log.
- Work-backed ordering of conflicting claims.
- Censorship resistance proportional to Bitcoin transaction inclusion.
- No need for a bespoke token or chain.

Trade-off: claiming a name costs Bitcoin fees, is visible on-chain, and is subject to Bitcoin confirmation latency. There is also no smart-contract-enforced renewal or clawback logic unless specified in higher-level protocol rules.

### Nostr record layer

After a name is claimed, the owner publishes signed Nostr events to update records. The NOM specifications define Nostr event kinds:

| Kind | Purpose | Source |
|------|---------|--------|
| `38300` | Name records | NOM-02 |
| `38301` | Relay-published index data | NOM-04 |

This makes updates cheap and widely relayable. Because Nostr events are signed, an indexer can verify that a record update came from the owner key anchored by the Bitcoin claim.

Trade-off: Nostr relays are not guaranteed to retain every event. Robust resolution needs multiple relays, replay protection, and indexer persistence.

### Indexer / name server

The `ursuscamp/nomen` repository includes the Nomen Explorer, described as the first indexer or name server for the protocol. Indexers are not trusted to create ownership, but users do rely on them for availability and correct materialization unless they run their own.

The clean deployment model is:

- Run your own Nomen indexer.
- Configure clients to use it as a resolver.
- Cross-check results against Bitcoin and Nostr signatures when high assurance matters.

## Evidence at a glance

| Claim | Evidence | Confidence |
|-------|----------|------------|
| Nomen uses Bitcoin for name-claim ordering | `ursuscamp/nomen` README: claims are published to Bitcoin; first valid claim wins | High |
| Nomen uses Nostr for record updates | `ursuscamp/nomen` README and `ursuscamp/noms`; event kind `38300` for name records | High |
| The project is experimental / lightly maintained | GitHub API on 2026-05-04: 17 stars, 4 forks, last push 2023-11-26 | High |
| The specification is Nostr-native | `ursuscamp/noms` says NOMs are modeled after NIPs; event kinds `38300` and `38301` | High |
| Production deployment is limited | No mainstream resolver/browser support; hosted explorer exists but should not be confused with broad adoption | Medium |

## Maturity and active development

| Component | Repository | Maturity | Activity snapshot (2026-05-04) |
|-----------|------------|----------|--------------------------------|
| Nomen implementation / explorer | [ursuscamp/nomen](https://github.com/ursuscamp/nomen) | Prototype | 17 stars, 4 forks, 5 releases, Rust, MIT, last pushed 2023-11-26 |
| NOM specifications | [ursuscamp/noms](https://github.com/ursuscamp/noms) | Early spec | 1 star, 7 commits, last pushed 2023-11-22 |
| Hosted explorer | `nomenexplorer.com` | Demo / service | Referenced by README; availability should be checked before relying on it |

Interpretation: Nomen is worth tracking as a design primitive, but not as a mature censorship-resistance substrate. It lacks the implementation depth of [GNS](/kb/gnu-name-system/), the economic/security weight of [ENS](/kb/ens/), and the active tooling momentum of [PKARR](/kb/pkarr/).

## Use cases

### 1. Nostr-native human names

Nostr has public keys but still leans on DNS/HTTPS for human-readable aliases through NIP-05. Nomen gives a Nostr-native alternative:

```text
alice.<nomen namespace>
  Bitcoin claim -> Alice's public key
  Nostr record -> relays, service endpoints, profile records
```

This removes dependence on a web domain for the alias, while preserving human readability.

### 2. Bitcoin-anchored service names

Services that already trust Bitcoin finality can use Nomen names for endpoints, donation addresses, mirrors, or metadata. A resolver could return:

- A records / AAAA records for IP endpoints.
- TXT records for contact metadata.
- Nostr relay hints.
- Content hashes for [IPFS and Filecoin](/kb/ipfs-and-filecoin/) or Arweave mirrors.

### 3. Experiments in minimal dDNS composition

Nomen is useful for protocol designers because it demonstrates a modular pattern:

- Use a battle-tested global ordering layer for scarce names.
- Use a signed event network for mutable records.
- Let resolvers be independently operated.

This pattern may reappear in future Bitcoin, Nostr, or off-grid naming systems.

## Trade-offs

### Strengths

- **No new blockchain.** Bitcoin handles global ordering and anti-double-claim semantics.
- **No new transport layer.** Nostr handles signed event distribution.
- **Simple ownership rule.** First valid claim wins.
- **Nostr-native.** Fits the relay/event culture better than DNSSEC or EVM-only systems.
- **Self-hostable indexer.** Users can run their own name server rather than trusting a company.

### Limitations

- **Light adoption.** Tiny GitHub footprint and no mainstream client support.
- **On-chain privacy leak.** Name claims are public Bitcoin transactions.
- **Name squatting.** First-claim-wins systems invite squatting unless there are auction, renewal, or social-layer mitigations.
- **Relay availability.** Nostr updates may disappear unless relays and indexers persist them.
- **Indexer complexity.** Resolvers must watch both Bitcoin and Nostr, then apply protocol rules correctly.
- **No native lookup privacy.** Queries to a Nomen resolver can reveal names being resolved unless combined with [Overview - Mix Networks](/kb/mix-networks/) or private resolver operation.

## Attack surface

| Attack | Applies to | Mitigation |
|--------|------------|------------|
| Bitcoin transaction censorship | Name claims | Use fee bumping, multiple broadcast paths, [Tor](/kb/tor/) / [I2P](/kb/i2p/) for broadcast privacy |
| Name squatting | Scarce human names | Auctions, social registries, namespaces, or acceptance that names are scarce property |
| Nostr event suppression | Record updates | Publish to many relays; run archival relays; indexer persistence |
| Indexer equivocation | Resolution | Run local indexer; verify against Bitcoin + Nostr signatures; compare multiple indexers |
| Key compromise | Name owner | Hardware signer, multisig/threshold signing, preplanned rotation if protocol supports it |
| Lookup surveillance | Users | Local resolver, Tor/VPN, mixnet transport, or private information retrieval layer |

## Comparison

| System | Ownership substrate | Record update substrate | Human-readable | Maturity | Best fit |
|--------|---------------------|-------------------------|----------------|----------|----------|
| [ENS](/kb/ens/) | Ethereum contracts | Ethereum / CCIP-Read | Yes | High | Crypto-native identity and wallet names |
| [Handshake](/kb/handshake/) | Handshake PoW chain | HNS DNS records | Yes | Niche | Permissionless TLD ownership |
| [PKARR](/kb/pkarr/) | Ed25519 key | Mainline DHT | No | Emerging | Self-authenticating service discovery |
| [GNS](/kb/gnu-name-system/) | Zone keys + petnames | GNUnet DHT | Local petnames | Niche but standardized | Privacy-preserving lookup |
| Nomen | Bitcoin transaction ordering | Nostr signed events | Yes | Experimental | Nostr/Bitcoin-native naming experiments |

## Operational notes

If experimenting with Nomen:

1. Treat it as a lab protocol, not critical production DNS.
2. Run your own indexer if correctness matters.
3. Archive relevant Nostr events; do not assume arbitrary relays preserve history.
4. Publish record updates to several relays.
5. Keep the Bitcoin claim key in cold storage or a hardware signer.
6. Mirror important endpoints in [PKARR](/kb/pkarr/), `.onion`, or conventional DNS until client support matures.

## Primary sources

- Nomen implementation — [github.com/ursuscamp/nomen](https://github.com/ursuscamp/nomen).
- Nomen specifications — [github.com/ursuscamp/noms](https://github.com/ursuscamp/noms).
- NOM-02 — protocol v1 and Nostr kind `38300` name records.
- NOM-04 — relay-published index data and Nostr kind `38301`.
- Nostr protocol specifications — [github.com/nostr-protocol/nips](https://github.com/nostr-protocol/nips).
- Bitcoin protocol reference — [developer.bitcoin.org](https://developer.bitcoin.org/).
