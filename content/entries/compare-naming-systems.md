---
title: "Naming systems compared"
slug: compare-naming-systems
type: comparison
pillars: [naming, identity]
description: "Compare ENS, Handshake, Namecoin, GNS, Pkarr, onion names and DNS: renewal, resolution, key recovery and the places censorship can still act."
dek: "A name's ownership, its resolution and the availability of its destination are separate questions."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [decentralized-dns, ens, handshake, namecoin, gnu-name-system, pkarr, onion-and-i2p-naming, uncensorable-website]
---

## Summary

Choose a naming system by what readers can resolve and how you will retain control. The table separates registration renewal from record publication. Recovery notes are operational consequences of each ownership model, not promises that a lost secret can be reset.

## Ownership and resolution

| System | Renewal or continued publication | Resolver needed | Recovery responsibility |
|---|---|---|---|
| [ENS](/kb/ens/) `.eth` | Time-limited registration; renew before losing the name | ENS-aware application using registry and resolver contracts | Recover control of the owner wallet; renewal does not replace its signing authority |
| [Handshake](/kb/handshake/) | Periodic on-chain renewal; ownership can expire | Handshake-aware resolver/node | Retain the wallet controlling the name; plan backups and renewal transactions |
| [Namecoin](/kb/namecoin/) `.bit` | Renew or update; a semi-expired name stops resolving before final expiry | Namecoin-aware resolution software | Back up the owning wallet; expired names can be registered by others |
| [GNS](/kb/gnu-name-system/) | Publish signed records with expiration; no global registrar's rental term | GNS resolver and zone context | Back up the zone private key; revocation invalidates a zone rather than reconstructing its key |
| [Pkarr](/kb/pkarr/) | Republish ephemeral DHT records; no name-registration renewal | Pkarr-capable client through DHT or relay | Preserve the signing key; a different public key is a different name |
| [Onion names](/kb/onion-and-i2p-naming/) | No registrar renewal; keep the service and its key available | Tor client, such as Tor Browser | Protect and back up the service keys; the address derives from the identity public key |
| Conventional DNS | Registration terms depend on registry/registrar; DNS record TTL is separate | Ordinary DNS resolver and authoritative servers | Registrar account recovery and registration policy |

For `.eth`, anyone can pay to renew a registration, but that does not make them its owner. For Pkarr, record disappearance is a publication problem rather than somebody else registering the same public key. These distinctions matter when automating upkeep.

## Where censorship can act

| Model | Control moved away from | Remaining dependency |
|---|---|---|
| ENS, Handshake, Namecoin | A conventional registrar as the sole source of ownership | Chain access, transaction inclusion, ownership keys and the resolver/client used by readers |
| GNS | A single global naming root | Zone keys, delegations, publication and reachable GNS infrastructure |
| Pkarr | A registry allocating names | Key custody, record republishing and available DHT/relay paths |
| Onion names | DNS registration for the service address | Service keys, service availability and a working Tor connection |
| DNS | Administration is delegated through the hierarchy | Registry, registrar, authoritative operator and recursive resolver choices |

This is an architectural assessment, not a guarantee of immunity. A name that remains valid does not force a host to serve its content. Plan replicas through [publishing a resilient website](/guides/uncensorable-website/) and the [publish and preserve path](/paths/publisher-archivist/).

## Readiness and limits

Use the individual entries for implementation readiness. **GNS remains experimental**: GNUnet's official overview describes its software as early alpha. A published RFC does not change that software status.

Test resolution on the actual devices your readers use, and rehearse recovery before attaching an important identity to a name. Record the key backup, renewal or publication job, and independent route for telling readers about a replacement.

## Primary sources

- [ENS `.eth` registrar, ownership and renewal](https://docs.ens.domains/registry/eth/)
- [Handshake node, resolver and wallet operations](https://github.com/handshake-org/hsd)
- [Handshake name-expiry implementation](https://github.com/handshake-org/hsd/blob/master/lib/covenants/namestate.js)
- [Namecoin FAQ: expiry, resolution and wallet backups](https://www.namecoin.org/docs/faq/)
- [RFC 9498: GNU Name System](https://www.rfc-editor.org/rfc/rfc9498.html)
- [GNUnet software status](https://www.gnunet.org/en/about.html)
- [Pkarr publication and resolution](https://github.com/pubky/pkarr)
- [Tor onion address encoding](https://spec.torproject.org/rend-spec/encoding-onion-addresses.html)
- [Tor onion service setup and key custody](https://community.torproject.org/onion-services/setup/)
- [RFC 1034: DNS delegation and resolution](https://www.rfc-editor.org/rfc/rfc1034.html)
- [ICANN registration process](https://www.icann.org/resources/pages/domain-name-registration-process-2023-11-02-en)
- [ICANN expired registration recovery policy](https://www.icann.org/resources/pages/errp-2013-02-28-en)
