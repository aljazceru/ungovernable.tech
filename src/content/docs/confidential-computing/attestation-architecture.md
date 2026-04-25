---
title: "Attestation Architecture"
tags:
  - "attestation"
  - "tee"
  - "dcap"
  - "sev-snp"
  - "tdx"
  - "rats"
  - "remote-attestation"
---
*Without attestation, a TEE is just a more expensive way to run the same trusted-operator model. Attestation is what makes "encrypted memory" useful to a remote party.*

---

## What attestation actually proves

A valid attestation quote proves, to a remote party, all of the following — and nothing more:

1. Hardware identity. A genuine CPU or GPU from the claimed vendor (Intel, AMD, NVIDIA) signed this quote, using a per-device key burned in at the factory.
2. TCB version. The microcode, firmware, and security-version-number (SVN) at the moment the quote was generated.
3. Measurement. A hash over the exact code and initial memory state running inside the TEE (MRENCLAVE for SGX, MRTD + RTMR for TDX, measurement for SEV-SNP, GSP firmware hash for NVIDIA).
4. Runtime data. A fixed 64-byte `REPORT_DATA` / `user_data` field the enclave chose at quote time, typically a hash of the session public key and a client-supplied nonce.

It does not prove that the code is bug-free, that the operator is honest, that the TCB is unexploited, that the code hash corresponds to readable source, that data stays confidential later, or that the quote was generated recently (without a nonce).

---

## The RATS model (IETF RFC 9334)

The IETF's Remote ATtestation procedureS architecture provides the vocabulary:

```
 ┌────────────┐  evidence   ┌──────────────┐
 │  Attester  │────────────▶│   Verifier   │
 │  (TEE)     │             │ (trusts CA)  │
 └────────────┘             └──────┬───────┘
                                   │ attestation result
                                   ▼
                            ┌──────────────┐
                            │ Relying Party│
                            └──────────────┘
```

- Attester: the TEE producing the quote (the thing being trusted).
- Evidence: the raw signed quote plus collateral.
- Verifier: the service that knows CA chains, CRLs, reference values, and decides pass or fail. It returns an attestation result, typically a JWT or EAT.
- Relying party: the client deciding "do I trust this endpoint with my prompt?" It trusts the verifier, not the attester directly.

The split matters because relying parties such as browsers and mobile apps cannot reasonably ship Intel, AMD, and NVIDIA root certificates and revocation logic. They delegate that to a verifier they trust.

Deployment styles:
- Passport model: attester sends evidence to the verifier, gets back an attestation result (token), and forwards it to the relying party on every session.
- Background-check model: relying party takes the evidence and queries the verifier itself.
- Direct: relying party is the verifier (high assurance, uncommon in consumer apps).

---

## Per-platform mechanisms

### Intel SGX (DCAP / ECDSA)

- Enclave produces an EREPORT (local, unsigned).
- Quoting Enclave produces a QUOTE: an ECDSA P-256 signature over the REPORT plus platform TCB, signed with a PCK (Platform Certification Key) whose cert chain is rooted at Intel.
- Verifier fetches PCK certs and TCB info from Intel's Provisioning Certification Service (PCS).
- DCAP (Data Center Attestation Primitives) replaces the older EPID-based model and is offline-verifiable against cached collateral.

Legacy EPID is deprecated for data centers; it is still relevant for client-SGX but mostly irrelevant to confidential inference.

### Intel TDX (Quote Generation Service)

- A TD quote is the hash of the TD's MRTD (build-time measurement of the initial guest image) plus RTMRs (four runtime-extended measurement registers) plus TCB info, signed by a TD Quoting Enclave using an ECDSA key chained to Intel.
- Verification uses DCAP collateral from Intel PCS, the same trust root as SGX.
- RTMRs let a guest bootloader extend measurements of kernel, initrd, and workload after launch. This is how you measure a running container image rather than only the VM's initial ROM.

### AMD SEV-SNP (VLEK / VCEK + ID-Block)

- The guest requests an attestation report from the PSP (Platform Security Processor) via `MSG_REPORT`.
- The report contains the launch digest, image ID, family/model/stepping, TCB version, guest-supplied `REPORT_DATA`, and a signature from the VCEK (Versioned Chip Endorsement Key) or VLEK (Versioned Loaded Endorsement Key).
- VCEK is rooted in AMD's KDS (Key Distribution Service); VLEK is cloud-issued (AWS, Azure) for operational reasons. Different trust story.
- The ID-Block / ID-Auth-Block lets the guest owner pre-commit to expected policy (debug off, SMT state, minimum ABI version) and bind that to the report.

### NVIDIA H100 / Blackwell (GSP + NRAS)

See [NVIDIA-GPU-TEE](/confidential-computing/nvidia-gpu-tee). The quote is signed by the per-device GSP key, rooted at NVIDIA's factory CA. Verification goes through NVIDIA Remote Attestation Service (NRAS) or a local verifier with pinned collateral.

### Apple Private Cloud Compute

Proprietary. Each PCC node's boot measurement is signed and published to a transparency log. The client refuses to connect unless the node's measurement is in the log. Effectively custom RATS with Apple as attester, verifier, and CA. The transparency log plus public build reproducibility make collusion detectable.

### AWS Nitro Enclaves

The Nitro Security Module signs an attestation document (COSE_Sign1) containing PCRs (typically 0, 1, 2, 8 = image, kernel, app, signing key). It's verified against AWS's Nitro root cert. Not a TEE in the SGX/SEV sense (no encrypted DRAM); it's a hardware-isolated mini-VM with attested measurement. Threat model: trust AWS silicon plus the Nitro hypervisor.

### ARM CCA (RME + RMM)

The Armv9 Realm Management Extension issues realm attestation tokens (EAT/CBOR, RFC 9711 claims) signed by a realm attestation key rooted in the platform's initial attestation key. Still early; production availability lags Intel and AMD.

---

## Collateral and freshness

A verifier needs:

1. CA / root certificates for each vendor (Intel, AMD, NVIDIA, Apple, AWS, etc.). Pin them.
2. TCB info (current security versions). Intel publishes `tcbinfo.json`, AMD publishes KDS responses. Refresh at least daily.
3. CRLs: revocation lists for compromised devices.
4. Reference values: the set of acceptable measurements (image hashes). Pipe these from your build system; do not accept "whatever was running."
5. Nonce / freshness binding: the quote must commit to a value the relying party generated this session. Without it, replay is trivial.

Practical rule: treat verifier collateral like a CA bundle. Stale collateral means false positives (accepting vulnerable TCBs) or false negatives (rejecting healthy ones).

---

## Verifier services

| Service | Scope | Notes |
|---|---|---|
| **Intel PCS / Tiber Trust Authority** | SGX + TDX | Intel's own verifier-as-a-service |
| **AMD KDS** | SEV-SNP | Raw VCEK / VLEK cert service; you still need a verifier library |
| **NVIDIA NRAS** | H100 / H200 / Blackwell | Returns EAT JWT |
| **Azure Attestation (MAA)** | Multi-platform | Azure-hosted verifier; returns JWT |
| **AWS KMS + Nitro attestation** | Nitro Enclaves | KMS policy can require specific PCR values for key release |
| **Project Veraison (CCC)** | Multi-platform, open-source | The only open, cross-vendor verifier. Pluggable. |
| **Confidential Containers Trustee / KBS** | CoCo | Attestation-gated secret release for CoCo pods |
| **Automata, Phala, Oasis on-chain** | Decentralized | On-chain quote verification; smart contracts enforce TCB minimums |

---

## Patterns for relying parties

### Key release gating (the common case)

Client uploads an encrypted model or secret to a KMS. Policy: only release the decryption key to a TEE whose measurement equals X and TCB is at least Y. The enclave requests the key, presents its quote, the KMS verifies, and the key is released. No human operator ever touches the key.

Implementations: AWS KMS + Nitro attestation conditions, Azure Key Vault Secure Key Release (SKR), GCP Confidential Space key release, CoCo Trustee, HashiCorp Vault plugin for SGX.

### Attested TLS

The TEE generates a TLS keypair inside the enclave; the public key's hash goes in `REPORT_DATA`. The client verifies the quote and pins the public key for the session. Every byte of the TLS session is bound to the attested enclave, so no intermediary can MITM.

Libraries: RA-TLS (original MSR paper plus Graphene/Gramine implementation), Occlum RA-TLS, Enarx attested TLS, Edgeless MarbleRun.

### Attested transparency (Apple PCC pattern)

The builder publishes the exact image and measurement to a signed transparency log (Sigstore / Rekor, Apple's internal log, or on-chain). The client refuses to send data unless the quote's measurement appears in the log within the last N days. This is the strongest model for public services: users do not need to inspect every image, but the image is globally auditable.

### Multi-party quorum

Two or more independent TEEs (different vendors, e.g. TDX + SEV-SNP) must both attest before a decision is accepted. Survives a single-vendor CVE. Used in some high-assurance oracle and MPC designs.

---

## Common mistakes

- No nonce. Quote replay turns attestation into theater.
- Accepting any TCB. You must reject below your minimum SVN. Quotes are happily produced by vulnerable silicon.
- Verifying only the CPU quote in a GPU inference stack. The GPU can be swapped or downgraded; see [NVIDIA-GPU-TEE](/confidential-computing/nvidia-gpu-tee).
- Hard-coding a single measurement. Any image update invalidates all clients. Use a signed allowlist or transparency log.
- Trusting the attester to time-stamp freshness. The TEE clock is not trusted; use the client nonce.
- Skipping collateral refresh. Yesterday's TCB info will not flag today's CVE.
- Logging the quote. Quotes contain `report_data`; if that includes a session key, do not log it.

---

## Related Files

- [Overview - Confidential Computing](/confidential-computing)
- [TEE-Technologies-Deep-Dive](/confidential-computing/tee-technologies-deep-dive)
- [NVIDIA-GPU-TEE](/confidential-computing/nvidia-gpu-tee)
- [Confidential-AI-Inference](/confidential-computing/confidential-ai-inference)
- [Confidential-Containers](/confidential-computing/confidential-containers)
- [TEE-Side-Channel-Attacks](/confidential-computing/tee-side-channel-attacks)

## Primary Sources

- IETF RFC 9334 — *Remote ATtestation procedureS (RATS) Architecture*
- Intel: *DCAP Reference Implementation* — `github.com/intel/SGXDataCenterAttestationPrimitives`
- Intel: *TDX Attestation Ecosystem* whitepaper
- AMD: *SEV Secure Nested Paging Firmware ABI Specification*
- Project Veraison — `github.com/veraison`
- CCC: *Common Terminology for Confidential Computing* (2022)

