---
title: "ENS as Identity"
tags:
  - "ens"
  - "identity"
  - "siwe"
  - "did-ens"
  - "deep-dive"
---
*The Ethereum Name Service is the largest deployed crypto-native identity primitive. This file looks at ENS through the identity lens: what is bound to a name, how it is used for login and reputation, and how it composes with the rest of the vault's identity story.*

---

## What an ENS name holds

A `.eth` name's records cover most of an online presence:

| Record type | Use |
|-------------|-----|
| `addr` (multi-coin) | Wallet addresses across chains |
| `contenthash` | IPFS / Arweave / Swarm content for the website |
| `text "url"` | Personal website URL |
| `text "avatar"` | Avatar (often IPFS or NFT URI) |
| `text "description"` | Short bio |
| `text "com.github"` | GitHub username (cross-platform identity) |
| `text "com.twitter"` | X / Twitter handle |
| `text "social.nostr.npub"` | Nostr public key |
| `text "lud16"` / `text "lud06"` | Lightning Address |
| `text "email"` | Email |
| `text "org"` | Organization affiliation |
| `did` records | DID methods bound to the name |

The aggregate is a portable profile: one ENS name carries identity, money, social presence, and content into every dApp or wallet that integrates ENS resolution.

---

## Sign-In with Ethereum (EIP-4361 / SIWE)

The login flow that made ENS practical for non-crypto sites:

```
Site:   "Sign this message: 'Login to example.com at 2026-04-25T13:30:00Z, nonce ABC'"
User:   signs with wallet private key
Site:   verifies signature against the user's address
        looks up address → ENS reverse record → "alice.eth"
        starts session as alice.eth
```

What the site gets:
- Cryptographic proof of address ownership.
- An ENS-resolved alias for UX.
- No password, no OAuth provider, no email.

What the user gets:
- One-click auth across any SIWE-supporting site.
- No site-specific account creation.
- A portable wallet, and therefore portable identity.

SIWE is in production at Snapshot voting, OpenSea, ENS Manager, many DeFi UIs, and a growing set of non-crypto sites that want decentralized auth.

---

## did:ens — the DID method

ENS names can also be expressed as DIDs:

```
did:ens:alice.eth
```

Resolution dereferences ENS records into a DID Document. Public keys, service endpoints, and other DID-Doc-shaped data come from ENS text records.

Position vs other DID methods:

| Method | Anchor | Best for |
|--------|--------|----------|
| `did:ens` | Ethereum L1 | Crypto-native identity |
| `did:web` | DNS | Enterprise / government |
| `did:plc` | Bluesky log | Social ATProto |
| `did:ion` | Bitcoin / Sidetree | High-stakes Bitcoin-anchored |

`did:ens` slots in cleanly: when ENS is already the de facto wallet identity, formalizing it as `did:ens` for VC interop is a small step.

---

## Reputation signals

An ENS name accumulates verifiable reputation over time:

- Token holdings at the address.
- NFT ownership (POAPs, badges, certifications).
- DeFi history (positions, governance votes).
- Social-graph followers (Lens, Farcaster).
- Linked credentials via off-chain VCs whose subject is the ENS name.

This is real reputation in a sense traditional identity systems struggle with: publicly verifiable, cryptographically signed, and accumulated through behavior. The trade-off is that it is publicly visible, which is bad for privacy.

For pseudonymous use, separate ENS names per context. For sovereign identity, one name with deliberate reputation building.

---

## Lightning Address records

Bind a Lightning Address to an ENS name:

```
ENS records:
  text "lud16" = "alice@yourln.example"
  text "lud06" = "lnurl...."
```

Effect: anyone who can resolve `alice.eth` can pay you over Lightning. No Lightning-network-specific account, no Twitter `@`-handle dependency. The identity layer (ENS) and payment layer (Lightning) couple via the records.

This is the cleanest "send me money to my name" UX in 2026.

---

## NIP-05 over ENS

Nostr's NIP-05 verifies a `user@domain.com` handle by fetching a JSON file from `domain.com/.well-known/nostr.json` mapping usernames to npubs.

Bridge with ENS: serve the `nostr.json` from a CCIP-Read endpoint pinned to an ENS name's contenthash. Effect: NIP-05 verification of `alice.alice.eth` is resolvable through pure ENS without DNS.

```
NIP-05 client looks up alice@alice.eth
  ↓ ENS resolver
  ↓ contenthash → IPFS hash
  ↓ /.well-known/nostr.json
  ↓ verify npub
```

This couples Nostr identity to Ethereum-anchored naming. Useful for users who want non-DNS NIP-05.

---

## Privacy trade-off

A single ENS name as your "online presence" is convenient but anti-private:

- Cross-context linkability: every site using SIWE knows your other tokens, history, and NFTs.
- Public history: Etherscan exposes everything.
- Doxxing risk: if an `.eth` ever leaks to a real-world identity, the chain is fully searchable.

Mitigations:

- Pseudonymous ENS: register a name not tied to your real identity and use it consistently in pseudonymous contexts.
- Multiple ENS names for different contexts (work, public, private).
- Privacy-respecting wallets (Aztec, Railgun, privacy pools for shielded transactions).
- Rotate per context: don't reuse the wallet that holds your salary as your `alice.eth` login wallet.

The point: ENS-as-identity is a deliberate publicness choice. Use it where public identity helps you (reputation, social, payments). Don't use it where pseudonymity matters.

---

## Comparison with Pubky / Nostr / DID

| Property | ENS | Nostr | Pubky | did:web |
|----------|-----|-------|-------|---------|
| Substrate | Ethereum L1 | Pubkey + relays | Ed25519 + Mainline DHT | DNS |
| Cost | Annual rent | Free | Free | DNS registrar fee |
| Censorship | Eth L1 finality | Per-relay | Per-DHT | Registrar / CA |
| Reputation | On-chain history | Social graph | Pubky homeserver content | Issuer chain |
| Login | SIWE | NIP-42 / SignNostr | Pubky auth | OIDC + DID |
| Lightning binding | text records | Zaps + LNURL | Records | Records |
| Privacy default | Low (chain-public) | Medium (relays see metadata) | Medium | Low |

For sovereignty users who want public reputation: ENS. For pseudonymous social: Nostr. For DNS-free naming: Pubky.

---

## Use cases

### One-name identity stack

```
alice.eth
├─ wallet address (Ethereum, Bitcoin, Solana via multi-coin records)
├─ contenthash → IPFS site
├─ avatar → IPFS image
├─ Lightning Address → receive sats
├─ Nostr npub → social
├─ GitHub username → code
└─ links: Twitter, Bluesky, blog
```

A single name as the root of online presence.

### Pseudonymous reputation building

A pseudonym registers `pseudo.eth` and builds reputation through participation (DAO voting, contributions, content). The reputation is verifiable by anyone; the link to a real identity stays private as long as the pseudonym maintains opsec.

### App SIWE login

A new dApp uses SIWE; users sign in with their existing ENS-bearing wallet. Onboarding is one click. Compare with email-and-password registration.

### DID-VC issuance to ENS

A credential issuer (DMV, university) issues a VC whose subject DID is `did:ens:alice.eth`. The credential can be presented anywhere, and the subject identity is portable across web, mobile, and crypto contexts.

---

## Trade-offs

### Strengths

- Massive ecosystem. Works across most major wallets, dApps, and DeFi.
- Real-world adoption: millions of names, daily active use.
- Composable with DIDs, VCs, Lightning, Nostr, NIP-05.
- Rich record model, far richer than DNS or `did:key`.
- L1-anchored, with strong finality and censorship resistance.

### Limitations

- Cost: annual rent, and vanity names are expensive.
- Public-by-default. Privacy requires deliberate compartmentalization.
- Ethereum dependency. Outages or extreme gas spikes affect resolution UX.
- No native rotation. Name ownership rotates only via NFT transfer.
- Reverse-resolution gaps. Many wallets don't set the reverse record, breaking SIWE UX.

---

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Wallet key theft | Hardware wallet; multisig ownership; account abstraction |
| Phishing via homoglyph (`vita1ik.eth`) | Petname systems; UI warnings |
| ENS contract bugs | DAO has timelocked governance; audits |
| Reverse-record manipulation | UI displays both forward and reverse for verification |
| Compromised CCIP-Read backing server | Periodic key rotation; on-chain fallback |
| Forgotten resolver upgrade | Default to PublicResolver; UX nudges |

---

## Operational patterns

### Personal stack

```
Hardware-wallet-controlled .eth
├─ records as above
└─ optional: 2-of-3 multisig ownership for high-value names
```

### App / org stack

```
Org owns parent.eth
├─ CCIP-Read serves <user>.parent.eth subnames at scale
└─ users get their app-bound subname for free
```

### Multi-context separation

```
public.eth        ─ public reputation, social
work.eth          ─ professional presence
treasury.eth      ─ multisig for funds
ephemeral-N.eth   ─ short-term, deactivated after use
```

---

## Recent developments (2024-2026)

- CCIP-Read in mainstream use; millions of subnames issued cheaply.
- ENS stays on L1 (Feb 2026) — Namechain L2 abandoned.
- ENS DAO governance maturing; treasury well-managed.
- DNSSEC integration to bridge legacy DNS holdings.
- SIWE adoption beyond crypto-native sites.
- Lightning Address records standardized as an ENS text key.

---

## Related files

- [Overview - Decentralized Identity](/identity/overview-decentralized-identity)
- [Overview - Identity & Pseudonymity](/identity)
- [DID Methods](/identity/did-methods)
- [Verifiable Credentials](/identity/verifiable-credentials)
- [ENS](/decentralized-dns/ens) — protocol from the DNS lens
- [Nostr](/identity/nostr)
- [Lightning Network Deep Dive](/financial-sovereignty/lightning-network-deep-dive)
- [MOC - Composing Primitives](/meta/moc-composing-primitives)

---

## Primary sources

- ENS docs — [docs.ens.domains](https://docs.ens.domains).
- EIP-4361 (Sign-In with Ethereum) — [eips.ethereum.org/EIPS/eip-4361](https://eips.ethereum.org/EIPS/eip-4361).
- EIP-3668 (CCIP-Read) — [eips.ethereum.org/EIPS/eip-3668](https://eips.ethereum.org/EIPS/eip-3668).
- did:ens method spec — DIF.
- ENS DAO governance forum — [discuss.ens.domains](https://discuss.ens.domains).
- LNURL / Lightning Address — [github.com/lnurl/luds](https://github.com/lnurl/luds).

