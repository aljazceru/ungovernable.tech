---
title: "Sovereign Applications: Distributable, Verifiable, Contained"
slug: sovereign-applications
type: explainer
pillars: [apps]
readiness: usable
description: "What makes an app sovereign: no gatekeeper can pull it, you can verify it is the author's code, and it holds only the access you grant."
dek: "Every other pillar ends up as an app on a device. If a store can delete that app, a server can swap its code, or the app itself can do anything you can, the protocol underneath does not save you."
updated: 2026-10-29
created: 2026-10-29
origin: original
related: [napplet, nsite, zapstore, compare-android-app-stores, pear-runtime, object-capabilities, local-first-crdts, verifying-software, grapheneos, tails-qubes-whonix]
aliases: ["Sovereign apps", "Unstoppable apps", "Permissionless app distribution"]
tags: ["apps", "distribution", "sandboxing", "local-first", "reproducible-builds", "capabilities", "explainer"]
---

## Summary

Encrypted messengers, wallets and mesh clients reach people as applications, and applications have their own chokepoints. App stores remove apps on request. Update servers can push a modified build to one person. A web app is re-downloaded from someone else's server on every visit. And most apps, once installed, can reach everything their user can.

A **sovereign application** answers three questions well:

1. **Distributable.** Can it reach users without a gatekeeper's permission, and keep reaching them if one host disappears?
2. **Verifiable.** Can you check that the code you run is the code its author published, and ideally that it matches public source?
3. **Contained.** Does it hold only the authority you grant, so a bad app or a bad update cannot take everything?

A fourth property, **your data stays yours**, is about where the app keeps state. Local-first software keeps the working copy on your device.

## Distributable: no single place to pull it from

- **Content addressing and signed manifests.** If files are addressed by their hash and listed in a manifest signed by the author's key, any server can host them and none can alter them. [nsites](/kb/nsite/) publish static websites this way on Nostr and [Blossom](/kb/blossom/); [IPFS](/kb/ipfs-and-filecoin/) does the same with content identifiers; see also [Publishing an Uncensorable Website](/kb/uncensorable-website/).
- **Peer-to-peer distribution.** [Pear](/kb/pear-runtime/) ships desktop and terminal apps over a `pear://` link that users seed to each other, with updates arriving the same way. Mobile apps still need a native install, after which Pear can deliver JavaScript updates peer to peer.
- **Open app catalogues.** [Zapstore](/kb/zapstore/) announces Android releases as signed Nostr events; F-Droid and Obtainium offer other routes. [Android app sources compared](/kb/compare-android-app-stores/) lays out the trade-offs.
- **Decentralised application platforms.** The new Freenet runs applications as contracts on a peer-to-peer network (see [Hyphanet and Freenet](/kb/hyphanet-and-freenet/) for how it differs from the original).

## Verifiable: the code is the code

- **Signatures** bind a release to the author's key. Hash checks bind a download to a release. Neither says the code is good. See [Verify software before installing it](/kb/verifying-software/).
- **Reproducible builds** let anyone rebuild from source and get the identical binary. F-Droid does this for many Android apps.
- **Pinned identity.** A [napplet's](/kb/napplet/) identity is computed from the hash of the bytes that run. Accrescent pins an app's signing key before the first install.

## Contained: least authority by default

- **Sandboxes.** Browsers isolate sandboxed iframes; napplets rely on that to keep keys and storage out of reach of applets. WebAssembly modules can call only the host functions they import. Hardened mobile systems such as [GrapheneOS](/kb/grapheneos/) sandbox every app and let you deny permissions such as network access.
- **Compartments.** Qubes OS runs apps in separate virtual machines ([Tails, Qubes OS and Whonix](/kb/tails-qubes-whonix/)).
- **Capabilities.** [Object-capability security](/kb/object-capabilities/) makes "you can only use what you were handed" the rule of the whole system, and Spritely Goblins and OCapN extend it across the network.
- **Keys stay with one trusted component.** Remote signers and napplet shells keep your Nostr key out of individual apps; see [Nostr key custody](/kb/nostr-key-custody/).

## Your data stays yours

[Local-first software](/kb/local-first-crdts/) keeps the primary copy of your data on your device and syncs with CRDTs. Peer-to-peer data layers such as [Hypercore](/kb/hypercore/) and key-owned stores such as [Pubky](/kb/pubky/) let apps work without a provider account.

## What none of this solves

- **A trusted author can still betray you.** A signed, reproducible, sandboxed app can still be malicious within the access you grant, and automatic updates let its author change it.
- **Curation becomes the new chokepoint.** Permissionless publishing means spam and malware are published too. Someone has to decide what to show you, and webs of trust or curated catalogues bring back judgment, ideally judgment you choose.
- **Gateways quietly recentralise.** Visiting an nsite or IPFS site through a public HTTP gateway means trusting that gateway, and censors block popular gateways.
- **The platform has the last word.** Operating systems decide what can be installed at all. Google's Android developer-verification rules, live in four countries since 30 September 2026 and planned for all certified devices in 2027, are the clearest current example.

## Where to start

- To publish something that should outlive any host: [nsite](/kb/nsite/).
- To get apps without Google Play: [Android app sources compared](/kb/compare-android-app-stores/), then [Zapstore](/kb/zapstore/).
- To build Nostr apps that never touch user keys: [Napplets](/kb/napplet/).
- To ship desktop software with no servers: [Pear](/kb/pear-runtime/).
- To check what you install: [Verify software before installing it](/kb/verifying-software/).

## Primary sources

- Ink & Switch, *Local-first software*: https://www.inkandswitch.com/essay/local-first/
- NIP-5A (nsites): https://github.com/nostr-protocol/nips/blob/master/5A.md
- NIP-5D draft (napplets): https://github.com/nostr-protocol/nips/pull/2303
- Pear documentation: https://docs.pears.com/
- F-Droid reproducible builds: https://f-droid.org/docs/Reproducible_Builds/
- WebAssembly security model: https://webassembly.org/docs/security/
- OCapN: https://ocapn.org/
- Android developer verification: https://developer.android.com/developer-verification/guides
