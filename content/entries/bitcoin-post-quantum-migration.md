---
title: "Bitcoin and the Post-Quantum Migration"
slug: bitcoin-post-quantum-migration
type: explainer
pillars: ["pqc", "money"]
description: "Why a large quantum computer would break Bitcoin's signatures, which coins are most exposed, and the proposals for migrating to post-quantum keys."
dek: "Bitcoin's signatures are quantum-vulnerable. Shor's algorithm against secp256k1 collapses ECDSA and Schnorr in polynomial time on a sufficiently large quantum computer. This file looks at the actual proposals, address-type exposure, and the soft-fork-vs-hard-fork debate, with honest status as of early 2026."
updated: 2026-10-25
created: 2026-04-26
origin: vault
source: "10-Post-Quantum/Bitcoin PQ Migration.md"
aliases: ["Bitcoin Quantum Migration", "BIP-360"]
tags: ["bitcoin", "post-quantum", "ecdsa", "schnorr", "secp256k1", "bip-360", "deep-dive"]
---

## The threat

Bitcoin uses **secp256k1** for both ECDSA (legacy) and Schnorr (Taproot, BIP-340). A cryptographically relevant quantum computer (CRQC) running Shor's algorithm would:

1. Recover the private key from the public key in polynomial time.
2. Spend any UTXO whose **public key is known** to the network.
3. Forge any future transaction, given enough quantum compute.

The economic impact would land instantly: the moment a CRQC is publicly known to exist, anyone with exposed pubkeys faces immediate theft.

The standard PQ migration playbook (used by TLS) doesn't apply directly. Bitcoin can't deprecate algorithms by serving a different cipher in a handshake; the chain has decade-old UTXOs locked to specific signature types, and any change requires consensus.

## Address-type exposure

Different Bitcoin address types expose pubkeys differently. **The pubkey is what a quantum computer needs.** P2PKH and P2WPKH outputs contain a public-key hash. P2TR outputs instead publish the tweaked public key when the output is created, before any spend.

| Address type | Pubkey on chain | Exposure |
|--------------|-----------------|----------|
| **P2PK** (pay-to-pubkey) | Always | Extreme. Pubkey is in the locking script. ~1.7M BTC sit in P2PK outputs (early Satoshi-era coins). All immediately at risk. |
| **P2PKH** (pay-to-pubkey-hash) | After first spend | Address is `HASH160(pubkey)`. Pubkey only revealed when spending. Reused addresses with prior spends are exposed. |
| **P2SH-wrapped** | Depends on script | Varies. A common P2SH-P2WPKH still hides pubkey until spend. |
| **P2WPKH** (native SegWit) | After first spend | Like P2PKH. Hash-only locking; pubkey in witness on spend. |
| **P2TR** (Taproot) | At output creation | The output contains the 32-byte tweaked public key Q. Key-path spending verifies a Schnorr signature against Q; Q is a curve point, not a public-key hash. |

### The "harvest" problem

For Bitcoin, "harvest now, decrypt later" plays out differently than TLS. Once a pubkey is on chain (because the user spent from that address), the protection is **single-use** — anyone watching mempool and chain has it forever. Even if the user moves coins to a fresh address afterwards, the original pubkey-to-amount linkage is permanent in the historical chain.

UTXO categorization for the migration discussion:

- **Already exposed**: P2PK, all reused addresses with prior spends, all addresses with leaked pubkeys (e.g., signed messages, PSBTs shared publicly).
- **Hash-protected for now**: hash-only addresses (P2PKH, P2WPKH) that have never been spent from.
- **Cold-storage-only**: hash-protected and never reused. The most defensible position pre-migration.

Unspent Taproot outputs belong in the exposed-public-key category. Never spending from a Taproot address does not hide its output key.

## The proposals

### BIP-360 — Pay-to-Merkle-Root (P2MR)

**Hunter Beast, Ethan Heilman, and Isabel Foxen Duke**, *BIP-360: Pay-to-Merkle-Root*, draft on `github.com/bitcoin/bips/blob/master/bip-0360.mediawiki` (assigned December 18, 2024; version 0.11.0 checked April 2026).

BIP-360 is narrower than the older "Pay-to-Quantum-Resistant-Hash" framing. The current draft introduces a new output type that keeps Taproot-style script trees but removes the key-path spend:

```
P2MR script: OP_PUSHNUM_3 <32-byte Merkle root>
```

That matters because Taproot outputs expose a long-lived x-only public key in the output itself. P2MR commits only to a script tree root. It protects against **long-exposure attacks** on public keys already visible on-chain, while preserving tapscript programmability.

Important limitation: P2MR **does not add post-quantum signatures**. Spending still uses scripts available to Bitcoin consensus. The draft explicitly treats protection against **short-exposure attacks** — where a CRQC attacks a public key revealed in the mempool before confirmation — as a separate proposal track that likely requires post-quantum signature support.

### PQ signature migration path

The likely signature candidates remain:

- **SLH-DSA** (FIPS 205) — conservative, very large signatures.
- **ML-DSA** (FIPS 204) — general-purpose, large but practical in many protocols.
- **FN-DSA / Falcon** (draft FIPS 206) — small signatures, attractive for block-space economics, harder to implement safely.

As of April 2026, no Bitcoin consensus proposal has selected one of these schemes for activation.

### Hybrid signatures inside witness data

A second proposal direction: keep classical Schnorr as the primary signature and add a PQ signature in witness data. The script would require both to be valid.

Pros: smooth migration, backward-compatible with existing infrastructure.
Cons: doubles signature size; doesn't actually protect existing addresses; just adds PQ to new addresses.

### Lamport / hash-based signatures via script

Some early proposals (Hülsing 2020, Anonymous Bitcoin BIP discussions) explored encoding hash-based one-time signatures inside existing OP_CHECKSIG semantics. These are mostly research proposals; they don't fit cleanly into Bitcoin script and have been overtaken by BIP-360.

### Commit-reveal migration

A migration scheme where users commit to a PQ-pubkey-hash early, then later reveal the PQ pubkey in a spend. This protects against the window between "CRQC arrives" and "user actually moves their coins" — assuming the user committed before the CRQC arrived.

This is the "early reservation" pattern: even before a PQ-signature output is consensus-active, users could publish PQ-pubkey commitments via OP_RETURN or signed messages, so that when migration becomes possible, they have prior evidence of ownership. This is not a deployed standard.

## Soft fork vs hard fork

### Soft fork (BIP-360 / P2MR path)

P2MR is a new SegWit version. Old nodes see it as "anyone can spend" and don't enforce the new rules. New nodes enforce the P2MR script-tree validation. As long as the majority of mining hash power upgrades, the soft fork holds.

Pros:
- No coordinated chain split.
- Backward-compatible with old nodes (they relay but don't validate).
- Same upgrade pattern as Taproot.

Cons:
- Old nodes don't actually verify the new rules.
- Doesn't solve short-exposure attacks during spending.
- Doesn't protect already-exposed UTXOs (P2PK, reused) unless owners migrate before a CRQC can exploit them.
- Anyone can in principle race a soft-forked transaction with a non-conforming spend (though current relay rules block this).

### Hard fork (deprecate vulnerable signatures)

A more aggressive proposal: at a flag day, deprecate ECDSA and Schnorr signature acceptance entirely. All UTXOs must be migrated to PQ addresses by date X.

Pros:
- Forces migration of vulnerable UTXOs.
- Simplifies long-term consensus rules.
- Cuts off the "exposed pubkey" attack surface.

Cons:
- Effectively burns un-migrated coins (hardline view: "if you don't migrate, you lose").
- Politically toxic. Touching dormant Satoshi-era P2PK coins is the third rail of Bitcoin governance.
- Requires near-universal coordination.

### Hybrid path

Most proposals split the difference:

1. Soft-fork low-risk quantum-hardening steps such as P2MR so users can reduce long-exposure risk.
2. Add a separate PQ-signature output once the scheme and block-space economics are agreed.
3. Run for years with both signature systems active.
4. Eventually hard-fork to deprecate ECDSA / Schnorr — but only after CRQC threat is imminent and coordination is feasible.

## Block-space economics

PQ signatures are **bigger than current signatures**, and Bitcoin's block weight budget is fixed. A typical P2WPKH spend signature is ~71 bytes. PQ replacements:

| Scheme | Signature | Public key | Total witness ~ |
|--------|-----------|-----------|-----------------|
| Current Schnorr | 64 B | 32 B | ~96 B |
| **FN-DSA-512 (Falcon)** | **~666 B** | **897 B** | **~1.5 KB** |
| **ML-DSA-44** | **2,420 B** | **1,312 B** | **~3.7 KB** |
| **SLH-DSA-SHA2-128s** | **7,856 B** | **32 B** | **~7.9 KB** |
| **SLH-DSA-SHA2-128f** | **17,088 B** | **32 B** | **~17 KB** |

A block today can hold ~3,000-4,000 typical transactions. With ML-DSA-44 signatures, that drops to ~250-400 transactions per block. With Falcon, perhaps ~600-1,000.

This is why **Falcon is attractive** for Bitcoin despite its implementation difficulty: the block-space cost is bearable.

The economic implications:

- Fees rise. Less throughput per block means higher per-transaction fee.
- Lightning becomes more important. Most user activity moves to L2.
- Single-sig PQ outputs may become rare cold-storage operations; multisig and L2 channels carry routine activity.
- Compact-signature schemes (Falcon, future signature aggregation) get prioritized.

## Cryptographer positions

Public statements from Bitcoin core developers and cryptographers (paraphrased; sources cited below):

- **Pieter Wuille** has noted (Bitcoin StackExchange, X posts 2024-2025) that PQ migration is technically tractable but politically and economically delicate. Conservative on hard fork; supportive of opt-in migration paths.
- **Adam Back** has written that the threat is real but not immediate, and that planning should start now without urgency. Has discussed hash-based signatures (LMS / SLH-DSA) as the conservative anchor and Falcon as the practical target.
- **Tim Ruffing** has co-authored work on Schnorr signatures and has commented on PQ Schnorr-replacement schemes (e.g., MuSig-PQ). Active in IETF PQ TLS work.
- **Hunter Beast** is the active driver of BIP-360.
- **Jameson Lopp** has written on quantum threat timelines (`blog.lopp.net`) — broadly: real threat, multi-year migration window, plan now.

There is **no consensus** on:
- Which PQ signature(s) to support (Falcon vs ML-DSA vs SLH-DSA vs all three).
- Soft fork timing.
- Hard-fork deprecation date.
- Treatment of Satoshi-era coins.

## Honest status (early 2026)

- **BIP-360**: still a draft. Number assigned, current text is P2MR rather than a PQ-signature output. No reference implementation merged into Bitcoin Core.
- **No consensus on activation timeline**. Discussion in the bitcoin-dev mailing list is pre-consensus. Most informed observers estimate **5-15 years** for a complete migration if started in earnest now.
- **No CRQC yet**. The largest demonstrated quantum factoring is small (under 25-bit RSA-equivalents). Expert estimates for CRQC: roughly 2030-2040, with wide error bars.
- **Wallets**: no production wallet supports PQ Bitcoin signatures as of early 2026. Sparrow, Trezor, Ledger, Coldcard all on classical only.
- **Lightning**: no PQ Lightning proposals at the protocol level. LN is even more pubkey-exposed than on-chain because channel announcements broadcast pubkeys.

The honest position: **Bitcoin's quantum threat is real but deferred, and the migration path is being designed without urgency.** If you hold significant BTC long-term:

- Use hash-protected addresses (P2PKH, P2WPKH).
- **Don't reuse addresses.**
- Avoid posting pubkeys (signed messages, public PSBTs).
- Move coins to fresh addresses after spends to "re-hide" the pubkey.
- Track BIP-360 and separate PQ-signature proposals; be ready to migrate when activation lands.

This buys time, not safety. P2MR would reduce long-exposure risk for new script-tree outputs; full safety against short-exposure attacks requires a future PQ-signature path and coins actually migrated to it.

## Migration recipe (for a holder)

1. Audit your UTXOs by exposure category. Identify any P2PK or reused-address UTXOs. These are first-priority migration targets.
2. Don't reuse addresses; for cold storage, use a fresh address per deposit.
3. Track BIP-360 P2MR status (`github.com/bitcoin/bips/blob/master/bip-0360.mediawiki`) and any separate PQ-signature BIPs.
4. When a quantum-hardening output activates, migrate from hash-protected addresses to the new output type if your wallet and hardware stack support it.
5. When PQ signatures exist: consider a policy that requires at least one PQ signer for very large holdings.

## Trade-offs

### Strengths of the BIP-360 path

- Soft-fork compatible with existing nodes.
- Small, conservative first step: removes Taproot's key-path public-key exposure for new script-tree outputs.
- Hash-protected addresses give a transition runway.
- No need to touch existing UTXOs unless their owner wants to migrate.

### Limitations

- Doesn't protect already-exposed UTXOs (P2PK and reused addresses).
- Does not add PQ signatures or protect the short mempool exposure window.
- A later PQ-signature path still faces block-space pressure from larger signatures.
- Requires wallet, hardware-wallet, and L2 ecosystem support before ordinary users can benefit.
- No clear answer for Satoshi-era P2PK coins (~1M+ BTC).
- Hard-fork-to-deprecate option is politically untouchable for now.

## Attack surface

| Attack | Mitigation |
|--------|-----------|
| CRQC steals from exposed pubkeys | Pre-emptive migration to hash-protected outputs; P2MR for future Taproot-like script trees; eventual PQ signatures |
| CRQC front-runs an in-flight transaction | Confirmation depth only helps against weak attackers; eventual PQ signatures are needed |
| Adversary records pubkeys for future quantum attack | Don't reuse addresses; minimize pubkey publication |
| Wallet implementation bug in PQ signing | Multiple independent implementations; hybrid signatures during transition |
| Soft-fork race condition during activation | Standard soft-fork activation pattern (BIP-9 / BIP-8 style) |

## Comparison with other chains

| Chain | PQ approach | Status |
|-------|-------------|--------|
| **Bitcoin** | BIP-360 P2MR for long-exposure hardening; PQ signatures remain a separate proposal track | Draft; no activation timeline |
| **Ethereum** | Account abstraction enables PQ via signature schemes; STARK-based zk-rollups have natural PQ paths | Research; multi-year roadmap |
| **Monero** | Confidential signatures use Schnorr-like; PQ research ongoing | Pre-design |
| **Zcash** | Sapling/Orchard rely on BLS12-381 pairings; full PQ migration would be a redesign | Long-term research |
| **Algorand** | Falcon supported in protocol since 2022 | Production |
| **QRL (Quantum Resistant Ledger)** | XMSS-based from genesis | Production niche |
| **IOTA** | Used WOTS+ historically; moved to Ed25519 in v1.5 (irony noted) | Mixed history |

Algorand's early Falcon adoption is the only major PQ deployment in production at L1. Bitcoin's caution is partly due to scale (more value at stake than any other chain) and partly due to consensus coordination cost.

## Primary sources

- [BIP 341: Taproot output keys and key-path validation](https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki)

- Beast, Heilman, Foxen Duke, *BIP-360: Pay-to-Merkle-Root (P2MR)*, draft assigned 2024-12-18; version 0.11.0 checked April 2026. `github.com/bitcoin/bips/blob/master/bip-0360.mediawiki`.
- NIST FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA), FIPS 206 IPD (FN-DSA / Falcon).
- Shor, *Algorithms for Quantum Computation: Discrete Logarithms and Factoring*, FOCS 1994.
- bitcoin-dev mailing list, *Quantum-Resistant Signatures* threads, 2023-2025. `lists.linuxfoundation.org/pipermail/bitcoin-dev/`.
- Wuille, Nick, Ruffing, *BIP-340: Schnorr Signatures for secp256k1*, 2020.
- Aggarwal, Brennen, Lee, Santha, Tomamichel, *Quantum attacks on Bitcoin, and how to protect against them*, Ledger 2018. `arxiv.org/abs/1710.10377`.
- Lopp, *Bitcoin and Quantum Computing*, `blog.lopp.net`, ongoing.
- Bitcoin StackExchange: Pieter Wuille on PQ migration. `bitcoin.stackexchange.com`.
- BIP-340 (Schnorr): `github.com/bitcoin/bips/blob/master/bip-0340.mediawiki`.
