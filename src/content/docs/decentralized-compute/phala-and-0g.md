---
title: "Phala and 0G"
tags:
  - "phala"
  - "0g"
  - "tee"
  - "decentralized-compute"
  - "attestation"
  - "deep-dive"
---
*Two TEE-first decentralized compute networks. Phala has the longer track record and the more mature TEE marketplace; 0G adds a "decentralized AI OS" framing with Phala as one of its compute layers. Both pin attestation reports on-chain so workloads carry verifiable trust from the silicon up.*

---

## Phala — position

Phala is the most-developed TEE marketplace in decentralized compute. Its evolution:

- Phase 1 (2018-2022): SGX-based confidential smart contracts.
- Phase 2 (2022-2024): Phala Cloud, a TEE marketplace running TDX, SEV-SNP, and NVIDIA H100 CC workloads.
- Phase 3 (2024-2026): `dstack`, a developer SDK that packages docker-compose-style workloads into TDX confidential VMs with on-chain attestation.

The differentiating claim is **on-chain attestation**. A Phala workload's attestation report is anchored to the Phala chain (or relayable to Ethereum or other chains), so any smart contract or off-chain client can verify "this workload runs the agreed binary in a real TDX VM" without trusting Phala itself.

---

## dstack — the developer story

```
Developer:
  - writes a docker-compose.yml
  - signs a manifest committing to the image hashes
  - deploys via Phala Cloud SDK

Phala:
  - allocates a TDX CVM on a participating provider
  - provider boots the docker-compose, fetches images by hash
  - TDX produces an attestation report covering the boot + image set
  - report posted on-chain

Client:
  - queries on-chain attestation
  - verifies provider's TDX certificate chain
  - obtains TLS-bound key from inside the enclave
  - establishes attested TLS to the workload
```

Effects:

- Familiar UX (docker-compose, not raw enclave SDK).
- Reproducible builds via manifest-pinned image hashes.
- On-chain verifiability so anyone can audit the trust chain.
- Multi-provider: workloads can move providers and re-attest.

This is the cleanest decentralized confidential-compute developer story in 2026.

---

## Phala for confidential AI

The flagship use case. A model owner ships an open-weights or proprietary LLM to a Phala dstack workload running TDX + H100 CC. End users connect over attested TLS, verify the attestation, and send prompts. Three properties hold:

- The operator can't read prompts. TDX + H100 CC encrypts everything.
- The operator can't extract model weights. GPU memory is encrypted.
- The client can verify that the workload runs the published binary on the published model.

Used in production by partners offering "open inference" services to users who don't want to send prompts to OpenAI.

---

## 0G — position

0G frames itself as a "decentralized AI OS" — broader scope than just compute. Components:

- 0G Storage: decentralized object storage with verifiable retrieval.
- 0G Compute: TEE-attested compute, often using Phala as the underlying infrastructure.
- 0G DA (Data Availability): modular DA layer for rollups.
- 0G Consensus: Cosmos-style chain anchoring everything.

The thesis is that training and serving large models requires storage, compute, data availability, and verifiable attestation. 0G assembles these into one tightly integrated stack rather than relying on independent providers for each.

In practice, 0G's compute layer composes with Phala (TEE attestation) and adapts the broader Cosmos / EVM tooling around it.

---

## Comparison

| Dimension | Phala / dstack | 0G | [Akash](/decentralized-compute/akash) | Marlin Oyster |
|-----------|----------------|-----|-----------|---------------|
| Trust model | TDX/SEV-SNP/H100 CC + on-chain attestation | TEE attestation across stack | Trust provider | TDX/Nitro+H100 CC |
| Workload | docker-compose | LLM serving + storage | Kubernetes containers | Custom CVM images |
| Attestation | On-chain | On-chain | None native | On-chain |
| GPU CC | Yes | Yes (via Phala) | Provider-dependent | Yes |
| Persistent storage | Limited | First-class (0G Storage) | Provider option | Limited |
| Maturity | Production | Growing | High | Growing |

---

## Use cases

### Confidential LLM endpoint

```
Model owner ─► dstack manifest ─► Phala Cloud
                                  ─► TDX + H100 CC instance
                                  ─► attested TLS endpoint
                                  ─► users verify, send prompts
```

Replaces "trust OpenAI's privacy policy" with "verify the silicon".

### Confidential RAG over private corpus

A customer's private document corpus is stored encrypted (or held in a TEE-readable form). Phala dstack runs the retrieval and the LLM. The provider sees neither corpus nor queries.

### Cross-chain attestation

A smart contract on Ethereum needs to know that the off-chain compute for a prediction market ran in a real TEE on the published code. Phala posts the attestation to Ethereum via a bridge; the contract verifies. The pattern is used in oracle-style flows where DLCs would be unwieldy.

### Decentralized AI workflows on 0G

Train a model on 0G Compute, store weights in 0G Storage, publish attestation, serve inference on Phala. All verifiable, all on-chain anchored.

---

## Trade-offs

### Strengths (both)

- TEE attestation as a first-class primitive. No other large decentralized compute network does this as well.
- GPU CC support. H100 confidential mode is integrated.
- On-chain verifiability. Any client can audit.
- Developer ergonomics improving. dstack is the cleanest TEE-aware docker-compose available.

### Limitations

- TEE trust assumption. You trust Intel, AMD, or NVIDIA. (This is true for any TEE-based system.)
- Smaller provider pool than Akash; less geographic diversity.
- Chain dependency. Both Phala and 0G run their own chains; chain liveness matters for attestation availability.
- 0G is newer, with less production track record than Phala.
- Token economics introduce attack surface separate from the technical design.

---

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| TEE side-channel on provider | Multi-vendor diversity; TCB updates; layer with FHE for highest stakes |
| Compromised attestation chain | Multi-party signing of attestation aggregations |
| Image-supply-chain | Pin image hashes; reproducible builds; Sigstore-like transparency |
| Provider downtime | Multi-provider redundancy via dstack manifests |
| Smart-contract bugs in attestation verifier | Audited verifier circuits / contracts |
| Token-economic attacks | Slashing, stake-bounded influence |

---

## Operational patterns

### Phala dstack quick start

```
git clone dstack-app-template
edit docker-compose.yml + manifest.yml
phala deploy --network mainnet
# returns attestation handle + endpoint
verify attestation client-side, then connect via attested TLS
```

### Multi-provider failover

dstack manifests can list multiple providers; if one drops, another picks up. Re-attestation happens automatically on failover.

### Combine with Akash

Some users deploy dstack workloads on Akash providers. Akash for the marketplace, dstack for the TEE attestation. A hybrid stack.

---

## Recent developments (2024-2026)

- dstack as the SDK pattern.
- NVIDIA H100 CC mainstream on Phala.
- 0G mainnet rollouts of compute, storage, and DA.
- Cross-chain attestation matured for Ethereum integrations.
- Open-source LLM hosting is now the dominant Phala workload.

---

## Related files

- [Overview - Decentralized Compute](/decentralized-compute)
- [Akash](/decentralized-compute/akash)
- [Bittensor](/decentralized-compute/bittensor)
- [Confidential-AI-Inference](/confidential-computing/confidential-ai-inference)
- [Overview - Confidential Computing](/confidential-computing)
- [NVIDIA-GPU-TEE](/confidential-computing/nvidia-gpu-tee)
- [Attestation-Architecture](/confidential-computing/attestation-architecture)
- [MOC - Composing Primitives](/meta/moc-composing-primitives)

---

## Primary sources

- Phala Network — [phala.network](https://phala.network).
- Phala Cloud — [docs.phala.network/phala-cloud](https://docs.phala.network/phala-cloud).
- dstack — [github.com/Phala-Network/dstack](https://github.com/Phala-Network/dstack).
- Phala source — [github.com/Phala-Network](https://github.com/Phala-Network).
- 0G Network — [0g.ai](https://0g.ai).
- 0G docs — [docs.0g.ai](https://docs.0g.ai).

