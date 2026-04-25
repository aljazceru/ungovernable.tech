---
title: "Composing Primitives"
tags:
  - "meta"
  - "moc"
  - "patterns"
  - "overview"
---
*A Map of Content for building real systems by stacking the cryptographic and network primitives in the vault. No single primitive solves everything; composition is where security comes from.*

---

## The composition lattice

Each primitive plugs a specific gap. Knowing what each one does (and does not do) is what lets you compose them safely.

| Primitive | Hides | Doesn't hide | Pairs well with |
|-----------|-------|--------------|-----------------|
| TLS | Wire content | Endpoints, sizes, timing | Mixnet, attestation |
| TEE | RAM from OS or cloud | Side channels, vendor backdoor | Attestation, transparency log |
| FHE | Plaintext during compute | Existence and size of inputs | ZK proof of correctness |
| ZK proof | Witness | Proof statement and result | FHE, on-chain verification |
| PIR | Index `i` | Database contents | Relays, mixnet for transport |
| Mixnet | Network metadata | Volume over long windows | Sealed sender, padding |
| Onion routing | Per-hop knowledge | Timing correlation | Padding, mixnet |
| Signal Protocol | Per-message keys | Recipient identity (without sealed sender) | Mixnet, MLS for groups |
| Decentralized name | Identity from registrar | Identity from blockchain analysis | Onion routing, PKARR |
| Self-custody key | From custodian | From your own device compromise | Hardware wallet, multisig |

---

## Common compositions

### Confidential AI inference

```
Decentralized name (.eth / PKARR / .onion)
   ↓
Attested TLS bound to enclave-generated key
   ↓
TDX or SEV-SNP confidential VM
   ↓
H100/H200 confidential GPU mode (encrypted PCIe)
   ↓
Open-weights LLM + reproducible build hash
   ↓
Transparency-logged release (à la Apple PCC)
```

Files: [Confidential-AI-Inference](/confidential-computing/confidential-ai-inference), [Private-LLM-Inference-Patterns](/confidential-computing/private-llm-inference-patterns), [NVIDIA-GPU-TEE](/confidential-computing/nvidia-gpu-tee), [Attestation-Architecture](/confidential-computing/attestation-architecture).

### Private query over public data

```
Client query
   ↓
PIR (single- or multi-server)
   ↓
Optional: ZK proof of correct database state
   ↓
Transport: Tor or Nym
```

Files: [Overview - Private Information Retrieval](/cryptography/overview-private-information-retrieval), [Overview - Mix Networks](/mix-networks).

### Censorship-resistant payment

```
Bitcoin keypair (self-custodied)
   ↓
Lightning channel
   ↓
Onion-routed HTLC payment
   ↓
Receiver: BOLT12 or LNURL with attested proof
```

Files: [Overview - Financial Sovereignty](/financial-sovereignty), [Lightning Network Deep Dive](/financial-sovereignty/lightning-network-deep-dive).

### Sovereign social account

```
Nostr keypair (signing key)
   ↓
NIP-17 gift-wrapped DMs (metadata protection)
   ↓
NIP-05 over PKARR (no DNS dependency)
   ↓
Multiple relays (transport redundancy)
   ↓
Lightning zaps for monetization
```

Files: [Overview - Encrypted Messaging](/encrypted-messaging), [Nostr Deep Dive](/encrypted-messaging/nostr-deep-dive), [Overview - Decentralized DNS](/decentralized-dns).

### Verifiable confidential computation

```
Client sends encrypted input
   ↓
Server runs computation under FHE
   ↓
Server attaches a SNARK proving the function was the agreed one
   ↓
Client verifies SNARK in milliseconds, then decrypts result
```

This is the vFHE (verifiable FHE) pattern. Either of these alternatives also works:

- FHE evaluator inside an attested TEE. The TEE attestation replaces the SNARK.
- Threshold FHE with active-secure honest-majority MPC. The protocol detects misbehavior.

Files: [Overview - Fully Homomorphic Encryption](/cryptography/overview-fully-homomorphic-encryption), [Overview - Zero-Knowledge Proofs](/zero-knowledge), [Overview - Confidential Computing](/confidential-computing).

### Post-quantum migration of everything

```
For each long-term-secret protocol (TLS, SSH, Signal, age-encrypted backups):
   1. Switch to a hybrid KEM (X25519 + ML-KEM-768/1024)
   2. Rotate signing keys to ML-DSA or hybrid Ed25519+ML-DSA
   3. Audit the symmetric key sizes — AES-256 stays
   4. Plan re-encryption for archived ciphertexts under new keys
```

Files: [Overview - Post-Quantum Cryptography](/post-quantum), [Glossary](/meta/glossary) (Hybrid KEM, Harvest now decrypt later).

---

## Anti-patterns

These look decentralized or private only on the surface:

- Custodial "non-custodial": exchange holds your keys but calls itself non-custodial.
- CDN'd onion service: operator's identity revealed via Cloudflare logs.
- Signal Desktop on a compromised OS: E2EE does not help if the endpoint is malware.
- Nostr without NIP-17: DMs leak the social graph to relays.
- TEE without attestation enforcement: the server runs in a TEE, but the client never checks.
- FHE without verifiability: the server can return garbage and the client cannot tell.
- Self-custody without a backup plan: losing the key is the same as a custodian losing your funds.

---

## Files most relevant

Every Overview in the vault. Start with **Research Methodology**'s evaluation criteria, then pick the relevant overviews and build a stack.

