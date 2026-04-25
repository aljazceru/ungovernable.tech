---
title: "CoinJoin Implementation"
tags:
  - "coinjoin"
  - "bitcoin"
  - "privacy"
  - "payjoin"
  - "wabisabi"
  - "joinmarket"
  - "deep-dive"
  - "financial"
---
*Collaborative Bitcoin transactions that break the common-input-ownership heuristic. The most important on-chain privacy technique.*

---

## Why CoinJoin

Bitcoin transactions are public and traceable. Chain-analysis firms cluster addresses using two heuristics:

1. Common-input ownership: all inputs to a transaction are assumed to belong to one spender.
2. Change detection: outputs are bucketed into "spend" vs "change" by amount and script-type heuristics.

CoinJoin defeats heuristic 1 by having multiple unrelated spenders construct one transaction together. Done well (equal-amount outputs, multiple rounds, no input/output linkability) it pushes chain analysts back to off-chain signals: KYC at fiat on-ramps, IP correlation, address reuse.

---

## How it works

```
        Alice's input ──┐
        Bob's input ────┼──► Joint TX ──┬──► 0.1 BTC (Alice'?)
        Carol's input ──┘               ├──► 0.1 BTC (Bob'?)
                                        ├──► 0.1 BTC (Carol'?)
                                        └──► change outputs
```

All inputs are signed by their owners; signatures are valid only when all inputs are present. Each participant verifies that their own output is included before signing. The coordinator (which can itself be untrusted) handles registration, blind-signs output addresses, and broadcasts the final tx.

---

## Generations of CoinJoin

### 1. Joinmarket (2015–)

Order book of *makers* (always available, paid a small fee) and *takers* (initiating the join). Decentralized, no central coordinator. Trade-off: complex peer discovery, Sybil-prone fee market.

### 2. Wasabi 1.0 (ZeroLink, 2018)

Coordinator-driven, equal-output (0.1 BTC denomination), Chaumian-blinded outputs so the coordinator never sees who owns what. Around 100 participants per round.

### 3. Wasabi 2.0 / WabiSabi (2022)

WabiSabi (Keyless Anonymous Credentials Scheme) replaced equal-output denominations with arbitrary-amount mixing using zero-knowledge anonymous credentials. Effects:

- Variable amounts, much wider anonymity sets (no longer limited to a 0.1 BTC bucket).
- More efficient per user (one transaction can mix many denominations).
- The coordinator can charge fees without seeing user identity.

### 4. Whirlpool (Samourai, 2019–2024)

Equal-output (5 denominations) with Tor-only registration. Strict no-link between rounds. Operationally separate from Wasabi. Status: a US DOJ enforcement action in April 2024 effectively shut down operations; users moved to alternatives.

### 5. Joinstr (2023–)

Nostr-based coordinator-less CoinJoin. Uses Nostr relays for coordination; PSBT exchange happens over Nostr DMs. Early-stage but interesting for sovereignty: there is no single party to coerce.

### 6. Payjoin (BIP-78, 2020–)

A two-party CoinJoin between sender and receiver. The receiver contributes their own inputs to the payment, breaking the common-input heuristic *for that single transaction* without needing a coordinator or anonymity set.

```
Without Payjoin:
   Alice (1.0) ──► Bob (0.5) + Alice change (0.5)
   Heuristic: input is Alice's. Smaller output is change.

With Payjoin:
   Alice (1.0) + Bob (0.3) ──► Bob (0.8) + Alice change (0.5)
   Heuristic now thinks: 1.3 BTC spender owns both inputs. Wrong.
```

Payjoin doesn't need a coordinator. The receiver runs a small endpoint. It is a substantial anonymity improvement at zero on-chain cost penalty.

---

## Privacy math

For an equal-output CoinJoin with `n` participants, the per-output anonymity set is `n` *for that round*. Multi-round mixing (Whirlpool, Wasabi 2.0 cascades) compounds: 3 rounds × 100 users = 1M combinations.

But:

- Address reuse kills it instantly.
- Spending unmixed change with mixed coins re-links them (the "change link" attack).
- Unique amount fingerprints in subsequent spends can re-link.
- Coordinator-side timing analysis can correlate registration to broadcast.
- Exchange and merchant deposits identify individual outputs.

Wallet hygiene matters as much as the join itself.

---

## Tools

| Tool | Status (2026) | Notes |
|------|---------------|-------|
| Wasabi 2.0 | Active | WabiSabi, GUI desktop wallet |
| JoinMarket | Active | CLI; runs over Tor; pays for joining |
| Sparrow Wallet | Active | UI wrapper for Whirlpool (legacy) and Joinmarket |
| Joinstr | Early-stage | Decentralized via Nostr |
| Payjoin support | Spreading | BTCPay, Wasabi, Sparrow, Phoenix on roadmap |
| Whirlpool | Frozen | Coordinator shutdown 2024 |

---

## Trade-offs

### Strengths

- On-chain privacy without a separate chain. Stays under Bitcoin's settlement guarantees.
- No trusted coordinator. Modern coordinators are blind; even compromised coordinators cannot link.
- Composable with Lightning, hardware wallets, and exchange withdrawals.

### Limitations

- Fee cost. CoinJoin transactions are larger and pay coordinator fees.
- Slow. Wasabi rounds take minutes; JoinMarket can take longer waiting for makers.
- Operational pitfalls. One mistake (address reuse, mixing with KYC'd coins) collapses the privacy gain.
- Regulatory exposure. Several jurisdictions and exchanges flag CoinJoin outputs; chain-analysis vendors tag mixing transactions.
- Anonymity set is not anonymity. A 100-person set narrows further with off-chain context.

---

## Attack surface

| Attack | Description | Mitigation |
|--------|-------------|------------|
| Sybil coordinator | Coordinator runs N-1 inputs in your round | WabiSabi blinding, multi-round mixing, decentralized coordinators |
| Change-link | Spending mixed + unmixed together | Strict UTXO segregation, never re-merge |
| Amount fingerprinting | Unique amounts make outputs identifiable | Equal-output rounds, splitting before spending |
| Network correlation | Coordinator sees IP at registration | Tor mandatory; some coordinators enforce |
| Exchange flagging | Surveillance vendor tags coins | Use non-KYC on-ramps; consider Lightning intermediation |
| Tx malleability via signature | Edge cases in PSBT exchange | Standard PSBTs and signed roundtrip |

---

## Operational recipe

1. Withdraw from a KYC source to a fresh address.
2. CoinJoin (multiple rounds) via Wasabi 2.0 or Joinmarket.
3. Spend mixed UTXOs only; never co-spend with non-mixed UTXOs.
4. For payments to merchants, prefer Lightning (next-best privacy) or Payjoin if accepted.
5. Avoid exchange round-trips that link mixed back to KYC.

---

## Related Files

- [Overview - Financial Sovereignty](/financial-sovereignty)
- [Lightning Network Deep Dive](/financial-sovereignty/lightning-network-deep-dive)
- [MOC - Metadata Privacy](/meta/moc-metadata-privacy)

---

## Primary Sources

- Maxwell, Gregory, *CoinJoin: Bitcoin privacy for the real world*, 2013. [bitcointalk.org/index.php?topic=279249.0](https://bitcointalk.org/index.php?topic=279249.0)
- Ficsór, Ádám, *ZeroLink: The Bitcoin Fungibility Framework*, 2018.
- Ficsór, Kogman, Ontivero, Seres, *WabiSabi: Centrally Coordinated CoinJoins with Variable Amounts*, IACR ePrint 2021/206.
- BIP-78 *Payjoin* — [github.com/bitcoin/bips/blob/master/bip-0078.mediawiki](https://github.com/bitcoin/bips/blob/master/bip-0078.mediawiki)
- Hill, *Joinstr: Coordinatorless CoinJoins via Nostr*, 2023.

