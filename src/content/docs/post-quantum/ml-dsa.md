---
title: "ML-DSA"
tags:
  - "ml-dsa"
  - "dilithium"
  - "signatures"
  - "fips-204"
  - "post-quantum"
  - "deep-dive"
---
*The NIST-standardized post-quantum signature scheme (FIPS 204, finalized August 2024). Companion to ML-KEM for the signing side of public-key cryptography. Replaces ECDSA, RSA-PSS, and EdDSA where post-quantum security is required.*

---

## What ML-DSA replaces

| Classical | ML-DSA |
|-----------|--------|
| ECDSA over secp256r1 / secp256k1 | ML-DSA-44 / 65 / 87 |
| Ed25519 / Ed448 | ML-DSA-* |
| RSA-PSS | ML-DSA-* |

Wherever a signature attests authenticity (TLS certificates, code signing, document signatures, blockchain transactions), ML-DSA can substitute as the post-quantum equivalent.

---

## Parameter sets

FIPS 204 specifies three:

| Variant | Security level | Public key | Signature |
|---------|---------------|-----------|-----------|
| **ML-DSA-44** | Category 2 (~AES-128) | 1312 B | 2420 B |
| **ML-DSA-65** | Category 3 (~AES-192) | 1952 B | 3293 B |
| **ML-DSA-87** | Category 5 (~AES-256) | 2592 B | 4595 B |

Compared to Ed25519 (32-byte public key, 64-byte signature), ML-DSA is dramatically larger. This is the central operational cost: signatures embedded in protocols (X.509 chains, code-signing manifests, on-chain transactions) become much bigger.

---

## How it works (conceptually)

ML-DSA is built on the **Fiat-Shamir with Aborts** paradigm over **Module-LWE / SIS**:

```
Sign:    sample y; compute w = A·y; c = H(message || w)
         z = y + c·s   (s = secret key)
         if z too large: reject and retry (ensures distribution leaks no info)
         else: return signature (z, c)

Verify:  check z's bounds; recompute w' = A·z - c·t (t = public key)
         check c == H(message || w')
```

The "abort" pattern is what makes the security proof work. Sampled `y`s outside a safe range are rejected and the protocol retries. This means signing has variable latency (a small probability of multiple retries).

---

## Companion standards

| Algorithm | Use |
|-----------|-----|
| **ML-DSA (FIPS 204)** | Module-LWE primary recommendation |
| **SLH-DSA (FIPS 205)** | Hash-based; conservative backup; bigger but rests only on hash assumptions |
| **FN-DSA (FIPS 206)** | Falcon — NTRU-based; smaller signatures than ML-DSA. Draft as of Aug 2025; final expected 2026. |

The right PQ signature depends on use case:

- **General-purpose**: ML-DSA.
- **Conservative / belt-and-suspenders**: SLH-DSA (only hashes; survives any lattice break).
- **Size-constrained**: FN-DSA (Falcon) for smaller signatures, but harder to implement constant-time.

---

## Hybrid signatures

Like ML-KEM, ML-DSA is often deployed alongside a classical scheme:

```
combined_sig = (ed25519_sig, ml-dsa-sig)
verify: BOTH must be valid
```

Use cases:

- Code signing for software with multi-decade lifecycle (firmware, signed binaries).
- TLS certificates where the CA is willing to issue both signatures.
- Document signing in regulated industries.

The cost is doubled signature size; the benefit is robustness to a break of either primitive.

---

## Performance

ML-DSA-65 in software (modern CPU):

- KeyGen: ~50-100 μs
- Sign: ~50-200 μs (with abort retries — probabilistic)
- Verify: ~50-100 μs

Comparable in throughput to RSA-2048 sign/verify, slower than Ed25519. For most protocols (TLS handshake, code signature verification) the latency is acceptable.

---

## Where ML-DSA is used

| System | Status |
|--------|--------|
| **TLS certificate signatures** | Hybrid X.509 certs in pilot (CA/B Forum 2025-2026) |
| **Code signing (Linux distros)** | Roadmap for kernel signing, package managers |
| **Code signing (Apple, Microsoft)** | Internal use; public exposure pending |
| **Sigstore / cosign** | PQ extension under discussion |
| **HSMs** | Most major HSM vendors support ML-DSA (Thales, Utimaco, AWS CloudHSM) |
| **WebAuthn / FIDO2** | PQ FIDO2 in research |
| **Bitcoin / Ethereum** | Research only — would require hard fork; no near-term deployment |

X.509-with-PQ deployment is the slowest layer because issuing CA certificates with massive signatures bloats the entire cert chain.

---

## Bitcoin and crypto-currencies

A significant open question: how do crypto-currencies migrate to PQ signatures?

- Bitcoin uses ECDSA (legacy) and Schnorr (Taproot). Both are quantum-vulnerable.
- A migration would require a hard fork to add PQ signature support, with a coordinated freeze on legacy addresses.
- ML-DSA-87 signatures are about 4.5 KB, far larger than Bitcoin's 64-byte Schnorr. Block size and fee impact are non-trivial.
- BIPs proposing PQ signatures exist (e.g., BIP-360); none deployed as of 2026.

Bitcoin's quantum vulnerability is real but deferred. Actual cryptographically relevant quantum computers don't exist yet, and the transition path is being designed without urgency.

For Lightning users with existing addresses: keep them out of public view (don't reveal pubkeys for receive-only addresses) until the migration path is clear.

---

## Trade-offs

### Strengths

- NIST-standardized (FIPS 204, August 2024).
- Strong cryptographic literature, well-studied through the NIST competition.
- Multiple security levels (44/65/87).
- Hybrid deployment combines with classical signatures.
- Hardware support in HSMs and modern crypto chips.

### Limitations

- Signatures are huge vs Ed25519 (~3 KB vs 64 B). Bandwidth and storage pressure.
- Public keys are large (~2 KB). X.509 chains balloon.
- Variable signing time due to rejection sampling.
- Side-channel surface in lattice arithmetic.
- No clean migration path for legacy systems with size constraints.

---

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Cryptanalytic break | Hybrid with classical signature; SLH-DSA fallback |
| Side-channel during signing | Constant-time implementations; masking; HSM offload |
| Implementation bugs | Audited libraries; formal verification |
| Downgrade attacks | Strict policy on accepted signature schemes |
| Quantum break (the threat ML-DSA addresses) | Module-LWE is conjectured hard for quantum |

---

## Deployment recipe

1. Update TLS / SSH stacks to support hybrid signatures.
2. For long-lived signatures (code signing, document signing): migrate to ML-DSA or SLH-DSA hybrids before any traffic with multi-decade secrecy is in flight.
3. HSM: confirm ML-DSA support in the firmware roadmap.
4. Inventory: list every place a signature is verified; classify by lifetime of the signed object; prioritize migration accordingly.
5. Test: early test deployments help shake out implementation issues before mainstream rollouts.

---

## Related files

- [Overview - Post-Quantum Cryptography](/post-quantum)
- [ML-KEM](/post-quantum/ml-kem)
- [Hybrid KEM Migration](/post-quantum/hybrid-kem-migration)
- [Glossary](/meta/glossary) — ML-DSA, SLH-DSA, FN-DSA, Module-SIS

---

## Primary sources

- NIST, *FIPS 204: Module-Lattice-Based Digital Signature Standard*, August 2024.
- NIST, *FIPS 205: Stateless Hash-Based Digital Signature Standard (SLH-DSA)*, August 2024.
- NIST, *FIPS 206: FN-DSA (Falcon)*, draft August 2025.
- Ducas et al., *CRYSTALS-Dilithium: A Lattice-Based Digital Signature Scheme*, IACR 2017/633.
- Lyubashevsky, *Fiat-Shamir with Aborts: Applications to Lattice and Factoring-Based Signatures*, ASIACRYPT 2009.
- liboqs — [openquantumsafe.org](https://openquantumsafe.org).
- pq-crystals/dilithium — [github.com/pq-crystals/dilithium](https://github.com/pq-crystals/dilithium).

