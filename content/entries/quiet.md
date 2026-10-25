---
title: "Quiet"
slug: quiet
type: deep-dive
pillars: [messaging, anonymity]
readiness: experimental
description: "Quiet synchronises team chat directly between members over Tor. Community owners control admission, and the unaudited software remains experimental."
dek: "A team-chat experiment that keeps community data on members' devices and uses Tor for the connections between them."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [jami, cwtch, briar, compare-messengers, tor]
---

## Summary

Quiet is a peer-to-peer team-chat project. Its [canonical repository](https://github.com/TryQuiet/quiet) describes communities whose devices synchronise over Tor without a central chat server. Each community forms its own network of members.

## How it works

The community owner supplies an invitation and issues the certificates used to admit members. OrbitDB synchronises messages between devices. A returning device can recover messages through peers that hold them; delivery therefore depends on members' devices being available.

## Trust model / threat model

Tor onion services protect the connections, while the community owner controls admission and certifies usernames. Those are different trust questions. Community members receive the shared data, and the owner's authority is part of the design. Compare [Cwtch](/kb/cwtch/) and [Jami](/kb/jami/) before treating decentralisation as a complete privacy guarantee.

## Readiness

**Experimental.** The project explicitly says Quiet is unaudited, lacks basic features, and should not be used when privacy and security are critical. That warning takes precedence over the availability of downloads.

## Limits

This is an internet-based Tor application, not an offline radio mesh. Peer availability and owner-controlled invitations shape its usability. Use the [messenger comparison](/kb/compare-messengers/) to distinguish that model from [Briar](/kb/briar/) and its local transports.

## Primary sources

- [Quiet: architecture, membership, synchronisation and security warning](https://github.com/TryQuiet/quiet).
