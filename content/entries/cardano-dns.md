---
title: "Cardano DNS"
slug: cardano-dns
type: deep-dive
pillars: ["naming"]
readiness: experimental
description: "Cardano DNS from Blink Labs combines Handshake top-level domains with Cardano native assets: an experimental approach to blockchain-owned names."
dek: "A young decentralized DNS effort from Blink Labs / Gimbalabs that combines Handshake top-level-domain ownership with Cardano native assets and smart contracts for second-level domains. The most concrete implementation is `cdnsd`, a DNS daemon that indexes Cardano data and serves records for configured TLD profiles."
updated: 2026-05-04
created: 2026-05-04
origin: vault
source: "03-Decentralized-DNS/Cardano DNS.md"
aliases: ["Cardano dDNS", "cDNS", "cdnsd"]
tags: ["cardano", "dns", "handshake", "decentralized-dns", "blinklabs", "cdnsd", "deep-dive"]
---

## Summary

Cardano DNS is not a universal replacement for DNS and not yet a broadly deployed public namespace. It is a set of open-source components for building a decentralized DNS market where:

- Top-level-domain authority can come from [Handshake](/kb/handshake/).
- Second-level names can be represented as Cardano native assets.
- DNS records can be written as on-chain datum data.
- A resolver/indexer (`cdnsd`) follows Cardano and Handshake state and serves DNS responses.

The project is important because it points to a compositional model: use the chain that already owns root-zone-like names (Handshake) and the chain with rich native assets / contracts (Cardano) for second-level marketplaces. That is different from [ENS](/kb/ens/), where the name and contract logic live in one EVM environment, and different from [PKARR](/kb/pkarr/), where there is no scarce human-readable name at all.

As of 2026-05-04, the project is active but early. GitHub API metadata showed:

| Repository | Stars | Forks | Language | Last pushed | Interpretation |
|------------|------:|------:|----------|-------------|----------------|
| [blinklabs-io/cardano-dns](https://github.com/blinklabs-io/cardano-dns) | 7 | 0 | Python | 2026-03-13 | Spec / shared design repo; small but current |
| [blinklabs-io/cdnsd](https://github.com/blinklabs-io/cdnsd) | 11 | 2 | Go | 2026-05-03 | Active resolver daemon implementation |

## Historical context

Most decentralized DNS projects choose one chain as the registry:

- Namecoin used a Bitcoin-derived chain for `.bit`.
- [Handshake](/kb/handshake/) created a PoW chain for top-level-domain ownership.
- [ENS](/kb/ens/) uses Ethereum contracts for `.eth` and resolver records.
- Unstoppable Domains uses blockchain records but a company-controlled product layer.

Cardano DNS instead splits the problem:

1. **Who controls a TLD?** Handshake is already designed for that.
2. **How do second-level names become programmable assets?** Cardano native assets and Plutus contracts can represent and transfer them.
3. **How do ordinary applications resolve records?** A DNS daemon indexes the chain state and answers normal DNS queries.

This design surfaced through Blink Labs' `cardano-dns` repo and a Project Catalyst Fund13 proposal for a decentralized DNS marketplace powered by Cardano and Handshake. The proposal describes a cross-chain, self-service DNS marketplace where Handshake TLD owners create second-level-domain marketplaces on Cardano.

## Architecture

```text
Handshake chain
  └─ proves/anchors TLD ownership

Cardano chain
  ├─ native asset represents domain / control token
  ├─ Plutus contracts validate updates and marketplace rules
  └─ inline datum stores DNSReferenceDatum / record data

cdnsd resolver
  ├─ follows Cardano chain via node / indexer configuration
  ├─ uses profiles for TLDs such as cardano, ada, hydra
  ├─ optionally follows Handshake data
  └─ serves DNS, DNS-over-TLS, metrics, and recursion fallback
```

The shape is closer to an indexer-backed DNS server than to a global recursive resolver. Users or infrastructure operators run `cdnsd`, configure a profile, and point clients or upstream resolvers at it.

## Main components

### `cardano-dns` design repository

The [blinklabs-io/cardano-dns](https://github.com/blinklabs-io/cardano-dns) repository is the shared design space for decentralized DNS on Cardano. It includes:

- Documentation for DNS record datum examples.
- Python proof-of-concept scripts (`dns.py`, `dns-kupo.py`) for parsing data and producing a zone file.
- Docker / BIND examples.
- Metadata and demo domain data.
- References to Plutus contract logic and token/datum concepts.

Key concepts in the repo include:

| Concept | Role |
|---------|------|
| `DNSReferenceDatum` | On-chain inline datum holding DNS record data |
| HNS token | Represents Handshake-related ownership / authority |
| DRAT / MHABAT | Token-policy-related primitives referenced by the design |
| `.cardano` examples | Preprod test records such as `village.cardano`, `town.cardano`, `city.cardano` |

The examples are explicitly pre-production test vectors. The repo's `write-datums-examples.md` distinguishes correct and incorrect datum examples, useful for implementers building validation logic.

### `cdnsd` resolver daemon

[blinklabs-io/cdnsd](https://github.com/blinklabs-io/cdnsd) is the production-shaped component: a Go DNS server that implements Cardano DNS resolution.

Its README describes it as:

> Resolver for Cardano-based second-level domains on Handshake top-level domains.

Important properties from the repository and docs:

- Configurable with YAML and environment variables.
- DNS listener defaults to UDP/TCP port `8053` rather than privileged port `53`.
- Optional DNS-over-TLS listener defaults to `8853`.
- Prometheus metrics support.
- Recursive DNS fallback can be enabled.
- Profiles define network, TLD, policy ID, script address, and chain intercept point.
- Profiles visible in `internal/config/profile.go` include `cardano-preprod-testing`, `ada-preprod`, `hydra-preprod`, and `auto-preprod`.

This makes `cdnsd` the practical entry point for experimentation.

### Project Catalyst Fund13 marketplace

The Project Catalyst proposal "Decentralized Domain Name System (DNS) Marketplace powered by Cardano and Handshake blockchains" frames the broader product:

- Open-source, self-service DNS marketplace.
- Handshake TLD owners can create marketplaces for second-level domains.
- Cardano smart contracts handle second-level-domain minting and updates.
- Domain records are represented with Cardano-native assets and on-chain data.
- Funding status observed: in progress, 3 of 5 milestones completed, 164,000 ADA distributed of 200,000 ADA requested.

Milestones reported by the project included Handshake signature validation in Cardano contracts, controller contracts, an example marketplace site, and domain contracts for minting/updating assets.

## Evidence at a glance

| Claim | Evidence | Confidence |
|-------|----------|------------|
| `cardano-dns` is a shared design repo for decentralized DNS on Cardano | Repository README: "Shared space for information about decentralized DNS on Cardano" | High |
| The goal is a Cardano-backed dDNS standard | README states goal of a standard for dDNS services on Cardano backed by blockchain data | High |
| `cdnsd` is the active resolver implementation | Repository description and README: Cardano DNS daemon implementing `cardano-dns`; last pushed 2026-05-03 | High |
| The system composes Cardano and Handshake | `cdnsd` README says Cardano-based second-level domains on Handshake TLDs; Catalyst proposal confirms cross-chain marketplace | High |
| Current deployment is preprod / experimental | Profiles and examples reference Cardano preprod; small repos; marketplace milestones still in progress | High |
| Mainstream adoption is low | No browser/OS native support and small GitHub footprint | High |

## Maturity and active development

Cardano DNS is best classified as **experimental but actively built**.

### Positive signs

- `cdnsd` had a very recent push (2026-05-03) when checked.
- The resolver has serious operational features: configuration, metrics, DNS-over-TLS, profiles, chain intercept configuration.
- Project Catalyst milestones indicate funded work rather than a weekend-only prototype.
- The design is open-source under MIT-style licensing.

### Caution signs

- GitHub stars and forks are tiny.
- Examples are mostly preprod/testnet oriented.
- The system requires users to run custom resolvers.
- Cross-chain proof of Handshake authority in Cardano contracts is complex.
- There is no mainstream client distribution, browser support, or public resolver ecosystem comparable to ENS gateways.

## How resolution works

A simplified Cardano DNS resolution path:

```text
query: village.cardano A

1. Client asks cdnsd.
2. cdnsd determines matching profile: TLD = cardano, network = preprod/mainnet profile.
3. cdnsd uses its local indexed state from Cardano chain data.
4. cdnsd validates whether the relevant token / policy / datum combination represents a valid record.
5. cdnsd emits a DNS answer or NXDOMAIN / validation failure.
```

For production Handshake-linked namespaces, an additional proof path exists: the TLD owner needs to demonstrate Handshake authority, and Cardano contracts use that authority to govern second-level domain issuance.

## Use cases

### 1. Handshake TLD marketplace on Cardano

A Handshake TLD holder wants to sell or distribute second-level domains without running a centralized registrar. Cardano DNS gives them:

- Cardano native assets for second-level names.
- Smart-contract rules for minting, transfer, and update rights.
- A DNS daemon that can serve records from chain data.

This is the headline use case from the Catalyst proposal.

### 2. Cardano dApp naming

Cardano applications could use `.ada`, `.hydra`, or other configured TLD profiles for dApp endpoints, metadata, or service discovery. The name can resolve to conventional IP addresses while ownership remains chain-backed.

### 3. Sovereign community namespace

A community can own or coordinate around a TLD and run several `cdnsd` resolvers. Members point their devices to those resolvers to resolve community names. This looks more like community infrastructure than global public DNS.

### 4. Disaster-resistant domain records

Because DNS data is derived from chain state, an adversary cannot simply coerce a registrar database row. They would need to compromise the chain keys, contract logic, resolver operators, or the underlying Handshake/Cardano security assumptions.

## Trade-offs

### Strengths

- **Cross-chain composition.** Uses [Handshake](/kb/handshake/) for TLD ownership and Cardano for programmable second-level assets.
- **Native assets.** Domain ownership can be represented as Cardano assets rather than off-chain database rows.
- **Open resolver.** `cdnsd` can be self-hosted and audited.
- **Operational tooling.** Metrics, configuration profiles, and DNS-over-TLS make it more deployable than many dDNS demos.
- **Marketplace path.** Project Catalyst funding pushes beyond pure protocol theory.

### Limitations

- **Early ecosystem.** Tiny repo adoption and mostly preprod examples.
- **Resolver dependency.** Users must configure `cdnsd` or trust someone else's resolver.
- **Complex trust stack.** Cardano + Handshake + resolver indexing is more complex than single-chain ENS.
- **Lookup privacy.** DNS queries to `cdnsd` are visible to the resolver unless wrapped in DoT/DoH/Tor/mixnet infrastructure.
- **Indexing correctness.** Resolver bugs can produce incorrect DNS answers even when chain state is correct.
- **Governance questions.** TLD owners, contract upgrades, and marketplace rules need explicit social and technical governance.

## Attack surface

| Attack | Where it lands | Mitigation |
|--------|----------------|------------|
| Compromised Cardano domain key | Second-level domain ownership / record updates | Hardware wallet, multisig, explicit key rotation patterns |
| Bad Plutus contract logic | Marketplace / update validation | Audits, small contract surface, staged rollout |
| Handshake proof failure | TLD authority bridge | Test vectors, independent verification, conservative acceptance rules |
| Resolver equivocation | `cdnsd` operator returns false records | Run local resolver; compare several resolvers; verify chain state directly |
| DNS query surveillance | Resolver observes names | Local resolver, DNS-over-TLS, Tor/I2P, future [Overview - Private Information Retrieval](/kb/private-information-retrieval/) patterns |
| Chain reorg / indexer lag | Stale or inconsistent answers | Confirmation thresholds, intercept points, monitoring |
| Centralized public resolver capture | Users depend on one gateway | Community-run resolvers and client-side verification |

## Comparison

| System | TLD authority | Record/asset layer | Resolver path | Maturity |
|--------|---------------|--------------------|---------------|----------|
| [ENS](/kb/ens/) | `.eth` on Ethereum | EVM registry + resolver contracts | Wallet/dApp libraries, gateways | High |
| [Handshake](/kb/handshake/) | Handshake chain | HNS records | hnsd / custom resolvers | Niche but live |
| Cardano DNS | Handshake TLD + Cardano contracts | Cardano native assets + inline datums | `cdnsd` | Experimental, active |
| [PKARR](/kb/pkarr/) | Public key itself | BEP44 mutable item on Mainline DHT | pkdns/native clients | Emerging |
| [GNS](/kb/gnu-name-system/) | Zone keys + petnames | GNUnet encrypted DHT records | GNUnet resolver/NSS | Niche, standardized |

Cardano DNS is strongest where the desired product is not merely a name, but a marketplace or ownership system around names. For a single service endpoint, [PKARR](/kb/pkarr/) is simpler; for broad wallet identity, [ENS](/kb/ens/) has much more distribution.

## Operational notes

If testing Cardano DNS:

1. Start with `cdnsd` rather than hand-parsing datums.
2. Use preprod profiles (`cardano-preprod-testing`, `ada-preprod`, `hydra-preprod`) until the contract and marketplace flow are stable.
3. Run with query logging disabled if resolver privacy matters.
4. Put `cdnsd` behind local-only access or a trusted network first; public recursive DNS is an abuse surface.
5. Monitor Prometheus metrics and chain sync lag.
6. Keep conventional DNS, [Handshake](/kb/handshake/), or [PKARR](/kb/pkarr/) mirrors until user resolvers are common.

## Primary sources

- `cardano-dns` design repository — [github.com/blinklabs-io/cardano-dns](https://github.com/blinklabs-io/cardano-dns).
- `cdnsd` resolver daemon — [github.com/blinklabs-io/cdnsd](https://github.com/blinklabs-io/cdnsd).
- Cardano DNS datum examples — [docs/write-datums-examples.md](https://github.com/blinklabs-io/cardano-dns/blob/main/docs/write-datums-examples.md).
- `cdnsd` profiles — [internal/config/profile.go](https://github.com/blinklabs-io/cdnsd/blob/main/internal/config/profile.go).
- Project Catalyst Fund13 proposal — [Decentralized DNS Marketplace powered by Cardano and Handshake](https://projectcatalyst.io/funds/13/cardano-open-developers/decentralized-domain-name-system-dns-marketplace-powered-by-cardano-and-handshake-blockchains).
- Handshake protocol — [handshake.org](https://handshake.org).
