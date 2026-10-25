---
title: "Map: Composing Primitives"
slug: map-composing-primitives
type: map
pillars: ["cryptography", "confidential"]
description: "A map for building real systems by combining primitives: TEEs with attestation, mixnets with ecash, ZK with identity, and where compositions fail."
dek: "A Map of Content for building real systems by stacking the cryptographic and network primitives in this library. No single primitive solves everything; composition is where security comes from."
updated: 2026-10-25
created: 2026-04-25
origin: vault
source: "00 - Meta/MOC - Composing Primitives.md"
tags: ["meta", "moc", "patterns", "overview"]
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
| Content-addressed storage | Byte substitution | Availability or confidentiality | Encryption, pinning, decentralized names |
| Self-custody key | From custodian | From your own device compromise | Hardware wallet, multisig |

## Common compositions

### Confidential AI inference

```
Decentralized name (.eth / PKARR / .onion)
   ↓
Attested TLS bound to enclave-generated key
   ↓
TDX or SEV-SNP confidential VM
   ↓
Confidential GPU mode with protected CPU–GPU transfers
   ↓
Open-weights LLM + reproducible build hash
   ↓
Transparency-logged release (à la Apple PCC)
```

Files: [Confidential-AI-Inference](/kb/confidential-ai-inference/), [Private-LLM-Inference-Patterns](/kb/private-llm-inference-patterns/), [NVIDIA-GPU-TEE](/kb/nvidia-gpu-tee/), [Attestation-Architecture](/kb/remote-attestation/).

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

Files: [Overview - Private Information Retrieval](/kb/private-information-retrieval/), [Overview - Mix Networks](/kb/mix-networks/).

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

Files: [Overview - Financial Sovereignty](/kb/financial-sovereignty/), [Lightning Network Deep Dive](/kb/lightning-network/).

### Sovereign social account

```
Nostr keypair (signing key)
   ↓
NIP-17 gift-wrapped DMs (sender hidden; recipient tag visible)
   ↓
Blossom for media blobs (SHA-256-addressed, mirrored)
   ↓
Public-key identity; optional NIP-05 alias via DNS and HTTPS
   ↓
Multiple relays (transport redundancy)
   ↓
Lightning zaps for monetization
```

Files: [Overview - Encrypted Messaging](/kb/encrypted-messaging/), [Nostr Deep Dive](/kb/nostr-protocol/), [Blossom](/kb/blossom/), [Overview - Decentralized DNS](/kb/decentralized-dns/).

### Sovereign off-grid node (Blackbox-style)

```
Local LLM inference (Ollama or equivalent, no cloud API)
   ↓
LoRa mesh (Meshtastic / MeshCore / Blackout Comms)
   ↓
Offline maps (TAK / equivalent, no Google)
   ↓
Cashu ecash + Bitcoin (blind tokens + self-custody, no bank)
   ↓
E2E encrypted request/response chunked over mesh (~200B packets)
```

One laptop + $30 radio. Zero internet, zero banks, zero datacenters. See [MeshCore](/kb/meshcore/), [Cashu and Chaumian Ecash](/kb/cashu-ecash/), off-grid files, and [MOC - Censorship Resistance](/kb/map-censorship-resistance/). Composes local confidential compute with air-gapped comms and private money.

### Durable public artifact

```
Release artifact or static site
   ↓
Hash and sign locally
   ↓
IPFS for content-addressed distribution
   ↓
Arweave for archival copy
   ↓
ENS / PKARR / signed index points to both
```

Files: [Overview - Decentralized Storage](/kb/decentralized-storage/), [IPFS and Filecoin](/kb/ipfs-and-filecoin/), [Arweave](/kb/arweave/), [Overview - Decentralized DNS](/kb/decentralized-dns/).

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

Files: [Overview - Fully Homomorphic Encryption](/kb/fully-homomorphic-encryption/), [Overview - Zero-Knowledge Proofs](/kb/zero-knowledge-proofs/), [Overview - Confidential Computing](/kb/confidential-computing/).

### Hardware-protected ecash mint (deployment pattern)

```
Bitcoin/Lightning reserves (self-custodied or on-chain visible)
   ↓
Cashu mint logic running inside attested TEE (keys generated in enclave, never exposed to host)
   ↓
Remote attestation + transparency log (client verifies correct code + measurement)
   ↓
Blind signatures issued; users hold bearer tokens offline / over Nostr / mesh
   ↓
Redemption still depends on the mint; evaluate code, reserves, rollback and hardware trust
```

Direct 01 + 06 composition. See [Cashu and Chaumian Ecash](/kb/cashu-ecash/) and confidential computing attestation files. Moves from "trust the mint runner" to "trust the hardware root + audited enclave code."

### Post-quantum migration of everything

```
For each long-term-secret protocol (TLS, SSH, Signal, age-encrypted backups):
   1. Switch to a hybrid KEM (X25519 + ML-KEM-768/1024)
   2. Rotate signing keys to ML-DSA or hybrid Ed25519+ML-DSA
   3. Audit the symmetric key sizes — AES-256 stays
   4. Plan re-encryption for archived ciphertexts under new keys
```

Files: [Overview - Post-Quantum Cryptography](/kb/post-quantum-cryptography/), [Glossary](/glossary/) (Hybrid KEM, Harvest now decrypt later).

## Anti-patterns

These look decentralized or private only on the surface:

- Custodial "non-custodial": exchange holds your keys but calls itself non-custodial.
- CDN'd onion service: operator's identity revealed via Cloudflare logs.
- Signal Desktop on a compromised OS: E2EE does not help if the endpoint is malware.
- Nostr without NIP-17: DMs leak the social graph to relays.
- TEE without attestation enforcement: the server runs in a TEE, but the client never checks.
- FHE without verifiability: the server can return garbage and the client cannot tell.
- Self-custody without a backup plan: losing the key is the same as a custodian losing your funds.

## Files most relevant

Every Overview in this library. Start with [Research Methodology](/method/)'s evaluation criteria, then pick the relevant overviews and build a stack.

## Primary sources

- [RFC 9334: attestation architecture](https://www.rfc-editor.org/rfc/rfc9334.html)
- [RA-TLS: binding attestation to TLS](https://arxiv.org/abs/1801.05863)
- [Nostr NIP-05: DNS-based identifiers](https://github.com/nostr-protocol/nips/blob/master/05.md)
- [Nostr NIP-59: gift-wrap metadata](https://github.com/nostr-protocol/nips/blob/master/59.md)
- [Cashu NUT-00: protocol and mint trust](https://github.com/cashubtc/nuts/blob/main/00.md)
- [Lightning BOLT 4: onion routing](https://github.com/lightning/bolts/blob/master/04-onion-routing.md)
- [NVIDIA: Confidential Computing on H100 GPUs](https://developer.nvidia.com/blog/confidential-computing-on-h100-gpus-for-secure-and-trustworthy-ai/)
