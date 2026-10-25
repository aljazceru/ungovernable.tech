---
title: "Compare decentralized compute platforms"
slug: compare-decentralized-compute
type: comparison
pillars: ["compute", "confidential"]
readiness: usable
description: "Compare compute platforms by customer access, provider admission, payments, workloads and attestation, separating documented controls from unverified claims."
dek: "A marketplace, a job scheduler and a confidential execution service have different admission and trust boundaries."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: ["decentralized-compute", "akash", "bacalhau", "aethir", "bittensor", "fluence", "marlin-oyster", "phala-and-0g"]
---

## Summary

“Decentralized compute” covers services with different customer paths and provider roles. Compare the particular route you will use, not a project's token alone. This table distinguishes confirmed documentation from gaps; an unspecified identity-check requirement is not evidence that no checks exist.

## Access, admission and payments

| Platform and route | Customer onboarding | Provider admission documented in the cited sources | Payment or incentives |
|---|---|---|---|
| [Akash](/kb/akash/), Console Air | Connect a wallet and sign transactions yourself; the interface is self-hostable. | Provider build guide specifies a Kubernetes cluster and operational prerequisites. This does not establish every listing or audit requirement. | Console Air documents an AKT/ACT wallet workflow. Check the current deployment denomination rather than treating the two assets as interchangeable. |
| [Bacalhau](/kb/bacalhau/), an operated cluster | Connect the CLI to the selected deployment. | Administrators can approve a pending compute node to join a cluster and receive work. | No marketplace payment token is established by these orchestration documents. |
| [Aethir](/kb/aethir/), Cloud portal | Bind a wallet; the customer wallet guide requires KYC before claiming or withdrawing ATH. | Hosts connect a wallet before onboarding GPUs; KYC is required before claiming or withdrawing earnings. | The documented portal balance and claims use ATH. |
| [Bittensor](/kb/bittensor/), subnet participation | Use the network SDK/CLI and a wallet; inspect the chosen subnet's separate interface. | Miners produce a subnet's commodity and validators score contributions. Exact participation requirements need the chosen subnet's documentation. | The network documentation describes TAO incentives; it does not establish a universal customer tariff. |
| [Fluence](/kb/fluence/), Console and Provider Application | Console documentation lists email, Google or GitHub sign-in; it still includes an alpha-program eligibility note. | Provider documentation requires team approval, KYB and Tier 3 or Tier 4 data centers. | Console uses a prepaid USD balance funded by card or crypto. Protocol documentation separately describes USDC provider revenue and FLT capacity incentives. |
| [Marlin Oyster](/kb/marlin-oyster/), CVM CLI | Deploy from a wallet using a Docker Compose file. | The canonical repository includes an AWS-account setup path and operator control-plane software. | The documented Arbitrum deployment path needs USDC and ETH for gas. |
| [Phala Cloud](/kb/phala-and-0g/) | Use a Cloud workspace and its balance. | This is the documented hosted Cloud path; a general independent-provider admission rule is not established here. | The FAQ documents balance top-ups and card auto-top-up. It does not require treating PHA as the customer billing unit. |
| [0G Compute](/kb/phala-and-0g/) | Router with an API key, or Direct SDK with wallet-signed requests. | The inference-provider guide requires a compatible model service, supported TEE hardware and a provider broker. | Router deposits use 0G tokens; the provider guide also requires 0G tokens for gas. |

## Workloads and confidentiality

| Platform | Workload established by its documentation | Confidentiality evidence |
|---|---|---|
| Akash | Container deployments. | The cited wallet/provider guides do not establish host-confidential execution. |
| Bacalhau | Docker and WebAssembly jobs placed near data. | Cluster membership controls do not establish protection from the compute-node operator. |
| Aethir | GPU capacity in the Cloud host/customer workflow. | The cited portal and payment guides do not establish enclave isolation. |
| Bittensor | Subnet-defined digital commodities, including compute, storage and prediction. | Contribution scoring is not itself evidence of host-confidential execution. |
| Fluence | CPU and GPU instances, including virtual machines. | The cited instance and admission documentation does not establish a TEE guarantee. |
| Marlin Oyster | Docker Compose workloads and enclave tooling. | The repository includes attestation generation and verification components; deployment must bind a workload to the expected attestation. |
| Phala Cloud | Container applications inside confidential VMs. | Its FAQ documents Intel TDX isolation and an attestation workflow. |
| 0G Compute | Model inference and fine-tuning. | The provider guide documents CPU/GPU attestation and signed results. Router-side verification has its own trust boundary. |

## Trust model / threat model

A notable distinction is explicit in 0G's verification documentation: requesting `verify_tee` asks the Router to verify the provider signature. The returned boolean is the Router's assertion; it is not the raw proof. The same document describes independent verification for callers who do not want to rely on that assertion.

For any TEE route, decide which measurement, signer and security baseline you accept before releasing secrets. See [remote attestation](/kb/remote-attestation/) and [TEE state and revocation](/kb/tee-state-and-revocation/). For other routes, do not infer host secrecy from decentralization, payments or performance scoring.

## Readiness

**Usable with route-specific qualifications.** These are documented software and service paths, not equivalent products. Some cited guides retain eligibility or rollout qualifications. Verify the exact customer and provider path before committing a workload.

## Limits

No blanket “no KYC,” permissionless-provider or confidential-by-default claim is made. Prices, capacity, performance rankings and token investment claims are omitted. Use [decentralized compute](/kb/decentralized-compute/) as the broader map, then verify the selected deployment's contract, billing and recovery conditions.

## Primary sources

- [Akash Console Air wallet and deployment interface](https://github.com/akash-network/console-air)
- [Akash self-custody, certificates and endpoints](https://github.com/akash-network/console-air/blob/main/docs/self-custody.md)
- [Akash provider prerequisites](https://github.com/akash-network/docs/blob/master/providers/build-a-cloud-provider/akash-cloud-provider-build-with-helm-charts/step-1-prerequisites-of-an-akash-provider.md)
- [Bacalhau architecture and supported workloads](https://docs.bacalhau.org/)
- [Bacalhau node approval](https://docs.bacalhau.org/cli/node/approve)
- [Aethir customer wallet and KYC](https://docs.aethir.com/aethir-cloud/aethir-cloud-customer/cloud-customer-portal-guide/manage-wallet)
- [Aethir host wallet, onboarding and KYC](https://docs.aethir.com/aethir-cloud/aethir-cloud-host/cloud-host-portal-guide/manage-your-wallet)
- [Bittensor roles, subnets and TAO](https://docs.learnbittensor.org/)
- [Fluence Console registration and eligibility note](https://fluence.dev/docs/build/registration.md)
- [Fluence Console payment balance](https://fluence.dev/docs/build/balance.md)
- [Fluence provider approval and KYB](https://fluence.dev/docs/connect_servers/login.md)
- [Fluence protocol payments and capacity incentives](https://fluence.dev/docs/stake/overview)
- [Fluence CPU instances](https://fluence.dev/docs/build/cpu_cloud/overview.md)
- [Marlin Oyster CVM deployment and funding](https://docs.marlin.org/oyster/build-cvm/quickstart)
- [Oyster operator and attestation implementations](https://github.com/marlinprotocol/oyster-monorepo)
- [Phala Cloud FAQ: TDX, workloads and billing](https://docs.phala.com/phala-cloud/faqs)
- [Phala attestation workflow](https://docs.phala.com/phala-cloud/attestation/overview)
- [0G Compute customer paths and funding](https://docs.0g.ai/developer-hub/building-on-0g/compute-network/overview)
- [0G inference-provider requirements](https://docs.0g.ai/developer-hub/building-on-0g/compute-network/inference-provider.md)
- [0G Router verification and independent verification](https://docs.0g.ai/developer-hub/building-on-0g/compute-network/router/features/verifiable-execution.md)
