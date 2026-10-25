---
title: "Off-grid communication compared"
slug: compare-off-grid
type: comparison
pillars: [mesh, messaging]
description: "Compare Meshtastic and MeshCore beside Reticulum, Briar, Bitchat, HF data and satellite IoT by reach, capacity, hardware, encryption and readiness."
dek: "Match the tool to the people and paths you can actually reach when connectivity fails."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [meshtastic, meshcore, reticulum, briar, bitchat, hf-data-modes, satellite-iot, off-grid-networks, building-a-mesh]
---

## Summary

An off-grid plan needs reachable peers, compatible hardware and a tested route. The ranges below describe the transport's reach, not guaranteed distances. Capacity is described by workload class because radio settings, topology and interference prevent a single useful throughput number across these systems.

## Meshtastic and MeshCore, side by side

| Question | [Meshtastic](/kb/meshtastic/) | [MeshCore](/kb/meshcore/) |
|---|---|---|
| Reach | LoRa links; the project describes kilometre-scale communication, extended by relaying | LoRa links extended by repeaters; survey the actual path |
| Capacity | Text and position messages over shared radio airtime | Short messages over shared radio airtime; learned paths for direct messages |
| Hardware | Supported LoRa radio; optional paired phone | Supported LoRa radio as companion, repeater or room server |
| Relaying | Nodes can rebroadcast packets through the mesh | Companions do not relay; dedicated repeaters do |
| Encryption | Channel keys and public-key direct messages; the default channel key is public; no forward secrecy | AES-128 block encryption in ECB mode with a short MAC; the default public channel key is published |
| Readiness | **Usable** | **Usable**, with the cryptographic limits described in its entry |

The [Meshtastic encryption documentation](https://meshtastic.org/docs/overview/encryption/) and [MeshCore FAQ](https://github.com/meshcore-dev/MeshCore/blob/main/docs/faq.md) distinguish private communication from public channel defaults. Choose one supported ecosystem for a radio group and rehearse it using [building a mesh](/guides/building-a-mesh/).

## Other transports and applications

| Option | Reach and capacity | Hardware | Encryption boundary | Readiness |
|---|---|---|---|---|
| [Reticulum](/kb/reticulum/) | Carrier-dependent local or wide-area links; supports low-bandwidth radios and higher-capacity backhaul | Computer plus interfaces such as RNode LoRa, packet radio or Wi-Fi | Encrypted communication and forward secrecy are documented; application behavior still matters | **Usable** |
| [Briar](/kb/briar/) | Nearby Bluetooth/Wi-Fi synchronization; Tor when internet exists; capacity follows transport | Supported devices with Briar installed | End-to-end encrypted communication; contacts and local device security matter | **Battle-tested**; project is in maintenance mode |
| [Bitchat](/kb/bitchat/) | Nearby BLE mesh, extended by relaying; short-message workload; Nostr path requires internet | Compatible phones or computers | Noise for live private chats; public broadcasts are not private; radio metadata remains visible | **Experimental** |
| [HF data modes](/kb/hf-data-modes/), illustrated by JS8Call | Long-distance radio under suitable propagation; low-bandwidth text and store-and-forward | HF radio, antenna and computer/audio connection | Do not treat amateur-radio traffic as a confidential channel; applicable rules matter | **Battle-tested** category; check the chosen mode and equipment |
| [Satellite IoT](/kb/satellite-iot/), illustrated by Iridium SBD | Global satellite service footprint; short packet messages | Compatible satellite modem and service plan | The cited SBD overview does not establish application end-to-end encryption | **Usable**, with operator and subscription dependencies |

## Trust model / threat model

Local radios avoid depending on a working internet path, but encrypted content does not make a transmitter unobservable. Bitchat's whitepaper specifically documents visible identity and routing metadata. Satellite connectivity depends on the operator's infrastructure even when local cellular service is absent.

For HF, licensing and content rules depend on the service and jurisdiction. As a concrete example, [US amateur-radio rules](https://www.ecfr.gov/current/title-47/chapter-I/subchapter-D/part-97/subpart-B/section-97.113) prohibit messages encoded to obscure their meaning, subject to specified exceptions. Do not transfer the private-channel assumptions of a different radio service to amateur HF.

## Readiness and limits

The labels match the individual entries. They describe implementation maturity, not coverage at your location. Before relying on a plan, test message delivery with internet disabled, normal device power settings, the intended antennas and the actual people who must receive it. Keep an alternative path and a meeting plan; start with [shutdown preparedness](/guides/internet-shutdown-preparedness/).

## Primary sources

- [Meshtastic introduction and radio model](https://meshtastic.org/docs/introduction/)
- [Meshtastic encryption and limits](https://meshtastic.org/docs/overview/encryption/)
- [MeshCore roles and routing FAQ](https://github.com/meshcore-dev/MeshCore/blob/main/docs/faq.md)
- [MeshCore encryption implementation](https://raw.githubusercontent.com/meshcore-dev/MeshCore/main/src/Utils.cpp)
- [Reticulum protocol and readiness](https://reticulum.network/manual/whatis.html)
- [Reticulum supported communications hardware](https://reticulum.network/manual/hardware.html)
- [Briar transport and security model](https://briarproject.org/how-it-works/)
- [Briar maintenance-mode announcement](https://briarproject.org/news/2026-maintenance-mode/)
- [Bitchat protocol and metadata limits](https://github.com/permissionlesstech/bitchat/blob/main/WHITEPAPER.md)
- [JS8Call project and radio workflow](https://js8call.com/)
- [US amateur-radio prohibited transmissions](https://www.ecfr.gov/current/title-47/chapter-I/subchapter-D/part-97/subpart-B/section-97.113)
- [Iridium Short Burst Data service](https://www.iridium.com/services/iridium-sbd/)
