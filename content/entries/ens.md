---
title: "Ethereum Name Service (ENS)"
slug: ens
type: deep-dive
pillars: ["naming"]
readiness: battle-tested
description: "The Ethereum Name Service, the largest deployed blockchain naming system: how registration and resolution work, and how it bridges to ordinary DNS."
dek: "The largest deployed decentralized naming system."
updated: 2026-10-25
created: 2026-04-25
origin: vault
source: "03-Decentralized-DNS/ENS.md"
aliases: ["Ethereum Name Service", ".eth"]
tags: ["ens", "ethereum", "naming", "dns", "ccip-read", "deep-dive"]
---

*The largest deployed decentralized naming system. `.eth` names registered on Ethereum, used as wallet aliases, IPFS content hashes, decentralized website domains, DIDs, and the spine of crypto-native identity. On August 9, 2026, the "Next Era of ENS DAO" executive proposal **passed on-chain** (1.27M For / 480.69K Against) — the ENS Foundation is now an operating entity with a five-seat board (Nick Johnson, Alexander Urbelis as Executive Director, Kartik Talwar, Brett Sun, Anthony Leutenegger). The DAO retains its 54.6M ENS tokens and $16M operational wallet; the Foundation administers the ~$65M Endowment and receives 1M ENS for employee compensation (multi-year vesting). Protocol governance stays with tokenholders. The ICANN `.ens` gTLD application was submitted before the August 12 window close. ENS's transition from DAO experiment to institutional infrastructure is complete.*

## What ENS provides

A `.eth` name like `alice.eth` resolves to:

- An Ethereum address (canonical use).
- An IPFS or Arweave content hash (decentralized website).
- Email, social media, avatar, and other free-form text records.
- A list of supported coin types (multi-chain wallet alias).
- Service endpoints (Nostr relays, MX records, Lightning addresses).

The name is owned by the holder of the underlying NFT (since 2020, ERC-721) on Ethereum L1. Transfers are on-chain. Records are read through the Resolver contract pattern.

## Architecture

```
ENS Registry (singleton contract)
  ├─ owner(node)        ─► account that controls this name
  └─ resolver(node)     ─► contract that returns records

Resolver
  ├─ addr(node)         ─► Ethereum address
  ├─ contenthash(node)  ─► IPFS / Swarm / Arweave URI
  ├─ text(node, key)    ─► arbitrary key-value records
  └─ name(node)         ─► reverse resolution

Names form a hierarchy (alice.eth → alice.charity.eth → ...).
```

The Registry stores ownership; Resolvers store data. Anyone can write a custom Resolver contract — many do — to expose richer record types or off-chain backing.

## CCIP-Read (EIP-3668)

The single most consequential ENS development for scaling. CCIP-Read lets a Resolver redirect record lookups to an off-chain HTTPS endpoint with cryptographic proof:

```
client.resolve("vitalik.eth", "addr") ──► on-chain Resolver
                                     ──► returns OffchainLookup error with URL
                                     ──► client fetches URL
                                     ──► server returns signed answer
                                     ──► client verifies signature on-chain
```

Effects:

- Subdomains scale to millions without on-chain gas. Each subdomain is a database row plus a signature, not a transaction.
- Off-chain backed names (Coinbase Wallet's `cb.id`, Uniswap's `uni.eth`, Linea's `linea.eth`) hand out subdomains for free.
- Trust model: the client trusts the off-chain server's signing key, registered on-chain by the parent name's owner.

CCIP-Read became the dominant ENS pattern in 2024-2025.

## ENSv2 and Namechain

ENS’s 17 November 2025 post described a plan to build Namechain on Nethermind’s Surge. On 6 February 2026, ENS announced that ENSv2 would deploy exclusively on Ethereum L1 and that Namechain development would cease. ENSv2 itself remained on the roadmap.

The November Surge proposal predates the February decision. It is not evidence that Namechain was revived in August or September 2026.

## DNSSEC integration

Owners of regular DNS names like `example.com` can claim their name on ENS using a DNSSEC proof. The DNS owner publishes a TXT record signed by their DNSSEC chain; an Ethereum smart contract verifies the chain back to the IANA root and grants control of the matching ENS subtree.

Use cases: bridging legacy DNS holdings into ENS-resolvable form, gradual migration paths.

## ICANN engagement (2025–2026)

ENS has been actively engaging with ICANN as the organization prepares for its gTLD expansion program:

**ICANN gTLD timeline:**
- Application round opens: **April 2026**
- Earliest possible TLD delegation: **2028**

**Key developments:**
- Alex Urbelis (General Counsel) spoke at WIPO 25th Anniversary UDRP event (April 2025, Geneva).
- Presented at DNS-OARC on "Web2 Woes / Web3 Warfare" (October 2025, Stockholm).
- Presented at ICANN's Registry Operator's Workshop on DNS/ENS integration (October 2025).

**D3 Protocol partnership (announced ICANN 84):**
- Allows domain owners to tokenize domains with control represented by transferable tokens.
- Goal: bring liquidity, distribution, and monetization of Web3 to the domain ecosystem.
- Early integrations: `.box`, `.art`, `.locker` (Orange Domains).
- Registry operators can contact ENS Labs to add ENS functionality.

**ENS .brand gTLD application:**
- ENS Labs is considering applying for a `.ens` gTLD as a **closed .brand** TLD (not open to public registrations initially).
- Could support names like `wallet.ens`, `dapp.ens`.
- Earliest delegation: 2028 if pursued.
- Door left open to transition to an open TLD in the future.

This engagement positions ENS as a bridge between DNS and blockchain naming, pursuing both integration with existing registries and potential direct participation in the ICANN gTLD program.

## ENS as identity

Beyond wallet aliases, ENS underpins:

- Sign-In with Ethereum (EIP-4361 / SIWE), where proof of `alice.eth` substitutes for OAuth or email.
- DIDs (`did:ens`), a W3C DID method anchored on ENS records.
- Lensh and Farcaster social identifiers, which can bind to ENS.
- NIP-05 over ENS for Nostr identifiers resolved through ENS records.
- Lightning Address records on ENS for receiving payments.
- Avatar, banner, and location records that form a portable profile. A user's ENS name carries their cross-platform identity.

The threat model is Ethereum's: as long as Ethereum mainnet is live and the private key isn't compromised, the name resolves and records are signed by the owner.

## Comparison

| Feature | ENS | Handshake | PKARR | DNS + CA |
|---------|-----|-----------|-------|----------|
| Chain / substrate | Ethereum L1 | Handshake L1 | Mainline DHT | DNS hierarchy |
| TLD | `.eth` only | Any (you own root) | None / custom | Existing TLDs |
| Cost | Annual ETH-priced rent | One-time auction | Free | Annual registrar |
| Resolution | On-chain or CCIP-Read | Custom resolver | DHT lookup | DNS recursion + DNSSEC |
| Censorship surface | Ethereum L1 finality | Handshake hashrate | DHT availability | Registrar + CA + ICANN |
| Maturity | High (2017+) | Niche | Emerging | Universal |
| Browser support | Plugins, MetaMask, Brave | Limited | Limited | Native |

## Trade-offs

### Strengths

- Real, large user base (~3M+ names registered, daily resolutions in the millions).
- L1 anchoring gives the strongest finality of any decentralized name.
- Composable with EVM apps, DIDs, and social protocols.
- DNSSEC bridging preserves legacy holdings.
- CCIP-Read scales subdomains to millions in practice.
- The 2026 stay-on-L1 decision removes L2 fragmentation risk.

### Limitations

- Ethereum-coupled. ENS goes down if Ethereum does (functionally a non-issue, conceptually a coupling).
- Cost. Even with cheaper L1, premium `.eth` names rent in the hundreds-to-thousands USD per year. CCIP-Read subdomains help for app deployments but not for user-owned vanity names.
- TLD limitation. `.eth` only at the top; can't compete with Handshake-style namespaces.
- Reverse resolution gaps. Not every wallet sets the reverse record correctly; primary-name UX is uneven.
- CA-equivalent risk in CCIP-Read. If the off-chain server's key is compromised, that subname's records are forgeable for users that don't verify.

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Private key theft | Hardware wallet, multisig ownership of the name |
| Frontend phishing (homoglyph) | Browser warnings; petname systems |
| CCIP-Read server compromise | Periodic key rotation; users can fall back to on-chain |
| Resolver contract bug | Audited resolver patterns; default to PublicResolver |
| Smart-contract upgrade hijack | ENS DAO has timelocked governance |
| DNSSEC chain compromise | Same as DNSSEC threat model — narrowly scoped |
| Long-range Ethereum reorg | Wait for sufficient confirmations on registrar txs |

## Operational patterns

### Personal identity stack

```
Hardware-wallet-controlled .eth name
  ├─ addr ─► self-custodied Ethereum address
  ├─ contenthash ─► IPFS site (or Arweave for permanence)
  ├─ avatar ─► IPFS image
  ├─ text "url" ─► website
  ├─ text "com.github" ─► GitHub username
  ├─ text "com.twitter" / "social.nostr.npub" ─► social
  └─ text "lud16" ─► Lightning Address
```

A single `.eth` name as the root of online presence — the role email plus DNS plus a CA used to play.

### App subdomain deployment

`yourapp.eth` buys a `.eth` and uses CCIP-Read to issue `<user>.yourapp.eth` for each signup. Users get an ENS-resolvable subdomain at zero on-chain cost; the app keeps the parent name and the signing key.

### DNSSEC migration

A `.com` holder uses DNSSEC to claim the matching ENS namespace, then migrates services without losing legacy users.

## Recent developments (2024-2026)

- CCIP-Read went mainstream; major wallets and dApps integrate it.
- ENS DAO governance matured and the treasury is well-managed.
- ENS Labs spun off as a non-profit.
- Stay-on-Ethereum-L1 decision (Feb 2026); Namechain L2 abandoned.
- ENS gas costs dropped ~99% over 2025 (Dencun → Pectra → Fusaka).
- Fusaka (Dec 2025): gas limit raised to 60 million (2x from early 2025).
- 2026 roadmap targets 200 million gas limit (3x current), before ZK upgrades.
- DNSSEC oracle improvements; more TLDs supported.
- Lightning Address records standardized as an ENS text key.
- Storage scaling via blobs reduces effective registration cost.
- ENS app and ENS Explorer overhauled in 2026.
- ENSv2 protocol revision (ground-up rewrite) advancing on L1.
- **ENSv2 App + Explorer Alpha (May 11, 2026)** — New ENS App and ENS Explorer deployed on Sepolia testnet for community feedback ahead of mainnet.
- **ENSv2 Role-Based Permissions (May 19, 2026)** — Granular per-role access control for .eth names launches, replacing the all-or-nothing single-owner model. Supports separate wallets for record updates, resolver management, and administrative settings — enabling corporate treasuries, team accounts, and shared wallets without transferring full ownership.
- **ICANN 84 (2026)** — Active engagement; D3 Protocol partnership announced; .brand gTLD application under consideration for earliest 2028 delegation.
- **Institutional adoption signal (June 2026)** — The Republic of Türkiye Directorate of Communications registered `cbiletisim.eth` as its official decentralized identity, featured in Ankara at Türkiye's AI and blockchain initiative. First major government adoption of ENS.
- **ENS Labs × Immunefi $70K audit competition (Aug 18–Sep 14, 2026)** — 4-week audit competition for the new ENS Manager + ENS Explorer + supporting app infrastructure (Workers, Transaction-manager, Smart-account). 137,845 LOC, 306 reports submitted, 20 confirmed valid, 56 under review (Aug 31 snapshot). **Closed Sep 14 11:00 UTC on schedule** (vault TVL $69,981.17 Sep 21, declined $8 from Sep 14 close). Sep 20 ENS deadline to resolve all reports; Sep 28 results frozen; Sep 29 final 48-hour dispute window closes; **Oct 26 payment + public results publication**. Gating step before ENSv2 mainnet deployment.
- **"Next Era of ENS DAO" Foundation proposal PASSED Aug 9** (1.27M For / 480.69K Against) — ENS Foundation is now an operating entity with a five-seat board (Nick Johnson, Alexander Urbelis as Executive Director, Kartik Talwar, Brett Sun, Anthony Leutenegger); Foundation administers the ~$65M Endowment + 1M ENS for compensation; DAO keeps 54.6M ENS + $16M wallet.
- **Namechain status** — the Surge architecture post is dated 17 November 2025. ENS’s 6 February 2026 announcement supersedes it: ENSv2 on Ethereum L1, with Namechain development ceased.
- **ENS DAO Newsletter #120 (Sep 15, 2026)** — most DAO-content-rich newsletter of Q3:
  - **ENS token-transparency filing** (Blockworks report) — investors told `$ENS` holders can delegate votes but have **no dividend or revenue-distribution rights**.
  - **ENS as Registry Layer for Tokenized Assets** (ENS Labs blog) — pitches ENSv2 hierarchical registries to the tokenized-asset issuer ecosystem.
  - **One-Click Registration** (production in ENS App) — choose name, payment, profile in one flow.
  - **Name Activity Notifications** (ENS App beta) — addresses the user-research finding "people are afraid of losing control of their names"; same feature adds proactive expiry notifications.
  - **ensjs PR #377** — points Sepolia at the clean hackathon testnet deployment (ENSv1 + ENSv2).
  - **ens-contracts PR #572 (adraffy)** — **DNSSEC ancestor inceptions stored onchain** per `(node, type)` with new `getInception(name, type)` getter + `InceptionChanged` event (backwards-compat fallback to `inceptions(node)`). The change Sepolia has been waiting for to make DNSSEC import trust-anchored.
  - **ens-contracts PR #573 (hiddentao)** — `.eth` resolver deploy-bug fix; routes resolver-setting through `RegistrarSecurityController` when it owns the registrar, making the deploy order-independent.
  - **docs PR #589 (schmidsi)** — adds `.locker` to the custom-TLD implementations table (block 25925109 ownership verified).
  - **Endowment NAV $93M**, **3.08% blended APY** (Steakhouse August slides), August strategy earnings **$223K**. Rebalancing ETH toward stablecoins; custody of endowment Safe moved to **Foundation**.
  - **Premium sales $113K in August** (Blockful + anticapture analysis) — 3-month rising trend, offsetting declining new-registration revenue.
  - **Blockful September delegation-incentive pool 8K ENS** — final month.
  - **SafeNotes shutting down** (Meta-Governance declines continued support).
- **ENSIP-31: Payment Preferences (Sep 17, 2026)** — Unruggable Labs / nxt3d. Standardizes **recipient-side chain routing** at the protocol layer via ENSIP-24 data records with key `payment-preference[<multichainTokenHash>]`. Recipients publish an ordered, token-specific list of preferred chains; wallets read before resolving the receiving address. **Open question** — how to fingerprint a multichain token (symbols aren't canonical; addresses are per-chain; ENSIP-31 currently hashes an immutable snapshot of chain-specific token representations). Draft PR [ensdomains/ensips#87](https://github.com/ensdomains/ensips/pull/87). Forum: [discuss.ens.domains/t/ensip-31-payment-preferences/22431](https://discuss.ens.domains/t/ensip-31-payment-preferences/22431). This is the **first ENSIP of 2026 to standardize recipient-side routing intent at the protocol layer**.
- **ENSv2 plugin for MetaMask Agent Wallet v0.8.0 (Sep 15, 2026)** — package `@estmcmxci/mm-plugin-ensv2` adds Sepolia ENSv2 resolution, registration, records, primary names, and **ERC-8004 agent identity** to the MetaMask Agent Wallet CLI. First ENSv2 SDK path through the MetaMask Agent Wallet surface. **Sepolia only — mainnet blocked on audit close + ENS Labs + DAO go/no-go from Oct 26 onwards.**
- **Earlier Surge proposal** — the official ENS post describes a proposed rollup architecture in November 2025, before the February 2026 decision to stop Namechain development.
- **ICANN TSG on gTLD Integrations with Alternative Naming Systems — public comment Aug 10–Sep 21, 2026** — the only formal ICANN venue open in Q3 2026 specifically addressing whether a gTLD can be integrated with the same domain name in an alternative naming system (blockchain, mesh, DHT-based). Closes TODAY Sep 21. This is the single highest-signal ICANN policy event for the decentralized-DNS stack in Q3 2026.
- **Root KSK rollover — Oct 11, 2026 hard cutover; T-20 days as of Sep 21**; old-key retirement Jan 2027. Only scheduled global DNS event in 2026.

## Primary sources

- [ENS is staying on Ethereum, 6 February 2026](https://ens.domains/blog/post/ens-staying-on-ethereum)
- [Earlier Namechain/Surge proposal, 17 November 2025](https://ens.domains/blog/post/namechain-nethermind-surge)

- ENS docs — [docs.ens.domains](https://docs.ens.domains).
- ENS protocol — [ens.domains](https://ens.domains).
- EIP-3668 (CCIP-Read) — [eips.ethereum.org/EIPS/eip-3668](https://eips.ethereum.org/EIPS/eip-3668).
- EIP-4361 (Sign-In with Ethereum) — [eips.ethereum.org/EIPS/eip-4361](https://eips.ethereum.org/EIPS/eip-4361).
- Nick Johnson, *ENS Staying on Ethereum*, blog post Feb 6, 2026.
- ENS DAO governance forum — [discuss.ens.domains](https://discuss.ens.domains).
- Source — [github.com/ensdomains](https://github.com/ensdomains).

Continue with [Sovereign name lifecycle](/kb/sovereign-name-lifecycle/).
