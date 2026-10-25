---
title: "Local-first Software and CRDTs"
slug: local-first-crdts
type: explainer
pillars: [storage, cryptography]
readiness: usable
description: "Local-first software keeps working data on your device; CRDTs merge concurrent edits, while encryption and access control remain separate choices."
dek: "Local copies make work possible without a server; merge algorithms help those copies converge when they meet again."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [syncthing, hypercore, tahoe-lafs, compare-storage, private-file-sync-and-backup]
tags: [local-first, crdt, automerge, yjs, cryptpad]
---

## Summary

Local-first software treats the copy on your own device as primary working data. You can read and edit it while disconnected, then synchronize later. Servers can still help replicas find each other and hold additional copies. The goal is to keep useful work possible without making every edit depend on a remote service.

The Ink & Switch local-first essay connects this design to offline use, collaboration, long-term access, privacy and user control. Those are design goals to assess in an application, not properties conferred by a label.

## How it works

A **conflict-free replicated data type (CRDT)** defines how independently edited copies merge. With the required changes delivered, replicas converge according to the data type's rules. That removes the need for a central server to order every edit. It does not decide whether the resulting prose, spreadsheet or application state is what the collaborators intended.

**Automerge** provides a CRDT data model, change history and synchronization machinery. Applications can merge concurrent changes and exchange them over different transports. Its core library does not require a particular network; surrounding libraries provide storage and networking integrations.

**Yjs** exposes shared types such as maps and arrays, editor integrations, network providers and persistence adapters. Its documentation states that update order does not matter as long as all changes eventually arrive. Developers still choose where updates persist and how they travel.

These libraries operate on application data. [Syncthing](/kb/syncthing/) synchronizes files; it does not turn an arbitrary file format into a collaborative data type.

## CryptPad: encrypted collaboration

CryptPad is a collaborative document suite with client-side, end-to-end encryption. It illustrates a separate decision from choosing a merge algorithm: whether the service storing and relaying collaboration data can read document contents. It should not be assumed to use Automerge or Yjs, or to satisfy every local-first goal, simply because it offers collaboration.

Under CryptPad's documented trust assumptions, the instance cannot read document contents. It can still see the user's IP address and browser information. Users must trust the instance to deliver the published client code and carry messages, and trust collaborators with the sharing links they receive. A server that delivers altered browser code is outside that trust model.

## Trust model / threat model

Convergence, authorization, confidentiality and durable storage are different requirements. A CRDT does not by itself establish who may edit, encrypt stored documents or keep a replica alive. Endpoints that hold readable data remain trusted. For encrypted collaboration, key distribution and sharing permissions matter as much as synchronization.

## Readiness

**Usable** as an application design approach with available libraries and an encrypted document suite. Assess the specific application: disconnect it, edit, reconnect, export the result and restore it on another device. Library capabilities alone do not establish that an application supports those operations.

## Limits

Offline editing delays communication with collaborators. Automatic merging can still require a human decision about meaning. Retained local history is useful, but it is not a substitute for a separate recovery copy. See [Private File Sync and Backup](/guides/private-file-sync-and-backup/) and [Hypercore](/kb/hypercore/) for related replication patterns.

## Primary sources

- [Ink & Switch: Local-first software](https://www.inkandswitch.com/essay/local-first/).
- [Automerge project](https://automerge.org/) and [core concepts](https://automerge.org/docs/hello).
- [Yjs documentation](https://docs.yjs.dev/).
- [CryptPad project](https://cryptpad.org/) and [security assumptions and metadata exposure](https://docs.cryptpad.org/en/user_guide/security.html).

Continue with [CryptPad](/kb/cryptpad/).
