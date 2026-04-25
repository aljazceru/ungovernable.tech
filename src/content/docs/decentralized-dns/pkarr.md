---
title: "PKARR"
tags:
  - "pkarr"
  - "dns"
  - "dht"
  - "mainline"
  - "ed25519"
  - "naming"
  - "deep-dive"
---
*A naming layer that uses an Ed25519 public key as the zone, signed DNS records as the payload, and the BitTorrent Mainline DHT as the registry. No blockchain, no registrar, no fees. Pairs with [Pubky](/identity/pubky) in 11-Identity, which is the identity stack built on top of this primitive.*

---

## What PKARR is

PKARR turns the DNS zone-file model on its head. Instead of asking "who owns this name?", it makes the name *be* a public key. The owner publishes signed DNS records (TXT, A, AAAA, SRV, CNAME, etc.) to a distributed hash table keyed by the hash of that public key. Anyone can look up the records, and signature verification proves the records came from the key holder.

The pieces:

- An Ed25519 keypair per zone. The public key is the zone identifier.
- DNS records (RFC 1035 wire format) authored by the zone owner.
- A signature over the encoded record set, made with the private key.
- The Mainline DHT (BitTorrent's DHT, around 10 million nodes) as the storage and lookup layer.
- BEP 44 mutable items as the DHT primitive that allows updatable, signed values.

There is no chain, no auction, no token, and no registrar. There is also no human-readable name — the zone identifier is the bare public key, usually rendered in a base32 form (`z32`).

---

## How resolution works

```
Owner side:
  (sk, pk)      = Ed25519 keypair
  records       = [TXT "homeserver=...", A 192.0.2.1, ...]
  signed_zone   = sign(sk, encode(records, seq))
  DHT[hash(pk)] = (signed_zone, seq, sig)

Resolver side:
  1. Compute hash(pk) from the requested name
  2. Look up the value in the Mainline DHT
  3. Verify signature against pk
  4. Parse records and return them to the application
```

The DHT lookup is a Kademlia-style iterative query (Maymounkov & Mazières, 2002). Mainline does not authenticate publishers, so the signature is what makes the value trustworthy: a record is valid only if it was signed by the key whose hash anchored the lookup. Republishing a record with a higher sequence number replaces older versions.

PKARR records are bound by the BEP 44 size limit (1000 bytes per item in typical practice), which forces compact encoding. Most deployments stay within a handful of records per zone.

---

## Wire format

PKARR records are standard RFC 1035 DNS resource records, packed into a DNS message and signed. The on-the-wire payload includes:

- The encoded record set.
- A 64-bit sequence number used by BEP 44 to order updates.
- A 64-byte Ed25519 signature.

Because the records are real DNS records, they round-trip cleanly through DNS tooling. A `pkdns` resolver can hand them straight to a system stub resolver, and the application sees ordinary `dig` output.

---

## pkdns — bridging into legacy DNS

`pkdns` (`github.com/pubky/pkdns`) is a recursive DNS server that resolves PKARR keys via a configurable TLD (commonly `.pkdns`). The bridge means:

- Browsers and system resolvers can reach PKARR-named services without changes.
- Existing TCP/IP applications work transparently.
- A user runs `pkdns` locally or points DNS at a community resolver.

For self-sovereign deployments, `pkdns` typically runs on the same host as the application, removing trust in any third party for resolution.

---

## Where it fits among decentralized name systems

| Feature | PKARR | [ENS](/decentralized-dns/ens) | [Handshake](/decentralized-dns/handshake) | [GNS](/decentralized-dns/gns) |
|---------|-------|---------|---------------|---------|
| Registry | Mainline DHT | Ethereum L1 | Handshake chain | GNUnet DHT |
| Cost | Free (DHT only) | Gas + rent | HNS auction | Free (GNUnet) |
| Resolution latency | DHT round-trip | RPC / CCIP-Read | SPV header sync | DHT round-trip (private) |
| Human-readable | No (key only) | Yes (`.eth`) | Yes (any TLD) | Yes (petnames) |
| Privacy of lookup | Low (DHT lookups visible) | Medium (RPC) | Medium | High (queries opaque) |
| Crypto | Ed25519 | secp256k1 + EVM | Schnorr / Cuckatoo32 PoW | Ed25519 / ECDSA |
| Governance | None (protocol only) | DAO + smart contracts | UTXO consensus | None |
| Maturity | Emerging (2025–26) | Production | Live mainnet | Standardized (RFC 9498) |

PKARR's pitch against the alternatives is the lowest-overhead option: no chain, no fees, no governance, just signed DNS records on a DHT that already exists. The cost is the absence of a human-readable layer and a different threat model than chain-anchored systems.

---

## Threat model

PKARR's threat model assumes the Mainline DHT is mostly available and not pervasively poisoned. It defends against:

- **Record forgery** — signatures bind records to the zone key.
- **Replay** — sequence numbers and timestamps order updates.
- **Registrar coercion** — there is no registrar to coerce.
- **TLD seizure** — there is no TLD.

It does not defend against:

- **Targeted record-hiding.** An adversary with significant DHT influence near a key's hash can refuse to serve it. Mitigations include republishing to multiple bootstrap nodes and pinning via known peers.
- **Lookup observation.** DHT queries leak the requested key hash to nodes the request passes through. PKARR is not a private-lookup system; for that, see [GNS](/decentralized-dns/gns) or query through Tor.
- **Key compromise.** Lose the key, lose the zone. There is no recovery path absent prior planning (threshold sigs, key rotation via signed delegation).
- **Quantum attack (future).** Ed25519 is not post-quantum. No specified migration yet.

The Mainline DHT was not designed for adversarial high-stakes use. Its scale (around 10M nodes) makes pervasive poisoning expensive but not impossible. Empirical adversarial studies of PKARR availability are an active area.

---

## Composition

PKARR is most useful when other systems sit on top of it.

| Layered on PKARR | Effect |
|------------------|--------|
| [Pubky](/identity/pubky) homeserver discovery | User publishes homeserver address as a TXT record; clients resolve and fetch data over HTTP. |
| Nostr NIP-05 ([Nostr](/identity/nostr)) | `nostr.json` served from a PKARR record instead of HTTPS — defeats DNS-level censorship of the alias. |
| Slashtags identifiers | Public-key-addressed app data using PKARR as the discovery layer. |
| TEE service addressing ([Overview - Confidential Computing](/confidential-computing)) | An attested confidential service publishes its endpoint and attestation key under a PKARR zone, removing the need for a CA-signed cert tied to a seizable domain. |
| Off-grid bootstrapping ([FIPS](/off-grid-networks/fips)) | Same key-as-address philosophy at the network layer. |

The recurring pattern is: a service holds a key, publishes a small, signed pointer through PKARR, and clients reach the service without any CA, registry, or registrar in the trust path.

---

## NIP-05 over PKARR

A practical example. Nostr's NIP-05 normally serves `alice@example.com` from `https://example.com/.well-known/nostr.json`. The trust falls back to TLS, DNS, and the CA system — DNS-level attacks can swap the `npub` silently.

Served via PKARR, the same alias becomes:

```
alice@<PKARR-key> → PKARR record points to homeserver
                  → fetch /.well-known/nostr.json
                  → contains npub
```

The DNS / CA chain is replaced by a DHT lookup and a signature check against the PKARR key.

---

## Limitations and current state

- **No human-readable names** without a layer on top (NIP-05 alias, petname client, Pubky homeserver-served handle).
- **Records must be small.** Non-trivial data is published via a homeserver pointer, not directly.
- **DHT churn.** Records must be republished periodically (around every 24 hours) or they expire from caches.
- **Smaller ecosystem** than ENS or Handshake. The main production users are Pubky, Slashtags, and a small set of Nostr-adjacent tools.
- **No standard for cross-zone naming.** Each zone is independent; building a hierarchy requires a separate convention (Pubky homeservers, GNS-style delegation, etc.).

---

## Implementations

- `pubky/pkarr` — reference Rust implementation of the protocol.
- `pubky/pkdns` — recursive DNS server bridging PKARR into legacy DNS.
- `pubky/pubky` — homeserver and client SDK that uses PKARR for discovery.
- `synonymdev/slashtags` — earlier alternative that helped develop the design.

---

## Recent developments (2024–2026)

- `pkdns` reached stable production with Linux and Docker deployments.
- Pubky homeserver and Pubky.app social went into public beta and launch in 2025.
- PKARR adoption picked up across Slashtags, Pubky, and small Nostr integrations.
- Community work on Nostr + PKARR bridges (NIP-05 over PKARR, cross-signing).
- No PQ-signature variant standardized yet.

---

## Related files

- [Pubky](/identity/pubky) — the identity and homeserver stack built on PKARR.
- [Overview - Decentralized DNS](/decentralized-dns) — broader naming context.
- [Nostr](/identity/nostr) — sibling key-rooted identity primitive; NIP-05 over PKARR is a common bridge.
- [ENS](/decentralized-dns/ens) — chain-anchored alternative with human-readable names.
- [Handshake](/decentralized-dns/handshake) — TLD-level alternative with PoW consensus.
- [GNS](/decentralized-dns/gns) — privacy-preserving alternative with opaque lookups.
- [FIPS](/off-grid-networks/fips) — same key-as-address pattern at the network layer.
- [Glossary](/meta/glossary) — PKARR, Mainline DHT, BEP 44, Ed25519.

---

## Primary sources

- Aiello, Hartshorn et al., *PKARR — Public-Key-Addressable Resource Records*, 2023.
- BEP 44 — *Storing arbitrary data in the DHT* (BitTorrent Enhancement Proposal).
- RFC 1035 — *Domain Names: Implementation and Specification* (record wire format).
- Maymounkov & Mazières, *Kademlia: A Peer-to-Peer Information System Based on the XOR Metric*, IPTPS 2002.
- pkarr — [github.com/pubky/pkarr](https://github.com/pubky/pkarr)
- pkdns — [github.com/pubky/pkdns](https://github.com/pubky/pkdns)
- Pubky homeserver — [github.com/pubky/pubky](https://github.com/pubky/pubky)
- docs.pubky.org

