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
## Overview

**Off-Grid Networks** are communication systems designed to operate independently of the traditional internet. They enable connectivity when:
- The internet is censored or shut down
- Infrastructure is destroyed (disaster, war)
- You need true operational security without any internet dependency
- You want to reduce your digital footprint

The key technologies include **mesh networking** (device-to-device direct communication), **LoRa radio** (long-range, low-power), **delay-tolerant protocols** (for intermittent connectivity), and **overlay networks** (encrypted tunnels over existing infrastructure).

---

## Historical Context

### Early Mesh Networks (1980s-2000s)

Mesh networking research began in military and academic contexts:
- **DARPA Packet Radio Research** (1970s-80s) — Precursors to modern mesh
- **IEEE 802.11s** (2007) — WiFi mesh standard
- **Serval Project** (2012) — Phone-to-phone mesh over WiFi

### The Modern Mesh Revolution (2019-Present)

- **Meshtastic** (2019) — Open-source LoRa mesh, explosion of adoption
- **Reticulum** (2022) — Markqvist's secure mesh stack
- **Yggdrasil** (2020) — Modern overlay network

### Key Drivers

1. **Censorship** — Internet shutdowns as political tool
2. **Privacy** — Desire to avoid internet dependency
3. **Disaster Resilience** — Hurricanes, earthquakes, war
4. **Sovereignty** — Building alternatives to corporate infrastructure

---

## Technology Categories

### 1. LoRa Mesh Networks

**LoRa** (Long Range) is a proprietary radio modulation scheme using chirp spread spectrum. It achieves:
- **Range**: 2-10 km in rural areas, longer with line of sight
- **Power**: Extremely low — can run for years on batteries
- **Bandwidth**: Very low (~300 bps to 19 kbps)
- **Frequencies**: ISM bands (433 MHz, 868 MHz EU, 915 MHz US)

#### Meshtastic

The most popular LoRa mesh platform:

- **Hardware**: Cheap ESP32-based radios ($20-50)
- **Software**: Open-source firmware
- **Range**: Up to 10 km with stock antennas
- **Features**: GPS, encrypted messaging, sensor integration
- **Ecosystem**: Multiple clients, maps, tracking dashboards

[Ripple](https://github.com/ripple-lib/ripple) — Experimental LoRa mesh  
[cubeos-app/meshsat](https://github.com/cubeos-app/meshsat) — Meshtastic-Iridium bridge

### 2. Reticulum Stack

A complete networking stack for secure mesh communication:

- **Auto-discovery**: Nodes find each other automatically
- **Encryption**: All traffic encrypted with Wireguard-style keys
- **Addressing**: Distributed addressing without DNS
- **Protocols**: IncludesLXMF (messaging), NomadNet (client)

[NomadNet](https://github.com/markqvist/NomadNet) — Encrypted chat over Reticulum  
[Sideband](https://github.com/markqvist/Sideband) — Mobile LXMF client

### 3. Overlay Networks

These run over existing internet but provide true P2P connectivity:

#### Yggdrasil

- **Architecture**: End-to-end encrypted overlay with Wireguard-style crypto
- **Routing**: Greedy routing on a spanning tree
- **Clients**: Native on many platforms
- **Performance**: Slower than native internet but fully encrypted

#### cjdns

- **Legacy**: The original encrypted IPv6 mesh protocol
- **Status**: Less actively maintained
- **Network**: Hyperboria — largest cjdns network

### 4. Delay-Tolerant Networks (DTN)

When connectivity is intermittent, DTN protocols store-and-forward:

#### Briar

- **Transport**: Bluetooth, WiFi, Tor
- **Protocol**: Store-and-forward messaging
- **Use Case**: Secure messaging when internet unavailable
- **Platforms**: Android (primary); desktop via Tor; iOS unsupported

#### Secure Scuttlebutt (SSB)

- **Protocol**: Append-only log with gossip replication
- **Platform**: Manyverse (Android), Patchwork (desktop)
- **Use Case**: Social networking without servers

---

## Network Comparison

| Network | Type | Range | Internet Required | Encryption | Active Development |
|---------|------|-------|--------------------|------------|--------------------|
| **Meshtastic** | LoRa | 2-10 km | No | Yes | Very Active |
| **Reticulum** | WiFi/LoRa/BT | Varies | Optional | Yes | Active |
| **Yggdrasil** | Overlay | N/A | Yes | Yes | Active |
| **cjdns** | Overlay | N/A | Optional | Yes | Moderate |
| **Briar** | BT/WiFi | 10-100m | No | Yes | Active |
| **SSB** | P2P | N/A | Optional | No | Moderate |

---

## Major Implementations

### Mesh Hardware

| Device | Price | Features |
|--------|-------|----------|
| **Heltec LoRa** | $20-30 | ESP32, OLED, GPS |
| **TTGO LoRa** | $25-40 | ESP32, battery holder |
| **RAK WisBlock** | $50+ | Modular, professional |
| **RAK WisMesh Pocket** | $80 | Pre-built handheld |
| **SpecFive Spectre** | $150 | Android phone + LoRa |

### Software Ecosystem

- [Meshtastic](https://meshtastic.org/) — Firmware and apps
- [Reticulum](https://reticulum.network/) — Full stack
- [Yggdrasil](https://yggdrasil-network.github.io/) — Overlay
- [awesome-meshtastic](https://github.com/ajmcquilkin/awesome-meshtastic) — Resources

---

## Use Cases

### 1. Disaster Communication

When cell towers and internet are down, mesh networks provide local communication:

- Hurricane response teams use Meshtastic
- Ukraine wartime communication
- Wildfire evacuation coordination

### 2. Privacy and Operational Security

- No internet dependency means no metadata leakage
- True air-gapped networks for sensitive operations
- Bypass surveillance infrastructure

### 3. Rural Connectivity

In areas without internet infrastructure:
- Remote villages in developing countries
- Scientific expeditions
- Maritime communications

### 4. Protest and Resistance

- Hong Kong protests used mesh
- Iran internet shutdown workarounds
- Emergency communication infrastructure

---

## Evidence at a Glance

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

- **Independence**: No internet required
- **Censorship resistance**: Can't block what they can't see
- **Low power**: Can run on batteries/solar
- **Lower cost**: No ISP, no cellular plan

### Limitations

- **Range limits**: Mesh requires nodes in proximity
- **Low bandwidth**: LoRa is very slow
- **User density**: More users = better network
- **Complexity**: Requires hardware and setup
- **Discovery**: Finding others on the network

### Operational Considerations

- More nodes = better range (mesh effect)
- Antenna choice matters significantly
- Line of sight dramatically increases range
- Battery life depends on usage patterns

---

## Attack Surface

### Physical Layer

- RF jamming (counter: frequency hopping, spread spectrum)
- Direction finding (counter: low-power transmissions, movement)
- RF interference

### Network Layer

- Sybil attacks (counter: node reputation)
- Eclipse attacks (counter: diverse peer selection)
- Routing attacks

### Social Layer

- Bad hardware (counter: verify sources)
- Compromised firmware (counter: reproducible builds)
- User error (counter: education)

---

## Related Files

- [Overview - Encrypted Messaging](/encrypted-messaging) — Briar, SimpleX, and offline-first protocols
- **Off-Grid Messaging** — practical patterns over LoRa, Reticulum, Briar, HF
- [Overview - Mix Networks](/mix-networks) — anonymity overlays applicable to mesh
- [Overview - Decentralized Identity](/identity/overview-decentralized-identity) — pseudonymous IDs in disconnected nets
