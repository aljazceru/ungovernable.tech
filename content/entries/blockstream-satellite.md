---
title: "Blockstream Satellite"
slug: blockstream-satellite
type: explainer
pillars: [money, circumvention]
readiness: usable
description: "Blockstream Satellite broadcasts Bitcoin data without an internet connection. Understand receiver hardware, coverage and the one-way link's limits."
dek: "Receive the Bitcoin blockchain from space; sending a transaction still needs a separate connection."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [bitcoin-self-custody, financial-sovereignty, internet-shutdown-preparedness, resilient-infrastructure]
tags: [bitcoin, satellite, connectivity, censorship-resistance]
---

## Summary

Blockstream Satellite broadcasts Bitcoin blockchain data over satellite. A receiver in coverage can keep a node synchronised without an internet connection. The service broadcasts the full block history as well as new blocks, so it can also support initial synchronisation.

## How it works

Blockstream ground stations transmit data to satellites, which broadcast it to receivers. A local setup needs an appropriately aligned antenna, compatible receiving hardware and software. The official guide covers coverage checks, equipment and Bitcoin Satellite, the client that handles the satellite data feed.

## Trust model / threat model

This gives a node another way to receive data when terrestrial connectivity fails. Reception still depends on Blockstream's broadcast infrastructure, satellite coverage and a usable signal. It does not provide an independent guarantee that the broadcaster will remain available.

## Readiness

**Usable.** The service publishes coverage information and setup instructions. Check the local line of sight and hardware requirements before treating it as an outage plan. The broadcast is free to receive; the equipment is not supplied by that claim.

## Limits

The satellite link is **receive-only**. A receiving dish cannot broadcast a new Bitcoin transaction back to the network; an internet connection or another outbound route is still needed. Weather or obstructions can disrupt reception. Satellite reception alone therefore does not provide complete offline payment connectivity.

Use it alongside a [Bitcoin self-custody setup](/guides/bitcoin-self-custody/) and broader [shutdown preparation](/guides/internet-shutdown-preparedness/).

## Primary sources

- [Blockstream Satellite: broadcast service, coverage and ground stations](https://blockstream.com/satellite/).
- [Official receiver guide: hardware and synchronisation from block history](https://blockstream.github.io/satellite/).
- [Blockstream FAQ: one-way reception and signal losses](https://help.blockstream.com/blockstream-satellite/faqs/how-does-blockstream-satellite-bitcoin-data-differ-from-regular-bitcoin-data).
