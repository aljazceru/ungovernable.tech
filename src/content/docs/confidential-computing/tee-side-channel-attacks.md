---
title: "TEE Side-Channel Attacks"
tags:
  - "tee"
  - "side-channel"
  - "sgx"
  - "sev"
  - "tdx"
  - "security"
  - "attacks"
---
*A field guide. The threat model of every TEE-based system begins with "assuming no new CVEs," which is a lie. Below: what has broken, what is likely to break, and how to reduce the blast radius.*

---

## Taxonomy

| Class | Mechanism | Typical Target |
|---|---|---|
| **Microarchitectural** | Cache, TLB, branch-predictor, MDS, LVI, speculative-execution variants | SGX, to a lesser extent SEV-SNP / TDX |
| **Transient execution** | Spectre family; data that never architecturally retires leaks | All TEEs; mitigations in microcode |
| **Memory-bus / DRAM** | Memory controller traffic observation, RowHammer, Plundervolt | SEV (less after SNP), TDX less so |
| **Power / EM** | Voltage, frequency, EM emissions | Physical-access attacks, also remote via software-observable frequency (Hertzbleed, Frequency throttling) |
| **Fault injection** | Voltage glitching, clock glitching | Physical attacks on client devices; harder in cloud |
| **Controlled-channel** | Malicious OS observes page-fault sequence | SGX specifically (the OS handles paging) |
| **Firmware / PSP** | Bugs in the trusted firmware (PSP for AMD, TDX Module for Intel, GSP for NVIDIA) | Platform-breaking when found |
| **Architectural design** | Debug modes, weak key derivation, bad defaults | Any TEE |

---

## Notable real-world breaks

### Intel SGX

- Foreshadow / L1TF (2018). Read enclave memory via L1 cache side channel. Required microcode plus OS mitigations and effectively broke SGX's confidentiality guarantee on affected CPUs until patched.
- Plundervolt (2019). Undervolting via `MSR 0x150` induced computation faults inside enclaves and leaked RSA/AES keys. Fixed by Intel disabling software voltage control on SGX-capable CPUs.
- LVI (Load Value Injection, 2020). Inverse of Spectre; the attacker injects values into victim enclave loads. Mitigations are expensive (LFENCE everywhere); some real deployments accept the risk rather than take the perf hit.
- ÆPIC Leak (2022). Stale data in APIC registers leaked enclave memory; fixed in microcode.
- SGAxe / CacheOut (2020). Extracted SGX attestation keys in some cases. Catastrophic, allowed forging quotes. Remediated by TCB update.
- Ongoing: cache-timing and branch-predictor-based key extraction against crypto libraries inside enclaves remains a research area. Use constant-time crypto (libsodium, ring) and disable SMT (HyperThreading) in production.

### AMD SEV / SEV-ES / SEV-SNP

- SEVurity, SEVered (2018-2020). Pre-SNP SEV had integrity-free memory encryption, so a malicious hypervisor could remap or replay ciphertext. SNP's reverse-map table (RMP) closed these.
- undeSErVed (2021 onward). Side-channel leaks via the NPT (nested page tables) the hypervisor still controls; partially mitigated by SNP.
- CacheWarp (CVE-2023-20592, disclosed Nov 2023; USENIX Security 2024). Architectural flaw allowing rollback of writes in SEV-ES / SEV-SNP VMs. AMD issued a microcode fix.
- BadRAM (Dec 2024). Physical attack: rogue SPD on DIMMs fools the CPU about RAM size and bypasses SNP memory protection. Mitigation: SPD verification, trusted DIMM provisioning. Not relevant against purely-remote attackers.
- TCB freshness is critical. Most SEV CVEs are fully mitigated by current microcode plus PSP firmware, but only if deployed.

### Intel TDX

- TDX is newer; fewer public breaks, but it shares a pedigree with SGX. Early Intel TDX security advisories (2023-2024) covered TDX Module bugs. The TDX Module is effectively a tiny hypervisor; bugs there break all TDs on the host.
- Downfall / Gather Data Sampling (2023). Affected AVX gather instructions broadly; TDX was impacted alongside general processors. Mitigated by microcode.
- Co-tenant speculation attacks between TDs on the same host are an active research area.

### NVIDIA H100 CC

- GSP firmware CVEs (2023 onward). Several DoS and information-disclosure issues; patched via GPU firmware updates. Small surface area relative to CPU TEEs but not zero.
- Timing and thermal side channels across CUDA kernels inside a CC GPU remain underexplored publicly.
- PCIe-side attacks are largely blocked by SPDM encryption, but implementation bugs in the guest NVIDIA driver could still leak.

### Apple Secure Enclave / PCC

- checkm8 (2019): bootROM exploit on older iPhones; not applicable to PCC, but it illustrates that "immutable ROM" is not.
- PCC itself has no publicly disclosed breaks as of early 2026, but the transparency log plus closed-source server silicon mean any audit is indirect.

### ARM TrustZone / CCA

- Historical TrustZone vendor-implementation breaks are abundant (Qualcomm, Samsung). CCA is newer and less battle-tested.

---

## Transient-execution family (affects every CPU TEE)

Spectre-v1/v2, Meltdown, MDS (Fallout, RIDL, ZombieLoad), Foreshadow, SRBDS, Downfall, INCEPTION, RETbleed: a parade. Mitigations come in three flavors:

1. Microcode: required, deploy as soon as possible after each advisory.
2. Compiler / kernel: retpolines, `LFENCE`, speculative-load hardening (SLH), disabling SMT.
3. Architectural: newer CPU generations fix some at the silicon level.

Operational posture: TCB minimum version enforcement in attestation is the only way to ensure clients only talk to patched silicon. Do not rely on "we patched the fleet"; an attacker can always try to route you to an unpatched node.

---

## Controlled-channel (SGX-specific)

Because the untrusted OS handles paging for SGX enclaves, the OS can observe which pages the enclave accesses (4KB granularity) and reconstruct secrets from access patterns. Classic result: recovering plaintext from a JPEG decoder in an enclave.

Mitigations:
- Oblivious algorithms (ORAM): expensive.
- Data-independent access patterns in crypto code.
- Large-page or batched access to reduce fault observability (partial).
- Move to TDX or SEV-SNP. VM-level TEEs do not expose per-page faults to the hypervisor in the same way, though coarser-grained signals remain.

---

## Supply-chain and platform-root attacks

The most catastrophic class. A single compromised attestation signing key can mint quotes for enclaves that do not exist.

- Intel / AMD factory key extraction. So far only theoretical; would require a very capable adversary.
- PSP / TDX Module RCE. Has happened in limited form; treat every PSP / TDX Module firmware update as security-critical.
- Cloud provider attestation collateral tampering. Mitigated by pinning vendor roots, not cloud-operator roots. Do not trust MAA / NRAS blindly; cross-check against Intel/AMD/NVIDIA-published collateral.

---

## Covert and leakage channels specific to inference

- Hertzbleed (2022) / frequency-throttling leaks. Dynamic frequency scaling depends on data operands, so it produces remotely observable timing leaks even inside a TEE. Mitigation: disable turbo on high-assurance hosts, or use constant-time/operand-independent code paths for crypto. Relevant for any AES/RSA inside an enclave.
- Power side channels on GPU. Recent papers show per-kernel power draw is enough to fingerprint model architectures. Not a plaintext leak but a privacy leak.
- LLM-specific: KV-cache timing, speculative-decode hit rate, MoE expert routing. See [Confidential-AI-Inference](/confidential-computing/confidential-ai-inference) §Attack Surface.

---

## Operational hardening checklist

1. Pin minimum TCB in attestation policy; update on every Intel/AMD/NVIDIA advisory.
2. Disable SMT / HyperThreading on high-assurance nodes. It roughly doubles cost but closes a whole attack family.
3. Disable turbo / dynamic frequency scaling where the threat model includes Hertzbleed-class leaks.
4. Use constant-time crypto everywhere inside the enclave; audit your dependencies.
5. Keep enclaves small. Every added MB of code is potential side-channel surface.
6. Prefer VM-level TEEs (TDX / SEV-SNP) over SGX for new work. Fewer controlled-channel problems, better maintained.
7. Defense in depth. Combine TEE with FHE for the innermost secrets, or split trust across two independent TEEs (multi-vendor quorum).
8. Monitor vendor advisories automatically. Subscribe to Intel SA, AMD PSIRT, NVIDIA PSIRT RSS; auto-raise policy-minimum TCB when a fix ships.
9. Have a kill switch. When the next CVE drops, you must be able to blackhole the vulnerable TCB in your attestation policy within hours, not weeks.
10. Accept that TEEs are probabilistic. For threat models where a single break is catastrophic, use a TEE as defense in depth behind a cryptographic guarantee (FHE, MPC, ZK), not as the sole line.

---

## Related Files

- [Overview - Confidential Computing](/confidential-computing)
- [TEE-Technologies-Deep-Dive](/confidential-computing/tee-technologies-deep-dive)
- [Attestation-Architecture](/confidential-computing/attestation-architecture)
- [NVIDIA-GPU-TEE](/confidential-computing/nvidia-gpu-tee)

## Primary Sources

- Van Bulck et al.: *A Tale of Two Worlds: Assessing the Vulnerability of Enclave Shielding Runtimes* — CCS 2019
- Chen et al.: *SgxPectre Attacks* — EuroS&P 2019
- *CacheWarp* — Zhang et al., USENIX Security 2024 (CVE-2023-20592)
- *Hertzbleed* — Wang et al., USENIX Security 2022
- Intel SGX / TDX security advisories — `intel.com/content/www/us/en/security-center`
- AMD PSIRT — `amd.com/en/resources/product-security`
- NVIDIA PSIRT — `nvidia.com/en-us/security`

