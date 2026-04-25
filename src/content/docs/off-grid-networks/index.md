---
title: "05 — Off-Grid Networks"
tags:
  - "off-grid"
  - "mesh"
  - "lora"
  - "dtn"
---
This section covers communication systems that operate independently of the traditional internet — essential for disaster resilience, censorship resistance, and operational sovereignty.

---

## Key Files

### [Overview - Off-Grid Networks](/off-grid-networks/overview-off-grid-networks)

Comprehensive introduction to mesh networks, LoRa, DTN protocols, and overlay networks.

### Technologies *(planned)*

These deep-dives are referenced from the Overview but not yet written. Track in [CHANGELOG](/meta/changelog).

- Meshtastic deep dive
- Reticulum stack
- Yggdrasil and cjdns
- Briar
- Secure Scuttlebutt (SSB)

### Practical *(planned)*

- Hardware guide — recommended devices
- Setup guide — getting started
- DTN / DHT protocol details

---

## Technology Map

```
Off-Grid Networks
├── LoRa Mesh
│   ├── Meshtastic
│   └── Hardware
├── Secure Stack
│   ├── Reticulum
│   ├── LXMF
│   └── NomadNet
├── Overlay Networks
│   ├── Yggdrasil
│   └── cjdns
├── Delay-Tolerant
│   ├── Briar
│   └── SSB
└── Use Cases
    ├── Disaster
    ├── Privacy
    └── Resistance
```

---

## Key Statistics

| Technology | Users | Active Dev |
|------------|-------|-----------|
| Meshtastic | Thousands | Very active |
| Reticulum | Growing | Active |
| Yggdrasil | Moderate | Active |

---

## Use Cases

| Scenario | Recommended Tech |
|----------|-----------------|
| Local mesh | Meshtastic |
| Secure comms | Reticulum |
| Remote access | Yggdrasil |
| Offline messaging | Briar |
