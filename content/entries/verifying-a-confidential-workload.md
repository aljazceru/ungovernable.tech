---
title: "Verifying a confidential workload"
slug: verifying-a-confidential-workload
type: guide
pillars: [confidential]
readiness: usable
description: "Verify an Intel SGX workload with Gramine RA-TLS: establish expected measurements, check hardware evidence and bind secret release to the connection."
dek: "Release a test secret only after the workload, hardware evidence and communication channel satisfy your policy."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [remote-attestation, tee-technologies, gramine, confidential-computing, tee-side-channel-attacks]
level: advanced
---

## Summary

This walkthrough uses **Intel SGX with Gramine's RA-TLS secret-provisioning example**, extending the [TEE overview](/kb/tee-technologies/). It requires an SGX-capable environment, Gramine with DCAP support, and working DCAP infrastructure. The example releases a disposable test secret; adapt it only after reviewing the application and verifier.

## 1. Establish what you intend to trust

Obtain a reviewed Gramine source checkout matching the installed libraries. Use `CI-Examples/ra-tls-secret-prov/secret_prov_minimal` as the workload. Read its manifest and application before generating expected measurements.

Change `sgx.debug` to `false` in the minimal client's manifest template before building. Keep the executable, dependencies and provisioning server's CA certificate among the trusted files. If the verifier runs on another machine, configure its address and your own TLS certificate infrastructure before signing.

Do not take an expected measurement from the untrusted workload's own report. Derive it from the build you approved:

```sh
# From CI-Examples/ra-tls-secret-prov in the reviewed source checkout:
make app dcap
gramine-sgx-sigstruct-view secret_prov_minimal/client.sig
```

Record `MRENCLAVE`, `MRSIGNER`, `ISV_PROD_ID` and `ISV_SVN`. The [example README](https://raw.githubusercontent.com/gramineproject/gramine/master/CI-Examples/ra-tls-secret-prov/README.md) documents these commands and its intentionally permissive test defaults.

## 2. Configure the verifier's acceptance policy

Run the provisioning server in an environment you trust. Set these variables from the reviewed signature information:

| Setting | Required check |
|---|---|
| `RA_TLS_MRENCLAVE` | Expected enclave measurement |
| `RA_TLS_MRSIGNER` | Expected enclave signer |
| `RA_TLS_ISV_PROD_ID` | Expected product ID |
| `RA_TLS_ISV_SVN` | Minimum accepted enclave security version |

Do not set them to `any`: that skips the corresponding check. Keep the debug and outdated-TCB bypasses disabled. The documented variables are `RA_TLS_ALLOW_DEBUG_ENCLAVE_INSECURE` and `RA_TLS_ALLOW_OUTDATED_TCB_INSECURE`. Review hardware-configuration and software-hardening results explicitly rather than copying the test suite's overrides.

The [RA-TLS reference](https://gramine.readthedocs.io/en/stable/attestation.html) describes how its verifier delegates quote checking to Intel's DCAP verification library. Working measurement comparisons alone are insufficient: hardware evidence and its supporting validation data must also pass your policy.

## 3. Attest, connect and release

Start the minimal provisioning server in its example directory on the verifier side:

```sh
cd secret_prov_minimal
./server_dcap
```

In the corresponding client directory on the SGX side, run:

```sh
gramine-sgx client
```

The client creates an RA-TLS certificate containing its SGX quote. The quote binds the TLS public key, so the verifier checks the evidence for the endpoint participating in the TLS session. The client also authenticates the provisioning server using its configured CA. Only successful verification should release the example secret through that connection.

## 4. Test rejection and repeat after updates

Change the expected measurement to a different value and confirm provisioning fails. Restore it, then confirm a debug enclave is rejected with the debug exception disabled. An updated application or manifest needs a new reviewed measurement; do not fix a failed update by allowing every measurement.

Distinguish a fresh TLS handshake from a blanket promise that all evidence is newly generated. Define evidence freshness and collateral-expiration policy explicitly, using the [RATS architecture](https://www.rfc-editor.org/rfc/rfc9334.html) as a checklist for evidence, endorsements, reference values and appraisal.

## Trust model / threat model

Trust includes Intel's attestation roots, the approved application and Gramine build, and the verifier's libraries, policy and reference-value distribution. A remote verification service adds its operator to that set. The host can still deny service; attestation is not a proof that application code has no bugs.

## Readiness and limits

**Usable integration pattern, with a demonstration service.** Gramine explicitly describes its secret-provisioning service as minimal. Replace example certificates and secrets, retain strict checks, and review [side channels](/kb/tee-side-channel-attacks/) before adapting it for sensitive workloads.

## Primary sources

- [Gramine attestation and RA-TLS verification](https://gramine.readthedocs.io/en/stable/attestation.html)
- [Secret-provisioning example instructions](https://raw.githubusercontent.com/gramineproject/gramine/master/CI-Examples/ra-tls-secret-prov/README.md)
- [Example build and execution targets](https://raw.githubusercontent.com/gramineproject/gramine/master/CI-Examples/ra-tls-secret-prov/Makefile)
- [Minimal client manifest](https://raw.githubusercontent.com/gramineproject/gramine/master/CI-Examples/ra-tls-secret-prov/secret_prov_minimal/client.manifest.template)
- [Gramine manifest and trusted-file rules](https://gramine.readthedocs.io/en/stable/manifest-syntax.html)
- [RFC 9334: remote attestation architecture](https://www.rfc-editor.org/rfc/rfc9334.html)
