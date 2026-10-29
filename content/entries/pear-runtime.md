---
title: "Pear: Peer-to-Peer App Runtime"
slug: pear-runtime
type: deep-dive
pillars: [apps, storage]
readiness: usable
description: "Pear, from Holepunch, ships desktop and terminal apps over pear:// links that peers seed and update directly, with no server, plus mobile JS updates."
dek: "An app's address is a public key: the code lives in a replicated Hyperdrive, peers seed it to each other, updates arrive when the drive grows, and multisig release lines stop one stolen laptop from shipping a bad build."
updated: 2026-10-29
created: 2026-10-29
origin: original
related: [hypercore, sovereign-applications, local-first-crdts, verifying-software, compare-storage, slashtags]
aliases: ["Pear", "Pear Runtime", "Holepunch Pear", "pear://", "Bare runtime"]
tags: ["pear", "holepunch", "hypercore", "p2p", "runtime", "distribution", "deep-dive"]
---

## Summary

Pear is Holepunch's peer-to-peer runtime and deployment platform for desktop, mobile and terminal applications. A project gets a `pear://` link, the code is synced into that link, and the network of peers distributes it. For desktop and terminal apps there is no download server, app store or update server: sharing the link is the distribution step. Mobile is different: the app itself is still a native React Native or Expo package that has to be installed through a store or sideloaded, and Pear then delivers JavaScript-only updates to it peer to peer. The `pear` CLI is Apache-2.0-licensed.

## How it works

**The link is a drive.** A project's files live in a [Hyperdrive](/kb/hypercore/), which sits on Hypercore's signed, append-only logs. The `pear://` link is that drive's address. Peers find each other through Hyperswarm and its distributed hash table, then replicate the drive directly. Anyone running the app can help seed it, and **blind peers**, helper nodes that keep Hypercores available when no writer is online, can hold data while the developer is offline.

**Updates.** A running Pear desktop app watches the drive behind its upgrade link. When the Hypercore log grows, it downloads the new build in the background and applies it on restart. Updates can be turned off per run or per app. On mobile, the same mechanism ships JavaScript-only updates without a store round trip; changes to native code still need a normal platform release, subject to store review where a store is used.

**Release lines.** The documented release flow has three steps: **stage** builds into a drive for iteration, **provision** a compacted prerelease drive from a versioned stage, and **multisig** commit into production, where a quorum of signers must agree before a release changes. The point, in Holepunch's words, is that "one compromised machine cannot redefine the release line."

**Runtime.** Pear runs on **Bare**, a minimal JavaScript runtime that can also be embedded in native apps or compiled into standalone binaries. Desktop Pear apps use Electron for the interface with Bare workers underneath. The same stack offers modules for peer connections, replicated databases (Hyperbee), file systems, Bluetooth Low Energy and on-device AI.

## What it protects against

- **Takedown of the distribution channel.** For desktop and terminal apps there is no server or store to order offline. As long as one peer seeds the drive, the app can be installed and updated. Mobile apps still depend on however their native package was installed.
- **Tampered builds in transit.** Hypercore data is verified against the writer's key, so peers cannot alter the app they relay.
- **A single stolen signing machine.** Multisig production lines require a quorum to publish a release.
- **Infrastructure cost and dependency.** Apps can talk peer to peer without backend servers.

## What it trusts, and the limits

- **The developer and the update key.** Automatic updates mean whoever controls the release line can ship new code to every user. Multisig raises the bar; it does not remove the trust. You can disable updates.
- **No browser-style sandbox.** Desktop Pear apps are Electron applications with Bare workers, so treat them as native software running with your user's privileges, not as sandboxed web pages.
- **Seeders.** If nobody seeds a drive, it cannot be fetched. Availability is a choice someone has to make and pay for.
- **IP addresses.** Peer-to-peer connections expose your IP address to the peers you connect to and reveal on the DHT that you are interested in a topic. Pear is not an anonymity tool.
- **One company's stack.** The runtime, protocols and most modules come from Holepunch. They are open source, but the ecosystem is concentrated around one maintainer.
- **Bootstrap.** The first install of the `pear` CLI comes from install.pears.com over ordinary HTTPS, so the usual software-verification care applies. See [Verify software before installing it](/kb/verifying-software/).

## Readiness

**Usable.** Pear and the Hypercore stack underneath it are actively developed and shipped, with templates for desktop, terminal and mobile apps and documented CI and multisig release pipelines. For desktop and terminal software, it is the most complete answer today to "how do I distribute and update an application with no servers at all". Its weak points are the usual ones for P2P: seeding, IP exposure, and trusting the author's update key.

## Primary sources

- Pear documentation: https://docs.pears.com/
- Releasing apps peer to peer (stage, provision, multisig): https://docs.pears.com/pear/explanation/deployment-releasing-apps-p2p/
- How the stack fits together: https://docs.pears.com/p2p/explanation/how-the-stack-fits-together/
- Pear mobile architecture (JS-only over-the-air updates): https://docs.pears.com/pear/explanation/pear-mobile-architecture/
- pear CLI and runtime (Apache-2.0): https://github.com/holepunchto/pear
- Hypercore: https://github.com/holepunchto/hypercore · Hyperdrive: https://github.com/holepunchto/hyperdrive · Hyperswarm: https://github.com/holepunchto/hyperswarm
- Bare runtime: https://github.com/holepunchto/bare
