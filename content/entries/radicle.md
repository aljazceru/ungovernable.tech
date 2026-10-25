---
title: "Radicle"
slug: radicle
type: deep-dive
pillars: [storage, identity]
readiness: cautionary
description: "Radicle replicates Git repositories, issues and patches between peers. Understand repository IDs, seed availability and forge federation."
dek: "Keep code and collaboration records with the people who use them, while checking the protocol's security limits."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [decentralized-storage, activitypub, uncensorable-website, nostr-protocol]
---

## Summary

Radicle is a peer-to-peer system for publishing and collaborating on Git repositories. Participants keep local copies of code and collaboration records. A repository remains retrievable while a reachable peer seeds it; an identifier alone does not preserve the data.

## How it works

- **Two kinds of ID.** A Node ID identifies a node by its Ed25519 public key. A Repository ID, or RID, starts with `rad:` and derives from the repository's initial identity document. Later changes to that document do not change the RID.
- **Gossip and replication.** Signed announcements advertise nodes, repository inventories and reference updates. Peers discover where a repository is available through gossip, then transfer its contents using Git.
- **Collaborative objects.** Issues, patches and repository identities are signed objects stored in Git and replicated with the repository. Collaboration history can travel with the code.

The [protocol guide](https://radicle.dev/guides/protocol) describes these mechanisms. The [user guide](https://radicle.dev/guides/user) covers the working-copy workflow, including publishing a repository and fetching another participant's changes.

## Trust model / threat model

Keep the expected RID and verify collaborator identities through a channel you already trust. A valid signature identifies a signing key; deciding whether to accept its code remains a review decision.

Seeds provide storage and availability. The [seeder guide](https://radicle.dev/guides/seeder) explains how operators choose repositories and peers to follow. Keep independent copies and more than one reachable seed when continued availability matters. See [decentralized storage](/kb/decentralized-storage/) for the difference between naming content and preserving it.

## ForgeFed: federation between forges

[ForgeFed](https://forgefed.org/) extends [ActivityPub](/kb/activitypub/) with vocabulary and interactions for repositories, issues and patches across hosting services. Its site identifies Vervis as a reference implementation and describes Forgejo federation as being implemented. That is a separate approach from Radicle's peer replication; do not assume either protocol imports the other's collaboration records.

## Readiness

**Cautionary.** Radicle has documented user and seed workflows, but the current protocol guide explicitly removes its transport-encryption discussion because of a severe security vulnerability. This rating reflects that warning. Evaluate current security guidance before exposing a node or using it for sensitive collaboration.

## Limits

The protocol guide says private repositories use replication allowlists and are not encrypted at rest. An allowed peer therefore belongs inside the confidentiality boundary. Backups, key custody and the continued operation of seeds remain responsibilities of the participants.

## Primary sources

- [Radicle protocol guide](https://radicle.dev/guides/protocol)
- [Radicle user guide](https://radicle.dev/guides/user)
- [Radicle seeder guide](https://radicle.dev/guides/seeder)
- [ForgeFed project and implementation status](https://forgefed.org/)
