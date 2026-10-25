---
title: "TEE state, recovery and revocation"
slug: tee-state-and-revocation
type: explainer
pillars: ["confidential"]
readiness: usable
description: "Trusted execution needs state freshness as well as isolation. Examine sealing, rollback protection, TCB recovery and changing attestation policy."
dek: "A valid enclave identity does not by itself prove that its saved state or security policy is current."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: ["remote-attestation", "tee-technologies", "tee-side-channel-attacks", "confidential-computing"]
---

## Summary

A trusted execution environment (TEE) has several different kinds of state: running code, persistent application data, firmware security versions and the verifier's accepted trust policy. Recovery must keep those layers consistent. [Remote attestation](/kb/remote-attestation/) is one input to that decision, not a complete application recovery procedure.

## Sealing and rollback

**Sealing** protects persistent data under keys tied to a platform and enclave policy. Intel's SGX TCB-recovery paper distinguishes sealing to the exact enclave measurement (`MRENCLAVE`) from sealing to a signer identity (`MRSIGNER`). The former restricts access to that enclave identity; the latter can support an update path for appropriately signed enclave versions.

Authenticating a stored blob is different from proving it is the newest blob. The cited SGX Windows SDK manual demonstrates a replay-protected policy using a monotonic counter: the enclave unseals data and compares its stored counter value with the current counter. That is a specific platform-service mechanism, not a promise that every TEE or cloud exposes counters.

Design and test how the application recognizes stale state. If it uses an external version service or checkpoint, include that service in the trust and availability model.

## TCB recovery and versioned keys

A **trusted computing base (TCB) recovery** changes the security baseline after a vulnerability or update. Intel documents renewed attestation material and migration of sealed data across TCB updates. Verifiers need an explicit rule for the accepted baseline.

AMD's SEV-SNP firmware specification separately tracks current, committed and reported TCB versions. Provisional firmware can be committed or rolled back; the reported TCB participates in deriving the versioned chip endorsement key used for attestation. These distinctions matter: a verifier should interpret the documented fields rather than assuming one version value describes every aspect of platform state.

## Attestation revocation and policy

Intel's PCS supplies certification and verification material. Its PCCS cache guide includes certificate-revocation lists, TCB information and quoting-enclave identity, and describes refreshing that material after TCB recovery. A cached certificate alone is not the complete verification input.

Intel Trust Authority documents how a platform can be reported out of date after a new baseline is published, even while a fleet update is underway. The relying party must decide what status and minimum TCB it accepts, including whether any limited transition period is appropriate.

## Trust model / threat model

Hardware vendors, firmware delivery, attestation roots, collateral freshness and the application state store remain dependencies. Updating an acceptance policy cannot retract secrets that were already exposed. Plan when to stop releasing keys, patch, re-attest, migrate data and resume service.

## Readiness

**Usable, but platform-specific.** The cited mechanisms are documented. Test recovery and rejection paths with the exact hardware, SDK and verifier you deploy.

## Limits

TCB recovery is not a guarantee against every side channel, and sealing is not an independent backup. Compare [TEE technologies](/kb/tee-technologies/), [TEE side-channel attacks](/kb/tee-side-channel-attacks/) and [confidential computing](/kb/confidential-computing/).

## Primary sources

- [Intel SGX TCB recovery and sealing-key policies](https://cdrdv2-public.intel.com/671176/intel-sgx-trusted-computing-base-recovery.pdf)
- [Intel SGX Windows SDK reference: sealed data and monotonic counters](https://cdrdv2-public.intel.com/671508/sgx-sdk-developer-reference-for-windows-os.pdf)
- [AMD SEV-SNP firmware ABI: current, committed and reported TCB](https://www.amd.com/content/dam/amd/en/documents/developer/56860.pdf)
- [Intel PCCS cache management and PCS collateral refresh](https://cc-enabling.trustedservices.intel.com/intel-sgx-tdx-pccs/08/cache_management_flows/)
- [Intel Trust Authority TCB acceptance policy](https://docs.trustauthority.intel.com/main/articles/articles/ita/concept-platform-tcb.html)
