---
title: "Nostr (as Identity)"
tags:
  - "nostr"
  - "identity"
  - "npub"
  - "pubkey"
  - "deep-dive"
---
*A Nostr identity is just a secp256k1 keypair. No registrar, no platform, no issuer involved. This file looks at Nostr through the identity lens; the messaging side is in [Nostr Deep Dive](/encrypted-messaging/nostr-deep-dive).*

---

## Why identity comes first in Nostr

Most messaging protocols start with messaging and add identity later. Nostr did it the other way around: a public key is the account, and notes, DMs, zaps, and marketplaces are built on top of that. Nothing has to be allocated or approved. If you have the key, you have the identity. If you lose it, it's gone.

That makes Nostr a simpler identity primitive than the alternatives:

- Email is tied to an SMTP host that can shut you down.
- DNS names are issued by registrars.
- W3C DIDs work but are heavier and need method-specific resolvers.
- OIDC depends on the issuer continuing to exist and cooperate.

The trade-offs: there is no built-in human-readable name (Zooko's triangle), no native discovery, and losing the key means losing the account.

---

## The basic pieces

### `npub` and `nsec`

- `nsec` is a bech32-encoded private key (secp256k1).
- `npub` is the bech32-encoded x-only public key.
- Event payloads use the hex form; `npub` is what users see.

The `nsec` does everything: signing Nostr events, signing Lightning zap requests, signing FIPS routing announcements (see [FIPS](/off-grid-networks/fips)), and proving ownership in OIDC-replacement flows. One key, many uses.

### NIP-05 — human-readable handles

`alice@ungovernable.tech` resolves through `https://ungovernable.tech/.well-known/nostr.json` to an `npub`. It's an alias only; the key is still the real identity.

The trust is whatever TLS to that domain is worth, which means it falls back to DNS and the CA system. Ways to reduce that dependency:

- Serve NIP-05 over PKARR or Pubky, so the record is self-authenticating (see [Pubky](/identity/pubky)).
- Serve NIP-05 from a `.onion` address, removing DNS and CAs from the picture.
- Have clients pin the `npub` on first contact (TOFU), so a later DNS attack doesn't silently swap the key.

### NIP-26 — delegation

The key holder signs a token authorizing another key to sign specific event kinds for a limited time. Useful for:

- Hot signing keys that don't put the master key at risk.
- Per-device keys that don't expose the root.
- Application-specific signing scopes.

NIP-26 is well-defined but client support is patchy.

---

## Using one key across multiple devices

If your only key sits on a phone that gets compromised, you lose your identity. Common workarounds:

### Hardware-signed events

Coldcard, Keystone, and a few other hardware wallets added Nostr event signing in 2024 and 2025. The key never leaves the device; events are signed via QR or USB. The trade-off is signing latency.

### NIP-46 (Bunker)

A signer service holds the key, and the application calls a remote signing API. The signer can enforce policies: which event kinds are allowed, rate limits, approval prompts. It can run on:

- A separate device (phone, hardware wallet).
- A self-hosted server, with the key in a TEE (see [Overview - Confidential Computing](/confidential-computing)).
- A custodial service like Amber or Alby, which is convenient but means trusting a third party.

### Account recovery (FROST, draft NIP)

Threshold signatures (FROST) let `t` of `n` cosigners sign Nostr events together. Lose one share and you still have your identity. Production tooling is rolling out in 2025 and 2026.

---

## Knowing whose key is whose

There is no directory, so "is this `npub` really Alice?" is a real problem. The usual answers:

### Web of trust

Each user's follow graph and signed metadata form a trust graph. Tools like Vertex, Wikifreedia, and social.coracle.social use it to filter feeds, surface accounts your friends have verified, and reduce spam. See [Overview - Web of Trust](/cryptography/overview-web-of-trust).

### NIP-05 verification

Domain-bound aliases. Fine for low or moderate stakes, but vulnerable to DNS-level attacks.

### Cross-signing

A trusted root (for example, a journalist's known organization) signs an attestation that `npub X` belongs to person Y. Manual but high-assurance.

### Out-of-band (QR, in person)

The strongest option. Same idea as Briar's in-room key exchange.

---

## Marmot Protocol — group identity

[Marmot Protocol](/encrypted-messaging/marmot-protocol) (specified in MIPs at github.com/marmot-protocol) brings MLS to Nostr. For identity, this means:

- The Nostr pubkey is used as the MLS BasicCredential identity, so the same key works on the social side and the group-messaging side.
- Each member's group activity uses an MLS-derived signing key, separate from the main Nostr key. If a group-signing key is compromised, the Nostr identity itself is not.
- MLS provides forward secrecy and post-compromise security. Plain Nostr DMs (NIP-04 and NIP-17) do not.
- KeyPackage events (kind 30443) are publicly addressable invitations. The identity layer stays public; the group messaging stays end-to-end encrypted.

The practical effect is that Marmot lets you cleanly separate Nostr-the-identity-layer from Nostr-the-encryption-layer. Serious group messaging on Nostr basically requires this split.

---

## Things not to do

- **Use one `npub` for everything.** Signing a transaction, posting a hot take, and broadcasting a FIPS routing announcement with the same key makes all three linkable. Use NIP-26 delegation or per-context keys when that matters.
- **Hand your key to a custodian.** A "Nostr account" hosted by Amber, Damus, or Iris that holds your key is a custodian. Not your keys, not your identity.
- **Send `nsec` to a relay.** Relays only need signed events. If a relay sees an `nsec`, you've already lost.
- **Treat NIP-05 as authentication.** It's an alias, not a credential. Don't trust it for high-stakes verification without other corroboration.
- **Announce a new account by posting "I left, my new account is X" from the old one.** Without a cryptographic delegation, the protocol can't verify the link; followers have to re-establish trust by hand.

---

## How it composes with the rest of the vault

| Other primitive | Combined identity |
|-----------------|-------------------|
| [Pubky](/identity/pubky) | NIP-05 served over PKARR — DNS-free human-readable handles |
| [FIPS](/off-grid-networks/fips) | The same `npub` addresses your network nodes |
| **Lightning Network Deep Dive** | Zaps tie payments to a social identity |
| [Marmot Protocol](/encrypted-messaging/marmot-protocol) | Group messaging keyed to a social identity |
| [Overview - Confidential Computing](/confidential-computing) | An attested signing service holding `nsec` in a TEE |
| [Overview - Web of Trust](/cryptography/overview-web-of-trust) | Social-graph reputation built on raw `npubs` |

---

## Trade-offs

### What's good

- Identity is just a key. Nothing to allocate, register, or apply for.
- Easy to move. There's no "account migration" because the same key works anywhere.
- Composable across protocols. One key for many uses, with the linkability caveat.
- Open to anyone. New identity-related NIPs can ship without permission.

### What's hard

- Key custody is the whole game. Without prior planning, there's no recovery.
- Using a single key for everything makes you fully linkable by default.
- Discovery is hard. There's no directory, so bootstrapping needs WoT or out-of-band contact.
- Nostr is not a credential system. For issuer/verifier roles, use VCs or SD-JWT (see [Overview - Decentralized Identity](/identity/overview-decentralized-identity)).
- Sybil attacks are easy. Anyone can mint as many keys as they want.

---

## Attack surface

| Attack | What helps |
|--------|------------|
| Key extracted from a device | Hardware wallets; NIP-46 with a TEE-backed signer |
| NIP-05 DNS attack | Self-hosting, PKARR, `.onion` fallback |
| Social-engineered pubkey | Cross-signing, WoT, out-of-band confirmation |
| Sybil flood or spam | WoT-rooted feeds, paid relays, content filters |
| Cross-context linkability | Per-context keys, NIP-26 delegation |
| Compromised signing service | Use only attested or self-hosted signers |
| Quantum attack (future) | Migrating to a PQ signature scheme; no NIP yet |

---

## Recent developments (2024–2026)

- Marmot Protocol MIPs are stabilizing MLS-over-Nostr.
- Hardware-signed events on Coldcard, Keystone, and Foundation Passport.
- NIP-46 Bunker widely supported (Amber, Nsec.app).
- FROST and threshold-Nostr experiments for multi-party key custody.
- NIP-05 served over PKARR via Pubky integration.

---

## Related files

- [Nostr Deep Dive](/encrypted-messaging/nostr-deep-dive) — the protocol from the messaging side.
- [Pubky](/identity/pubky) — a sibling identity model using PKARR resolution.
- [Marmot Protocol](/encrypted-messaging/marmot-protocol) — MLS group messaging on Nostr keys.
- [Overview - Web of Trust](/cryptography/overview-web-of-trust)
- [Overview - Decentralized Identity](/identity/overview-decentralized-identity)
- [Overview - Identity & Pseudonymity](/identity)
- [FIPS](/off-grid-networks/fips)
- **Hardware Wallet Guide**

---

## Primary sources

- fiatjaf, *Nostr — Notes and Other Stuff Transmitted by Relays*, 2020. [github.com/nostr-protocol/nostr](https://github.com/nostr-protocol/nostr)
- NIPs registry — [github.com/nostr-protocol/nips](https://github.com/nostr-protocol/nips)
- NIP-05, NIP-26, NIP-46 specifications.
- Marmot Protocol MIPs — [github.com/marmot-protocol/marmot](https://github.com/marmot-protocol/marmot)
- FROST — Komlo & Goldberg, *FROST: Flexible Round-Optimized Schnorr Threshold Signatures*, IACR 2020/852.

