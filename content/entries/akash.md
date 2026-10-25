---
title: "Akash Network"
slug: akash
type: deep-dive
pillars: ["compute"]
readiness: usable
description: "Akash Network, an open-source decentralized cloud: a reverse-auction marketplace for container workloads and GPUs, its trust model and its limits."
dek: "The most-deployed open-source decentralized cloud. A Cosmos-SDK chain coordinates a reverse-auction marketplace for Kubernetes-style workloads, with growing GPU support and a real production user base."
updated: 2026-09-08
created: 2026-04-25
origin: vault
source: "04-Decentralized-Compute/Akash.md"
aliases: ["Akash Network"]
tags: ["akash", "depin", "decentralized-compute", "kubernetes", "deep-dive"]
---

## What Akash is

Akash is a decentralized compute marketplace. Workload deployers (tenants) post **deployments** specifying compute requirements as **SDL** (Stack Definition Language, a Kubernetes-flavored YAML). Provider operators bid; the lowest bidder gets the workload. Settlement happens on-chain in AKT.

Compared to AWS:

- No account; payment via wallet.
- Sanctioned, under-banked, or pseudonymous users can deploy.
- Provider diversity beats hyperscaler concentration.
- Container-only — Kubernetes Pod-equivalent workloads.

Compared to Phala / Marlin:

- No TEE attestation by default; trust the provider operator (or layer TEE on top).
- Mature Kubernetes-style scheduling.
- Larger active provider set.

## Architecture

```
Tenant         Akash chain (Cosmos SDK)        Provider
   │                  │                            │
   ├─ post SDL ──────►│                            │
   │                  ├─ broadcast deployment ────►│
   │                  │                            ├─ submit bid
   │                  │◄────── bids ───────────────┤
   ├─ select bid ────►│                            │
   │                  ├─ create lease ────────────►│
   │                  │                            ├─ run workload
   ├─ direct conn  ─────────────────────────────►  │ (container)
```

Once the lease is created, the tenant talks to the provider directly (port forwarding, ingress, logs); the chain handles only payment and lifecycle events.

## SDL — the workload spec

```yaml
version: "2.0"
services:
  web:
    image: nginx
    expose:
      - port: 80
        as: 80
        to:
          - global: true
profiles:
  compute:
    web:
      resources:
        cpu:
          units: 0.5
        memory:
          size: 512Mi
        storage:
          size: 1Gi
  placement:
    westcoast:
      pricing:
        web:
          denom: uakt
          amount: 1000
deployment:
  web:
    westcoast:
      profile: web
      count: 1
```

A Helm-chart-shaped YAML that Akash providers can run. Most existing Docker / Kubernetes apps port over with minimal changes.

## GPU support

Akash added GPU support for AI workloads in 2023-2024. Provider operators can advertise:

- GPU model (RTX 4090, A100, H100, H200, B200, etc.).
- VRAM size.
- Custom labels for filtering.

Tenants specify the required GPU type in SDL. The reverse auction picks providers offering it. By 2025-2026 the Akash GPU marketplace had thousands of GPUs across consumer and datacenter classes; the long tail of consumer GPUs makes Akash a low-cost option for inference workloads that don't need the latest H200 or B200 hardware.

## AKT and economics

- AKT token for payment, staking, and governance.
- A small **take rate** is charged on every lease, going to staking rewards and the DAO treasury.
- Provider rewards based on staked AKT and uptime.
- Provider services. Providers can also offer specialized features (TEE, IPFS, persistent storage) at premium pricing.

Akash's economic story is closer to "marketplace with a token" than to pure DePIN tokenomics. AKT exists primarily to coordinate, not to be speculatively staked for unrelated workloads.

## Recent developments (2024-2026)

### BME (Burn-Mint Equilibrium) — Live March 23, 2026

The most significant tokenomics change in any major DePIN compute network. AEP-76 (BME) activated on Mainnet 17 following Proposal 318:

```
User payment → buys AKT on open market → AKT burned → produces ACT (non-transferable stablecoin)
ACT settles transaction with providers
Providers mint ACT back to AKT at market price
```

- Every compute transaction burns AKT, creating deflationary pressure as usage grows.
- Providers receive stable ACT, satisfying enterprise settlement needs.
- Post-launch: Akash crossed **$5M monthly compute spend** in Q1 2026, confirming the tokenomics thesis.
- Testnet: 250+ participants, 10+ test categories, $10,000+ incentives distributed before mainnet launch.

### AkashML — 1.7 Billion Tokens/Day on OpenRouter

AkashML launched November 2025 with an OpenAI-compatible API. As of Q1 2026:

- Processing **1.7 billion tokens/day** via OpenRouter integration.
- OpenAI-compatible API: swap `base_url` to point at AkashML endpoints.
- Dominant player in the AI inference DePIN ecosystem per Q1 2026 report.

### Homenode Early Access — Live May 2026

Purpose-built for consumer/prosumer GPU contribution. Phase 1 supported GPUs:

| GPU | Class |
|---|---|
| RTX 4090 | Consumer, 24GB |
| RTX 5090 | Consumer, 32GB (new) |
| Quadro RTX 6000 Ada | Professional |

- Enables average users to participate as providers — not just data center operators.
- Resilience argument: distributed home nodes eliminate single points of failure.
- Physical infrastructure argument (Greg Osuri, NEARCON SF): conflicts and grid failures in one region are absorbed by nodes elsewhere.
- URL: `homenode.akash.network`

### Akash Agents Platform — One-Click AI Agent Deployment

Built by community member Sandeep Narahari:

- Powered by AkashML inference.
- One-click agent deployments on decentralized compute.
- No infrastructure management overhead.
- Inherits Akash's provider diversity and anti-censorship properties for agentic AI workloads.

### AEP-65: Confidential Computing with TEE — Live May 19, 2026

Akash launched Confidential Computing (announced via X, May 2026):

- Provider operators cannot read tenant workloads inside TEE.
- Attestation reports prove hardware integrity on-chain.
- Composable with [Phala and 0G](/kb/phala-and-0g/) and [Confidential-AI-Inference](/kb/confidential-ai-inference/) stack.
- AEP-29 (Hardware Verification using Trusted Execution) already live for provider attestation.
- AEP-65: enabling providers with TEE hardware to offer confidential workload deployments.
- This eliminates the primary trust gap that separated Akash (trust the provider) from Phala/Marlin (TEE-attested).

### DOOOR — TEE Integration on Akash (Community SDK)

Community project integrating Trusted Execution Environments into Akash Network, enabling secure and verifiable AI execution. See GitHub discussion (akash-network/discussions/872) for the open-source SDK approach.

### 500,000 AKT Burned via BME — On-Chain Evidence (May 26, 2026)

From on-chain data: **500,000 AKT burned** via BME mechanism. This is direct evidence of real compute usage translating to token deflation — the core thesis of Akash's March 2026 tokenomics upgrade. AKT trading range ~$0.85–$0.97 in May 2026, up ~24.85% weekly as top AI/DePIN gainer.

### GPU Marketplace Growth

- Thousands of GPUs across consumer and datacenter classes.
- H200 and B200 nodes added to GPU waitlist.
- AkashML OpenRouter integration making AI inference the dominant workload.

### Akash Network 2025 Year in Review Highlights

- Razer partnership: $0.01/image cost via Akash's peer-to-peer GPU market.
- Venice.ai: end-to-end encrypted AI inference mode on Akash — prompts encrypted on device, stay encrypted in transit.
- Flashback Labs: built privacy-first AI platform letting users create AI twins trained entirely on their own data.
- Sigea Cloud Labs: deployed privacy-first cloud storage on Akash.
- Codex: deployed decentralized Codex Storage Nodes via Akash.
- Morpheus: integrated Akash into Smart Agent Builder compute marketplace.
- Akash Console UX is friendlier than the original CLI-only flow.
- Network-funded grants for specific use cases (AI inference, model serving, dev tools).

### Q4 2026 Roadmap — Four Firm Dates Published (September 2026)

The Akash 2026 roadmap page now lists four Q4 deliverables with concrete completion dates:

| AEP / Initiative | Completion | Status (Sept 2026) |
|---|---|---|
| **AEP-46** Spot Instances | (Draft since Dec 2024) | **Draft** |
| **AEP-67** Console Bid Screening | (Last Call since May 2025) | **Last Call** |
| Custom Domain Configuration via Akash Console | **Nov 15, 2026** | Estimated |
| Managed Services Market (AEP-11) | **Dec 15, 2026** | Estimated |
| Onchain Provider Incentives (AEP-53) | **Dec 31, 2026** | Estimated |
| Akash on Shared Security (AEP-79) | **Dec 31, 2026** | Estimated |

What changed: the team's published schedule moved from quarterly buckets to fixed dates. AEP-46 Spot Instances has been Draft for 23 months; AEP-67 Console Bid Screening has been Last Call for 16 months. The Sep 1 weekly confirmed AEP-46 + AEP-67 were delivered Aug 30/31 — those were the preceding gates to the Q4 deliverables.

**AEP-79 Shared Security** is the security/economics pillar the Cosmos-to-Solana migration debate has been circling. The **late-2026 target** means a chain decision (or a no-migration defense) is structurally required by year-end. AKT traded $0.465–$0.561 across Sept 4–7 (CMC AI Sep 7), with a "$2 target" framing from a bullish analyst offset by persistent sell pressure testing critical support.

See [Decentralized Compute Tuesday — September 08 2026 Weekly Update](/briefings/compute/2026-09-08/) for the full Q4 roadmap table and AKT price context.

## Comparison

| Dimension | Akash | Phala / Marlin | io.net | Render |
|-----------|-------|----------------|--------|--------|
| Workload | Kubernetes containers | TEE-attested CVMs | GPU pools for AI | Specific (rendering / ML) |
| Trust model | Trust provider operator | TEE attestation | TEE + GPU CC roadmap | Trust render service |
| Token | AKT | PHA / POND | IO | RNDR |
| Maturity | High | Growing | High | High |
| Confidential by default | No | Yes | No | No |

## Use cases

### Cheap inference

Run open-weights LLMs (Llama 3, Mistral, etc.) on Akash provider GPUs. Cost is roughly 30-60% of AWS for comparable hardware. No KYC. Pay in AKT (or via fiat-on-ramps that abstract this).

### Web2 service hosting on a censorship-resistant fabric

A Nostr relay, a website, a Bitcoin node — anything you'd put on a small VPS — runs on Akash with similar uptime. A provider can refuse, but the marketplace lets you redeploy elsewhere.

### Distributed CI and batch jobs

Spawn ephemeral workers via SDL for periodic batch jobs (data ETL, ML training nights, scientific compute) without committing to fixed cloud spend.

### TEE-as-a-service composition

Run Phala's dstack or a Marlin Oyster CVM image as your container. Akash provides the box, the TEE provides the integrity layer. The pattern is documented in [MOC - Composing Primitives](/kb/map-composing-primitives/).

## Trade-offs

### Strengths

- Open source, permissionless.
- Real GPU marketplace at scale.
- Kubernetes-flavored UX, low porting cost from existing apps.
- Mature, with years of production operation.
- Lower cost than hyperscalers for many workloads.

### Limitations

- No native TEE attestation. Trust the provider, or combine with attested workload images for integrity.
- Provider quality varies. Some are professional shops; others are home-rigs with unstable links.
- Limited managed services. No managed databases, queues, etc.; bring your own.
- Egress can be expensive depending on provider pricing.
- Token-coupled UX. Fiat onramps exist but are friction.

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Provider compromise | Use attested workloads; treat provider as untrusted |
| Sybil providers | Stake-weighted bidding; reputation systems |
| Lease grief | On-chain escrow protects both parties |
| Network-level attacks on tenant traffic | TLS / mixnet on top |
| AKT price volatility | Hedge or pay via stablecoin-priced wrappers |
| Censorship of specific deployments | Re-deploy with different SDL hash |

## Operational patterns

### Permissionless Nostr relay

```
Akash deployment with strfry container
  ↓
Public WebSocket on Akash provider IP
  ↓
NIP-11 relay metadata
```

If a provider drops you, redeploy elsewhere. Relay state can be replicated across Akash providers via standard Nostr replication.

### Akash plus TEE = confidential compute

```
SDL specifies a TEE-aware image (Phala dstack, Marlin Oyster snapshot)
  ↓
Image boots inside provider's TDX/SEV-SNP machine
  ↓
Workload attests to client; client verifies
```

The Akash chain coordinates payment; the TEE provides the integrity layer; the workload is end-to-end confidential.

## Primary sources

- Akash Network — [akash.network](https://akash.network).
- Documentation — [docs.akash.network](https://docs.akash.network).
- Source — [github.com/akash-network](https://github.com/akash-network).
- SDL reference — [docs.akash.network/readme/stack-definition-language](https://docs.akash.network/readme/stack-definition-language).
- Cosmos SDK — [docs.cosmos.network](https://docs.cosmos.network).

For a deployment walkthrough with an exit plan, see [deploying on decentralized compute](/guides/deploying-on-decentralized-compute/).
