---
title: "LibreMesh"
slug: libremesh
type: deep-dive
pillars: ["mesh"]
readiness: usable
description: "LibreMesh builds community mesh firmware on OpenWrt. Learn how BATMAN-adv and Babel connect routers, and what network operators must manage."
dek: "Community firmware combines local roaming and routed links; the people running gateways still matter."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: ["community-networks", "batman-adv-and-cjdns", "building-a-mesh", "off-grid-networks"]
---

## Summary

LibreMesh is a collection of OpenWrt packages and firmware tools for community networks. It combines a local mesh with routing between mesh areas, with community-wide and device-specific configuration. See [community networks](/kb/community-networks/) for the ownership and maintenance questions behind the firmware.

## How it works

The documented architecture has two layers. **BATMAN-adv** joins a local mesh into a layer-2 broadcast domain, so it behaves like a shared LAN. **Babel** supplies layer-3 routing between these areas. The project describes this separation as a way to support local roaming while connecting a larger network. Compare [BATMAN-adv and cjdns](/kb/batman-adv-and-cjdns/).

Configuration comes from `/etc/config/lime-*` files. The documented merge order distinguishes defaults, community settings, node settings and generated settings. This makes a shared network profile possible without pretending every router has the same interfaces or role.

## Trust model / threat model

Choose who can change the community profile, administer routers and operate internet gateways. Mesh routing does not by itself establish a confidentiality policy for users' applications. Keep sensitive services encrypted and separate administrative access from public client access.

## Readiness

**Usable.** LibreMesh publishes installation instructions, package selection guidance and firmware tooling. Hardware selection remains device-specific: the getting-started guide tells operators to check OpenWrt support and the installation instructions for the exact router before flashing it.

## Limits

Firmware cannot replace a coverage survey, power planning or someone able to recover a failed node. The package guide documents radio-driver constraints and reduced configurations for limited hardware; do not assume all OpenWrt-supported routers make equally suitable mesh nodes.

For a deployment workflow, follow [Build a community Wi-Fi network](/guides/community-wifi-network/). For separate low-bandwidth radio options, compare [Meshtastic](/kb/meshtastic/) and [MeshCore](/kb/meshcore/) in [Building a mesh](/guides/building-a-mesh/).

## Primary sources

- [LibreMesh architecture: BATMAN-adv and Babel](https://libremesh.org/what-is-libremesh.html)
- [Installation and hardware prerequisites](https://libremesh.org/getting-started.html)
- [Package selection and driver constraints](https://libremesh.org/guide/packages-selection.html)
- [Configuration layers](https://libremesh.org/reference/configuration.html)
- [OpenWrt packages and firmware build instructions](https://github.com/libremesh/lime-packages)
