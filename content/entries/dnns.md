---
title: "DNNS"
slug: dnns
type: deep-dive
pillars: ["naming"]
readiness: experimental
description: "DNNS is Lithosphere’s experimental on-chain naming application: public contracts, the Kamet testnet interface and its trust limits."
dek: "Lithosphere’s ENS-derived naming application has public contracts, deployment manifests and a documented Kamet testnet interface for .litho names."
updated: 2026-10-25
created: 2026-05-18
origin: vault
source: "03-Decentralized-DNS/DNNS.md"
aliases: ["Decentralized Naming System (Lithosphere)", "Lithosphere DNNS"]
tags: ["dnns", "lithosphere", "naming", "decentralized-dns", "web4", "blockchain", "deep-dive"]
---

## Summary

DNNS is Lithosphere’s on-chain naming application. Its public repository contains an ENS-derived implementation, custom Solidity contracts, deployment manifests and explorer integration. The documented v0 service uses the `.litho` namespace on the Kamet testnet.

This is a blockchain application namespace. It does not replace the public DNS root. Compare [ENS](/kb/ens/), [Handshake](/kb/handshake/) and [PKARR](/kb/pkarr/) in the [decentralized naming overview](/kb/decentralized-dns/).

## How it works

The documented Kamet deployment uses an ENS registry, base registrar, custom registration controller, public resolver and reverse registrar. Registration follows a commit–wait–reveal flow. The owner sets resolver records separately from registration.

The v0 interface supports second-level `.litho` names and free testnet registration. The repository distinguishes that deployed interface from later reference architectures and cross-chain work; these should not be treated as one interchangeable production system.

The explorer’s acceptance record documents forward resolution and forward-confirmed reverse resolution. A reverse name is displayed only after resolving that name back to the queried address.

## Trust model / threat model

- Name control depends on the selected chain, deployed contracts and controller configuration.
- RPC services and explorer interfaces affect availability and the information shown to users.
- Publishing source and deployment addresses does not establish that the contracts have been independently audited.
- The project’s security notes identify unresolved development-tool dependencies and distinguish them from the contracts’ runtime behavior.

## Readiness

Experimental. Public code and a documented testnet deployment exist. The repository’s acceptance record describes a supported Kamet interface and explorer checks; that evidence supports testing this implementation, not a claim of general cross-chain production readiness.

## Limits

- The documented v0 interface is limited to Kamet and second-level names.
- Registration and record updates are separate operations.
- Cross-chain expansion must be evaluated against the specific implementation and deployment being used.
- A source release and an acceptance checklist are not a security audit.

## Primary sources

- [Lithosphere source](https://github.com/KaJLabs/lithosphere)
- [DNNS implementation overview](https://github.com/KaJLabs/lithosphere/blob/main/DNNS/README.md)
- [DNNS code provenance](https://github.com/KaJLabs/lithosphere/blob/main/DNNS/PROVENANCE.md)
- [DNNS security model](https://github.com/KaJLabs/lithosphere/blob/main/DNNS/SECURITY.md)
- [DNNS acceptance checks](https://github.com/KaJLabs/lithosphere/blob/main/docs/dnns-acceptance.md)
