---
title: "Marmot Protocol"
tags:
  - "marmot"
  - "mls"
  - "nostr"
  - "e2ee"
  - "group-messaging"
  - "deep-dive"
---
*MLS (RFC 9420) layered on Nostr's identity and relay infrastructure to deliver end-to-end encrypted, scalable, metadata-protected group messaging without centralized servers.*

---

## What Marmot is

Marmot is a specification (a series of MIPs, Marmot Implementation Protocols) for using Nostr as the transport and identity layer for MLS, the IETF Messaging Layer Security standard. The result is a messaging system that combines:

- Signal-grade cryptographic guarantees (forward secrecy, post-compromise security) via MLS.
- Nostr-grade decentralization (no central server, key-rooted identity, censorship resistance) via Nostr.
- Logarithmic scaling for groups (MLS's TreeKEM) instead of Signal's per-pair Sender Keys.
- Metadata protection via NIP-59 gift-wrapping for membership-changing events.

It addresses a real gap in the Nostr ecosystem: NIP-04 and NIP-17 are per-message DM ciphers without forward secrecy and without group support. Marmot is the next layer.

Status: experimental. Active development through 2024-2026, specification under iteration.

---

## How it plugs into Nostr

Nostr provides three things Marmot uses directly:

1. Identity. Each user already has a `secp256k1` Nostr keypair (`npub`).
2. Delivery substrate. Relays accept and forward signed events globally and asynchronously.
3. Asynchronous semantics. Receivers can come online later and pull events.

Marmot defines new event kinds on top of this:

| Kind | Purpose |
|------|---------|
| `30443` | KeyPackage event — published "invitation cards" |
| `444` | Welcome rumor (gift-wrapped at kind `1059`) |
| `445` | Group event (Proposal / Commit / Application message) |

The spec is in MIP-00 through MIP-05 in the [marmot-protocol/marmot](https://github.com/marmot-protocol/marmot) repository.

---

## The three event flows

### KeyPackage publishing (MIP-00)

Each user publishes a `kind:30443` *KeyPackage* containing:

- An MLS BasicCredential whose `identity` field is the raw 32-byte Nostr public key.
- A signing key (distinct from the Nostr identity, MLS-specific).
- Ciphersuite, MLS extensions, and supported proposal types (including `self_remove` for cooperative leaving).
- Relays where this KeyPackage is published (for discovery).

KeyPackages are basically asynchronous invitation cards. When Alice wants to add Bob to a group, she fetches Bob's KeyPackage and uses it to encode a Welcome message addressed to him.

### Welcome (MIP-02)

When a user is added to a group, the admin sends a *Welcome event*:

```
kind: 1059 (gift wrap)
   └── kind: 13 (NIP-59 seal)
         └── kind: 444 (rumor — Welcome MLS message)
```

NIP-59 gift-wrapping hides both the recipient and the fact that a Welcome happened from any relay or observer. The Welcome MUST be sent only after the corresponding MLS Commit has been confirmed by relays. Sending it earlier causes a state fork where the new member sits at one MLS epoch and existing members at another, and decryption breaks until manual recovery.

### Group events (MIP-03)

After joining, members exchange `kind:445` events for everything inside the group:

- Proposals (add member, remove member, update keys).
- Commits (apply pending proposals, advance epoch).
- Application messages (the actual chat content).

Each kind:445 event:

- Is signed by an *ephemeral* Nostr keypair, distinct per event, never reused. This hides the sender at the relay layer.
- Contains the MLS `MLSMessage` encrypted with ChaCha20-Poly1305 using a per-epoch key derived from MLS exporter secrets.
- Carries an `h` tag with the group's `nostr_group_id` (from the `marmot_group_data` extension) for relay routing without revealing the MLS group ID.

---

## Cryptographic properties

| Property | Source | Status |
|----------|--------|--------|
| End-to-end encryption | MLS + ChaCha20-Poly1305 | Strong |
| Forward secrecy | MLS ratchet | Strong |
| Post-compromise security | MLS Commits rotate keys | Strong |
| Membership privacy | NIP-59 gift wrap on Welcome | Strong; observers can't tell who's in which group from public events |
| Sender unlinkability per-message | Ephemeral keypairs on kind:445 | Strong, with per-epoch caveats — see below |
| Group size privacy | Encrypted content; ephemeral senders | Strong against external observers |
| Identity continuity | Nostr identity + distinct MLS signing key | Group compromise doesn't burn Nostr identity |
| Disappearing messages | NIP-40 expiration via `marmot_group_data` extension | Hint to relays; clients enforce |

### What Marmot doesn't try to hide

- The fact that you publish KeyPackages. Anyone can see your `kind:30443` events.
- The fact you receive `kind:1059` gift wraps. Standard Nostr gift-wrap visibility.
- Endpoint compromise. Same as everywhere.

---

## Comparison

| Property | Signal Sender Keys | Matrix Megolm | Marmot (MLS over Nostr) | NIP-04 / NIP-17 |
|----------|-------------------|---------------|-------------------------|-----------------|
| Group scaling | Linear per send | Log (Megolm) | Log (MLS TreeKEM) | Linear |
| Forward secrecy | Yes | Yes (rotation) | Yes (per-Commit) | No |
| Post-compromise security | Limited | Per-rotation | Yes (per-Commit) | No |
| Decentralization | Single org | Federated | Permissionless | Permissionless |
| Identity | Phone number | MXID | Nostr keypair | Nostr keypair |
| Metadata protection | Sealed sender (server) | Server-side | Gift-wrapped Welcomes; ephemeral senders | NIP-17 gift wrap (DMs only) |
| Group join | Server-mediated | Federation handshake | KeyPackage from relay | N/A (no native groups) |
| Spec status | Closed | Open (Matrix MLS in dev) | Open spec, experimental | Mature for DMs |

---

## Why Marmot is interesting

- Plugs the group-messaging gap in Nostr. NIP-17 is a DM solution; Marmot is the answer when you have 50 friends in a chat and the protocol still has to work.
- Decentralized Signal-equivalent. The first protocol to combine MLS-grade crypto with permissionless infrastructure. Neither Signal nor Matrix offers that combination today.
- Identity reuse without compromise. The Nostr identity key is preserved; group-internal signing uses a distinct MLS key. Compromising one doesn't burn the other.
- Clean separation of layers. Identity (Nostr key) ≠ group signing key (MLS) ≠ encryption key (per-epoch derived). Each can rotate or be revoked independently.

---

## Trade-offs

### Strengths

- MLS scaling: log-cost group operations.
- Forward secrecy and post-compromise security, both real.
- No central server to subpoena or shut down.
- Metadata-protected group membership.
- Identity continuity with the rest of the Nostr ecosystem.

### Limitations

- Experimental. The spec is iterating; clients are early.
- Implementation complexity. MLS is a substantial library (OpenMLS in Rust, mls-rs from AWS).
- Race conditions on add. State-fork prevention requires careful timing of Commit confirmation before Welcome dispatch, easy to get wrong.
- Relay coverage required. A KeyPackage published only to a relay nobody else uses is invisible.
- Multi-device. MLS treats each device as a separate group member; a user with two devices joins a group twice.
- Backups and history sync. Not yet standardized; loss of device may mean loss of message history depending on client design.

---

## Implementation surfaces

- MLS library: OpenMLS (Rust), mls-rs (AWS, Rust). Both can be used with Marmot.
- Nostr library: any Nostr client SDK (rust-nostr, nostr-tools, NDK).
- Reference clients: White Noise (Rust + iOS Swift), some early Damus and 0xchat work.
- KeyPackage publishing: clients publish KeyPackages on app launch and rotate them periodically.

---

## Operational patterns

### Activist group with Nostr identities

Members already have npubs. They publish KeyPackages, an organizer creates a group, gift-wrapped Welcomes invite each member. All group communication flows through public Nostr relays as opaque ciphertext. Adding and removing members is an MLS Commit + Welcome flow; epochs advance.

### Multi-device join

Each device generates its own MLS signing key and publishes its own KeyPackage. The group has separate "Alice-on-phone" and "Alice-on-laptop" leaves. This is a feature for forward secrecy (compromise one device, the other still works) and a footgun for group size accounting.

### Hybrid with [FIPS](/off-grid-networks/fips)

Group communication over the FIPS mesh: KeyPackages discovered via Nostr relays accessible over FIPS, then group events flow over the mesh. End-to-end encrypted by Marmot, mesh-routable by FIPS, identity unified by the Nostr keypair.

---

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| KeyPackage exhaustion / reuse | `last_resort` extension for fallback; rotate eagerly |
| State fork on race | Strict Commit-confirmation-before-Welcome ordering |
| Compromised member exfiltrates ratchet | MLS PCS — eventually rotated out of group on next Commit |
| Relay denial of service | Multi-relay publishing; redundancy |
| Identity key compromise | Migrate via signed delegation; group recovery is application-defined |
| Endpoint compromise | Out of scope; standard hardening |

---

## Recent developments (2024-2026)

- MIP-00 through MIP-05 stabilization.
- White Noise reference clients (desktop and iOS).
- Damus integration experiments.
- OpenMLS version compatibility maintained.
- NIP-EE legacy: predecessor draft NIP for MLS-over-Nostr; superseded by Marmot's MIP organization.

---

## Related Files

- [Overview - Encrypted Messaging](/encrypted-messaging)
- [Nostr Deep Dive](/encrypted-messaging/nostr-deep-dive) — the underlying protocol from the messaging side.
- [Nostr](/identity/nostr) — Nostr from the identity side, including Marmot integration notes.
- [Signal Protocol Technical](/encrypted-messaging/signal-protocol-technical) — comparison reference.
- [Matrix and E2EE](/encrypted-messaging/matrix-and-e2ee) — the other federated alternative; Matrix's MLS profile is in development.
- [Metadata Resistance](/encrypted-messaging/metadata-resistance)
- [MOC - Composing Primitives](/meta/moc-composing-primitives)

---

## Primary Sources

- Marmot Protocol — [github.com/marmot-protocol/marmot](https://github.com/marmot-protocol/marmot) (MIP-00 through MIP-05).
- RFC 9420, *Messaging Layer Security*, IETF, 2023.
- RFC 9750, *MLS Protocol Architecture*.
- Cohn-Gordon et al., *On Ends-to-Ends Encryption: Asynchronous Group Messaging with Strong Security Guarantees* (TreeKEM origin), CCS 2018.
- NIP-59 (gift-wrap), NIP-44 (cipher), NIP-EE (legacy MLS-over-Nostr) — [github.com/nostr-protocol/nips](https://github.com/nostr-protocol/nips).
- OpenMLS — [github.com/openmls/openmls](https://github.com/openmls/openmls).
- mls-rs — [github.com/awslabs/mls-rs](https://github.com/awslabs/mls-rs).

