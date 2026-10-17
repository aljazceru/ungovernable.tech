---
title: "OPAQUE and PAKEs"
slug: opaque-and-pake
type: deep-dive
pillars: ["cryptography"]
readiness: usable
description: "Password-authenticated key exchange and OPAQUE: logging in with a password without the server ever learning it, standardised by the IETF."
dek: "Password-Authenticated Key Exchange: protocols where two parties agree on a strong shared key from a low-entropy password, without ever sending the password (or anything offline-attackable) over the wire. The asymmetric variants (aPAKE) further ensure the server stores no usable password equivalent."
updated: 2026-04-26
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
- In aPAKE variants, the server stores a value that does not enable a server-side dictionary attack.

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
| Symmetric PAKE (e.g. CPace) | shared password | yes (both sides equivalent) | RFC 9710 (2024) |
| aPAKE (e.g. SRP, OPAQUE) | a verifier (one-way) | depends on construction | varies |
| Strong aPAKE (OPAQUE) | OPRF-blinded envelope | no offline crack pre-compromise | RFC 9807 (2025) |

The "strong" qualifier matters: vanilla aPAKE schemes including SRP allow a server-side breach to enable offline dictionary attacks. OPAQUE is the first widely-adopted PAKE that resists this.

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

Haase and Labrique, *AuCPace*. Standardized as **RFC 9710** (April 2024) under the CFRG CPace track. Symmetric PAKE — both parties hold the password, no server-stored verifier asymmetry.

```
both parties:  G = hash_to_curve(password, sid, ad)
client:        ya ←$ scalar; Ya = ya · G
server:        yb ←$ scalar; Yb = yb · G
shared:        K = ya · Yb = yb · Ya
```

Use cases: device pairing (Bluetooth-style PIN), key escrow recovery between two devices the same user holds, two-party flows where a stored verifier doesn't fit the trust model. Not the right tool for client-server account login at scale (use OPAQUE).

## OPAQUE

Jarecki, Krawczyk and Xu, *OPAQUE: An Asymmetric PAKE Protocol Secure Against Pre-Computation Attacks*, EUROCRYPT 2018. Standardized as **RFC 9807** (March 2025) after a multi-year CFRG draft process.

Core idea: combine an Oblivious PRF (OPRF) with an authenticated key exchange. Registration:

```
client:  rwd = H(password, OPRF(server_oprf_key, password))
client:  envelope = AEAD(rwd, key_pair_for_login)
client → server: store(envelope, oprf_key_per_user)
```

Login:

```
client → server: OPRF eval blind for password
server → client: oprf_response (without learning password)
client:  rwd = H(password, OPRF eval)
client:  decrypt envelope → long-term keypair
both:   AKE using the keypair
```

Properties:

- Server never sees the password or anything from which it can derive the password offline. The OPRF binds the password evaluation to the server's secret OPRF key, which is what blocks pre-computation: an attacker who steals the database must still query a (potentially rate-limited) OPRF online for each guess, or must additionally steal the OPRF key.
- Even with both database and OPRF key stolen, the work factor is one OPRF per guess plus one AEAD decryption — defenders can pick a slow OPRF and a memory-hard KDF (Argon2id) inside the envelope to make brute force expensive.
- Composable AKE: the IETF spec permits 3DH and HMQV-style instantiations. Reference uses 3DH over `ristretto255` or `decaf448`.

### Cipher suites in RFC 9807

| Suite | Group | OPRF | AKE | Hash |
|-------|-------|------|-----|------|
| `OPAQUE-3DH-Ristretto255-SHA512` | ristretto255 | ristretto255 OPRF | 3DH | SHA-512 |
| `OPAQUE-3DH-Decaf448-SHAKE256` | decaf448 | decaf448 OPRF | 3DH | SHAKE-256 |
| `OPAQUE-3DH-P256-SHA256` | NIST P-256 | P-256 OPRF | 3DH | SHA-256 |
| `OPAQUE-3DH-P384-SHA384` | NIST P-384 | P-384 OPRF | 3DH | SHA-384 |
| `OPAQUE-3DH-P521-SHA512` | NIST P-521 | P-521 OPRF | 3DH | SHA-512 |

## Production deployments

### WhatsApp encrypted backups (2021)

WhatsApp shipped end-to-end encrypted iCloud/Google Drive backups in 2021 using an HSM-backed PAKE-like protocol. Public materials describe a flow consistent with an OPRF + envelope (an OPAQUE-class design), with the OPRF evaluated by an HSM array. Offline attacks against the HSM-locked secrets are blocked unless an attacker compromises the HSM. This was a flagship deployment that pushed CFRG to finalize OPAQUE as a standard.

Source: WhatsApp engineering whitepaper, *Security of End-to-End Encrypted Backups*, 2021.

### Cloudflare and the Privacy Pass adjacency

Cloudflare's research org has deployed OPAQUE and the OPRF subprotocol in multiple contexts. The OPRF used inside OPAQUE shares the construction with VOPRF in [VRFs](/kb/verifiable-random-functions/)-adjacent privacy-pass tokens.

### Passwordless / device-binding flows

Modern passkey-style auth (WebAuthn, FIDO2) competes with OPAQUE on the same problem space. OPAQUE is a *password-based* protocol; passkeys remove the password entirely. The two coexist: OPAQUE is appropriate when a user's master secret must be a memorized password (encrypted-backup unlock, threshold custody recovery), passkeys are better when device-bound public-key auth is acceptable.

## Comparison

| Property | SRP | CPace | OPAQUE |
|----------|-----|-------|--------|
| Asymmetric (server-only verifier) | yes | no | yes |
| Strong aPAKE (no offline crack from DB) | no | n/a | **yes** |
| RFC | 2945, 5054 (TLS) | 9710 | **9807** |
| Curve choice | discrete-log group | EC | EC |
| Round trips | 2 | 2 | 3 (registration) / 2 (login) |
| OPRF dependency | none | none | required |
| Production scale | legacy at 1Password, Apple | newer | WhatsApp backups |
| Recommended for new use | no | device pairing only | yes (login + envelope) |

## Security assumptions

- OPAQUE: OPRF security (one-more-DH or analogous), AKE security of the underlying 3DH, AEAD soundness, KDF irreducibility. The 2018 paper's UC-style proof has been refined through CFRG review.
- Side-channel: hash-to-curve in the OPRF must be constant-time (RFC 9380 SSWU/Elligator2).
- Quantum: all listed PAKEs are broken by Shor on the elliptic-curve operations. Lattice-based PAKE constructions exist (e.g., Beguinet et al. 2023) but no IETF-blessed cipher suite as of 2026.

## Pitfalls

- **Don't roll your own.** PAKE has historically broken under subtle modifications. Use audited libraries (`opaque-ke` in Rust, Cloudflare's reference, the `voprf` crate).
- **Salt and parameters must be deterministic per user.** Generating fresh salts on each login defeats aPAKE.
- **Argon2id inside the envelope is recommended** so that even if both DB and OPRF key leak, the per-guess cost is high.
- **TLS underneath is still required** for transport-level integrity and replay protection — OPAQUE is not a substitute for TLS.

## Primary sources

- Wu, *The SRP Authentication and Key Exchange System*, RFC 2945 (Sep 2000).
- Taylor, Wu, Mavrogiannopoulos, Perrin, *Using SRP for TLS Authentication*, RFC 5054 (Nov 2007).
- Jarecki, Krawczyk, Xu, *OPAQUE: An Asymmetric PAKE Protocol Secure Against Pre-Computation Attacks*, EUROCRYPT 2018.
- Bourdrez, Krawczyk, Lewi, Wood, *The OPAQUE Asymmetric PAKE Protocol*, RFC 9807 (Mar 2025).
- Haase, Labrique, *CPace, a Balanced Composable PAKE*, RFC 9710 (Apr 2024).
- WhatsApp, *Security of End-to-End Encrypted Backups*, 2021 whitepaper.
- `opaque-ke` (Rust): [github.com/facebook/opaque-ke](https://github.com/facebook/opaque-ke).
- CFRG VOPRF: RFC 9497 (Dec 2023).
