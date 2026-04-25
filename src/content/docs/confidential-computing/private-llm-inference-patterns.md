---
title: "Private LLM Inference Patterns"
tags:
  - "confidential-inference"
  - "llm"
  - "patterns"
  - "attestation"
  - "privacy"
  - "tee"
---
*Recipes, not frameworks. The patterns below combine TEEs, attestation, KMS, and transparency logs into concrete deployable services with explicit threat models.*

See [Confidential-AI-Inference](/confidential-computing/confidential-ai-inference) for context and [Attestation-Architecture](/confidential-computing/attestation-architecture) for the primitives these patterns assume.

---

## Pattern 1: Attested-TLS inference endpoint

Goal: a user sends a prompt to a remote LLM, and neither the cloud operator nor any network middlebox can read it.

Pieces:
- Confidential VM (TDX or SEV-SNP) plus an H100 CC GPU.
- Inside the CVM: a TLS terminator whose private key is generated inside the enclave; the public key hash goes in the attestation `REPORT_DATA`.
- A client library that (a) fetches the quote, (b) verifies it against pinned vendor roots plus a minimum TCB plus an allowlisted measurement, and (c) pins the TLS key for the session.

Flow:

1. Client sends `GET /attestation?nonce=N` and gets back a CPU quote, a GPU quote, and a TLS pubkey.
2. Client verifies both quotes; aborts on any failure (do not render UI first, do not "just warn").
3. Client opens TLS, pins the enclave-generated cert, and sends the prompt.
4. The enclave decrypts the prompt, runs inference on the attested GPU, and streams tokens back over the same TLS.
5. No prompt, KV cache, or output is written to any non-enclave storage.

Threat model: trusts Intel, AMD, and NVIDIA silicon, the build of the enclave image, and the transparency log (if one is used). Untrusts cloud operator, hypervisor, host OS, network.

Used by: Tinfoil, Marlin, most Phala deployments.

---

## Pattern 2: KMS-gated weight release

Goal: a model provider uploads weights to a cloud, and weights must never be decrypted outside an attested enclave of a known version.

Pieces:
- Object store (S3/GCS/Blob) holds weights encrypted with a data-encryption key (DEK).
- The DEK is wrapped by a key in a KMS that supports attestation conditions (Azure Key Vault SKR, AWS KMS with Nitro conditions, GCP Confidential Space, HashiCorp Vault + SGX).
- KMS policy: release the DEK only if the quote measurement is in the allowlist AND TCB ≥ min AND GPU CC-On.

Flow on cold start:

1. The enclave boots, self-measures, and generates an ephemeral keypair.
2. The enclave calls the KMS with its quote (binding its pubkey in `REPORT_DATA`).
3. The KMS verifies, encrypts the DEK to the enclave pubkey, and returns it.
4. The enclave decrypts the DEK in memory, streams encrypted weights from object store, decrypts them into HBM, and runs.

Rotation: issue a new image, get a new measurement, extend the KMS allowlist, roll the deployment, then remove the old measurement from the allowlist. Old enclaves automatically lose key access.

Threat model: as Pattern 1, plus trust in the KMS operator's enforcement of attestation conditions. To reduce KMS trust, use a multi-KMS Shamir split across different clouds.

---

## Pattern 3: Transparency-logged builds

Goal: anyone can independently verify what code is running.

Pieces:
- Reproducible container or image build (Nix, Bazel, SLSA L3+).
- On every release, publish `{image_hash, source_commit, SBOM, signature}` to a transparency log (Sigstore Rekor or a custom Merkle log).
- Verifier (either the client's library or a separate service) refuses quotes whose measurement is not in the log with a sufficiently old inclusion proof, which prevents same-block substitution attacks.

Why it matters: without this, an attestation quote only proves "trust the image-builder's private signing key." With it, the builder cannot silently ship a backdoored image to a single targeted user without being publicly detectable.

Used by: Apple PCC, Tinfoil, some Confidential Container deployments.

Pitfall: reproducibility is hard. Most "works for me" containers do not rebuild bit-identically on a different machine. Budget real engineering time. This pattern is what separates "cryptographically private" from "cryptographically theatrical."

---

## Pattern 4: No-persistence enclaves

Goal: even if an operator is compelled by a court order, there is nothing logged to hand over.

Design rules:
- Rootfs mounted as `tmpfs` or read-only overlay; no writable persistent disk attached to the TEE.
- Stdout and stderr routed to `/dev/null` inside the enclave. No sidecar log shipper.
- KV cache, scratch, and swap all live in memory or in encrypted ephemeral storage.
- Any metrics emitted are pre-aggregated counters or histograms with no user content, and rate-limited to prevent covert channels.
- Telemetry is opt-in explicit; default off.
- On shutdown or reboot, memory is wiped by hardware (TDX and SEV-SNP do this; verify).

Why structural beats policy: a config flag that "disables logging" can be flipped by a compromised operator with a new deployment. Compiling out the logging code entirely, and attesting the resulting image, cannot be undone without changing the measurement and invalidating every client's trust.

---

## Pattern 5: Client-side verification

Goal: the person typing the prompt, not just an enterprise middleware layer, verifies the attestation.

Challenge: browsers and mobile apps do not ship Intel/AMD/NVIDIA root stores; verification is fiddly.

Options:
- WASM verifier in the browser (used by Tinfoil): a ~2MB WASM blob containing collateral and verification logic. Served from a separate origin (ideally pinned via Subresource Integrity), or loaded from a domain different from the inference provider so a compromised provider cannot swap the verifier.
- Mobile SDK with pinned roots and background collateral refresh.
- Browser extension (EFF-style) for users who want cryptographic verification they control. Useful for high-risk users; not scalable to the general public.
- Remote verifier service the client trusts. Weakest option: the client now trusts another party, but at least not the same party running the model.

The UX trap to avoid: a green padlock labeled "Confidential" that does not actually verify anything. If verification cannot fail loudly, it is not verification.

---

## Pattern 6: Split / confidential RAG

Goal: run retrieval-augmented generation where the documents, the query, and the retrieval index are all confidential.

Components:
- Vector DB inside a CVM (TDX); index encrypted in HBM or on disk with a key released only to attested index enclaves.
- Retrieval and generation in the same enclave (or a federated pair over attested channels).
- Ingestion pipeline also attested. Otherwise the threat model is "operator saw every document at ingest."

Harder problems:
- Oblivious retrieval: without it, access patterns (which vectors were hit) leak even inside the TEE because the memory controller sees them. Combine with ORAM or PIR for high assurance; costs can be 10-100x. For most threat models, in-TEE is good enough.
- Index freshness: re-attesting on each ingest is heavy. Use an attested ingest service plus signed index chunks.

---

## Pattern 7: Confidential fine-tuning

Goal: a customer uploads private training data, the provider's base model weights are also private, and the resulting fine-tuned delta is usable only under further attestation.

Shape:
- Base weights encrypted, released to the training enclave via Pattern 2.
- Training data encrypted to the training enclave's pubkey.
- Output: LoRA or full delta, re-encrypted to a customer-controlled key or to a downstream inference enclave's attestation policy.
- Optional: zero-knowledge proof that training was the published code over the claimed hyperparameters (heavy, research-only today).

Gotcha: training is PCIe-heavy; CC overhead is higher than for inference. Budget 15-25% on H100. Blackwell is meaningfully better.

---

## Pattern 8: Attested tool use

Problem: a model in a TEE is only confidential until it calls `requests.get(url)`. The tool call exits the enclave.

Mitigations:
- In-enclave tools only: a code interpreter that runs in a second nested enclave; network egress blocked.
- Attested proxy: all tool HTTP traffic routed through an attested proxy that strips user-identifying headers, logs nothing, and re-TLS-terminates.
- Differential privacy on tool outputs: noise added before returning to the model, so tool-source inference attacks are bounded.
- Policy enclave: a separate enclave that pre-approves (or rewrites) every outbound tool call based on attested policy. The model cannot exfiltrate the prompt via a crafted URL without the policy enclave signing off.

Tool use is where most "private inference" products quietly fail their threat model. Scrutinize it first in any audit.

---

## Anti-patterns (do not ship)

- "Confidential" branding with no client-side attestation. If the client does not verify, the guarantee is a pinky promise.
- A trusted operator holds the KMS key. Then the TEE does not help against the one adversary it was supposed to stop.
- Single-vendor TCB with no revocation plan. You will wake up to a CVE; have the playbook written before the day.
- Attesting the VM but not the GPU. See [NVIDIA-GPU-TEE](/confidential-computing/nvidia-gpu-tee).
- Opaque image builds. If nobody outside the provider can reproduce the measurement, the attestation binds the world to a black box.
- Logging "just prompts, no identity" — prompts are identity.
- Debug or developer attestation in production. SGX, TDX, and SEV-SNP all have debug modes; production policy must reject them.

---

## Related Files

- [Confidential-AI-Inference](/confidential-computing/confidential-ai-inference)
- [Attestation-Architecture](/confidential-computing/attestation-architecture)
- [NVIDIA-GPU-TEE](/confidential-computing/nvidia-gpu-tee)
- [Confidential-Containers](/confidential-computing/confidential-containers)
- [TEE-Side-Channel-Attacks](/confidential-computing/tee-side-channel-attacks)

## Primary Sources

- Apple: *Private Cloud Compute Security Guide*
- Microsoft: *Confidential AI and Inferencing* whitepapers (2024–)
- Knauth et al.: *Integrating Remote Attestation with Transport Layer Security* (RA-TLS, 2018)
- Sigstore / Rekor transparency log — `sigstore.dev`
- NIST SP 800-204D (software supply chain, informs the build side)

