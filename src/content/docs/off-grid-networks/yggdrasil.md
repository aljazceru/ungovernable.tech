---
title: "Yggdrasil"
tags:
  - "yggdrasil"
  - "overlay"
  - "ipv6"
  - "mesh"
  - "off-grid"
  - "deep-dive"
---
*An end-to-end encrypted IPv6 overlay mesh. Every node has an IPv6 address derived from its public key, traffic is automatically encrypted between nodes, and the network self-organizes via greedy routing on a spanning tree.*

---

## What Yggdrasil is

Yggdrasil is a small (~10K LoC Go), single-binary mesh overlay. Run `yggdrasilctl` on two computers anywhere in the world that can reach each other on any transport (TCP, link-local Ethernet, Tor SOCKS, WireGuard tunnel, AX.25 packet radio), and they get a routable, encrypted IPv6 link.

Compared with Tor: faster, no anonymity goal, full IPv6 connectivity including incoming connections.
Compared with WireGuard / Tailscale: no central coordination, no enrollment, no dependency on a control plane.
Compared with cjdns: simpler design, more active development.

The address space is `200::/7` (i.e. the first byte is `0x02` or `0x03`), an IPv6 prefix derived deterministically from each node's Ed25519 public key. Two nodes with overlapping addresses can never coexist; collisions are infeasible.

---

## How it works

### Identity = key = address

Each node runs Ed25519 keys. The IPv6 address is derived from a SHA-512 hash of the public key: count the leading binary `1`s of the hash and prefix with that count, fitting into the `200::/7` space. The first byte is `0x02` (with `0x03` reserved for the routable `/64` prefix). This means:

- The address proves the key (the hash makes deriving from the address back to a key infeasible without knowing the pubkey).
- Encrypted sessions to an address authenticate the peer's key; no separate PKI.
- No address allocation; no DHCP; no NAT.

### Routing

Yggdrasil builds a spanning tree of all reachable nodes (any node can volunteer as root; lowest public key wins ties). Once the tree exists, every node has tree coordinates.

Greedy forwarding: send to the neighbor with tree coordinates closest to the destination. This works even when the path is not on the tree; a path through any well-connected neighbor that is "closer" in tree-distance suffices.

Routing is *eventually consistent*; topology changes propagate over seconds to minutes. Not optimized for ultra-low-latency critical paths but good for general-purpose connectivity.

### Encryption

All traffic between Yggdrasil nodes is encrypted with a Noise-derived per-session key. There is no plaintext mode. Hop-by-hop encryption between adjacent nodes plus end-to-end ChaCha20-Poly1305 between source and destination.

### Peering

A new node needs at least one peer to bootstrap. Public peers are listed in `yggdrasilctl getpeers` and on community lists. Once peered, the node discovers others via the tree.

---

## What you get

A user-space network interface (`tun0` on Linux/macOS) with a stable IPv6 address. Anything that speaks IPv6 just works:

```
ssh user@200:abcd:1234::1
ping 200:abcd:1234::1
http://[200:abcd:1234::1]:8080
```

No port forwarding, no DDNS, no certificate ceremony. End-to-end encrypted by Yggdrasil; layer TLS on top if you want app-level auth.

---

## Topology patterns

### Sysadmin LAN

Yggdrasil on every laptop, server, and Raspberry Pi. A single peering line in each config. Now everything routes to everything regardless of NAT or roaming networks.

### Hidden services without Tor

Run a public-facing HTTP server bound only to the Yggdrasil interface. Reachable to anyone running Yggdrasil; invisible to clearnet scans.

### Off-grid IP

Yggdrasil runs over heterogeneous transports. A LAN-only Yggdrasil mesh in a building combined with one node bridging via internet peering yields a single address space spanning local-only and global. If the internet leg goes down, local nodes keep talking.

### Tor / I2P bridging

Peer over `socks5://127.0.0.1:9050` to use Tor as the transport. Yggdrasil traffic flows through Tor circuits, anonymizing the underlying IP while preserving Yggdrasil's routing semantics.

---

## Trust properties

| Property | Status |
|----------|--------|
| Hop-to-hop encryption | Yes (Noise) |
| End-to-end encryption | Yes (ChaCha20-Poly1305 from source to destination) |
| Authentication of peer | Yes (address = key) |
| Anonymity | No; peers see your IP and your Yggdrasil address |
| Forward secrecy | Per-session, yes |
| Post-quantum | Not yet; Curve25519/Ed25519 |
| Censorship resistance | Reasonable; runs over any byte transport |

Yggdrasil is not an anonymity tool. Use Tor or I2P for anonymity; use Yggdrasil for connectivity-with-encryption when you can't use cleartext IP.

---

## Comparison

| System | Routing | Encryption | Identity | Anonymity |
|--------|---------|------------|----------|-----------|
| **Yggdrasil** | Greedy on spanning tree | Noise + ChaCha20-Poly1305 | Ed25519 = address | No |
| **cjdns** | DHT-based + path-vector | Curve25519 | Curve25519 = address | No |
| **Tor** | Circuit, three-hop onion | Layered AES | TLS to relays | Yes |
| **I2P** | Garlic, unidirectional | ElGamal + AES | Destination keys | Yes |
| **WireGuard** | Static routes / configs | Curve25519 + ChaCha20-Poly1305 | Static keys | No |
| **Reticulum** | Path announce + transports | Curve25519 + AES-256 | Identity destinations | No |

---

## Trade-offs

### Strengths

- Just works. Two configs, one peering line, you have IPv6.
- No central authority, no enrollment.
- Encrypted by default end to end.
- Single-binary, low resource use.
- Cross-transport: TCP, multicast, Tor, Bluetooth tunnels.

### Limitations

- Not anonymous. Peers see your real IP.
- No incoming-connection authorization at the network layer; every Yggdrasil node can attempt to connect. Use app-layer auth.
- Routing is eventually consistent, so topology churn shows in latency.
- The public peer list is community-maintained; you depend on it for bootstrap.
- No bandwidth-aware routing; heavy traffic can crowd a single peer.

---

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Peer compromise | E2E encryption protects content; rotate peers |
| Tree-root takeover | Anyone can be root; resolved by lowest-pubkey rule |
| Sybil flooding | Limited by per-peer rate limiting |
| Endpoint compromise | Standard endpoint hygiene |
| Misconfigured incoming services | Bind to Yggdrasil interface only; firewall on LAN |
| Quantum adversary (future) | Curve25519/Ed25519 vulnerable; PQ migration needed |

---

## Recent developments (2024-2026)

- Yggdrasil v0.5.x: protocol changes (renamed admin socket, new packet format).
- Mobile clients: Android (well-maintained), iOS via Network Extensions (limited).
- Performance work: better routing convergence on lossy links.
- OpenWrt packages: turnkey for routers.

---

## Related files

- [Overview - Off-Grid Networks](/off-grid-networks)
- [Reticulum](/off-grid-networks/reticulum)
- [FIPS](/off-grid-networks/fips)
- [Meshtastic](/off-grid-networks/meshtastic)
- [MOC - Censorship Resistance](/meta/moc-censorship-resistance)

---

## Primary sources

- Yggdrasil Network — [yggdrasil-network.github.io](https://yggdrasil-network.github.io/)
- Source — [github.com/yggdrasil-network/yggdrasil-go](https://github.com/yggdrasil-network/yggdrasil-go)
- Configuration manual — [yggdrasil-network.github.io/configurationref.html](https://yggdrasil-network.github.io/configurationref.html)
- Public peers — [github.com/yggdrasil-network/public-peers](https://github.com/yggdrasil-network/public-peers)
- cjdns (predecessor / inspiration) — [github.com/cjdelisle/cjdns](https://github.com/cjdelisle/cjdns)

