---
title: "Pubky"
tags:
  - "pubky"
  - "pkarr"
  - "identity"
  - "dht"
  - "mainline"
  - "deep-dive"
---
*An identity and naming system from Synonym built around PKARR (Public-Key-Addressable Resource Records) over the Mainline DHT. Names are Ed25519 public keys, records are signed, and resolution needs no blockchain, DNS, registrar, or fees.*

---

## What Pubky is

Pubky combines several pieces into one identity stack:

- **PKARR** — names are keys; records are DNS-style signed entries stored on the DHT.
- **Pubky homeserver** — a per-user data layer that holds signed user content.
- **Pubky drive** — an HTTP-style addressing scheme over PKARR for user data.
- **Pubky.app social** — a permissionless, key-rooted social application built on the rest.

The design choice is to lean on existing P2P infrastructure (the BitTorrent Mainline DHT, around 10M nodes) rather than build a new chain. There are no tokens, no fees, and no consensus delay. The trade-off is small record sizes and a different threat model than blockchain naming systems like ENS.

---

## PKARR, the core primitive

### Mechanics

Each user generates an Ed25519 keypair. The public key is the *zone*. The user authors DNS-style records (TXT, A, AAAA, SRV, etc.), signs the zone, and publishes the signed record to the Mainline DHT under the keyhash.

```
User keypair: (sk, pk)
Zone records: [TXT "homeserver=...", A 192.0.2.1, ...]
Signature:    sign(sk, encoded_zone)
Published:    DHT[hash(pk)] = (encoded_zone, sig)
```

To resolve, anyone:

1. Computes `hash(pk)`.
2. Looks up the DHT.
3. Verifies the signature with `pk`.
4. Reads the records.

### Properties

- **No registry.** Mainline DHT is permissionless and ambient.
- **No fees.** Publishing and resolving are free.
- **No blockchain.** Latency is a DHT round-trip, not block time.
- **Self-authenticating.** A record is valid only if signed by the key whose hash anchors the lookup.
- **Updatable.** Republishing replaces older records; newer timestamp wins.

### Limitations

- **Records must be small.** Mainline DHT items have size constraints (around 1000 bytes in typical practice). PKARR uses compact encodings.
- **DHT churn.** A record must be republished periodically (around 24h) or it expires from caches.
- **DHT poisoning.** Mainline was not designed for adversarial high-stakes use. Signed records mitigate but do not eliminate availability attacks.
- **No human-readable names** without a layer on top, such as NIP-05-style aliases.

PKARR's threat model assumes the DHT is mostly available and not pervasively poisoned. It defends against record forgery via signatures but not against record-hiding; an adversary with significant DHT influence could refuse to serve a key.

---

## Pubky homeserver

A *homeserver* is the data plane that complements PKARR's naming plane. Each user has one or more homeservers, each a host that stores signed user data (posts, profile, follow lists, generic key-value records).

The homeserver address is published in PKARR records. Clients resolve a key, find the homeserver, and pull data over HTTP. Properties:

- **User-owned data.** The user signs data and chooses where to host it.
- **Portable.** Switching homeservers means republishing a PKARR record. Old data can be re-fetched and re-published.
- **Permissionless hosting.** Run your own homeserver, or use a public one.
- **Authenticated reads.** Records are signed, and clients verify before trusting.

Compared with ActivityPub, the federation feel is similar, but the user is the server-of-record via PKARR. Compared with Nostr relays, the model is more structured: homeservers store user data per user, while relays store events per relay.

---

## pkdns, a production DNS resolver

`pkdns` is a recursive DNS server that resolves `.pkdns` (or other configured) TLDs over PKARR. The effects:

- Standard DNS clients (browsers, system resolvers) can resolve PKARR keys via `pkdns`.
- Existing TCP/IP applications work transparently.
- PKARR bridges into the legacy DNS-based world.

A typical setup runs `pkdns` locally or on a network resolver, configures browsers to send `.pkdns` queries through it, and PKARR-rooted services then become reachable like any other domain.

---

## Pubky.app, a reference social stack

Pubky.app is a social application from Synonym that uses:

- **PKARR** for identity and homeserver discovery.
- **Pubky homeserver** for user data.
- **Web of trust** for filtering and discovery.
- **No relay model**, unlike Nostr; content lives on the user's homeserver, and gossip happens at the application layer.

It is a different bet than Nostr on the same identity primitive: more structured, less event-stream-shaped.

---

## Pubky vs Nostr at the identity layer

Both are key-rooted identity systems. They differ:

| Dimension | [Nostr](/identity/nostr) | Pubky |
|-----------|-----------|-------|
| Identity | secp256k1 / Schnorr (`npub`) | Ed25519 (PKARR key) |
| Discovery / addressing | Relays + NIP-05 | Mainline DHT (PKARR) |
| Data model | Append-only signed events to relays | Key-value signed records on homeserver |
| Naming | NIP-05 alias | PKARR + optional NIP-05 |
| Censorship resistance | Per-relay; multi-relay redundancy | Per-homeserver + DHT |
| Latency | Real-time event stream | HTTP fetch + DHT resolve |
| Maturity | Larger ecosystem (2024-2026) | Smaller, growing |

The two are more complementary than competing. Many users will hold both an Ed25519 PKARR key and a secp256k1 Nostr key, or use cross-signing to bind them.

### NIP-05 over PKARR

A useful pattern is to serve the Nostr `nostr.json` from a PKARR record instead of HTTPS. This defeats DNS-level censorship of NIP-05.

```
nostr-username@<PKARR-key> → PKARR record points to homeserver
                          → fetch /.well-known/nostr.json
                          → contains npub
```

---

## Trade-offs

### Strengths

- No blockchain, no token, no fees. Just cryptography and an ambient DHT.
- Self-authenticating names. The address proves the key.
- Composable with existing DNS via pkdns.
- No central registrar, so no takedown vector at the naming layer.
- The homeserver pattern provides more structure than Nostr's flat event log for some use cases (profile, content, follow lists).

### Limitations

- DHT availability is an assumption. Mainline is ambient, but adversarial scenarios are less studied than Tor or I2P.
- Records are small, so non-trivial data needs careful encoding.
- Less mature than Nostr. Smaller ecosystem of clients and integrations.
- Homeserver hosting is still an operational burden, and public homeservers re-introduce some centralization.
- Quantum: Ed25519-based, with no specified PQ migration yet.

---

## Operational patterns

### Personal stack

```
Generate Ed25519 keypair → Pubky identity
Run pkdns locally or use a community resolver
Publish PKARR record with homeserver pointer
Run a self-hosted homeserver (Docker, ~one-VM workload)
Use Pubky.app or another client
```

The equivalent of self-hosting an online presence without DNS or a domain.

### NIP-05 over PKARR

For Nostr users who want a censorship-resistant NIP-05 alias:

```
PKARR record → points homeserver to URL
homeserver → serves /.well-known/nostr.json
nostr.json → maps username → npub
```

A motivated adversary can attack the homeserver host but cannot compel ICANN or a registrar.

### Combined Nostr + Pubky stack

Hold both keys and bind them via cross-signed records. Use Nostr for real-time social and Pubky for structured content (long-form, profile, drive-style file storage).

---

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| DHT poisoning hides record | Republish to multiple bootstrap nodes; pin via known peers |
| Homeserver compromise | Records are signed; homeserver compromise affects availability, not authenticity |
| Key compromise | Same as Nostr — rotate via signed delegation; FROST for threshold custody |
| Quantum (future) | Migration plan to PQ signature scheme TBD |
| Sybil at DHT layer | Mainline's design wasn't adversarial-by-default; mitigations under research |
| pkdns trust | Run locally; verify resolver implementation |

---

## Recent developments (2024-2026)

- pkdns reached stable production with Linux and Docker deployments.
- The Pubky homeserver reference implementation matured.
- Pubky.app social went into beta and launch in 2025.
- Community work on Nostr + Pubky bridges and shared identity.
- PKARR adoption picked up in Slashtags, Pubky, and other integrations.

---

## Related files

- [Overview - Decentralized DNS](/decentralized-dns) — broader naming context including PKARR.
- [Overview - Decentralized Identity](/identity/overview-decentralized-identity) — formal DID / VC alternatives.
- [Overview - Identity & Pseudonymity](/identity)
- [Nostr](/identity/nostr) — sibling identity primitive.
- [FIPS](/off-grid-networks/fips) — same key-as-address philosophy.
- [Glossary](/meta/glossary) — PKARR, Mainline DHT, Pubky, Ed25519.

---

## Primary sources

- Aiello, Hartshorn et al., *PKARR — Public-Key-Addressable Resource Records*, 2023.
- pkarr — [github.com/pubky/pkarr](https://github.com/pubky/pkarr)
- pkdns — [github.com/pubky/pkdns](https://github.com/pubky/pkdns)
- Pubky homeserver — [github.com/pubky/pubky](https://github.com/pubky/pubky)
- docs.pubky.org
- Maymounkov & Mazières, *Kademlia: A Peer-to-Peer Information System Based on the XOR Metric*, IPTPS 2002.

