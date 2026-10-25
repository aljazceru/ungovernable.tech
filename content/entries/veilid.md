---
title: "Veilid"
slug: veilid
type: deep-dive
pillars: [anonymity, messaging]
readiness: experimental
description: "Veilid is a peer-to-peer application framework with encrypted private routing. It supplies network building blocks, not a complete messenger trust model."
dek: "Private routing for applications: assess the framework and the application using it as separate parts of the system."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [tor, quiet, metadata-resistance, compare-messengers]
---

## Summary

Veilid is an open-source framework for peer-to-peer applications, not itself a general-purpose messenger. The [project site](https://veilid.com/) describes encrypted communication as a building block and separately offers a beta of VeilidChat.

## How it works

The [networking documentation](https://veilid.com/documentation/networking/) describes peer discovery, bootstrap nodes, NAT traversal and relays. Nodes contribute connectivity according to their capabilities; applications can use the public network or a separate network.

[Private routing](https://veilid.com/documentation/private-routing/) combines a sender-chosen **safety route** with a destination-chosen **private route**. Neither side delegates the choice of the entire path to the other. Encrypted envelopes limit what intermediate hops learn about the path.

## Trust model / threat model

Private routing addresses network exposure. The application still determines how users authenticate contacts, store messages and handle compromised devices. Treat those as additional requirements before relying on a messenger built with Veilid; compare [metadata resistance](/kb/metadata-resistance/) and [Tor](/kb/tor/).

## Readiness

**Experimental for choosing a messenger.** The framework has documented interfaces and network mechanisms, but VeilidChat is presented as a public beta. Framework availability is not evidence that every application built on it is ready for sensitive use.

## Limits

Private routing involves performance and privacy trade-offs; the project's routing page explicitly lists further improvements. This entry makes no claim of protection against every traffic-analysis adversary. Consult the [messenger comparison](/kb/compare-messengers/) when choosing an application rather than a development framework.

## Primary sources

- [Veilid framework and VeilidChat beta](https://veilid.com/).
- [Veilid networking](https://veilid.com/documentation/networking/).
- [Private routes, safety routes and documented limitations](https://veilid.com/documentation/private-routing/).
