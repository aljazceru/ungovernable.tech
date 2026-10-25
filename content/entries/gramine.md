---
title: "Gramine"
slug: gramine
type: deep-dive
pillars: [confidential]
readiness: usable
description: "Gramine runs Linux applications in Intel SGX enclaves. Learn how manifests, trusted files and remote attestation define its security boundary."
dek: "A library OS can bring an existing application into an enclave; its manifest determines much of what that enclave trusts."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [confidential-computing, tee-technologies, remote-attestation, verifying-a-confidential-workload, oblivious-ram]
---

## Summary

Gramine is a Linux-compatible library operating system with Intel SGX support. It provides an environment for applications inside an enclave, reducing the need to rewrite them around enclave-specific interfaces. The [project overview](https://gramineproject.io/) and [repository](https://github.com/gramineproject/gramine) describe its application model.

## How it works

A **manifest** declares the executable, filesystem mappings, environment and SGX settings. Rendering and signing the manifest prepares an enclave configuration for execution. Review this configuration together with the application and its dependencies.

The [manifest reference](https://gramine.readthedocs.io/en/stable/manifest-syntax.html) distinguishes:

- **Trusted files:** their contents are checked against hashes incorporated during signing. Trusting a file establishes expected contents, not secrecy from the host holding it.
- **Allowed files:** the application may access them without that integrity guarantee. Treat their contents as attacker-controlled input.
- **Encrypted files:** a separate mechanism protects file contents; provision the necessary key through an appropriate trusted channel.

## Trust model / threat model

The protected application, its libraries, Gramine and Intel SGX's hardware and attestation foundations belong in the trust assessment. A manifest that imports unsafe environment variables or allows arbitrary configuration can undermine an otherwise valid enclave measurement.

**Attestation is also a policy decision.** Gramine exposes SGX evidence and supplies RA-TLS libraries. RA-TLS binds a TLS public key to an SGX quote. The verifier checks the quote and expected enclave measurements before releasing data over the connection. See [verifying a confidential workload](/guides/verifying-a-confidential-workload/) for a concrete walkthrough.

## Readiness

**Usable for supported SGX applications.** Gramine has documented manifest, attestation and secret-provisioning interfaces. Application compatibility, host SGX support and the verifier's policy still need testing; ordinary Linux execution is not proof that enclave protection is active.

## Limits

The attestation documentation calls its secret-provisioning service a minimal reference implementation. Treat its examples as integration exercises. The example manifests enable debug enclaves, which the accompanying README warns against using in production.

An attested program can still contain vulnerabilities. Review [TEE side channels](/kb/tee-side-channel-attacks/) and [ORAM](/kb/oblivious-ram/) when the threat includes observations outside the protected memory boundary.

## Primary sources

- [Gramine project](https://gramineproject.io/)
- [Gramine canonical repository](https://github.com/gramineproject/gramine)
- [Manifest syntax and file policies](https://gramine.readthedocs.io/en/stable/manifest-syntax.html)
- [Attestation, RA-TLS and secret provisioning](https://gramine.readthedocs.io/en/stable/attestation.html)
- [Secret-provisioning example and security caveats](https://raw.githubusercontent.com/gramineproject/gramine/master/CI-Examples/ra-tls-secret-prov/README.md)
