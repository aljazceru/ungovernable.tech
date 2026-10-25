---
title: "Satellite IoT and Direct-to-Device Links"
slug: satellite-iot
type: deep-dive
pillars: ["mesh"]
readiness: usable
description: "Narrowband data over satellite constellations and direct-to-phone links: short messages and telemetry from anywhere, and who controls them."
dek: "Narrowband data over commercial satellite constellations: short text messages, position pings, telemetry. The category covers Iridium Short Burst Data, Globalstar (powering Apple Emergency SOS), Swarm (about to be decommissioned), Astrocast, and Lacuna Space. Distinct from satellite broadband (Starlink, OneWeb) and from amateur HF data — the niche is \"a few hundred bytes per message, anywhere on Earth, no terrestrial infrastructure required.\""
updated: 2026-04-26
created: 2026-04-26
origin: vault
source: "05-Off-Grid-Networks/Satellite IoT.md"
aliases: ["Satellite Messaging", "Iridium SBD", "Globalstar", "Swarm", "Astrocast", "Lacuna Space"]
tags: ["satellite", "iridium", "globalstar", "swarm", "astrocast", "lacuna", "lorawan", "m2m", "off-grid", "deep-dive"]
---

## What this category isn't

To set scope cleanly:

- **Not Starlink, OneWeb, Kuiper.** Those are LEO broadband — tens of Mbps with a pizza-box terminal. Different power budget, different cost, different threat model.
- **Not amateur HF data.** [HF Data Modes](/kb/hf-data-modes/) use ionospheric skywave with no per-message fee. Satellite IoT uses commercial constellations with subscriptions.
- **Not direct-to-cell.** Apple iPhone 14+ Emergency SOS via satellite is a specific Globalstar implementation; Starlink/T-Mobile direct-to-cell is a different (broader-bandwidth) product.

Satellite IoT is for: a remote sensor that needs to phone home a few times a day, a hiker who wants to send "I'm OK" from the backcountry, a sailor outside cellular range, a logistics asset reporting location across an ocean.

## The constellations

### Iridium

Iridium operates 66 LEO satellites in cross-linked polar orbits — the only constellation with true global coverage including the poles. Originally deployed 1997-1998, near-bankrupt 2000, rebuilt as Iridium NEXT 2017-2019.

Two relevant services:

- **Iridium Short Burst Data (SBD)** — store-and-forward 340-byte messages either direction. Standard latency ~10-20 seconds when a satellite is overhead. Used by Garmin inReach, ZOLEO, RockBLOCK modules ([rock7.com](https://www.rock7.com/products/rockblock-9603-compact-plug-and-play-satellite-transmitter)), and most marine and aviation tracking devices.
- **Iridium Certus** — broadband (up to ~700 kbps), different terminal class, used by maritime and government.

Pricing for SBD via consumer products like Garmin inReach: $15-65/month for various message-volume tiers. Direct via RockBLOCK: ~$0.12 per message plus a monthly line rental.

Coverage: truly global, including poles, oceans, and mid-Pacific.

### Globalstar

Globalstar's constellation (24 LEO satellites) is the carrier behind:

- **Apple iPhone 14+ Emergency SOS via satellite** (2022 onwards). Free for two years from device activation, then a paid subscription that Apple has been extending. The phone has a custom Globalstar antenna; messages route through Globalstar to terrestrial gateways, then to dispatch services.
- **SPOT** trackers — older consumer devices for hiking and adventure, one-way and two-way variants.
- Various B2B IoT services.

Coverage: most of the populated world but not the poles. Real-world latency ~30-60 seconds.

The Apple deal (announced 2022, extended 2023-2024) effectively put Globalstar in 100M+ pockets and made satellite SOS a default consumer expectation.

### Swarm — winding down

Swarm Technologies launched a constellation of small (sandwich-sized) satellites starting 2018. Notable for:

- Aggressive pricing: $5/month for ~750 short messages, $119 for the M138 ground modem.
- Tiny ground modules, low power, simple UART interface.
- Acquired by SpaceX in **August 2021**.

In **April 2024 SpaceX announced Swarm would be decommissioned**, with service ending in stages through 2025-2026. Existing satellites are being deorbited, gateways are being shut down. The customer story is migration to Starlink direct-to-cell or to other narrowband providers.

If you read older off-grid documentation that recommends Swarm, that recommendation is no longer current. The constellation is going away.

### Astrocast

Astrocast is a Swiss operator running a small constellation (~10-20 cubesats) at low altitude. Their protocol is custom and L-band-based, similar in spirit to LoRaWAN (low duty cycle, narrowband, asynchronous). Modules cost ~$50-100; service plans start under $1/month for very low volume.

Targeting industrial M2M: agriculture, oil and gas, asset tracking. Coverage: not continuous; messages are queued and delivered when a satellite passes overhead, latency from minutes to hours.

Project: [astrocast.com](https://astrocast.com).

### Lacuna Space

Lacuna runs a small LEO constellation that listens for **standard LoRaWAN uplinks**. A LoRaWAN sensor that already works on the ground also reaches Lacuna's satellites with the same modem and same firmware — just with the sat-side gateway in orbit instead of on a tower.

This is a fundamentally different go-to-market: instead of selling a proprietary radio, Lacuna sells coverage for the radios that the LPWAN ecosystem already shipped. Power-efficient, cheap modems ($5-15), but very low data rate (a few hundred bytes per pass).

Project: [lacuna.space](https://lacuna.space).

### Other operators (briefly)

- **Inmarsat** — older GEO constellation (3 high-orbit sats), longer latency, used by maritime industry. BGAN service for higher data rate.
- **Orbcomm** — long-running M2M operator, used in fleet tracking; less consumer-visible.
- **Hiber** — Dutch IoT cubesat operator, paused operations 2022.
- **Sateliot** — Spanish 5G NB-IoT-via-satellite operator, in deployment 2024-2026.

## Comparison

| Provider | Coverage | Latency | Per-message cost | Open ecosystem |
|----------|----------|---------|--------------------|----------------|
| Iridium SBD | Global incl. poles | ~10-20 s | ~$0.12 | Modules available (RockBLOCK) |
| Globalstar (iPhone SOS) | Most populated | ~30-60 s | Bundled with iPhone | Closed |
| Globalstar SPOT | Most populated | ~minutes | $15-30/mo | Consumer hardware only |
| Swarm | Was global ex-poles | ~hours | $5/mo (DEPRECATED) | Was open |
| Astrocast | Most populated | ~minutes-hours | <$1/mo low volume | Modules available |
| Lacuna Space | Most populated | ~hours | LoRaWAN economics | Yes (LoRaWAN standard) |

## How payload encryption sits

This matters and is often glossed over: the satellite operator sees all metadata. Source identity, destination, time, message size, often message content unless the user encrypts.

| Layer | Visible to operator? |
|-------|------------------------|
| Modem ID / IMEI / device serial | Yes (it's the routing identifier) |
| Sender/recipient gateway addresses | Yes |
| Timestamp | Yes |
| Approximate location | Yes (which satellite spot beam saw the uplink) |
| Payload bytes | Yes, unless app-level encryption is applied |

For a Garmin inReach or ZOLEO, the consumer sees their messages routed through the manufacturer's portal, then to SMS / email. The portal sees plaintext unless you encrypt above it. The "Iridium sees plaintext" point is the same.

If confidentiality matters: encrypt the payload before passing it to the modem. A 340-byte SBD slot easily holds a Curve25519+AES-GCM ciphertext of a 100-byte message. PGP-encoded text fits when compressed. This is purely an application-layer concern; the constellation is a transport.

The metadata — that you sent a message at a certain time from approximately some location — cannot be hidden. The constellations track it as part of operating the network.

## Threat model

What satellite IoT does:

- Provides global reach without local infrastructure.
- Survives terrestrial outages: cellular, internet, fiber cuts, power.
- Works (mostly) under hostile RF conditions where cellular gets jammed selectively but satellite frequencies are harder to jam locally.

What it doesn't:

- Operator can comply with subpoenas, lawful intercept requests, and most US-jurisdictional pressure (Iridium, Globalstar, SpaceX/Swarm are US companies; Astrocast is Swiss; Lacuna is Dutch — jurisdiction varies).
- Operator can disable a device's account; service is permissioned.
- The satellite uplink is an RF signal; broad-area direction-finding by capable adversaries is feasible.
- Encryption of payload is on you. Default products (Garmin inReach, etc.) do not E2E-encrypt user content from the operator's portal.

If your threat model is "I want a state-resistant communication channel," satellite IoT is one transport in a stack — with payload encryption layered on top — not a complete answer. If your threat model is "the internet went down in my country and I need to reach the outside world," it is excellent for what it is.

## When to use which

- **Two-way messaging in the global backcountry, including poles:** Iridium SBD via Garmin inReach or ZOLEO. The reference choice for serious expedition use.
- **Emergency SOS from a smartphone you already own:** Apple iPhone 14+ (Globalstar) or, increasingly, Android phones with Snapdragon Satellite (Iridium-backed) and Samsung's emerging direct-to-cell. Free or cheap, low-friction.
- **Battery-powered sensor reporting once or twice a day:** Astrocast (custom modem) or Lacuna Space (LoRaWAN modem). Cheaper than Iridium per-message at low volume.
- **You were planning to use Swarm:** don't. Pick another provider (constellation winding down).
- **You need broadband, not narrowband:** Starlink Mini or Iridium Certus, depending on power budget and latency tolerance.

## Combining with other off-grid tools

A typical layered off-grid stack:

```
Local mesh ── LoRa ── [Meshtastic] ── Bluetooth ── Phone with sat modem ── Iridium SBD
```

Or:

```
[Reticulum over LoRa] ── gateway node ── [Reticulum over Iridium SBD]
```

Reticulum's transport-agnostic design ([Reticulum](/kb/reticulum/)) makes it natural to bridge a local LoRa mesh to a satellite SBD link. Encryption is handled by Reticulum end-to-end; the satellite operator carries opaque ciphertext.

For HF as an alternative (no per-message fee, no operator dependence, but no encryption legally allowed on amateur bands), see [HF Data Modes](/kb/hf-data-modes/).

## Ecosystem realism

- Costs are not trivial for high-volume use. A device pinging position every 10 minutes can cost $50-200/month.
- Modems use real power. Iridium SBD transmits at a few watts; sustained polling drains batteries that last forever in low-power LoRa mode.
- "Always-on" is not the operating model. Send when you have something to send.
- Two-way latency varies hugely. Iridium ~10-20 s; Astrocast / Lacuna can be hours.
- Globalstar/Apple Emergency SOS is genuinely lifesaving for the case it covers (lost in mountains, can't make a call) but is not a free messenger replacement.

## Primary sources

- Iridium Short Burst Data — [iridium.com/services/sbd](https://www.iridium.com/services/sbd).
- Garmin inReach product line — [garmin.com/en-US/c/sports-fitness/inreach-satellite-communicators](https://www.garmin.com).
- ZOLEO — [zoleo.com](https://www.zoleo.com).
- RockBLOCK 9603 module — [rock7.com](https://www.rock7.com).
- Globalstar — [globalstar.com](https://www.globalstar.com).
- Apple Emergency SOS via satellite — [apple.com/newsroom/2022/11/emergency-sos-via-satellite-makes-its-debut-today-on-the-iphone-14-lineup](https://www.apple.com/newsroom).
- Swarm acquisition by SpaceX (August 2021) and decommissioning announcement (April 2024) — [spacenews.com](https://spacenews.com) coverage; Swarm operator notices.
- Astrocast — [astrocast.com](https://astrocast.com).
- Lacuna Space — [lacuna.space](https://lacuna.space). LoRaWAN spec — [lora-alliance.org](https://lora-alliance.org).
- Inmarsat BGAN, Orbcomm, Sateliot — operator websites.

Continue with [Satellite broadband and direct-to-cell](/kb/satellite-broadband/).
