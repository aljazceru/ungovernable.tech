---
title: "Akash"
tags:
  - "akash"
  - "depin"
  - "decentralized-compute"
  - "kubernetes"
  - "deep-dive"
---
*The most-deployed open-source decentralized cloud. A Cosmos-SDK chain coordinates a reverse-auction marketplace for Kubernetes-style workloads, with growing GPU support and a real production user base.*

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

---

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

---

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

---

## GPU support

Akash added GPU support for AI workloads in 2023-2024. Provider operators can advertise:

- GPU model (RTX 4090, A100, H100, H200, B200, etc.).
- VRAM size.
- Custom labels for filtering.

Tenants specify the required GPU type in SDL. The reverse auction picks providers offering it. By 2025-2026 the Akash GPU marketplace had thousands of GPUs across consumer and datacenter classes; the long tail of consumer GPUs makes Akash a low-cost option for inference workloads that don't need the latest H200 or B200 hardware.

---

## AKT and economics

- AKT token for payment, staking, and governance.
- A small **take rate** is charged on every lease, going to staking rewards and the DAO treasury.
- Provider rewards based on staked AKT and uptime.
- Provider services. Providers can also offer specialized features (TEE, IPFS, persistent storage) at premium pricing.

Akash's economic story is closer to "marketplace with a token" than to pure DePIN tokenomics. AKT exists primarily to coordinate, not to be speculatively staked for unrelated workloads.

---

## Recent developments (2024-2026)

- GPU marketplace matured; thousands of GPUs across classes.
- Provider-side improvements in scheduling, resource isolation, and observability.
- Persistent storage as a first-class resource.
- Akash Console UX is friendlier than the original CLI-only flow.
- Network-funded grants for specific use cases (AI inference, model serving, dev tools).

---

## Comparison

| Dimension | Akash | Phala / Marlin | io.net | Render |
|-----------|-------|----------------|--------|--------|
| Workload | Kubernetes containers | TEE-attested CVMs | GPU pools for AI | Specific (rendering / ML) |
| Trust model | Trust provider operator | TEE attestation | TEE + GPU CC roadmap | Trust render service |
| Token | AKT | PHA / POND | IO | RNDR |
| Maturity | High | Growing | High | High |
| Confidential by default | No | Yes | No | No |

---

## Use cases

### Cheap inference

Run open-weights LLMs (Llama 3, Mistral, etc.) on Akash provider GPUs. Cost is roughly 30-60% of AWS for comparable hardware. No KYC. Pay in AKT (or via fiat-on-ramps that abstract this).

### Web2 service hosting on a censorship-resistant fabric

A Nostr relay, a website, a Bitcoin node — anything you'd put on a small VPS — runs on Akash with similar uptime. A provider can refuse, but the marketplace lets you redeploy elsewhere.

### Distributed CI and batch jobs

Spawn ephemeral workers via SDL for periodic batch jobs (data ETL, ML training nights, scientific compute) without committing to fixed cloud spend.

### TEE-as-a-service composition

Run Phala's dstack or a Marlin Oyster CVM image as your container. Akash provides the box, the TEE provides the integrity layer. The pattern is documented in [MOC - Composing Primitives](/meta/moc-composing-primitives).

---

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

---

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| Provider compromise | Use attested workloads; treat provider as untrusted |
| Sybil providers | Stake-weighted bidding; reputation systems |
| Lease grief | On-chain escrow protects both parties |
| Network-level attacks on tenant traffic | TLS / mixnet on top |
| AKT price volatility | Hedge or pay via stablecoin-priced wrappers |
| Censorship of specific deployments | Re-deploy with different SDL hash |

---

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

---

## Related files

- [Overview - Decentralized Compute](/decentralized-compute)
- [Phala and 0G](/decentralized-compute/phala-and-0g)
- [Confidential-AI-Inference](/confidential-computing/confidential-ai-inference)
- [Overview - Confidential Computing](/confidential-computing)

---

## Primary sources

- Akash Network — [akash.network](https://akash.network).
- Documentation — [docs.akash.network](https://docs.akash.network).
- Source — [github.com/akash-network](https://github.com/akash-network).
- SDL reference — [docs.akash.network/readme/stack-definition-language](https://docs.akash.network/readme/stack-definition-language).
- Cosmos SDK — [docs.cosmos.network](https://docs.cosmos.network).

