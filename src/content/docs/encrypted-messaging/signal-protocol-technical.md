---
title: "Signal Protocol Technical"
tags:
  - "signal"
  - "e2ee"
  - "double-ratchet"
  - "x3dh"
  - "pqxdh"
  - "mls"
  - "messaging"
  - "deep-dive"
---
*The reference for asynchronous end-to-end encryption: forward secrecy, post-compromise security, deniability, and now post-quantum hybrid key exchange.*

---

## Why it's the reference

Most modern E2EE messengers (WhatsApp, Google Messages RCS, Skype Private Conversations, Wire 1.0, early Element) are direct or close ports of the Signal Protocol. The combination of:

- X3DH initial key agreement,
- Double Ratchet per-message key derivation,
- Sealed sender for metadata reduction,
- PQXDH post-quantum hybrid initial agreement (since 2023),

…produces a protocol with strong properties that few competitors match formally:

| Property | Means |
|----------|-------|
| Forward secrecy | Compromising current keys doesn't expose past messages |
| Post-compromise security | Future messages re-secure after key compromise once a ratchet step occurs |
| Deniability | No long-term signature on message content; recipients can't prove who sent what |
| Asynchronous start | Two parties can establish a session without both being online |
| Post-quantum forward secrecy | PQXDH protects current sessions against future quantum decrypt-later |

---

## X3DH (Extended Triple Diffie-Hellman)

Initial key agreement when Alice wants to message Bob who is offline. Bob's server hosts a pre-key bundle:

- `IK_B` — Bob's identity key (long-term)
- `SPK_B` — Bob's signed pre-key (medium-term)
- `OPK_B` — Bob's one-time pre-key (single-use)

Alice fetches the bundle and computes:

```
DH1 = DH(IK_A, SPK_B)
DH2 = DH(EK_A, IK_B)       (EK_A = ephemeral)
DH3 = DH(EK_A, SPK_B)
DH4 = DH(EK_A, OPK_B)      (if OPK present)
SK  = KDF(DH1 || DH2 || DH3 || DH4)
```

`SK` is the root key for the Double Ratchet. Alice attaches her ephemeral public key and identity key to her first message; Bob can re-derive `SK`.

---

## PQXDH (Post-Quantum Extended Triple Diffie-Hellman, 2023)

Adds an ML-KEM-1024 KEM to X3DH. Bob's pre-key bundle now includes a signed PQ pre-key (`PQPK_B`). Alice generates an ML-KEM ciphertext encapsulating to `PQPK_B`; the resulting shared secret is mixed into the X3DH KDF.

```
SK = KDF( X3DH_secrets  ||  ML-KEM-shared-secret )
```

Even if a future quantum adversary records today's traffic and breaks all ECDH, they still face an unbroken ML-KEM. Currently deployed in Signal mobile clients since fall 2023.

---

## Double Ratchet

After the initial `SK`, every message derives a fresh key. Two ratchets:

- DH ratchet: when Alice sends a new message after receiving from Bob, she generates a new ECDH keypair and includes the public key. Bob ratchets forward on receipt. Provides post-compromise security.
- Symmetric ratchet: within a "sending chain" between DH steps, message keys derive from a chained KDF. Provides forward secrecy.

```
Root chain:    K_root  ──(DH)──►  K_root'  ──(DH)──►  K_root''
               │                 │                  │
               KDF                KDF                KDF
               ▼                  ▼                  ▼
Send chain:   K_s, K_s', K_s''…  (each KDFed for forward secrecy)
```

The result: each message is encrypted under a unique key, deletable immediately after decryption.

---

## Sealed sender

By default the server knows `sender_id → recipient_id`. Sealed sender envelopes the sender identity inside the encrypted payload; the server sees only the recipient.

The recipient validates an attached *delivery token* (rate-limit) and *unidentified-sender certificate* (Signal's signed pseudonymous binding) without revealing identity to the server.

Limit: the server still sees connection metadata (IP, timing). For full metadata privacy, combine with Tor.

---

## Group messaging

Signal's original group protocol was pairwise: every group message sent N times. Modern Signal moved to a Sender Keys scheme (one symmetric chain per sender within the group). Limitations: leaving requires re-keying. Not as strong as MLS for very large groups.

MLS (RFC 9420) is the IETF standard for group E2EE: TreeKEM-based continuous group key agreement scaling to thousands. Wire and Cisco Webex use it; Signal has not migrated yet.

---

## Implementation surfaces

| Component | Library | Notes |
|-----------|---------|-------|
| Core protocol | [libsignal](https://github.com/signalapp/libsignal) | Rust core, language bindings |
| Group | Sender Keys (in libsignal) | Signal proprietary group |
| Server-side | Signal-Server (Java) | KGB / contact discovery |
| Contact discovery | SGX-based PIR | `Overview - Private Information Retrieval` |
| Sealed sender certificates | Signal-issued, time-limited | Operationally tied to Signal |

---

## What Signal doesn't solve

- Server-controlled identity (phone number). Signal requires a phone for registration; usernames since 2024 mitigate display, not registration.
- Centralized infrastructure. Signal-Server is one organization; takedown removes the messaging fabric.
- Backups. Cloud backups (iOS / Android) bypass the protocol's deletability.
- Group membership privacy. Server knows group rosters (mitigated via private groups, contact discovery in SGX).
- Endpoint compromise. Malware on the phone reads everything pre-encryption.

These motivate the federated and decentralized alternatives: [Matrix and E2EE](/encrypted-messaging/matrix-and-e2ee), [Nostr Deep Dive](/encrypted-messaging/nostr-deep-dive), SimpleX.

---

## Trade-offs

### Strengths

- Best-in-class cryptographic core, formally analyzed (CRYPTREC, ProVerif).
- Smooth UX: sealed sender, disappearing messages, view-once.
- Production PQ readiness: PQXDH shipped years before most peers.

### Limitations

- Centralization: single org, single jurisdiction.
- Phone-number identity: non-pseudonymous registration.
- No multi-device peer-to-peer: secondary devices link to a primary.
- Backups outside the protocol undermine deletability if used.

---

## Related Files

- [Overview - Encrypted Messaging](/encrypted-messaging)
- [Metadata Resistance](/encrypted-messaging/metadata-resistance)
- [Nostr Deep Dive](/encrypted-messaging/nostr-deep-dive) — alternative trust model
- [Matrix and E2EE](/encrypted-messaging/matrix-and-e2ee) — federated alternative
- [Overview - Post-Quantum Cryptography](/post-quantum) — PQXDH context

---

## Primary Sources

- Marlinspike & Perrin, *The X3DH Key Agreement Protocol*, 2016.
- Perrin & Marlinspike, *The Double Ratchet Algorithm*, 2016.
- Kret & Marlinspike, *The PQXDH Key Agreement Protocol*, 2023. [signal.org/docs/specifications/pqxdh](https://signal.org/docs/specifications/pqxdh/)
- Cohn-Gordon et al., *A Formal Security Analysis of the Signal Messaging Protocol*, EuroS&P 2017.
- RFC 9420, *Messaging Layer Security*.
- libsignal — [github.com/signalapp/libsignal](https://github.com/signalapp/libsignal)

