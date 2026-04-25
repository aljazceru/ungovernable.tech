---
title: "GNS"
tags:
  - "gns"
  - "gnunet"
  - "naming"
  - "petnames"
  - "deep-dive"
  - "dns"
---
*A privacy-preserving, hierarchical, petname-based naming system that resolves through GNUnet's distributed hash table. Standardized as RFC 9498 in 2023. The most thought-through privacy story of any decentralized naming layer.*

---

## What GNS argues

The conventional decentralized-naming designs (ENS, Handshake, PKARR) ask how to replace the registrar. GNS asks a different question: what naming system would you design if privacy were a first-class requirement?

The answer is a system where:

- Looking up a name doesn't reveal the lookup to the network.
- The naming hierarchy is per-user, not global.
- Cross-user names are resolved through cryptographic delegation.
- No party — including the global infrastructure — can observe queries or correlate them across time.

This is closer to *petname systems* (Stiegler, Mark Miller) than to global registries. GNS plus petnames is what Mark Miller called the resolution of Zooko's triangle: secure, decentralized, and human-meaningful.

---

## How it works

### Zone keys are identities

Every user has an Ed25519 (or ECDSA-secp256r1) keypair. The public key is the zone identifier. Names are scoped per zone.

### Local petnames

You assign local nicknames to zones you've encountered:

```
my-zone:
  alice ─► <Alice's pubkey>
  bob   ─► <Bob's pubkey>
```

`alice.gnu` is *your* alice. It's meaningful only to you. Two users can both have `alice.gnu` pointing to different keys; that's fine because names are per-zone-relative.

### Hierarchical delegation

Inside Alice's zone, she can have her own subnames. You access them as `name.alice.gnu`:

```
my-zone:
  alice ─► <Alice's pubkey>

Alice's zone (resolved when you ask):
  blog  ─► <some destination>
  shop  ─► <some destination>
```

So you can ask for `blog.alice.gnu` — your local nickname for Alice plus her local name for blog. The resolution chain is: local zone → Alice's pubkey → DHT lookup → Alice's signed records.

### DHT storage

Each zone publishes a signed namestore under its public key in GNUnet's DHT. Records are encrypted under a key derived from the zone's pubkey plus the label being looked up. The important properties:

- The DHT can't see the queried name. A lookup of `blog.alice.gnu` doesn't reveal "blog" to the DHT — only an opaque ciphertext-keyed lookup.
- Records are encrypted. Without knowing the queried label, an observer can't decrypt records.
- Per-zone keys mean leaks don't cascade between zones.

This privacy property is unique among production decentralized naming systems.

---

## RFC 9498 (2023)

GNS was standardized by the IETF in September 2023 as RFC 9498 (Schanzenbach, Grothoff, Fix). The standard documents:

- Wire formats and crypto.
- Hierarchical delegation.
- DHT-based block format (encrypted resource records).
- Conflict resolution under delegation.
- Bridging to legacy DNS.

The RFC formalizes what GNUnet has implemented since around 2014. It is a published RFC, not a draft.

---

## GNUnet 0.26.0 (Nov 2025)

The reference implementation. GNUnet is a broader project (P2P framework, mesh routing, file sharing, voting, GNS), but GNS is the most-deployed component. Version 0.26.0 (November 2025) shipped:

- Full RFC 9498 conformance.
- Improved DHT throughput.
- Better integration with NSS (name service switch) on Linux.
- Multi-zone management UX.
- Working petname tooling.

Run on Debian or NixOS with `apt install gnunet` or equivalent; it brings up a node that participates in the GNS DHT.

---

## Trust model

| Property | GNS | DNS |
|----------|-----|-----|
| Lookup privacy | Yes (encrypted records, queries indistinguishable) | No (resolver sees query) |
| Authentication | Per-zone signature | DNSSEC (optional) + CA chain |
| Censorship | Encrypted DHT records resist takedown | Registrar / CA / ISP |
| Discovery | Petname-mediated (out-of-band) | Search engines + DNS root |
| Performance | DHT (slower) | Caching pyramid (fast) |
| Adoption | Niche | Universal |

The GNS design accepts performance and discovery costs in exchange for strong privacy and censorship-resistance.

---

## Petnames as a Zooko's-triangle resolution

Zooko's triangle says a name can be human-meaningful, decentralized, and globally unique, but supposedly not all three. GNS sidesteps this:

- Globally unique identifiers are zone keys (random Ed25519 pubkeys).
- Human-meaningful names are local petnames assigned by each user.
- Decentralized because no central authority maps petnames to zone keys.

The trick is that `alice.gnu` doesn't need to be globally unique, only locally. Different users may have different `alice.gnu`s. That's a feature: it matches how humans actually use names in the real world.

---

## Comparison

| System | Architecture | Privacy | Adoption |
|--------|--------------|---------|----------|
| GNS | DHT + petnames + per-zone keys | High (queries opaque) | Niche |
| ENS | Ethereum L1 + CCIP-Read | Low (lookups public) | High |
| Handshake | PoW chain + SPV | Low (chain public) | Niche |
| PKARR / Pubky | Mainline DHT + signed records | Low (records public, queries are key hashes) | Emerging |
| Tor `.onion` | Self-authenticating service IDs | High (rendezvous-routed) | Wide in Tor |

GNS and Tor `.onion` are the two privacy-respecting options. The others reveal the *what* of lookups even where they decentralize the *who*.

---

## Use cases

### Censorship-resistant overlay

Organizations or activist communities run a GNS zone hosted on a GNUnet node, distribute their public key to members, and use a petname like `org.gnu` inside their group. Records are encrypted; lookups don't reveal who's asking for what.

### Privacy-respecting web

A blog at `blog.alice.gnu` is reachable by anyone who has Alice's pubkey assigned to a petname. Visitors don't reveal "I went to blog.alice.gnu" to a recursive resolver — the GNUnet DHT lookup doesn't expose the human-readable label.

### Identity-rooted federation

Each user is a zone. Users delegate to other users they trust. The graph of cross-zone delegations forms a kind of web-of-trust at the naming layer.

---

## Trade-offs

### Strengths

- Privacy first. Queries are opaque to observers, including the DHT.
- Petname-based, so it sidesteps Zooko's triangle (locally meaningful rather than globally unique).
- Standardized as RFC 9498.
- Production implementation in GNUnet 0.26.0.
- Free, no chain, no fees.

### Limitations

- Discovery is hard. Without a global directory, finding a new zone needs out-of-band contact (the same as Tor v3 onion).
- Performance. DHT lookups are slower than DNS caching.
- Adoption is tiny. The GNUnet user base is small.
- Browser integration is missing. No mainstream browser supports GNS resolution natively.
- Operational dependency on GNUnet. Running GNS means running a GNUnet node, and the broader project complexity is non-trivial.

---

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| DHT poisoning | Per-zone signatures; record verification |
| Zone-key compromise | Rotate zone key; petname users verify out-of-band |
| Sybil at DHT layer | GNUnet's reputation and routing constraints |
| Side-channel via DHT timing | Mixing or batching on the DHT layer |
| Quantum (future) | Migration to PQ signatures planned |

---

## Operational patterns

### Personal stack

```
GNUnet node + GNS zone
  ├─ records: blog ─► IPFS hash, mail ─► server, ...
  ├─ delegate: friend ─► <friend's zone pubkey>
  └─ petnames: assign locally
```

Distribute the zone pubkey out-of-band (QR, Briar, in person).

### Bridge to legacy DNS

GNS can bridge a `.gnu` query (or any GNS-resolvable name) to traditional DNS through a configured gateway. Useful for hybrid deployments.

### Privacy-respecting org infrastructure

Org members all have `org.gnu` as a petname for the org's zone. Internal services (`wiki.org.gnu`, `mail.org.gnu`) resolve via GNS. Lookups don't leak to outsiders.

---

## Recent developments (2024-2026)

- RFC 9498 published in September 2023.
- GNUnet 0.26.0 (November 2025) brought RFC-conforming implementation.
- NLnet funding for GNUnet development continues.
- NSS module improvements for transparent system integration.
- Curve25519 / Ed25519 zone keys (deprecating older ECDSA defaults).

---

## Related files

- [Overview - Decentralized DNS](/decentralized-dns)
- [ENS](/decentralized-dns/ens)
- [Handshake](/decentralized-dns/handshake)
- [Pubky](/identity/pubky)
- [Overview - Mix Networks](/mix-networks) — adjacent privacy-of-routing concerns
- [Glossary](/meta/glossary) — Petname, Zooko's triangle

---

## Primary sources

- Schanzenbach, Grothoff, Fix, *The GNU Name System*, RFC 9498, IETF, September 2023.
- GNUnet — [gnunet.org](https://www.gnunet.org).
- GNS overview — [gnunet.org/en/gns.html](https://www.gnunet.org/en/gns.html).
- NLnet GNS project — [nlnet.nl/project/GNS](https://nlnet.nl/project/GNS).
- Stiegler, *An Introduction to Petname Systems*, 2005.
- Wilcox-O'Hearn, *Names: Distributed, Secure, Human-Readable: Choose Two* (Zooko's Triangle), 2001.

