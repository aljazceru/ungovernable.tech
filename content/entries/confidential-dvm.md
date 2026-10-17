---
title: "Confidential Data Vending Machines"
slug: confidential-dvm
type: research-note
pillars: [confidential, identity, compute]
readiness: research
description: "An open research note on running Nostr Data Vending Machine jobs inside confidential containers, so a provider can process private data it can never see."
dek: "Can you rent a model and a GPU for one job, hand it private data, and be sure the provider never sees either the data or the result?"
updated: 2026-10-17
created: 2024-06-27
origin: original
related: [confidential-containers, remote-attestation, confidential-ai-inference, private-llm-inference-patterns, nostr-protocol]
---

*This is a working research note from the ungovernable.tech project, not a finished design.*

Data Vending Machines (DVMs) are a Nostr pattern (NIP-90) in which a user publishes a job request, such as "transcribe this audio" or "summarise these documents", and service providers compete to do it for a Lightning payment. Today the provider sees everything: the input, the output and often the identity of the requester.

Processing confidential data currently means one of two things: give up the privacy, or run everything locally. Local processing is viable for many tasks on consumer hardware, but not when the job is occasional and needs hardware you do not own, or when you want to use a model you cannot buy outright. Confidential computing offers a third way: both parties place their part (model and data) into an encrypted, attested virtual machine, and only the owner of the data receives the result.

## Use cases

- Providing sensitive documents as retrieval context to a language model.
- Analysing confidential datasets without handing them to the analyst.

## Sketch of the flow

1. **Deploy a fresh confidential container for each job** (for example with [Confidential Containers](/kb/confidential-containers/) on AMD SEV-SNP or Intel TDX).
2. **Establish a secure channel with the user.** The container generates a one-time Nostr key pair inside the enclave and contacts the user. On its own this is not enough: the user must be able to verify that the key was generated inside the attested environment, so the attestation report must bind the public key ([Remote Attestation Architecture](/kb/remote-attestation/)).
3. **Gather the data.** Either the user sends inputs over encrypted direct messages to the enclave key, or the DVM job flow is extended to hand the user the attested channel.
4. **Execute the job.**
5. **Deliver the result** over the secure channel.
6. **Destroy the VM** and its keys.

## Open problems

- Attestation in confidential containers was immature when this note was started; an attestation service running in a trusted environment is needed to release secrets only to verified workloads (the CoCo *Trustee* key broker addresses this).
- GPU confidential computing requires specific hardware combinations (for example NVIDIA Hopper-class GPUs with a CPU TEE), and cloud support for confidential GPU nodes has been uneven ([NVIDIA GPU TEEs](/kb/nvidia-gpu-tee/)).
- Pushing an entire VM per job is heavy; per-job confidential containers are lighter but have a larger trusted computing base.
- The provider still learns metadata: that a job happened, its size and timing, and the payment.

A first proof of concept ("something works") lives in the repository's [`simple-test/`](https://github.com/aljazceru/ungovernable.tech/tree/main/simple-test) directory.

## Related reading

- [Confidential AI Inference](/kb/confidential-ai-inference/) and [Private LLM Inference Patterns](/kb/private-llm-inference-patterns/)
- NIP-90, *Data Vending Machines*: <https://github.com/nostr-protocol/nips/blob/master/90.md>
- Data Vending Machines: <https://www.data-vending-machines.org/>
- Confidential Containers: <https://github.com/confidential-containers/>
