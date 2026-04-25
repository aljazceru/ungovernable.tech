---
title: "Private LLM Inference Patterns"
tags:
  - "confidential-inference"
  - "llm"
  - "patterns"
  - "attestation"
  - "privacy"
  - "tee"
sidebar: {"label":"Private LLM Inference Patterns"}
---
*Recipes — not frameworks. The patterns below compose TEEs, attestation, KMS, and transparency logs into concrete deployable services with clear threat models.*

See [Confidential-AI-Inference](/confidential-computing/confidential-ai-inference) for context and [Attestation-Architecture](/confidential-computing/attestation-architecture) for the primitives these patterns assume.

---

## Pattern 1: Attested-TLS Inference Endpoint

**Goal:** user sends prompt to a remote LLM; neither the cloud operator nor any network middlebox can read it.

**Pieces:**
- Confidential VM (TDX or SEV-SNP) + H100 CC GPU.
- Inside the CVM: TLS terminator whose private key is generated inside the enclave; public key hash placed in the attestation `REPORT_DATA`.
- Client library that (a) fetches the quote, (b) verifies it against pinned vendor roots + minimum TCB + allowlisted measurement, (c) pins the TLS key for the session.

**Flow:**

1. Client → `GET /attestation?nonce=N` → gets CPU quote + GPU quote + TLS pubkey.
2. Client verifies both quotes; aborts on any failure (don't render UI first, don't "just warn").
3. Client opens TLS, pins the enclave-generated cert, sends prompt.
4. Enclave decrypts prompt, runs inference on attested GPU, streams tokens back over the same TLS.
5. No prompt, KV cache, or output is written to any non-enclave storage.

**Threat model:** trusts Intel+AMD+NVIDIA silicon, the build of the enclave image, and the transparency log (if using one). Untrusts cloud operator, hypervisor, host OS, network.

**Used by:** Tinfoil, Marlin, most Phala deployments.

---

## Pattern 2: KMS-Gated Weight Release

**Goal:** model provider uploads weights to a cloud; weights must *never* be decrypted outside an attested enclave of a known version.

**Pieces:**
- Object store (S3/GCS/Blob) holds weights encrypted with a data-encryption key (DEK).
- DEK wrapped by a key in a KMS that supports attestation conditions (Azure Key Vault SKR, AWS KMS with Nitro conditions, GCP Confidential Space, HashiCorp Vault + SGX).
- KMS policy: release DEK only if quote measurement ∈ allowlist AND TCB ≥ min AND GPU CC-On.

**Flow on cold start:**

1. Enclave boots, self-measures, generates ephemeral keypair.
2. Enclave calls KMS with its quote (binding its pubkey in `REPORT_DATA`).
3. KMS verifies; encrypts DEK to the enclave pubkey; returns.
4. Enclave decrypts DEK in-memory, streams encrypted weights from object store, decrypts into HBM, runs.

**Rotation:** issue a new image → new measurement → extend KMS allowlist → roll deployment → remove old measurement from allowlist. Old enclaves automatically lose key access.

**Threat model:** as Pattern 1, plus trust in the KMS operator's enforcement of attestation conditions. To reduce KMS trust, use multi-KMS split (Shamir) across different clouds.

---

## Pattern 3: Transparency-Logged Builds

**Goal:** anyone can independently verify what code is running.

**Pieces:**
- Reproducible container / image build (Nix, Bazel, SLSA L3+).
- On every release, publish `{image_hash, source_commit, SBOM, signature}` to a transparency log (Sigstore Rekor, or a custom Merkle log).
- Verifier (either the client's library or a separate service) refuses quotes whose measurement isn't in the log with a sufficiently old inclusion proof (prevents same-block substitution attacks).

**Why it matters:** without this, an attestation quote only proves "trust the image-builder's private signing key." With it, the builder cannot silently ship a backdoored image to a single targeted user without being publicly detectable.

**Used by:** Apple PCC, Tinfoil, some Confidential Container deployments.

**Pitfall:** reproducibility is hard. Most "works for me" containers won't rebuild bit-identically on a different machine. Budget real engineering time — this pattern is what separates "cryptographically private" from "cryptographically theatrical."

---

## Pattern 4: No-Persistence Enclaves

**Goal:** even if an operator compels the provider, there is nothing logged to hand over.

**Design rules:**
- Rootfs mounted `tmpfs` or read-only overlay; no writable persistent disk attached to the TEE at all.
- Stdout/stderr routed to `/dev/null` inside the enclave. No sidecar log shipper.
- KV cache, scratch, swap — all in-memory or encrypted ephemeral.
- Metrics emitted must be pre-aggregated (counters, histograms) with no user content, and rate-limited to prevent covert channels.
- Telemetry opt-in explicit; default off.
- On shutdown/reboot, memory is wiped by hardware (TDX and SEV-SNP do this; verify).

**Why structural beats policy:** a config flag that "disables logging" can be flipped by a compromised operator with a new deployment. Compiling out the logging code entirely, and attesting the resulting image, cannot be undone without changing the measurement and invalidating every client's trust.

---

## Pattern 5: Client-Side Verification

**Goal:** the person typing the prompt, not just an enterprise middleware layer, verifies the attestation.

**Challenge:** browsers and mobile apps don't ship Intel/AMD/NVIDIA root stores; verification is fiddly.

**Options:**
- **WASM verifier** in the browser (used by Tinfoil): ~2MB WASM blob containing collateral + verification logic. Served from a separate origin ideally pinned via Subresource Integrity, or loaded from a domain different from the inference provider so a compromised provider can't swap the verifier.
- **Mobile SDK** with pinned roots and background collateral refresh.
- **Browser extension** (EFF-style) for users who want cryptographic verification they control. Useful for high-risk users; not scalable to general public.
- **Remote verifier service** that the client trusts (weakest — client now trusts another party, but at least not the same party running the model).

The UX lie to avoid: a green padlock icon labeled "Confidential" that doesn't actually verify anything. If the verification can't fail loudly, it isn't verification.

---

## Pattern 6: Split / Confidential RAG

**Goal:** run retrieval-augmented generation where the documents, the query, *and* the retrieval index are confidential.

**Components:**
- Vector DB inside a CVM (TDX); index encrypted in HBM or disk with a key released only to attested index enclaves.
- Retrieval and generation in the *same* enclave (or a federated pair over attested channels).
- Ingestion pipeline also attested — otherwise the threat model is "operator saw every document at ingest."

**Harder problems:**
- **Oblivious retrieval:** without it, access patterns (which vectors were hit) leak even inside the TEE because the memory controller sees them. Combine with ORAM or PIR for high-assurance; costs can be 10–100×. For most threat models, in-TEE is good enough.
- **Freshness of index:** re-attesting on each ingest is heavy; use an attested ingest service + signed index chunks.

---

## Pattern 7: Confidential Fine-Tuning

**Goal:** customer uploads private training data; provider's base model weights are also private; resulting fine-tuned delta must be usable only under further attestation.

**Shape:**
- Base weights encrypted, released to training enclave via Pattern 2.
- Training data encrypted to training enclave pubkey.
- Output: LoRA / full delta, re-encrypted to a customer-controlled key or to a downstream inference enclave's attestation policy.
- Optional: zero-knowledge proof that training was the published code over the claimed hyperparameters (heavy; research-only today).

**Gotcha:** training is PCIe-heavy; CC overhead is higher than inference. Budget 15–25% on H100; Blackwell meaningfully better.

---

## Pattern 8: Attested Tool Use

**Problem:** a model in a TEE is only confidential until it calls `requests.get(url)`. The tool call exits the enclave.

**Mitigations:**
- **In-enclave tools only:** a code-interpreter that runs in a *second* nested enclave; network egress blocked.
- **Attested proxy:** all tool HTTP traffic routed through an attested proxy that strips user-identifying headers, logs nothing, and re-TLS-terminates.
- **Differential privacy on tool outputs:** noise added before returning to the model, so tool-source inference attacks are bounded.
- **Policy enclave:** a separate enclave that pre-approves (or rewrites) every outbound tool call based on attested policy; model can't exfiltrate the prompt via a crafted URL without the policy enclave signing off.

Tool use is where most "private inference" products quietly fail their threat model — scrutinize it first in any audit.

---

## Anti-Patterns (Do Not Ship)

- **"Confidential" branding with no client-side attestation.** If the client doesn't verify, the guarantee is a pinky promise.
- **Trusted operator holds the KMS key.** Then the TEE doesn't help against the one adversary it was supposed to stop.
- **Single-vendor TCB with no revocation plan.** You will wake up to a CVE; have the playbook written before the day.
- **Attesting the VM but not the GPU.** See [NVIDIA-GPU-TEE](/confidential-computing/nvidia-gpu-tee).
- **Opaque image builds.** If nobody outside the provider can reproduce the measurement, the attestation binds the world to a black box.
- **Logging "just prompts, no identity"** — prompts are identity.
- **Debug / developer attestation in prod.** SGX / TDX / SEV-SNP all have debug modes; production policy must reject them.

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

