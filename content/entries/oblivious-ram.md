---
title: "Oblivious RAM"
slug: oblivious-ram
type: explainer
pillars: [cryptography, confidential]
readiness: research
description: "Oblivious RAM hides storage access patterns, including repeated reads and writes. Learn Path ORAM's design and how it differs from PIR and TEEs."
dek: "Encrypting a block does not hide which block you access next."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [private-information-retrieval, pir-use-cases, confidential-computing, tee-side-channel-attacks, authenticated-data-structures]
---

## Summary

Oblivious RAM, or ORAM, hides a client's sequence of logical memory accesses from an observer of the storage interface. Path ORAM, by Stefanov and colleagues, is documented in [paper 2013/280](https://eprint.iacr.org/2013/280). Its security definition compares access sequences of the same length.

## How Path ORAM works

The server stores encrypted blocks in a tree. The client keeps a **position map** assigning each block to a random leaf and a **stash** for blocks temporarily held outside the tree.

For each logical read or write, the client reads an entire root-to-leaf path, accesses the desired block, assigns it a fresh random leaf, then re-encrypts and writes back the path. Real and dummy blocks occupy the buckets. Repeated access to the same logical block therefore does not simply repeat its physical address.

## ORAM, PIR and TEEs

| Tool | Question it addresses | Integration consequence |
|---|---|---|
| ORAM | Which sequence of blocks did the client read or write? | Maintain private state and transform storage accesses |
| [PIR](/kb/private-information-retrieval/) | Which database item did the reader request? | Choose a retrieval protocol and its server assumptions |
| [TEE](/kb/confidential-computing/) | Can the host inspect protected computation? | Establish a hardware boundary and verify its configuration |

[SimplePIR](https://github.com/ahenzinger/simplepir) illustrates private retrieval from a server-held database. It does not provide a general replacement for an ORAM read/write interface. The Path ORAM paper also discusses secure processors: a protected processor can keep ORAM client state while hiding accesses to external memory. The combined design inherits the processor's trust assumptions.

## Trust model / threat model

Keep the position map, stash and encryption keys within the trusted client boundary. Path ORAM's main presentation does not hide request timing or frequency and treats malicious-server integrity separately. Use [authenticated data structures](/kb/authenticated-data-structures/) when evaluating integrity alongside access-pattern privacy.

## Readiness

**Research as a general integration building block.** The paper provides a construction, analysis and evaluation. That is not evidence that an arbitrary database or enclave becomes oblivious by enabling a setting.

## Limits

Path transfers, client state and stash capacity are additional costs. The paper's asymptotic bounds depend on block-size and storage assumptions; they are not a measured slowdown for your application. Compare [PIR use cases](/kb/pir-use-cases/) before choosing which privacy problem to solve.

## Primary sources

- [Path ORAM, Stefanov et al., ePrint 2013/280](https://eprint.iacr.org/2013/280)
- [Path ORAM full paper, author-submitted manuscript](https://arxiv.org/pdf/1202.5150)
- [SimplePIR and DoublePIR reference implementation](https://github.com/ahenzinger/simplepir)
