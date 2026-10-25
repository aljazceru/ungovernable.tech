---
title: "B.A.T.M.A.N. advanced and cjdns"
slug: batman-adv-and-cjdns
type: deep-dive
pillars: ["mesh"]
readiness: usable
description: "Two long-running approaches to mesh routing compared: B.A.T.M.A.N. advanced for local Layer 2 meshes and cjdns for encrypted IPv6 overlay networks."
dek: "Two long-running mesh routing approaches from very different traditions: BATMAN-adv, a Linux-kernel Layer-2 mesh from the Freifunk community-wifi movement, and cjdns, a self-encrypting Layer-3 mesh whose IPv6 address is derived from a public key. Same problem (route packets across an arbitrary mesh of peers) at different layers with different threat models."
updated: 2026-04-26
created: 2026-04-26
origin: vault
source: "05-Off-Grid-Networks/BATMAN-adv and cjdns.md"
aliases: ["BATMAN-adv", "cjdns", "Hyperboria", "Freifunk"]
tags: ["batman-adv", "cjdns", "mesh", "freifunk", "hyperboria", "layer-2", "ipv6", "deep-dive"]
---

## What they share

Both grew out of the late-2000s push to build community-owned wireless networks independent of telco infrastructure. Both predate Yggdrasil, Reticulum, and the modern wave of cryptographic overlays. Both still ship.

The shared properties:

- Self-organizing — nodes discover each other and form routes without a central controller.
- Open source, multi-decade codebases.
- Designed for community wifi as the canonical use case.
- Survive partial connectivity (some links up, some down, mesh reorganizes).

What they don't share is layer, threat model, or addressing.

## BATMAN-adv

### Origins and place in the stack

B.A.T.M.A.N. (Better Approach To Mobile Ad-hoc Networking) came out of the Freifunk community in Berlin in the mid-2000s as an answer to OLSR's complexity. The original B.A.T.M.A.N. is a Layer-3 daemon (`batmand`); the more interesting variant for community networks turned out to be **B.A.T.M.A.N. Advanced** (BATMAN-adv), a Linux kernel module operating at Layer 2.

BATMAN-adv builds an Ethernet mesh: every participating node looks, to local applications, like it is on the same broadcast domain. Bridges, DHCP, ARP, and ordinary Layer-3 protocols just work. The mesh is invisible to higher layers.

That property — Layer 2 transparency — is why community wireless networks like Freifunk standardized on BATMAN-adv. A Freifunk router presents itself as an ordinary access point; clients get an IP from a community DHCP server; traffic is routed across the mesh without per-client awareness.

### Routing: OGM

The protocol primitive is the **OGM** (Originator Message). Every node periodically broadcasts a small OGM. Neighbors rebroadcast OGMs they hear, with TQ (Transmit Quality) values updated to reflect link quality. After a few rounds, every node has a table mapping originator MAC → best-quality next-hop neighbor.

There is no global topology view. Each node has only its own routing table; loops are prevented by sequence numbers, link quality is the metric. The protocol is lightweight enough to run on $30 OpenWrt routers with 32 MB of RAM.

### Encryption story

BATMAN-adv has none. It is a routing protocol, not a security protocol. Encrypted traffic on a BATMAN-adv mesh comes from higher layers: WireGuard tunnels, HTTPS, or the per-link WPA on the underlying wifi.

This is intentional. Freifunk's threat model treats the mesh as a public commons; users running confidential traffic are expected to encrypt end-to-end themselves. The mesh's job is to deliver bytes.

### Adoption

Freifunk operates BATMAN-adv meshes in dozens of German cities and many other parts of Europe. The Berlin mesh has had thousands of nodes; smaller cities run hundreds. Other adopters: Athens Wireless Metropolitan Network (AWMN), Funkfeuer (Vienna), guifi.net (Catalonia, partly).

OpenWrt ships BATMAN-adv as a standard package; the [github.com/open-mesh-mirror/batman-adv](https://github.com/open-mesh-mirror/batman-adv) tree is actively maintained and tracks the upstream Linux kernel.

## cjdns

### Origins and design intent

cjdns ("Caleb James DeLisle's Network Suite", later just "cjdns") emerged around 2011 as a more ambitious answer: build a mesh where the address space *is* a cryptographic identity space, and forwarding is permissioned by the destination's public key.

The result is the **Hyperboria** network — the largest cjdns deployment, peaking at a few thousand nodes in the mid-2010s, smaller now but still alive in 2025-2026.

### Address = public key

Every cjdns node generates a Curve25519 keypair. The IPv6 address is derived directly from the public key's hash:

```
fc00::/8        ← reserved IPv6 ULA range that cjdns claims
fcXX:XXXX:...   ← truncated SHA-512 of the public key, prefix-tagged
```

Two consequences:

- An IPv6 address inherently authenticates: knowing someone's address means you can encrypt to them.
- There is no DHCP, no allocation, no registry. Generate a key, you have an address.

This is the same self-certifying design as Yggdrasil, Tor v3, Nostr npubs, and Reticulum destinations.

### Encryption everywhere

Every hop is encrypted. cjdns doesn't have a "plaintext mode." A packet from Alice to Bob:

1. Alice encrypts the payload to Bob's public key (end-to-end).
2. Each hop also runs an authenticated Curve25519/Poly1305 channel with its neighbor (link layer).

So both link-level and end-to-end are encrypted. The on-wire bytes between two cjdns peers are unintelligible to a passive observer.

### Routing: source routing on a switching tree

cjdns calls its routing layer "switching" rather than routing. The network is organized as a tree-ish structure with a numbered switching path; a sender prepends a source route and each switch peels off one hop's worth of label.

Path discovery uses a Kademlia-style DHT keyed on the address space, so nodes find paths to any address by querying the DHT for closer-and-closer neighbors. This is how cjdns claims to scale: routing tables are small, the DHT does the heavy lifting.

In practice, the DHT has been the network's stress point: at scale, churn and partitions cause path-discovery latency, and Hyperboria has had operational pain in keeping it healthy.

### Status

cjdns the project is alive but quieter than during its 2013-2017 peak. The repo at [github.com/cjdelisle/cjdns](https://github.com/cjdelisle/cjdns) sees periodic commits. Hyperboria remains reachable; new participants peer with willing existing nodes, often via the [Hyperboria intro page](https://hyperboria.net) and the `#cjdns` IRC channel. Headcount in 2025 is in the hundreds rather than thousands.

Yggdrasil ([Yggdrasil](/kb/yggdrasil/)) was started in 2018 by former cjdns contributors who wanted to fix what they saw as cjdns's architectural mistakes (DHT brittleness, source routing). For a "modern cjdns," look there.

## Side-by-side

| Aspect | BATMAN-adv | cjdns |
|--------|------------|-------|
| OSI layer | 2 (Ethernet) | 3 (IPv6 overlay) |
| Address space | MAC, application-assigned IP | `fc00::/8` derived from pubkey |
| Encryption | None at protocol layer | Curve25519 link + payload, mandatory |
| Routing | OGM flooding + TQ metric | Switching tree + Kademlia DHT |
| Implementation | Linux kernel module | Userspace daemon |
| Typical hardware | OpenWrt routers, OLSR-class | Any Linux/macOS/FreeBSD host |
| Trust model | "Mesh is a public commons" | "Address is a key" |
| Canonical network | Freifunk (community wifi) | Hyperboria |
| Active in 2026 | Yes, healthy | Yes, niche |

## When you want which

- **Local community wifi, pole-mounted radios, transparent bridging:** BATMAN-adv. The L2 transparency means existing applications (DHCP, mDNS, captive portals, Plex) work unchanged.

- **Cryptographically authenticated identities across the public internet:** cjdns or, more typically in 2026, Yggdrasil. Address-as-key is the right primitive.

- **Adversarial conditions where mesh is everything:** neither. Use [Reticulum](/kb/reticulum/) over LoRa, [Briar](/kb/briar/) over Bluetooth and Tor, or [Bitchat](/kb/bitchat/) over BLE. Both BATMAN-adv and cjdns assume reliable IP transport between neighbors.

- **You want to peer your machine into a multi-thousand-node already-existing IPv6 community network:** Yggdrasil first; cjdns / Hyperboria for historical reasons or specific peering.

## Trust and threat model

### BATMAN-adv

- Anyone on the broadcast domain sees broadcast traffic.
- A malicious node can advertise high-quality OGMs to attract traffic (sybil-style sinkholes).
- No authentication on OGMs. Defense is by encryption above the mesh and by community-managed peering policies.
- Direction-finding the underlying wifi radios is straightforward.

### cjdns

- Passive on-path observers see encrypted bytes; they can do traffic analysis (timing, size, who-talks-to-whom by `fc00::` address).
- Active attackers cannot inject content that decrypts at the destination (Curve25519 + Poly1305 authentication).
- The DHT is a known stress point; routing-layer DoS via DHT poisoning is plausible.
- Endpoint security is on you: a compromised cjdns node leaks its private key.
- Quantum: Curve25519 throughout. No post-quantum migration in either project.

## Operational notes

### BATMAN-adv

- Tune `orig_interval` and `hop_penalty` to your link characteristics.
- Use multicast snooping and gateway selection to prevent broadcast storms in larger meshes.
- Underlying wifi: ad-hoc (IBSS) mode is the historical setup; 802.11s and "managed mode + 4addr" are alternatives.
- Mesh sizes: comfortable to ~200 nodes; community deployments push to ~1,000 with careful tuning.

### cjdns

- Peering is manual: edit `cjdroute.conf`, paste a peer's public key + UDP/IP info.
- Run as a daemon; expose `tun0` to applications. Ordinary IPv6 sockets to `fc00::` addresses just work.
- Combine with Yggdrasil or Tor for additional path diversity.
- Bandwidth overhead from per-hop encryption is real but manageable on modern hardware.

## Primary sources

- BATMAN-adv documentation — [open-mesh.org/projects/batman-adv/wiki](https://www.open-mesh.org/projects/batman-adv/wiki).
- BATMAN-adv source — [git.open-mesh.org/batman-adv.git](https://git.open-mesh.org/batman-adv.git).
- Freifunk — [freifunk.net](https://freifunk.net).
- cjdns source — [github.com/cjdelisle/cjdns](https://github.com/cjdelisle/cjdns).
- cjdns whitepaper — [docs/Whitepaper.md](https://github.com/cjdelisle/cjdns/blob/master/doc/Whitepaper.md).
- Hyperboria — [hyperboria.net](https://hyperboria.net).
- Neumann, Aichele, Lindner, Wunderlich, "Better Approach To Mobile Ad-hoc Networking" (IETF Internet-Draft, 2008).

Continue with [LibreMesh](/kb/libremesh/) and [Build a community Wi-Fi network](/guides/community-wifi-network/).
