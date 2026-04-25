---
title: "Off-Grid Networks"
tags:
  - "off-grid"
  - "mesh-network"
  - "meshnet"
  - "lora"
  - "dtn"
  - "reticulumm"
  - "meshtastic"
  - "yggdrasil"
sidebar: {"label":"Overview","order":0}
---
## What this covers

Off-grid networks are communication systems that work without depending on the public internet. They are useful when:

- The internet is censored or shut down.
- Infrastructure is destroyed by disaster or war.
- Operational security requires no internet path.
- The goal is to reduce a digital footprint.

The main building blocks are mesh networking (devices talking directly to one another), LoRa radio (long-range and low-power), delay-tolerant protocols (for intermittent links), and overlay networks (encrypted tunnels that ride on whatever transport is available).

---

## Background

### Early mesh networks (1980s-2000s)

Mesh networking research started in military and academic settings:

- DARPA Packet Radio Research (1970s-80s) — predecessors of modern mesh.
- IEEE 802.11s (2007) — Wi-Fi mesh standard.
- Serval Project (2012) — phone-to-phone mesh over Wi-Fi.

### Recent activity (2019-present)

- Yggdrasil (2018) — modern IPv6 overlay network.
- Meshtastic (2019) — open-source LoRa mesh, broad adoption.
- Reticulum (2018+, RNS 0.x branches matured 2021-2024) — Markqvist's encrypted-by-default mesh stack.
- Bitchat (2024) — phone-only BLE mesh with a Nostr fallback.
- FIPS (2024+) — Nostr-keyed mesh routing protocol.

### What drove this

1. Internet shutdowns used as a political tool.
2. The wish to avoid internet dependency for privacy reasons.
3. Disaster resilience: hurricanes, earthquakes, war.
4. Building alternatives to corporate infrastructure.

---

## Categories

### 1. LoRa mesh networks

LoRa (Long Range) is a proprietary chirp-spread-spectrum modulation. Typical figures:

- Range: 2-10 km in rural areas, longer with line of sight.
- Power: very low, batteries last years.
- Bandwidth: very low (~300 bps to 19 kbps).
- Frequencies: ISM bands (433 MHz, 868 MHz EU, 915 MHz US).

#### Meshtastic

The most widely used LoRa mesh platform:

- Hardware: cheap ESP32-based radios ($20-50).
- Software: open-source firmware.
- Range: up to 10 km with stock antennas.
- Features: GPS, encrypted messaging, sensor integration.
- Ecosystem: multiple clients, maps, tracking dashboards.

[Ripple](https://github.com/ripple-lib/ripple) — experimental LoRa mesh.
[cubeos-app/meshsat](https://github.com/cubeos-app/meshsat) — Meshtastic-Iridium bridge.

### 2. Reticulum stack

A full networking stack for secure mesh communication:

- Auto-discovery: nodes find each other on their own.
- Encryption: all traffic encrypted with Wireguard-style keys.
- Addressing: distributed addressing without DNS.
- Protocols: includes LXMF (messaging) and NomadNet (client).

[NomadNet](https://github.com/markqvist/NomadNet) — encrypted chat over Reticulum.
[Sideband](https://github.com/markqvist/Sideband) — mobile LXMF client.

### 3. Overlay networks

These run over the existing internet but provide direct P2P connectivity.

#### Yggdrasil

- Architecture: end-to-end encrypted overlay with Wireguard-style crypto.
- Routing: greedy routing on a spanning tree.
- Clients: native on many platforms.
- Performance: slower than the native internet but fully encrypted.

#### cjdns

- Legacy: the original encrypted IPv6 mesh protocol.
- Status: less actively maintained.
- Network: Hyperboria, the largest cjdns network.

### 4. Delay-tolerant networks (DTN)

When connectivity is intermittent, DTN protocols store and forward.

#### Briar

- Transport: Bluetooth, Wi-Fi, Tor.
- Protocol: store-and-forward messaging.
- Use case: secure messaging when internet is unavailable.
- Platforms: Android (primary); desktop via Tor; iOS unsupported.

#### Secure Scuttlebutt (SSB)

- Protocol: append-only log with gossip replication.
- Platform: Manyverse (Android), Patchwork (desktop).
- Use case: social networking without servers.

---

## Comparison

| Network | Type | Range | Internet required | Encryption | Active development |
|---------|------|-------|--------------------|------------|--------------------|
| **Meshtastic** | LoRa | 2-10 km | No | Yes | Very active |
| **Reticulum** | WiFi/LoRa/BT | Varies | Optional | Yes | Active |
| **Yggdrasil** | Overlay | N/A | Yes | Yes | Active |
| **cjdns** | Overlay | N/A | Optional | Yes | Moderate |
| **Briar** | BT/WiFi | 10-100m | No | Yes | Active |
| **SSB** | P2P | N/A | Optional | No | Moderate |

---

## Implementations

### Mesh hardware

| Device | Price | Features |
|--------|-------|----------|
| **Heltec LoRa** | $20-30 | ESP32, OLED, GPS |
| **TTGO LoRa** | $25-40 | ESP32, battery holder |
| **RAK WisBlock** | $50+ | Modular, professional |
| **RAK WisMesh Pocket** | $80 | Pre-built handheld |
| **SpecFive Spectre** | $150 | Android phone + LoRa |

### Software ecosystem

- [Meshtastic](https://meshtastic.org/) — firmware and apps.
- [Reticulum](https://reticulum.network/) — full stack.
- [Yggdrasil](https://yggdrasil-network.github.io/) — overlay.
- [awesome-meshtastic](https://github.com/ajmcquilkin/awesome-meshtastic) — resources.

---

## Use cases

### 1. Disaster communication

When cell towers and internet are down, mesh networks provide local communication:

- Hurricane response teams use Meshtastic.
- Wartime communication in Ukraine.
- Wildfire evacuation coordination.

### 2. Privacy and operational security

- No internet path means no metadata leakage.
- Air-gapped networks for sensitive operations.
- A way around surveillance infrastructure.

### 3. Rural connectivity

In areas with no internet infrastructure:

- Remote villages in developing countries.
- Scientific expeditions.
- Maritime communications.

### 4. Protest and resistance

- Hong Kong protests used mesh networks.
- Iran internet shutdown workarounds.
- Emergency communication infrastructure.

---

## Evidence at a glance

| Technology | Maturity | Evidence |
|------------|----------|----------|
| Meshtastic | Production | Thousands of users, active dev |
| Reticulum | Production | Working software, growing |
| Yggdrasil | Production | Stable releases |
| Briar | Production | Used in conflict zones |
| SSB | Beta | Active community |

---

## Trade-offs

### Strengths

- Independence: no internet required.
- Censorship resistance: hard to block what isn't seen.
- Low power: can run on batteries or solar.
- Lower cost: no ISP, no cellular plan.

### Limitations

- Range is bounded; mesh needs nodes in proximity.
- Bandwidth is low; LoRa is very slow.
- More users mean a better network.
- Hardware and setup add complexity.
- Discovery is hard.

### Operational notes

- More nodes mean more range (the mesh effect).
- Antenna choice matters a lot.
- Line of sight increases range substantially.
- Battery life depends on usage patterns.

---

## Attack surface

### Physical layer

- RF jamming (counter: frequency hopping, spread spectrum).
- Direction finding (counter: low-power transmissions, movement).
- RF interference.

### Network layer

- Sybil attacks (counter: node reputation).
- Eclipse attacks (counter: diverse peer selection).
- Routing attacks.

### Social layer

- Bad hardware (counter: verify sources).
- Compromised firmware (counter: reproducible builds).
- User error (counter: training).

---

## Related files

- [Overview - Encrypted Messaging](/encrypted-messaging) — Briar, SimpleX, and offline-first protocols.
- [Off-Grid Messaging](/encrypted-messaging/off-grid-messaging) — practical patterns over LoRa, Reticulum, Briar, HF.
- [Overview - Mix Networks](/mix-networks) — anonymity overlays applicable to mesh.
- [Overview - Decentralized Identity](/identity/overview-decentralized-identity) — pseudonymous IDs in disconnected networks.

