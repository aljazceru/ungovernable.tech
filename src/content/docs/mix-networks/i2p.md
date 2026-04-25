---
title: "I2P"
tags:
  - "i2p"
  - "garlic-routing"
  - "anonymity"
  - "mix-networks"
  - "deep-dive"
---
*The Invisible Internet Project. An anonymous overlay network optimized for hidden services rather than clearnet browsing, with garlic routing, unidirectional tunnels, and a fully decentralized peer database.*

---

## I2P vs Tor in one paragraph

Tor is optimized to make clearnet browsing private. Most circuits exit to public sites. I2P is optimized to make a self-contained anonymous network. Most traffic stays inside I2P, between *eepsites*, IRC, BitTorrent, and other I2P-native services. There's no central directory; peer information lives in a fully distributed *netDB*. Tunnels are unidirectional (separate inbound and outbound). Clearnet exits exist (`outproxies`) but are explicitly secondary.

For "I want to use Twitter privately", use Tor. For "I want to host an anonymous service or run an anonymous BitTorrent client", I2P often does it better.

---

## Architecture

### Tunnels are unidirectional

Each I2P node has separate inbound and outbound tunnels:

```
Alice's outbound:  Alice → A → B → C → ...exit
Alice's inbound:   ...entry → D → E → F → Alice
```

A peer reaching Alice goes via her *inbound* tunnel; her replies go via her *outbound* tunnel. The two halves don't share relays. This makes timing correlation across in/out traffic harder than in Tor's symmetric circuits.

### Garlic routing

Each I2P packet ("clove") may bundle several inner messages (the "garlic bulb") with different destinations or delivery instructions. Effects:

- Padding via cover messages becomes natural. A clove can include a real message and a dummy.
- Multi-recipient delivery in one packet (replies, ACKs, and new requests piggybacked).
- Length analysis is harder because of variable garlic sizes.

### NetDB (network database)

Replaces Tor's centralized directory authorities. Peer information (RouterInfo) and destination information (LeaseSet) live in a distributed Kademlia-derived database. *Floodfill* nodes participate in storage; peers query nearby floodfills for routing data.

This is more decentralized than Tor (no authority quorum) but more complex to bootstrap. New nodes need a "reseed", initial RouterInfos signed by known sources, to join the netDB.

### Destinations and LeaseSets

- A *destination* is an I2P address, a long base64 string derived from key material.
- A *LeaseSet* is the destination's currently-published inbound tunnels (typically rotating every 10 minutes or so).
- Clients fetch the LeaseSet from netDB to know how to reach a destination.

The b32 form (`example.b32.i2p`) is a 52-character base32 of the destination's hash, analogous to a Tor v3 onion address.

---

## I2P-native applications

| App | What it is |
|-----|------------|
| **eepsites** | I2P hidden websites (`.i2p` URLs) |
| **i2p-bote** | Email-style asynchronous messaging via DHT |
| **i2psnark** | I2P-only BitTorrent client |
| **IRC over I2P** | I2P2 anonymous IRC servers |
| **i2pchat** / **MuWire** | File sharing and chat |

Web access uses the I2P proxy (default `127.0.0.1:4444`). Many services exist clearnet-equivalent inside I2P.

### Outproxies

A small number of nodes egress to the clearnet, typically restricted to specific use cases (HTTP only). I2P discourages clearnet exit as the primary use case. For that, prefer Tor.

---

## Cryptography

- Curve25519 + AES-256 for tunnel encryption.
- ECIES for message encryption (replaced ElGamal in 2023).
- Ed25519 signatures for newer destinations.
- Hash-based MACs for tunnel integrity.

I2P moved from ElGamal-2048 to ECIES + Curve25519 starting around 2021, with completion for new destinations by 2023. Older RSA-based destinations are deprecated.

---

## Two implementations

### I2P (Java)

The original. Heavier (JVM), feature-rich. Web console at `127.0.0.1:7657`. Default reseed and bundled apps. Most users.

### i2pd (C++)

Lighter, faster, embeddable. CLI-first, smaller resource footprint. A better fit for embedded devices and as a daemon. Compatible with the same network.

Both are fully interoperable. They are the same network, two clients.

---

## Performance

I2P typically has better aggregate throughput than Tor for in-network traffic. Many users with many tunnels and active BitTorrent shape a different bandwidth pattern. Latency varies similarly to Tor (seconds-scale for hidden-service round trips).

For BitTorrent specifically, I2P is the preferred anonymous network. Tor explicitly discourages BitTorrent because of its impact on exit relays and the protocol's tendency to leak peer identifiers.

---

## Threat model

| Property | Status |
|----------|--------|
| Sender unlinkability inside I2P | Yes (multi-hop unidirectional tunnels) |
| Receiver unlinkability inside I2P | Yes (LeaseSets rotate) |
| Defense against global passive observer | Limited. Same low-latency limitation as Tor |
| Sybil resistance | Floodfill voting plus per-peer rate limits; weaker than authority-vetted Tor |
| Censorship resistance | Strong. Fully distributed netDB, no central choke point |

Like Tor, I2P does **not** defend against an adversary observing both ends with traffic analysis. For that, use [Nym](/mix-networks/nym) or [Katzenpost](/mix-networks/katzenpost).

---

## Comparison with Tor

| Dimension | Tor | I2P |
|-----------|-----|-----|
| **Optimized for** | Browsing clearnet privately | Hidden services and in-network apps |
| **Routing** | Symmetric three-hop circuits | Asymmetric unidirectional tunnels (configurable hops) |
| **Directory** | Centralized authorities | Distributed netDB (Kademlia-derived) |
| **Hidden service address** | 56-char `.onion` (Ed25519) | 52-char `.b32.i2p` (hash of destination) |
| **Bandwidth model** | Bandwidth-weighted relay selection | All peers route by default |
| **BitTorrent** | Discouraged | Native and supported |
| **Bootstrapping** | Public consensus | Manual reseed |
| **Pluggable transports** | Many (obfs4, meek, snowflake) | Fewer; obfuscation roadmap |
| **Maturity** | Higher (older codebase, more usage) | Smaller community, active dev |

---

## Trade-offs

### Strengths

- Fully decentralized. No directory authorities to compromise.
- Garlic routing provides flexibility that Tor cells don't.
- Unidirectional tunnels are harder to correlate.
- Native BitTorrent. No exit-relay tension.
- Designed for in-network services.

### Limitations

- Smaller user base. Anonymity sets matter, and Tor's are bigger for many use cases.
- Bootstrapping is friction. Reseed dependence.
- Outproxies are a weak point for clearnet usage. Concentrated and limited.
- Documentation aimed at developers more than end users.
- No first-class browser. The typical setup is Java I2P plus Firefox configured for the proxy.

---

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Traffic confirmation | Same as Tor. A global observer can correlate |
| Sybil flooding netDB | Floodfill rate limits; reputation under research |
| Reseed compromise | Multiple reseed sources; pinned hashes |
| Malicious floodfill | Replicated stores; verification of signatures |
| Clearnet leakage via outproxies | Avoid outproxies for sensitive content |
| Application leakage | Use I2P-aware apps; audit configs |

---

## Recent developments (2024-2026)

- ECIES rollout completed for new destinations.
- i2pd packaging improvements; smaller binaries.
- Tunnel build encryption improvements (LS2 / ECIES-X25519).
- Ongoing PQ migration. Research and roadmap, no production deployment yet.
- Better mobile clients. Android (i2pd-based) is more polished.

---

## Related files

- [Overview - Mix Networks](/mix-networks)
- [Tor](/mix-networks/tor)
- [Nym](/mix-networks/nym)
- [Katzenpost](/mix-networks/katzenpost)
- [MOC - Metadata Privacy](/meta/moc-metadata-privacy)
- [MOC - Censorship Resistance](/meta/moc-censorship-resistance)

---

## Primary sources

- *I2P Documentation* — [geti2p.net/en/docs](https://geti2p.net/en/docs/)
- I2P specifications — [geti2p.net/spec](https://geti2p.net/spec)
- i2pd — [i2pd.website](https://i2pd.website)
- Zantout & Haraty, *I2P Data Communication System* (background paper).
- LS2 specification — *I2P LeaseSet 2 with ECIES*.

