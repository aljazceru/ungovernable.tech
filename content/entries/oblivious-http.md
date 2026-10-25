---
title: "Oblivious HTTP and DNS"
slug: oblivious-http
type: explainer
pillars: [anonymity, cryptography]
readiness: usable
description: "Oblivious HTTP and Oblivious DNS over HTTPS separate a client's address from request contents, provided the relay and gateway do not collude."
dek: "Split knowledge between a forwarding service and the service that decrypts the request."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [private-information-retrieval, pir-use-cases, metadata-resistance, browser-and-network-privacy, tor]
---

## Summary

**Oblivious HTTP (OHTTP)**, specified in RFC 9458, encrypts an HTTP message to a gateway and sends it through a relay. **Oblivious DNS over HTTPS (ODoH)**, specified in RFC 9230, applies a related separation to DNS queries using a proxy and target resolver. They are distinct protocols, not interchangeable wire formats.

## How it works

| Participant | OHTTP visibility | ODoH visibility |
|---|---|---|
| Client | Original request and returned response | Original DNS query and answer |
| Relay / proxy | Client network address, destination gateway/target, encrypted messages | Client network address, target resolver, encrypted DNS messages |
| Gateway / target | Decrypted HTTP request; relay's network address | Decrypted DNS query; proxy's network address |

The client obtains the decryption service's public-key configuration before encrypting. Responses return encrypted through the forwarding service.

## Trust model / threat model

The separation depends on the forwarding and decrypting parties **not colluding**. Combining their observations can reconnect a request with its origin. Operators, configuration distribution and traffic analysis therefore belong in the threat model.

OHTTP does not remove identifiers already inside a request. An account token can identify a user to the gateway even when the network address is hidden. Message sizes and timing can also reveal information; padding mitigates some size leakage.

## Readiness

**Usable as specified application components.** The RFCs define interoperable message flows. RFC 9230 is an Experimental RFC; this library's usability label does not change that standards status. A usable deployment still needs compatible clients, key distribution and independently operated services.

## Limits

The decrypting service still learns the query. [Private information retrieval](/kb/private-information-retrieval/) addresses that different question. Neither OHTTP nor ODoH is a general anonymity network for all device traffic; compare [Tor](/kb/tor/) and [metadata resistance](/kb/metadata-resistance/).

## Primary sources

- [RFC 9458: Oblivious HTTP](https://www.rfc-editor.org/rfc/rfc9458.html)
- [RFC 9230: Oblivious DNS over HTTPS](https://www.rfc-editor.org/rfc/rfc9230.html)
