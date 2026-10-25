---
title: "Secure Scuttlebutt"
slug: secure-scuttlebutt
type: deep-dive
pillars: ["identity", "storage"]
readiness: usable
description: "Secure Scuttlebutt replicates signed append-only feeds between peers. Understand gossip, public content, identity keys and the roles of pubs and rooms."
dek: "A feed travels with its signatures; availability comes from peers retaining and exchanging copies."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: ["nostr-protocol", "hypercore", "local-first-crdts", "off-grid-networks"]
---

## Summary

Secure Scuttlebutt (SSB) is a peer-to-peer protocol built around signed, append-only feeds. An identity has a signing key, and a feed's messages link to the previous message. Peers can verify a feed received through another peer rather than trusting that intermediary to author it correctly.

## How it works

The protocol guide describes Ed25519 identity keys, hash-linked feed messages and replication between peers. `ssb-server` describes its synchronization as a gossip network: a peer can retain and relay another peer's log and files. Locally held data can therefore remain useful while disconnected, then synchronize during a later contact.

**Pubs** are reachable peers that participate in replication. **Rooms** help peers establish tunneled connections; they are a distinct role from retaining everyone's feeds. The Go room implementation documents connection tunneling, membership controls and administrative roles. A community must choose which services it needs and who maintains them.

## Trust model / threat model

Signatures authenticate feed updates under a key. They do not make a public post confidential or prevent a recipient from keeping a copy. The protocol guide separately specifies private-message encryption. Treat public feeds, following relationships and replication choices as potential disclosures.

Identity depends on the secret key. The protocol guide warns that losing it loses the ability to publish as that identity. Keep recovery material securely and check the client's identity model before trying to share one signing identity across devices.

## Readiness

**Usable at the protocol level.** The protocol guide and server implementations document the core mechanisms. Choose a client only after checking its current maintenance, supported feed formats and recovery workflow; no client support or release schedule is assumed here.

## Limits

Append-only replicated content is a poor fit for promises of universal erasure. Room admission controls also do not erase copies already held by members. Compare [Nostr](/kb/nostr-protocol/), [Hypercore](/kb/hypercore/) and [local-first software](/kb/local-first-crdts/) for other ways to combine keys, replication and collaboration.

## Primary sources

- [SSB protocol guide: identities, feeds, replication, pubs and rooms](https://ssbc.github.io/scuttlebutt-protocol-guide/)
- [ssb-server gossip and feed replication](https://github.com/ssbc/ssb-server)
- [Minimal pub server](https://github.com/ssbc/ssb-minimal-pub-server)
- [Go SSB room implementation and administrative controls](https://github.com/ssbc/go-ssb-room)
