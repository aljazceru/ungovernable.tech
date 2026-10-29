---
title: "Hyphanet and Freenet"
slug: hyphanet-and-freenet
type: deep-dive
pillars: ["storage", "anonymity"]
readiness: usable
description: "Hyphanet (the original Freenet) is a long-running anonymous publishing network built on a distributed, encrypted store. How it works and its limits."
dek: "A 25-year-old anonymous content-publishing network, built on small-world routing over a peer-to-peer key-addressable store. In 2023 the project renamed itself \"Hyphanet\" because Ian Clarke (its original author) reused the \"Freenet\" name for an unrelated newer project. The disambiguation matters: the two systems share a name in popular memory and almost nothing else."
updated: 2026-04-26
created: 2026-04-26
origin: vault
source: "05-Off-Grid-Networks/Hyphanet and Freenet.md"
aliases: ["Hyphanet", "Freenet (legacy)", "Freenet Project", "Locutus"]
tags: ["hyphanet", "freenet", "p2p", "anonymity", "censorship-resistance", "small-world", "darknet", "deep-dive"]
---

## Naming, briefly

The Freenet Project, started in 1999-2000 by Ian Clarke at the University of Edinburgh and continued under the Freenet Project Inc. nonprofit, is a censorship-resistant content-store P2P network. In **2023 it renamed itself to Hyphanet** to free the "Freenet" name.

Concurrently, Ian Clarke launched a new project — also called Freenet (sometimes "Freenet 2024" or its codename Locutus) — that is a completely different design: a decentralized application platform with a contract / state model, more in the spirit of a distributed Substrate or NEAR than the old anonymous datastore.

This file covers **Hyphanet** (the original anonymous datastore, 2000-present, formerly Freenet). The Locutus / new-Freenet project is mentioned only for disambiguation.

## What Hyphanet is

Hyphanet is a P2P network whose nodes pool storage and bandwidth into a globally addressable content store. You insert a file by encrypting it under a key, computing the storage key (a hash of that key), and pushing the data into the network. Anyone who knows the URI can retrieve it; nobody (including the inserter, after enough time) can prove who originally published any given block.

It is not a chat system, not a web overlay, not a mesh radio protocol. It is closer to "anonymous BitTorrent crossed with a key-value store, with publishing deniability as a core property."

Use cases historically: dissident publishing, leaked documents, anonymous blogs (FMS / FlogHelper / Sone / Frost), discussion boards, file mirrors that needed to outlive the original publisher.

## How it works

### Content-addressable store

Files are split into blocks. Each block is encrypted and stored on multiple nodes by content-derived key. Hyphanet supports several URI types:

| URI | Meaning |
|-----|---------|
| **CHK** (Content Hash Key) | URI = hash of encrypted content + decryption key. Immutable; same content always has same CHK. |
| **SSK** (Signed Subspace Key) | A signing keypair owns a namespace; updates to a path are signed. |
| **USK** (Updatable Subspace Key) | Versioned SSK; clients track the latest version. |
| **KSK** (Keyword Signed Key) | Human-readable keyword; insecure but easy. |

CHKs are the workhorse. The decryption key is part of the URI itself — a friend who knows the URI can decrypt; a node storing the block cannot.

### Small-world routing

Each node keeps connections to a handful of peers (typically 5-50). Nodes are ranked along a ring of "locations" between 0 and 1. Routing a request for key K means: forward to the peer whose location is closest to K, and have them do the same.

This is small-world routing in the Watts-Strogatz / Kleinberg sense. With enough random long-range links, requests find their target in O(log N) hops on average even though no node has a global view.

The locations are self-organized: a node observes which keys it gets requests for and slowly drifts its location toward the average. Over time the network achieves a "swap-able" equilibrium that supports efficient routing.

### Caching as a side effect of routing

A request for key K travels through several peers. Every peer on the success path caches a copy. Popular content propagates organically; rarely-requested content eventually drops from the network.

This is what Hyphanet means by "store on demand": you don't pin content; you publish it and hope it gets requested often enough that the caches keep it alive. Files that nobody asks for fall off in days to weeks.

### Two operating modes: opennet and darknet

This is Hyphanet's defining innovation:

- **Opennet** — your node accepts connections from any peer. Easy to bootstrap, anyone can find you; weak against traffic-analysis adversaries because anyone can become your peer.

- **Darknet (friend-to-friend, F2F)** — your node only peers with people whose public key you have manually added. The network outside your friend-of-friend horizon is completely invisible to a passive observer. This is the "deniability mode" that early-2000s Hyphanet documentation emphasized.

Most users run opennet. Activists and dissidents in hostile network environments are intended to run darknet.

## Threat model

### What Hyphanet is meant to resist

- **Pseudonymous publishing.** No node can reliably prove which peer originated a given block; routing and caching mean the block has been seen by many peers before any observer arrives.
- **Plausible deniability of stored content.** Your node's local storage holds a `datastore.bdb`-style keystore of encrypted blocks. You cannot decrypt them without the URI. The classic argument is: if you don't know the URI, you don't know what your node is storing, so storage doesn't imply consent.
- **Censorship resistance for published content.** Once a CHK has propagated, removing it requires either every cache to drop it or the network to be shut down.

### What it doesn't resist

- **Traffic-pattern analysis** by an adversary observing many nodes. Hyphanet is not a mixnet; cover traffic is limited.
- **Active attackers running many opennet peers** can perform Sybil-style positioning attacks to surveil specific keys (the well-known Mobile Attacker Source Tracing / MAST work, McCoy & others, 2010s).
- **Endpoint compromise.** Nothing protects you if your node's filesystem is read by an adversary with the keys.
- **Legal-jurisdictional pressure** on operators who store content. The deniability argument is technical; courts may or may not accept it.

The University of Edinburgh and TU Dresden published a series of papers on Hyphanet's security properties in the late 2000s; Ben Roberts and others have analyzed the protocol over the years. The general academic consensus: Hyphanet's threat model holds against passive observers and against limited active attackers, weakens against well-resourced active attackers running many peers.

## Architecture today

The current Hyphanet codebase is Java, descended from the original 2000 implementation. It runs as a daemon on Windows, Linux, and macOS, exposes a localhost web UI on port 8888, and supports applications via a FreenetClientProtocol (FCP) socket.

Applications layered on top:

- **Freesite** publishing — static websites accessible via a Hyphanet URI, browsed through the Hyphanet web UI.
- **FMS** (Freenet Message System) — anonymous bulletin boards.
- **Sone** — Twitter-style microblogging with pseudonymous identities.
- **Frost** — older message system, mostly retired.
- **FlogHelper** — blog publishing tool.
- **Web of Trust (WoT)** — a Hyphanet-internal pseudonymous identity and trust system; not the OpenPGP web of trust (see [Overview - Web of Trust](/kb/web-of-trust/)).

Codebase: [github.com/hyphanet/fred](https://github.com/hyphanet/fred). "fred" stands for "Freenet REference Daemon."

## Comparison

| Property | Hyphanet | Tor onion services | I2P eepsites | IPFS |
|----------|----------|---------------------|--------------|------|
| Anonymous publishing | Yes (deniable) | Yes (operator anonymous) | Yes | No |
| Anonymous reading | Yes | Yes | Yes | No |
| Persistent storage without operator | Yes (caching) | No (operator must stay up) | No | Pinned by participants |
| Latency | Slow (seconds-minutes) | Slow | Slow | Fast (when content is online) |
| Active adversary resistance | Weak in opennet, strong in darknet | Strong | Strong | None |
| Active in 2026 | Yes (small) | Very active | Active | Very active |

Hyphanet's distinctive niche is the combination of **anonymous publishing with operator-independent persistence** plus the **darknet F2F mode**. No mainstream successor offers exactly that combination.

## Disambiguation: Locutus / new-Freenet

The new "Freenet" (sometimes Freenet 2024, sometimes Locutus) is Ian Clarke's redesign as a decentralized application platform. It uses small-world routing as well, but the unit of state is a "contract" — code + data with update rules — not an immutable content blob. Think of it as closer to NEAR or a smart-contract platform than to anonymous publishing.

If you read documents written before 2023 referring to "Freenet," they almost certainly mean Hyphanet. If you read post-2023 marketing material at [freenet.org](https://freenet.org), that is the new project. The two have different goals, different code, different threat models.

## Operational notes

- Run Hyphanet on a machine with reasonable disk (20-100 GB) and reasonable bandwidth (a few Mbps up). Slower nodes do work but slow down their peers.
- For sensitive use, run **darknet only** with a small set of manually-added peers you trust. Opennet is a softer target.
- Treat freenet.org / hyphanet.net URIs as public; assume traffic-analysis adversaries see request patterns even in darknet.
- Don't store URIs on systems an adversary can search. The URI is the decryption key.

## Primary sources

- Clarke, Sandberg, Wiley, Hong, "Freenet: A Distributed Anonymous Information Storage and Retrieval System" (ICSI Workshop on Design Issues in Anonymity and Unobservability, 2000).
- Hyphanet (formerly Freenet) — [hyphanet.org](https://hyphanet.org).
- Hyphanet source (`fred`) — [github.com/hyphanet/fred](https://github.com/hyphanet/fred).
- The 2023 rename announcement — [hyphanet.org/pages/news.html](https://hyphanet.org/pages/news.html).
- Roos, Beverly, Strufe, "Provable polylogarithmic-time routing in distributed networks" (2015), formal analysis of small-world routing of the kind Hyphanet uses.
- Roberts, "Routing in the Dark" — analyses of darknet F2F routing.
- New Freenet / Locutus (separate project) — [freenet.org](https://freenet.org). Disambiguated from Hyphanet.

For other ways to distribute applications without a central host, see [Sovereign Applications](/kb/sovereign-applications/) and [Pear](/kb/pear-runtime/).
