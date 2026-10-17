---
title: "age: Modern File Encryption"
slug: age-encryption
type: deep-dive
pillars: ["endpoint", "cryptography"]
readiness: battle-tested
description: "age is a small, modern file-encryption tool built on X25519 and ChaCha20-Poly1305: how it works, how to use it, and where it beats PGP for files."
dek: "A small, opinionated file-encryption format and CLI. Built around X25519 recipient keys, ChaCha20-Poly1305 streaming, and HMAC-SHA-256 header authentication. Designed as a replacement for `gpg -c` and ad-hoc OpenSSL pipelines for everyday encryption-at-rest."
updated: 2026-04-26
created: 2026-04-26
origin: vault
source: "02-Cryptography/age Toolchain.md"
aliases: ["age", "actually-good-encryption", "rage"]
tags: ["age", "encryption", "file-encryption", "x25519", "chacha20", "cryptography", "deep-dive"]
---

## Origin and scope

age (lowercase) was designed by Filippo Valsorda and Ben Cartwright-Cox starting 2019. The reference implementation `filippo.io/age` is in Go; the format spec lives at [age-encryption.org/v1](https://age-encryption.org/v1) (originally [c2sp/age](https://github.com/C2SP/C2SP/tree/main/age)). A Rust implementation, **rage** by Jack Grigg, tracks the same spec.

Stated goals:

- One file format, one set of cipher choices, no algorithm negotiation.
- Public-key recipient model — encrypt to keys, not to users.
- No signatures. Authenticity comes from key possession, not identity.
- Pluggable identities (smart cards, TPMs, FIDO2) without changing the wire format.

Stated non-goals:

- Long-term archive standardization on the level of CMS/OpenPGP.
- Revocation, key servers, web-of-trust.
- Embedded metadata (filename, timestamps).

## Format

Specified at [age-encryption.org/v1](https://age-encryption.org/v1). Header:

```
age-encryption.org/v1
-> X25519 <recipient-ephemeral-public-key>
<wrapped file key>
-> X25519 <next-recipient>
<wrapped file key>
--- <HMAC-SHA-256(header[:-mac])>
```

Each `->` stanza is a *recipient stanza*. The "file key" is a 16-byte symmetric key; each recipient stanza wraps it for one recipient. The HMAC line is keyed by an HKDF derivation from the file key, authenticating the entire header so a recipient cannot be tampered with or removed.

After the header, the payload is encrypted with ChaCha20-Poly1305 in 64 KiB chunks, each with a counter nonce and a "last chunk" flag in the final byte. Streaming is real: encryption and decryption don't need the whole file in memory.

Recipient types defined in v1:

- **X25519** — direct public-key recipient.
- **scrypt** — passphrase-only mode (no public-key recipient; key derived from passphrase).
- **ssh-rsa**, **ssh-ed25519** — derive an X25519 key from an SSH key for casual reuse.

Plugins extend the recipient stanza set without bumping the format version.

## Cipher choices

| Component | Algorithm | Why |
|-----------|-----------|-----|
| ECDH | X25519 (RFC 7748) | Fast, misuse-resistant, nothing-up-my-sleeve curve |
| KDF | HKDF-SHA-256 | Standard, simple |
| AEAD (chunks) | ChaCha20-Poly1305 (RFC 8439) | Fast in software, no AES-NI assumption |
| Header MAC | HMAC-SHA-256 | Authenticates the recipient list |
| Passphrase mode | scrypt | Memory-hard, well-studied |

No AES-GCM, no NIST P-curves, no choice of mode. Everything is fixed.

## Plugin ecosystem

Plugins implement custom recipient and identity types. The CLI invokes `age-plugin-<name>` over stdio in a documented protocol; the file format remains unchanged. Notable plugins:

| Plugin | Backend | Status (2026) |
|--------|---------|---------------|
| `age-plugin-yubikey` | YubiKey PIV (NIST P-256 ECDH) | mature, by Jack Grigg |
| `age-plugin-tpm` | TPM 2.0 sealed key | active |
| `age-plugin-fido2-hmac` | FIDO2 hmac-secret extension | active |
| `age-plugin-se` | Apple Secure Enclave (P-256) | active, macOS-only |
| `age-plugin-ledger` | Ledger hardware wallet | community |
| `age-plugin-1p` | 1Password CLI | community |
| `age-plugin-sss` | Shamir secret sharing | community |

This decoupling is what makes age viable across hardware boundaries. The CLI doesn't need to know about YubiKey internals; the plugin negotiates with the device and returns a wrapped file key in the standard format.

## Implementations

| Implementation | Language | Notes |
|----------------|----------|-------|
| `filippo.io/age` | Go | reference |
| **rage** | Rust | feature-equivalent, used by `agenix` and others |
| `pyrage` | Python (Rust binding) | bindings to rage |
| `typage` | TypeScript | browser/Node |
| `age` (Java/Kotlin), `age-rs`, etc. | various | community |

Reference: [github.com/FiloSottile/age](https://github.com/FiloSottile/age), rage at [github.com/str4d/rage](https://github.com/str4d/rage).

## Use cases

### Backup encryption

Encrypt a tarball to one or more X25519 recipient keys before pushing to S3/Backblaze/IPFS. Each backup file's recipient set is decoupled from any user identity. Adding a new recovery key means re-encrypting only the header (no plaintext re-encryption) — a common operation that age does not provide directly; in practice you re-encrypt the file or maintain a small encrypted-file-key envelope.

### Deployment secrets

Tools like **agenix** (Nix), **sops** (Mozilla, supports age), **chezmoi**, and **SOPS-native secrets in Kubernetes** use age to encrypt config files where each developer's SSH key or YubiKey is a recipient. Rotating a developer means re-encrypting with the updated recipient list.

### Replacement for `gpg -c`

For "encrypt this file with a passphrase" workflows, `age -p` is a drop-in replacement for `gpg -c`. The output is shorter, the cipher choice is fixed (no MD5 surprises), and the passphrase-mode KDF is scrypt rather than the variable choices in OpenPGP.

### CI / CD secret injection

Encrypt secrets with public keys held by build agents (TPM-bound, YubiKey-bound). The plaintext only exists transiently inside the agent's process. Combined with `age-plugin-tpm`, secrets are bound to a specific machine attested at boot.

## age vs OpenPGP / GnuPG

| Aspect | age | OpenPGP (GnuPG) |
|--------|-----|-----------------|
| Algorithm choice | fixed | many, negotiated |
| Format complexity | tiny | substantial |
| Signatures | no | yes |
| Identity / key management | external | built-in (keyrings) |
| Web of trust | no | yes (see [Overview - Web of Trust](/kb/web-of-trust/)) |
| Streaming | yes (chunks) | yes (CFB legacy + EAX) |
| Hardware support | via plugins | via gpg-agent / smartcard |
| Standardization | community spec | RFC 9580 (OpenPGP) |
| Long-term archive | not designed for it | yes (CMS analog, S/MIME-adjacent) |
| Footgun surface | small | large |

When age is right: encrypt-at-rest, deploy-time secrets, backups, tooling that needs simple semantics.

When OpenPGP is right: signing identity assertions, email encryption, archives that need to survive software churn for decades, ecosystems where signature semantics matter.

When **neither** is right: messaging — use Signal Protocol or MLS. age has no forward secrecy and no replay protection; signatures aren't part of the model so authenticity rests entirely on recipient-key possession.

## Honest scope

age is not a long-term archive standard like CMS. Specifically:

- The format spec is community-maintained, not IETF-tracked.
- No formal interoperability profile beyond the reference + rage.
- No standardized signature mode (a separate spec proposal exists but is not part of v1).
- Algorithm agility is by design absent — when ChaCha20 or X25519 needs replacement, age v2 will be a new format, not an in-place upgrade.

For a 30-year-archive use case, CMS / S/MIME or OpenPGP remain the more conservative choices despite their warts.

## Pitfalls

- **No filename or metadata encryption.** Wrap in tar/zip if filenames are sensitive.
- **No replay protection.** A stale ciphertext is just as decryptable as a fresh one.
- **Recipient list is visible** in the header (count and ephemeral X25519 publics, though not the recipient identities themselves directly). Anonymity-set considerations apply.
- **Passphrase mode is not for casual users.** scrypt parameters are reasonable but not memory-hard at the level of Argon2id; for high-stakes passphrase protection, derive a key with Argon2id externally and feed it as an X25519 key.
- **No signing.** If you need to assert *who* encrypted a file, sign with a separate primitive (minisign, signify, ssh-keygen -Y).

## Primary sources

- Valsorda, Cartwright-Cox, *age v1 specification*, age-encryption.org/v1.
- Bernstein, Hamburg, Krasnova, Lange, *Curve25519* and X25519 (RFC 7748, Jan 2016).
- Nir, Langley, *ChaCha20 and Poly1305 for IETF Protocols*, RFC 8439 (Jun 2018).
- Krawczyk, Eronen, *HMAC-based Extract-and-Expand Key Derivation Function (HKDF)*, RFC 5869 (May 2010).
- Reference implementation: [github.com/FiloSottile/age](https://github.com/FiloSottile/age).
- rage: [github.com/str4d/rage](https://github.com/str4d/rage).
- age-plugin-yubikey: [github.com/str4d/age-plugin-yubikey](https://github.com/str4d/age-plugin-yubikey).
- age-plugin-tpm: [github.com/Foxboron/age-plugin-tpm](https://github.com/Foxboron/age-plugin-tpm).
- age-plugin-fido2-hmac: [github.com/olastor/age-plugin-fido2-hmac](https://github.com/olastor/age-plugin-fido2-hmac).
- age-plugin-se: [github.com/remko/age-plugin-se](https://github.com/remko/age-plugin-se).
- agenix (Nix): [github.com/ryantm/agenix](https://github.com/ryantm/agenix).
