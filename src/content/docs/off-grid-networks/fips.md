---
title: "FIPS"
tags:
  - "fips"
  - "mesh"
  - "nostr"
  - "routing"
  - "off-grid"
  - "deep-dive"
---
*A Rust mesh routing protocol that uses Nostr keypairs as native node identities. Multi-transport (UDP / TCP / Ethernet / Tor / BLE), Noise-encrypted hop-to-hop and end-to-end, with an IPv6 TUN adapter that lets unmodified TCP/IP applications speak across the mesh.*

---

## Why FIPS is interesting

FIPS bridges two things the vault already covers separately: mesh routing (Reticulum, Yggdrasil, Meshtastic) and Nostr identity ([Nostr](/identity/nostr), [Pubky](/identity/pubky)). Instead of a new address space, FIPS uses Nostr `npub`s as node identities. The same keypair signs your social posts and routes packets to your laptop. This collapses identity layers across the stack.

It is also a fairly bold engineering bet: spanning-tree plus bloom-filter routing in Rust, transports including BLE L2CAP, and IPv6 adaptation so legacy software just works.

---

## Identity model

Every FIPS node has a Nostr secp256k1 / Schnorr keypair. The `npub` (bech32-encoded x-only public key) is the node's address. Two consequences:

1. The same keypair you'd use for Nostr social or messaging works as a network address.
2. There is no enrollment, no registry, no DNS. Generate a key and you have a routable identity.

Within FIPS the npub is mapped deterministically to a 128-bit IPv6 address in the `fd00::/8` range so legacy IP applications can address it like any other host. A TUN adapter on the host converts between the two.

---

## Routing

FIPS does not flood. It builds a *spanning tree* across the mesh, with greedy coordinate routing on top, similar in spirit to Yggdrasil but with bloom-filter-guided discovery for finding nodes outside the tree.

- Spanning tree: every node has tree coordinates after convergence; routing follows tree-distance.
- Bloom filter discovery: nodes advertise compact summaries of which neighborhoods they know about; queries probe single-path with retry rather than flooding.
- No global routing tables. Local state only.

Convergence is fast on small and medium meshes. On hundreds of nodes the discovery overhead grows but stays below flooding levels.

---

## Transports

FIPS runs over heterogeneous links; the routing layer is indifferent.

| Transport | Use case |
|-----------|----------|
| **UDP** | Standard internet overlay |
| **TCP** | Strict NAT environments where UDP is blocked |
| **Ethernet (raw)** | LAN-scale mesh, no IP needed |
| **Tor** | Anonymized backbone |
| **BLE L2CAP** | Phone-to-phone short-range, no infrastructure |

Per-link MTU is negotiated; the protocol fragments above and reassembles below. The roadmap targets serial and radio (LoRa-style) transports.

This makes FIPS a fit for hybrid deployments: a city-scale BLE mesh on phones bridged to a continent-scale Tor backbone, with Ethernet links connecting machines in a single room, all in one address space.

---

## Encryption

Two cryptographic layers:

1. Hop-to-hop: Noise IK between adjacent nodes. Authenticated, encrypted, replay-resistant. Periodic rekey.
2. End-to-end: Noise XK between FIPS endpoints, independent of any intermediate node. Periodic rekey for forward secrecy.

The combination resembles Tor's onion routing for confidentiality, but without the anonymity goal: the *content* is end-to-end encrypted, but the *path* is observable to participating nodes.

---

## IPv6 adaptation

The TUN adapter does three useful things:

- Maps `npub` → IPv6 (`fd00::/8`). Pings, SSH, HTTP, anything that takes an IPv6 address can address a FIPS node.
- Resolves `.fips` DNS. A built-in stub resolver answers `.fips` lookups against the mesh.
- Static hostname mapping. `/etc/fips/hosts` maps human-readable names to mesh addresses, auto-reloading.

The effect is that legacy TCP/IP software just works. SSH to a friend's `npub`-derived hostname; serve HTTP on a node; mount NFS over the mesh. None of those apps need to know FIPS exists.

---

## Native FIPS-aware apps

Applications that opt in can address each other directly with `npub:port` semantics, avoiding the IPv6 translation layer. This is more efficient and exposes the cryptographic identity directly to the application, which is useful for end-to-end signing, attestation, and protocol-aware features.

The first canonical use case in the FIPS examples: a Nostr relay (strfry) reachable only over the FIPS mesh, sharing a sidecar's network namespace.

---

## Composition

FIPS plays well with the rest of the vault's primitives:

- Nostr social and Nostr-as-network. One keypair across both planes.
- Tor as a transport. Run FIPS over Tor; Tor anonymizes the underlying IP, FIPS gives mesh routing semantics on top.
- Reticulum interop. Both use cryptographic identities; gateways bridging FIPS and Reticulum are plausible.
- Mix networks layered above. FIPS is not anonymous on its own; combine with Nym or Katzenpost for metadata privacy.
- Confidential AI inference. A FIPS-only LLM endpoint pinned to a Nostr identity, behind attested TLS, reachable across heterogeneous transports.

---

## Trade-offs

### Strengths

- Nostr-native identity. Single keypair across the social and network layers.
- Multi-transport without rework. The same node speaks UDP, BLE, and Tor; the protocol picks the best.
- Encrypted by default, hop-to-hop and end-to-end.
- Legacy-compatible via IPv6 TUN. TCP/IP apps just work.
- Rust implementation, memory-safe and modern.

### Limitations

- Early-stage (v0.2.0 in 2026). Wire format still changing; no published crate; APIs not stable.
- Smaller community than Yggdrasil or Reticulum. Fewer nodes, fewer integrations.
- Not anonymous. Like Yggdrasil, not a Tor replacement.
- No security audit yet (in roadmap).
- No published mobile binaries yet.

---

## Comparison

| System | Identity | Routing | Encryption | Anonymity | Status |
|--------|----------|---------|------------|-----------|--------|
| **FIPS** | Nostr secp256k1 = npub | Spanning tree + bloom | Noise IK + XK | No | v0.2.0, active |
| **Yggdrasil** | Ed25519 = IPv6 | Greedy on spanning tree | Noise + ChaCha20 | No | Stable |
| **Reticulum** | Curve25519 destinations | Path announce + transports | AES-256 + Curve25519 | No | Stable |
| **cjdns** | Curve25519 = IPv6 | DHT + path-vector | Curve25519 | No | Maintained |
| **Tor** | TLS to relays | Three-hop circuits | Layered AES | Yes | Stable |
| **Meshtastic** | Hardware ID + key | Managed flood | AES-256-CTR per channel | No | Stable |

---

## Use cases

### Single-keypair operator

Generate one Nostr keypair. Use it to:

- Post on Nostr.
- Sign Lightning zaps.
- Address a FIPS node, your laptop, accessible from your phone over Tor or BLE.
- Bind a confidential AI endpoint to it via attested TLS.

The cognitive overhead of N identities collapses to one.

### Hybrid hostile-environment mesh

```
[FIPS over BLE] — phones in a building
   ↕
[FIPS over Ethernet] — wired router fleet
   ↕
[FIPS over Tor] — to a remote office or cloud node
```

Same address space, same encryption, same identity. When one transport fails, the others carry traffic.

### Sidecar deployment

K8s sidecar pattern: FIPS runs alongside an existing service, presenting `fips0` in the pod's network namespace. Other containers in the pod get mesh access transparently.

---

## Recent developments (2026)

- v0.2.0: Tor and BLE L2CAP transports, ECN congestion signaling, improved discovery, IPv6 TUN with multi-backend DNS auto-config.
- Roadmap: Nostr-relay-based bootstrap (no static peer lists), native API for FIPS-aware apps, security audit.
- Linux, macOS, and Windows packaging in place.

---

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Active path interception | Hop-to-hop Noise IK + end-to-end Noise XK |
| Sybil node flooding | Bloom-filter discovery limits scope; reputation TBD |
| Key compromise | Per-session forward secrecy via rekey |
| Route hijack | Cryptographically-signed routing announcements |
| Quantum (future) | Curve25519/Schnorr; PQ migration not yet specified |
| Endpoint compromise | Standard hygiene; not different from any mesh |

---

## Related files

- [Overview - Off-Grid Networks](/off-grid-networks)
- [Yggdrasil](/off-grid-networks/yggdrasil)
- [Reticulum](/off-grid-networks/reticulum)
- [Meshtastic](/off-grid-networks/meshtastic)
- [Nostr](/identity/nostr) — same keypair, social plane
- [Pubky](/identity/pubky) — adjacent project, same identity philosophy
- [MOC - Composing Primitives](/meta/moc-composing-primitives)

---

## Primary sources

- FIPS — [github.com/jmcorgan/fips](https://github.com/jmcorgan/fips)
- Protocol design — `docs/design/` in the FIPS repository.
- *fips-intro.md* — top-level overview.
- Noise Protocol Framework — [noiseprotocol.org](https://noiseprotocol.org/).
- Nostr Protocol — [github.com/nostr-protocol/nostr](https://github.com/nostr-protocol/nostr).

