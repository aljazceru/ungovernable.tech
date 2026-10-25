---
title: "Naming on Mesh and Off-Grid Networks"
slug: mesh-naming
type: explainer
pillars: ["naming", "mesh"]
description: "How mesh and off-grid networks name things without the global DNS: key-derived addresses, local registries and naming on Yggdrasil, cjdns and Reticulum."
dek: "Mesh networks don't run on the global DNS — they have to invent their own naming because there's no ICANN root zone, no registrar, and often no working internet connection. Two overlay approaches are Yggdrasil (key-derived IPv6 over an encrypted overlay) and cjdns (key-derived IPv6 over a DHT). On top of these sit application-layer naming systems — Briar's contact-graph, IPFS's content addressing, Nostr's NIP-05, and PKARR zones — that compose the broader off-grid identity stack. See Overview - Decentralized DNS for the comparative landscape; Overlay Naming - Tor .onion and I2P for the parallel hidden-service naming systems."
updated: 2026-10-25
created: 2026-06-22
origin: vault
source: "03-Decentralized-DNS/Mesh & Off-Grid Naming.md"
aliases: ["Mesh Naming", "Yggdrasil Addressing", "cjdns CryptoAuth", "Briar Address Book", "Off-Grid DNS"]
tags: ["mesh", "yggdrasil", "cjdns", "hyperboria", "briar", "off-grid", "naming", "deep-dive"]
---

## Why mesh naming is its own thing

A mesh network — community wireless, disaster-response, off-grid activism, darknet-over-radio — has three properties that break normal DNS:

1. **No upstream DNS resolver.** The global DNS is a tree anchored at the ICANN root zone; mesh nodes may not have a path to it.
2. **No stable IP addresses.** Nodes come and go; DHCP is the wrong abstraction.
3. **Adversarial environment.** You don't trust the operator next door any more than you trust your ISP.

Mesh naming systems replace the IP-address-plus-DNS-lookup model with **a key-derived identifier that is also a routable address**. The name, the address, and the cryptographic identity are the same thing. This is Zooko's triangle resolved in the same direction as PKARR and onion services, but in a network that may not reach the global internet at all.

## Yggdrasil Network

### What it is

Yggdrasil is an encrypted IPv6 overlay that gives every node a stable, cryptographically-derived IPv6 address. It runs as a userspace daemon (`yggdrasil`) on Linux, macOS, Windows, BSD, iOS, and Android; it appears as a TUN/TAP interface. Each node has an Ed25519 keypair; the IPv6 address is deterministically derived from the public key.

### Address format

```
200:<rest of address derived from NodeID>/128      (host address)
300:<rest of address>/64                             (routed prefix, for sharing with LAN clients)
```

- `200::/7` is the IANA range originally allocated for NSAP-mapped addresses (RFC 1888, deprecated by RFC 4048, currently unused).
- Yggdrasil uses `200::/8` for host addresses and `300::/8` for prefixes; the rest of the bits are derived from the node's NodeID.
- A node's NodeID is `sha512(curve25519_public_key)`, truncated by an "address collapse" algorithm that gives collision resistance comparable to a true 128-bit hash by counting leading `1` bits.

The result: `300:abcd:ef12:3456:7890:abcd:ef12:3456` is a stable, self-authenticating, routable address. There is no DNS lookup. There is no DHCP lease. There is no A record.

### How routing works

Yggdrasil is **name-independent**: identifiers (the IPv6 address) and network state (where the node is on the underlying network) are independent. The router maintains a spanning tree rooted at a peer-determined root, and each node has `coords` — a list of interface hops from the root to that node. Lookups use a Kademlia-like DHT of `NodeID → coords` to find paths.

The addressing post that defines this is "Addressing and Name-Independent Routing" (Arceliar, 28 July 2018) — see Primary Sources.

### What naming looks like on Yggdrasil

There is no built-in DNS. Naming happens at one of three layers:

1. **The IPv6 address itself is the name.** `300:abcd:...` is both the address and the identifier.
2. **DNS-over-Yggdrasil.** Community DNS resolvers (`loki.network`, `kroket.xyz`, etc.) publish their IPv6 addresses on the Yggdrasil network; users point their system resolvers at them. The global DNS zones resolve normally for nodes that can reach the public internet.
3. **Application-layer names.** Yggdrasil nodes often run a homeserver (often [Pubky](/kb/pubky/)) or a content-addressed system (often IPFS) on top. The Yggdrasil address is the network identity; the application maps the address to whatever the application needs.

### Maturity (2026)

- **Experimental.** Yggdrasil describes its software as alpha-stage and warns that future changes may break compatibility.
- Mobile port `yggdrasil-android`: active, recent releases.
- Embedded Go library release (Asciimoth, 2024–2025): lets you embed a Yggdrasil node in a Go application.
- Cross-compilation for routers (OpenWrt) maintained.
- Active community: a few thousand public peers on the global Yggdrasil network.
- PKARR integration: discussed in the 2026 PKARR ecosystem; PKARR over Yggdrasil as a transport is a natural fit because both are key-rooted, no-DNS, edge-to-edge.

### Strengths and limitations

**Strengths**
- The address is the key. Self-authenticating.
- Stable across network changes — name-independent routing.
- Full IPv6 stack on top; any IPv6 app works.
- End-to-end encrypted overlay.
- Multi-transport: can run over TCP, TLS, Unix sockets, QUIC.
- Lightweight enough to embed in a router or mobile app.

**Limitations**
- No human-readable names by default. The 200:/300: addresses are 32 hex chars — workable but not user-friendly.
- No native DNS; community resolvers fill the gap.
- Performance depends on underlying transport and spanning-tree state.
- Adoption is small (~thousand public nodes, plus private deployments).
- Sybil resistance at the DHT layer depends on the leading-1-bits trick — better than naive 128-bit truncation but not a full proof.

## cjdns

### What it is

cjdns is the older cousin of Yggdrasil. Written in C, originally designed by Caleb James DeLisle starting ~2010, it powers the Hyperboria community network. Like Yggdrasil, every node has an Ed25519 keypair and the IPv6 address is derived from the public key. Unlike Yggdrasil, it uses a Kademlia-based DHT directly for routing rather than a spanning tree.

### Address format

```
fc<rest of address derived from key hash>:/128
```

- cjdns uses the `fc00::/8` range (the IPv6 Unique Local Address range).
- The address is constructed from `sha512(public_key)` truncated to 128 bits; the first 8 bits are set to `fc`.
- Same property as Yggdrasil: address = key hash = identifier. There is no DNS.

### Routing: CryptoAuth

cjdns introduces a layer called **CryptoAuth**. Every packet has an authentication header. Switches verify the header is consistent with the claimed source — that the claimed source address could plausibly have signed the header with the corresponding private key. This defends against IP spoofing inside the mesh: a node cannot claim to be at another node's address without holding that node's private key.

The protocol details: CryptoAuth uses a handshake piggybacked on regular data packets, with a switch label that is bit-reversed for efficient lookup. Replay protection and forward secrecy are limited — the protocol has known limitations in this area (per PKT Cash analysis).

### Maturity (2026)

- Reference implementation in C: maintained, slow but steady cadence.
- Community network Hyperboria still operates (~hundreds of public nodes).
- Used as a substrate in some privacy-network projects (e.g., the original Project Meshnet, Althea).
- The cjdns codebase is showing its age (C, no active major feature work), but the protocol design is well-understood and forks have been used in research.

### Comparison with Yggdrasil

| Dimension | cjdns | Yggdrasil |
|-----------|-------|-----------|
| Language | C | Go |
| Routing | Kademlia DHT | Spanning tree + Kademlia DHT for NodeID→coords |
| Transport | UDP/encrypted | TCP, TLS, QUIC, Unix |
| Mobile support | Limited | Native Android port |
| Active development | Maintenance mode | Active v0.5.x |
| Adoption | Hyperboria (~hundreds) | Global Yggdrasil (~thousands) |
| Address range | `fc00::/8` | `200::/8` / `300::/8` |

Yggdrasil is the modern choice for new deployments; cjdns is the historical reference. Many of the design lessons — name-independent routing, key-derived addresses, encrypted overlay — fed directly from cjdns into Yggdrasil.

## Briar's address book

Briar is a peer-to-peer messenger for activists, journalists, and high-risk users. Its naming model is the simplest of the lot: there is no global namespace at all. The "address book" is built from contacts you've added out-of-band.

### How naming works

1. Each user has a long-term Ed25519 identity keypair.
2. The "name" of a contact is whatever you've called them locally.
3. To add a contact, you either:
   - Scan a QR code (offline, in-person).
   - Exchange a `briar://` URI over a secure channel.
   - Meet over Bluetooth / Wi-Fi / Tor and discover peers.
4. The contact's `briar://` URI encodes their public key, display name, and a "known fingerprints" hint.

The "name" is a string the user types in the contact list; the "address" is the public key, used for end-to-end encryption of direct messages and forum posts.

### Transport fallback

Briar uses the most aggressive transport fallback in the production privacy stack:

- **Internet available**: connect via Tor.
- **Internet available but Tor blocked**: connect via pluggable transports (Snowflake, meek, etc.).
- **No internet**: connect over Bluetooth or Wi-Fi to nearby contacts.

In the Bluetooth / Wi-Fi mode, "naming" is reduced to physical presence: you tap "Add contact", the phones discover each other over the local radio, exchange keys, and the contact is added. This is a kind of physical-layer out-of-band authentication, stronger than any DNS-based system.

### Maturity (2026)

- Briar 1.5.17 (March 2026) — current release.
- Briar Desktop 0.6.0-beta — released 2026.
- Active development; stable on Android, beta on desktop.
- Used by activists, journalists, dissidents; not mainstream, not meant to be.

### What Briar teaches about mesh naming

- "Naming" can be reduced to **out-of-band key exchange + a local petname system**. The global namespace is unnecessary.
- Strongest adversary model: no internet at all. The protocol is built so Bluetooth / Wi-Fi is a first-class transport.
- No DHT, no DNS, no chain. Just keys, contacts, and local trust.

## The off-grid naming stack

In practice, a serious off-grid deployment layers multiple systems:

```
Local mesh (Yggdrasil / cjdns)
  ├─ IPv6 address = node's public key
  ├─ Application-layer: Pubky, IPFS, Nostr, etc.
  ├─ Local DNS: optional, via community resolvers
  └─ Contacts: Briar / Briar-like; out-of-band exchange

Internet-side fallback (if a path exists)
  ├─ .onion v3 for sensitive services
  ├─ .b32.i2p for eepsites
  ├─ PKARR zone for DHT-direct discovery
  └─ ENS or Handshake for human-readable names
```

The mesh address is the network identity; the overlay names (onion, PKARR, ENS) are the application identities. A single Ed25519 keypair can be the master identity across all of these — a property that meshes well with [Pubky](/kb/pubky/)'s approach.

## Comparison

| System | Naming primitive | Internet required | Human-readable | Best for |
|--------|------------------|-------------------|----------------|----------|
| Yggdrasil | IPv6 = key hash | No | No (address only) | Encrypted IPv6 mesh |
| cjdns | IPv6 = key hash | No | No (address only) | Legacy mesh (Hyperboria) |
| Briar | Public key + local petname | No (BT/Wi-Fi work) | Local petname | Activist messaging |
| [Overlay Naming - Tor .onion and I2P](/kb/onion-and-i2p-naming/) | Ed25519 pubkey | Yes (Tor / I2P) | No | Hidden services |
| [PKARR](/kb/pkarr/) | Ed25519 pubkey | Yes (Mainline DHT) | No (pkdns bridge) | DHT-direct discovery |
| [GNS](/kb/gnu-name-system/) | Per-zone Ed25519 | Optional | Local petname | Privacy-respecting apps |
| [ENS](/kb/ens/) | Smart-contract NFT | Yes (Ethereum) | Yes (`.eth`) | Mainstream Web3 |
| [Handshake](/kb/handshake/) | UTXO chain | Yes (HNS resolvers) | Yes (TLD) | Permissionless namespaces |

## Trade-offs

### Strengths

- **Works without the global internet.** Yggdrasil and cjdns route over any underlying transport; Briar works over Bluetooth and Wi-Fi alone.
- **Name = key = address.** No DNS lookup, no CA, no trust path.
- **End-to-end encryption** is mandatory, not optional.
- **Adversary-resilient.** Sybil and DoS resistance built into the protocols.

### Limitations

- **Not human-readable.** A Yggdrasil address is 32 hex chars. Mesh + [PKARR](/kb/pkarr/) or + a DNS layer is needed for usability.
- **No global discovery.** Finding a new node usually means out-of-band exchange.
- **Small user bases.** None of these systems have billions of users.
- **Operational complexity.** Running a Yggdrasil node + a Briar instance + a PKARR homeserver is more work than spinning up a domain name.
- **Mixed maturity.** Yggdrasil is healthy; cjdns is maintenance-mode; Briar is small but committed.

## Attack surface

| Attack | Affected systems | Mitigation |
|--------|------------------|------------|
| Sybil at DHT layer | Yggdrasil, cjdns | Leading-1-bits trick; peer reputation; economic cost of keys |
| Key compromise | All | Hardware signer; threshold sigs (FROST); key rotation |
| Physical-layer attack | Yggdrasil, cjdns, Briar | Encryption at transport; out-of-band key exchange |
| Routing manipulation | Yggdrasil, cjdns | Tree depth checks; signed path information |
| Eavesdropping on Bluetooth | Briar | Encrypted channels; on-device key storage |

## Recent developments (2024–2026)

- **Yggdrasil** — experimental, alpha-stage software; future changes may break compatibility.
- **Briar 1.5.17 (March 2026)**, **Briar Desktop 0.6.0-beta (2026)** — active development continues.
- **Embedded Yggdrasil in Go applications** (Asciimoth, dev.to, 2024) — easier integration of Yggdrasil as a library.
- **PKARR over Yggdrasil** — community work on using PKARR's signed DNS records as a service-discovery layer for Yggdrasil services.
- **Hacker News renewed interest (May 2025)** — the original 2018 announcement post resurfaced on the front page, drove a wave of new experimentation.
- **I2P and Tor v3** continue to be the production overlays; the off-grid side is increasingly composed of Yggdrasil + Briar + Pubky.

## Primary sources

- [Yggdrasil project status](https://yggdrasil-network.github.io/)

- Yggdrasil addressing — `yggdrasil-network.github.io/2018/07/28/addressing.html`.
- Yggdrasil `yggdrasil-go` — `github.com/yggdrasil-network/yggdrasil-go`.
- Yggdrasil embedded Go library — `dev.to/asciimoth/yggdrasil-network-as-an-embedded-go-library-9h`.
- cjdns — `github.com/cjdelisle/cjdns`.
- Hyperboria — `hyperboria.net`.
- Briar — `briarproject.org`.
- CryptoAuth technical analysis — `crypto.pkt.cash/updates/compact-source-routing`.
