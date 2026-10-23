---
title: "Open-Source TEEs"
slug: open-source-tees
type: deep-dive
pillars: ["confidential"]
readiness: experimental
description: "Open-source trusted execution environments such as Keystone on RISC-V and OP-TEE: alternatives to vendor TEEs, and how far they have come."
dek: "The other half of the confidential-computing landscape. Vendor TEEs (SGX, SEV-SNP, TDX, Apple SEP) ship with proprietary firmware and vendor-controlled attestation roots. Open-architecture projects — Keystone, Sanctum, OpenTitan, RISC-V CoVE, MultiZone — try to move root-of-trust authority into auditable silicon and code."
updated: 2026-04-26
created: 2026-04-26
origin: vault
source: "01-Confidential-Computing/Open Source TEEs.md"
aliases: ["Open Source TEE", "Open TEE", "Open Architecture TEE", "RISC-V TEE"]
tags: ["confidential-computing", "tee", "open-source", "riscv", "keystone", "opentitan", "sanctum", "cove", "multizone"]
---

## Why open TEEs matter

Every commercial TEE has the same structural property: the root of trust signing key lives at the silicon vendor. Intel signs SGX/TDX collateral; AMD signs SEV-SNP via the PSP; NVIDIA signs GSP firmware; Apple signs SEPOS; IBM signs SE host-key documents. Customers of those TEEs get strong isolation against everyone *except* the silicon vendor.

Open TEE projects address two distinct pieces of that problem:

1. **Open architecture** — the spec and reference implementation are public, so the protocol is auditable even if a given chip's instantiation is not.
2. **Open root of trust** — the chip's master signing key is generated and held under conditions the customer can verify, ideally via reproducible builds and open silicon design, not just vendor attestation.

Most production projects today address only the first. OpenTitan is the most credible attempt at the second.

## Keystone (UC Berkeley)

### What it is

Keystone is a modular framework for building enclaves on RISC-V, started at UC Berkeley around 2018 and presented at EuroSys 2020 (Lee et al., *Keystone: An Open Framework for Architecting Trusted Execution Environments*). Rather than a single TEE, it is a kit of components: a Security Monitor (SM) running in RISC-V machine mode (M-mode) plus a runtime (Eyrie) running in supervisor mode (S-mode) inside each enclave.

### Architecture

```
   M-mode    │  Security Monitor (SBI extension)        │  ← Keystone TCB
   S-mode    │  Eyrie runtime    │  Untrusted host OS    │
   U-mode    │  Enclave app      │  Untrusted apps       │
             └───────────────────┴───────────────────────┘
             │  Physical Memory Protection (PMP)         │
             │  enforces enclave boundaries              │
```

- The SM uses RISC-V's Physical Memory Protection (PMP) registers to wall off enclave physical memory.
- Eyrie provides an enclave-side runtime that can be customized: minimal libc, simple paging, etc.
- Each enclave gets its own measurement and attestation key derived from the SM's measurement chain.

### Status and use

- Mostly academic. The reference port runs on SiFive boards and on QEMU.
- Industrial uptake is limited. Some research projects (Sanctuary, CURE, and various follow-ons) extend or compete with Keystone.
- Works on top of any RISC-V core that supports PMP, which is most of them. Does not require special silicon — its TCB is the Security Monitor code, not new instructions.
- Not a replacement for SEV-SNP/TDX in production. Treat Keystone as a research baseline and as a reference implementation people learn enclave architecture from.

### Repo and paper

- Repo: <https://github.com/keystone-enclave/keystone>.
- Paper: Lee, Kohlbrenner, Shinde, Asanović, Song, *Keystone: An Open Framework for Architecting Trusted Execution Environments*, EuroSys 2020.

## Sanctum (MIT)

Sanctum is the older of the two academic RISC-V TEE projects, presented at USENIX Security 2016 (Costan, Lebedev, Devadas). It predates Keystone and influenced its design. Sanctum's contribution is a clean treatment of cache side channels: the spec partitions the L1 and LLC by enclave so that timing side channels via shared cache lines are foreclosed at the architectural level rather than mitigated after the fact.

Sanctum did not become a production system. Its ideas — particularly cache partitioning as a first-class isolation primitive — show up in research papers and influenced later proposals including aspects of CoVE.

- Paper: Costan, Lebedev, Devadas, *Sanctum: Minimal Hardware Extensions for Strong Software Isolation*, USENIX Security 2016.
- Repo (historical): <https://github.com/mit-enclaves/sanctum>.

## OpenTitan

### What it is

OpenTitan is the most serious open-silicon root-of-trust project to date. lowRISC, Google, G+D Mobile Security, Nuvoton, Rivos, Seagate, Western Digital, Winbond, and others co-develop the design under an Apache-2.0 license at <https://opentitan.org>. The first commercial silicon, **Earlgrey**, taped out in 2024 with foundry partners; production silicon from Nuvoton and Winbond began sampling in 2024–2025.

OpenTitan is not a TEE for application workloads in the SGX sense. It is a discrete root-of-trust chip — the open analogue of Google's Titan, Apple's SE, or a TPM 2.0 — that other systems use as a measurement root, key custodian, and attestation source.

### What's in Earlgrey

- A 32-bit Ibex RISC-V core (in-order, 2-stage pipeline, formally verified at the ISA level via Ibex's verification effort).
- AES, HMAC, KMAC, OTBN (a big-number coprocessor for RSA / ECC / lattice crypto).
- A True Random Number Generator with NIST SP 800-90B entropy source.
- Always-on (OT-AON) domain that runs even when the host system is suspended, used for tamper detection and slow-loop monitoring.
- Manufacturing-time provisioned identities (Creator and Owner identities), enabling shared-fabrication models where the silicon vendor and the device owner are different parties.
- Fuses, life-cycle controller, and a clear life-cycle state machine (RAW → TEST → DEV → PROD → RMA).

### Why it matters

OpenTitan attacks the most opaque part of the TEE stack: the silicon root of trust itself. Where SGX/SNP/TDX/SEP all require trusting a vendor's signed firmware blobs, OpenTitan publishes the RTL, the boot ROM, and the build process. A customer with sufficient resources can verify that a given Earlgrey die corresponds to the published design, and the life-cycle controller separates "who fabbed this" from "who owns this".

OpenTitan does not, in itself, make a server confidential. It makes the *root* of confidential-computing claims auditable. Pair it with a CPU TEE for the workload-isolation half.

### Status

- Earlgrey first taped out 2024 (announcement: lowRISC, January 2024).
- Discrete chips from Nuvoton (NPCT/NTT line) and Winbond (W77Q line) are sampling and being adopted in security-sensitive products through 2024–2025.
- Google's production Titan chips have moved (or are moving) to OpenTitan-based designs internally.
- Active integration work in TPM-style use cases, secure-boot anchors, and HSM front-ends.

### Repo and docs

- <https://github.com/lowRISC/opentitan>
- <https://opentitan.org/book/>
- lowRISC, *OpenTitan Earlgrey: First Commercial Open-Source Silicon Root of Trust*, blog, 2024.

## RISC-V CoVE (Confidential VM Extension)

CoVE is the RISC-V International working group's effort to standardize VM-level confidential computing on RISC-V — the open analogue of SEV-SNP and TDX. Status as of early 2026 is in-flight: the architecture document is publicly drafted and iterating, with reference implementations in software emulators and on a few academic platforms.

Key design choices in current drafts:

- A small TEE Security Monitor (TSM) running in M-mode that mediates entry and exit from confidential VMs. Conceptually similar to the TDX module or Arm RMM.
- Memory isolation via an extension of the IOMMU and PMP infrastructure to per-VM isolation domains.
- An attestation evidence format aligned with the IETF RATS work (the same direction Arm CCA took with its CWT-based token).
- Explicit support for confidential I/O via PCIe TDISP, on the assumption RISC-V servers will adopt the same PCIe security extensions x86 and Arm are converging on.

CoVE intentionally does not specify the root signing authority for attestation — that is left to the silicon implementer — which preserves the open-architecture property without forcing a single trust hierarchy.

Production silicon implementing CoVE remains outside commodity scale. The first server-class RISC-V parts (SiFive Performance, Rivos, Ventana Veyron) are sampling or in early-access; whether and when they ship CoVE-compliant configurations depends on each vendor's roadmap. Treat CoVE as a 2026-2028 standardization story.

- Working group page and drafts: <https://github.com/riscv-non-isa/riscv-ap-tee>.
- Sahita et al., *CoVE: Confidential VMs on RISC-V*, RISC-V Summit talks, 2023–2024.

## MultiZone (Hex Five)

MultiZone is a commercial-but-open RISC-V TEE from Hex Five Security. It is a different shape from Keystone: instead of one enclave-per-process, MultiZone partitions a single RISC-V core into multiple equal-trust "zones", each with its own memory region and IRQ rights, mediated by a tiny separation kernel (the nanokernel) running in M-mode. It uses RISC-V PMP for isolation, like Keystone, but the design philosophy is closer to a separation kernel for embedded workloads than to a TDX-style confidential VM.

- Source-available reference under a dual license; commercial offering for embedded customers.
- Targets MCU-class RISC-V parts (SiFive E series, GreenWaves GAP, etc.) rather than application processors.
- Useful in the same niche as Trustonic Kinibi or ProvenCore for Arm: small, audit-friendly, embedded TEE for IoT and automotive.

Site: <https://hex-five.com/>.

## The open-vs-proprietary attestation root tension

The hard problem none of these projects fully solves: *who certifies the silicon?*

- A TEE attestation only means something if the verifier trusts the signing key.
- For Intel/AMD/Arm/Apple, the answer is "the silicon vendor".
- For OpenTitan, the design is open and the build is auditable, but the *fab* still has to be trusted, the provisioning process still has to be witnessed, and the resulting device certificate still has to be signed by *someone*.
- Keystone and Sanctum sidestep the question by reusing whatever silicon they run on, which means their root of trust is the underlying SoC vendor's — same problem, one layer up.
- CoVE inherits the same property; it standardizes the protocol but not the trust hierarchy.

A handful of partial answers in active research and deployment:

- Multi-vendor attestation: require quotes from independently rooted hardware (e.g., one Intel TDX + one AMD SEV-SNP + one OpenTitan) and only release secrets if all agree.
- Transparency-logged provisioning: publish every device certificate to a public log, so a vendor cannot silently issue a key to a different party.
- Air-gapped / witnessed provisioning: independent observers attend the key-generation ceremony.

None of these is mainstream. Treat the question as live research with practical workarounds rather than a solved problem. See [Attestation-Architecture](/kb/remote-attestation/) for how the RATS architecture frames this.

## Comparison

| Project | Layer | Open hardware | Open firmware | Production silicon | Posture |
|---|---|---|---|---|---|
| Keystone | Enclave framework on RISC-V | Reuses host silicon | Yes (Apache-2.0) | Runs on commodity RISC-V | Academic / research baseline |
| Sanctum | Architecture extension | Spec is open | Reference impl public | None at scale | Academic, influential ideas |
| OpenTitan | Root-of-trust chip | Yes (RTL public) | Yes (Apache-2.0) | Earlgrey (2024+); Nuvoton, Winbond | Production-grade RoT |
| RISC-V CoVE | VM-level TEE spec | Spec open | Reference impls in progress | Pre-scale | In-flight standardization |
| MultiZone | Separation kernel for MCUs | Reuses host silicon | Source-available, dual license | Embedded RISC-V parts | Commercial embedded TEE |

## When to use what

- *I want to research enclave architecture or build a teaching example.* Keystone, on a SiFive board or QEMU.
- *I want a measurement root and attestation source under my own audit, not Intel's or Apple's.* OpenTitan, paired with whatever CPU TEE makes sense for the workload.
- *I am building an embedded device with strict separation requirements.* MultiZone or a comparable separation kernel.
- *I am betting on a 2027+ open RISC-V server stack.* Watch CoVE; production planning should wait for commodity CoVE silicon.
- *I need confidential computing today on commodity cloud.* Use vendor TEEs (TDX, SEV-SNP) and accept the closed root of trust, or compose with an open RoT for sensitive key custody.

## Primary sources

- Lee et al., *Keystone: An Open Framework for Architecting Trusted Execution Environments*, EuroSys 2020.
- Costan, Lebedev, Devadas, *Sanctum: Minimal Hardware Extensions for Strong Software Isolation*, USENIX Security 2016.
- OpenTitan project — <https://opentitan.org> and <https://github.com/lowRISC/opentitan>.
- lowRISC blog: *OpenTitan: World's first open source silicon design verified to commercial standards*, 2024.
- RISC-V CoVE working group — <https://github.com/riscv-non-isa/riscv-ap-tee>.
- Sahita et al., *CoVE: Confidential VMs on RISC-V*, RISC-V Summit, 2023–2024.
- Hex Five MultiZone — <https://hex-five.com/multizone-security-tee-riscv/>.
