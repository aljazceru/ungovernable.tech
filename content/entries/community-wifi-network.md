---
title: "Build a community Wi-Fi network"
slug: community-wifi-network
type: guide
pillars: ["mesh"]
readiness: usable
description: "Plan a small community Wi-Fi network with OpenWrt and LibreMesh, including hardware checks, backhaul, shared administration and outage tests."
dek: "Begin with a small, maintainable network whose local services still have a purpose when the upstream connection fails."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: ["community-networks", "libremesh", "batman-adv-and-cjdns", "building-a-mesh", "resilient-infrastructure"]
level: intermediate
---

## Summary

This guide is a planning and commissioning workflow for a small shared Wi-Fi network. [OpenWrt](https://github.com/openwrt/openwrt) provides the router operating system; [LibreMesh](/kb/libremesh/) supplies community-oriented packages and configuration. The people, sites and maintenance agreement are part of the design: start with [community networks](/kb/community-networks/).

## 1. Agree on the service

Write down who will use the network, the places it must cover, which local services matter, and whether internet access is part of the promise. Name the people responsible for power, firmware updates, equipment replacement and support. Agree how configuration changes will be reviewed and how users can report a failure.

## 2. Survey sites and backhaul

Draw the proposed nodes, wired links, radio links and internet gateways. Test candidate links at the intended mounting positions before buying the full set of equipment. Identify where power and upstream connectivity come from, and whether losing either disconnects a whole area.

Separate **local connectivity** from **backhaul**, the connection onward to another network or the internet. Test local services with the upstream gateway disconnected. Keep an alternative way for maintainers to communicate during that test.

## 3. Select and prepare hardware

LibreMesh's getting-started guide requires checking OpenWrt support and device-specific flashing instructions. Match the exact hardware revision, not just a product-family name. Check recovery instructions and keep a known-good configuration before changing firmware.

The LibreMesh package guide documents radio-driver limitations and reduced configurations for small devices. Use that evidence when selecting hardware; do not promise a universal range or throughput from the firmware name alone.

## 4. Configure a small pilot

Start with a few nodes you can physically reach. LibreMesh documents BATMAN-adv for local layer-2 mesh areas and Babel for layer-3 routing. Its configuration layers distinguish community settings from node settings; keep the shared profile under version control and record device-specific changes.

Set administrative credentials, decide which interfaces provide client access and which carry mesh traffic, and document gateway and DNS choices. Keep application confidentiality as a separate requirement from routing. Compare [BATMAN-adv and cjdns](/kb/batman-adv-and-cjdns/) before changing the architecture.

## 5. Check permissions and operating rules

Confirm permission to mount equipment, local channel and transmit-power requirements, and the upstream provider's sharing terms. Resolve these questions before connecting neighbours. This guide does not assume one jurisdiction's radio or telecommunications rules apply everywhere.

## 6. Commission and maintain

Record client connectivity, local-service reachability and upstream reachability separately. Reboot nodes, disconnect one link at a time, restore configuration from backup, and check that someone besides the original installer can recover the pilot. Expand only after the intended services and recovery procedure work.

## Trust model / threat model

Network administrators and gateway operators remain operational dependencies. Agree who can change routing, inspect logs and recover access. Use [resilient infrastructure](/guides/resilient-infrastructure/) to plan beyond a single administrator or power source.

## Readiness and limits

**Usable.** The firmware and configuration mechanisms are documented; coverage and resilience must be established at the actual sites. For low-bandwidth radio alongside Wi-Fi, compare [Meshtastic](/kb/meshtastic/) and [MeshCore](/kb/meshcore/) in [Building a mesh](/guides/building-a-mesh/).

## Primary sources

- [OpenWrt project and router operating system](https://github.com/openwrt/openwrt)
- [LibreMesh installation and hardware checks](https://libremesh.org/getting-started.html)
- [LibreMesh routing architecture](https://libremesh.org/what-is-libremesh.html)
- [LibreMesh package and driver considerations](https://libremesh.org/guide/packages-selection.html)
- [LibreMesh community and node configuration](https://libremesh.org/reference/configuration.html)
