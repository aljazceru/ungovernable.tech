---
title: "Overview - Encrypted Messaging"
tags:
  - "encrypted-messaging"
  - "e2ee"
  - "signal"
  - "matrix"
  - "nostr"
  - "communications"
---
## Overview

**Encrypted Messaging** ensures that only the intended recipients can read your communications — not the platform, not your ISP, not anyone intercepting the traffic. Modern E2EE (end-to-end encryption) goes beyond simple TLS to provide **forward secrecy** (compromising one key doesn't expose past messages) and **metadata resistance** (minimizing information leakage).

This section covers:
- **Signal Protocol** — The gold standard for async messaging
- **Matrix** — Decentralized chat with E2EE
- **Nostr** — Censorship-resistant social protocol
- **SimpleX** — Metadata-resistant messaging
- **Traditional options** — Signal, WhatsApp, iMessage

> "Every company or individual is one court order away from needing to decide how long they are willing to spend behind bars for not sharing the data with the government." — Ungovernable.tech

---

## The Metadata Problem

Encryption protects **content**, but metadata often reveals more:

| Data Type | Example | Risk |
|----------|---------|------|
| Who | Alice → Bob | Social graph |
| When | Timestamp | Pattern of life |
| Where | IP address | Location |
| How | Device, client | Fingerprinting |
| Size | Message length | Traffic analysis |

Truly private systems must address metadata, not just content.

---

## Key Technologies

### Signal Protocol

**What it is**: The gold standard for async E2EE messaging, used by Signal, WhatsApp, and Google Messages.

**Core components**:
- **Double Ratchet** — Forward secret key evolution
- **X3DH** — Asymmetric key agreement
- **Sesame** — Session management for multi-device

**How it works**:
1. Alice and Bob exchange keys once
2. New keys derived for each message
3. Forward secrecy: compromising current key doesn't expose past

**Limitations**:
- Requires phone number (metadata)
- Centralized servers
- Not metadata resistant

### Matrix

**What it is**: Decentralized chat protocol with E2EE (Megolm/olm).

**Architecture**:
- **Homeservers** — Store message history
- **Bridges** — Connect to other networks
- **E2EE** — Available but optional

**Trade-offs**:
- Pros: Decentralized, federated, open-source
- Cons: E2EE not default, complex, metadata leaks

### Nostr

**What it is**: "Notes and Other Stuff Transmitted by Relays" — minimalist, censorship-resistant protocol.

**Architecture**:
- **Keys** — npub/nsec (like Bitcoin)
- **Relays** — Simple message brokers (any app can run one)
- **Clients** — UI for reading/writing

**How it works**:
1. Sign messages with nsec
2. Publish to any relay
3. Relays forward to clients
4. Clients verify signatures

**Trade-offs**:
- Pros: Simple, censorship-resistant, no phone \#, client diversity
- Cons: No E2EE (yet), spam, relay discovery

**Resources**:
- [NIPs](https://github.com/nostr-protocol/nips) — Protocol specs
- [awesome-nostr](https://github.com/aljazceru/awesome-nostr) — Curated list

### SimpleX

**What it is**: Messaging protocol designed for metadata resistance.

**Features**:
- No user identifiers
- Anonymous routing
- No address book correlation

**Trade-offs**:
- Pros: Metadata resistant
- Cons: Newer, smaller ecosystem

---

## Network Comparison

| Protocol | Metadata | Decentralized | E2EE | Open Source |
|----------|---------|-------------|-------|------------|
| **Signal** | Poor | No | Yes | Core |
| **WhatsApp** | Poor | No | No |
| **Matrix** | Moderate | Yes | Optional | Yes |
| **Nostr** | Good | Yes | No | Yes |
| **SimpleX** | Good | Partial | Yes | Yes |
| **Session** | Good | Yes | Yes | Yes |

---

## Client Recommendations

### For Security Focus

| Client | Platform | Protocol | Notes |
|--------|----------|---------|-------|
| **Signal** | All | Signal | Best E2EE, metadata weak |
| **Briar** | Android | Briar | Off-grid, Tor |
| **Session** | All | Session | Metadata resistant |

### For Decentralization

| Client | Platform | Protocol | Notes |
|--------|----------|---------|-------|
| **Element** | All | Matrix | Full implementation |
| **Flemish** | iOS | Nostr | Early |
| **Damus** | iOS | Nostr | Popular |

---

## Evidence at a Glance

| Technology | Maturity | Evidence |
|------------|----------|----------|
| Signal Protocol | Production | Billions of users |
| Matrix | Production | Active development |
| Nostr | Production | Growing ecosystem |
| SimpleX | Beta | Active dev |

---

## Trade-offs

### Strengths

- **Content privacy** — Only sender/receiver can read
- **Forward secrecy** — Past messages safe if key compromised
- **Censorship resistance** (some platforms)
- **Self-sovereign identity** (Nostr)

### Limitations

- **Metadata leaks** — Most platforms leak who/when
- **Metadata correlation** — Can link to off-platform data
- **Key compromise** — Device compromise undermines all
- **Jurisdiction** — Some platforms not available

### Operational Security

- Verify contacts (key fingerprints)
- Use ephemeral messages for sensitive topics
- Consider device compromise models
- Use separate devices for sensitive work

---

## Related Files

- [Nostr Deep Dive](/encrypted-messaging/nostr-deep-dive)
- [Signal Protocol Technical](/encrypted-messaging/signal-protocol-technical)
- [Matrix and E2EE](/encrypted-messaging/matrix-and-e2ee)
- [Metadata Resistance](/encrypted-messaging/metadata-resistance)
- [Off-Grid Messaging](/encrypted-messaging/off-grid-messaging)
