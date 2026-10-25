---
title: "Overlay Naming: Tor .onion and I2P"
slug: onion-and-i2p-naming
type: explainer
pillars: ["naming", "anonymity"]
readiness: battle-tested
description: "Tor .onion and I2P names are public keys, so no registrar can seize them: how overlay naming works, and its usability trade-offs."
dek: "Tor onion services and I2P destinations bind overlay addresses to cryptographic identities, with human-readable aliases and availability as separate concerns."
updated: 2026-10-25
created: 2026-06-22
origin: vault
source: "03-Decentralized-DNS/Overlay Naming - Tor .onion and I2P.md"
aliases: [".onion", "Onion v3", "I2P destinations", ".b32.i2p", "Hidden service naming"]
tags: ["tor", "onion", "i2p", "b32", "naming", "overlay", "hidden-services", "deep-dive"]
---

## Summary

Tor onion services and I2P destinations bind overlay addresses to cryptographic identities. They avoid a conventional registrar for the cryptographic address, while still depending on software, keys and a functioning overlay network.

Human-readable aliases are a separate layer. See [decentralized naming](/kb/decentralized-dns/), [GNS](/kb/gnu-name-system/) and [PKARR](/kb/pkarr/) for other approaches to that trade-off.

## How it works

### Tor v3 onion services

A v3 onion address encodes the service’s Ed25519 public key, a checksum and a version byte:

```
base32(public_key || checksum || version) + ".onion"
```

The public key occupies 32 bytes, the checksum 2 bytes and the version 1 byte. Together they produce a 56-character base32 label. The checksum is derived from SHA3-256 over the onion-checksum prefix, public key and version.

Clients derive a time-period-specific blinded key and obtain the corresponding service descriptor from onion-service directories. The descriptor supplies introduction points. Client and service establish separate circuits to a rendezvous relay; the onion address itself is not that relay’s address.

Descriptor signing keys, blinded keys and the long-term identity key have different roles. The descriptor verification chain connects the service description to the identity encoded in the address.

### Onion authentication and HTTPS

Tor authenticates the onion service and encrypts the connection within the overlay. HTTPS can add a separate TLS layer. Ordinary HTTPS certificate validation still applies: Tor Browser does not universally replace it with a deterministic pin derived from the onion key. The Tor Project documents CA-issued certificates for onion services.

Running an onion service does not require operating a public Tor relay. The service setup guide describes configuring a Tor client and a local service endpoint.

### I2P destinations

An I2P Destination is a serialized structure containing public-key fields and a certificate. It is not universally a 516-byte object: its encoding depends on the certificate and key types.

A conventional `.b32.i2p` address uses the base32-encoded SHA-256 hash of the complete Destination, yielding a 52-character label. It is not a hash of only the signing key. The router obtains the corresponding LeaseSet and Destination information to establish communication.

Human-readable `.i2p` names are local address-book mappings, often populated through subscriptions. Different users can have different mappings; this is not a single global registrar-controlled namespace.

### Post-quantum work

I2P Proposal 169 separates work on the ratchet, NTCP2, SSU2 and signature types. Its status table marks hybrid ratchet work complete in Java I2P and i2pd, while other components have separate rollout states. It does not support the blanket claim that all post-quantum work remains an undeployed development-branch experiment.

## Trust model / threat model

- Verify the address through a channel appropriate to the application. A self-authenticating address proves control of a key, not a person’s real-world identity.
- Protect service keys and endpoints. Address authentication cannot repair a compromised application or stolen identity key.
- Directory, tunnel and routing mechanisms still have availability and traffic-analysis limits.
- Human-readable aliases introduce trust in whoever supplies the mapping.

## Readiness

Tor v3 onion services and I2P destination naming are implemented and documented. Follow the current service and router documentation; protocol support and migration status depend on the particular implementation.

## Limits

Cryptographic addresses are long and normally distributed out of band. They do not guarantee availability, eliminate phishing, or make traffic correlation impossible. Vanity-address tools such as mkp224o change the appearance of a Tor address by searching keys; they do not change its authentication model.

A service can publish an onion address, an I2P address and a conventional domain for different audiences. Treat each as a distinct access path and verify the bindings between them.

## Primary sources

- [Tor: encoding v3 onion addresses](https://spec.torproject.org/rend-spec/encoding-onion-addresses.html)
- [Tor onion-service protocol](https://spec.torproject.org/rend-spec/index.html)
- [Tor: onion services version 3](https://blog.torproject.org/v3-onion-services-usage/)
- [I2P development roadmap](https://i2p.net/en/get-involved/roadmap)
- [mkp224o vanity onion generator](https://github.com/cathugger/mkp224o)
- [I2P naming overview](https://i2p.net/en/docs/overview/naming/)
- [Tor onion service authentication and HTTPS](https://community.torproject.org/onion-services/advanced/https/)
- [Tor onion-service setup](https://community.torproject.org/onion-services/setup/)
- [I2P common structures: Destination](https://i2p.net/en/docs/specs/common-structures/)
- [I2P Proposal 169 current specification](https://i2p.net/en/proposals/169-pq-crypto/)
