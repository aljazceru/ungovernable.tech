---
title: "TLSNotary"
slug: tlsnotary
type: deep-dive
pillars: [zk, identity]
readiness: experimental
description: "TLSNotary proves selected data came from a TLS session. Learn MPC-TLS, selective disclosure, notary trust and the limits of website provenance."
dek: "Show selected parts of a website response while withholding the rest of the session."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [multi-party-computation, zero-knowledge-proofs, zkemail, verifiable-credentials]
---

## Summary

TLSNotary lets a prover demonstrate the origin of selected data from a TLS session. Its default MPC-TLS mode involves another participant in the cryptographic computation, without showing that participant the session plaintext. The website sees a normal TLS connection.

## How it works

1. The prover and verifier jointly operate the TLS session using [multi-party computation](/kb/multi-party-computation/).
2. The prover selects which transcript data to disclose.
3. The verifier checks the evidence and interprets the disclosed application data.

In the **notary** arrangement, a separate participant performs the MPC step and signs commitments to the transcript and server identity. The prover can later present selected data to a verifier that trusts this notary. The [protocol introduction](https://tlsnotary.org/docs/intro/) distinguishes this portable arrangement from direct verification.

## Trust model / threat model

The verifier must authenticate the notary's signing key and decide to trust it. A notary colluding with the prover defeats that reliance. The verifier also relies on TLS server authentication and the certificate-authority system for the claimed origin.

Selective disclosure needs an application-specific parser. A verifier must check that the disclosed field belongs to the expected response and has enough surrounding context to support the claim. The [verification documentation](https://tlsnotary.org/docs/protocol/verification/) describes checking commitment openings, TLS-specific data and server identity before parsing the revealed transcript.

This establishes provenance within those assumptions. It does not establish that a website's statement is true in the outside world. A balance, name or timestamp has only the meaning the application can justify.

## Readiness

**Experimental.** The [canonical repository](https://github.com/tlsnotary/tlsn) explicitly says the software should not be used in production and warns of bugs and major breaking changes. Use disposable test accounts and non-sensitive demonstrations while evaluating an integration.

## Limits

The introduction documents TLS 1.2 support and places TLS 1.3 on the roadmap. It also describes a separate proxy mode with a network-path assumption; its security model should not be silently substituted for MPC-TLS.

Redaction itself reveals the selected bytes. Proving a predicate about hidden bytes requires additional proof machinery. Compare [zero-knowledge proofs](/kb/zero-knowledge-proofs/) and [verifiable credentials](/kb/verifiable-credentials/) before choosing a website transcript as your evidence format.

## Primary sources

- [TLSNotary introduction and supported TLS version](https://tlsnotary.org/docs/intro/)
- [TLSNotary verification procedure](https://tlsnotary.org/docs/protocol/verification/)
- [TLSNotary repository and development warning](https://github.com/tlsnotary/tlsn)
