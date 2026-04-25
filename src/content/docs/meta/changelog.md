---
title: "CHANGELOG"
tags:
  - "meta"
  - "changelog"
sidebar: {"label":"CHANGELOG"}
---
Vault-level changes. New entries at top. Format:

```
## YYYY-MM-DD — One-line summary

- Change 1 (file or section)
- Change 2
```

Per-file changes appear in each file's `updated:` frontmatter; this log captures structural changes to the vault as a whole.

---

## 2026-04-25 — Scope adjustment to 06 Financial Sovereignty

- Removed `Liquid Network.md` and `DLCs and Oracles.md` — out of scope for practical-Bitcoin-sovereignty focus.
- Updated Overview, _Index, Glossary (Liquid, DLC entries removed), Sources, and MOC cross-references to match.

## 2026-04-25 — Vault audit and restructuring

- Fixed broken wikilinks across vault (README, all `_Index.md`, content files cross-referencing each other). Folder-style links replaced with links to section Overview pages.
- Standardized frontmatter — closed-set `status` values (`stub | draft | active | mature | archived`); removed non-standard `last_updated`, `maturity`, `last-review` keys; normalized `emerging` to `active`.
- Fixed factual errors:
  - `Overview - Confidential Computing`: AWS SEV-SNP cloud listing corrected to M7a/C7a/R7a; clarified Nitro Enclaves are not a CPU TEE.
  - `Overview - Fully Homomorphic Encryption`: typo `slows` → `slower`; removed unsupported "verified computation" claim, added vFHE caveat.
  - `Overview - Decentralized DNS`: cleaned draft cruft in history table; corrected Tor v3 onion-address derivation (Ed25519 base32, not SHA-1).
- Added [Research Methodology](/meta/research-methodology) § Status Legend and § Tag Taxonomy with controlled vocabulary.
- Rewrote [Glossary](/meta/glossary) — added ~50 new terms (X3DH, MLS, KEM, hybrid KEM, attested TLS, KBS, RATS, MPC, Schnorr, Taproot, fhEVM, BBS+, SD-JWT, Loopix, Sphinx, garlic routing, ML-KEM/ML-DSA, etc.); removed ambiguous entries (Cross-Signaling, generic Forking).
- Added `00 - Meta/Templates/` with Note, Overview, and Threat Model templates.
- Added MOCs for cross-cutting themes: [MOC - Censorship Resistance](/meta/moc-censorship-resistance), [MOC - Metadata Privacy](/meta/moc-metadata-privacy), [MOC - Threat Models](/meta/moc-threat-models), [MOC - Composing Primitives](/meta/moc-composing-primitives).
- Built out section 06 — Financial Sovereignty (scope: practical Bitcoin sovereignty): Lightning Network, CoinJoin, Hardware Wallets. Reframed Overview to explicitly defer Bitcoin fundamentals to existing literature.
- Built out section 07 — Encrypted Messaging: Signal Protocol, Nostr, Matrix, Metadata Resistance.
- Expanded `Sources/Sources.md` into a section-anchored bibliography.
- Updated README directory tree to match actual hyphenated folder names.

---

## 2026-04-24 — Mix Networks expansion

- `Overview - Mix Networks` content matured — Loopix, Nym, Katzenpost detail.

## 2026-04-23 — Web of Trust added

- Added `02-Cryptography/Overview - Web of Trust.md`.

## 2026-04-22 — PIR overview matured

## 2026-04-21 — Decentralized Compute expanded

- Major update to `Overview - Decentralized Compute` — Phala Cloud, Marlin Oyster, Aethir, 0G.

## 2026-04-20 — Decentralized DNS matured

## 2026-04-19 — Identity & Pseudonymity overview added

## 2026-04-17 — TEE deep-dive, side-channels, mix networks, ZK, PQC, identity initial drafts

## 2026-04-15 — Vault initialized

- 00 - Meta scaffold (README, Glossary, Research Methodology).
- Initial overviews for Confidential Computing, FHE, Off-Grid, Financial Sovereignty, Encrypted Messaging.

