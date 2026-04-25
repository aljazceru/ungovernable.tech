---
title: "Encrypted Messaging"
tags:
  - "encrypted-messaging"
  - "e2ee"
  - "signal"
  - "matrix"
  - "nostr"
  - "communications"
sidebar: {"label":"Overview","order":0}
---
## What this section is about

Encrypted messaging makes sure only the intended recipients can read your communications. Not the platform, not your ISP, not anyone intercepting traffic. Modern E2EE (end-to-end encryption) goes beyond simple TLS to provide forward secrecy (compromising one key doesn't expose past messages) and metadata resistance (minimizing what leaks beyond the message body).

This section covers:

- Signal Protocol — the reference for asynchronous messaging.
- Matrix — decentralized chat with E2EE.
- Nostr — censorship-resistant social protocol.
- SimpleX — metadata-resistant messaging.
- Traditional options — Signal, WhatsApp, iMessage.

> "Every company or individual is one court order away from needing to decide how long they are willing to spend behind bars for not sharing the data with the government." — Ungovernable.tech

---

## The metadata problem

Encryption protects content. Metadata often reveals more:

| Data type | Example | Risk |
|----------|---------|------|
| Who | Alice → Bob | Social graph |
| When | Timestamp | Pattern of life |
| Where | IP address | Location |
| How | Device, client | Fingerprinting |
| Size | Message length | Traffic analysis |

Truly private systems address metadata, not just content.

---

## Key technologies

### Signal Protocol

The reference for asynchronous E2EE messaging, used by Signal, WhatsApp, and Google Messages.

Core components:

- Double Ratchet — forward-secret key evolution.
- X3DH — asymmetric key agreement.
- Sesame — session management for multi-device.

How it works:

1. Alice and Bob exchange keys once.
2. New keys are derived for each message.
3. Forward secrecy: compromising the current key does not expose past messages.

Limitations:

- Requires a phone number (metadata).
- Centralized servers.
- Not metadata resistant.

### Matrix

A decentralized chat protocol with E2EE (Megolm/Olm).

Architecture:

- Homeservers store message history.
- Bridges connect to other networks.
- E2EE is available but optional.

Trade-offs:

- Pros: decentralized, federated, open-source.
- Cons: E2EE not on by default, complex, leaks metadata.

### Nostr

"Notes and Other Stuff Transmitted by Relays" — a minimalist, censorship-resistant protocol.

Architecture:

- Keys: npub/nsec (like Bitcoin).
- Relays: simple message brokers; any app can run one.
- Clients: UI for reading and writing.

How it works:

1. Sign messages with `nsec`.
2. Publish to any relay.
3. Relays forward to clients.
4. Clients verify signatures.

Trade-offs:

- Pros: simple, censorship-resistant, no phone number, client diversity.
- Cons: no E2EE by default, spam, relay discovery.

Resources:

- [NIPs](https://github.com/nostr-protocol/nips) — protocol specs
- [awesome-nostr](https://github.com/aljazceru/awesome-nostr) — curated list

### SimpleX

A messaging protocol designed for metadata resistance.

Features:

- No user identifiers.
- Anonymous routing.
- No address-book correlation.

Trade-offs:

- Pros: metadata resistant.
- Cons: newer, smaller ecosystem.

---

## Network comparison

| Protocol | Metadata | Decentralized | E2EE | Open source |
|----------|---------|-------------|-------|------------|
| Signal | Poor | No | Yes | Core |
| WhatsApp | Poor | No | No | |
| Matrix | Moderate | Yes | Optional | Yes |
| Nostr | Good | Yes | No | Yes |
| SimpleX | Good | Partial | Yes | Yes |
| Session | Good | Yes | Yes | Yes |

---

## Client recommendations

### Security focus

| Client | Platform | Protocol | Notes |
|--------|----------|---------|-------|
| Signal | All | Signal | Best E2EE, weak metadata |
| Briar | Android | Briar | Off-grid, Tor |
| Session | All | Session | Metadata resistant |

### Decentralization

| Client | Platform | Protocol | Notes |
|--------|----------|---------|-------|
| Element | All | Matrix | Full implementation |
| Flemish | iOS | Nostr | Early |
| Damus | iOS | Nostr | Popular |

---

## Evidence at a glance

| Technology | Maturity | Evidence |
|------------|----------|----------|
| Signal Protocol | Production | Billions of users |
| Matrix | Production | Active development |
| Nostr | Production | Growing ecosystem |
| SimpleX | Beta | Active dev |

---

## Trade-offs

### Strengths

- Content privacy — only sender and receiver can read.
- Forward secrecy — past messages stay safe if a key is compromised.
- Censorship resistance on some platforms.
- Self-sovereign identity (Nostr).

### Limitations

- Metadata leaks — most platforms expose who and when.
- Metadata correlation — can be linked to off-platform data.
- Key compromise — device compromise breaks everything.
- Jurisdiction — some platforms aren't available in some places.

### Operational security

- Verify contacts via key fingerprints.
- Use ephemeral messages for sensitive topics.
- Consider device-compromise models.
- Use separate devices for sensitive work.

---

## Related Files

- [Nostr Deep Dive](/encrypted-messaging/nostr-deep-dive)
- [Signal Protocol Technical](/encrypted-messaging/signal-protocol-technical)
- [Matrix and E2EE](/encrypted-messaging/matrix-and-e2ee)
- [Metadata Resistance](/encrypted-messaging/metadata-resistance)
- **Off-Grid Messaging**

