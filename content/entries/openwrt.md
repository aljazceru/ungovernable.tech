---
title: "OpenWrt"
slug: openwrt
type: deep-dive
pillars: [endpoint, mesh]
readiness: usable
description: "OpenWrt replaces supported routers' firmware with a configurable Linux system. Check hardware, packages, upgrades, VPN and mesh uses, and trust."
dek: "Control the router's software, while taking responsibility for compatibility, configuration and updates."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [hardware-supply-chain-trust, batman-adv-and-cjdns, community-networks, running-freedom-infrastructure, startos, yunohost]
tags: [routers, firmware, openwrt, wireguard, mesh]
---

## Summary

[OpenWrt](https://openwrt.org/) is a Linux operating system for embedded devices, including supported routers. It provides a writable filesystem and package management instead of a fixed selection of vendor applications. The same router can be configured for ordinary internet access, a VPN connection or a role in a community network.

Replacing firmware is a hardware-specific operation. Start with the [Table of Hardware](https://openwrt.org/toh/start) and [Firmware Selector](https://firmware-selector.openwrt.org/), then read the installation instructions for the exact device and revision. The [canonical repository](https://github.com/openwrt/openwrt) directs users to those device-specific instructions.

## How it works

OpenWrt supplies the operating system and networking packages; LuCI provides a web administration interface. You select an image for the device, install it using that device's supported procedure, and configure the network and additional packages.

**Packages: check the release before copying commands.** The current stable release family is **25.12**, whose release notes document the switch from `opkg` to **`apk`**. Older 24.10 instructions use `opkg`; their command syntax is not interchangeable. This is confirmed by the [official release history](https://github.com/openwrt/openwrt/releases) and the [25.12 release notes](https://github.com/openwrt/openwrt/releases/tag/v25.12.0).

**Updates: plan for a firmware upgrade.** Attended Sysupgrade builds an image that includes the installed packages and supports retaining configuration. The 25.12 release includes its LuCI application by default; the command-line `owut` client is also available. Back up the configuration and read the release's device-specific exceptions before proceeding. A package install or package-list refresh is not a substitute for upgrading the firmware.

## VPN and mesh uses

OpenWrt's [LuCI WireGuard package](https://github.com/openwrt/luci/blob/master/protocols/luci-proto-wireguard/Makefile) provides support for configuring WireGuard VPN interfaces. Decide which peer should receive your traffic and which routes should use the tunnel; installing a package alone does not establish that policy.

For mesh networks, compare [B.A.T.M.A.N. advanced and cjdns](/kb/batman-adv-and-cjdns/) and the governance and deployment questions in [Community Networks](/kb/community-networks/). [LibreMesh](https://libremesh.org/) builds mesh firmware from OpenWrt and its own packages, with profiles for individual communities. Its [canonical repository](https://github.com/libremesh/lime-packages) explains the relationship and warns users to follow model-specific installation instructions. OpenWrt support alone does not establish that a router is suitable for a particular LibreMesh configuration.

## Trust model

You trust the OpenWrt build and package distribution, maintainers of the software you install, the router's hardware and lower-level firmware, and whoever administers it. Attended Sysupgrade adds a build service to that path: the client sends a package list and retrieves a customized image. Its [source repository](https://github.com/openwrt/asu) documents this service.

Open source makes these components inspectable. It does not demonstrate that an individual router is free of compromise. Keep administration access restricted and document how to recover the device if an upgrade or configuration change fails.

## Readiness

**Usable on supported hardware.** The project publishes stable firmware releases, supported-device information and upgrade tools. Suitability depends on the exact board, available storage and memory, drivers, and required network features. Check support before buying or flashing.

## Limits

Hardware support and upgrade paths vary. The release notes include devices that require special handling; do not assume every model can retain its configuration across a major upgrade. Custom firmware also does not remove dependencies on power, upstream connectivity or the hardware's own trust assumptions.

For the layers below the router operating system, see [Hardware and Firmware Supply-Chain Trust](/kb/hardware-supply-chain-trust/).

## Primary sources

- [OpenWrt canonical repository](https://github.com/openwrt/openwrt).
- [Table of Hardware](https://openwrt.org/toh/start) and [Firmware Selector](https://firmware-selector.openwrt.org/).
- [Official release history](https://github.com/openwrt/openwrt/releases) and [25.12 package-manager and upgrade changes](https://github.com/openwrt/openwrt/releases/tag/v25.12.0).
- [Attended Sysupgrade source and architecture](https://github.com/openwrt/asu).
- [LuCI WireGuard package definition](https://github.com/openwrt/luci/blob/master/protocols/luci-proto-wireguard/Makefile).
- [LibreMesh project](https://libremesh.org/) and [firmware packages](https://github.com/libremesh/lime-packages).
