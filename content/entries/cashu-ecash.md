---
title: "Cashu and Chaumian Ecash"
slug: cashu-ecash
type: deep-dive
pillars: ["money"]
readiness: usable
description: "Cashu brings Chaumian ecash to Bitcoin: blind-signed bearer tokens that give near-cash payment privacy, in exchange for trusting the mint with custody."
dek: "Bearer-token ecash using blind signatures (Chaum 1982/83) backed by Bitcoin/Lightning. Private, offline-capable, small-to-medium value transfers with no on-chain footprint until redemption. 2026 milestone: first production-path \"unruggable\" mints running keys inside TEE enclaves."
updated: 2026-06-22
created: 2026-06-22
origin: vault
source: "06-Financial-Sovereignty/Cashu and Chaumian Ecash.md"
aliases: ["Ecash", "Chaumian Ecash", "NIP-60"]
tags: ["cashu", "ecash", "chaumian", "blind-signatures", "fedimint", "lightning", "nostr", "financial-privacy", "deep-dive"]
---

## Why ecash for sovereignty

Bitcoin + Lightning give censorship-resistant value and speed, but:

- On-chain is public (even CoinJoin has limits and cost).
- Lightning channels have liquidity and online requirements; graph analysis possible at scale.
- Small daily spends or tips leak via amounts/timing.

Chaumian ecash gives **bearer tokens**:
- Mint issues blinded signed "notes" (proofs) in exchange for BTC/LN.
- You hold the tokens locally (like digital cash in a wallet).
- Spend by sending proofs to receiver or another mint (swaps).
- No one but you and the final redeemer sees the chain of custody.
- Works offline (send tokens via any transport: Nostr DM, USB, QR, LoRa).
- Denominations + swaps provide some fungibility.

Cashu (Bitcoin/Lightning native implementation) + NIP-60/61 (Nostr wallet + nutzaps) made it practical for the ungovernable stack.

## Core mechanics (Cashu)

- **Blind signatures**: User blinds the secret before asking mint to sign; mint signs without learning the secret. User unblinds to get a valid token. Mint cannot link issuance to redemption.
- **Proofs**: Each token is a secret + signature over a commitment. Mint tracks spent secrets (double-spend prevention via simple set).
- **Token format**: Compact (cashu: or base64) that encodes amount + proofs for a given keyset/mint.
- **Keysets**: Mint rotates keys; old keysets are for redemption only.
- **Swaps / Lightning**: Deposit via LN invoice; withdraw via LN; internal swaps between users or mints move value without on-chain.
- **Multi-mint**: Wallets can hold balances across many independent mints (diversify trust).

**Fedimint** variant: federated (threshold) mints. Multiple guardians run the mint with threshold blind signing. No single operator can inflate or steal reserves alone. More resilient but adds coordination.

## 2026: TEE-protected "unruggable" mints

Classic risk: the mint operator (or coerced) can:
- Inflate supply (sign extra notes without reserves).
- Steal backing BTC/LN.
- Correlate users via timing/amounts if not careful (or log).

Milestone (public testing reported by Cashu lead calle ~May/June 2026): first on-chain Cashu mint with keys generated and operated **entirely inside a TEE enclave** (e.g., Intel TDX/SEV-SNP or equivalent). 

- Mint operator never sees the signing keys.
- Attestation proves the correct code is running.
- Reserves can be on-chain / LN with enclave-controlled access.
- Operator cannot unilaterally inflate or exit with funds.

This moves the trust from "don't trust the mint operator" toward "trust the TEE + attestation + reproducible build + on-chain visibility of backing".

See cross-reference: [Confidential-AI-Inference](/kb/confidential-ai-inference/) / [Overview - Confidential Computing](/kb/confidential-computing/) and TEE attestation patterns. This is the canonical ungovernable composition of confidential compute + financial privacy primitive.

Still early (testing/research at time of writing); production mints will need audits, transparency logs for attestation, and user-side verification of measurements.

## Nostr integration (NIP-60 / 61)

- **NIP-60**: Ecash wallet standard for Nostr. Wallets store/receive/send tokens via Nostr events (gift-wrapped for privacy).
- **NIP-61**: Nutzaps — Cashu-based zaps/tips over Nostr (private, no public LN invoice exposure).
- Clients (Amethyst v1.12+ etc.): unified balance across Lightning + on-chain + Cashu + NWC. Per-mint views.
- Trade protocols (Mostro, Chama): use gift-wrapped transport + ecash/Fedimint settlement for P2P trades without leaking to public relays.

This makes ecash first-class in the sovereign social + money stack.

## Trust model & attack surface

### What you trust (per mint)
- Mint honesty (won't inflate or freeze redemption) — reduced by TEE + federation + on-chain proof of reserves/attestation.
- Mint availability (can redeem or swap).
- Your own key/seed backup (losing ecash tokens = lost money, like cash).
- Transport privacy when moving tokens (use gift-wrap, mixnets, offline).

### Practical attacks
- **Mint rug / inflation**: Historical risk; TEEs + threshold signing (Fedimint) + transparency are the mitigations in flight.
- **Double-spend by receiver**: Prevented by mint tracking spent secrets (if you send the same proof twice, second fails).
- **Key loss / device loss**: No recovery unless you backed up the tokens or used multi-mint + social recovery patterns.
- **Mint correlation**: A single mint sees all its issuances and redemptions. Use many small mints + swaps.
- **Nostr metadata**: Without NIP-17 gift wrapping, ecash events leak graph. Use wrapped.
- **Quantum**: Blind sig schemes (often RSA or similar in Cashu today) need PQ migration planning; symmetric parts inside proofs are easier.

### Operational hygiene
- Verify mint URL + pubkey / attestation where provided.
- Small, frequent swaps and multi-mint holdings.
- Prefer TEE/federated mints as they mature.
- Backup token exports (encrypted) separately from Nostr keys.
- For high value: treat like physical cash — small denominations, redeem to self-custody LN/on-chain promptly.

## Comparison to other privacy tools in 06

| Tool          | Privacy vs whom          | Offline | Denom flexibility | Trust minimized by     | Best for                  |
|---------------|--------------------------|---------|-------------------|------------------------|---------------------------|
| CoinJoin (WabiSabi/JoinMarket) | Chain analysts + casual observers | No (needs on-chain) | UTXO level | Participation volume + equal outputs | Larger on-chain amounts |
| Lightning     | Intermediate nodes (partial) | Needs online for routing | High (sats) | Channel counterparties + liquidity | Fast payments, larger |
| Cashu/Ecash   | Mint(s) + network observers | Yes    | Fixed + swaps    | Blind sigs + now TEE/federation | Small spends, tips, offline, private zaps |

They compose: CoinJoin → LN channel → Cashu mint deposit → private ecash spends.

## Implementations & wallets (2026 snapshot)

- **Cashu core**: Python reference, various Rust/TS ports; protocol continues evolving with keyset rotation, DLEQ proofs for better security, etc.
- **Fedimint**: Federated Chaumian; used in some Nostr trade stacks (Chama etc.).
- **Wallets**: Amethyst (unified Nostr + Cashu + LN + on-chain), Zeus (Cashu + NIP-47), Minibits, others with NIP-60.
- **Mints**: Public "trust-minimized" ones; watch for TEE deployments and independent audits. Run your own for personal use.
- **Nutzaps**: Native in modern Nostr clients supporting NIP-61.

See [Nostr Deep Dive](/kb/nostr-protocol/) and recent Identity weeklies for client status.

## Sources & Evidence

- Chaum original: "Blind Signatures for Untraceable Payments" (1982/83).
- Cashu: protocol docs, NIPs 60/61 in nostr-protocol/nips; implementation repos under cashubtc org.
- Fedimint: threshold/federated variant docs and code.
- 2026 TEE milestone: public statements and testing notes from calle (Cashu lead); Socratic seminars and Nostr discussions covering design tradeoffs and attestation.
- Client integrations: Amethyst release notes (v1.12+), Zeus PRs.
- Primary verification: run/test mints, inspect proofs, check attestation measurements when TEE mints publish them.

*Ecash is production for small values today; TEE/federated backing is the active research-to-deployment frontier that directly strengthens the ungovernable claim.*
