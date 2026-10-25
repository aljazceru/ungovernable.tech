---
title: "drand and tlock"
slug: drand-tlock
type: deep-dive
pillars: ["cryptography"]
readiness: usable
description: "drand supplies threshold-signed randomness; tlock encrypts to a future beacon round. Understand early-release trust, availability and public decryption."
dek: "Timelock encryption delegates the release time to a threshold beacon rather than a single release server."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: ["threshold-signatures", "verifiable-delay-functions", "verifiable-random-functions", "age-encryption"]
---

## Summary

`drand` is a distributed randomness beacon. `tlock` uses an unchained drand network to encrypt data to a future beacon round. When the required round's signature becomes available, it supplies the material needed to unlock the ciphertext.

## How it works

Drand's distributed key generation gives participants shares of a collective secret. A threshold of participants can produce a BLS signature that anyone with the network public key can verify. The League of Entropy operates public drand networks through multiple member organizations.

Tlock combines identity-based encryption with those future signatures. Its `tle` command-line tool accepts a round or duration, and its library wraps the file-encryption key rather than applying the timelock construction directly to every byte. The repository documents an additional encryption layer when only selected recipients should read the released material.

## Trust model / threat model

The threshold participants must not collaborate to release a future signature early. They must also remain able to produce the signature when its round arrives. These are separate confidentiality and availability assumptions: losing enough participants can delay release even if no one learns the plaintext early.

Pin the intended beacon identity and public key. The tool documents using the chain hash to preserve public-key integrity. A test network is not a substitute for the intended production trust set.

## Readiness

**Usable.** The repository provides a Go library, command-line tool and documented mainnet configuration. Review the selected network and recovery needs before encrypting the only copy of important material.

## Limits

Once the round is public, anyone holding an otherwise unprotected tlock ciphertext can decrypt it. Use another encryption layer if access must remain restricted. The project also states that its BLS and identity-based encryption are not post-quantum secure.

This is not a claim that a fixed amount of sequential computation enforces the delay. Compare [verifiable delay functions](/kb/verifiable-delay-functions/), [threshold signatures](/kb/threshold-signatures/) and [age encryption](/kb/age-encryption/).

## Primary sources

- [tlock implementation, security assumptions and CLI](https://github.com/drand/tlock)
- [drand threshold cryptography](https://docs.drand.love/docs/cryptography/)
- [drand implementation and network operation](https://github.com/drand/drand)
- [League of Entropy operators](https://drand.love/loe/)
