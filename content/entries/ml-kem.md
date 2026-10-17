---
title: "ML-KEM (FIPS 203)"
slug: ml-kem
type: deep-dive
pillars: ["pqc"]
readiness: usable
description: "ML-KEM (FIPS 203), NIST's post-quantum key encapsulation standard: how it works, its parameter sets, and its use in hybrid TLS key exchange."
dek: "The NIST-standardized post-quantum KEM (FIPS 203, finalized August 2024). Replaces ECDH and RSA-KEM for key establishment. Already deployed in TLS 1.3, SSH, Signal, and iMessage. The first NIST PQC standard to see real-world adoption at scale."
updated: 2026-05-16
created: 2026-04-25
origin: vault
source: "10-Post-Quantum/ML-KEM.md"
aliases: ["Kyber", "FIPS 203"]
tags: ["ml-kem", "kyber", "kem", "fips-203", "post-quantum", "deep-dive"]
---

## What ML-KEM replaces

| Classical primitive | ML-KEM |
|--------------------|--------|
| RSA-KEM (RSA-2048+) | ML-KEM-512/768/1024 |
| ECDH (X25519, P-256) | ML-KEM-768 (typical) |
| DH (Diffie-Hellman) | ML-KEM-* |

The pattern is to encapsulate a symmetric key (about 32 bytes) for the recipient's public key. Replaces "send Diffie-Hellman ephemeral and derive shared secret" with "send a KEM ciphertext and decapsulate to shared secret."

## Parameter sets

FIPS 203 specifies three:

| Variant | Security level (NIST) | Public key | Ciphertext | Shared secret |
|---------|----------------------|-----------|------------|---------------|
| **ML-KEM-512** | Category 1 (~AES-128) | 800 B | 768 B | 32 B |
| **ML-KEM-768** | Category 3 (~AES-192) | 1184 B | 1088 B | 32 B |
| **ML-KEM-1024** | Category 5 (~AES-256) | 1568 B | 1568 B | 32 B |

Most production deployments pick ML-KEM-768 as the sweet spot: strong security and reasonable bandwidth. ML-KEM-1024 for higher-stakes long-term-secrecy contexts.

## How it works (briefly)

ML-KEM is based on Module-LWE (Learning With Errors over polynomial rings). The hard problem: given many noisy linear equations modulo a prime, recover the secret. With well-chosen parameters this is conjectured hard for both classical and quantum computers (no Shor-style attack known).

```
KeyGen:  generate (s, A); public key = A·s + e (with small noise e)
Encaps:  recipient generates (r, e1, e2)
         u = A^T·r + e1
         v = b^T·r + e2 + ⌈q/2⌉·m   (m is the random message)
         ciphertext = (u, v); shared secret = KDF(m)
Decaps:  recipient computes m' = decode(v - s^T·u)
         shared secret = KDF(m')
```

The math is straightforward; the hard work is in parameter choice (q, n, η, du, dv) so that decryption succeeds with overwhelming probability while maintaining security. NIST's FIPS 203 fixes these choices.

## Hybrid KEM, the production pattern

ML-KEM is rarely deployed alone. The dominant pattern is hybrid KEM, combining classical (X25519) and post-quantum (ML-KEM) shared secrets:

```
classical_shared = X25519(client_priv, server_pub)
pq_shared        = ML-KEM-768(client_pq_priv, server_pq_ciphertext)
final_shared     = HKDF(classical_shared || pq_shared || transcript)
```

Rationale:

- If ML-KEM is broken in the future (cryptanalysis discovers a new weakness), the classical layer protects the session.
- If X25519 is broken by a quantum computer, the PQ layer protects the session.
- The session is secure if either primitive is sound.

This is the harvest-now-decrypt-later defense. Even traffic recorded today and decrypted in the future requires breaking both layers.

## Where ML-KEM is deployed (mid-2026)

|| Protocol | Hybrid scheme | Status ||
|----------|--------------|--------|
| **TLS 1.3** | X25519MLKEM768 | Mainstream — Chrome, Firefox, Cloudflare (>65% traffic), AWS KMS/SecretsManager/ACM (April 2026), Google services |
| **SSH (OpenSSH ≥ 9.0)** | sntrup761x25519-sha512 (NTRU-Prime hybrid; ML-KEM hybrid landing in 10.x) | Default in OpenSSH 9.x |
| **Signal Protocol** | PQXDH (X3DH + ML-KEM-1024) | Production since fall 2023 |
| **iMessage PQ3** | Custom hybrid Apple scheme | Production since Feb 2024; iOS 26 extends ML-KEM to TLS |
| **WireGuard** | Research / experimental | No standardized native profile |
| **age (encrypted files)** | age-plugin-pq experimental | Plugin-stage |
| **OpenPGP** | Draft RFC; minimal adoption | Slow rollout |
| **Bitcoin / Lightning** | Research; no deployment | Future |
| **Kyber Ransomware** | ML-KEM-1024 + X25519 + AES-256 | Active since September 2025; confirmed April 2026 |

The 2024-2026 wave of TLS 1.3 hybrid deployment was substantial. Chrome enabled X25519MLKEM768 by default in early 2024; Cloudflare and AWS rolled out hybrid endpoints; major CDNs followed.

## Performance

ML-KEM-768 in software (modern CPU, optimized implementation):

- KeyGen: ~30-50 μs
- Encaps: ~30-50 μs
- Decaps: ~30-50 μs

Bandwidth overhead per handshake: about 2 KB extra vs pure X25519. For most TLS connections this is a one-time setup cost, dwarfed by the connection's data plane.

Hardware support is emerging: ARMv8 Crypto Extensions, AVX-512, dedicated ASICs (in some HSMs).

## Implementations

| Library | Language | Notes |
|---------|----------|-------|
| **liboqs** (Open Quantum Safe) | C with bindings | Reference for benchmarking and prototyping |
| **PQClean** | C | Clean reference implementations |
| **kyber-rs / pqcrypto-mlkem** | Rust | Production Rust KEM |
| **OpenSSL ≥ 3.5** | C | Native ML-KEM support |
| **BoringSSL** | C | Hybrid KEM in TLS 1.3 (Chrome) |
| **Bouncy Castle** | Java | Mature PQ support |
| **Apple CryptoKit** (PQ3) | Swift | iMessage integration |

Reference implementation lives at [github.com/pq-crystals/kyber](https://github.com/pq-crystals/kyber).

## Trust and security caveats

- The NIST process vetted ML-KEM through 4 rounds (2017-2024). Cryptographic confidence is high.
- Side-channel risk is real and active. KyberSlash (TCHES 2025) demonstrated secret-dependent division timings in several implementations including the reference code. Constant-time implementations, compiler-barrier hardening (PQShield mlkem-native), and post-compilation TVLA testing are essential.
- liboqs ≤ 0.13 had a CVE around lattice-rejection sampling. The v0.14.0 security fix addressed this; always use current releases.
- New lattice cryptanalysis has not broken ML-KEM's security margins, but ongoing research (IACR ePrint 2025/1577) continues to probe pair-wise multiplication side channels.
- Quantum cryptanalysis doesn't have a known polynomial attack on Module-LWE; classical attacks (lattice reduction) define the security level.
- Decryption failures are bounded but non-zero; NIST parameters set this probability negligibly low (~2⁻¹⁶⁰).

## Trade-offs

### Strengths

- NIST-standardized (FIPS 203, August 2024).
- Real-world deployment in mainstream protocols.
- Hybrid pattern combines classical and PQ.
- Reasonable bandwidth: a few KB extra per handshake.
- Software performance acceptable on modern CPUs.

### Limitations

- Larger keys and ciphertexts vs ECDH (~2 KB vs ~32 bytes).
- New attack surface. Module-LWE is well-studied but newer than RSA / ECDH.
- Side-channel pitfalls in implementation.
- Decryption failures non-zero (negligible but nonzero).
- Hybrid handshake transcript complexity adds protocol surface.

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Cryptanalytic break | Hybrid with classical KEM as defense in depth |
| Side-channel timing | Constant-time implementation; audited libraries |
| Decryption-failure exploitation | Bounded failure prob; rejection sampling |
| Implementation bugs | Audited libraries; formal verification |
| Downgrade to non-hybrid | Strict transcript binding; reject classical-only |
| Harvest-now-decrypt-later | Migrate to hybrid for any traffic with long secrecy horizon |

## Deployment recipe

For a service operator in 2026:

1. Update TLS stack to one supporting **X25519MLKEM768** (BoringSSL ≥ 1.1, OpenSSL ≥ 3.5, rustls ≥ 0.23).
2. Enable hybrid KEM in TLS configuration.
3. Audit handshakes. Verify clients negotiate hybrid where supported.
4. Update SSH server to OpenSSH ≥ 9.x with `KexAlgorithms` allowing `sntrup761x25519-sha512` or `mlkem768x25519-sha256` once standardized.
5. For long-term-secret data (encrypted backups, age files), migrate to PQ-aware tooling.
6. Plan re-encryption for archives with multi-decade secrecy horizons.

## Primary sources

- NIST, *FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard*, August 2024.
- Bos et al., *CRYSTALS — Kyber: A CCA-secure module-lattice-based KEM*, IACR 2017/634.
- Avanzi et al., *CRYSTALS-Kyber Algorithm Specifications and Supporting Documentation*, NIST submission (Round 3).
- Apple, *iMessage with PQ3*, security blog Feb 2024.
- Signal, *PQXDH*, Sep 2023. [signal.org/docs/specifications/pqxdh](https://signal.org/docs/specifications/pqxdh).
- liboqs — [openquantumsafe.org](https://openquantumsafe.org).
- OpenSSL PQ — [github.com/openssl/openssl](https://github.com/openssl/openssl).
- Cloudflare PQC research — [blog.cloudflare.com](https://blog.cloudflare.com).
