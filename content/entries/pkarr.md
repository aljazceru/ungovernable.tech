---
title: "PKARR: Public-Key Addressable Resource Records"
slug: pkarr
type: deep-dive
pillars: ["naming", "identity"]
readiness: usable
description: "PKARR turns an Ed25519 public key into a DNS zone: signed records are published to the BitTorrent Mainline DHT, with no registrar involved."
dek: "A naming layer that uses an Ed25519 public key as the zone, signed DNS records as the payload, and the BitTorrent Mainline DHT as the registry."
updated: 2026-10-25
created: 2026-04-25
origin: vault
source: "03-Decentralized-DNS/PKARR.md"
aliases: ["Public-Key-Addressable Resource Records"]
tags: ["pkarr", "dns", "dht", "mainline", "ed25519", "naming", "deep-dive"]
---

*A naming layer that uses an Ed25519 public key as the zone, signed DNS records as the payload, and the BitTorrent Mainline DHT as the registry. No blockchain, no registrar, no fees. **Sep 21, 2026**: the Pubky ecosystem ended its release plateau with three tagged releases in 7 days — **pubky-app v1.10.0** (Sep 18, breaking the 32-day plateau since v1.7.0 Aug 13) and **pubky-app v1.9.0** (Sep 17) and **pubky-homeserver v0.12.0** (Sep 14 09:52 — missed by the Sep 14 weekly; ending 26-day plateau since v0.11.0 Aug 19). v1.10.0 = 45+ PRs (PWA service worker, OAuth completion, undo on reposts, cypress e2e utf-16 limit match). v0.12.0 = Docker default flips to homeserver (BREAKING); SDK two-stage auth flow publicly available (BREAKING for SDK); **PKARR-relay republishing enabled** in homeserver (`#580` by @andrei-21); rate-limit sort before evaluating (`#573`). **pkarr** trunk is in **shared-ci-workflows migration + dependabot** mode (Sep 18 / Sep 16 / Sep 15 commits); latest tag still **v8.0.1** (Aug 31). See [Pubky](/kb/pubky/) in 11-Identity for the full system.*

## What PKARR is

PKARR turns the DNS zone-file model on its head. Instead of asking "who owns this name?", it makes the name *be* a public key. The owner publishes signed DNS records (TXT, A, AAAA, SRV, CNAME, etc.) to a distributed hash table keyed by the hash of that public key. Anyone can look up the records, and signature verification proves the records came from the key holder.

The pieces:

- An Ed25519 keypair per zone. The public key is the zone identifier.
- DNS records (RFC 1035 wire format) authored by the zone owner.
- A signature over the encoded record set, made with the private key.
- The Mainline DHT (BitTorrent's DHT, around 10 million nodes) as the storage and lookup layer.
- BEP 44 mutable items as the DHT primitive that allows updatable, signed values.

There is no chain, no auction, no token, and no registrar. There is also no human-readable name — the zone identifier is the bare public key, usually rendered in a base32 form (`z32`).

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

## Wire format

PKARR records are standard RFC 1035 DNS resource records, packed into a DNS message and signed. The on-the-wire payload includes:

- The encoded record set.
- A 64-bit sequence number used by BEP 44 to order updates.
- A 64-byte Ed25519 signature.

Because the records are real DNS records, they round-trip cleanly through DNS tooling. A `pkdns` resolver can hand them straight to the operating system's local DNS resolver, and the application sees ordinary `dig` output.

## pkdns — bridging into legacy DNS

`pkdns` (`github.com/pubky/pkdns`) is a recursive DNS server that resolves PKARR keys via a configurable TLD (commonly `.pkdns`). The bridge means:

- Browsers and system resolvers can reach PKARR-named services without changes.
- Existing TCP/IP applications work transparently.
- A user runs `pkdns` locally or points DNS at a community resolver.

For self-sovereign deployments, `pkdns` typically runs on the same host as the application, removing trust in any third party for resolution.

## Where it fits among decentralized name systems

|| Feature | PKARR + [Pubky](/kb/pubky/) | [ENS](/kb/ens/) | [Handshake](/kb/handshake/) | [GNS](/kb/gnu-name-system/) |
|---------|-------|---------|---------------|---------|
| Registry | Mainline DHT | Ethereum L1 | Handshake chain | GNUnet DHT |
| Cost | Free (DHT only) | Gas + rent | HNS auction | Free (GNUnet) |
| Resolution latency | DHT round-trip | RPC / CCIP-Read | SPV header sync | DHT round-trip (private) |
| Human-readable | No (key only) — add petname/NIP-05 layer | Yes (`.eth`) | Yes (any TLD) | Yes (petnames) |
| Privacy of lookup | Low (DHT lookups visible) | Medium (RPC) | Medium | High (queries opaque) |
| Crypto | Ed25519 | secp256k1 + EVM | Schnorr / BLAKE2b + SHA3 PoW | Ed25519 / ECDSA |
| Governance | None (protocol only) | DAO + smart contracts | UTXO consensus | None |
| Maturity | Emerging (2025–26) | Production | Live mainnet | Standardized (RFC 9498) |
| Production app stack | Pubky Core (SDKs, social, Ring, Nexus) | — | — | — |

PKARR's pitch against the alternatives is the lowest-overhead option: no chain, no fees, no governance, just signed DNS records on a DHT that already exists. Pubky Core adds the application layer on top. The cost is the absence of a human-readable layer and a different threat model than chain-anchored systems.

## Threat model

PKARR's threat model assumes the Mainline DHT is mostly available and not pervasively poisoned. It defends against:

- **Record forgery** — signatures bind records to the zone key.
- **Replay** — sequence numbers and timestamps order updates.
- **Registrar coercion** — there is no registrar to coerce.
- **TLD seizure** — there is no TLD.

It does not defend against:

- **Targeted record-hiding.** An adversary with significant DHT influence near a key's hash can refuse to serve it. Mitigations include republishing to multiple bootstrap nodes and pinning via known peers.
- **Lookup observation.** DHT queries leak the requested key hash to nodes the request passes through. PKARR is not a private-lookup system; for that, see [GNS](/kb/gnu-name-system/) or query through Tor.
- **Key compromise.** Lose the key, lose the zone. There is no recovery path absent prior planning (threshold sigs, key rotation via signed delegation).
- **Quantum attack (future).** Ed25519 is not post-quantum. No specified migration yet.

The Mainline DHT was not designed for adversarial high-stakes use. Its scale (around 10M nodes) makes pervasive poisoning expensive but not impossible. Empirical adversarial studies of PKARR availability are an active area.

## Composition

PKARR is most useful when other systems sit on top of it.

| Layered on PKARR | Effect |
|------------------|--------|
| [Pubky](/kb/pubky/) homeserver discovery | User publishes homeserver address as a TXT record; clients resolve and fetch data over HTTP. |
| Nostr NIP-05 ([Nostr](/kb/nostr-identity/)) | `nostr.json` served from a PKARR record instead of HTTPS — defeats DNS-level censorship of the alias. |
| Slashtags identifiers | Public-key-addressed app data using PKARR as the discovery layer. |
| TEE service addressing ([Overview - Confidential Computing](/kb/confidential-computing/)) | An attested confidential service publishes its endpoint and attestation key under a PKARR zone, removing the need for a CA-signed cert tied to a seizable domain. |
| Off-grid bootstrapping ([FIPS](/kb/fips-mesh/)) | Same key-as-address philosophy at the network layer. |

The recurring pattern is: a service holds a key, publishes a small, signed pointer through PKARR, and clients reach the service without any CA, registry, or registrar in the trust path.

## NIP-05 over PKARR

A practical example. Nostr's NIP-05 normally serves `alice@example.com` from `https://example.com/.well-known/nostr.json`. The trust falls back to TLS, DNS, and the CA system — DNS-level attacks can swap the `npub` silently.

Served via PKARR, the same alias becomes:

```
alice@<PKARR-key> → PKARR record points to homeserver
                  → fetch /.well-known/nostr.json
                  → contains npub
```

The DNS / CA chain is replaced by a DHT lookup and a signature check against the PKARR key.

## Limitations and current state

- **No human-readable names** without a layer on top (NIP-05 alias, petname client, Pubky homeserver-served handle).
- **Records must be small.** Non-trivial data is published via a homeserver pointer, not directly.
- **DHT churn.** Records must be republished periodically (around every 24 hours) or they expire from caches.
- **Smaller ecosystem** than ENS or Handshake. The main production users are Pubky, Slashtags, and a small set of Nostr-adjacent tools.
- **No standard for cross-zone naming.** Each zone is independent; building a hierarchy requires a separate convention (Pubky homeservers, GNS-style delegation, etc.).

## Implementations

- `pubky/pkarr` — reference Rust implementation of the protocol.
- `pubky/pkdns` — recursive DNS server bridging PKARR into legacy DNS.
- `pubky/pubky` — homeserver and client SDK that uses PKARR for discovery.
- `synonymdev/slashtags` — earlier alternative that helped develop the design.

## Recent developments (2024–2026)

- `pkdns` reached stable production with Linux and Docker deployments.
- Pubky homeserver and Pubky.app social went into public beta and launch in 2025.
- **Pubky Core launched (2025-2026)** — a comprehensive open protocol suite extending PKARR with production SDKs (Rust, JavaScript, Swift, Kotlin), a semantic social graph, homeserver discovery, and RESTful HTTP APIs. See [Pubky](/kb/pubky/).
- PKARR adoption picked up across Slashtags, Pubky, and small Nostr integrations.
- Community work on Nostr + PKARR bridges (NIP-05 over PKARR, cross-signing).
- **Iroh integration** — Pubky Dev Community Call #2 (2026) explored integrating Iroh (a modern Rust peer-to-peer library) with PKARR for improved relay/transport.
- **No PQ-signature variant standardized yet.**

## Primary sources

- [hsd proof-of-work implementation](https://github.com/handshake-org/hsd/blob/master/lib/primitives/abstractblock.js)

- Aiello, Hartshorn et al., *PKARR — Public-Key-Addressable Resource Records*, 2023.
- BEP 44 — *Storing arbitrary data in the DHT* (BitTorrent Enhancement Proposal).
- RFC 1035 — *Domain Names: Implementation and Specification* (record wire format).
- Maymounkov & Mazières, *Kademlia: A Peer-to-Peer Information System Based on the XOR Metric*, IPTPS 2002.
- pkarr — [github.com/pubky/pkarr](https://github.com/pubky/pkarr)
- pkdns — [github.com/pubky/pkdns](https://github.com/pubky/pkdns)
- Pubky homeserver — [github.com/pubky/pubky](https://github.com/pubky/pubky)
- docs.pubky.org
