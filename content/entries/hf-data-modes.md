---
title: "HF Radio Data Modes"
slug: hf-data-modes
type: deep-dive
pillars: ["mesh"]
readiness: battle-tested
description: "Text and email over shortwave radio, from Winlink to JS8Call and VARA: continental links that survive when the internet and local networks fail."
dek: "Amateur-radio data over high-frequency shortwave (3-30 MHz). Continental and intercontinental text and email links that survive when the internet, cellular, and satellite paths are gone, at the cost of bandwidth measured in kilobits per second and a regulatory regime that prohibits encryption on most amateur bands."
updated: 2026-04-26
created: 2026-04-26
origin: vault
source: "05-Off-Grid-Networks/HF Data Modes.md"
aliases: ["Amateur Radio Data", "HF Digital Modes", "Winlink", "JS8Call", "VARA HF"]
tags: ["hf", "amateur-radio", "winlink", "js8call", "vara", "fldigi", "off-grid", "ham-radio", "deep-dive"]
---

## What HF buys you

HF (high frequency, 3-30 MHz) propagates by ionospheric skywave. A 100-watt transmitter into a wire dipole can land a digital message on another continent without any infrastructure between sender and receiver. There is no ISP, no cell tower, no satellite gateway, no fiber.

That is the value proposition: a path independent of every other communications system. It is what polar expeditions, offshore sailors, and disaster volunteers fall back on when terrestrial and satellite paths fail.

The cost is bandwidth. The fastest amateur HF data modes peak around 9-12 kbps under ideal conditions and drop to a few hundred bits per second when the channel is poor. Throughput is more like 1980s telephone modems than modern data links.

## Regulatory context (and why encryption is mostly off the table)

Amateur ("ham") radio bands are licensed services in essentially every country. Operators take written exams and receive a callsign. Three classes apply in the US:

| Class | Privileges |
|-------|-----------|
| Technician | Mostly VHF/UHF; limited HF |
| General | Most HF allocations, full data privileges |
| Extra | All amateur privileges |

The CEPT system harmonizes amateur licensing across most of Europe and reciprocally with several non-EU countries.

The crucial constraint for security work: **47 CFR §97.113(a)(4)** in the US, and equivalent rules in most ITU jurisdictions, prohibit "messages encoded for the purpose of obscuring their meaning" on amateur bands. Authentication signatures and obfuscation for compression are tolerated; symmetric or public-key encryption of message content is not.

This is fundamentally different from MURS, GMRS, FRS, ISM, or Part 15 unlicensed services, where encryption is permitted (or in some cases mandated by the carrier protocol). In the US:

| Service | Encryption legal? |
|---------|--------------------|
| Amateur HF/VHF/UHF (Part 97) | No (content obfuscation prohibited) |
| MURS / GMRS / FRS | Voice yes (analog), commercial use restricted |
| ISM 433/868/915 MHz (Part 15) | Yes (LoRa, Meshtastic) |
| Citizens Band (Part 95) | No |

For privacy-sensitive traffic, the realistic threat model is: anyone within radio range, including state SIGINT, can read your HF data. Use HF for emergency coordination, position reports, and traffic that would already be plaintext on the public internet, not for confidential matter.

There are workarounds. Dual-licensed services (e.g. MARS in the US, or Part 90 commercial allocations with appropriate licensing) permit encryption. Non-amateur HF frequencies allocated to maritime mobile, aeronautical, or government use have their own rules.

## The major modes

### Winlink

Winlink is a global radio-email system operated by the Amateur Radio Safety Foundation. It is the closest thing amateur radio has to "internet over HF": users compose mail in a Winlink Express client, the client connects via radio to a Common Message Server (CMS) gateway, and the message goes onto the public internet as ordinary email. Reverse direction works the same way.

Architecture:

```
[User PC + radio] ── HF/VHF ── [RMS gateway] ── Internet ── [Winlink CMS] ── Internet/SMTP
```

- RMS Express / Winlink Express is the official Windows client; Pat is a cross-platform alternative.
- Gateways are run by volunteer operators worldwide; coverage is dense in North America and Europe, sparser elsewhere.
- Three transport protocols dominate: **Pactor** (Special Communications Systems hardware modem, the historical standard, expensive at $1,000+), **VARA HF** (soft-modem by ROS Electronics, dominant in 2025), and **ARDOP** (Amateur Radio Digital Open Protocol, fully open-source).
- Throughput: Pactor 4 ~5 kbps; VARA HF up to ~9 kbps in P3 mode; ARDOP closer to 1-3 kbps.

Use cases: emergency-services digital traffic (Winlink is integrated into US ARES/AUXCOMM and many national civil-defense systems), maritime mobile email for sailors, polar and backcountry email out.

Project home: [winlink.org](https://winlink.org). Open-source clients: [github.com/la5nta/pat](https://github.com/la5nta/pat).

### JS8Call

JS8Call is keyboard-to-keyboard weak-signal text. It is derived from Joe Taylor's FT8 protocol family, the same techniques that allow EME (moonbounce) and meteor-scatter contacts to work at S/N below the noise floor.

Where FT8 is purely a contest-contact protocol (callsign, grid square, signal report), JS8Call extends the modulation to carry arbitrary short text messages. A typical exchange happens at -10 to -20 dB S/N: a signal you cannot hear by ear at all decodes reliably to text.

- Throughput: ~16 baud "fast" mode, ~6 baud "normal," ~3 baud "slow." Realistically tens of bytes per minute.
- Network features: relay (a station can ask another station to forward), heartbeat (periodic presence beacon), inbox (messages stored at a relay until pickup).
- Open source: [github.com/jsherer/js8call](https://github.com/jsherer/js8call) (Jordan Sherer KN4CRD).

Best for: emergency check-ins, very long-range low-power work (QRP), polar/maritime when nothing else will close the link.

### VARA HF / VARA FM

VARA is a soft-modem (PC sound-card based) with both HF and FM variants, developed by Jose Alberto Nieto Ros (EA5HVK). It has become the de facto fast HF data mode for Winlink and for direct peer-to-peer.

- VARA HF: OFDM-based, adaptive bandwidth (500 Hz / 2.3 kHz), throughput up to ~9 kbps in good conditions.
- VARA FM: similar principles for VHF/UHF FM channels, up to ~25 kbps.
- Closed-source. The free version is bandwidth-limited; the full-speed version is paid (~$70 one-time).

The closed-source nature is a sore point for the open-source amateur community; ARDOP and FreeDATA are the alternatives.

### FLDIGI / FLAMP / FLMSG

FLDIGI is a multi-mode digital terminal supporting dozens of legacy and modern modes (PSK31, MFSK, Olivia, Contestia, Thor, etc.). FLAMP (Amateur Multicast Protocol) layers a broadcast file-transfer protocol on top: a sender transmits a file repeatedly with FEC; receivers listen passively and assemble blocks, requesting only specific absent segments.

FLAMP is unusual in being *broadcast-oriented*: one transmission feeds an arbitrary number of receivers, no acknowledgment required. That makes it useful for mass info distribution (situation reports, frequency lists, evacuation notices) where ARQ-style point-to-point protocols would saturate.

FLMSG is the structured-form companion (ICS-213, Red Cross forms, NTS messages) commonly used in amateur emergency-services traffic.

Project home: [w1hkj.com](http://www.w1hkj.com).

### FreeDATA

A newer fully open-source Winlink-class transport using a custom soft-modem: [github.com/DJ2LS/FreeDATA](https://github.com/DJ2LS/FreeDATA). Aims to provide VARA-equivalent performance without the closed-source dependency. As of 2026 still maturing.

## Comparison

| Mode | Throughput (good) | Throughput (poor) | Open source | Use |
|------|--------------------|--------------------|-------------|-----|
| Pactor 4 | ~5 kbps | ~0.3 kbps | No (HW modem) | Winlink, marine email |
| VARA HF | ~9 kbps | ~0.3 kbps | No (soft-modem, paid) | Winlink, P2P |
| ARDOP | ~3 kbps | ~0.2 kbps | Yes | Winlink, P2P |
| FreeDATA | ~3 kbps | ~0.2 kbps | Yes | P2P, Winlink experimental |
| JS8Call | ~30 bytes/min | text decodes at -20 dB | Yes | Weak-signal text |
| FLDIGI/Olivia | ~70 bps | works at -10 dB | Yes | Robust ragchew, broadcast |
| FLAMP | broadcast | tolerates loss via FEC + repeat | Yes | One-to-many file transfer |

## Trust and threat model

What HF amateur data does:

- Provides a path independent of internet, cellular, and satellite infrastructure.
- Survives many failure modes of those systems (jamming of GPS, fiber cuts, power outages, cellular network failure).
- Has a global volunteer operator base trained for emergency operations.

What HF amateur data does not:

- Does not provide content confidentiality. Any receiver in skip range can decode.
- Does not hide your callsign, your approximate location (via DF or grid-square exchange), or your traffic patterns.
- Does not scale beyond very low data rates. Voice or video are not on the table.

Threat-model honesty: HF data is observable by every adversary with a receiver and a sound card. Treat the channel as an open postcard. The right uses are:

- Emergency coordination where the alternative is no communication at all.
- Position reports and welfare traffic.
- Distribution of public information (weather, evacuation orders).
- Logistics traffic that would already be unencrypted email.

Where confidentiality matters and the regulatory regime forbids encryption, HF amateur is not a fit. Use Iridium SBD (commercial, encrypted by user), [Reticulum](/kb/reticulum/) over Tor (when an internet path exists), or pre-shared physical signal codes.

## Hardware

A workable HF data station:

- Transceiver: Yaesu FT-891 (~$650), Icom IC-7300 (~$1,000), or used Kenwood TS-590 / Yaesu FT-857. Anything covering 80 m through 10 m at 100 W will do.
- Antenna: end-fed half-wave, dipole, or magnetic loop. The single biggest determinant of station performance.
- Sound-card interface: SignaLink USB, Digirig, or a built-in USB sound card on modern radios.
- Computer: anything running Windows for VARA / Winlink Express, or Linux for Pat / FLDIGI / JS8Call.
- Power: 13.8 V DC, 25 A. A small LiFePO4 battery and a solar panel make a self-contained station.

A complete portable HF data setup fits in a backpack at 7-10 kg.

## Deployment status

- Winlink: tens of thousands of active users globally, hundreds of RMS gateways. Heavy emergency-services and maritime use. ARRL and Red Cross integrations.
- JS8Call: niche, dedicated user base in the low thousands; very active in QRP/emcomm circles.
- VARA: dominant in Winlink as of 2025-2026.
- FreeDATA: small but growing as an open-source escape hatch from VARA.

## Primary sources

- 47 CFR §97.113 — US amateur radio prohibitions on encrypted communications. [ecfr.gov/current/title-47/chapter-I/subchapter-D/part-97](https://www.ecfr.gov/current/title-47/chapter-I/subchapter-D/part-97)
- ITU Radio Regulations, Article 25 — international amateur service definitions.
- Winlink Global Radio Email — [winlink.org](https://winlink.org).
- Pat (open Winlink client) — [github.com/la5nta/pat](https://github.com/la5nta/pat).
- JS8Call — [github.com/jsherer/js8call](https://github.com/jsherer/js8call); KN4CRD.
- WSJT-X family (FT8/FT4 origins) — [wsjt.sourceforge.io](https://wsjt.sourceforge.io); Joe Taylor K1JT.
- VARA HF/FM — [rosmodem.wordpress.com](https://rosmodem.wordpress.com); EA5HVK.
- FLDIGI / FLAMP / FLMSG — [w1hkj.com](http://www.w1hkj.com).
- FreeDATA — [github.com/DJ2LS/FreeDATA](https://github.com/DJ2LS/FreeDATA).
- ARDOP specification — [github.com/pflarue/ardop](https://github.com/pflarue/ardop).
