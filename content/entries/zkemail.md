---
title: "ZK Email"
slug: zkemail
type: deep-dive
pillars: ["zk", "identity"]
readiness: experimental
description: "ZK Email proves facts about emails, such as who sent them, by verifying DKIM signatures inside a zero-knowledge proof without revealing the email."
dek: "Verifying RSA-2048 DKIM signatures inside a SNARK. The construction lets a user prove \"this email landed in my inbox from `sender@domain`, with these specific contents matching this regex,\" without revealing the rest of the email or trusting any party other than the SMTP infrastructure that already exists. Originated by Sora Suegami and the zkEmail Project (Privacy & Scaling Explorations, Ethereum Foundation, 2023). Practical applications include account recovery, email-based identity proofs, and peer-to-peer fiat onramps using payment-confirmation emails."
updated: 2026-04-26
created: 2026-04-26
origin: vault
source: "09-Zero-Knowledge/zkEmail.md"
aliases: ["ZK Email", "DKIM ZKP"]
tags: ["zk", "zkemail", "dkim", "email", "identity", "deep-dive"]
---

## Why this matters

Email is the closest thing to a universal identity layer. Most online accounts authenticate via email, payment providers send signed receipts to email, and the SMTP infrastructure already cryptographically signs outbound mail via DKIM (DomainKeys Identified Mail, RFC 6376).

A DKIM signature is an RSA signature over a canonicalized hash of email headers (and optionally body). The signing key's public component is published in DNS as a TXT record at `<selector>._domainkey.<domain>`. Any receiver can verify a DKIM signature without contacting the sender — the cryptographic chain is sender's domain DNS → public key → signature on email content.

zkEmail makes the verifier into a SNARK circuit. The user proves to a third party (or an on-chain contract) that they hold an email validly signed by `<domain>`, satisfying some predicate over its content, *without revealing the full email*.

This is potentially powerful: any email-driven workflow becomes a primitive that can be plugged into ZK applications without requiring the email provider's cooperation.

## Construction

The circuit verifies, in zero-knowledge:

1. **RSA signature verification.** Given a domain's public key (typically RSA-2048), verify that the DKIM `b=` signature is valid for the canonicalized headers (and optionally body hash).
2. **Email parsing via regex circuits.** Apply a precompiled regex circuit to specific portions of the email (for example: `From:` line, `Subject:` line, the body) to extract committed substrings.
3. **Predicate over extracted substrings.** Check the predicate the application cares about — e.g. "the From header equals `payments@venmo.com`," "the body contains an amount field matching `$\d+\.\d{2}`."
4. **Public outputs.** The proof publishes only the things the application needs: the sender domain, the public key fingerprint, and any predicate outputs (e.g. extracted amount, recipient handle).

The user's email body, headers, and other fields stay private.

### RSA-2048 in a SNARK

Verifying a 2048-bit RSA signature inside a SNARK requires implementing big-integer modular exponentiation in the SNARK's native field (typically a 254-bit BN254 field). This is expensive — the original 2023 zkEmail circuit took on the order of minutes to prove on commodity hardware.

The circuit decomposes the 2048-bit modular exponentiation into chunks (often 121-bit or 64-bit limbs) and uses lookup arguments to accelerate range checks. Much of the engineering work in zkEmail since 2023 has been driving prover times down by a factor of 10x to 100x.

By 2024-2025, optimizations brought typical proof generation to seconds-to-tens-of-seconds on a laptop, with WASM-based browser proving feasible for many email shapes.

### Regex circuits

The "regex in a SNARK" component is a separate but reusable piece of zkEmail's infrastructure. The team built a compiler from regex patterns to circuit constraints — the compiler outputs a state-transition table for a deterministic finite automaton (DFA) and the circuit proves that running the DFA over the (private) input ends in an accepting state.

This regex-in-SNARK component is independently useful (used elsewhere for parsing JSON, JWT, etc.).

## Applications

### Email-based identity proofs

A user can prove "I received an email from `boarding@united.com` containing flight reference `ABCD12`" without revealing the rest of the email. Application: prove participation in an event, prove receipt of a specific service, prove a relationship with a specific company.

### ZK email account recovery

Email-based account recovery for smart wallets. The pattern:

1. The wallet stores a recovery email address committed inside the contract.
2. To trigger recovery, the user emails their wallet a message like "I want to recover wallet 0x123 to new address 0x456".
3. The SMTP server signs the email with DKIM.
4. The user generates a zkEmail proof that the signed email matches the format and originated from the committed address.
5. The wallet contract verifies the proof and updates the owner.

This avoids the user revealing the contents of their email or trusting an oracle. Used by experimental account-abstraction wallets in 2024-2025.

### ZKP2P — peer-to-peer fiat onramp

ZKP2P (zkp2p.xyz, 2023-) uses email-receipt-style proofs from Venmo, PayPal, Revolut, and similar services to allow trustless fiat-to-crypto exchanges:

1. Buyer wants to acquire crypto, sends fiat via Venmo to a seller off-chain.
2. Buyer receives Venmo confirmation email, signed with DKIM by `venmo.com`.
3. Buyer generates zkEmail proof of "Venmo confirmation, amount X, recipient seller".
4. On-chain contract verifies proof and releases seller's locked crypto to buyer.

The system replaces a traditional escrow's trusted operator with a SNARK over a payment-confirmation email. The seller doesn't have to trust the buyer; the buyer doesn't have to trust an oracle. The trust assumption is *DKIM* — the seller trusts that Venmo's keys haven't been compromised.

ZKP2P expanded across multiple payment processors over 2024-2025.

### Anonymous attestation of email events

A user can prove "I received an email from a `*.gov` domain about a public-record event" while hiding the recipient's identity. Application: whistleblowing, public-records reporting, journalism source verification.

### Domain-bound identity

Prove "I have an `@harvard.edu` email" without revealing which one. Composes with [Semaphore](/kb/semaphore/)-style group membership: an issuer can issue identity commitments to anyone who proves a `@harvard.edu` email via zkEmail.

## Trust assumptions

### What you trust

1. **DKIM signing key publication.** You trust that the public key the prover used was correctly resolved from DNS for the relevant domain at the relevant time. Any project verifying a zkEmail proof must check that the key fingerprint matches a known DKIM key for the claimed domain.
2. **DNS / DNSSEC.** Without DNSSEC, the DNS-published key is itself trust-on-first-use. Most production DKIM deployments don't use DNSSEC, so a domain-takeover attacker who briefly controls DNS could publish a fake key. zkEmail proofs are only as strong as the DNS-key resolution layer.
3. **DKIM key rotation.** Keys rotate; archived emails carry the key from when they were sent. The verifier needs a registry of historical DKIM keys. Projects use the `zk-email-archive` (or equivalent) to commit to historical key sets on-chain.
4. **Sending domain.** You trust that the domain's mail infrastructure isn't compromised — a compromised mail server could sign arbitrary emails.

### What you don't have to trust

- The recipient. The recipient generates the proof; the verifier doesn't trust them.
- An oracle or attestation provider. There's no separate party signing "this email was real."
- The email transport. SMTP can be unencrypted; DKIM is end-to-end.

## Limitations

### Performance

RSA-2048 in a SNARK is heavy. Despite optimization work, prover times remain measured in seconds on capable hardware and tens of seconds in browser/mobile contexts. This makes zkEmail feel sluggish for casual UX even when it works.

### Email format brittleness

Real emails have idiosyncratic formatting. Different senders (and even different versions of the same sender) format their emails differently — Venmo's confirmation email format has changed multiple times over the years. Each format change requires updating the regex circuits.

Projects maintain registries of supported email formats per provider, with provider-specific circuits. This is operational debt.

### DKIM canonicalization quirks

DKIM's canonicalization (`relaxed` vs. `simple` for headers and body) affects how the signed bytes are constructed. Implementations have to match exactly or signature verification fails. Subtle bugs in canonicalization handling have been a recurring source of zkEmail circuit issues.

### Body hash size

If the predicate is over the email body, the circuit must verify the body hash matches the DKIM body-hash assertion. Long emails make this expensive.

### RSA-2048 vs. Ed25519 DKIM

Newer DKIM deployments support Ed25519 keys (RFC 8463). Ed25519 verification in a SNARK is significantly cheaper than RSA-2048. Migrating off RSA-2048 would speed up proving substantially, but most large mail services still use RSA-2048; circuit support for Ed25519 DKIM is a forward-looking project.

## Comparison with adjacent primitives

| Primitive | What it proves | Trust root |
|-----------|----------------|------------|
| **zkEmail** | "I have an email signed by `<domain>` matching pattern" | DKIM keys via DNS |
| **TLS Notary / DECO** | "I had a TLS session with `<server>` returning data" | TLS server's cert chain |
| **zkLogin / zkPassport** | "I am a holder of a passport / OAuth identity" | Government cert chain / OAuth provider |
| **Web of Trust** | "I am vouched for by these parties" | Pairwise trust |

zkEmail is structurally similar to TLS-Notary-style approaches: extract a cryptographic statement about a real-world transaction and re-prove it in zero knowledge. Email's advantage is that DKIM is widely deployed and the cryptographic envelope is per-message (so archived emails are still verifiable). The disadvantage is heavier proving cost and format brittleness.

## Primary sources

- zkEmail Project — [zkemail.gitbook.io](https://zkemail.gitbook.io) and [github.com/zkemail](https://github.com/zkemail).
- Suegami, Tan, Ngn, *Demystifying zk-email*, PSE blog 2023.
- DKIM specification — Crocker, Hansen, Kucherawy, *DomainKeys Identified Mail (DKIM) Signatures*, RFC 6376, 2011.
- DKIM Ed25519 — Levine, *A New Cryptographic Signature Method for DKIM*, RFC 8463, 2018.
- ZKP2P — [zkp2p.xyz](https://zkp2p.xyz) and [github.com/zkp2p](https://github.com/zkp2p).
- PSE — [pse.dev](https://pse.dev).
- Regex-circom compiler — [github.com/zkemail/zk-regex](https://github.com/zkemail/zk-regex).

For evidence from web sessions, compare [TLSNotary](/kb/tlsnotary/).
