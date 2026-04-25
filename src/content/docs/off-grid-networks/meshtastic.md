---
title: "Meshtastic"
tags:
  - "meshtastic"
  - "lora"
  - "mesh"
  - "off-grid"
  - "deep-dive"
---
*Open-source LoRa mesh firmware that turns commodity ESP32 / RAK / nRF52 boards into a self-organizing, kilometers-range, encrypted text and telemetry mesh. No cell network, no internet, no subscription.*

---

## What it is

Meshtastic is firmware (and an ecosystem of clients) for LoRa radios on the unlicensed sub-GHz ISM bands (868 MHz EU, 915 MHz US, 433 MHz Asia). Each node has a 32-bit hardware ID and an Ed25519 keypair (post v2.5). Nodes flood-route packets across a many-hop mesh; each hop re-broadcasts unless the packet has already been seen.

Use cases:

- Hiking, sailing, off-grid groups out of cell range.
- Neighborhood resilience networks.
- Festival and event comms.
- Disaster fallback (Hurricane Helene 2024 saw substantial Meshtastic deployment).
- Emergency-services ad-hoc coordination.

What it explicitly is not: a private mesh. The default channel is broadcast and observable by anyone in radio range with the channel key.

---

## Hardware

The reference platforms are inexpensive (€20-€60) integrated boards:

| Board | MCU | LoRa | Notes |
|-------|-----|------|-------|
| **LILYGO T-Beam** | ESP32 | SX1276/1262 | GPS, OLED, 18650 battery, most common starter |
| **Heltec V3** | ESP32-S3 | SX1262 | Compact, OLED, USB-C |
| **RAK WisBlock 4631** | nRF52840 | SX1262 | Modular, low power, BLE |
| **LILYGO T-Echo** | nRF52840 | SX1262 | E-paper, GPS, ultra-low power |
| **Station G2 / G1** | ESP32 | SX1262 | Solar-friendly, no battery in box |

Antennas matter more than the radio chip. A $5 stock antenna will give 1 km; a tuned 5 dBi at 5-10 m elevation reaches 30+ km line-of-sight.

---

## Protocol mechanics

### Packet structure

Every packet is a small Protobuf-encoded `MeshPacket`:

```
from        : node_id (32-bit)
to          : node_id (32-bit, broadcast = 0xFFFFFFFF)
channel     : 0-7 (selects channel key)
hop_limit   : starts at 3-7, decremented per relay
want_ack    : optional reliability flag
payload     : encrypted PortNum + bytes
```

LoRa airtime limits push payload sizes to ~230 bytes for the most common settings. The protocol frames messages, sensor telemetry, position reports, and routing control packets identically.

### Routing: managed flood

Default mode is managed flood routing: each node retransmits packets it hasn't seen, with a randomized contention window to avoid collisions, and a strict hop limit. Routing is stateless; there is no neighbor discovery beyond passive observation.

Newer features:

- Next-hop routing (v2.5+): opportunistic learning of best-next-hop from received packets.
- MQTT bridge: a single node with internet uplink can bridge a regional mesh to a global MQTT broker for cross-mesh and integration with home automation.

### Encryption

Per-channel symmetric AES-256-CTR with a pre-shared key. The default channel uses a well-known key (`AQ==`) that is broadcast-readable by intent so newcomers can join. Private channels use a user-generated 256-bit key shared out-of-band.

v2.5+ direct messages add public-key encryption: each node has a Curve25519 keypair, and DMs are encrypted to the recipient's public key. Forward secrecy is not provided; keys are long-term. Public keys are distributed via NodeInfo broadcasts.

### Channel hash and utilization

Each channel computes a 1-byte hash to deduplicate cross-channel traffic. The protocol intentionally rate-limits each node; one chatty node can saturate the entire mesh's airtime, so firmware enforces per-port caps.

---

## Modes / presets

Trade-offs between range, throughput, and airtime. Current presets (US 915 MHz; verify rates against [meshtastic.org/docs/overview/radio-settings](https://meshtastic.org/docs/overview/radio-settings/)):

| Preset | SF | BW | Approx. bitrate | Range (typ.) |
|--------|----|----|-----------------|--------------|
| **Short Turbo** | 7 | 500 kHz | ~21.9 kbps | <1 km |
| **Short Fast** | 7 | 250 kHz | ~10.9 kbps | 1-3 km |
| **Short Slow** | 8 | 250 kHz | ~6.25 kbps | 2-5 km |
| **Medium Fast** | 9 | 250 kHz | ~3.52 kbps | 4-8 km |
| **Medium Slow** | 10 | 250 kHz | ~1.95 kbps | 5-12 km |
| **Long Moderate** | 11 | 250 kHz | ~1.07 kbps | 8-20 km |
| **Long Fast** *(default)* | 11 | 250 kHz | ~1.07 kbps | 10-25 km |
| **Long Slow** *(deprecated)* | 12 | 125 kHz | ~0.18 kbps | 20-60 km |

Mismatched presets produce silent meshes, a common mistake. All nodes in a mesh must agree on preset and frequency. The older "Very Long Slow" preset has been removed.

---

## Clients

| Client | Platform | Notes |
|--------|----------|-------|
| **Meshtastic Android / iOS** | Mobile | Reference apps; BLE pairing |
| **Web Client** | Browser | WebSerial pairing; Tailscale-friendly |
| **Meshtastic Python CLI** | Desktop | Scripting and automation |
| **NodeRed integrations** | Server | Home automation bridges |

A node is typically operated headless (battery + radio) and paired to a phone via BLE for messaging UX.

---

## Privacy properties

| Property | Status |
|----------|--------|
| Content confidentiality (with channel key) | Yes (AES-256-CTR) |
| Sender authentication | v2.5+ (Curve25519 signatures on packets) |
| Forward secrecy | No; channel keys static, DM keys long-term |
| Metadata privacy | No; packet headers carry node IDs in plaintext |
| Direction-finding resistance | No; active radios are triangulable |
| Sybil resistance | None inherent |

For threat models that include radio surveillance, layer Meshtastic with [Off-Grid Messaging](/encrypted-messaging/off-grid-messaging) patterns: short bursts, low duty cycle, mobile transmitters, mission-keys-only on participants' devices.

---

## Operational patterns

### Default channel + private channel

Run two channels: default for joining new participants and emergencies, a private channel for the actual group comms with a key shared in person.

### Solar / battery node

A LILYGO T-Beam or Station G2 with a 5 W solar panel and 18650 cells is autonomous indefinitely. Place high (rooftop, hilltop) for range; low duty cycle minimizes draw.

### MQTT bridge to internet

One node with a Wi-Fi or cell uplink and the MQTT bridge enabled connects the local mesh to the global Meshtastic MQTT topic. Useful for cross-region monitoring; breaks the off-grid model if compromised.

### Position privacy

The `want_position` flag is on by default. Disable it for adversarial environments. A beacon transmitting position every minute is a homing signal.

---

## Trade-offs

### Strengths

- Very cheap; full kit under €60.
- Easy to deploy; flash firmware, pair phone, send.
- Self-organizing; no infrastructure, no admin.
- Multi-day battery and solar friendly.
- Open firmware, large community.

### Limitations

- Tiny bandwidth; text, not media.
- Public protocol; no protocol-level metadata privacy.
- No forward secrecy.
- Channel key compromise reveals all past channel traffic.
- Direction-finding; emitting nodes are locatable.
- Channel utilization is fragile; one chatty bot can saturate a region.

---

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Channel-key compromise | Rotate; segment via multiple channels |
| Sybil flooding | Per-node airtime cap; trusted-node lists |
| DF / triangulation | Low duty cycle, mobile transmitters, mission-keys-only |
| MQTT bridge compromise | Don't enable in adversarial deployments |
| Firmware supply-chain | Flash from official releases; verify signatures |
| Endpoint compromise | Phone E2EE / disk encryption |

---

## Recent developments (2024-2026)

- PKI / DM encryption (v2.5+): Curve25519 keys per node for direct messages.
- Next-hop routing beyond pure flood.
- Range expansion with new firmware optimizations.
- Hurricane Helene 2024: substantial real-world deployment for relief coordination.
- Position obfuscation options expanded for safety in adversarial regions.

---

## Related files

- [Overview - Off-Grid Networks](/off-grid-networks)
- [Reticulum](/off-grid-networks/reticulum) — alternative stack with built-in E2EE
- [FIPS](/off-grid-networks/fips) — Nostr-keyed mesh routing
- [Off-Grid Messaging](/encrypted-messaging/off-grid-messaging)
- [MOC - Censorship Resistance](/meta/moc-censorship-resistance)

---

## Primary sources

- Meshtastic — [meshtastic.org](https://meshtastic.org)
- Firmware repository — [github.com/meshtastic/firmware](https://github.com/meshtastic/firmware)
- Protocol spec — [meshtastic.org/docs/overview/mesh-algo](https://meshtastic.org/docs/overview/mesh-algo)
- LoRa Alliance, *LoRaWAN Regional Parameters*.

