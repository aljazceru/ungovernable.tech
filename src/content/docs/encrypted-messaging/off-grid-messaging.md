---
title: "Off-Grid Messaging"
tags:
  - "off-grid"
  - "messaging"
  - "briar"
  - "meshtastic"
  - "reticulum"
  - "lxmf"
  - "deep-dive"
---
*Communication that survives when the internet doesn't. Mesh radios, peer-to-peer over Bluetooth, store-and-forward bundles, and human couriers.*

> Pairs with [Overview - Off-Grid Networks](/off-grid-networks) (transport layer) and [Overview - Encrypted Messaging](/encrypted-messaging) (security model).

---

## Why it matters

The internet has many choke points: ISPs, cloud providers, CAs, governments. Off-grid messaging assumes those have failed (by censorship, infrastructure damage, or power loss) and asks whether people can still communicate.

Threats addressed:

- Internet shutdowns (Iran, Belarus, Cuba, Myanmar — recurring).
- Disaster scenarios where centralized infrastructure is offline.
- Surveillance environments where any internet contact is logged.
- Physical occupation where the only safe channel is short-range.

---

## Approach families

### 1. LoRa Mesh (Meshtastic)

LoRa radios on 868 / 915 MHz ISM bands provide kilometers of range at low bandwidth. Meshtastic firmware turns devices into a self-organizing mesh:

- Range: 1-10 km line-of-sight, 30+ km from elevation.
- Throughput: 100-1500 bytes/sec depending on settings.
- Power: multi-day battery; solar-friendly.
- Crypto: AES-256 channel encryption (shared key per channel).

Use cases: hiking groups, neighborhood resilience networks, festival comms, emergency channels. It doesn't replace the internet; it provides a graceful-degradation channel when the internet is gone.

### 2. Reticulum + LXMF

Reticulum is a generic encrypted-by-default mesh networking stack (Markqvist) supporting LoRa, packet radio, TCP, serial. LXMF is its message format. It's like email but built on Reticulum's identity model, where each user is a public key.

Properties:

- End-to-end encrypted (Curve25519 + AES) by stack design.
- Store-and-forward: propagating nodes hold messages until the recipient is reachable.
- Identity is the key, the same as Tor v3, Nostr, PKARR.
- Heterogeneous transport: runs over anything that delivers bytes.

Tooling: NomadNet (terminal UI), Sideband (cross-platform messenger), MeshChat.

### 3. Briar (P2P over Bluetooth / Wi-Fi / Tor)

Designed for activists and journalists in adversarial conditions. Three transports:

- Bluetooth: short-range, no infrastructure, no logs.
- Wi-Fi direct / hotspot: faster, slightly longer range.
- Tor onion services: when the internet exists.

The same client uses all three transparently. A user can switch between modes as the threat environment changes. Briar Mailbox lets messages queue while peers are offline.

### 4. Bluetooth-mesh apps

- Bitchat: modern BLE mesh from Permissionlesstech with Nostr fallback. Phone-only, multi-hop (up to 7), Noise-encrypted. iOS / macOS / Android. See [Bitchat](/off-grid-networks/bitchat).
- Bridgefy: Bluetooth mesh; used in protests in Hong Kong (2019) and Belarus (2020). Cryptographic concerns surfaced in 2020 audits; updated since.
- AirChat / Apple Find My abuse: research projects using Bluetooth advertising for opportunistic tiny messages.

### 5. Long-range HF / packet radio

- JS8Call: keyboard-to-keyboard chat over HF radio (3-30 MHz). Truly intercontinental, very low bandwidth.
- AX.25 packet radio: legacy ham digital mode; slow but survives anything.
- Reticulum over HF: emerging, combines RNS encryption with HF range.

Requires an amateur radio license in most jurisdictions for legal operation; the threshold model in extremis differs.

---

## Comparing range vs throughput

| Approach | Range (typ.) | Throughput | Power | Infra-free? |
|----------|-------------|-----------|-------|-------------|
| Bluetooth mesh | 10-100 m | Mbit/s | Phone battery | Yes |
| Wi-Fi Direct | 50-200 m | 10-100 Mbit/s | Phone battery | Yes |
| LoRa Mesh | 1-30 km | 0.3-50 kbit/s | Multi-day | Yes |
| Reticulum on LoRa | Same as LoRa | Same | Same | Yes |
| Reticulum on TCP | Internet range | Link-limited | Server | Needs internet |
| HF packet radio | Global | 50-1200 baud | License needed | Yes |
| Briar via Tor | Internet range | TCP-limited | Phone battery | Needs internet |

---

## Threat model considerations

Off-grid messaging has *different* threats from internet-based messaging:

- Direction-finding (DF). Active radios are locatable. LoRa transmissions can be triangulated. Mitigations: low duty cycle, mobile transmitters, secure-by-design protocols that don't disclose source until needed.
- Capture of nodes. Physical compromise reveals stored messages and keys. Mitigations: encrypted storage, ephemeral keys, no message history retention (Briar's default).
- Mesh-flood DoS. Spam in a low-bandwidth mesh saturates it. Mitigations: rate limiting, proof-of-work, paid-relay variants.
- Sybil at the routing layer. Adversary floods mesh with fake nodes to deny service or surveil. Mitigations: cryptographic node identity, web-of-trust admission.
- Endpoint compromise. Same as everywhere; harder when the endpoint is a small embedded device with limited security primitives.

---

## Operational patterns

### Disaster resilience kit

```
- 2× LoRa Meshtastic devices per household
- Solar charging
- Pre-shared channel keys distributed in person
- Offline maps and predefined fallback rendezvous
- Reticulum / LXMF for richer messaging if smartphones survive
```

### Activist comms in shutdown

```
- Briar with Bluetooth + Tor
- Distributed channel keys via QR
- Pre-arranged identity rotation
- Briar Mailbox or trusted host as async store
```

### Pseudonymous community network

```
- Reticulum nodes (Raspberry Pi + LoRa hat)
- LXMF accounts as identity
- Cross-community gateways via internet when available
```

---

## Trade-offs

### Strengths

- Survives infrastructure failure. No internet, no cloud, no DNS dependency.
- No external observers. A LoRa mesh is invisible to non-participants without DF gear.
- Cheap. $30 LoRa devices, free open-source firmware.

### Limitations

- Bandwidth is brutal. A few kbit/s caps app design — text only, no media.
- Range is uneven. Topography, weather, foliage all affect link quality.
- Latency. Store-and-forward adds delay; not for synchronous chat.
- Discovery and bootstrapping. Out-of-band contact establishment is mandatory.
- DF risk. Active radios are physically locatable.

---

## Related Files

- [Overview - Off-Grid Networks](/off-grid-networks)
- [Overview - Encrypted Messaging](/encrypted-messaging)
- [Metadata Resistance](/encrypted-messaging/metadata-resistance)
- [MOC - Censorship Resistance](/meta/moc-censorship-resistance)

---

## Primary Sources

- Meshtastic — [meshtastic.org](https://meshtastic.org); [github.com/meshtastic](https://github.com/meshtastic)
- Reticulum / RNS — [reticulum.network](https://reticulum.network); [github.com/markqvist/Reticulum](https://github.com/markqvist/Reticulum)
- LXMF — [github.com/markqvist/LXMF](https://github.com/markqvist/LXMF)
- Briar — [briarproject.org](https://briarproject.org)
- Bridgefy security audit, *Mesh-based messaging app cryptography*, 2020.

