---
title: "I2P (Invisible Internet Project)"
slug: i2p
type: deep-dive
pillars: ["anonymity"]
readiness: battle-tested
description: "I2P, the Invisible Internet Project: an anonymous overlay network optimised for hidden services, with garlic routing and every user a router."
dek: "The Invisible Internet Project. An anonymous overlay network optimized for hidden services rather than clearnet browsing, with garlic routing, unidirectional tunnels, and a fully decentralized peer database."
updated: 2026-09-04
created: 2026-04-25
origin: vault
source: "08-Mix-Networks/I2P.md"
aliases: ["Invisible Internet Project"]
tags: ["i2p", "garlic-routing", "anonymity", "mix-networks", "deep-dive", "post-quantum"]
---

## I2P vs Tor in one paragraph

Tor is optimized to make clearnet browsing private. Most circuits exit to public sites. I2P is optimized to make a self-contained anonymous network. Most traffic stays inside I2P, between *eepsites*, IRC, BitTorrent, and other I2P-native services. There's no central directory; peer information lives in a fully distributed *netDB*. Tunnels are unidirectional (separate inbound and outbound). Clearnet exits exist (`outproxies`) but are explicitly secondary.

For "I want to use Twitter privately", use Tor. For "I want to host an anonymous service or run an anonymous BitTorrent client", I2P often does it better.

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

## Cryptography

- Curve25519 + AES-256 for tunnel encryption.
- ECIES for message encryption (replaced ElGamal in 2023).
- Ed25519 signatures for newer destinations.
- Hash-based MACs for tunnel integrity.

I2P moved from ElGamal-2048 to ECIES + Curve25519 starting around 2021, with completion for new destinations by 2023. Older RSA-based destinations are deprecated.

### Post-quantum cryptography proposal (Proposal 169)

I2P is implementing post-quantum cryptography per **Proposal 169** (i2p.net/en/proposals/169-pq-crypto). The approach is **hybrid only** — combining classical and PQ primitives — so that breaking either alone does not compromise the system. Key implementation details:

**Key exchange (hybrid ML-KEM + X25519)**:
| Type | Code | Public key length | Notes |
|------|------|-----------------|-------|
| `MLKEM512_X25519` | 5 | 32 B | Leasesets only |
| `MLKEM768_X25519` | 6 | 32 B | Leasesets only |
| `MLKEM1024_X25519` | 7 | 32 B | Leasesets only |
| `MLKEM512` | 800 | Handshakes only | |
| `MLKEM768` | 1184 | Handshakes only | |
| `MLKEM1024` | 1568 | Handshakes only | Not for SSU2 (MTU limit) |

Key exchange sizes increase 8-15x over classical; this is the primary PQ overhead. **SSU2** (new transport) beta is Q3 2026 with MLKEM768 minimum MTU of 1318 bytes (IPv4). **NTCP2** (TCP transport) beta shipped Q1 2026, release Q2 2026.

**Signatures (hybrid MLDSA + Ed25519)**:
| Type | Code | Public key | Signature |
|------|------|-----------|---------|
| `MLDSA44` | 12 | 1312 B | 2420 B |
| `MLDSA65` | 13 | 1952 B | 3309 B |
| `MLDSA87` | 14 | 2592 B | 4627 B |

Signature sizes increase 38-76x over Ed25519 — this is a significant size and in-transit overhead. **MLDSA signature types are on hold until 2027-2028** pending IETF PLANTS working group decisions on algorithm selection and size reduction.

The ratchet-layer PQ implementation is enabled by default in I2P 2.11.0+ (2026-02). The handshake-layer PQ (NTCP2, SSU2) is staged: NTCP2 PQ in production Q2 2026, SSU2 PQ in beta Q2 2026, release Q3 2026. The delay for SSU2 is the MTU constraint: MLKEM1024 keys are too large for the 1500-byte MTU limit.

This makes I2P a concrete example of a live anonymity network doing phased PQ migration with hybrid primitives — the same cryptographic migration challenges that apply to TLS, SSH, and messaging systems apply here.

## Two implementations

### I2P (Java)

The original. Heavier (JVM), feature-rich. Web console at `127.0.0.1:7657`. Default reseed and bundled apps. Most users.

### i2pd (C++)

Lighter, faster, embeddable. CLI-first, smaller resource footprint. A better fit for embedded devices and as a daemon. Compatible with the same network.

Both are fully interoperable. They are the same network, two clients.

## Performance

I2P typically has better aggregate throughput than Tor for in-network traffic. Many users with many tunnels and active BitTorrent shape a different bandwidth pattern. Latency varies similarly to Tor (seconds-scale for hidden-service round trips).

For BitTorrent specifically, I2P is the preferred anonymous network. Tor explicitly discourages BitTorrent because of its impact on exit relays and the protocol's tendency to leak peer identifiers.

## 2026 releases, post-quantum ratchet, and Kimwolf stress test

I2P 2.11.0 (2026-02-09) raised the runtime baseline to Java 17, moved to Jetty 12, enabled post-quantum crypto at the ratchet layer by default, upgraded SAMv3 datagram support, and shipped first-round spam-attack mitigations. I2P 2.12.0 (2026-04-20) continued performance/security work, improved PQ interoperability, and fixed a SAMv3 lookup bug affecting Bitcoin and BitTorrent clients.

The Kimwolf botnet incident in February 2026 is a live operational lesson. Krebs on Security reported that Kimwolf operators attempted to join roughly 700,000 infected devices as I2P nodes while using the network for fallback command-and-control, degrading successful connections. For a decentralized anonymity network this is exactly the hard problem: openness makes bootstrapping and censorship resistance possible, but it also creates Sybil and spam pressure.

Maturity assessment: I2P is a mature production network, especially for in-network services and BitTorrent, but ongoing Sybil resistance and PQ migration are active engineering areas.

## Threat model

| Property | Status |
|----------|--------|
| Sender unlinkability inside I2P | Yes (multi-hop unidirectional tunnels) |
| Receiver unlinkability inside I2P | Yes (LeaseSets rotate) |
| Defense against global passive observer | Limited. Same low-latency limitation as Tor |
| Sybil resistance | Floodfill voting plus per-peer rate limits; weaker than authority-vetted Tor |
| Censorship resistance | Strong. Fully distributed netDB, no central choke point |

Like Tor, I2P does **not** defend against an adversary observing both ends with traffic analysis. For that, use [Nym](/kb/nym/) or [Katzenpost](/kb/katzenpost/).

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

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Traffic confirmation | Same as Tor. A global observer can correlate |
| Sybil flooding netDB | Floodfill rate limits; reputation under research |
| Reseed compromise | Multiple reseed sources; pinned hashes |
| Malicious floodfill | Replicated stores; verification of signatures |
| Clearnet leakage via outproxies | Avoid outproxies for sensitive content |
| Application leakage | Use I2P-aware apps; audit configs |

## Recent developments (2024-2026)

- ECIES rollout completed for new destinations.
- i2pd packaging improvements; smaller binaries.
- Tunnel build encryption improvements (LS2 / ECIES-X25519).
- Ongoing PQ migration. Research and roadmap, no production deployment yet.
- Better mobile clients. Android (i2pd-based) is more polished.

## September 04, 2026 Update — i2psnark Hardening Continues; 2.14.0 PQ-SSU2 Targeted Oct 2026

The i2p.i2p Java repo shows **27 commits Aug 24 → Sep 2**, concentrated in `i2psnark` (the built-in BitTorrent client):

- **i2psnark magnet/trackers** (Aug 28–29): UDP-URL-without-path validation, magnet-link tracker parsing (clip long magnets, save and show all trackers, use all trackers in magnet, add length from xl param to magnet name).
- **i2psnark disk-space** (Aug 31, Sep 1): Check available space when adding torrent files, stop FetchAndAdd if not enough space, show free disk space on add-torrent form, default tracker type to open on add tracker form.
- **i2psnark audio preview** (Sep 2): Increase min completion for audio preview, js audio playlist controls, loading directives for HTML5 elements, build fix from previous checkin.
- **i2psnark WIP** (Aug 27, ongoing): `i2psnark: v2 WIP part 7` — multi-commit refactor of the BitTorrent client internals.
- **Router** (Aug 29, 31): `Router: Ensure log gzipper finishes after shutdown signal` (signal-handler correctness), `reseed update` (Aug 31), `bump -5` (Aug 31, version-internal bump).
- **I2CP** (Aug 26, 30): `I2CP: Add new discardMessage() to session API` (Aug 26, was new last week), `I2CP: API interface javadoc clarifications` (Aug 30).
- **i2psnark KRPC** (Aug 26, 31): `i2psnark: Compress KRPC DG1 messages`, `i2psnark: Send sorted dictionaries in extensions as required by spec`, `i2psnark: Don't NPE on missing map in extension handshake` (Aug 31), `i2psnark: Compress UDP connect requests` (Aug 26 — was new last week).

**No I2P core release this window**; I2P 2.13.0 (Jul 24, 2026) remains current. Per proposal 169, **I2P 2.14.0 is targeted for October 2026 with the Hybrid MLKEM SSU2 release** (PQ handshake for the UDP transport layer). Proposal status table (Apr 9):
- **Ratchet**: Complete in Java I2P and i2pd (shipped)
- **NTCP2**: Beta Q1 2026 → Release Q2 2026 (shipped in 2.12.0)
- **SSU2**: Beta Q2 2026 → Release Q3 2026 (the missing piece, now ~3 months late from the Apr 9 schedule but on track for Oct)
- **MLDSA SigTypes 12-14**: On hold until 2027

The Oct 2026 2.14.0 target now looks achievable — the Aug/Sep i2psnark work and the I2CP API additions are the kind of housekeeping that precedes a major protocol-version cut-over.

See [Mix Networks Friday — September 04 2026 Weekly Update](/briefings/mix-networks/2026-09-04/) for the full weekly delta.

## Primary sources

- *I2P Documentation* — [geti2p.net/en/docs](https://geti2p.net/en/docs/)
- I2P specifications — [geti2p.net/spec](https://geti2p.net/spec)
- i2pd — [i2pd.website](https://i2pd.website)
- Zantout & Haraty, *I2P Data Communication System* (background paper).
- LS2 specification — *I2P LeaseSet 2 with ECIES*.
