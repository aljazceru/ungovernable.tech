---
title: "MeshCore"
slug: meshcore
type: deep-dive
pillars: ["mesh"]
readiness: usable
description: "MeshCore, lightweight firmware for multi-hop LoRa mesh messaging with dedicated repeaters and direct-path routing: how it differs from Meshtastic."
dek: "Lightweight, portable C++ library and firmware for multi-hop LoRa (and other packet radio) mesh routing. Designed for embedded, custom, and resilient off-grid networks with explicit node roles and focus on simplicity for developers."
updated: 2026-06-22
created: 2026-06-22
origin: vault
source: "05-Off-Grid-Networks/MeshCore.md"
aliases: ["Mesh Core"]
tags: ["meshcore", "lora", "mesh", "off-grid", "deep-dive", "routing"]
---

## What it is

MeshCore (meshcore-dev org) provides a minimal routing core + reference firmwares (Companion, Repeater, Room Server) that turn supported LoRa boards into a decentralized, self-healing mesh. It emphasizes:

- Fixed node roles to control routing quality (Companions do not repeat traffic by default).
- No central servers or internet dependency.
- Easy flashing via web flasher for supported hardware; developer-friendly C++ library and examples.
- MIT license, portable to embedded projects.

Positioning vs peers (per project and community comparisons):
- Vs [Meshtastic](/kb/meshtastic/): lighter core, more embedded/developer-oriented, explicit roles and room-server BBS primitives, different routing emphasis (hybrid elements).
- Vs [Reticulum](/kb/reticulum/): narrower (primarily LoRa packet radio focus vs full stack over many transports); simpler for radio-centric use cases.
- Vs Bitchat: radio hardware first (not phone-BLE only).

Active in 2026 with firmware releases, client apps (iOS/Android/web), HA integration, gateways, and community nodes.

## Architecture & Roles

### Core routing library
- C++ , no dynamic allocation outside init (embedded-friendly).
- Multi-hop packet routing with hop limit.
- Self-healing mesh; passive neighbor observation.
- Supports LoRa (and designed for other packet radios).

### Firmware roles (pre-built via flasher)
- **Companion**: Pairs with external client apps over BLE/USB/Wi-Fi/Serial. Does not repeat messages (prevents polluting routes from mobile/handheld nodes).
- **Repeater**: Extends coverage; relays traffic. Can be solar-powered (e.g., SenseCAP Solar Node).
- **Room Server**: Simple BBS / shared posts server for group coordination or data sharing over the mesh.

Examples in repo also include KISS modem (serial bridge), simple secure chat, sensor telemetry.

### Clients & tooling
- Official companion apps: web (app.meshcore.nz), Android (Liam Cottle), iOS.
- Config tool: config.meshcore.io (for repeaters/room servers over USB or remote LoRa mgmt).
- Flasher: https://meshcore.io/flasher (prebuilts for Heltec, RAK, LILYGO etc.).
- Libraries: meshcore.js (Node), Python CLI, ESPHome component, HA integration.
- Remote management of infrastructure nodes over the mesh itself.

### Hardware
Targets common ESP32 / nRF / RAK LoRa boards (Heltec V3/V4, RAK WisBlock, LILYGO T-Deck / T-LoRa / T-Watch variants, Wio Tracker, ThinkNode, WisMesh, etc.). See flasher for current matrix. Antennas and placement dominate range (same physics as other LoRa meshes).

## Protocol & Features

- Packet routing focused on reliability for embedded use.
- Public channels / group comms via clients; private/encrypted sessions in examples (Simple Secure Chat uses Noise or equivalent).
- Room server for structured shared "posts" / BBS-style messaging (durable within mesh).
- Sensor support and telemetry examples.
- Gateways/MQTT bridges exist in community (bidirectional to internet when desired, without mandating it).
- Low-power design; repeaters can run solar.

Encryption: End-to-end options in client paths; core library is transport/routing. Past public issues around AES implementation were identified and addressed in development (see repo issues ~2025). Verify current primitives in active firmware.

KISS modem protocol for host integration documented.

## Trade-offs

### Strengths
- Explicit role model reduces certain routing pathologies (mobile nodes don't become accidental backbone).
- Very lightweight and auditable C++ core suitable for custom embedded sovereign devices.
- Fast path to working mesh with prebuilts + flasher; good for tactical, IoT, repeater networks.
- Room server primitive enables lightweight shared state without full app servers.
- Active cross-ecosystem tooling (HA, ESPHome, gateways) for practical deployments.

### Limitations
- Younger / smaller ecosystem than Meshtastic (fewer off-the-shelf clients, maps, long-running community meshes documented at scale).
- Documentation and protocol spec still maturing (FAQ, KISS docs, but V2 protocol discussions on roadmap).
- Range/airtime physics identical to other LoRa: low bandwidth, duty-cycle limits, line-of-sight dependent.
- Encryption story is "in the apps/examples" rather than uniform default like some stacks; audit per deployment.
- Companion devices require a paired "controller" (phone/laptop) for full UX in many cases (standalone options exist via T-Deck etc.).

## Attack Surface

- **RF layer**: Jamming, direction finding, collision (same as [Meshtastic](/kb/meshtastic/), [Reticulum](/kb/reticulum/) LoRa modes). Mitigations: low duty cycle, mobility, directional antennas, frequency agility where supported.
- **Routing**: Flood/routing attacks, wormhole, Sybil via many cheap nodes. Fixed roles and companion non-repeating help; reputation or ACLs on roadmap for repeaters.
- **Crypto**: Historical AES issues in early versions — confirm current firmware uses reviewed modes (e.g. authenticated encryption, proper IVs). Noise in chat examples provides forward secrecy where used.
- **Endpoint / companion**: Phone or host compromise leaks keys/session; use hardened OS where possible.
- **Physical / supply**: Rogue firmware on cheap boards; prefer reproducible or verified flashes. Solar repeaters add physical access risk.
- **Internet bridges/gateways**: If used, introduce metadata or availability dependency — optional for pure off-grid.

## Comparison Snapshot (LoRa meshes)

| Project     | Focus                  | Roles / Topology Control | Encryption Model          | Standout Primitive     | Ecosystem Maturity |
|-------------|------------------------|----------------------------|---------------------------|------------------------|--------------------|
| Meshtastic | Consumer + telemetry  | Managed flood, some next-hop | Per-channel AES + optional PK | MQTT bridge, maps, sensors | Very high |
| MeshCore   | Embedded / custom / routers | Explicit: Companion (no repeat), Repeater, Room Server | App/example level (Noise etc.); routing core transport | Room Server BBS, KISS, flasher simplicity | Growing (2026) |
| Reticulum  | Full encrypted stack  | Destination-oriented, multi-transport | Wireguard-style + app protocols | LXMF messaging, NomadNet | High for stack |

## Operational Notes

- Start with flasher + supported board (Heltec/RAK common).
- Use Companion firmware + mobile/desktop app for chat.
- Deploy solar repeaters at elevation for coverage.
- For custom: build on the C++ lib + examples (companion radio, sensor, secure chat).
- Monitor airtime; same LoRa constraints.
- Community: meshcore.gg Discord, docs.meshcore.io, YouTube explainers (Comms Channel, Liam Cottle tech talk).

## Evidence & Status

- Active repo under meshcore-dev (firmware, examples, issues with power measurements, hardware quirks 2026).
- Pre-built flashing, multi-platform clients shipping.
- MIT; contributions via dev branch.
- Used in off-grid, emergency prep, tactical discussions on X 2026; hardware vendors shipping "for MeshCore" nodes.
- Not yet at Meshtastic's deployment volume but strong for developers wanting controllable mesh routing without full Meshtastic feature surface.

## Sources & References

- Project site: https://meshcore.io/
- GitHub: https://github.com/meshcore-dev/MeshCore (library, firmware, examples)
- Flasher & docs: https://meshcore.io/flasher , https://docs.meshcore.io , FAQ in repo
- Clients & tools: liamcottle repos, meshcore.js, community gateways/HA/ESPHome
- Presentations: MeshCore Technical Presentation (Liam Cottle), quickstart series (The Comms Channel)
- Comparisons: Community posts and Blackout Comms site explicitly compare MeshCore/Meshtastic/Blackout Comms

*Primary sources preferred: repo code, protocol docs, hardware measurements from issues.*
