---
title: "Overlay Naming: Tor .onion and I2P"
slug: onion-and-i2p-naming
type: explainer
pillars: ["naming", "anonymity"]
readiness: battle-tested
description: "Tor .onion and I2P names are public keys, so no registrar can seize them: how overlay naming works, and its usability trade-offs."
dek: "The only naming systems in production where the name is a public key, and where no third party can take the name down."
updated: 2026-10-25
created: 2026-06-22
origin: vault
source: "03-Decentralized-DNS/Overlay Naming - Tor .onion and I2P.md"
aliases: [".onion", "Onion v3", "I2P destinations", ".b32.i2p", "Hidden service naming"]
tags: ["tor", "onion", "i2p", "b32", "naming", "overlay", "hidden-services", "deep-dive"]
---

*The only naming systems in production where the name **is** a public key, and where no third party can take the name down. Tor and I2P are full overlay networks — naming is just one of several layers — but the address format is the most elegant expression of Zooko's triangle in real-world infrastructure: a 56-character string that humans type, that is mathematically the operator's long-term identity key, and that the network uses to rendezvous-route a connection. See [Overview - Decentralized DNS](/kb/decentralized-dns/) for the broader landscape; [GNS](/kb/gnu-name-system/) and [PKARR](/kb/pkarr/) for the cryptographic patterns they share.*

## Why overlay naming matters

A `.com` is a database row a registrar can rewrite. An `.eth` is a smart-contract entry. A Handshake TLD is an auction outcome. **A Tor v3 `.onion` is a curve point**: `base32(pubkey ‖ checksum ‖ version)`. The name proves the key. The key proves the operator. There is nothing for an adversary to seize except the private key.

The structural properties are the same as [PKARR](/kb/pkarr/) (Ed25519) and [GNS](/kb/gnu-name-system/) (per-zone Ed25519 / ECDSA), but Tor and I2P take them further: there is no global DHT and no global namespace, so the name is not only self-authenticating, it is also **globally unique by construction**. The key has 2²⁵² entropy; collisions are impossible. The trade-off is that overlay names are not human-readable and not resolvable outside the overlay — by design.

## Tor v3 onion services

### Address format

A v3 address is:

```
<base32( ed25519_pubkey || checksum || version )>.onion
```

- 32 bytes Ed25519 long-term identity public key.
- A 2-byte checksum: the first two bytes of SHA3-256 over `".onion checksum" || public_key || version`.
- 1-byte version byte (`0x03`).
- Total: 35 bytes → 56 base32 characters.

The address itself is a Tor service ID. To connect, the client performs a Tor rendezvous using this as the rendezvous point. The 56-character length is a deliberate friction: hard to type, hard to mistake for a normal domain, hard to typo-squat.

### Key evolution (v1 → v2 → v3)

| Version | Crypto | Length | Status | Year introduced / retired |
|---------|--------|--------|--------|----------------------------|
| v1 | RSA-1024 | 16 chars | Deprecated in v3 core (2014) | 2003 |
| v2 | RSA-1024, SHA-1 truncated | 16 chars | **Removed in Tor 0.4.6** (2021); 2021-10-15 HSDir began refusing to publish v2 descriptors; on 2021-12-15 the Tor Browser ceased resolving v2 addresses | 2004 |
| v3 | Ed25519 + Curve25519 (NTor) + SHA-3 | 56 chars | **Current standard** | 2017 (rend-spec-v3) |

v2 deprecation is one of the most consequential forced migrations in decentralized naming — six months from announcement to removal, billions of historical v2 addresses rendered dead. The reasons: RSA-1024 was demonstrably weak; v2 descriptor publication was unencrypted to HSDirs (the relays that stored the descriptors), so HSDir operators could learn which onion was online and roughly how popular. v3 encrypts the entire descriptor; HSDir stores only blinded public keys.

### Crypto pieces in v3

A v3 service uses three keys:

| Key | Algorithm | Purpose |
|-----|-----------|---------|
| Long-term identity (`hs_blind_id`) | Ed25519 | The public component of the `.onion` address. Used by clients to verify the descriptor signing key. |
| Service descriptor signing key | Ed25519 (short-term, rotated ~12h to 24h, signed by long-term key) | Signs descriptor entries in the HSDir DHT. |
| Service online key (`NTor onion key`) | Curve25519 | Used for the NTor three-way handshake when the client connects. |

The blinding protocol: `hs_blind_id = blind(hs_blind_pubkey, N)` where `N` is a time-varying parameter published in the consensus. As long as the time parameter `N` stays current (within 12-24 hours), the same service can be found at the same `.onion`. After expiry, clients need a fresh consensus to re-derive the blinded key, and the service uploads a new descriptor. This is what makes HSDir enumeration hard: an HSDir sees a moving target.

### Resolution (rendezvous)

A client looking up `expyuzz4wqqyqhjn.onion`:

1. Derive blinded key for current time period.
2. DHT-lookup of descriptor in the HSDir ring.
3. Verify descriptor signature against the long-term identity key.
4. Get the service's introduction points and NTor onion key.
5. Open a Tor circuit to a random relay (rendezvous point), send an INTRODUCE1 cell to a service introduction point, wait for RENDEZVOUS2, and complete the NTor handshake.

The result is a Tor circuit terminated at the service with no party in the path knowing both who the client is and where the service is. The client knows only the `.onion`; the service knows only the rendezvous-point circuit.

### Why browser UX works

The Tor Browser ships a custom `.onion` resolver that bypasses normal DNS. Firefox, Brave, and Chrome follow via the `.onion` HTTPS upgrade heuristic. Major services (Facebook, BBC, NYT, ProPublica, the New York Times, ProtonMail) have run v3 onion services for years. Facebook's `facebookwkhpilnemxj7asaniu7vnjjbiltxjqhye3mhbshg7kx5tfyd.onion` was the largest production deployment of v3 in history before they decommissioned it in May 2024 — but other news services still use it.

### The cert story solved

Inside Tor, the TLS certificate presented by the service is **unrelated to a CA**. Clients verify that the certificate's public key matches the `.onion` long-term identity. The Tor Browser pins a deterministic 56-char SHA-256 of the pubkey as the cert's SPKI fingerprint. There is no CA, no ICANN, no registrar — and the connection is encrypted by the Tor circuit anyway, so TLS is defense in depth.

### Deployment realities (2026)

- v3 is the only supported form. v2 was excised 2021-12-15.
- A meaningful fraction of public web traffic to media and darknet services runs over v3.
- Major wallets and crypto services (e.g., Bisq, Peach Bitcoin, Robosats, Bisq 2) use v3 onion services for backend connectivity.
- Performance is worse than clearnet: 3-hop circuit, plus rendezvous, plus handshake. v3 connections are slower than v2 in latency but stronger in confidentiality.
- Vanity `.onion` generators (mkp224o) are CPU-bound but feasible — projects like the BBC routinely use 8-12 char vanity prefixes.

### Trade-offs

**Strengths**
- Strongest operator confidentiality in production.
- No global state to censor.
- Self-authenticating; the name proves the key.
- Strong end-to-end encryption built in.
- Multi-layer defense (circuit + TLS + key pinning).

**Limitations**
- 56 characters — UX friction, error-prone.
- Slower than clearnet.
- Hidden services only; not a general DNS.
- Discovery is out-of-band (no search engine).
- Operational complexity — running a Tor relay, then a service, plus key custody.

### Attack surface

| Attack | Mitigation |
|--------|-----------|
| RSA-1024 break (v2 era) | Mitigated by v3 (Ed25519) — historic issue |
| HSDir enumeration | Blinded keys; encrypted descriptors |
| HSDir / guard DoS | Multiple introduction points; guard rotation; load-balancing |
| Rendezvous-point analysis | Padded cells; timing obfuscation; multiple RPs |
| Service private key compromise | Hardware token custody; periodic subkey rotation |
| Onion-phish (homoglyph in 56-char string) | Browser warnings; petname UIs |

## I2P destinations

I2P (Invisible Internet Project) is a separate, more fully distributed overlay with its own naming model.

### Address format

An I2P destination is **not a single 56-char string**. The network identifier is a 516-byte binary blob (a 256-byte public key, 128-byte signing key, and certificate) that is hashed and base32-encoded. The hash is a 52-character base32 of a SHA-256 of the destination's signing key, but the actual data the network uses is the full 516-byte structure. To route a connection, peers exchange the binary structure directly — `.b32.i2p` is a hash for human memory, not a network identifier.

```
<base32( sha256( signing_key ) )>.b32.i2p  →  52 characters
```

The 516-byte destination is what gets published in I2P's NetDB (the network database) and exchanged by peers.

### Crypto pieces

- **Signing key**: Ed25519 (default since I2P 0.9.46, 2021).
- **Encryption key**: X25519 (ElGamal for older destinations).
- **Certificate**: Type byte + signing key + optional encryption key.

### Resolution (floodfill router + NetDB)

I2P's floodfill routers collectively maintain the NetDB — a distributed Kademlia-like DHT of `destination → router contact info`. Lookups for `.b32.i2p` go through the local NetDB; if the entry isn't local, the request floods out to floodfill peers.

- Local NetDB: fast (in-memory).
- Distributed NetDB: tunnel-routed, latency adds up.
- Lease sets: every destination periodically publishes its current router contact info to the NetDB.

### Hosts.txt and naming

I2P ships a generic naming library with a `hosts.txt` base implementation. The `i2pd` C++ router and the Java I2P router both support `hosts.txt` mappings, but the canonical name is the destination hash. Custom naming overlays (`addon.i2p` services like `stats.i2p`, `i2p.rocks`, `stormycloud.i2p`) build human-readable aliases on top of base32.

### Key evolution

| Era | Default key type | Notes |
|-----|------------------|-------|
| Pre-0.9.46 | DSA-SHA1 (1280-bit ElGamal) | Older destinations still on the network |
| 0.9.46 (2021) | Ed25519 + X25519 | Default for new destinations |
| 2026 (post-quantum work) | Ed25519 / X25519 with hybrid PQ proposals | Proposal 169: hybrid X25519 + ML-KEM, hybrid Ed25519 + ML-DSA. Implementation in progress on ratchet and SSU2 transports. |

### Post-quantum roadmap (2025–2026)

I2P Proposal 169 (2023, still in progress) lays out the PQ migration:
- Hybrid X25519 + ML-KEM (Kyber) key exchange for NTCP2, SSU2, and Ratchet.
- Hybrid Ed25519 + ML-DSA (Dilithium) signatures.
- Goal: don't break interoperability with existing Ed25519-only destinations.
- Work is incremental and ongoing; production I2P traffic is still primarily classical crypto in 2026.

### Comparison with Tor

| Dimension | Tor v3 | I2P |
|-----------|--------|-----|
| Address | 56-char base32 Ed25519 | 52-char base32 SHA-256 of Ed25519 + 516-byte destination blob |
| Network model | Centralized directory authorities + DHT for services | Distributed floodfill + DHT for NetDB |
| Service model | Outproxy to clearnet optional; primarily onion services | Eepsites (`.i2p` internal web), `i2p.rocks` exit, full internal services |
| User base | Larger public footprint | Smaller but vibrant; more eepsite content |
| PQ status | Draft proposals, hybrid Tor pluggable transports | Proposal 169, hybrid ratchet/SSU2 in progress |
| Crypto | Ed25519 + Curve25519 + SHA-3 | Ed25519 + X25519, PQ in progress |

### I2P as a naming substrate

For an `eepsite` (`http://example.i2p`), the user-facing name is a domain under `.i2p` registered in a custom naming service (`stats.i2p`, etc.). The lookup eventually produces a 52-char base32 destination, which the router converts to the full 516-byte destination for routing.

This is closer to a GNS-style system than to a global DNS: the `.i2p` TLDs are managed by overlay services, not by a single registry. Lookup privacy is high because the network uses unidirectional tunnels per direction and pads traffic; an observer outside the I2P overlay cannot see queries.

### Trade-offs

**Strengths**
- Self-authenticating; name proves the operator.
- No CA, no global registry, no ICANN involvement.
- Strongly distributed (no directory authority in the Tor sense).
- Internal eepsites — a self-contained dark web.
- Per-destination keys; compromise of one does not break the network.

**Limitations**
- 52-char base32; worse UX than 16-char v2 onion.
- Internal service model only; clearnet exit requires explicit configuration.
- Smaller user base than Tor.
- Post-quantum migration in progress, not landed.
- Discovery is out-of-band.

### Attack surface

| Attack | Mitigation |
|--------|-----------|
| Floodfill takeover | Multiple redundant floodfills; republishing |
| Destination compromise | Hardware custody; rotation if supported |
| Tunnel deanonymization | Padded messages; varied tunnel lengths |
| Eepsite enumeration | Base32 is not enumeratable (2²⁵² space) |
| Naming overlay takeover | Use multiple naming services; verify destination out-of-band |

## How overlay naming composes with the rest of the stack

The deep question for the Ungovernable.tech stack is: when do you put a service behind an onion / eepsite vs. behind a PKARR / ENS / Handshake name?

| Stack | Reach | Confidentiality | Trust model | Best for |
|-------|-------|-----------------|-------------|----------|
| `.onion` v3 | Tor users only | Strongest | Self-authenticating | Sensitive services (wallets, leakdrops, journalism) |
| `.b32.i2p` | I2P users only | Strong | Self-authenticating | Eepsites, internal services, fully distributed apps |
| `.eth` / CCIP-Read | Web2 + Web3 | Low (DNS visible) | Chain + CA | Mainstream apps with crypto identity |
| Handshake TLD | HNS resolvers | Low (chain public) | Chain | Permissionless namespaces |
| PKARR / Pubky | DHT lookups + bridge | Low (DHT visible) | Ed25519 | Self-sovereign data platforms |
| GNS | GNS-aware apps | Strongest queries | Ed25519 + per-zone | Privacy-respecting apps inside GNUnet |

A serious Ungovernable deployment layers them:

```
Edge service
  ├─ v3 .onion   ─► Tor users (max confidentiality)
  ├─ .b32.i2p    ─► I2P users (distributed)
  ├─ .eth        ─► Web3 mainstream (CCIP-Read subdomain for off-chain records)
  ├─ PKARR zone  ─► DHT-direct clients, Pubky social
  └─ legacy .com ─► Web2 fallback
```

This is the practical pattern: the `.onion` is the kill-switch-resistant address; the `.eth` is the everyday address; the PKARR zone is the self-sovereign data plane.

## Recent developments (2024–2026)

- **v2 fully retired** (2021-12-15); v3 is the only supported form.
- Facebook decommissioned its massive v3 deployment in May 2024; the darknet footprint of major mainstream media remains.
- I2P 0.9.46+ (2021) made Ed25519 the default signing key. PQ migration in progress under Proposal 169.
- Bisq 2 (2024), Robosats, Peach Bitcoin, and dozens of crypto projects ship v3 onion services as primary endpoints.
- Vanity `.onion` generators (mkp224o) continue to mature; 8–12 char prefixes are realistic on a small cluster.
- Tor Project explores post-quantum handshake upgrades (Proposal 323, hybrid PQ + classical) — not yet deployed in stable releases.
- **2026**: Tor's stable channel 0.4.8.x carries v3 + post-quantum handshake drafts. I2P ratchet (a replacement for the older ElGamal transport) gains hybrid X25519 + ML-KEM support on a development branch.

## Primary sources

- [Tor specification: encoding v3 onion addresses](https://spec.torproject.org/rend-spec/encoding-onion-addresses.html)

- Tor Rendezvous Specification v3 — `spec.torproject.org/rend-spec-v3.html`.
- Tor Onion Services v3 — `spec.torproject.org/v3 onion services`.
- Tor Project blog: v3 onion services — `blog.torproject.org/v3-onion-services-usage/`.
- I2P naming overview — `i2p.net/en/docs/overview/naming`.
- I2P Proposal 169 — Post-Quantum Crypto Protocols — `i2p.net/en/proposals/169-pq-crypto`.
- I2P Development Roadmap — `i2p.net/en/get-involved/roadmap`.
- mK224o vanity onion generator — `github.com/cathugger/mkp224o`.
- Zooko Wilcox-O'Hearn, *Names: Distributed, Secure, Human-Readable: Choose Two*, 2001 (Zooko's triangle).
