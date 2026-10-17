---
title: "Arm Confidential Compute Architecture (CCA)"
slug: arm-cca
type: deep-dive
pillars: ["confidential"]
readiness: experimental
description: "Arm Confidential Compute Architecture adds Realms, hardware-isolated VMs, to Arm chips: how CCA works, how it compares with TDX and SEV-SNP, and its status."
dek: "Arm's answer to TDX and SEV-SNP. Adds a fourth security state (\"Realm\") on top of the long-standing Normal/Secure split, plus a small monitor (RMM) that the hypervisor cannot observe or modify."
updated: 2026-04-26
created: 2026-04-26
origin: vault
source: "01-Confidential-Computing/Arm CCA.md"
aliases: ["Arm CCA", "Arm Confidential Compute Architecture", "Realm Management Extension", "RME"]
tags: ["confidential-computing", "tee", "arm", "cca", "realm", "armv9", "neoverse"]
---

## What CCA provides

CCA is the umbrella name for the architectural extensions Arm announced in 2021 that bring VM-level confidential computing to the Armv9-A profile. The hardware piece is the Realm Management Extension (RME); the firmware piece is the Realm Management Monitor (RMM); the memory-protection piece is the Granule Protection Table (GPT). Together they let a guest VM run in a new "Realm world" that is mutually distrustful with the hypervisor running in Normal world.

Concretely, CCA gives a guest:

- Memory confidentiality and integrity against the hypervisor, the host OS, and other VMs.
- A hardware-rooted attestation token (CCA platform + Realm token) that a relying party can verify before releasing secrets.
- A way to map I/O through the hypervisor without exposing plaintext in shared buffers (using Realm-aware virtio and, eventually, encrypted DMA via PCIe TDISP / IDE).

CCA targets both server (Neoverse) and client (Cortex-A/X) silicon. The same architecture description covers laptops, phones, and datacentre nodes.

## Architecture

### Four security states

Pre-CCA Armv8 has two orthogonal axes: privilege level (EL0…EL3) and security state (Secure or Non-secure, the TrustZone split). RME adds two more states: Realm and Root.

```
                    Non-secure          Secure         Realm           Root
  EL3                                                              Monitor / EL3
  EL2     Hypervisor (KVM)         Secure-EL2    RMM (Realm Mgmt Monitor)
  EL1     Host kernel / Guest      TrustZone OS  Realm guest kernel
  EL0     User processes           TA            Realm guest userspace
```

Root world (EL3 only) holds the platform monitor and is the most privileged. Realm world is where confidential VMs (Realms) execute. The hypervisor in Normal world can schedule a Realm and pass it I/O, but it cannot read its memory or registers.

### Granule Protection Table (GPT)

Physical memory is divided into 4 KiB granules. The GPT, owned by EL3, marks each granule as belonging to one of the four worlds. The Granule Protection Check (GPC) hardware blocks any access whose current world does not match the granule's owner. This is the primitive that gives Realms their memory isolation; it replaces SEV-SNP's RMP and TDX's SEAM mode as the integrity-enforcement structure.

### Realm Management Monitor (RMM)

The RMM is a small piece of firmware running at EL2 in Realm world. It is roughly analogous to Intel's TDX module (the SEAM module) and AMD's PSP-resident SEV firmware. Its job is to:

- Initialize Realms on hypervisor request (RMI calls from Normal-world EL2).
- Manage Realm page tables (RTTs).
- Generate Realm attestation tokens.
- Mediate every world transition into and out of Realms.

Arm publishes the RMM specification (latest revision 1.0-rel0-rc1, 2024) and a reference implementation under TF-RMM at <https://www.trustedfirmware.org/projects/tf-rmm/>. The reference RMM is small (tens of thousands of lines) compared with the Linux KVM stack the Realm cannot see.

### Realm attestation tokens

A Realm produces a CCA attestation token that is a CBOR Web Token (CWT) signed by the platform's attestation key. The token chains two parts:

- The Platform token: identifies the SoC, firmware versions for Root, RMM, and lower components, and the Hardware Implementation ID (HW IID).
- The Realm token: contains the Realm Initial Measurement (RIM, hash of initial code/data), Realm Extensible Measurements (REMs, four hash registers updated by the Realm), and a freshness nonce supplied by the relying party.

Arm has published the token format as IETF drafts under the Remote ATtestation procedureS (RATS) WG (`draft-ffm-rats-cca-token`). Verification follows the standard RATS attester / verifier / relying-party split documented in [Attestation-Architecture](/kb/remote-attestation/).

## Threat model

In the TCB:

- The CPU silicon (including caches, fabric, GPCs).
- EL3 monitor firmware (typically Trusted Firmware-A).
- The RMM at Realm-EL2.
- The Realm guest itself.

Out of the TCB:

- The hypervisor at Normal-EL2 (KVM, Xen).
- The host OS at Normal-EL1.
- All other VMs.
- The cloud operator, including DRAM-bus attackers within the limits of the platform's memory encryption (where available).

Notes on memory encryption:

- The CCA architecture does not mandate memory encryption; it mandates isolation. Some CCA implementations layer Memory Encryption Contexts (MEC) on top of GPT for confidentiality against physical DRAM attacks. Whether a given SoC encrypts Realm memory is an implementation choice; check the silicon vendor's claims.
- Compare with SEV-SNP, where AES-XEX of DRAM is mandatory, and TDX, which uses MK-TME with integrity. Arm's posture leaves more to platform vendors.

## Trade-offs

### Strengths

- Clean architectural separation: a Realm cannot be entered except through the RMM, and the GPT enforcement is a hardware check on every access.
- The RMM is small and standardized, with an open reference implementation. The TCB at the firmware layer is auditable in a way SEAM and SEV firmware historically have not been.
- Same architecture spans client and server, so a single attestation model can cover phones, edge boxes, and datacentre nodes.
- Open IETF token format aligns with the RATS architecture rather than a vendor-specific quote format.

### Limitations

- Silicon availability is still narrow. As of early 2026 it is shipping but remains outside commodity datacentre offerings.
- DRAM encryption is implementation-defined; do not assume a specific SoC matches SEV-SNP's threat model without checking.
- Side-channel posture is still being characterized in production. Arm has historically had Spectre-class issues across its cores (Spectre-BHB, the recent TIKTAG paper on MTE). The Realm boundary is new and will attract microarchitectural research; expect findings.
- Confidential I/O depends on PCIe TDISP/IDE adoption, which is still rolling out across the ecosystem.

### Side-channel posture

Cross-world attacks via cache, branch predictor, and TLB are the obvious surface. Arm's RME spec mandates context flushing on world transitions and context-tagged predictors on compliant cores, but the details vary by implementation. The TIKTAG work (Lee et al., USENIX Security 2024) showed that Memory Tagging Extension (MTE) leaks tags via speculation on Cortex-A715 and M3, which is a cautionary signal about new Armv9 features. Treat published papers like Tyche (EPFL, 2024) and Veracruz (Arm Research, 2022) as the academic baseline for how to reason about RME isolation; both predate widespread silicon and have specific assumptions worth reading.

## Comparison vs SEV-SNP and TDX

| Property | Arm CCA | AMD SEV-SNP | Intel TDX |
|---|---|---|---|
| Isolation primitive | Granule Protection Table | Reverse Map Table (RMP) | EPT + SEAM mode |
| Trusted firmware | RMM (open spec, reference impl) | PSP / SEV firmware (closed) | TDX module / SEAM (signed by Intel) |
| Memory encryption | Implementation-defined (often MEC) | Mandatory AES-XEX, per-VM key | Mandatory MK-TME with integrity |
| Attestation format | CCA token (CWT, RATS-aligned) | SEV-SNP attestation report (binary) | TDX quote (DCAP) |
| Live migration | Spec-defined; impl maturing | Yes (since SEV-SNP 1.55) | Yes (TD migration, GA 2024) |
| Client + server scope | Yes (single arch) | Server-only (EPYC) | Server-only (Xeon) |
| Production silicon | Cortex-X925/A725 (2024), Neoverse V3 (2024 design) | EPYC Milan onward (2021+) | Xeon 5th gen (Emerald Rapids, 2024 GA) |

## Primary sources

- Arm: *Arm Confidential Compute Architecture Software Stack Guide* and *Realm Management Monitor Specification* — <https://developer.arm.com/documentation/den0137/latest>.
- Arm: *Learn the Architecture: Realm Management Extension* — <https://developer.arm.com/documentation/den0126/latest>.
- TF-RMM reference implementation — <https://www.trustedfirmware.org/projects/tf-rmm/>.
- IETF RATS: *A CBOR-encoded Token for the Arm CCA Attestation Service* (`draft-ffm-rats-cca-token`).
- Sahita et al., *Tyche: A Programmable Reference Architecture for Confidential Computing*, EPFL technical report, 2024.
- Brossard et al., *Private Delegated Computations Using Strong Isolation* (Veracruz), Arm Research, 2022.
- Lee et al., *TIKTAG: Breaking ARM's Memory Tagging Extension with Speculative Execution*, USENIX Security 2024.
- Cortex-X925 / Cortex-A725 announcement, Arm press, May 2024.
- Neoverse V3 announcement, Arm press, February 2024.
