---
title: "IPNS and DNSLink"
slug: ipns-dnslink
type: deep-dive
pillars: [storage, naming]
readiness: usable
description: "IPNS signs mutable pointers to IPFS content, while DNSLink publishes paths in DNS TXT records; both need available content and careful name management."
dek: "Give changing content a stable address, with different trust models for a cryptographic key and a DNS domain."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [ipfs-and-filecoin, decentralized-dns, compare-storage, uncensorable-website, pkarr]
tags: [ipns, dnslink, ipfs, naming]
---

## Summary

Changing content changes its [IPFS](/kb/ipfs-and-filecoin/) content identifier. **IPNS** and **DNSLink** put an updateable name in front of that identifier. The name can keep pointing to the current publication while earlier CIDs continue to identify earlier content.

Neither mechanism stores the underlying files. Keep the named content available independently through pins or other retained replicas.

## How IPNS works

An IPNS name identifies a public key. Its record contains a target path, a sequence number, validity information and a signature from the corresponding private key. Verification binds the update to that key without requiring a particular server to vouch for it.

**Publishing is separate from signing.** Records can travel through different routing systems. IPFS documentation describes publishing and resolving them through the DHT, and using PubSub topics to distribute records among interested peers. Kubo documents PubSub as an opt-in transport alongside DHT publication.

An operator must manage three different lifetimes:

| Setting or condition | Meaning |
|---|---|
| Record validity | The signed expiration time after which the record must no longer be accepted. |
| Record TTL | A caching hint for when resolvers should look for an update. |
| Routing-system retention | How long the distribution system keeps the record; republishing may be needed before its signed validity ends. |

A longer validity period can keep a signed record useful when its signer is unavailable, but also leaves an older valid record acceptable for longer. A signature proves authority; it does not prove that a resolver has found the newest update.

## How DNSLink works

DNSLink publishes a TXT record at the `_dnslink` subdomain. Its value has the form `dnslink=/ipfs/<CID>` or can point to an IPNS path. Updating the DNS record changes the target; DNS caching affects when readers see the change.

The record belongs to the domain's DNS administration. **The resulting trust boundary includes the domain controller and DNS resolution path.** This follows from storing the binding in DNS: DNSLink does not turn the domain into an independently controlled IPNS key. A DNSLink path displayed under `/ipns/` may still be a DNS name rather than a key-based IPNS name.

## Trust model / threat model

Protect an IPNS private key as the authority to publish updates. With DNSLink, protect control of the relevant DNS records. If DNSLink points to an IPNS key, verify that key's record as well; the initial DNS binding remains a separate dependency.

A conventional HTTP gateway may resolve the name on your behalf. In that case you trust its resolution result unless your client independently verifies the signed record and addressed content. Naming and gateways also do not conceal which content is requested.

## Readiness

**Usable**, with specifications and implementation documentation. Plan for republishing, resolver caches and recovery of the signing key or DNS account. Test updates through the actual resolution path your readers will use.

## Limits

Names can resolve correctly while the content is unavailable. Stale records and caches can delay an update. Losing the IPNS signing key prevents further updates under that key. See [An Uncensorable Website](/guides/uncensorable-website/) for publication planning and [Choosing Decentralized Storage](/kb/compare-storage/) for retention choices.

## Primary sources

- [IPFS documentation: IPNS transports, validity and caching](https://docs.ipfs.tech/concepts/ipns/).
- [IPNS record and protocol specification](https://specs.ipfs.tech/ipns/ipns-record/).
- [DNSLink specification](https://dnslink.dev/).
- [IPFS documentation: DNSLink paths and publication](https://docs.ipfs.tech/concepts/dnslink/).
- [IPFS persistence and pinning](https://docs.ipfs.tech/concepts/persistence/).
- [IPFS privacy and encryption](https://docs.ipfs.tech/concepts/privacy-and-encryption/).
