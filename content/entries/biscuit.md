---
title: "Biscuit authorization tokens"
slug: biscuit
type: deep-dive
pillars: ["identity", "cryptography"]
readiness: usable
description: "Biscuit tokens combine public-key signatures with Datalog authorization. Holders can append restrictions offline, while verifiers enforce local policy."
dek: "Delegate a smaller set of permissions without contacting the issuer for every restriction."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: ["decentralized-identity", "verifiable-credentials", "remote-signing"]
---

## Summary

Biscuit is an authorization-token format and policy language. A holder can append restrictions to a token without contacting the issuer: **offline attenuation**. A verifier uses the issuer's public key and local authorization policy to decide whether a request is allowed.

## How it works

The issuer creates an authority block. Later blocks add checks, such as limiting a token to reading a particular resource or to a time window. The documented Datalog scoping rules are designed so that adding a block can restrict authority but cannot grant extra authority from untrusted assertions.

The current specification describes a chain of public-key signatures. Ed25519 is the default signature algorithm; the specification also supports a defined ECDSA profile. A verifier must check the cryptographic chain and evaluate checks and policy with facts about the actual request. A valid signature alone is not an authorization decision.

## Trust model / threat model

Biscuit is a **bearer token**: possession matters. Limit what a delegated copy permits and protect the original. The authorizer supplies facts such as the requested operation and current time; incorrect application facts can defeat an otherwise correct policy.

Offline verification does not supply an always-current revocation database. The project’s revocation guide describes revocation identifiers, shared revocation lists and time-based restrictions. Decide how revocation information reaches each verifier and how stale it may be.

## Readiness

**Usable with application review.** The project publishes a specification, policy documentation and implementations. Its FAQ says the specification and implementations have not been formally audited. Review the exact implementation and authorization rules before using it to protect valuable operations.

## Limits

Authorization tokens do not replace transport encryption, secure key storage or a decision about who may issue permissions. Compare [verifiable credentials](/kb/verifiable-credentials/) for signed claims, [decentralized identity](/kb/decentralized-identity/) for identifiers, and [remote signing](/kb/remote-signing/) for a separate delegation boundary.

## Primary sources

- [Biscuit introduction and offline attenuation](https://biscuitsec.org/docs/getting-started/introduction/)
- [Datalog reference and block scoping](https://biscuitsec.org/docs/reference/datalog/)
- [Current token and cryptographic specification](https://doc.biscuitsec.org/reference/specifications)
- [FAQ: audits, revocation and security limitations](https://www.biscuitsec.org/docs/help/faq/)
- [Revocation identifiers and distribution of revocation lists](https://www.biscuitsec.org/docs/guides/revocation/)
