---
title: "Building a Local Mesh Network"
slug: building-a-mesh
type: guide
pillars: [mesh, messaging]
description: "How to set up LoRa radios with Meshtastic or MeshCore for off-grid text messaging: choosing hardware, flashing firmware, private channels, placement and privacy."
dek: "A few cheap radios and a phone app give you a text network that needs no towers, no SIM cards and no internet."
updated: 2026-10-17
created: 2026-10-17
origin: original
level: beginner
time: "2 hours"
related: [meshtastic, meshcore, reticulum, off-grid-networks, internet-shutdown-preparedness, off-grid-messaging]
---

LoRa (long range) is a radio modulation that trades speed for distance: it moves tiny amounts of data, but it can do so over several kilometres with milliwatts of power, in licence-free bands. Two open-source projects turn inexpensive LoRa boards into a self-healing text mesh that your phone talks to over Bluetooth: **Meshtastic** and **MeshCore**. This guide gets a small group up and running. For the architecture behind them, read [Meshtastic](/kb/meshtastic/), [MeshCore](/kb/meshcore/) and [Off-Grid and Mesh Networks](/kb/off-grid-networks/).

## 1. Choose the firmware

| | Meshtastic | MeshCore |
|---|---|---|
| Routing | Managed flooding: every node rebroadcasts, up to a hop limit (default 3, maximum 7) | Flood to discover a path, then send directly along it; dedicated repeaters and room servers |
| Strength | Large community, many apps and integrations, easy start | Scales better in dense or large meshes; fewer redundant rebroadcasts |
| Apps | Android, iOS, web, desktop | Android, iOS, web |
| Best for | Getting a group talking quickly | Building a wider, planned network with fixed repeaters |

The two do not interoperate. Pick one for your group and area; check which one people near you already run.

## 2. Get hardware

Common boards include Heltec LoRa 32 and Wireless Stick boards, LILYGO T-Beam (with GPS) and T-Echo, and RAKwireless WisBlock kits. Both projects publish lists of supported devices. You need:

- the **right frequency for your region**: 868 MHz in Europe, 915 MHz in the Americas and Australia, others elsewhere. Using the wrong band is illegal and works badly;
- a **decent antenna** (the stock antennas on many boards are poor; a tuned antenna is the cheapest upgrade);
- a **battery** (most boards take a single 18650 or LiPo cell), or a small solar panel for a fixed node.

Never power on a LoRa board without its antenna connected; that can damage the radio.

## 3. Flash the firmware

- Meshtastic: the web flasher at <https://flasher.meshtastic.org/> from a Chromium-based browser over USB.
- MeshCore: the web flasher linked from <https://meshcore.co.uk/> or the project's GitHub.

Then install the phone app, pair with the radio over Bluetooth, and **set your region** before anything else.

## 4. Make it private

- **The default Meshtastic channel is not private.** Its key is publicly known, so anyone running Meshtastic nearby can read it. Create your own channel with a randomly generated key and share it with your group by QR code, in person.
- **Direct messages** between Meshtastic nodes are encrypted with public-key cryptography (since firmware 2.5), so only the recipient can read them, but relaying nodes still see who is messaging whom.
- **Position sharing leaks your location.** Turn it off, or reduce its precision, for anyone who should not be found.
- **Node names are broadcast.** Do not use real names.
- **Radio can be located.** A transmitting radio can be found with direction-finding equipment. This is a real risk under a hostile government; transmit only what you need.

## 5. Placement is everything

LoRa needs line of sight more than power. A node on a rooftop, hilltop or high window reaches far further than ten nodes at street level. Plan a few **fixed relay nodes** in high places (Meshtastic's *router* or *repeater* roles; MeshCore's dedicated repeater firmware), powered by solar panels where mains is not available, and keep handheld nodes as clients.

## 6. Respect the rules

In licence-free bands there are limits on power and, in Europe, on **duty cycle** (the share of time a device may transmit, for example 1% or 10% depending on the sub-band). The firmware enforces sensible defaults when the region is set correctly. If you are a licensed radio amateur and enable *ham mode* to use more power, **encryption is switched off**, because encryption is not permitted on amateur bands.

## 7. Practise

Run a drill: everyone switches phones to airplane mode with Bluetooth on, and the group coordinates a meeting point using only the mesh. You will find the dead spots, the confusing settings and the flat batteries before they matter.

## Going further

- [Reticulum](/kb/reticulum/) is a full networking stack that can run over LoRa, packet radio, Wi-Fi and the internet at once, with end-to-end encryption and its own addressing.
- [Briar](/kb/briar/) and [Bitchat](/kb/bitchat/) mesh phones directly over Bluetooth with no extra hardware.
- [Naming on Mesh and Off-Grid Networks](/kb/mesh-naming/) covers how services are found without DNS.

## Sources

- Meshtastic documentation, *Introduction*, *Supported hardware* and *Encryption*: <https://meshtastic.org/docs/introduction/>, <https://meshtastic.org/docs/overview/encryption/>
- Meshtastic, *Firmware 2.5 release notes* (public-key encrypted direct messages): <https://github.com/meshtastic/firmware/releases>
- MeshCore project: <https://github.com/meshcore-dev/MeshCore>
- ETSI EN 300 220 (short range devices, 25 MHz to 1 GHz), duty-cycle limits in Europe: <https://www.etsi.org/>
- Reticulum Network Stack manual: <https://reticulum.network/manual/>
