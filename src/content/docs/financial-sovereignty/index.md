---
title: "06 — Financial Sovereignty"
tags:
  - "bitcoin"
  - "lightning"
  - "privacy"
  - "self-custody"
---
Practical Bitcoin self-custody, Lightning, and on-chain privacy. **Scope-limited by design** — this section assumes Bitcoin fundamentals are well-covered elsewhere (Antonopoulos, Bitcoin Optech, learnmeabitcoin.com) and focuses on operational sovereignty practice and how Bitcoin composes with the rest of the vault.

---

## Key Files

### [Overview - Financial Sovereignty](/financial-sovereignty/overview-financial-sovereignty)

Section landing page. Self-custody principles, privacy trade-offs, scope statement.

### Practical deep-dives

- [Lightning Network Deep Dive](/financial-sovereignty/lightning-network-deep-dive) — channels, HTLCs, BOLTs, privacy properties, recent developments.
- [CoinJoin Implementation](/financial-sovereignty/coinjoin-implementation) — Wasabi 2.0 / WabiSabi, Joinmarket, Payjoin operational recipes.
- [Hardware Wallet Guide](/financial-sovereignty/hardware-wallet-guide) — device comparison, multisig patterns, threat model.

---

## Quick Reference

| Goal | Solution |
|------|---------|
| Self-custody | Hardware wallet (single-sig + passphrase, or multisig) |
| Daily-spend privacy | Lightning |
| On-chain privacy | CoinJoin (Wasabi 2.0) or Payjoin where supported |
| Instant payments | Lightning |
| Long-term storage | Multisig with diverse hardware vendors |

---

## What This Section Doesn't Cover

- Bitcoin protocol fundamentals (script, consensus, mempool) — see *Mastering Bitcoin*.
- Speculation, price analysis, "crypto" investing.
- Altcoins.
- Custodial services, ETFs.
- Sidechains and federated chains (out of scope for sovereignty practice).
