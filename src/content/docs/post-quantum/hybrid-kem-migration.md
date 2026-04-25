---
title: "Hybrid KEM Migration"
tags:
  - "pq"
  - "migration"
  - "hybrid-kem"
  - "deep-dive"
---
*Operational guide to migrating real systems to post-quantum cryptography. Most engineers don't need to understand Module-LWE. They need to know which version of OpenSSL to install, when to enable PQ in their TLS profile, and what data to re-encrypt. This file is that.*

---

## The threat, restated plainly

A cryptographically relevant quantum computer (CRQC) doesn't exist today and probably won't for a decade. But:

1. Adversaries record encrypted traffic now. ISPs, intelligence agencies, and well-resourced actors store encrypted bulk traffic indefinitely.
2. Once a CRQC exists, all that recorded traffic decrypts retroactively if its key exchange used pre-quantum primitives (RSA, DH, ECDH).
3. Symmetric crypto (AES, ChaCha20) is largely fine. Doubling key length defeats Grover's algorithm. The problem is asymmetric, in KEMs and signatures.

Migration timing depends on **secrecy horizon**: how long does the data need to stay confidential? If the answer is "5 years," you can wait. If the answer is "30 years," you need to be migrating now.

---

## Triage by secrecy horizon

| Data class | Horizon | Action |
|------------|---------|--------|
| Real-time chat (most users) | Seconds-to-days | Migrate when convenient (already done in Signal) |
| Bank transactions | Years | Migrate within current decade |
| Healthcare records | Decades | **Migrate now** |
| State secrets | Lifetime | **Migrated already in classified contexts** |
| Source-protection materials (journalism) | Decades | **Migrate now** |
| Bitcoin private keys (revealed at spend) | One-time exposure | Don't reveal pubkeys; consider PQ post-fork migration |
| Long-term encrypted backups | Decades | **Re-encrypt with PQ-aware tooling** |
| Embedded firmware (IoT, satellites) | Lifetime of device | **Migrate now** for long-lived hardware |

The harvest-now-decrypt-later threat is real for the bottom half of this list. For the top half, migrate when your stack supports it; no urgency.

---

## TLS 1.3 migration

### Today (early 2026)

Most modern stacks support **X25519MLKEM768** as a hybrid KEM:

- **BoringSSL** (Chrome, Edge): default since 2024.
- **rustls ≥ 0.23**: opt-in flag.
- **OpenSSL ≥ 3.5**: configurable.
- **Go 1.23+**: default-on.
- **Apple** (Safari): rolling out 2025-2026.
- **Cloudflare**: enabled at edge.
- **Google services**: enabled.

Server configuration:

```
# nginx with OpenSSL 3.5+
ssl_protocols TLSv1.3;
ssl_curves X25519MLKEM768:X25519:secp256r1;
```

Verify with `openssl s_client -connect host:443 -groups X25519MLKEM768`.

### Caveats

- Older clients fall back to X25519. That's fine, the negotiation is by design backward-compatible.
- Middleboxes (some legacy SSL inspection) drop hybrid handshakes. Test rollouts with `--alt-svc` toggles.
- Performance: about 2 KB extra per handshake. For most applications, negligible.

### What about pure-PQ?

Don't deploy pure ML-KEM yet. Hybrid is the production pattern in 2026 and will remain so for years. Pure PQ deployment requires more confidence in the lattice security level than the community currently has.

---

## SSH migration

OpenSSH ≥ 9.0 ships **sntrup761x25519-sha512** by default, a hybrid combining NTRU-Prime (a different PQ scheme) with X25519. ML-KEM hybrids are landing in OpenSSH 10.x.

Server `sshd_config`:

```
KexAlgorithms sntrup761x25519-sha512@openssh.com,curve25519-sha256
```

Client config (`~/.ssh/config`):

```
KexAlgorithms sntrup761x25519-sha512@openssh.com,curve25519-sha256
```

Modern OpenSSH on both sides means already migrated. No further action for most users.

---

## Encrypted messengers

| App | Status |
|-----|--------|
| **Signal** | PQXDH (hybrid X3DH + ML-KEM-1024) since Sep 2023 — production |
| **iMessage** | PQ3 hybrid since Feb 2024 — production |
| **WhatsApp** | Adopting PQ — staged rollout |
| **Telegram** | Pre-quantum; no public PQ roadmap |
| **Matrix** | MLS profile in development includes PQ groundwork |
| **Briar** | Research; experimental hybrid handshakes |
| **SimpleX** | PQ via NTRU experiments |

For users: most messengers don't need active migration; providers handle it transparently. Audit which messengers you trust for long-secrecy traffic.

---

## VPN / mesh migration

| System | PQ status |
|--------|-----------|
| **WireGuard** | Pre-quantum (Curve25519). Hybrid extensions experimental. |
| **OpenVPN** | OpenSSL-stack-dependent; can use OpenSSL 3.5+ PQ. |
| **Tor** | Roadmap; v3 onion will eventually migrate Ed25519/curve25519 to PQ. |
| **Yggdrasil** | Pre-quantum. PQ migration not yet specified. |
| **Reticulum / FIPS** | Pre-quantum. PQ research in roadmap. |

For high-stakes mesh / overlay deployments, layer with TLS-over-TCP using PQ TLS rather than relying on the underlay's pre-quantum keys.

---

## Code signing

Long-lived signed artifacts (firmware, OS distributions, vendor tools) need migration first. The signature on a kernel binary signed today must verify in 30 years; the verifier will exist in a quantum world.

Migration paths:

- Hybrid signatures: classical Ed25519 + ML-DSA-65 (or SLH-DSA for conservative). Verify both.
- Sigstore: PQ extension in discussion.
- OS package managers: per-distro roadmaps. Debian, Fedora exploring; Arch leaning on upstream.

For long-lived embedded systems (cars, satellites, industrial control): re-sign existing firmware with hybrid signatures during scheduled updates.

---

## Encrypted backups and archives

`age`, `gpg`, `7zip --encrypt`, and similar use pre-quantum KEMs by default. For long-secrecy archives:

- **age**: `age-plugin-pq` provides ML-KEM hybrid wrapping. Plugin-stage but functional.
- **GPG**: OpenPGP PQ draft RFC; mainline OpenPGP support pending. Not yet production.
- **Roll-your-own with libsodium-PQ**: practical for new systems, not for migration.

The pragmatic 2026 advice: re-encrypt critical archives using `age` with the PQ plugin once it stabilizes. For now, increase the symmetric key length to 256-bit and store the symmetric key with PQ-wrapped keys when possible.

---

## Bitcoin and crypto-currencies

Bitcoin's signatures (ECDSA legacy and Schnorr Taproot) are pre-quantum. The migration:

- Pubkey reuse increases exposure. Once an address has spent, its pubkey is on-chain and a future quantum computer can derive the private key.
- Send-only-once practice: derive a new address per receive; spend once; new address.
- Cold storage (P2PK addresses) are the highest risk. Many old satoshis sit at P2PK addresses with revealed public keys.
- BIP-360 and similar drafts propose adding PQ-friendly signature support; none deployed as of 2026.

The actionable 2026 guidance: avoid address reuse; don't be one of the public-key-revealed-at-rest holders.

---

## Database / at-rest encryption

Most database / disk encryption uses symmetric primitives (AES-256-GCM, XTS), which are fine post-quantum. The vulnerable layer is **key wrapping** and **key escrow**, the asymmetric layer that wraps the symmetric key.

Audit:

- AWS KMS, Azure Key Vault, GCP KMS: classical RSA / EC key wrap. Some PQ pilot offerings.
- HSMs: confirm ML-KEM support in firmware.
- Custom key-wrap protocols: migrate to hybrid wraps.

For most cloud users, the cloud KMS team handles this; ensure your key-wrap algorithm choice points to PQ-supporting variants when available.

---

## Crypto-agility

The right architecture isn't "deploy ML-KEM today and forget it." It's crypto-agility: the ability to swap primitives quickly when one breaks. Practical:

- Negotiate algorithms at protocol layer; don't hardcode.
- Version your protocols so policy can be tightened without breaking deployment.
- Monitor the field. New attacks on Module-LWE could change parameter recommendations.
- Hybrid by default. Single-primitive deployment is the anti-pattern.

---

## Trade-offs

### Strengths

- Hybrid migration is mature and battle-tested.
- Wide library support in 2026.
- Operationally manageable. Most stacks need configuration, not custom code.

### Limitations

- Bandwidth cost. Hybrid handshakes are 2-5 KB larger.
- Library bugs still being shaken out in newer PQ implementations.
- Long-tail systems (legacy embedded, IoT, blockchains) have unclear paths.
- Coordination across PKI hierarchies (X.509, code signing) is slow.

---

## Quick reference: 2026 migration checklist

```
[ ] TLS 1.3 servers updated to OpenSSL 3.5+ / boringssl with X25519MLKEM768 enabled
[ ] SSH client + server on OpenSSH ≥ 9.0
[ ] Encrypted messengers in use confirmed PQ-capable (Signal: yes; iMessage: yes; ...)
[ ] Long-lived code-signing keys planned for hybrid migration
[ ] Long-lived encrypted archives re-encryption planned
[ ] HSM firmware audited for ML-KEM/ML-DSA support
[ ] Crypto-agility — algorithms negotiable in custom protocols
[ ] Bitcoin / crypto: avoid address reuse; track BIP migrations
```

---

## Related files

- [Overview - Post-Quantum Cryptography](/post-quantum)
- [ML-KEM](/post-quantum/ml-kem)
- [ML-DSA](/post-quantum/ml-dsa)
- [Glossary](/meta/glossary) — Hybrid KEM, harvest-now-decrypt-later, Module-LWE

---

## Primary sources

- IETF, *Hybrid key exchange in TLS 1.3*, draft-ietf-tls-hybrid-design.
- Cloudflare PQC blogs — [blog.cloudflare.com](https://blog.cloudflare.com).
- Apple, *iMessage with PQ3*, security blog Feb 2024.
- Signal, *PQXDH*, Sep 2023.
- NIST PQC project — [csrc.nist.gov/projects/post-quantum-cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography).
- liboqs — [openquantumsafe.org](https://openquantumsafe.org).
- *Migrating to Post-Quantum Cryptography* (NIST IR 8413, 2024).

