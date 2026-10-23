---
title: "Cover Traffic and Constant-Rate Padding"
slug: cover-traffic
type: explainer
pillars: [anonymity]
description: "Encryption hides message contents, not the pattern of sending. Cover traffic and constant-rate padding hide that pattern from an observer watching the wire, at a cost."
dek: "An observer who cannot read your messages can still learn a lot from when and how much you send. Cover traffic fills the silences so the pattern says nothing."
updated: 2026-10-18
created: 2026-10-18
origin: original
related: [mix-networks, loopix, nym, katzenpost, sphinx-packet-format, metadata-resistance, global-passive-adversary, tor]
---

Encryption protects the contents of a message. It does nothing to hide *that* a message was sent, *when*, *how large* it was, or *how often* you communicate. To an adversary who can watch the links — an ISP, a backbone tap, a [global passive adversary](/kb/global-passive-adversary/) — that pattern alone is often enough to identify who is talking to whom and to correlate the two ends of an anonymity network by timing and volume. Cover traffic is the family of defences that attack this leak directly, by making the pattern of transmission independent of the real messages underneath.

## The idea

The problem with real traffic is that it is *bursty and informative*: silence when you have nothing to say, a spike when you do. Cover traffic (also called chaff or dummy traffic) adds padding packets that are indistinguishable, once encrypted, from real ones. Done thoroughly, the sequence of packets an observer sees no longer depends on your actual activity.

There are two broad strategies:

- **Constant-rate (CBR) padding** — a link sends a fixed-size packet at a fixed interval no matter what. When you have real data it rides inside the next slot; when you do not, a dummy goes out instead. The observed stream is a metronome, revealing nothing about the payload. The cost is blunt: you pay for the full rate continuously, and the rate caps your real throughput.
- **Randomized / Poisson cover** — instead of a rigid clock, each node emits packets according to a random (typically Poisson) process. This provides strong statistical cover with less rigidity, and lets dummy packets double as probes that loop through the network to detect active attacks.

## Where it is used

- **[Mix networks](/kb/mix-networks/)** were the first systems to take this seriously. [Loopix](/kb/loopix/) (2017) is the canonical modern design: it combines per-link Poisson cover traffic with *loop* traffic — dummies a node sends to itself through the network — to get provable anonymity against an adversary watching every link ([USENIX Security 2017](https://www.usenix.org/conference/usenixsecurity17/technical-sessions/presentation/piotrowska)). Its descendants, [Nym](https://nymtech.net/) and [Katzenpost](/kb/katzenpost/), ship cover traffic in production.
- **[Tor](/kb/tor/)** does not use full constant-rate padding — it would be far too expensive for low-latency browsing — but it does deploy lighter *circuit padding* to blunt specific traffic-analysis and website-fingerprinting attacks, descended from the WTF-PAD design ([paper](https://arxiv.org/abs/1512.00524)); see the [Tor padding specification](https://spec.torproject.org/padding-spec/).

All of these rely on a packet format in which real and dummy traffic are byte-for-byte indistinguishable, such as the [Sphinx packet format](/kb/sphinx-packet-format/).

## The cost, and why most systems skip it

Cover traffic is not free, and the trade-off explains why most of the internet does without it:

- **Bandwidth.** Constant-rate schemes transmit continuously; much of that is dummy data someone has to pay for and carry.
- **Latency.** Strong metadata protection usually means batching or delaying messages, which suits email- and messaging-style use but not live browsing or voice.
- **Battery and metered links.** A phone that must emit a steady stream of padding pays for it in power and data.

This is the central tension of [metadata resistance](/kb/metadata-resistance/): the defences that work are expensive, so systems either accept the cost for a narrow use case (high-latency mixnets) or apply partial padding and accept weaker guarantees (Tor). An honest reading is that cover traffic is well understood in theory and deployed in a handful of mix networks, but remains too costly for most mainstream tools — which is exactly why the metadata leak persists.

## What it protects against, and what it does not

Cover traffic defends against **traffic-analysis and end-to-end correlation** by an observer of the links. It does **not** hide content (that is encryption's job), does not protect against an endpoint that is itself compromised, and does not help if the padding is imperfect — a scheme that pads only in one direction, or whose dummies are distinguishable from real packets under load, can leak the very signal it was meant to bury. Padding is only as good as its indistinguishability.
