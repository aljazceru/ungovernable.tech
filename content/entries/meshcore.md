---
title: "MeshCore"
slug: meshcore
type: deep-dive
pillars: [mesh]
readiness: usable
description: "MeshCore turns inexpensive LoRa boards into an off-grid text mesh with dedicated repeaters and learned direct routes. How it works and how it differs from Meshtastic."
dek: "Meshtastic's closest sibling: the same cheap LoRa radios, but only dedicated repeaters relay traffic, and routes are learned rather than flooded. Lighter on airtime, with thinner cryptography."
updated: 2026-10-23
created: 2026-06-22
origin: original
related: [meshtastic, building-a-mesh, off-grid-networks, off-grid-messaging, reticulum, bitchat, internet-shutdown-preparedness, running-freedom-infrastructure]
aliases: ["Mesh Core", "MeshCore LoRa"]
tags: ["meshcore", "lora", "mesh", "off-grid", "deep-dive"]
---

MeshCore is open-source firmware and a C++ routing library that turn inexpensive LoRa radios into a multi-hop text mesh with no towers, SIM cards or internet. It is the closest alternative to [Meshtastic](/kb/meshtastic/). It runs on the same boards (Heltec, RAK WisBlock, LILYGO T-Deck and T-Beam, Seeed and others) and serves the same uses, from emergency response to hiking to events. But it makes a different bet about routing. In Meshtastic, every node helps relay. In MeshCore, **only dedicated repeaters relay**, and once a route is known, messages follow it instead of flooding the whole mesh. The core firmware is MIT-licensed and developed at meshcore-dev, with prebuilt firmware flashable from a browser. Its UK community hub, meshcore.co.uk, reports more than 30,000 users in more than 80 countries.

## How it works

**Roles.** You flash each radio as one of three firmware types:
- **Companion**: your personal node, paired over Bluetooth, USB or Wi-Fi with a phone, desktop or web app. It does **not** repeat other people's traffic, so mobile handhelds never become accidental backbone links.
- **Repeater**: a fixed relay, often solar-powered on a rooftop or hill, that you administer remotely over the mesh.
- **Room server**: a small bulletin board that stores shared posts for a group.

There is also standalone firmware for devices with keyboards and screens, such as the T-Deck.

**Routing.** The first message to a contact floods through the repeaters. The recipient's delivery report comes back carrying the list of repeaters the message passed through. The sender stores that path, and later messages carry it in the packet, so only the repeaters named on the path retransmit. Group channels have no single destination, so they always flood, but repeater operators can cap how far floods travel (`flood.max`). Nodes announce themselves with **adverts**: a name, a position if they choose, and an Ed25519 public key signed against spoofing. Companions advertise only when the user taps the button; repeaters advertise every 12 hours by default.

**Encryption.** Every node has an Ed25519 identity key. Direct messages use a shared secret from an elliptic-curve key exchange between the two nodes' keys. Group channels use a shared 128- or 256-bit channel secret. The default public channel's key is published, so anyone can read it. Payloads are encrypted with **AES-128 in ECB mode**, followed by an HMAC-SHA256 tag **truncated to 2 bytes**. Packets address the sender and recipient by **1-byte hashes** of their keys. A planned v2 packet format reserves room for 2-byte hashes and a 4-byte MAC.

**Software.** The firmware, flasher and configuration tools are open source. Clients include the web app at app.meshcore.nz, Liam Cottle's Android and iOS apps, meshcore.js and a Python CLI. Per the project FAQ, the T-Deck standalone firmware and the native mobile apps are **not** open source. Some features, such as deeper T-Deck maps and immediate remote administration from the phone apps, are unlocked by a paid registration. meshcore.co.uk also sells *MeshOS*, a standalone-device firmware licensed at £8 per device, and a MeshCore handset.

## MeshCore and Meshtastic

| | MeshCore | [Meshtastic](/kb/meshtastic/) |
|---|---|---|
| Who relays | Dedicated repeaters only; companions never repeat | Every node by default, through managed flooding (roles can mute clients) |
| Direct messages | Flood once, then a learned source path | Managed flood; next-hop routing since firmware 2.6 |
| Group channels | Always flood, with hop caps per repeater | Managed flood |
| Direct-message crypto | ECDH shared secret, AES-128-ECB, 2-byte MAC | X25519, then AES-256-CCM (authenticated) |
| Channel crypto | Shared secret, AES-128-ECB, 2-byte MAC; public channel key published | AES-CTR channel key (AEAD option from 2.8.1); default key published |
| Forward secrecy | No | No |
| Licensing | MIT firmware; T-Deck firmware and native apps closed | GPL-3.0 firmware; open apps |
| Maturity | Younger (2025), fast-growing, frequent releases | Older (2019), largest LoRa-mesh community and ecosystem |

The practical upshot: MeshCore spends less airtime on busy meshes and gives repeater operators more control. That suits planned regional networks with a few well-placed solar repeaters. Meshtastic has the larger ecosystem, fully open clients, and more conservative, authenticated cryptography. The two do not interoperate over the air, although community bridges exist. A neighbourhood should pick one; see [Building a Mesh](/guides/building-a-mesh/).

## What it protects against

- **Infrastructure loss.** It needs no towers, SIM cards, internet or accounts, and a mesh keeps working through outages and shutdowns.
- **Casual eavesdropping.** Direct messages and private channels are unreadable without the keys, including to the repeaters that carry them.
- **Spoofed node announcements.** Adverts are signed.
- **Airtime exhaustion.** Learned paths and non-repeating companions reduce flooding, which keeps a shared, duty-cycle-limited radio channel usable as the mesh grows.

## What it trusts, and the limits

- **Thin cryptography.** ECB mode leaks when two 16-byte blocks of plaintext are identical. A 2-byte MAC means a forged packet has about a 1-in-65,536 chance of being accepted. There is no forward secrecy: anyone who records traffic and later obtains a key (for example from a seized node) can decrypt everything recorded. No independent audit has been published. Treat MeshCore as private from bystanders, not from a determined adversary.
- **Metadata on the air.** Headers, hashed addresses and routing paths are visible. Adverts broadcast names, keys and optional positions. 1-byte hashes collide on large meshes. Like any radio, LoRa transmitters can be located by direction finding and jammed.
- **Repeater operators and their defaults.** Routes depend on whoever runs the repeaters. The default admin password is `password`, so change it. Physical access to a repeater exposes its keys.
- **Closed and paid pieces.** The main phone apps and standalone firmware are not open source, so part of what you run cannot be inspected.
- **Physics.** Expect kilometres of range with line of sight, a few hundred bytes per message, and regional duty-cycle limits.

## Readiness

**Usable.** MeshCore has shipped stable firmware releases since 2025 (v1.18.0 in October 2026). It runs on dozens of widely available boards and is deployed by tens of thousands of users. For off-grid text in an outage, at events or in the backcountry, it works today, and on large meshes it is often more airtime-efficient than Meshtastic. Its weaker, unaudited cryptography and partly closed client stack are the reasons to prefer Meshtastic (or [Reticulum](/kb/reticulum/)) when confidentiality really matters.

For the wider comparison of online and off-grid choices, see [Choosing a private messenger](/kb/compare-messengers/).

## Primary sources

- MeshCore (UK community hub, user guides, MeshOS): https://meshcore.co.uk/ · MeshOS: https://www.meshcore.co.uk/meshos.html
- Firmware and library (MIT): https://github.com/meshcore-dev/MeshCore · Releases: https://github.com/meshcore-dev/MeshCore/releases · Documentation: https://docs.meshcore.io/
- Protocol: packet format https://github.com/meshcore-dev/MeshCore/blob/main/docs/packet_format.md · payloads https://github.com/meshcore-dev/MeshCore/blob/main/docs/payloads.md · encryption code https://github.com/meshcore-dev/MeshCore/blob/main/src/Utils.cpp
- FAQ (routing, roles, open-source status, defaults): https://github.com/meshcore-dev/MeshCore/blob/main/docs/faq.md
- Tools: flasher https://meshcore.io/flasher · config https://config.meshcore.io/ · web app https://app.meshcore.nz/ · meshcore.js https://github.com/liamcottle/meshcore.js · Python CLI https://github.com/fdlamotte/meshcore-cli
- Meshtastic, for the comparison: encryption https://meshtastic.org/docs/overview/encryption/ · routing https://meshtastic.org/docs/overview/mesh-algo/
