---
title: "Katzenpost"
tags:
  - "katzenpost"
  - "mixnet"
  - "post-quantum"
  - "anonymity"
  - "sphinx"
  - "deep-dive"
---
*A research-grade, post-quantum-secure mix network. Loopix-based design with hybrid PQ key exchange built in from the start, federated authority structure, and a clear separation between transport (mix) and applications.*

---

## Position vs Nym

Both Katzenpost and [Nym](/mix-networks/nym) are Loopix-derived mix networks aiming to defeat a global passive adversary. They differ on:

| Aspect | Nym | Katzenpost |
|--------|-----|------------|
| Network type | Permissionless, stake-weighted | Federated; operators run mixes by agreement |
| Token economics | NYM token, on-chain stake | None — operator-funded |
| Post-quantum | Roadmap | Built-in (CTIDH + Kyber hybrid) |
| Maturity | Production network, consumer apps | Research-grade with deployments |
| Sphinx variant | Standard Sphinx | Modified Sphinx with PQ KEM |
| Apps | NymVPN, service providers | Catshadow (messenger), Reunion (key exchange) |

If Nym is "productize Loopix as a market", Katzenpost is "productize Loopix as a federation, with PQ-readiness baked in". Different bets on how anonymity infrastructure should be governed.

---

## Architecture

Same Loopix substrate as Nym:

- Three-tier mixnet with provider nodes at the edges.
- Continuous-time Poisson mixing per node.
- Sphinx-format packets with cover traffic and decoys.
- PKI managed by mix authorities (federation), with voted consensus per epoch.

Differences:

- Authorities are federated, not consensus-elected via stake. The honesty assumption is "majority of authorities honest in the federation".
- Provider nodes work much like Nym's gateways. They accept user packets and deliver to and from the mix.

---

## Post-quantum crypto

Katzenpost was designed with quantum-adversary resistance as a first-class concern. The Sphinx-PQ design uses:

- CTIDH (commutative-isogeny-based DH) and/or Kyber/ML-KEM as the asymmetric primitive for layered encryption.
- Hybrid mode. Classical (X25519) plus PQ KEM, so that breaking either independently doesn't compromise the system.

The reason: harvest-now-decrypt-later. Mixnet traffic is interesting to record now; if the cryptography is broken in the future, the historical metadata could be deanonymized retroactively. PQ-from-the-start is the only defense.

---

## Catshadow messenger

Katzenpost ships a reference messenger, **Catshadow**. Properties:

- E2E encrypted with Signal-like Double Ratchet, ratcheted over the mix transport.
- Per-message routing via separate mix paths. Long-term sender/recipient correlation broken.
- Synchronous and asynchronous delivery via the mixnet's Service Providers.
- Open-source Go implementation.

This is the "Signal but over a mixnet" pattern: Signal-grade content security, mixnet-grade metadata security. The UX is far less polished than Signal. Catshadow is more research artifact than consumer app.

---

## Reunion protocol

A Katzenpost contribution: **Reunion** is a contact-establishment protocol over the mixnet that doesn't require either party to know the other's address in advance. Useful for resilience scenarios where users want to find each other after a disruption without revealing identifiers to the network.

(The concept echoes [Briar](/off-grid-networks/briar)'s contact protocols but executed over a mixnet with stronger anonymity properties.)

---

## Threat model

Same as Loopix-based systems generally:

| Adversary | Status |
|-----------|--------|
| Global passive observer | Defeated under Loopix assumptions |
| Quantum adversary harvesting traffic | Defeated by hybrid PQ KEM |
| Compromised mix subset | Defeated by 3-layer plus cover traffic |
| Compromised authority | Federated honest-majority assumption |
| Endpoint malware | Out of scope |
| Active adversary modifying packets | Replay protection plus integrity |

The PQ angle is what makes Katzenpost distinctive: traffic recorded today survives the day a CRQC (cryptographically relevant quantum computer) appears.

---

## Real-world deployments

- Mix testnet operated by Katzenpost developers and partners.
- OpenDoor (Hashcloak) provided mix capacity.
- Specific NGO and research deployments for journalism and activist scenarios.

Catshadow has been used in workshops and pilot deployments. Less consumer-visible than Nym's NymVPN, but technically interesting for the threat model and PQ readiness.

---

## Trade-offs

### Strengths

- Post-quantum from day one. The only deployed mixnet with this property.
- Federated authority model, which is different governance than stake-weighted.
- Includes a reference messenger (Catshadow) for the full E2E story.
- Reunion protocol for anonymous contact establishment.
- Clean separation between mix transport and applications.

### Limitations

- Research-grade. Smaller deployments, less polished tooling than Tor or Nym.
- Federation requires bootstrap trust. Permissioned set of operators.
- Catshadow UX is barebones.
- Documentation is academic-style, with fewer consumer guides.
- No token economics. Relies on operator funding for sustainability.

---

## Operational patterns

### Threat-model-extreme messaging

For a journalist with a multi-decade secrecy horizon (think nuclear or state-secret leaks), Catshadow's combination of mixnet anonymity plus PQ-secure key agreement is closer to "future-proof" than Signal-over-Tor today.

### Research benchmarking

Katzenpost is the de-facto reference implementation for mixnet research papers. It is the comparison baseline for Loopix variants, PQ Sphinx, and traffic-analysis attacks.

### Hybrid deployments

Katzenpost-style mix transport with custom application protocols on top, an emerging research pattern combining the best parts of MLS / Marmot with mixnet metadata defense.

---

## Recent developments (2024-2026)

- CTIDH integration for compact PQ key exchange in Sphinx.
- Kyber/ML-KEM hybrid completed; running in testnets.
- Catshadow updates: improved key management, multi-device exploration.
- Reunion protocol stabilized.
- Performance work for higher-throughput mixes under cover-traffic load.

---

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Long-term traffic correlation (GPA) | Loopix Poisson plus cover traffic |
| Compromised mix subset | 3-layer architecture |
| Compromised authority majority | Federation diversity is the assumption |
| Quantum cryptanalysis (future) | Hybrid PQ KEM in Sphinx |
| Endpoint compromise | Out of scope |
| Implementation bugs | Open source, ongoing audit |

---

## Comparison summary

| Dimension | Tor | I2P | Nym | Katzenpost |
|-----------|-----|-----|-----|------------|
| Threat: GPA | No | No | Yes | Yes |
| Threat: Quantum harvest | No | No | Roadmap | **Yes** |
| Latency | Sec | Sec | Sec | Sec-tens |
| Token model | None | None | NYM stake | None (federation) |
| Default messenger | None | None | None | Catshadow |
| Maturity | High | Medium | Medium | Research-deployed |

---

## Related files

- [Overview - Mix Networks](/mix-networks)
- [Tor](/mix-networks/tor)
- [I2P](/mix-networks/i2p)
- [Nym](/mix-networks/nym)
- [Overview - Post-Quantum Cryptography](/post-quantum) — hybrid KEM context
- [MOC - Metadata Privacy](/meta/moc-metadata-privacy)

---

## Primary sources

- Katzenpost — [katzenpost.network](https://katzenpost.network)
- Source — [github.com/katzenpost/katzenpost](https://github.com/katzenpost/katzenpost)
- Piotrowska et al., *Loopix*, USENIX 2017.
- Hashcloak / Katzenpost developers, *Post-Quantum Sphinx*, technical reports.
- Reunion protocol specification — Katzenpost docs.
- *CTIDH: Faster Constant-Time CSIDH*, IACR 2021/633.

