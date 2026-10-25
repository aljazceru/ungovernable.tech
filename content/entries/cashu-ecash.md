---
title: "Cashu and Chaumian Ecash"
slug: cashu-ecash
type: deep-dive
pillars: ["money"]
readiness: usable
description: "Cashu brings Chaumian ecash to Bitcoin: blind-signed bearer tokens that give near-cash payment privacy, in exchange for trusting the mint with custody."
dek: "Bearer-token ecash using blind signatures (Chaum 1982/83) backed by Bitcoin/Lightning. Private, offline-capable, small-to-medium value transfers with no on-chain footprint until redemption. Mint custody remains a central trust assumption."
updated: 2026-10-25
created: 2026-06-22
origin: vault
source: "06-Financial-Sovereignty/Cashu and Chaumian Ecash.md"
aliases: ["Ecash", "Chaumian Ecash", "NIP-60"]
tags: ["cashu", "ecash", "chaumian", "blind-signatures", "fedimint", "lightning", "nostr", "financial-privacy", "deep-dive"]
related: ["fedimint", "bitcoin-self-custody", "btcpay-server", "zcash"]
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
- Tokens can be transferred offline by QR, USB or another transport, but the recipient must contact the mint to swap them and establish that they have not already been spent.
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

## Mint custody and hardware protection

Blind signatures protect the link between issuance and redemption; they do not prove reserves or prevent the mint from refusing redemption. Cashu users still trust the mint’s custody and availability.

Running mint code in a TEE is a possible deployment pattern, not a guarantee supplied by Cashu. Attestation must be checked against a policy, and hardware, code, reserve custody and rollback behavior remain part of the threat model. See [Remote attestation](/kb/remote-attestation/) and [Confidential computing](/kb/confidential-computing/).

## Nostr integration (NIP-60 / 61)

- **NIP-60**: Ecash wallet standard for Nostr. Wallet state and token records use encrypted Nostr events as specified by NIP-60.
- **NIP-61**: Nutzaps — Cashu tips using kind 9321 events. Recipient tags, sender identity and proofs in these events are public; the proofs are locked for the recipient.
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
- **Double-spend risk**: A sender can pass the same proof to multiple recipients. The mint rejects already-spent proofs; recipients need an online swap before treating payment as final.
- **Key loss / device loss**: No recovery unless you backed up the tokens or used multi-mint + social recovery patterns.
- **Mint correlation**: A single mint sees all its issuances and redemptions. Use many small mints + swaps.
- **Nostr metadata**: Without NIP-17 gift wrapping, ecash events leak graph. Use wrapped.
- **Cryptographic basis**: Cashu uses Blind Diffie-Hellman Key Exchange (BDHKE) on secp256k1, as specified by NUT-00. For migration considerations, see [Post-Quantum Cryptography](/kb/post-quantum-cryptography/).

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
| Cashu/Ecash | Blindness against mint; transport metadata remains | Token transfer only; online check needed | Fixed + swaps | Blind signatures; mint remains custodian | Small transfers and tips |

They compose: CoinJoin → LN channel → Cashu mint deposit → private ecash spends.

## Implementations & wallets (2026 snapshot)

- **Cashu core**: Python reference, various Rust/TS ports; protocol continues evolving with keyset rotation, DLEQ proofs for better security, etc.
- **Fedimint**: Federated Chaumian; used in some Nostr trade stacks (Chama etc.).
- **Wallets**: Amethyst (unified Nostr + Cashu + LN + on-chain), Zeus (Cashu + NIP-47), Minibits, others with NIP-60.
- **Mints**: Public "trust-minimized" ones; watch for TEE deployments and independent audits. Run your own for personal use.
- **Nutzaps**: Native in modern Nostr clients supporting NIP-61.

See [Nostr Deep Dive](/kb/nostr-protocol/) and recent Identity weeklies for client status.

## Primary sources

- [Cashu NUT-00: blind Diffie-Hellman signatures and tokens](https://github.com/cashubtc/nuts/blob/main/00.md)
- [Cashu NUT-03: token swaps and double-spend checking](https://github.com/cashubtc/nuts/blob/main/03.md)
- [NIP-60: Cashu wallet events](https://github.com/nostr-protocol/nips/blob/master/60.md)
- [NIP-61: Nutzaps](https://github.com/nostr-protocol/nips/blob/master/61.md)
- [Cashu reference implementation](https://github.com/cashubtc/nutshell)
- [Fedimint implementation](https://github.com/fedimint/fedimint)
- [Amethyst releases](https://github.com/vitorpamplona/amethyst/releases)
- [Zeus releases](https://github.com/ZeusLN/zeus/releases)
- [Cashu FAQ: custody and mint trust](https://docs.cashu.space/faq)
- [Chaum: Blind Signatures for Untraceable Payments](https://chaum.com/wp-content/uploads/2022/01/Chaum-blind-signatures.pdf)
- [RFC 9334: Remote ATtestation procedureS Architecture](https://www.rfc-editor.org/rfc/rfc9334.html)

For a dedicated account of guardian custody, threshold blind signatures and Lightning gateway contracts, see [Fedimint](/kb/fedimint/). Compare it with [Bitcoin self-custody](/guides/bitcoin-self-custody/), [BTCPay Server](/kb/btcpay-server/) and [Zcash](/kb/zcash/) when deciding which custody and privacy assumptions fit a payment.
