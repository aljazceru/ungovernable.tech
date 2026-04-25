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
*Dedicated signing devices that keep private keys offline and approve transactions out-of-band. The practical foundation of self-custody.*

---

## What a hardware wallet does

A hardware wallet is a single-purpose computer with three jobs:

1. Generate and store a master seed offline.
2. Display the transaction (amounts, addresses, fees) on a trusted screen.
3. Sign with the seed-derived key only after the user confirms via a physical button.

The signed transaction goes back to the host computer, which broadcasts it. The seed never leaves the device. A compromised host cannot exfiltrate keys; at most it can try to display fake transaction details, which the user catches on the device screen.

### What it doesn't do

- It doesn't run the wallet UI. That lives on the host (Sparrow, Specter, BlueWallet, etc.).
- It usually doesn't connect to the internet directly.
- It doesn't protect against you signing a bad transaction if you don't read the screen.

---

## Threat model

| Adversary | Defended? |
|-----------|-----------|
| Malware on host computer | Yes. Keys never leave the device; transaction confirmation is on the device screen |
| Remote attacker via internet | Yes. Air-gapped or USB-only |
| Physical theft (without PIN) | Yes. PIN with retry counter, factory wipe on N failures |
| Physical theft (with PIN coercion) | Partial. Passphrase or "duress wallet" feature |
| Supply-chain backdoor | Partial. Open-source firmware verification, multi-vendor diversity |
| $5 wrench | No. Physical coercion of the user; mitigate with multisig + geographic distribution |
| Side-channel attack on the chip | Varies. Secure Element (SE) chips raise the bar; not a full defense |
| Lost device | Recovery via 12/24-word seed (BIP-39) on a new device |

---

## Architectural variants

### Secure Element + MCU

Most consumer wallets (Ledger, Jade, BitBox02, Trezor Safe family) pair a general-purpose MCU with a tamper-resistant Secure Element (SE). The SE holds the seed; the MCU runs the UI and USB stack.

Pro: hardware-grade tamper resistance.
Con: SE firmware is typically closed-source (proprietary EAL5+ certified chips). The trust boundary is the chip vendor (NXP, STMicroelectronics, etc.).

### MCU-only (open silicon)

Trezor One/Model T, Foundation Passport (older), some experimental DIY designs.

Pro: fully open hardware and firmware, fully reviewable.
Con: no SE means the seed sits in general-purpose flash; physical extraction attacks have demonstrated feasibility (Kraken Security Labs, 2020 Trezor One break).

### Air-gapped

QR-code or microSD-based transaction transport (Cobo Vault, Foundation Passport, Keystone, SeedSigner). Never plugs into a computer.

Pro: removes the entire USB attack surface.
Con: slower UX; QR cameras add a new attack surface (image-based malware).

### DIY / open hardware

SeedSigner: Raspberry Pi Zero plus camera and screen, runs from a stateless live image, signs via QR. No persistent storage of keys. Fully reproducible.

---

## Comparison snapshot (early 2026)

| Device | SE | Open firmware | Air-gap | Multisig UX | Notes |
|--------|------|---------------|---------|-------------|-------|
| Ledger Stax / Flex | Yes (proprietary) | No | No | Good | See Ledger Recover controversy 2023 |
| Trezor Safe 5 | Yes (Infineon Optiga Trust M, EAL6+ SE) | Yes (firmware) | No | Good | Bitcoin-only firmware available |
| Coldcard Mk4 / Q | Yes (dual SE) | Yes | Yes (microSD) | Excellent | Bitcoin-only |
| BitBox02 | Yes | Yes | No | Good | Swiss-made, BTC + multi |
| Blockstream Jade | No | Yes | Yes (QR) | Excellent | Native Liquid + Bitcoin |
| Foundation Passport | Yes (ATECC608) | Yes | Yes (microSD/QR) | Excellent | Bitcoin-only |
| Keystone 3 Pro | Yes (triple SE) | Yes | Yes (QR) | Good | Multi-coin including BTC |
| SeedSigner | No | Yes (DIY) | Yes (QR) | Good | Stateless; build it yourself |

---

## Operational patterns

### Single-sig with passphrase

Standard 12/24-word seed plus a 25th-word "passphrase" stored in the user's head or in a separate location. The passphrase produces a different wallet entirely; without it, the seed reveals only a decoy ("plausible deniability").

### Multisig (k-of-n)

The strongest practical setup: 2-of-3 with three different vendors and three different backup locations. Compromising one vendor or one location is not enough to spend.

```
Key 1: Coldcard at home (cosigner)
Key 2: BitBox02 at office (cosigner)
Key 3: Foundation Passport at remote location (cosigner / recovery)
```

Tools: Sparrow Wallet, Specter Desktop, Nunchuk, Liana.

### Inheritance and succession

Multisig with one cosigner held by a service (Casa, Unchained) or a trusted person, plus time-locked recovery (Liana, Miniscript-based) for "if you don't sign within 1 year, the beneficiary can spend".

### Hot/warm/cold tiers

| Tier | Holds | Device |
|------|-------|--------|
| Hot | Daily spend (< 1 month expenses) | Phone wallet, Lightning |
| Warm | Monthly spend / dApp interactions | Hardware wallet, single-sig |
| Cold | Long-term savings | Multisig, distributed locations |

---

## Recurring mistakes

- Storing the seed digitally. No photos, no cloud, no Notion. Pen and steel backup only.
- Using one vendor for multisig. That defeats the diversity benefit.
- Skipping receive-address verification. Always verify on the device screen.
- Trusting the host wallet's PSBT. Read the device's confirmation; the host can lie.
- No test recovery. Restore the seed on a fresh device to a *throwaway* wallet to confirm the seed actually works *before* funding.
- Sending signing data through cloud sync. Some wallet UIs sync PSBT through cloud; treat all cloud-touching workflows as a compromised host.

---

## Steel backups

Paper rots, burns, and is unreadable after a flood. Steel plates (stamped, washer/screw, tile-based) survive fires up to ~1500°C and submersion. Notable products: Cryptosteel Capsule, Blockplate, SeedHammer, OneKey KeyTag.

For multisig, use Shamir's Secret Sharing (SSSS) sparingly. Multiple cosigners are usually simpler. SSSS adds implementation risk; standard BIP-39 words distributed geographically are usually safer.

---

## Lightning + hardware wallets

Lightning's online requirement conflicts with cold storage. Practical patterns:

- Phoenix / Mutiny / Zeus: non-custodial mobile LN; use as the *hot* tier.
- Voltage / Umbrel + Coldcard: the node holds channel state; Coldcard holds the recovery seed and signs forced closes.
- PCC + LN: emerging, with phone signing backed by a hardware enclave (Apple Secure Enclave, StrongBox).

---

## Recent developments (2024-2026)

- Taproot multisig (FROST/MuSig2): k-of-n hardware-wallet multisig with a single Schnorr key on-chain. Better privacy and lower fees. Tooling has been landing in Sparrow and Liana through 2024-2025.
- Miniscript: declarative spending policies; Liana uses it for time-locked inheritance.
- PSBT v2: improved transaction format with better hardware-wallet UX.
- Ledger Recover: opt-in custodial seed backup launched in 2023, controversial; users can verify it remains opt-in.
- Reproducible builds: increasingly the norm. Trezor, Coldcard, Jade, and Passport publish bitwise-reproducible firmware builds.

---

## Related Files

- [Overview - Financial Sovereignty](/financial-sovereignty)
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

