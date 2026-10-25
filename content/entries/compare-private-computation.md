---
title: "Private computation compared"
slug: compare-private-computation
type: comparison
pillars: [cryptography, confidential, zk]
description: "Compare MPC, FHE, zero-knowledge proofs, TEEs and PIR by what they hide, who must be trusted, practical cost and implementation readiness."
dek: "Start with who must not learn what, then choose the computation model."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [multi-party-computation, fully-homomorphic-encryption, zero-knowledge-proofs, confidential-computing, private-information-retrieval, oblivious-ram, zkvms]
---

## Summary

These mechanisms solve different privacy problems. The matrix summarizes the existing entries, using the primary implementations and specifications below to qualify their assumptions. Readiness belongs to a concrete protocol and implementation, not an acronym.

## What is hidden from whom?

| Mechanism | Hidden information | Who still learns something? | Trust assumption to check |
|---|---|---|---|
| [MPC](/kb/multi-party-computation/) | Participants' inputs from other participants, within the protocol's corruption model | Authorized recipients learn the agreed output | Allowed collusion threshold; passive versus malicious security; input and output policy |
| [FHE](/kb/fully-homomorphic-encryption/) | Plaintext inputs and results from an evaluator without the decryption key | Key holders can decrypt; the evaluator performs the chosen computation | Encryption parameters and key custody; separate assurance of correct evaluation |
| [ZK proofs](/kb/zero-knowledge-proofs/) | Witness from the verifier, in a zero-knowledge proof mode | Prover knows its witness; verifier learns the public statement | Sound proof system, correct program/circuit, approved verifier parameters and any setup assumptions |
| [TEE](/kb/confidential-computing/) | Protected memory from actors outside the supported hardware boundary | The program inside sees plaintext; its outputs disclose what it permits | Hardware, firmware, attestation roots, measured software and verifier policy |
| [PIR](/kb/private-information-retrieval/) | Requested item/index from the database service | Client receives the item; server may still see connection metadata | Computational assumptions for single-server schemes, or non-collusion for relevant multi-server schemes |

These are privacy boundaries, not guarantees about whether an answer is safe to reveal. Output policy matters for every row. A membership result can disclose sensitive information even when intermediate computation stays private.

## Cost and readiness

| Mechanism | Practical performance class | Readiness boundary |
|---|---|---|
| MPC | Interactive work; protocol choice, communication and preprocessing matter | Implementations cover several security models; choose the one your deployment satisfies |
| FHE | Substantial arithmetic and ciphertext overhead; operation mix and parameters dominate | Libraries support concrete encrypted arithmetic; porting an arbitrary program is a separate engineering task |
| ZK | Proof generation adds work; proof mode determines proof size and verification cost | [zkVMs](/kb/zkvms/) offer developer workflows, but validity-only proof modes must not be assumed private |
| TEE | Hardware execution with isolation, enclave transitions and memory constraints | [Gramine](/kb/gramine/) documents an SGX implementation; host support and application review remain necessary |
| PIR | Server computation and preprocessing can dominate retrieval; database shape matters | SimplePIR's repository explicitly labels its implementation a research prototype |

This is a qualitative comparison. No universal slowdown factor or fastest system follows from these sources. Measure the whole path, including preprocessing, network transfer and verification, for the intended workload.

## Choosing and composing

- To compute across independently held inputs, start with MPC and define collusion and output rules.
- To outsource operations while retaining the decryption key, evaluate FHE and decide how to check the answer.
- To check execution, choose a proof system and fix the program identity. To hide the witness too, verify its zero-knowledge mode.
- To release secrets to an approved workload, use [attestation verification](/guides/verifying-a-confidential-workload/).
- To hide which record you retrieve, compare [PIR use cases](/kb/pir-use-cases/). To hide a sequence of storage reads and writes, investigate [ORAM](/kb/oblivious-ram/).

## Primary sources

- [MP-SPDZ security models and protocol selection](https://mp-spdz.readthedocs.io/en/latest/readme.html)
- [Microsoft SEAL: encrypted arithmetic and its limitations](https://github.com/microsoft/SEAL)
- [Microsoft SEAL security requirements, including integrity](https://github.com/microsoft/SEAL/blob/main/SECURITY.md)
- [SP1 security model, including proof privacy](https://docs.succinct.xyz/docs/sp1/security/security-model)
- [SP1 proving and execution costs](https://docs.succinct.xyz/docs/sp1/generating-proofs/basics)
- [SP1 proof-format trade-offs](https://docs.succinct.xyz/docs/sp1/generating-proofs/proof-types)
- [Gramine SGX concepts](https://gramine.readthedocs.io/en/stable/sgx-intro.html)
- [RFC 9334: attestation trust and appraisal](https://www.rfc-editor.org/rfc/rfc9334.html)
- [SimplePIR and DoublePIR reference implementation](https://github.com/ahenzinger/simplepir)
