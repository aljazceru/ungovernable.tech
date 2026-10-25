---
title: "General-purpose zkVMs"
slug: zkvms
type: deep-dive
pillars: [zk, compute]
readiness: usable
description: "Compare RISC Zero and SP1: program identity, public outputs, private witnesses, proof modes, and the privacy cost of outsourcing proof generation."
dek: "A proof of program execution is useful only when the verifier knows which program and which public statement to accept."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [zero-knowledge-proofs, starks, snarks, decentralized-compute, compare-private-computation]
---

## Summary

A zkVM lets a developer prove the execution of a program rather than design a separate circuit for every application. RISC Zero and SP1 document workflows for compiling programs, generating proofs and verifying results. The name does not guarantee that every available proof format hides the execution witness.

## How it works

The prover executes a guest program with its inputs and generates a proof. The verifier checks the proof against an expected program identity and interprets its public outputs. Approving the program identity is essential: successful verification of somebody else's program does not establish your intended claim.

| Question | RISC Zero | SP1 |
|---|---|---|
| What identifies the program? | An **image ID**, checked when verifying a receipt | A program **verification key**, or its hash in the documented external verifier interface |
| What is public? | The receipt's **journal** contains public program outputs | The program commits **public values**, supplied to verification |
| What does the prover receive? | The guest program and its execution inputs | The compiled program and input stream used for execution |
| Where can proving run? | Local CPU/GPU, or remote proving through Boundless | Local proving, or the Succinct Prover Network |
| Which privacy caveat matters? | Development mode generates no real proof | The security model says individual STARK proofs are not zero-knowledge; its Groth16 and PLONK implementations are |

The [RISC Zero receipt guide](https://dev.risczero.com/api/zkvm/receipts) and [SP1 verification guide](https://docs.succinct.xyz/docs/sp1/generating-proofs/off-chain-verification) describe the verifier interfaces. Pin the program identity through your own build or a trusted distribution channel, then validate the meaning of the public result.

## Trust model / threat model

**Private from whom?** Data omitted from public outputs may be hidden from the proof recipient in an appropriate zero-knowledge mode. It is still available to the machine doing the proving. RISC Zero explicitly recommends local proving for private inputs. The Succinct network assigns requests to third-party provers; outsourcing therefore changes who receives the witness.

**Correct execution is a narrow claim.** SP1's security model requires applications to validate private inputs and hints. A proof does not authenticate an external data source or repair an unsafe program. Bind the expected dataset, authorization rules and requested operation into the statement your verifier accepts.

## Readiness

**Usable for supported developer workflows.** Both projects document proving and verification APIs. This is not a blanket rating of every program, proof mode or network service. Review the chosen backend's security assumptions, including any setup ceremony, and benchmark the actual workload.

## Limits

Proving cost and verification cost are different budgets. SP1 documents trade-offs between core, compressed and wrapped proofs; there is no workload-independent speed ranking here. Use [private computation compared](/kb/compare-private-computation/) to decide whether you need a proof, confidential execution, or both.

## Primary sources

- [RISC Zero receipts and image IDs](https://dev.risczero.com/api/zkvm/receipts)
- [RISC Zero proof-generation options](https://dev.risczero.com/api/generating-proofs/proving-options)
- [SP1 proving basics](https://docs.succinct.xyz/docs/sp1/generating-proofs/basics)
- [SP1 off-chain verification](https://docs.succinct.xyz/docs/sp1/generating-proofs/off-chain-verification)
- [SP1 proof types](https://docs.succinct.xyz/docs/sp1/generating-proofs/proof-types)
- [SP1 security model](https://docs.succinct.xyz/docs/sp1/security/security-model)
- [Succinct Prover Network](https://docs.succinct.xyz/docs/sp1/prover-network/intro)
