---
title: "XMPP with OMEMO"
slug: xmpp-omemo
type: deep-dive
pillars: [messaging]
readiness: usable
description: "XMPP federates chat between independent servers; OMEMO encrypts messages between devices. Understand client choice, key verification and metadata limits."
dek: "Choose your server and client, then check that the conversation actually uses compatible end-to-end encryption."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [compare-messengers, matrix, delta-chat, signal-protocol, metadata-resistance]
---

## Summary

XMPP is a federated messaging protocol. An account has an address such as `name@example.org`; independently operated servers exchange messages for their users. **OMEMO**, specified in XEP-0384, adds end-to-end encryption between devices. Federation and encryption are separate properties: using XMPP alone does not establish an encrypted conversation.

## How it works

The [XMPP core standard](https://www.rfc-editor.org/rfc/rfc6120.html) defines addressing and server communication. [OMEMO](https://xmpp.org/extensions/xep-0384.html) establishes a Double Ratchet session for each recipient device, then encrypts message key material for those devices. It supports asynchronous messaging and multiple devices, with forward secrecy and recovery after key compromise under its stated assumptions.

Usable clients include [Conversations](https://conversations.im/), [Dino](https://dino.im/), Gajim, which documents [integrated OMEMO support](https://gajim.org/posts/2023-05-27-gajim-1.8.0-released/), and Monal, whose [supported-extension manifest](https://github.com/monal-im/Monal/blob/develop/monal.doap) lists OMEMO. Support for the name does not establish support for every revision of the specification. Check encryption with the particular clients and devices your contacts use.

## Trust model / threat model

OMEMO protects message content from servers when the intended devices' identity keys are correctly authenticated. Verify those keys through a trusted channel, and review new devices. Its specification explicitly excludes protection against metadata and traffic analysis.

Your server stores your contact roster under the [XMPP instant-messaging standard](https://www.rfc-editor.org/rfc/rfc6121.html). Routing still exposes account addresses and message traffic to participating servers. A self-hosted server changes the operator you trust; it does not remove the other participants' servers or their view of the exchange.

## Readiness

**Usable, with client-dependent setup.** Released clients implement OMEMO, while XEP-0384 itself remains marked **Experimental**. The protocol's standards status and the availability of working applications are different measures.

## Limits

Encryption defaults and supported extensions vary by client. Confirm that OMEMO is active instead of treating TLS to a server as end-to-end encryption. XEP-0384 also qualifies its forward-secrecy guarantee: the session key is protected only once both parties complete the key exchange. Device verification and compatibility remain part of the operational burden. This is server-mediated chat, not an off-grid transport; compare [Matrix](/kb/matrix/) and [Delta Chat](/kb/delta-chat/), or use the [messenger comparison](/kb/compare-messengers/).

## Primary sources

- [RFC 6120: XMPP core and federation](https://www.rfc-editor.org/rfc/rfc6120.html).
- [RFC 6121: rosters and messaging](https://www.rfc-editor.org/rfc/rfc6121.html).
- [XEP-0384: OMEMO, guarantees and threat model](https://xmpp.org/extensions/xep-0384.html).
- [Conversations](https://conversations.im/) and [Dino](https://dino.im/).
- [Gajim's integrated OMEMO implementation](https://gajim.org/posts/2023-05-27-gajim-1.8.0-released/).
- [Monal's supported XMPP extensions](https://github.com/monal-im/Monal/blob/develop/monal.doap).
