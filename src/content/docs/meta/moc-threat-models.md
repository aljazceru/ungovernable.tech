---
title: "Threat Models"
tags:
  - "meta"
  - "moc"
  - "threat-model"
  - "overview"
---
*A Map of Content indexing recurring adversaries, trust assumptions, and failure modes across the vault.*

> Threat-modeling rule: name the adversary, name the asset, name the assumption you make about each component. If you cannot write it down, you do not have a threat model. You have hope.

---

## Recurring adversaries

| Adversary | Capability | Where it appears |
|-----------|------------|------------------|
| Global passive observer | Wire taps at IXPs, ISP backbones | [Overview - Mix Networks](/mix-networks), [MOC - Metadata Privacy](/meta/moc-metadata-privacy) |
| Cloud provider or hypervisor | Read VM RAM, modify boot, snapshot disk | [Overview - Confidential Computing](/confidential-computing), [Cloud-Provider-Comparison](/confidential-computing/cloud-provider-comparison) |
| Compromised relay or node | Selective forwarding, traffic injection, dropping | [Overview - Mix Networks](/mix-networks), [Overview - Decentralized Compute](/decentralized-compute) |
| Compromised hardware vendor | Sign attestation reports for arbitrary code | [TEE-Side-Channel-Attacks](/confidential-computing/tee-side-channel-attacks), [Attestation-Architecture](/confidential-computing/attestation-architecture) |
| Court order or subpoena | Compel logs, key disclosure, code injection | [Overview - Encrypted Messaging](/encrypted-messaging), [MOC - Censorship Resistance](/meta/moc-censorship-resistance) |
| Supply chain attacker | Inject backdoor at build or package time | reproducible builds, transparency logs |
| 51% or Sybil attacker | Outvote consensus, censor blocks | **Overview - Financial Sovereignty**, [Overview - Decentralized DNS](/decentralized-dns) |
| Malicious user device | Full read; export keys | [Overview - Identity & Pseudonymity](/identity), hardware-wallet patterns |
| Quantum adversary (future) | Solve DLog and factoring | [Overview - Post-Quantum Cryptography](/post-quantum) |

---

## Recurring trust assumptions

When a system claims a property, ask which of these it requires:

- Trust the CPU vendor: TEEs require Intel, AMD, or NVIDIA not to misissue attestations.
- Trust the CA: TLS without pinning lets any CA mint an MITM cert.
- Trust the registrar or DNS path: can be bypassed by self-authenticating names.
- Trust at least one honest relay: Tor relies on this for onion routing.
- Trust the majority of validators: PoS and PoW security models.
- Trust no party: pure cryptographic constructions (FHE, ZK, MPC with honest majority).
- Trust your own keys and endpoint: true for everything. If your client is compromised, all bets are off.

---

## Recurring failure modes

| Failure mode | Manifests as | Counter |
|--------------|-------------|---------|
| Side-channel leak | Cache timing, page faults, EM | Defense in depth, multi-vendor TEE, oblivious algorithms |
| Implementation bug | Memory safety, parser issues | Audited primitives, fuzzing, memory-safe languages |
| Operational mistake | Key reuse, missing pinning | Default-secure tooling, hardware key custody |
| Protocol downgrade | Negotiate weak parameters | Strict policy in attestation, no fallback |
| Metadata leak | Even with E2EE | Mixnets, sealed sender, padding |
| Vendor coercion | Court order to ship signed backdoor | Reproducible builds, transparency logs, multi-signer release |
| Lost custody | Key destroyed or stolen | Backups, multisig, social recovery |

---

## Files with detailed threat models

| File | Adversary focus |
|------|-----------------|
| [TEE-Side-Channel-Attacks](/confidential-computing/tee-side-channel-attacks) | Hardware side channels (Foreshadow, CacheWarp, Hertzbleed, ÆPIC) |
| [Confidential-AI-Inference](/confidential-computing/confidential-ai-inference) | Inference-specific leaks, oracle adversaries |
| [Overview - Mix Networks](/mix-networks) | Global observer, compromised mixes |
| [Overview - Encrypted Messaging](/encrypted-messaging) | Court order, server compromise, social-graph leak |
| **Overview - Financial Sovereignty** | Custodial counterparty, chain analysis |
| [Overview - Decentralized DNS](/decentralized-dns) | Registrar coercion, DHT poisoning |
| [Overview - Web of Trust](/cryptography/overview-web-of-trust) | Sybil, key compromise, signing equivocation |

---

## Template

For new threat models, use **Threat Model Template**.

