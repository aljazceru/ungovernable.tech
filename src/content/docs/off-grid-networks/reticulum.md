---
title: "Reticulum"
tags:
  - "reticulum"
  - "rns"
  - "lxmf"
  - "mesh"
  - "off-grid"
  - "encryption"
  - "deep-dive"
---
*A general-purpose, transport-agnostic, encrypted-by-default mesh networking stack. The link layer is treated as a commodity; identity, routing, and end-to-end secure transports are layered on top, running over LoRa, packet radio, TCP, serial, or anything else that delivers bytes.*

---

## Position in the stack

Reticulum (RNS, the Reticulum Network Stack) is not a chat app. It is the substrate. Compared with Meshtastic:

| Aspect | Meshtastic | Reticulum |
|--------|-----------|-----------|
| Scope | Mostly LoRa | Any transport |
| Encryption | Per-channel symmetric (default) | Per-destination Curve25519 + AES-256, by design |
| Identity | Node ID + key | Cryptographic destinations (named keys) |
| Routing | Managed flood | Path discovery + announce + transport |
| Apps | Built-in messenger | Pluggable: LXMF, NomadNet, Sideband, MeshChat |

If Meshtastic is a CB radio with a screen, Reticulum is a TCP/IP analogue tuned for adversarial conditions.

---

## Identity model

Every endpoint is a *destination*: a named cryptographic identity.

```
RNS.Identity     ─ a Curve25519 keypair + an X25519 keypair + a name
RNS.Destination  ─ Identity + app namespace + aspect path
```

Destinations are addressed by 16-byte truncated SHA-256 hashes. Two destinations with the same Identity but different aspects (`alice.messenger`, `alice.files`) can be addressed independently while sharing a key.

This is the same general pattern as Tor v3 hidden services or Nostr npubs: the address is the key.

---

## Cryptography

- Forward secrecy via per-link X25519 ECDH and ratcheted symmetric keys.
- AES-256 for bulk encryption.
- Ed25519 / Curve25519 for identity and signatures.
- Token-based authentication: a destination can require knowledge of a pre-shared secret without revealing it.

Encryption is not optional. There is no "plain Reticulum" mode. Every link establishes a key during path setup; bulk traffic uses derived per-link keys.

---

## Routing

### Path announce

When a destination wants to be reachable, it broadcasts an *announce* packet that propagates outward through the mesh. Intermediate transports cache the path. When a sender wants to reach that destination, it queries the cached path table.

### Discovery

Discovery is on-demand. Paths are not flooded continuously. A destination that hasn't announced recently isn't reachable; this trades cold-contact latency for bandwidth efficiency.

### Multi-link and bundling

A single Reticulum mesh can mix transports: a node connected to one neighbor over LoRa, another over TCP, and a third over serial all share the same address space. Packets cross transport boundaries transparently, including through intermediate gateway nodes (rnsd).

### Resource transfer

For files larger than a single packet, Reticulum has a *Resource* primitive: chunked, with sequence and integrity, resumable. Used by NomadNet for file sharing and by LXMF for attachments.

---

## LXMF — Lightweight Extensible Message Format

LXMF is a messaging-format-as-a-protocol layered on RNS:

- Identity = address, like email but without the @ host.
- Store-and-forward: propagating nodes act as mailboxes; the recipient pulls when reachable.
- End-to-end encrypted by the RNS layer.
- Time-stamped, signed message format.

It is what makes Reticulum usable as messaging without a central server. LXMF runs equally well over LoRa-only meshes, an internet TCP backbone, or hybrid setups.

---

## Applications

| App | Type | Notes |
|-----|------|-------|
| **NomadNet** | Terminal UI | Browser for "pages" served over RNS, like an offline-first BBS |
| **Sideband** | Cross-platform messenger | LXMF-based; iOS, Android, desktop |
| **MeshChat** | Web UI messenger | Easier UX for non-technical users |
| **rnsd** | Daemon | Headless transport node, runs the mesh |
| **rnstatus / rncheck** | CLI | Diagnostic tools |

---

## Hardware profiles

Because RNS is transport-agnostic, hardware choices are flexible:

- LoRa via RNode: Markqvist's hardware with explicit RNS firmware. ~20-50 km range; ~1 kbit/s.
- HF via packet modem: RNS over AX.25. Continental range; very slow.
- Serial / KISS: wired connections, debugging, mesh seeding.
- TCP / I2P: internet overlay; combine with `.i2p` for anonymity.
- Bluetooth Classic: short-range smartphone link.

The same node can speak multiple transports at once and bridge them.

---

## Trust and threat model

### What RNS does

- E2E encrypts all destination-to-destination traffic.
- Authenticates announcements via signing.
- Allows resource isolation: a public destination, a friends-only destination, a confidential destination, each with distinct keys.

### What RNS doesn't do

- Does not hide source/destination addresses from on-path observers (bytes pass through transports).
- Does not provide cover traffic; it is observable that a destination is active.
- Cannot defeat physical direction-finding of LoRa radios.

For metadata privacy, layer with mixnets ([Overview - Mix Networks](/mix-networks)) or operate in adversarial mode (low duty cycle, mobile, mission-key only).

---

## Trade-offs

### Strengths

- Transport-agnostic. One stack, many radios.
- Encrypted by default. No "plaintext mode" footgun.
- Cryptographic identity. Address = key.
- Composable. Apps share the identity layer.
- Permissionless. No registry, no server, no fees.

### Limitations

- Smaller user base than Meshtastic. Fewer ecosystems, fewer integrations.
- Path discovery latency. First contact has a setup cost.
- No formal post-quantum migration yet. Curve25519 throughout.
- NomadNet aesthetics. Terminal-first; a barrier for non-technical users.
- Documentation is dense. Markqvist's manual is the primary reference; community tutorials are sparse.

---

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Active path interception | E2E crypto; verifying announces |
| Replay | Per-link nonces |
| DoS by announce flooding | Rate limiting in announce table |
| Endpoint key compromise | Identity rotation; multi-aspect destinations |
| Transport-layer DF | Layer with low-duty-cycle operations |
| Compromised gateway node | E2E means it sees only routing metadata |

---

## Practical setups

### Single-radio LoRa mesh

```
[Phone (Sideband)] ── BLE ── [RNode] ── LoRa ── [RNode] ── BLE ── [Phone]
```

Encrypted hop-to-hop, encrypted end-to-end. Range depends on RNode antenna and terrain.

### Internet-bridged adversarial-friendly mesh

```
[Phone] ── BLE ── [RNode] ── LoRa ── [Pi running rnsd + Tor] ── Tor ── [Pi running rnsd] ── ... ── recipient
```

LoRa for last-mile in a difficult region; Tor for backbone where internet works. The endpoints don't change app.

### Off-grid BBS

NomadNet pages served from a rnsd-equipped node. Forum-style content delivered over a LoRa mesh, persistent across power cycles.

---

## Recent developments (2024-2026)

- Sideband 2.x: major UX improvements; iOS native.
- MeshChat: friendlier web UX, raising the floor for new users.
- rnsd packaging improvements for OpenWrt and embedded.
- Performance: LoRa throughput optimizations under specific channel models.
- Increasing Reticulum-over-TCP-over-Tor deployments.

---

## Related files

- [Overview - Off-Grid Networks](/off-grid-networks)
- [Meshtastic](/off-grid-networks/meshtastic)
- [FIPS](/off-grid-networks/fips)
- [Yggdrasil](/off-grid-networks/yggdrasil)
- [Briar](/off-grid-networks/briar)
- [Off-Grid Messaging](/encrypted-messaging/off-grid-messaging)
- [MOC - Censorship Resistance](/meta/moc-censorship-resistance)

---

## Primary sources

- Markqvist, *Reticulum Network Stack Specification*. [reticulum.network/manual](https://reticulum.network/manual)
- RNS source — [github.com/markqvist/Reticulum](https://github.com/markqvist/Reticulum)
- LXMF — [github.com/markqvist/LXMF](https://github.com/markqvist/LXMF)
- NomadNet — [github.com/markqvist/NomadNet](https://github.com/markqvist/NomadNet)
- Sideband — [github.com/markqvist/Sideband](https://github.com/markqvist/Sideband)

