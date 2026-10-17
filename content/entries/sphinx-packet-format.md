---
title: "Sphinx Packet Format"
slug: sphinx-packet-format
type: explainer
pillars: ["anonymity", "cryptography"]
description: "Sphinx, the compact, provably secure onion packet format used by modern mix networks and Lightning: how it hides route and position."
dek: "A fixed-size, provably-secure onion-routed packet format. The cryptographic substrate underlying every modern mixnet — Nym, Katzenpost, HOPR, the Lightning Network Deep Dive payment routing, and Loopix-derived research designs."
updated: 2026-06-13
created: 2026-04-26
origin: vault
source: "08-Mix-Networks/Sphinx Packet Format.md"
aliases: ["Sphinx", "Sphinx Mix Format"]
tags: ["sphinx", "mix-networks", "onion-routing", "cryptography", "packet-format", "deep-dive", "post-quantum", "outfox"]
---

## What problem Sphinx solves

Earlier onion-routing formats (Type-II Mixmaster, Tor relay cells, Mixminion) had observable distinctions between forward packets, reply packets, and packets at different positions in their route. An adversary watching multiple links could fingerprint a packet's hop count, payload size, or header structure and use those features to correlate ingress and egress.

Sphinx (Danezis & Goldberg, "Sphinx: A Compact and Provably Secure Mix Format", IEEE S&P 2009) was designed to give *every* packet at *every* hop the same observable shape. The properties it guarantees:

- **Bitwise indistinguishability**. Every packet on the wire is the same fixed length, regardless of position in route or payload type.
- **Per-hop unlinkability**. The output of a mix node is unlinkable to its input by anyone other than that mix.
- **Replay protection**. Each mix detects and drops packets it has already processed.
- **Tagging-attack resistance**. Active modification of any byte in transit is detected by the next honest mix.
- **Compact**. Header size grows linearly in maximum hop count but with a small constant, and the body is a single fixed buffer.

Provable security against an active adaptive adversary in the Universal Composability framework, under standard cryptographic assumptions (DDH in the chosen group, PRP security of the underlying block cipher).

## Packet structure

A Sphinx packet is the tuple `(α, β, γ, δ)`:

```
+-----------+--------------+-----+--------------------+
|     α     |      β       |  γ  |         δ          |
| group elt | routing info | MAC |    body (payload)  |
+-----------+--------------+-----+--------------------+
   32 B          ~routing      16 B    fixed (e.g. 1024 B)
```

- **α (alpha)**: a group element (typically a Curve25519 point, 32 bytes). The current hop's ECDH input.
- **β (beta)**: the routing-information header. A fixed-size buffer encrypted in layers, one per hop. Includes the next-hop address and per-hop instructions.
- **γ (gamma)**: a MAC over `β` keyed by the per-hop shared secret. Detects tagging attacks.
- **δ (delta)**: the payload body. Encrypted in layers (one peeled per hop). Reaches the final recipient as plaintext after the last layer is stripped.

### Per-hop processing

When mix `i` receives `(α_i, β_i, γ_i, δ_i)`:

1. Derive shared secret `s_i = H(α_i^{x_i})` where `x_i` is the mix's private key.
2. Verify `γ_i == MAC(s_i, β_i)`. Drop on mismatch.
3. Check `H(s_i)` against the replay-detection set. Drop on hit.
4. Decrypt one layer of `β_i` using the stream cipher keyed by `s_i`, revealing the next-hop address and `(γ_{i+1}, β_{i+1})`.
5. Blind `α_i` to produce `α_{i+1} = α_i^{b_i}` where `b_i = H(α_i, s_i)`. This is the trick that makes alpha unlinkable across hops.
6. Decrypt one layer of `δ_i` using a PRP keyed by `s_i`, producing `δ_{i+1}`.
7. Forward `(α_{i+1}, β_{i+1}, γ_{i+1}, δ_{i+1})` to the next hop.

The blinding step is the critical innovation. Without it, an adversary sees `α_i` enter mix `i` and `α_{i+1}` leave; both could be linked by replay. With the blinding factor `b_i` derived from the shared secret, only the next hop (which knows `s_i`) can recompute the relation; everyone else sees a fresh, uncorrelated group element.

## Single-use reply blocks (SURBs)

Sphinx supports anonymous replies via SURBs. The recipient generates a partially-constructed Sphinx header that encodes a return route back to themselves, then sends it (in the body of an outbound packet) to a correspondent who doesn't know the recipient's address. The correspondent uses the SURB to build a reply packet without ever learning the route.

Each SURB is single-use to prevent intersection attacks across multiple replies. This pattern enables anonymous-by-default protocols (e.g., the [Loopix](/kb/loopix/) message system, [Katzenpost](/kb/katzenpost/)'s Catshadow).

## Indistinguishability properties

Three classes of indistinguishability are formally proved:

1. **Path indistinguishability**: an honest mix cannot tell from its input whether it is the first, middle, or last hop on the path.
2. **Reply indistinguishability**: a forward packet and a reply packet are indistinguishable to any mix other than the one acting on them.
3. **Hop indistinguishability**: any two packets on the same link are indistinguishable except by their (hidden) routing info.

These translate into the operational property that a global passive adversary cannot trace a packet through the network better than chance, given a sufficiently mixed traffic pattern (which is what Loopix-style cover traffic plus delays guarantees at the network level).

## Adoption

| System | Sphinx variant | Notes |
|--------|---------------|-------|
| [Lightning Network Deep Dive](/kb/lightning-network/) | BOLT 4 onion routing | HTLC payment routing uses Sphinx for the per-hop encrypted info. Fixed 1300-byte hop_payloads buffer |
| [Nym](/kb/nym/) | Standard Sphinx (X25519) | Default Loopix-style mixnet packets |
| [Katzenpost](/kb/katzenpost/) | Sphinx-PQ (hybrid X25519 + ML-KEM/CTIDH) | Post-quantum modification |
| [HOPR](/kb/hopr/) | Sphinx over libp2p | With per-hop ticket attachments |
| Loopix research | Standard Sphinx | The reference implementation |
| Mixminion (legacy) | Pre-Sphinx, similar concept | Predecessor; see [Mixminion and Mixmaster](/kb/mixminion-and-mixmaster/) |

The Lightning adoption is significant: the most production-deployed instance of Sphinx in the world is in payment routing, not anonymity, because the format's "every hop sees only the next hop" property maps directly onto multi-hop payment privacy.

## Comparison vs Tor's relay protocol

Tor uses fixed-size 514-byte cells but a different structure:

| Property | Sphinx | Tor cells |
|----------|--------|-----------|
| Cell size | Fixed (whole packet) | Fixed (one cell per relay command) |
| Encryption | Per-hop layered ECDH derivation, blinded group element | Per-hop AES-CTR keyed by ntor handshake |
| Per-hop info | Self-contained in `β` | Out-of-band (circuit established beforehand) |
| Replay protection | Per-mix bloom filter | Counter mode prevents replay implicitly |
| Reply mechanism | SURBs | Bidirectional circuits |
| Connection model | Connectionless (per-packet routing) | Circuit-oriented (long-lived) |

Tor's circuit model is faster (one handshake amortized across many cells) but requires correlation-vulnerable persistent circuits. Sphinx's per-packet model is slower per packet but allows each packet to take an independent route, which is the property packet mixnets exploit for Loopix-style mixing.

## Post-quantum extensions

The original Sphinx uses Diffie-Hellman in a prime-order group (X25519 or similar). A quantum adversary running Shor's algorithm could retroactively decrypt recorded mixnet traffic, breaking the harvest-now-decrypt-later defense.

Two main lines of post-quantum Sphinx work:

- **Hybrid X25519 + ML-KEM (Kyber)**. Per-hop key derivation combines a classical ECDH share with a Kyber KEM share. Breaking either alone leaks no per-hop key material. This is the approach in [Katzenpost](/kb/katzenpost/)'s deployment as of 2025.
- **CTIDH (commutative isogeny-based DH)**. A post-quantum drop-in for DH with the same algebraic structure (group action) that Sphinx requires. See *CTIDH: Faster Constant-Time CSIDH* (IACR 2021/633). Smaller keys than Kyber but slower operations.

The design challenge is preserving Sphinx's compactness — Kyber public keys are roughly 800 bytes versus 32 bytes for X25519, which inflates the per-hop header size unless careful packing or aggregated KEM techniques are used. Research in 2023-2025 has produced PQ-Sphinx variants with manageable header growth (factor of ~2-4x classical) at the cost of additional CPU cost per hop.

### Outfox: PQ packet format for layered mixnets (ACM SIGCOMM 2025)

**Outfox** (Groth, 2025 / ACM SIGCOMM) is the most concrete post-quantum Sphinx variant to date. It addresses the fundamental size-inflation problem that makes naïve Kyber-Sphinx distinguishable: if classical Sphinx packets and PQ-Sphinx packets have different header lengths, a global passive adversary can segment the network into PQ-using and non-PQ-using nodes and attack the weaker cohort.

Outfox's design:
- **Simplified packet geometry**: Unlike original Sphinx, Outfox is designed for *fixed-route layered mixnets* (every packet goes through exactly one mix per layer, no branching). This simplifies the header structure and removes the need for variable-length routing info that caused size inflation in naive PQ extensions.
- **Hybrid KEM encapsulation**: Combines X25519 with an ML-KEM variant at each hop. The key innovation is using a *single combined ciphertext* that is the same size class regardless of which KEM is used — careful algebraic construction of the KEM scheme lets both classical and PQ shares fit in a uniform header slot.
- **Preserved Sphinx properties**: Bitwise indistinguishability, per-hop unlinkability, tagging-attack resistance, replay protection — all formally proved in the paper.
- **Concrete sizes**: Outfox reports header sizes roughly 2.5-3x classical Sphinx, within acceptable bounds for practical deployment.

Outfox matters for [Nym](/kb/nym/) and [Katzenpost](/kb/katzenpost/) because it is the reference design that any production PQ Sphinx upgrade will likely converge on. Nym's long-term PQ roadmap (upgrading the Sphinx packet layer beyond the current Lewes Protocol handshakes) explicitly identifies this class of design. [Katzenpost](/kb/katzenpost/)'s hpqc library already implements hybrid KEMs, so an Outfox-style refactoring of the Sphinx layer is the logical next step.

**Primary source**: Groth et al., "Outfox: A Postquantum Packet Format for Layered Mixnets," ACM SIGCOMM 2025. [arXiv:2412.19937](https://arxiv.org/html/2412.19937v2)

## Trade-offs

### Strengths

- Provably secure under standard assumptions.
- Fixed packet size eliminates an entire class of fingerprinting attacks.
- Compact relative to alternatives (Mixminion, naïve onion encryption).
- Connectionless: each packet routes independently, enabling per-packet mixing.
- Well-studied; over 15 years of follow-on analysis.

### Limitations

- Per-hop ECDH cost. Each mix does a public-key operation per packet.
- Header size grows linearly with maximum hop count, capping practical route length.
- Replay protection requires per-mix state (bloom filter). State management is non-trivial at scale.
- Original construction is not post-quantum; PQ variants inflate sizes.
- Tagging attacks against `δ` are detected only at the *next* honest mix, so an attacker can corrupt a packet and observe which subsequent hop drops it (a known limitation, addressed in subsequent constructions like HORNET and Mix1 designs).

## Primary sources

- Danezis, G., Goldberg, I. *Sphinx: A Compact and Provably Secure Mix Format*. IEEE Symposium on Security and Privacy, 2009. [cypherpunks.ca/~iang/pubs/Sphinx_Oakland09.pdf](https://cypherpunks.ca/~iang/pubs/Sphinx_Oakland09.pdf)
- Piotrowska et al. *The Loopix Anonymity System*, USENIX Security 2017 (uses Sphinx as the substrate).
- BOLT #4: Onion Routing Protocol, [github.com/lightning/bolts/blob/master/04-onion-routing.md](https://github.com/lightning/bolts/blob/master/04-onion-routing.md).
- Beato, F., Halunen, K., Mennink, B. *Improving the Sphinx Mix Network*. IACR ePrint 2016/489.
- Katzenpost PQ-Sphinx specification — [github.com/katzenpost/katzenpost/tree/main/docs](https://github.com/katzenpost/katzenpost/tree/main/docs).
- *CTIDH: Faster Constant-Time CSIDH*, IACR 2021/633.
- Groth et al., *Outfox: A Postquantum Packet Format for Layered Mixnets*, ACM SIGCOMM 2025. [arXiv:2412.19937](https://arxiv.org/html/2412.19937v2)
