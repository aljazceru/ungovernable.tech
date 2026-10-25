---
title: "APRS"
slug: aprs
type: deep-dive
pillars: ["mesh"]
readiness: usable
description: "APRS shares amateur-radio position and status packets through digipeaters and internet gateways. Understand its public data and operating limits."
dek: "Amateur packet reporting is useful for shared situational awareness; plan for positions and messages to be public."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: ["hf-data-modes", "off-grid-networks", "meshtastic", "meshcore", "satellite-iot"]
---

## Summary

The Automatic Packet Reporting System (APRS) carries amateur-radio information such as positions, status, messages and telemetry. A **digipeater** repeats radio packets; an **IGate** connects radio traffic to the APRS Internet Service (APRS-IS). These roles extend distribution, including beyond the area where a packet was transmitted.

## How it works

Dire Wolf's implementation provides an AX.25 packet modem and supports APRS digipeater and IGate operation. APRS-IS documents a network of servers to which client software can connect. Its IGate rules describe forwarding eligible received radio packets to the internet and selectively returning messages and associated positions to radio.

That is a different service from a private group messenger. A receiver or internet client can consume the shared reports; APRS-IS even requires clients to consider that injected packets may be gated onto radio.

## Trust model / threat model

Assume a transmitted position can be observed, copied and retained beyond the intended local group. A gateway's decision about forwarding is not a confidentiality boundary. Do not publish a location that must remain private, and do not rely on a callsign field alone as cryptographic authentication.

In the United States, **47 CFR 97.113(a)(4)** prohibits messages encoded to obscure their meaning on amateur stations, with exceptions elsewhere in the rules. That makes ordinary encrypted private messaging unsuitable for amateur-band APRS operation. This is a U.S. rule, not a claim that every jurisdiction has identical wording; check the rules for the station and band you will use.

## Readiness

**Usable.** Packet software and APRS-IS interfaces are documented and available. A working local deployment still depends on compatible radio equipment, configuration, coverage and lawful operation.

## Limits

Do not assume a digipeater or internet gateway is present where you need it, or that a message was delivered merely because it was transmitted. For other radio choices, read [HF data modes](/kb/hf-data-modes/) and compare [Meshtastic](/kb/meshtastic/) with [MeshCore](/kb/meshcore/). For commercial satellite messaging, see [satellite IoT](/kb/satellite-iot/).

## Primary sources

- [Dire Wolf packet modem, APRS digipeater and IGate implementation](https://github.com/wb2osz/direwolf)
- [APRS-IS service and public feed](https://www.aprs-is.net/)
- [IGate forwarding rules](https://www.aprs-is.net/IGateDetails.aspx)
- [Connecting software to APRS-IS](https://www.aprs-is.net/Connecting.aspx)
- [eCFR: 47 CFR 97.113, prohibited transmissions](https://www.ecfr.gov/current/title-47/chapter-I/subchapter-D/part-97/subpart-B/section-97.113)
