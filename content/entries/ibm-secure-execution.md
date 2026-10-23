---
title: "IBM Secure Execution (LinuxONE / Z)"
slug: ibm-secure-execution
type: deep-dive
pillars: ["confidential"]
readiness: usable
description: "IBM Secure Execution brings confidential VMs to IBM Z and LinuxONE mainframes: architecture, attestation and how it compares with x86 TEEs."
dek: "The mainframe answer to confidential computing. Fifty years of LPAR isolation engineering, repackaged as an Ultravisor that protects Linux guests from the hosting hypervisor and operator."
updated: 2026-04-26
created: 2026-04-26
origin: vault
source: "01-Confidential-Computing/IBM Secure Execution.md"
aliases: ["IBM Secure Execution", "Secure Execution for Linux", "IBM SE", "Ultravisor"]
tags: ["confidential-computing", "tee", "ibm", "s390x", "secure-execution", "ultravisor", "hyper-protect"]
---

## What it provides

Secure Execution for Linux is IBM Z's VM-level confidential-computing facility on the s390x architecture. It is the moral equivalent of SEV-SNP or TDX on x86: an unmodified-ish Linux guest runs as a "Secure Execution guest" with memory encryption, integrity protection, and remote attestation against the hypervisor (KVM or z/VM), the host operator, and physical bus attackers.

What a Secure Execution guest gets:

- Memory encryption at the hardware level, with per-guest keys held by trusted firmware.
- Integrity-protected initial image: the boot disk is wrapped to a host-key document that names a specific machine, and the firmware refuses to start the guest anywhere else.
- Attestation that the running image matches the wrapped one, signed by IBM with a CCA-rooted certificate chain (separate from Arm CCA — IBM CCA stands for Common Cryptographic Architecture, a long-standing crypto-card stack).
- A clear separation between control (the hypervisor can start, stop, schedule) and visibility (the hypervisor cannot read state).

The story IBM tells: SE is not a new TEE category. It is a refinement of the same workload-isolation discipline that LPAR (Logical Partitioning) and PR/SM have provided on Z mainframes since the 1980s, now extended down to individual KVM guests rather than whole partitions.

## Architecture

### Privilege model: PR/SM, hypervisor, Ultravisor

```
   ┌──────────────────────────────────────────────────────┐
   │                    Z hardware (CPC)                   │
   │  ┌───────────────────────────────────────────────┐    │
   │  │   PR/SM hypervisor (LPAR isolation, EAL5+)    │    │
   │  │  ┌──────────────────┐  ┌──────────────────┐   │    │
   │  │  │   LPAR (z/OS)    │  │   LPAR (Linux)   │   │    │
   │  │  │                  │  │  ┌────────────┐  │   │    │
   │  │  │                  │  │  │ KVM / z/VM │  │   │    │
   │  │  │                  │  │  └────────────┘  │   │    │
   │  │  │                  │  │  ┌────────────┐  │   │    │
   │  │  │                  │  │  │ SE guest A │  │   │    │
   │  │  │                  │  │  └────────────┘  │   │    │
   │  │  │                  │  │  ┌────────────┐  │   │    │
   │  │  │                  │  │  │ SE guest B │  │   │    │
   │  │  │                  │  │  └────────────┘  │   │    │
   │  │  └──────────────────┘  └──────────────────┘   │    │
   │  └───────────────────────────────────────────────┘    │
   │  ┌───────────────────────────────────────────────┐    │
   │  │   Ultravisor (millicode + firmware)           │    │
   │  │   - Memory protection, key custody, attest    │    │
   │  └───────────────────────────────────────────────┘    │
   │  ┌───────────────┐  ┌───────────────┐                  │
   │  │  CEX8S HSM    │  │  CEX8S HSM    │  (CCA / EP11)    │
   │  └───────────────┘  └───────────────┘                  │
   └──────────────────────────────────────────────────────┘
```

The Ultravisor is the core architectural addition. It runs at a privilege level above the hypervisor (z/Architecture introduced UV-call instructions and a dedicated state). The Ultravisor owns the page-encryption keys, owns the integrity tags, and is the only entity that can move a page between "secure" and "shared" states. The hypervisor schedules the SE guest and sees its IO traffic, but every memory access from outside the guest goes through the Ultravisor's mediation.

### Key wrapping and the host-key document

Each Z machine has a unique host key — an asymmetric key whose public half IBM publishes as a signed "host-key document" associated with that specific CPC's serial number. To deploy an SE workload:

1. The image owner takes a Linux kernel + initrd + parameters and uses `genprotimg` to wrap it to one or more host-key documents.
2. The resulting image binds the workload to those specific machines. It cannot be booted elsewhere, even by the rightful owner; it cannot be inspected by the hypervisor.
3. At boot, the Ultravisor unwraps the image with the host key, verifies the integrity tag, and starts the guest in protected mode.

This is a different shape of attestation from SGX/SNP/TDX: the trust decision is made *before* deployment, by signing the image to a target machine, rather than at run time. SE also supports run-time attestation queries via the `pvattest` tool, which generates a request, the Ultravisor produces a signed response, and an external verifier checks it against IBM's cert chain.

### CEX HSM cards

Z systems pair SE with CEX (Crypto Express) cards — physical HSMs that run either CCA firmware (banking-grade key management, FIPS 140-3 Level 4 in some configurations) or EP11 (PKCS#11-compatible). Hyper Protect Crypto Services on IBM Cloud is built on these. SE guests can be wired to a CEX card via APQN passthrough so that a workload's keys never exist outside the HSM, even inside the SE-protected guest.

This combination — encrypted memory plus dedicated HSM-resident keys plus PR/SM partitioning — gives a defence-in-depth posture that does not exist on commodity x86 in the same productized form.

## Threat model

In the TCB:

- The Z processor silicon and millicode.
- The Ultravisor firmware.
- IBM's host-key signing infrastructure.
- The signed Linux kernel + initrd that the customer wrapped.
- Optionally: CEX8S firmware for HSM-backed keys.

Out of the TCB:

- The hypervisor (KVM running in a Linux LPAR, or z/VM).
- The host Linux kernel underneath KVM.
- Cloud or datacentre operators.
- Other LPARs on the same machine (PR/SM enforces this; SE adds a second layer).

Honest scoping notes:

- The TCB sits on IBM-controlled silicon and IBM-signed firmware. As with SEV-SNP (AMD-controlled) and TDX (Intel-controlled), the vendor is the root of trust. The difference is that IBM also operates the cloud where these workloads typically run (IBM Cloud Hyper Protect Virtual Servers), so customers are explicitly trusting IBM at multiple layers.
- Hyper Protect markets a "Confidential Computing for cloud-native workloads" story where IBM administrators have no path to the customer's data even with full operational access. IBM's contractual claim is "IBM does not have access" — backed by SE's architectural enforcement, not just policy.

## Trade-offs

### Strengths

- Mature isolation lineage: LPAR has decades of audit history (Common Criteria EAL5+ for PR/SM). SE inherits that discipline rather than starting from a 2015-era cold start like SGX.
- Memory encryption + integrity is mandatory and architecturally enforced, comparable to SEV-SNP rather than to bare SEV.
- HSM integration via CEX cards is unmatched in the commodity-x86 world. AWS Nitro Enclaves talk to KMS; SE can talk to a physical FIPS 140-3 L4 module on the same chassis.
- The pre-deployment image-signing model removes a class of run-time attestation foot-guns. The image either matches a host key or it does not boot.
- Exceptionally low side-channel surface in published literature, partly because z/Architecture is less academically targeted than x86.

### Limitations

- Vendor and platform lock-in. SE only runs on IBM Z (z15, z16, z17 generations) and LinuxONE. There is no commodity-server analogue.
- Cost. Z silicon, software stack, and operational tooling carry a mainframe price tag.
- Smaller ecosystem of confidential-computing tooling. Most cloud-native CC tools (Confidential Containers, Constellation, Marblerun) target x86 first; s390x support is a second-class citizen if it exists.
- The pre-deployment wrapping model is rigid for highly dynamic workloads; you cannot easily move an SE image between machines without re-wrapping to the new host-key documents.

### Side-channel posture

Public side-channel research on z/Architecture is sparse compared with x86. This is partly because of architectural differences (different cache hierarchy, no SMT in many configurations) and partly because the academic target of opportunity is x86 hyperscaler workloads. Absence of evidence is not evidence of absence; treat it as an under-studied platform rather than a definitively safer one.

## Comparison vs SEV-SNP / TDX

| Property | IBM Secure Execution | AMD SEV-SNP | Intel TDX |
|---|---|---|---|
| Vendor root of trust | IBM | AMD | Intel |
| Memory protection | Encryption + integrity, per-guest key | Encryption + integrity (RMP) | Encryption + integrity (MK-TME) |
| Attestation timing | Mostly pre-deployment (image wrap) + run-time pvattest | Run-time (SNP report) | Run-time (TDX quote) |
| HSM integration | CEX cards, CCA / EP11, FIPS 140-3 L4 possible | KMS-mediated | KMS-mediated |
| Heritage | PR/SM (1988+), LPAR audit lineage | Bare-metal AMD-V + SEV (2017+) | VT-x + SEAM (2022+) |
| Hardware footprint | IBM Z mainframe only | EPYC servers | Xeon servers |
| Live migration | Yes (within a CPC, between SE-capable machines with appropriate wrapping) | Yes (SEV-SNP 1.55+) | Yes (TD migration GA 2024) |
| Public side-channel research | Sparse | Several (CacheWarp, Hertzbleed) | Several (TDXDown, etc.) |

## Primary sources

- IBM Redbooks: *Introducing IBM Secure Execution for Linux* (SG24-8501) — <https://www.redbooks.ibm.com/abstracts/sg248501.html>.
- IBM Documentation: *Secure Execution* on z/Architecture — <https://www.ibm.com/docs/en/linux-on-systems?topic=virtualization-secure-execution>.
- s390-tools repository — <https://github.com/ibm-s390-linux/s390-tools> (`genprotimg`, `pvattest`).
- Linux kernel `Documentation/arch/s390/protvirt.rst`.
- IBM Z Hardware Security Module: *Crypto Express 8S* product brief.
- z17 announcement, IBM, April 2025 (Telum II processor).
- IBM Hyper Protect Virtual Servers documentation — <https://www.ibm.com/products/hyper-protect-virtual-servers>.
