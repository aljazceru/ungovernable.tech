---
title: "StartOS"
slug: startos
type: deep-dive
pillars: [endpoint, compute]
readiness: usable
description: "StartOS manages a personal server through a browser. Understand service installation, backups, updates, optional Tor access and operator trust."
dek: "A personal server interface for running services yourself, with the maintenance responsibilities made explicit."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [yunohost, openwrt, running-freedom-infrastructure, encrypting-files-and-backups, tor, hardware-supply-chain-trust]
tags: [self-hosting, servers, start9, startos]
---

## Summary

Start9's StartOS is a Linux-based operating system for a personal server. Its browser interface manages service installation, networking, backups and system administration. It moves those services onto a machine you administer; it does not remove the need to maintain that machine or understand each application's security.

Compare [YunoHost](/kb/yunohost/) for another approach to server administration, and [Running Freedom Infrastructure](/guides/running-freedom-infrastructure/) for deciding what to operate.

## How it works

The [Marketplace workflow](https://docs.start9.com/start-os/0.4.0.x/installing.html) installs packaged services. It includes Start9 and Community registries and permits additional registries. Services can also be installed from `.s9pk` files. A convenient installation format still leaves a trust decision: review the registry, package maintainer and application before installing it.

**Updates require action.** The [current update documentation](https://docs.start9.com/start-os/0.4.0.x/updating-startos.html) says operating-system and service updates are not automatic. Use the update interface, read the release notes and allow for the required restart. Assign someone responsibility for checking and applying updates.

**Backups require a separate destination.** StartOS can back up to an attached drive or a network folder. Its [backup documentation](https://docs.start9.com/start-os/0.4.0.x/backup-create.html) says backups are encrypted using the master password; backups made before a password change retain the old password. Save the necessary recovery information separately and test a restore before depending on the server.

Backup coverage is service-specific: a service can exclude files from its backup. Read the report and the service's own recovery instructions. The documented differential backup to the same target replaces the previous backup, so use separate targets when you need distinct recovery points.

## Remote access

The [current remote-access guide](https://docs.start9.com/start-os/0.4.0.x/remote-access.html) describes VPN, Tor and ordinary public-domain access, with different setup requirements.

**Tor is optional.** In the documented StartOS workflow, install the Tor service from the Marketplace, start it, and add an onion service to the relevant service interface. It is not included by default. The [Tor guide](https://docs.start9.com/start-os/0.4.0.x/tor.html) documents access without router port forwarding or a public DNS name. Clients still need a way to use Tor. See [Tor](/kb/tor/) for the transport's trust model.

Treat an onion address as a way to reach a service, and use the application's access controls for private data. Review which interfaces you expose and who should be able to use them.

## Trust model

You trust StartOS, the installed packages and their upstream software, the hardware, and the administrator. Adding a registry adds another source of software to evaluate. Running a service for someone else makes you part of that person's trust model.

Start9's [FAQ](https://start9.com/faq/) says the company does not have access to server data or encryption keys, but its registry can observe which IP addresses download which services. That claim is about Start9's access through its service; it is not a guarantee against a compromised application, administrator or endpoint.

## Readiness

**Usable.** Installation, service management, remote access and recovery are documented workflows. Match an individual service's requirements and backup behavior to your needs before moving important data into it.

## Limits

You remain responsible for availability, software updates, credentials and recoverable backups. A server at home depends on that home's power and connectivity. Tor reachability does not itself make every hosted application private. The FAQ also warns that its at-rest encryption should not be relied on against a sophisticated attacker with physical access.

Use [Encrypting Files, Disks and Backups](/guides/encrypting-files-and-backups/) to plan which data needs protection independently of the server.

## Primary sources

- [StartOS documentation](https://docs.start9.com/start-os/0.4.0.x/).
- [Start9 FAQ: Linux base, operator access and physical-security limits](https://start9.com/faq/).
- [Installing services and choosing registries](https://docs.start9.com/start-os/0.4.0.x/installing.html).
- [Updating StartOS](https://docs.start9.com/start-os/0.4.0.x/updating-startos.html).
- [Creating and protecting backups](https://docs.start9.com/start-os/0.4.0.x/backup-create.html).
- [Remote access](https://docs.start9.com/start-os/0.4.0.x/remote-access.html) and [Tor configuration](https://docs.start9.com/start-os/0.4.0.x/tor.html).
