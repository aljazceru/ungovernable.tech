---
title: "OPAQUE and PAKEs"
slug: opaque-and-pake
type: deep-dive
pillars: ["cryptography"]
readiness: usable
description: "Password-authenticated key exchange and OPAQUE: logging in with a password without the server ever learning it, standardised by the IETF."
dek: "Password-Authenticated Key Exchange: protocols where two parties agree on a strong shared key from a low-entropy password, without ever sending the password (or anything offline-attackable) over the wire. The asymmetric variants (aPAKE) further ensure the server stores no usable password equivalent."
updated: 2026-10-25
created: 2026-04-26
origin: vault
source: "02-Cryptography/OPAQUE and PAKE.md"
aliases: ["PAKE", "aPAKE", "OPAQUE"]
tags: ["pake", "opaque", "srp", "cpace", "password", "authentication", "cryptography", "deep-dive"]
---

## Why PAKE exists

The TLS-then-send-password pattern leaks the password to anyone who can compromise the server, the TLS certificate, or any middlebox the server trusts. Even with TLS, a server breach exposes hashed passwords for offline cracking. PAKE replaces this with a protocol where:

- The protocol transcript leaks no information enabling offline password guessing.
- Each session yields a key only obtainable by parties who knew the password during the exchange.
- In aPAKE variants, the server stores a registration record instead of the plaintext password. Full server compromise can still permit offline password guessing.

The shared abstraction:

```
client(password)        server(verifier or password-hash)
       │                          │
       ├──── round(s) ───────────┤
       │                          │
       └─→ shared key K ←─────────┘    (only with correct password)
```

## Categories

| Category | Server stores | Stolen DB enables offline crack | Standardized |
|----------|---------------|---------------------------------|--------------|
| Symmetric PAKE (e.g. CPace) | shared password | yes (both sides equivalent) | CFRG Internet-Draft |
| aPAKE (e.g. SRP, OPAQUE) | a verifier (one-way) | depends on construction | varies |
| Strong aPAKE (OPAQUE) | OPRF-blinded envelope | resists precomputation; full compromise permits guessing | RFC 9807 (2025) |

OPAQUE resists precomputed password attacks before server compromise. After full compromise, including the server’s OPRF secret, an attacker can test guesses offline; key stretching raises the cost per guess.

## SRP (Secure Remote Password)

Wu, *The SRP Authentication and Key Exchange System*, RFC 2945 (Sep 2000). TLS-SRP extension in **RFC 5054** (2007).

Stores a verifier `v = g^x mod N` where `x = H(salt, username, password)`. Login uses a Diffie-Hellman-like exchange so the password is never sent.

Limitations (motivated OPAQUE):

- Pre-computation attacks possible if salt is sent before authentication.
- Verifier `v` allows offline dictionary attacks once the database is leaked (an attacker guesses `password`, computes `v`, compares).
- Custom group arithmetic, fragile against implementation mistakes.
- No clean elliptic-curve variant that the IETF blessed.

Despite the warts, SRP is in production at 1Password (key-derivation handshake), Apple iCloud Keychain (legacy), and various enterprise SSO products. Replacements are slow because deployments are long-lived.

## CPace

CPace is specified in the CFRG Internet-Draft `draft-irtf-cfrg-cpace`. Symmetric PAKE — both parties hold the password, no server-stored verifier asymmetry.

```
both parties:  G = hash_to_curve(password, sid, ad)
client:        ya ←$ scalar; Ya = ya · G
server:        yb ←$ scalar; Yb = yb · G
shared:        K = ya · Yb = yb · Ya
```

Use cases: device pairing (Bluetooth-style PIN), key escrow recovery between two devices the same user holds, two-party flows where a stored verifier doesn't fit the trust model. Not the right tool for client-server account login at scale (use OPAQUE).

## OPAQUE

Jarecki, Krawczyk and Xu, *OPAQUE: An Asymmetric PAKE Protocol Secure Against Pre-Computation Attacks*, EUROCRYPT 2018. Published as the informational IRTF **RFC 9807** (July 2025) after a multi-year CFRG draft process.

Core idea: combine an Oblivious PRF (OPRF), credential recovery, and authenticated key exchange. The client blinds its password for the OPRF exchange, derives a randomized password, and uses it to recover authentication credentials. The server does not receive the plaintext password, including during registration.

RFC 9807’s envelope contains a nonce and authentication tag. The client derives its private key and authenticates the associated credentials; the envelope is not simply an AEAD-encrypted private-key blob.

The RFC specifies a 3DH instantiation. Implementations must agree on the OPRF, group, hash, KDF, MAC and key-stretching parameters. Full server compromise permits offline guessing, while separating the OPRF secret into a rate-limited protected service can change that deployment’s compromise boundary.

## Production deployments

### WhatsApp encrypted backups (2021)

WhatsApp’s published encrypted-backup design uses OPAQUE to authenticate password-based access to a backup-key vault protected by HSMs. Its guessing limits depend on that protected service, not on OPAQUE eliminating offline guessing after full compromise.

### Cloudflare and the Privacy Pass adjacency

Cloudflare's research org has deployed OPAQUE and the OPRF subprotocol in multiple contexts. The OPRF used inside OPAQUE shares the construction with VOPRF in [VRFs](/kb/verifiable-random-functions/)-adjacent privacy-pass tokens.

### Passwordless / device-binding flows

Modern passkey-style auth (WebAuthn, FIDO2) competes with OPAQUE on the same problem space. OPAQUE is a *password-based* protocol; passkeys remove the password entirely. The two coexist: OPAQUE is appropriate when a user's master secret must be a memorized password (encrypted-backup unlock, threshold custody recovery), passkeys are better when device-bound public-key auth is acceptable.

## Comparison

| Property | SRP | CPace | OPAQUE |
|----------|-----|-------|--------|
| Asymmetric (server-only verifier) | yes | no | yes |
| Resists password precomputation before server compromise | no | n/a | **yes** |
| Specification | RFC 2945, 5054 (TLS) | CFRG CPace draft | RFC 9807 (informational) |
| Curve choice | discrete-log group | EC | EC |
| Round trips | 2 | 2 | 3 (registration) / 2 (login) |
| OPRF dependency | none | none | required |
| Production scale | legacy at 1Password, Apple | newer | WhatsApp backups |
| Recommended for new use | no | device pairing only | yes (login + envelope) |

## Security assumptions

- OPAQUE: OPRF security (one-more-DH or analogous), AKE security of the underlying 3DH, MAC and KDF security. The 2018 paper's UC-style proof has been refined through CFRG review.
- Side-channel: hash-to-curve in the OPRF must be constant-time (RFC 9380 SSWU/Elligator2).
- Quantum: all listed PAKEs are broken by Shor on the elliptic-curve operations. Lattice-based PAKE constructions exist (e.g., Beguinet et al. 2023) but no IETF-blessed cipher suite as of 2026.

## Pitfalls

- **Don't roll your own.** PAKE has historically broken under subtle modifications. Use audited libraries (`opaque-ke` in Rust, Cloudflare's reference, the `voprf` crate).
- **Salt and parameters must be deterministic per user.** Generating fresh salts on each login defeats aPAKE.
- **Use the agreed key-stretching function** so that even if both DB and OPRF key leak, the per-guess cost is high.
- **TLS underneath is still required** for transport-level integrity and replay protection — OPAQUE is not a substitute for TLS.

## Primary sources

- [RFC 2945: The SRP Authentication and Key Exchange System](https://www.rfc-editor.org/rfc/rfc2945.html)
- [RFC 5054: Using SRP for TLS Authentication](https://www.rfc-editor.org/rfc/rfc5054.html)
- [OPAQUE: An Asymmetric PAKE Protocol Secure Against Pre-Computation Attacks](https://eprint.iacr.org/2018/163)
- [RFC 9807: The OPAQUE Asymmetric PAKE Protocol](https://www.rfc-editor.org/rfc/rfc9807.html)
- [CFRG: CPace, a balanced composable PAKE](https://datatracker.ietf.org/doc/draft-irtf-cfrg-cpace/)
- [opaque-ke implementation](https://github.com/facebook/opaque-ke)
- [RFC 9497: OPRFs using prime-order groups](https://www.rfc-editor.org/rfc/rfc9497.html)
- [WhatsApp: encrypted backups design](https://engineering.fb.com/2021/09/10/security/whatsapp-e2ee-backups/)
