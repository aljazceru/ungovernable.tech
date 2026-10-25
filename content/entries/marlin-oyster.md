---
title: "Marlin Oyster"
slug: marlin-oyster
type: deep-dive
pillars: ["compute", "confidential"]
readiness: usable
description: "Marlin Oyster, a decentralized confidential computing network offering TEE-backed virtual machines and serverless functions: design and trust model."
dek: "A decentralized confidential computing protocol. Oyster provides TEE-backed Confidential Virtual Machines (CVMs) and a serverless option as an alternative to centralized cloud, with Verida and others using it to run private AI over sensitive user data without exposing it to the operator."
updated: 2026-10-25
created: 2026-06-08
origin: vault
source: "04-Decentralized-Compute/Marlin Oyster.md"
aliases: ["Oyster", "Marlin Labs", "Confidential VMs"]
tags: ["marlin", "oyster", "cvm", "tee", "confidential-compute", "depin", "deep-dive"]
---

## Position

Marlin Oyster is the confidential computing layer of the Marlin Protocol — a decentralized marketplace for Trusted Execution Environments (TEEs). Where standard decentralized compute (Akash, Golem, Fluence) runs workloads on nodes that can read the data, Oyster's CVMs ensure the operator cannot access the data or the computation.

The canonical use case emerging in 2025-2026 is **private AI inference**: an AI agent needs to process sensitive user data (emails, health records, financial data), and using centralized cloud means that data touches a third-party operator's infrastructure. Oyster provides verifiable TEEs where data is decrypted only inside the hardware-isolated enclave, processed, and returned encrypted.

Marlin positions between:

- **Phala** (TEE-native on-chain compute, Polkadot/ETH ecosystem).
- **Fluence** (WASM/serverless, Arbitrum L2).
- **Azure/GCP confidential VMs** (centralized, enterprise-billing).

Oyster's differentiation is the combination of a decentralized P2P network with TEE hardware attestation and a focus on the developer experience for deploying real applications (LLM inference, AI agents, privacy-preserving compute).

## Architecture

### Confidential Virtual Machines (CVMs)

Oyster CVMs are hardware-isolated virtual machines running on provider nodes. The isolation is provided by:

- **Intel TDX** (Trust Domain Extensions) — VM-level isolation.
- **AMD SEV-SNP** (Secure Nested Paging) — memory encryption and integrity.

The CVM's memory and computation are encrypted and inaccessible to the host operator, the hypervisor, and any other software on the machine. Remote attestation allows a client to cryptographically verify the CVM's state before trusting it with data.

A CVM lifecycle:

1. **Deployment**: a developer specifies a CVM image (EIF = Enclave Image File) and deploys it to a participating provider.
2. **Attestation**: the provider's TEE generates an attestation quote — a signed statement of the CVM's identity, code hash, and hardware state.
3. **Execution**: data is sent to the CVM; it's decrypted inside the enclave by the CVM's own keys (never exposed to the host), processed, and returned.
4. **Verification**: the client verifies the attestation quote against the hardware manufacturer's root keys before trusting the CVM.

### Serverless option

Oyster also offers a serverless deployment model (Oyster Serverless), which is a lighter-weight option than full CVMs. This targets functions and lightweight services where the full VM isolation model is overkill.

### Key Management Service (KMS)

A critical challenge for CVMs: cryptographic keys reset on every system restart (by design — the TEE clears state on reboot). Oyster provides a KMS that allows persistent application secrets across CVM restarts, using a key derivation scheme tied to the CVM's identity.

This enables patterns like:
- API keys that survive restarts.
- Database credentials that persist across provider migrations.
- User-specific secrets that only the specific CVM instance can access.

### Oyster protocol

The broader Oyster protocol handles:

- **Provider discovery**: finding TEE-enabled nodes in the network.
- **Market and pricing**: Oyster CVM documentation defines USDC as the payment token and POND as the staking token.
- **Attestation verification**: on-chain or off-chain verification of provider quotes.
- **Deployment lifecycle**: image management, scaling, health checking.

## Verida partnership — private AI

The most concrete production use of Oyster is the **Verida partnership**, announced in 2026. Verida is a decentralized identity and data infrastructure layer. Their architecture:

- **User data** is stored in Verida's decentralized storage (encrypted).
- **AI processing** happens inside Marlin Oyster CVMs.
- **Confidential compute**: data is pulled from Verida storage, decrypted inside the TEE, processed (e.g., fine-tuning, RAG, inference), and results returned — all without the Marlin operator or any other party seeing plaintext.

The Verida litepaper frames it as "Self-Sovereign Confidential Compute to Secure Private AI":

| Layer | Centralized AI | Verida + Oyster |
|-------|---------------|-----------------|
| Data | Exposed to cloud operator | Encrypted, user-controlled |
| Compute | Cloud-controlled key | TEE-protected key |
| Model | Operator's model | Open weights (optional) |
| Inference | Prompt exposed | Decrypted only inside TEE |
| RAG | Data exposed to server | Confidential retrieval |

This is architecturally similar to Apple Private Cloud Compute (PPC) — the hybrid local + secure cloud approach — but with the addition of decentralization and verifiable TEEs.

## Technical stack

### Hardware support

Oyster CVMs currently support:
- **Intel TDX** — TD-measured VMs with hardware isolation.
- **AMD SEV-SNP** — memory encryption and integrity.

Both are production-grade TEE technologies supported by major cloud providers (Azure, Google Cloud) and increasingly by DePIN compute networks.

### SDK and tooling

- **Rust SDK**: primary language for building Oyster services.
- **Go SDK**: for Go developers.
- **Python SDK**: for AI/ML workflows.
- **CLI tooling**: `oyster` CLI for deployment and management.

### Guides and templates

Oyster documentation includes production guides for:
- Deploy a Node.js server.
- Deploy Llama 3.2 for confidential AI inference.
- Deploy a Twitter Agent Service (AI agent that reads/writes Twitter via API, with API keys protected inside the TEE).
- Privacy-preserving addition (simple MPC-style computation without revealing inputs).

### EIF (Enclave Image File)

The CVM image format is EIF — a signed, reproducible build artifact. The same guarantees as reproducible Docker images apply: you can verify that a specific EIF was derived from specific source code via reproducible builds.

## Payment and staking tokens

Oyster CVM uses **USDC** for payments. Its token definition identifies **POND** on Arbitrum One or through Symbiotic vaults on Ethereum as the staking token. Payment and staking are separate roles.

## Comparison

|| Dimension | Marlin Oyster | Phala | Fluence | Akash |
||-----------|--------------|-------|---------|-------|
| Model | CVM + serverless | TEE VMs | WASM serverless | K8s containers |
| Confidential | Yes (TEE) | Yes (TEE) | TEE roadmap | No |
| Hardware | Intel TDX, AMD SEV-SNP | TDX, H100 CC | CPU first | GPU (H100) |
| AI inference | Llama guide, agent | Production | Roadmap | Via containers |
| Verida integration | Live 2026 | No | No | No |
| Token | USDC (payments); POND (staking) | PHA | FLT | AKT |
| Chain | P2P (own network) | Substrate/ETH L2 | Arbitrum Orbit | Cosmos |

## Trade-offs

### Strengths

- **Hardware-level confidentiality**: Intel TDX / AMD SEV-SNP means the provider operator literally cannot read data inside the CVM.
- **Production TEE tooling**: Llama deployment guide, Twitter agent guide, KMS — real developer paths, not just a spec.
- **Verida partnership**: concrete private AI use case with real deployment.
- **Reproducible builds**: EIF format enables attestation of the exact code running.
- **Decentralized**: no single cloud provider, no hyperscaler lock-in.
- **Serverless option**: lighter-weight than full CVMs for simpler workloads.

### Limitations

- **GPU TEE**: not as far along as Phala for H100 confidential GPU compute. Current focus is CPU TEE (TDX/SEV-SNP).
- **Ecosystem size**: smaller than Phala's on-chain TEE story; less validator diversity.
- **Network maturity**: less battle-tested than centralized TEE options (Azure Confidential Computing, Google Cloud Confidential VMs).
- **AI story**: has Llama guide but not production-proven at Phala's scale.

## Attack surface

|| Attack | Mitigation |
||--------|-----------|
| Provider key compromise | TEE protects keys; keys never in host memory |
| Attestation forgery | Hardware-rooted quotes; verify against manufacturer keys |
| CVM image tampering | EIF reproducible builds; attestation verifies code hash |
| Provider lie about hardware | Challenge-response attestation; on-chain verification |
| Data in transit | TLS to CVM; PCIe encryption (for GPU scenarios) |
| Replay attacks | Nonce-based session establishment inside TEE |
| Side-channel (cache timing) | TDX cache partitioning; mitigation in spec |

## Primary sources

- [Oyster CVM actors and operator staking](https://docs.marlin.org/oyster/protocol/cvm/actors)

- [Oyster CVM definitions: payment token and staking token](https://docs.marlin.org/oyster/protocol/cvm/definitions)

- Oyster docs — [docs.marlin.org/oyster](https://docs.marlin.org/oyster)
- Marlin Oyster GitHub — [github.com/marlin-project/oyster](https://github.com/marlin-project/oyster)
- Verida case study — [blog.marlin.org/veridas-use-of-marlin-to-compute-on-personal-data-securely-in-tees](https://blog.marlin.org/veridas-use-of-marlin-to-compute-on-personal-data-securely-in-tees)
- Verida + Oyster partnership — [news.verida.network/verida-and-marlin-a-partnership-to-power-private-ai](https://news.verida.network/verida-and-marlin-a-partnership-to-power-private-ai-3a25c68072fb)
- Oyster Key Management Service — [x.com/MarlinProtocol/status/1906000030403531072](https://x.com/MarlinProtocol/status/1906000030403531072)
- CVM quickstart — [docs.marlin.org/oyster/build-cvm/quickstart](https://docs.marlin.org/oyster/build-cvm/quickstart)
- Llama 3.2 deployment guide — [docs.marlin.org/oyster/build-cvm/guides/llama3_2](https://docs.marlin.org/oyster/build-cvm/guides/llama3_2)
- Twitter Agent Service guide — [docs.marlin.org/oyster/build-cvm/guides/twitter-agent-service](https://docs.marlin.org/oyster/build-cvm/guides/twitter-agent-service)
