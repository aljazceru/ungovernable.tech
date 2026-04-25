---
title: "Hardware Wallet Guide"
tags:
  - "hardware-wallet"
  - "self-custody"
  - "bitcoin"
  - "security"
  - "financial"
  - "deep-dive"
---
*Dedicated signing devices that keep private keys offline and approve transactions out-of-band — the practical foundation of self-custody.*

---

## What a Hardware Wallet Actually Does

A hardware wallet is a single-purpose computer with three jobs:

1. **Generate and store** a master seed offline.
2. **Display the transaction** to be signed (amounts, addresses, fees) on a trusted screen.
3. **Sign** with the seed-derived key only after the user confirms via physical button press.

The signed transaction goes back to the host computer, which broadcasts it. The seed never leaves the device. A compromised host computer cannot exfiltrate keys; it can at most try to display fake transaction details, which the user catches on the device's own screen.

### What it doesn't do

- It doesn't run wallet UI — that's on the host (Sparrow, Specter, BlueWallet, etc.).
- It doesn't connect to the internet directly (most don't).
- It doesn't protect against you signing a bad transaction if you don't read the screen.

---

## Threat Model

| Adversary | Defended? |
|-----------|-----------|
| Malware on host computer | **Yes** — keys never leave device; transaction confirmation on device screen |
| Remote attacker via internet | **Yes** — air-gapped or USB-only |
| Physical device theft (without PIN) | **Yes** — PIN with retry counter, factory wipe on N failures |
| Physical device theft (with PIN coercion) | **Partial** — passphrase / "duress wallet" feature |
| Supply-chain backdoor | **Partial** — open-source firmware verification, multi-vendor diversity |
| $5 wrench | **No** — physical coercion of user; mitigate with multisig + geographic distribution |
| Side-channel attack on the chip | **Varies** — Secure Element (SE) chips raise the bar; not a full defense |
| Lost device | Recovery via 12/24-word seed (BIP-39) on a new device |

---

## Architectural Variants

### Secure Element + MCU

Most consumer wallets (Ledger, Jade, BitBox02, Trezor Safe family) pair a general-purpose MCU with a tamper-resistant Secure Element (SE). The SE holds the seed; the MCU runs UI and USB stack.

**Pro:** Hardware-grade tamper resistance.
**Con:** SE firmware is typically closed-source (proprietary EAL5+ certified chips). Trust boundary is the chip vendor (NXP, STMicroelectronics, etc.).

### MCU-only (open silicon)

Trezor One/Model T, Foundation Passport (older), some experimental DIY designs.

**Pro:** Fully open hardware + firmware, fully reviewable.
**Con:** No SE means seed is in general-purpose flash; physical extraction attacks have demonstrated feasibility (Kraken Security Labs, 2020 Trezor One break).

### Air-gapped

QR-code or microSD-based transaction transport (Cobo Vault, Foundation Passport, Keystone, SeedSigner). Never plugs into a computer.

**Pro:** Eliminates entire USB attack surface.
**Con:** Slower UX; QR cameras add new attack surface (image-based malware).

### DIY / Open Hardware

SeedSigner — Raspberry Pi Zero + camera + screen, runs from a stateless live image, signs via QR. No persistent storage of keys. Fully reproducible.

---

## Comparison Snapshot (early 2026)

| Device | SE | Open Firmware | Air-gap | Multisig UX | Notes |
|--------|------|---------------|---------|-------------|-------|
| **Ledger Stax / Flex** | Yes (proprietary) | No | No | Good | Recall: Ledger Recover controversy 2023 |
| **Trezor Safe 5** | Yes (Optiga TPM) | Yes (firmware) | No | Good | Bitcoin-only firmware available |
| **Coldcard Mk4 / Q** | Yes (dual SE) | Yes | Yes (microSD) | Excellent | Bitcoin-only |
| **BitBox02** | Yes | Yes | No | Good | Swiss-made, BTC + multi |
| **Blockstream Jade** | No | Yes | Yes (QR) | Excellent | Native Liquid + Bitcoin |
| **Foundation Passport** | Yes (ATECC608) | Yes | Yes (microSD/QR) | Excellent | Bitcoin-only |
| **Keystone 3 Pro** | Yes (triple SE) | Yes | Yes (QR) | Good | Multi-coin including BTC |
| **SeedSigner** | No | Yes (DIY) | Yes (QR) | Good | Stateless; build it yourself |

---

## Operational Patterns

### Single-sig with passphrase

Standard 12/24-word seed + a 25th-word "passphrase" stored in the user's head or a separate location. The passphrase produces a different wallet entirely; without it, the seed reveals only a decoy ("plausible deniability").

### Multisig (k-of-n)

The strongest practical setup: 2-of-3 with three different vendors and three different backup locations. Compromising one vendor or one location is insufficient to spend.

```
Key 1: Coldcard at home (cosigner)
Key 2: BitBox02 at office (cosigner)
Key 3: Foundation Passport at remote location (cosigner / recovery)
```

Tools: Sparrow Wallet, Specter Desktop, Nunchuk, Liana.

### Inheritance & succession

Multisig with one cosigner held by a service (Casa, Unchained) or a trusted person, plus time-locked recovery (Liana, MIniscript-based) for "if you don't sign within 1 year, beneficiary can spend".

### Hot/Warm/Cold tiers

| Tier | Holds | Device |
|------|-------|--------|
| Hot | Daily spend (< 1 month expenses) | Phone wallet, Lightning |
| Warm | Monthly spend / dApp interactions | Hardware wallet, single-sig |
| Cold | Long-term savings | Multisig, distributed locations |

---

## Recurring Mistakes

- **Storing the seed digitally.** No photos, no cloud, no Notion. Pen + steel backup.
- **Using one vendor for multisig.** Defeats the diversity benefit.
- **Skipping the receive-address verification.** Always verify on the device screen.
- **Trusting the host wallet's PSBT.** Read the device's confirmation; the host can lie.
- **No test recovery.** Restore the seed on a fresh device to a *throwaway* wallet — confirm the seed actually works *before* funding.
- **Sending signing data through cloud sync.** Some wallet UIs sync PSBT through cloud; treat all cloud-touching workflows as compromised host.

---

## Steel Backups

Paper rots, burns, and is illegible after a flood. Steel plates (stamped, washer/screw, tile-based) survive fires up to ~1500°C and submersion. Notable products: Cryptosteel Capsule, Blockplate, SeedHammer, OneKey KeyTag.

For multisig, use **Shamir's Secret Sharing (SSSS)** sparingly — most cosigners are simpler. SSSS introduces additional implementation risk; standard BIP-39 words distributed geographically are usually safer.

---

## Lightning + Hardware Wallets

Lightning's online requirement conflicts with cold storage. Practical patterns:

- **Phoenix / Mutiny / Zeus** — non-custodial mobile LN; use as the *hot* tier.
- **Voltage / Umbrel + Coldcard** — node holds the channel state; Coldcard holds the recovery seed and signs forced closes.
- **PCC + LN** — emerging: phone signing with hardware-backed enclave (Apple Secure Enclave, StrongBox).

---

## Recent Developments (2024-2026)

- **Taproot multisig (FROST/MuSig2)** — k-of-n hardware-wallet multisig with a single Schnorr key on-chain. Better privacy and lower fees. Tooling landing in Sparrow, Liana 2024-2025.
- **Miniscript** — declarative spending policies; wallets like Liana use it for time-locked inheritance.
- **PSBT v2** — improved transaction format with better hardware-wallet UX.
- **Ledger Recover** — opt-in custodial seed backup launched 2023, controversial; users can verify it remains opt-in.
- **Reproducible builds** — increasingly the standard; Trezor, Coldcard, Jade, Passport publish bitwise-reproducible firmware builds.

---

## Related Files

- [Overview - Financial Sovereignty](/financial-sovereignty/overview-financial-sovereignty)
- [Lightning Network Deep Dive](/financial-sovereignty/lightning-network-deep-dive)
- [CoinJoin Implementation](/financial-sovereignty/coinjoin-implementation)
- [MOC - Threat Models](/meta/moc-threat-models)

---

## Primary Sources

- BIP-32 (HD wallets) — [github.com/bitcoin/bips/blob/master/bip-0032.mediawiki](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki)
- BIP-39 (mnemonic seed) — [github.com/bitcoin/bips/blob/master/bip-0039.mediawiki](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)
- BIP-174 (PSBT) — [github.com/bitcoin/bips/blob/master/bip-0174.mediawiki](https://github.com/bitcoin/bips/blob/master/bip-0174.mediawiki)
- Andreas Antonopoulos, *Mastering Bitcoin*, 3rd ed. — chapters on key derivation and signing.
- Coldcard, Trezor, Jade, Passport documentation.
- Kraken Security Labs, *Trezor Physical Extraction*, 2020.

