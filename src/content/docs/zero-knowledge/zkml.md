---
title: "ZKML"
tags:
  - "zkml"
  - "zk"
  - "machine-learning"
  - "ezkl"
  - "risc-zero"
  - "deep-dive"
  - "ai"
---
*Cryptographic proofs that a specific model produced a specific output for a specific input, without revealing the model, the input, or both. The intersection of ZK and ML is shifting from "research toy" to "deployed primitive" in 2024-2026, with concrete production applications in confidential AI inference, attested AI agents, and verifiable machine-learning pipelines.*

---

## What ZKML provides

Three orthogonal properties; pick which combinations you need:

| Goal | Hides input | Hides model | Proves output |
|------|-------------|-------------|---------------|
| **Verify-only** | No | No | Yes |
| **Private-input verification** | Yes | No | Yes |
| **Private-model verification** | No | Yes | Yes |
| **Fully private inference** | Yes | Yes | Yes |

The most common ZKML pattern in production is verify-only. A user (or auditor) wants to know "this output came from running model M on input X". Neither input nor model is private, but the user wants cryptographic proof rather than the operator's word.

For full privacy, ZKML competes (and composes) with FHE and TEEs:

| Technique | Hides | Trust |
|-----------|-------|-------|
| **ZKML** | Witness from verifier (model and/or input) | Math + prover correctness |
| **FHE** | Plaintext from compute provider | Math (lattice hardness) |
| **TEE** | RAM from cloud / OS / hypervisor | Hardware vendor |

---

## The cost problem

A medium-sized neural network forward pass involves billions of arithmetic operations. Naively SNARKing a forward pass produces an enormous circuit. The 2022 state of the art could prove a small CNN inference in tens of minutes; large transformers were impossible.

Folding schemes ([Folding Schemes](/zero-knowledge/folding-schemes)) and lookup arguments changed this. Per-layer or per-operation folding lets you prove inference incrementally. Lookup arguments make non-arithmetic operations (ReLU, softmax, attention) cheap.

By 2024-2026, ZKML proving for small-to-medium models is practical:

- ResNet-50 in seconds to minutes.
- BERT-base in tens of minutes.
- Small transformers (~7B params) in hours, with hardware acceleration.
- Frontier-scale (~70B+) still impractical for full proofs.

---

## Major ZKML frameworks (2026)

### EZKL

Open-source, Halo2-based ZKML compiler. Takes ONNX models as input; generates Halo2 circuits for inference proving. Used in production for verifiable model serving, on-chain ML, and AI auditing.

Workflow:

```
your_model.onnx ─► ezkl ─► Halo2 circuit + setup
inference call → ezkl prove → SNARK proof of (input, output, model_hash)
on-chain or off-chain verifier checks proof
```

Strong tooling; the most-used ZKML framework in production.

### Risc0 / SP1 / Jolt for ML

Rather than compile the model into a custom ZK circuit, run it inside a RISC-V zkVM. Trade-off: simpler developer experience (just regular code), worse performance than circuit-specific provers like EZKL.

For small or experimental models, this is the path of least resistance.

### Giza

ZKML platform built on Cairo / StarkNet. Targets verifiable AI agents on-chain.

### Modulus Labs

Production ZKML for on-chain AI services. Demonstrated verifiable inference for trading bots, DAO decision-makers, and AI-driven oracle systems.

### Lattigo + ZK / hybrid systems

Some research combines lattice-based ML primitives (FHE-style) with ZK for the proving layer.

---

## Use cases

### Verifiable LLM endpoint

Pattern: a model owner publishes the model hash; the inference operator generates a ZK proof that "this output came from running model M on input X." The user verifies the proof and decrypts the output.

Composition:

```
Model owner ─► commit model hash on-chain
User       ─► input → operator's API
Operator  ─► run inference, generate ZK proof of (input, output, model_hash)
User       ─► verify proof, accept output
```

This is the verify-only pattern. For input privacy, combine with TEE or FHE.

### On-chain AI agents

A smart contract acts as a buyer or arbitrator that needs AI judgment. A ZKML proof lets the contract verify "this AI's judgment came from running this model on these inputs" without trusting the AI service. Used for: oracle computations, prediction markets, verifiable ML-driven yield strategies.

### Privacy-preserving model serving

A medical model is run on patient data; the patient gets a diagnosis with proof of correct execution. Combine with FHE or TEE for input privacy. ZKML proves the diagnosis came from the agreed model; FHE / TEE keeps the input data confidential.

### Verifiable model audits

A regulator wants to verify that a deployed model is the same as the one passed audit. Hash the model post-audit; require ZKML proofs that production inferences come from that hash.

### AI-output watermarking and attribution

Combined with cryptographic signatures, ZKML can prove "this output came from this model at this time", a content-attribution primitive useful in disputes about generated content.

---

## Architecture patterns

### ZKML + TEE

Operator runs the model in a TEE (TDX + H100 CC), generating an attested TLS endpoint. The TEE also generates a ZKML proof for each inference. The ZK proof can be verified by parties that don't trust the hardware vendor; the TEE attestation guarantees the proof was generated honestly.

Result: defense in depth. TEE for confidentiality, ZK for verifiability without TEE trust.

### ZKML + FHE

Input encrypted under FHE; operator runs the model homomorphically; outputs encrypted ciphertext. ZKML proof certifies the homomorphic computation matches the agreed model. (This is essentially **vFHE** ([FHE Bootstrapping and Verification](/cryptography/fhe-bootstrapping-and-verification)) specialized to ML circuits.)

### ZKML standalone

For verify-only use cases where input and model aren't sensitive, just proving the model ran correctly. Cheapest ZKML option.

---

## Performance snapshot (early 2026)

| Model | Framework | Prove time | Proof size |
|-------|-----------|-----------|-----------|
| MLP (tiny) | EZKL | seconds | ~10 KB |
| ResNet-50 | EZKL | minutes | ~30 KB |
| BERT-base | EZKL or zkVM | tens of minutes | ~50 KB |
| Llama-7B (research) | Specialized provers | hours | ~100 KB |
| Frontier (Llama-70B+) | Not yet practical | — | — |

GPU acceleration (Cysic, Ingonyama) reduces these by 10-50x for supported pipelines. Folding schemes are bringing per-layer costs down.

---

## Trade-offs

### Strengths

- Cryptographic verification of ML, no operator trust required.
- Composable with FHE and TEEs for orthogonal protections.
- Production tooling maturing rapidly (EZKL, Modulus, Giza).
- Auditable AI. Regulators and users can verify deployed models.

### Limitations

- Prover cost. Minutes-to-hours for non-trivial models.
- Frontier-scale impractical. 70B+ models out of reach for full ZK proofs.
- Quantization required. ZKML works in fixed-point fields, not floats. Models must be quantized; precision loss can affect output.
- Trusted setup for some Halo2 deployments (mitigated by transparent variants).
- Operational complexity. Managing model hashes, circuit setups, and verifier contracts adds infrastructure burden.

---

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Quantization-induced output divergence | Match quantization scheme prove-side and inference-side; deterministic models |
| Prover supplies wrong input commitment | Bind input to public commitment; verifier checks |
| Model substitution | Model hash committed publicly; verifier checks |
| Soundness bug in circuit | Audit circuit code; formal verification |
| Side-channel on prover | Constant-time proving libraries |
| Model exfiltration via inference oracle | Compose with FHE / TEE for input privacy |

---

## Recent developments (2024-2026)

- EZKL stabilizes as the production ZKML framework.
- Folding-based ZKML brings per-layer proving into reach.
- GPU prover acceleration drops prove times by 10-50x.
- Verifiable AI agents on-chain (Modulus, Giza demonstrations).
- AI watermarking plus ZKML combinations explored for content-attribution.
- Model-on-FHE-with-ZK research for full vFHE ML.

---

## Related files

- [Overview - Zero-Knowledge Proofs](/zero-knowledge)
- [SNARKs](/zero-knowledge/snarks)
- [Folding Schemes](/zero-knowledge/folding-schemes)
- [FHE Bootstrapping and Verification](/cryptography/fhe-bootstrapping-and-verification)
- [Confidential-AI-Inference](/confidential-computing/confidential-ai-inference)
- [Decentralized Training](/decentralized-compute/decentralized-training)
- [MOC - Composing Primitives](/meta/moc-composing-primitives)

---

## Primary sources

- Liu, Xie, Zhang, *zkCNN: Zero-knowledge Proofs for Convolutional Neural Networks*, CCS 2021.
- ZKonduit / EZKL — [github.com/zkonduit/ezkl](https://github.com/zkonduit/ezkl).
- Modulus Labs — [moduluslabs.xyz](https://moduluslabs.xyz).
- Giza — [gizatech.xyz](https://gizatech.xyz).
- Risc0 / SP1 / Jolt for ML.
- *zkML survey* (assorted 2024-2025 papers — see arXiv `cs.CR` cross-listings).

