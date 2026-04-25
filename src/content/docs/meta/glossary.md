---
title: "Glossary"
tags:
  - "meta"
  - "glossary"
  - "terminology"
---
Authoritative definitions for terms used across the vault. New terms must be added here on first use; deprecated terms get a `(deprecated)` marker rather than deletion.

---

## A

**Attestation** — Cryptographic proof of the identity, configuration, and code hash of a piece of software running inside a TEE. Anchors trust in the hardware vendor's signing keys (Intel DCAP, AMD KDS, NVIDIA NRAS). See [Attestation-Architecture](/confidential-computing/attestation-architecture).

**Attested TLS** — TLS connection where the server's keypair is generated *inside* an enclave and the attestation report is bound to the TLS certificate (or pinned in a Channel Binding). Lets a client verify it's talking to specific code on specific hardware, not just any holder of the cert.

**AEAD** — Authenticated Encryption with Associated Data. Modern symmetric mode (AES-GCM, ChaCha20-Poly1305) that combines confidentiality and integrity in one primitive.

**Alice / Bob / Eve / Mallory** — Standard cryptographic placeholder names. Alice and Bob are honest parties; Eve is a passive eavesdropper; Mallory is an active attacker.

---

## B

**BBS+** — Pairing-based signature scheme that supports selective disclosure of attributes and zero-knowledge proofs of possession. Foundation of W3C Verifiable Credentials with privacy.

**Bulletproofs** — Short, non-interactive zero-knowledge range proofs that need no trusted setup. Used in Monero (transaction amounts) and various confidential-transaction protocols.

**Blinding / Blind signature** — Cryptographic technique where a signer signs a message it cannot read. Used by Chaumian eCash, Cashu, and parts of mixnet payment schemes.

---

## C

**CCIP-Read (EIP-3668)** — Pattern that lets ENS resolvers serve names from off-chain backends with cryptographic proofs.

**Chaumian eCash** — Bearer token system using blind signatures (Chaum, 1983). Modern implementations: Cashu (Bitcoin/Lightning), GNU Taler.

**CoCo (Confidential Containers)** — CNCF project bringing confidential computing to Kubernetes via Kata + TEE-backed VMs and a Trustee KBS. See [Confidential-Containers](/confidential-computing/confidential-containers).

**Confidential Computing** — Hardware-backed protection of data *during computation*, complementing at-rest and in-transit encryption.

**Cover traffic** — Dummy packets sent on a schedule to hide whether real traffic is flowing. Core to mixnet metadata defense.

**CRR (Continual Re-Randomization)** — Property of mix networks where each hop re-encrypts (or re-blinds) the packet so the bit pattern changes between links.

---

## D

**DCAP (Data Center Attestation Primitives)** — Intel's open attestation infrastructure for SGX/TDX, replacing the EPID-based Attestation Service for production use.

**DHT (Distributed Hash Table)** — Key-value store spread across many nodes (Kademlia, Mainline). Used for peer discovery, BitTorrent trackers, PKARR record storage.

**DID (Decentralized Identifier)** — W3C URI scheme `did:method:id` resolving to a DID Document with public keys and service endpoints. Methods: `did:key`, `did:web`, `did:ion`, `did:plc`, `did:peer`, `did:ens`.

**Double Ratchet** — Per-message key rotation algorithm in Signal/MLS that combines a Diffie-Hellman ratchet with a symmetric KDF chain to deliver forward secrecy and post-compromise security.

**DTN (Delay-Tolerant Network)** — Networking architecture (RFC 4838) for intermittent or high-latency links. Uses store-carry-forward bundles. Used in mesh, satellite, and disconnected operation.

---

## E

**Ed25519** — EdDSA signature scheme over Curve25519. Compact, fast, deterministic; the de-facto modern signature primitive in Tor v3, Nostr, Signal, Pubky, etc.

**EIP-7702 / EIP-4337** — Ethereum account-abstraction proposals enabling smart-contract behavior on EOAs and bundled UserOps respectively.

**Enclave** — Hardware-isolated region of memory and execution; the umbrella term for SGX enclaves, SEV-SNP VMs, TDX TDs, etc.

---

## F

**fhEVM** — Ethereum-compatible EVM that operates on FHE ciphertexts. Zama's flagship.

**FHE (Fully Homomorphic Encryption)** — Encryption that supports arbitrary computation on ciphertexts. See [Overview - Fully Homomorphic Encryption](/cryptography/overview-fully-homomorphic-encryption).

**Forward Secrecy** — Property where compromising long-term keys does not compromise past session keys. Achieved via ephemeral DH (TLS 1.3, Signal X3DH/PQXDH).

**FROST** — Flexible Round-Optimized Schnorr Threshold signatures. Used for threshold Bitcoin/Nostr key custody.

---

## G

**Garlic Routing** — I2P's variant of onion routing where one packet ("garlic clove bundle") may contain multiple inner messages with different destinations.

**GNS (GNU Name System)** — Privacy-preserving petname-based hierarchical naming, RFC 9498.

**Groth16** — Pairing-based zk-SNARK with 200-byte proofs and per-circuit trusted setup. Used by Zcash Sapling, Tornado Cash.

**Grover's algorithm** — Quantum search algorithm giving a √N speedup over classical brute force. Effectively halves symmetric key strength — AES-256 retains a 128-bit security margin against it.

---

## H

**Halo2** — PLONK-family proof system from Electric Coin Co.; recursive composition without a fresh trusted setup per circuit. Used in Zcash Orchard.

**Handshake (HNS)** — Blockchain-based replacement for the DNS root zone, with permissionless TLD ownership.

**Harvest now, decrypt later** — Adversary records encrypted traffic today expecting to decrypt it once a quantum computer exists. The motivation for migrating long-secrecy traffic to post-quantum KEMs *now*.

**Hybrid KEM** — Composition of a classical KEM (e.g. X25519) and a post-quantum KEM (e.g. ML-KEM-768) where the shared secret is the KDF of both halves. Currently deployed in TLS 1.3, SSH, Signal PQXDH, iMessage PQ3.

---

## I

**I2P (Invisible Internet Project)** — Anonymous overlay network using garlic routing and unidirectional tunnels.

**IETF** — Internet Engineering Task Force; the body that publishes RFCs.

**Ion / did:ion** — DIF DID method anchored on Bitcoin via Sidetree (a Layer-2 ledger).

---

## K

**Kademlia** — DHT algorithm using XOR distance for routing. The basis of Mainline DHT, IPFS, libp2p Kad-DHT.

**KBS (Key Broker Service)** — Component in CoCo Trustee that releases secrets to enclaves only on a valid attestation.

**KEM (Key Encapsulation Mechanism)** — Primitive that produces an encapsulated symmetric key for a recipient public key. Replaces Diffie-Hellman in post-quantum protocols.

**KDS (Key Distribution Service)** — AMD's attestation backend: serves VCEK / VLEK certificates that endorse SEV-SNP attestation reports.

**Key Escrow** — Third-party holding of decryption keys. Contradicts sovereignty; historically pushed by states (Clipper chip).

---

## L

**Lattice cryptography** — Hardness assumptions based on lattice problems (LWE, Ring-LWE, Module-LWE, NTRU). Foundation of FHE and most NIST PQC standards.

**Lightning Network** — Layer 2 Bitcoin protocol of bidirectional payment channels with hash-time-locked routed payments. See [Lightning Network Deep Dive](/financial-sovereignty/lightning-network-deep-dive).

**Loopix** — Continuous-time mix network design (Piotrowska et al., 2017) — Poisson-mixing with cover traffic. Foundation of Nym and Katzenpost.

**LoRa** — Low-power long-range radio modulation (sub-GHz ISM bands) used by Meshtastic and other off-grid networks.

**LWE (Learning With Errors)** — Lattice problem on which most modern lattice crypto rests.

---

## M

**Mainline DHT** — The BitTorrent DHT, ~10 million nodes worldwide. Used by PKARR/Pubky for record publication.

**mDL (Mobile Driver's License, ISO 18013-5)** — Standard for mobile credentials with selective disclosure. Deployed in several US states and EU Digital Wallet.

**MEV (Maximal Extractable Value)** — Value extracted from transaction ordering by validators/builders. *Originally "Miner Extractable Value"; renamed when Ethereum left PoW.*

**Mixnet** — Network that batches, reorders, and re-encrypts traffic across multiple hops to hide who-talks-to-whom from a global observer. See [Overview - Mix Networks](/mix-networks).

**ML-DSA (FIPS 204)** — Module-LWE signature scheme based on Dilithium. Replaces ECDSA / RSA-PSS for post-quantum signatures.

**ML-KEM (FIPS 203)** — Module-LWE key encapsulation based on Kyber. Replaces ECDH / RSA-KEM for post-quantum key exchange.

**MLS (Messaging Layer Security, RFC 9420)** — IETF standard for group E2EE with continuous group key agreement (TreeKEM). Used in Wire and Cisco Webex; Matrix MLS profile in development.

**MPC (Multi-Party Computation)** — Cryptographic primitive where parties jointly compute a function over their private inputs without revealing them. Honest-majority and dishonest-majority variants exist.

**MRENCLAVE / MRSIGNER** — SGX measurements: hash of the enclave's initial code/data (MRENCLAVE) and the signing identity (MRSIGNER). Used in attestation policies.

---

## N

**Namecoin** — Earliest functional blockchain naming system (2011), merged-mined with Bitcoin. `.bit` TLD.

**NIP-05 / NIP-44 / NIP-17** — Nostr Implementation Possibilities. NIP-05: human-readable identifiers; NIP-44: modern E2EE DM cipher; NIP-17: gift-wrapped DMs with metadata protection.

**Nostr** — *Notes and Other Stuff Transmitted by Relays.* Pubkey-rooted social protocol; events signed by Schnorr/Ed25519 keys, served by relays.

**NRAS (NVIDIA Remote Attestation Service)** — Attestation backend for H100/H200/Blackwell confidential computing.

---

## O

**Onion routing** — Layered encryption such that each relay can peel one layer revealing only the next hop. Tor is the canonical implementation.

**OPRF (Oblivious Pseudo-Random Function)** — Two-party protocol where the client gets `f_k(x)` without learning `k` and the server doesn't learn `x`. Used in PIR, password-authenticated key exchange, and private set intersection.

**ORAM (Oblivious RAM)** — Technique that hides memory access patterns from an observer who can see which addresses are touched.

**Overlay network** — Logical network running on top of an existing underlay (Yggdrasil, cjdns, Tor, I2P).

---

## P

**PCC (Private Cloud Compute)** — Apple's confidential AI inference platform (announced 2024). Combines Secure Enclave, code transparency log, and stateless attested servers.

**Payjoin (BIP-78)** — Two-party CoinJoin variant where the receiver contributes inputs, breaking the common-input-ownership heuristic.

**Petname** — Local nickname for a globally-unique cryptographic identifier (Stiegler's petname system; Zooko's triangle resolution).

**PIR (Private Information Retrieval)** — Protocol that lets a client retrieve record `i` from a database while the server learns nothing about `i`. See [Overview - Private Information Retrieval](/cryptography/overview-private-information-retrieval).

**PKARR** — Public-Key-Addressable Resource Records over Mainline DHT. Names are Ed25519 keys; records are signed and stored under the keyhash.

**PoW / PoS** — Proof of Work / Proof of Stake. Sybil-resistance mechanisms for permissionless consensus.

**PQC (Post-Quantum Cryptography)** — Cryptography secure against polynomial-time quantum adversaries. See [Overview - Post-Quantum Cryptography](/post-quantum).

**PQXDH** — Post-quantum extended X3DH; the hybrid (X25519 + ML-KEM-1024) key agreement used by Signal since 2023.

**Pubky** — PKARR-based identity and naming system from Synonym.

---

## R

**Ratchet** — A keying scheme that derives new keys irreversibly forward, providing forward secrecy. *Symmetric ratchet*: KDF chain. *DH ratchet*: Diffie-Hellman re-key per round-trip.

**RATS (Remote ATtestation procedureS)** — IETF working group and architecture (RFC 9334) for remote attestation. Defines the Attester / Verifier / Relying-Party roles used across CC ecosystems.

**Reticulum** — Markqvist's encrypted-by-default mesh networking stack. Runs over LoRa, packet radio, TCP, serial.

**Ring-LWE** — Variant of LWE on polynomial rings. Smaller keys / faster ops than plain LWE.

---

## S

**SD-JWT (IETF)** — Selective Disclosure JWT — VC format that uses a Merkle-style salted-hash tree so the holder can reveal a subset of claims to the verifier.

**SEV-SNP** — AMD Secure Encrypted Virtualization with Secure Nested Paging. VM-level TEE with integrity protection. See [TEE-Technologies-Deep-Dive](/confidential-computing/tee-technologies-deep-dive).

**SGX (Software Guard Extensions)** — Intel's per-process TEE (2015–). Powerful but punctuated by side-channel breaks; legacy for new workloads.

**Schnorr signature** — Linear, aggregatable signature scheme. Bitcoin Taproot uses Schnorr/BIP340.

**Sphinx packet** — Format for fixed-size, layered-encrypted mixnet packets that hide path length and per-hop processing.

**STARK** — Scalable Transparent Argument of Knowledge. Hash-based, no trusted setup, post-quantum candidate; large proofs but fast verifier.

**Steganography** — Hiding data within other data (messages in images, traffic shaped to look like benign traffic).

---

## T

**Taproot (BIP-340/341/342)** — Bitcoin upgrade (2021) introducing Schnorr signatures and MAST script trees; basis for sub-second-cost cooperative-spend privacy.

**TCB (Trusted Computing Base)** — The set of hardware/firmware/software a security claim relies on. Smaller TCB = smaller attack surface. TCB versions appear in attestation reports.

**TDX (Trust Domain Extensions)** — Intel's VM-level TEE (2022–).

**TEE (Trusted Execution Environment)** — Hardware mechanism for isolated execution. Umbrella term covering SGX, TDX, SEV-SNP, Arm CCA, IBM SE.

**Threshold signature** — Signature where any `t` of `n` parties can sign; fewer than `t` cannot. FROST (Schnorr), GG20 (ECDSA), Pedersen DKG.

**TOR / Tor (The Onion Router)** — Low-latency onion-routing anonymity network. Three-hop default circuits; v3 hidden services.

**Trustee** — CoCo's KBS implementation; gates secret release on attestation policy.

---

## V

**VC (Verifiable Credential, W3C)** — Signed JSON-LD or JWT structure asserting claims about a subject. Issuer → Holder → Verifier model.

**VCEK / VLEK** — AMD chip-bound (VCEK) and platform-bound (VLEK) endorsement keys signed by KDS, used to verify SEV-SNP attestation reports.

**vFHE (Verifiable FHE)** — FHE composed with a SNARK over the homomorphic circuit so the decryptor can verify the server computed the function honestly.

---

## W

**WireGuard** — Modern VPN protocol; minimal cryptographic core (Curve25519, ChaCha20-Poly1305, BLAKE2s). Influences Yggdrasil, Tailscale, Mullvad.

**WoT (Web of Trust)** — Peer-attestation trust model — OpenPGP and Nostr social-graph variants. See [Overview - Web of Trust](/cryptography/overview-web-of-trust).

---

## X

**X25519** — Diffie-Hellman over Curve25519. Default ECDH primitive in TLS 1.3, Signal, WireGuard.

**X3DH** — Extended Triple Diffie-Hellman key agreement (Signal, 2016). Replaced by PQXDH in production.

---

## Y

**Yggdrasil** — Encrypted IPv6 mesh overlay; routing by cryptographic identity.

---

## Z

**Zama** — Commercial FHE company; ships Concrete (TFHE) and fhEVM.

**ZK Proof (Zero-Knowledge Proof)** — Prove a statement true without revealing why.

**ZK-SNARK** — Zero-Knowledge Succinct Non-interactive ARgument of Knowledge.

**ZK-STARK** — Zero-Knowledge Scalable Transparent ARgument of Knowledge.

**Zooko's triangle** — Hypothesis that names cannot be simultaneously human-meaningful, decentralized, and globally unique. Petnames + cryptographic IDs (e.g., Pubky, ENS) are partial resolutions.

