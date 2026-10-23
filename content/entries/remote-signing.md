---
title: "Remote Signing (NIP-46 and Friends)"
slug: remote-signing
type: deep-dive
pillars: ["identity", "endpoint"]
readiness: usable
description: "Remote signers and bunkers (NIP-46 and others) keep Nostr private keys on one device and sign for many apps, ending the habit of pasting keys."
dek: "The ecosystem that replaced \"paste your nsec into every client\" with proper key custody. NIP-46 bunkers, NIP-07 browser extensions, Amber on Android, hardware-wallet signing — same goal, different threat models. This file maps the landscape and the trust calculus for each option."
updated: 2026-04-26
created: 2026-04-26
origin: vault
source: "11-Identity/Remote Signing.md"
aliases: ["NIP-46", "Nsec Bunker", "Nostr Connect", "Remote Signers"]
tags: ["nostr", "nip-46", "nip-07", "bunker", "amber", "remote-signer", "key-custody", "deep-dive"]
---

## Why remote signing matters for Nostr

A Nostr identity is just a secp256k1 keypair (see [Nostr](/kb/nostr-identity/)). The `nsec` (private key) does everything: signs DMs, posts, zap requests, profile updates, FIPS routing announcements. Whoever has the `nsec` *is* the identity.

The early UX was disastrous: every Nostr client wanted the user to paste the `nsec` into a text field on first run. Web apps, mobile apps, browser tabs, all asking for the secret key. This violated every principle of key custody:

- A malicious or compromised client steals the key.
- The user has no idea how many clients hold their key.
- Revocation is impossible — Nostr identity is the key.
- Multi-device use means the key is in N places, each a separate compromise vector.

Remote signing fixes this. The signer holds the `nsec`; clients request signatures over the wire. The client never sees the key. This pattern aligns Nostr's UX with how modern wallets, password managers, and SSH agents work.

## NIP-07 — browser extension signers

**NIP-07** ("Window.nostr capability for web browsers") defines a browser API that web Nostr clients can call to request signatures from a browser extension. Spec: `github.com/nostr-protocol/nips/blob/master/07.md`.

```javascript
// Web client never touches the key directly:
const event = await window.nostr.signEvent({
    kind: 1,
    content: "hello world",
    tags: [],
    created_at: Math.floor(Date.now() / 1000),
});
```

The extension holds the key, prompts the user for confirmation (or auto-approves whitelisted origins), and returns the signed event.

### Implementations

| Extension | Notes |
|-----------|-------|
| **Alby** (`getalby.com`) | Browser extension and self-hosted hub; also handles Lightning. Acquired by Open Sats steward; multi-key support. |
| **nos2x** (`github.com/fiatjaf/nos2x`) | Minimal reference implementation by fiatjaf. |
| **Flamingo** | Newer entrant; emphasis on multi-account UX. |
| **Nostore (iOS)** | Safari extension equivalent. |
| **Horse** | Chrome extension with security-focused defaults. |

### Threat model

- Key sits in the browser extension's storage (encrypted with a password, ideally).
- Web origin is checked; per-site approval prompts.
- Compromised browser or extension stack leaks the key.
- No hardware isolation. A determined attacker with browser access wins.

NIP-07 is the **convenience tier**: better than pasting nsec, worse than hardware. Acceptable for low-stakes identities (casual social posting, low-value zaps).

## NIP-46 — Nostr Connect (the bunker pattern)

**NIP-46** ("Nostr Connect / Remote Signing") is the protocol for remote signing over Nostr relays. Spec: `github.com/nostr-protocol/nips/blob/master/46.md`.

The flow:

```
Client (e.g., a web app)             Bunker (signer service)
    │                                       │
    │  Pairing: user pastes bunker URI      │
    │  ─────────────────────────────────►   │
    │                                       │  (User on bunker
    │                                       │   side approves)
    │                                       │
    │  signEvent(unsigned_event) request    │
    │  ───── via Nostr relay (encrypted) ─► │
    │                                       │  (Bunker signs)
    │  signed_event response                │
    │  ◄──── via Nostr relay (encrypted) ── │
    │                                       │
```

Key properties:

- **Transport is Nostr relays.** Both sides connect to a shared relay; messages are encrypted (NIP-04 / NIP-44 ChaCha20-Poly1305 to a session key).
- **Pairing**: the user gets a `bunker://` or `nostrconnect://` URI from the bunker, pastes it into the client. The URI contains the bunker's signing pubkey and a connection secret.
- **The client never sees the nsec.** It only sends unsigned events to the bunker and gets signed events back.
- **The bunker can enforce policy**: rate limits, allowed event kinds, approval prompts before signing.

### Bunker implementations

| Bunker | Where it runs | Threat model |
|--------|--------------|--------------|
| **Amber** (Android) | User's phone | Key on phone; signing requires explicit approval per request. Strong UX. |
| **Nsec.app** (`nsec.app`) | Self-hosted web bunker | Lightweight web app; key in browser local storage. Casual use. |
| **Bunker.app** | Hosted service | Convenience custodial; trusts the operator. |
| **Nsecbunker** (`github.com/kind-0/nsecbunkerd`) | Self-hosted daemon | Server-side bunker; key in a TEE-friendly process; multi-user policy. |
| **Keychat / Khatru-bunker** | Self-hosted | Variations on the daemon pattern. |

### Self-hosted bunker in a TEE

A pattern increasingly discussed: run the bunker inside a TEE (Intel TDX, AMD SEV-SNP, AWS Nitro Enclaves) so the key is hardware-isolated. The bunker exposes signing via NIP-46; the TEE attests to its code so the user can verify the bunker isn't a malicious copy. See [Overview - Confidential Computing](/kb/confidential-computing/).

This gives:
- Hardware key isolation.
- Remote signing UX from any client.
- Verifiable bunker code (no rogue admin extracting the key).

It's the best-of-both-worlds option for users with serious operational threat models.

### Threat model for NIP-46

- The bunker holds the key. Compromise of the bunker = compromise of the identity.
- The relay sees encrypted traffic. Choose relays you trust not to log metadata.
- Pairing leaks the bunker pubkey (which is the signing key in some implementations) — a privacy concern, not a security one.
- Replay attacks are mitigated by per-session keys and timestamp validation.
- A compromised client can request many signatures; bunker policy (rate limit, kind filter, approval prompts) is the defense.

## Amber (Android) — the deep dive

**Amber** (`github.com/greenart7c3/Amber`) is the dominant Android signer. It's not just a NIP-46 client; it can also act as a system-wide intent target, so any Nostr client on Android can request a signature via Android's intent mechanism.

Architecture:

- Key stored on Android device, encrypted with a user-set password / biometric.
- Signing requests come in via Android intents (local IPC) or NIP-46 (relay-based).
- Each request prompts the user (or follows policy: auto-approve specific event kinds for whitelisted apps).
- Multi-account support; one Amber install can hold many nsecs.

For Android Nostr users, Amber is the de-facto standard. UX is comparable to a password manager.

iOS lacks an Amber equivalent (Apple's intent system is more locked-down); iOS users typically use NIP-46 to a web bunker or a desktop signer.

## Hardware-wallet signing

The strongest custody option: the key never leaves a hardware wallet.

### Coldcard

Coldcard added Nostr event signing in firmware 5.x (2024). Workflow:

1. Generate Nostr key on Coldcard, derived from BIP-39 seed via a Nostr-specific derivation path.
2. Construct unsigned event on a desktop client.
3. Pass to Coldcard via QR code or microSD.
4. Coldcard displays event content for review.
5. User confirms; Coldcard returns signed event.

The signing latency is meaningful (10-30 seconds per event), so Coldcard is impractical for high-frequency posting. It's the cold-storage option for high-stakes Nostr identities (long-form publishing, key witnesses, organizational accounts).

### Foundation Passport

Passport added Nostr signing capabilities (2024-2025). Similar QR-based UX. Targets Bitcoin-Nostr users who want unified hardware key management.

### Keystone

Keystone Pro added Nostr signing support. Air-gapped QR workflow.

### Research: PSBT-like Nostr signing

A research direction: a "**NSBT**" (Nostr-equivalent of PSBT) format that lets multiple parties contribute to event construction (e.g., multisig FROST signing) and pass partially-signed events between hardware devices and software clients. As of early 2026, this is exploratory; no standard exists.

## Comparison table

| Approach | Key custody | UX | Trust assumption | Best for |
|----------|------------|----|----|----------|
| **Pasted nsec (legacy)** | Every client | Easy | Trust every app forever | **Don't do this** |
| **NIP-07 extension** | Browser extension | Easy | Trust browser + extension | Casual social, web only |
| **NIP-46 hosted bunker** | Bunker operator | Easy | Trust bunker operator | Convenience custodial |
| **NIP-46 self-hosted** | Your server | Medium | Trust your own infra | Self-sovereign default |
| **NIP-46 TEE bunker** | Attested TEE | Medium | Trust hardware vendor | High-stakes self-sovereign |
| **Amber (Android)** | Phone | Easy | Trust phone OS | Mobile-first users |
| **Hardware wallet (Coldcard, Passport)** | Air-gapped HW | Slow | Trust hardware vendor | Cold-storage, high-stakes |
| **FROST threshold (Frostr, draft NIP)** | Distributed | Hard | Trust threshold of cosigners | Group / org accounts |

## Threshold signing — Frostr / FROST-Nostr

A future-facing direction: **FROST** (Komlo & Goldberg, IACR 2020/852) threshold Schnorr signatures, applied to secp256k1 Nostr keys. The Frostr proposal (`github.com/cmdruid/frost`) and related drafts let `t-of-n` cosigners produce a Nostr signature without ever reconstructing the full nsec.

Use cases:

- **Personal**: split your key 2-of-3 across phone, laptop, hardware wallet. Lose one device, identity survives.
- **Organizational**: a Nostr account controlled by 3-of-5 board members.
- **Custody-as-a-service**: a user holds 1-of-3 shares; a custodian holds 2-of-3 but can't sign without the user.

This intersects with [Threshold Signatures](/kb/threshold-signatures/) (forthcoming) and is relevant to [Marmot Protocol](/kb/marmot-protocol/) group identity.

As of early 2026: tooling is alpha. Production-grade UX is at least 6-12 months out.

## Marmot and remote signing

[Marmot Protocol](/kb/marmot-protocol/) (MLS over Nostr) signs **a lot**: every group operation, every welcome, every commit. A user in 5 active Marmot groups might generate dozens of signatures per day. This makes:

- **Hardware-wallet signing** impractical for Marmot (too many prompts).
- **NIP-07 / NIP-46** the right fit, with policy: auto-approve Marmot event kinds for the Marmot client.
- **TEE bunkers** especially attractive: hardware-isolated key + high-frequency signing without UX friction.

A typical recommendation: hardware wallet for high-stakes events (profile changes, account rotations, kind-0 metadata), NIP-46 or Amber for everything else. The signer's policy distinguishes between event kinds.

## Threat models in practice

| You're worried about | Solution |
|---------------------|----------|
| Casual key theft from sketchy web apps | NIP-07 or NIP-46 |
| Your laptop is compromised | NIP-46 to phone (Amber) or TEE bunker |
| Your phone is compromised | Hardware wallet for high-value signatures |
| Targeted attack against you specifically | TEE bunker + hardware wallet for cold ops |
| Account takeover (key theft) | FROST threshold (when production-ready) |
| Coercion (someone forces you to sign) | Threshold with one party offline / abroad |
| Mass surveillance of relay metadata | Use Tor / `.onion` relays for bunker traffic |

## Trade-offs

### Strengths of remote signing generally

- Removes the "every client holds your nsec" footgun.
- Makes high-stakes Nostr accounts viable (organizations, journalists, whistleblowers).
- Enables policy enforcement (rate limits, approval prompts, kind whitelists).
- Composable with hardware isolation (TEE, hardware wallets).
- NIP-46's relay-based transport works across NAT, firewalls, anywhere Nostr works.

### Limitations

- More moving parts. A bunker is one more thing to operate or trust.
- Latency. Every signature is a round-trip via relay.
- Bunker compromise is identity compromise. Operational discipline matters.
- UX is still rough for non-technical users.
- iOS lacks an Amber equivalent.
- Hardware-wallet flow is too slow for active Nostr use.

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Bunker server compromise | Self-host; run in a TEE; minimize attack surface |
| Compromised client requests many signatures | Bunker policy: rate limit, approval prompts, kind whitelist |
| Pairing URI leaked | Single-use pairing tokens; rotate connection secrets |
| Relay logs metadata | Use trusted relays; route bunker traffic over Tor |
| Hardware-wallet supply-chain attack | Verify firmware signatures; buy direct from vendor |
| User social-engineered into approving malicious request | Bunker UX shows full event content before signing |

## Primary sources

- fiatjaf et al., *Nostr Implementation Possibilities*, `github.com/nostr-protocol/nips`.
- NIP-07: *window.nostr capability for web browsers*. `github.com/nostr-protocol/nips/blob/master/07.md`.
- NIP-46: *Nostr Connect / Remote Signing*. `github.com/nostr-protocol/nips/blob/master/46.md`.
- NIP-44: *Versioned encryption*. `github.com/nostr-protocol/nips/blob/master/44.md`.
- Komlo, Goldberg, *FROST: Flexible Round-Optimized Schnorr Threshold Signatures*, IACR ePrint 2020/852.
- Amber — `github.com/greenart7c3/Amber`.
- Nsecbunker — `github.com/kind-0/nsecbunkerd`.
- Alby — `github.com/getAlby/lightning-browser-extension`.
- nos2x — `github.com/fiatjaf/nos2x`.
- Frostr — `github.com/cmdruid/frost`.
- Coldcard Nostr signing release notes — `coldcard.com/docs`.
