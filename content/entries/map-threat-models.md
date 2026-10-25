---
title: "Map: Threat Models"
slug: map-threat-models
type: map
pillars: ["endpoint"]
description: "A map of the recurring adversaries, trust assumptions and failure modes across this library, from cloud operators to quantum computers."
dek: "A Map of Content indexing recurring adversaries, trust assumptions, and failure modes across this library."
updated: 2026-10-25
created: 2026-04-25
origin: vault
source: "00 - Meta/MOC - Threat Models.md"
tags: ["meta", "moc", "threat-model", "overview"]
---

> Threat-modeling rule: name the adversary, name the asset, name the assumption you make about each component. If you cannot write it down, you do not have a threat model. You have hope.

## Recurring adversaries

| Adversary | Capability | Where it appears |
|-----------|------------|------------------|
| Global passive observer | Wire taps at IXPs, ISP backbones | [Overview - Mix Networks](/kb/mix-networks/), [MOC - Metadata Privacy](/kb/map-metadata-privacy/) |
| Cloud provider or hypervisor | Read VM RAM, modify boot, snapshot disk | [Overview - Confidential Computing](/kb/confidential-computing/), [Cloud-Provider-Comparison](/kb/confidential-cloud-comparison/) |
| Compromised relay or node | Selective forwarding, traffic injection, dropping | [Overview - Mix Networks](/kb/mix-networks/), [Overview - Decentralized Compute](/kb/decentralized-compute/) |
| Compromised hardware vendor | Sign attestation reports for arbitrary code | [TEE-Side-Channel-Attacks](/kb/tee-side-channel-attacks/), [Attestation-Architecture](/kb/remote-attestation/) |
| Court order or subpoena | Compel logs, key disclosure, code injection | [Overview - Encrypted Messaging](/kb/encrypted-messaging/), [MOC - Censorship Resistance](/kb/map-censorship-resistance/) |
| Supply chain attacker | Inject backdoor at build or package time | reproducible builds, transparency logs |
| 51% or Sybil attacker | Outvote consensus, censor blocks | [Overview - Financial Sovereignty](/kb/financial-sovereignty/), [Overview - Decentralized DNS](/kb/decentralized-dns/) |
| Malicious user device | Full read; export keys | [Overview - Identity & Pseudonymity](/kb/identity-and-pseudonymity/), hardware-wallet patterns |
| Quantum adversary (future) | Solve DLog and factoring | [Overview - Post-Quantum Cryptography](/kb/post-quantum-cryptography/) |

## Recurring trust assumptions

When a system claims a property, ask which of these it requires:

- Trust the CPU vendor: TEEs require Intel, AMD, or NVIDIA not to misissue attestations.
- Trust the CA: TLS without pinning lets any CA mint an MITM cert.
- Trust the registrar or DNS path: can be bypassed by self-authenticating names.
- Tor separates knowledge across relays; it does not protect against an observer who can correlate both ends of a connection merely because one relay is honest.
- Trust the majority of validators: PoS and PoW security models.
- Cryptographic constructions have distinct assumptions: FHE and ZK depend on their schemes, while honest-majority MPC explicitly assumes enough non-colluding participants.
- Trust your own keys and endpoint: true for everything. If your client is compromised, all bets are off.

## Recurring failure modes

| Failure mode | Manifests as | Counter |
|--------------|-------------|---------|
| Side-channel leak | Cache timing, page faults, EM | Defense in depth, multi-vendor TEE, oblivious algorithms |
| Implementation bug | Memory safety, parser issues | Audited primitives, fuzzing, memory-safe languages |
| Operational mistake | Key reuse, absent pinning | Default-secure tooling, hardware key custody |
| Protocol downgrade | Negotiate weak parameters | Strict policy in attestation, no fallback |
| Metadata leak | Even with E2EE | Mixnets, sealed sender, padding |
| Vendor coercion | Court order to ship signed backdoor | Reproducible builds, transparency logs, multi-signer release |
| Lost custody | Key destroyed or stolen | Backups, multisig, social recovery |

## Files with detailed threat models

| File | Adversary focus |
|------|-----------------|
| [TEE-Side-Channel-Attacks](/kb/tee-side-channel-attacks/) | Hardware side channels (Foreshadow, CacheWarp, Hertzbleed, ÆPIC) |
| [Confidential-AI-Inference](/kb/confidential-ai-inference/) | Inference-specific leaks, oracle adversaries |
| [Overview - Mix Networks](/kb/mix-networks/) | Global observer, compromised mixes |
| [Overview - Encrypted Messaging](/kb/encrypted-messaging/) | Court order, server compromise, social-graph leak |
| [Overview - Financial Sovereignty](/kb/financial-sovereignty/) | Custodial counterparty, chain analysis |
| [Overview - Decentralized DNS](/kb/decentralized-dns/) | Registrar coercion, DHT poisoning |
| [Overview - Web of Trust](/kb/web-of-trust/) | Sybil, key compromise, signing equivocation |

## New Threat Models

For new threat models, follow the structure of mature security-analysis files in this library and complete every section before adding the note to an index.

## Primary sources

- [Tor: The Second-Generation Onion Router](https://www.usenix.org/conference/13th-usenix-security-symposium/tor-second-generation-onion-router)
- [RFC 9334: attestation roles and trust](https://www.rfc-editor.org/rfc/rfc9334.html)
- [NIST SP 800-204D: software supply chain security](https://csrc.nist.gov/pubs/sp/800/204/d/final)
- [Secure Multiparty Computation (MPC)](https://eprint.iacr.org/2020/300)
- [Shor: quantum factoring and discrete logarithms](https://arxiv.org/abs/quant-ph/9508027)
