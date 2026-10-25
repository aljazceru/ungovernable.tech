---
title: "Resilient and Relocatable Infrastructure"
slug: resilient-infrastructure
type: guide
pillars: [anonymity, mesh]
description: "Running a relay, node or server that keeps working through outages, seizure and censorship: redundancy, geographic spread, encrypted backups and portability."
dek: "The networks on this site are only as strong as the infrastructure behind them. Here is how to run yours so that losing any one machine, provider or jurisdiction does not take it down."
updated: 2026-10-18
created: 2026-10-18
origin: original
level: intermediate
time: "a weekend to set up, ongoing to run"
related: [running-freedom-infrastructure, encrypting-files-and-backups, decentralized-storage, internet-shutdown-preparedness, community-networks, tor, building-a-mesh, hardware-supply-chain-trust]
---

[Running Infrastructure for Freedom](/guides/running-freedom-infrastructure/) covers *what* to run — a Tor bridge, a Nostr relay, a Bitcoin node, a mesh repeater. This guide is about running it *so it survives*: so that a hardware failure, a seized server, a terminated hosting account or a national outage degrades the service instead of ending it. The principles are the same whether you run one relay or a small fleet, and they are deliberately general — no single product makes infrastructure resilient; a few habits do.

## Design for the loss of any one thing

The core discipline is to assume every individual component will fail or be taken, and to make sure none of them is irreplaceable.

- **No single point of failure.** Run at least two of anything that matters, so maintenance or a raid on one node is routine rather than fatal.
- **Diversity, not just redundancy.** Two servers at the same host, in the same country, on the same account are one failure. Spread across **different providers, different jurisdictions and different payment methods** so that no single order, invoice or legal request reaches all of them.
- **Keep identity separate from any one host.** Tie the service to a key or a name you control — a [self-hosted DNS name](/kb/decentralized-dns/), a Nostr key, an onion address — not to a provider's hostname, so you can move it without the users noticing.

## Backups you have actually restored

A backup is a hypothesis until you restore from it.

- **Encrypt before it leaves the machine.** Use client-side encryption so backups are safe on any host; see [encrypting files and backups](/guides/encrypting-files-and-backups/). Tools like [restic](https://restic.net/) and [BorgBackup](https://www.borgbackup.org/) do deduplicated, encrypted, incremental backups by default.
- **Follow 3-2-1.** Three copies, on two kinds of media, with one off-site — and for high-risk work, one in a different jurisdiction. [Decentralized storage](/kb/decentralized-storage/) can serve as a censorship-resistant off-site copy.
- **Rehearse the restore.** Schedule a real restore to a clean machine on a calendar. An untested backup is not a backup.

## Make rebuilding boring

If standing a node back up is a long, manual, half-remembered process, you will not do it under pressure.

- **Infrastructure as code.** Keep the whole configuration in version control and provision from it with a tool like [OpenTofu](https://opentofu.org/) or equivalent, so a replacement machine is minutes of automation, not a day of clicking.
- **Document the runbook.** Write down exactly how to bring the service up from nothing, and store it with (not only on) the infrastructure.
- **Automate the moving parts.** Certificate renewal, updates and health checks should not depend on you remembering.

## Plan the exit before you need it

Relocatability is a feature you build in advance, not a scramble during a crisis.

- **Portable state.** Keep the data that defines the service — keys, databases, config — small, encrypted and ready to move. Software built for this, like the [strfry](https://github.com/hoytech/strfry) Nostr relay, makes state easy to copy and resync.
- **Low TTLs and fast failover.** Short DNS TTLs and a warm standby mean you can repoint traffic in minutes.
- **Graceful shutdown and key rotation.** Know how to take a node down cleanly, rotate any keys it held, and bring the service up elsewhere without losing the users' trust in its identity.

## Trust the layers underneath

Resilience assumes the machine itself is honest. For infrastructure that may face physical access or seizure, pair this with attention to the layers below the operating system — see [hardware and firmware supply-chain trust](/kb/hardware-supply-chain-trust/) — and, where the network itself may go down, with local-first options like [community networks](/kb/community-networks/) and [mesh](/guides/building-a-mesh/) so the service stays reachable even when the wider internet does not.

## A short checklist

- Two independent instances, different providers and jurisdictions.
- Service identity bound to a key or name you control, not a host.
- Encrypted, deduplicated backups; a restore rehearsed in the last month.
- The whole setup reproducible from version control.
- A written runbook stored off the box.
- A tested plan to relocate and rotate keys within an hour.
