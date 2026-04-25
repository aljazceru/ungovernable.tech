---
title: "ENS"
tags:
  - "ens"
  - "ethereum"
  - "naming"
  - "dns"
  - "ccip-read"
  - "deep-dive"
---
*The largest deployed decentralized naming system. `.eth` names registered on Ethereum, used as wallet aliases, IPFS content hashes, decentralized website domains, DIDs, and the spine of crypto-native identity.*

---

## What ENS provides

A `.eth` name like `alice.eth` resolves to:

- An Ethereum address (canonical use).
- An IPFS or Arweave content hash (decentralized website).
- Email, social media, avatar, and other free-form text records.
- A list of supported coin types (multi-chain wallet alias).
- Service endpoints (Nostr relays, MX records, Lightning addresses).

The name is owned by the holder of the underlying NFT (since 2020, ERC-721) on Ethereum L1. Transfers are on-chain. Records are read through the Resolver contract pattern.

---

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

---

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

---

## ENSv2 and the Namechain reversal

The original plan was to launch an L2 (Namechain) and migrate ENS off L1 for cheaper transactions.

In February 2026, Nick Johnson announced ENS would abandon Namechain. The reasoning:

- Ethereum gas costs had dropped enough with Dencun (blobs) and later throughput improvements.
- Subdomains via CCIP-Read solved the scale problem without leaving L1.
- Staying on L1 preserves the maximalist censorship-resistance story: ENS records anchored to Ethereum mainnet.

Net effect: ENS is Ethereum-L1-resident going forward, with off-chain backing for cheap subdomains.

---

## DNSSEC integration

Owners of regular DNS names like `example.com` can claim their name on ENS using a DNSSEC proof. The DNS owner publishes a TXT record signed by their DNSSEC chain; an Ethereum smart contract verifies the chain back to the IANA root and grants control of the matching ENS subtree.

Use cases: bridging legacy DNS holdings into ENS-resolvable form, gradual migration paths.

---

## ENS as identity

Beyond wallet aliases, ENS underpins:

- Sign-In with Ethereum (EIP-4361 / SIWE), where proof of `alice.eth` substitutes for OAuth or email.
- DIDs (`did:ens`), a W3C DID method anchored on ENS records.
- Lensh and Farcaster social identifiers, which can bind to ENS.
- NIP-05 over ENS for Nostr identifiers resolved through ENS records.
- Lightning Address records on ENS for receiving payments.
- Avatar, banner, and location records that form a portable profile. A user's ENS name carries their cross-platform identity.

The threat model is Ethereum's: as long as Ethereum mainnet is live and the private key isn't compromised, the name resolves and records are signed by the owner.

---

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

---

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

---

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

---

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

---

## Recent developments (2024-2026)

- CCIP-Read went mainstream; major wallets and dApps integrate it.
- ENS DAO governance matured and the treasury is well-managed.
- ENS Labs spun off as a non-profit.
- Stay-on-Ethereum-L1 decision (Feb 2026); Namechain L2 abandoned.
- DNSSEC oracle improvements; more TLDs supported.
- Lightning Address records standardized as an ENS text key.
- Storage scaling via blobs reduces effective registration cost.

---

## Related files

- [Overview - Decentralized DNS](/decentralized-dns)
- [Handshake](/decentralized-dns/handshake)
- [GNS](/decentralized-dns/gns)
- [Pubky](/identity/pubky) — alternative philosophy
- [Overview - Decentralized Identity](/identity/overview-decentralized-identity) — did:ens
- [Nostr](/identity/nostr) — NIP-05 over ENS
- [Lightning Network Deep Dive](/financial-sovereignty/lightning-network-deep-dive) — Lightning Address records

---

## Primary sources

- ENS docs — [docs.ens.domains](https://docs.ens.domains).
- ENS protocol — [ens.domains](https://ens.domains).
- EIP-3668 (CCIP-Read) — [eips.ethereum.org/EIPS/eip-3668](https://eips.ethereum.org/EIPS/eip-3668).
- EIP-4361 (Sign-In with Ethereum) — [eips.ethereum.org/EIPS/eip-4361](https://eips.ethereum.org/EIPS/eip-4361).
- Nick Johnson, *ENS Staying on Ethereum*, blog post Feb 6, 2026.
- ENS DAO governance forum — [discuss.ens.domains](https://discuss.ens.domains).
- Source — [github.com/ensdomains](https://github.com/ensdomains).

