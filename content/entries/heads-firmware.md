---
title: "Heads Firmware"
slug: heads-firmware
type: deep-dive
pillars: [endpoint]
readiness: usable
description: "Heads combines open boot firmware with integrity checks. Understand TPM measurements, TOTP and HOTP verification, hardware support and limits."
dek: "A boot process that lets you check for changes before trusting the machine with a secret."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [hardware-supply-chain-trust, tails-qubes-whonix, encrypting-files-and-backups, passkeys-and-security-keys]
tags: [firmware, coreboot, measured-boot, tpm]
---

## Summary

[Heads](https://osresearch.net/) is boot firmware with integrity checks for supported hardware. Its typical x86 configuration combines coreboot with a Linux kernel and initial filesystem as the payload. On configurations with TPM measured boot enabled, it records firmware measurements and uses sealed secrets to help you detect changes before trusting the operating system.

This addresses the boot and physical-tampering part of [hardware and firmware supply-chain trust](/kb/hardware-supply-chain-trust/). It does not replace operating-system updates or isolation of untrusted applications.

## How it works

In the documented TPM configuration, coreboot measures boot stages and the Heads payload into the TPM. A secret sealed to expected measurements can be recovered only when the measurements match. Heads uses that secret for a check you can verify independently:

- **TOTP:** compare the time-based code displayed by Heads with the code on your separately enrolled authenticator.
- **HOTP:** Heads sends a counter-based code to a compatible USB token. The token verifies it and signals success or failure. The project calls this reverse HOTP because the computer generates the code and the token checks it.

Heads also verifies signed files in `/boot`. Supported configurations can combine those checks with TPM-sealed disk-unlock material. The [security model](https://github.com/linuxboot/heads/blob/master/doc/security-model.md) describes how these pieces fit together and where they depend on board configuration.

## Hardware and keys

Check the [hardware compatibility list](https://osresearch.net/Hardware-Compatibility/) and the exact board's [prerequisites](https://osresearch.net/Prerequisites). Listed platforms include specific ThinkPads, Librem machines, NitroPads and NovaCustom laptops; a brand name alone is not a compatibility guarantee. Some installations require an external flash programmer and a backup of the original firmware.

The token requirements are distinct from [passkeys and FIDO security keys](/kb/passkeys-and-security-keys/). Heads uses OpenPGP for signing boot contents, and HOTP verification requires the specialized compatible protocol. The prerequisites list Librem Key and supported Nitrokey models for this role. A token supporting only FIDO2/U2F will not do it.

## Trust model

You trust the initial firmware and enrollment, the TPM where used, the token or separate TOTP device, and the underlying hardware. A matching code tells you something about the enrolled boot state. It is not proof that every component of the computer is benign.

An unexpected failure calls for investigation. Re-sealing a secret or accepting new boot files changes the trusted baseline; do that only after establishing why the state changed. Keep the verifier under separate physical control so it remains a meaningful independent check.

## Readiness

**Usable on supported configurations, for people prepared to maintain the boot checks.** The project publishes installation instructions and board support details. This is a specialist firmware choice: confirm the exact model, enabled protections and recovery procedure before flashing.

## Limits

**TPM protection is not universal across Heads boards.** The current security documentation distinguishes measured-boot configurations, configurations where measurement is disabled, and boards without TPM support. The latter can use a ROM-hash HOTP mechanism, which is not the same guarantee as a TPM-sealed secret. Check the documented protection status for your board.

Boot checks do not monitor all software after startup or defeat arbitrary hardware replacement. The [threat model](https://osresearch.net/Heads-threat-model/) also discusses physical attacks and the assumptions beneath measurement. Use Heads as one part of a plan that includes [disk encryption](/guides/encrypting-files-and-backups/) and [operating-system compartmentalization](/guides/tails-qubes-whonix/).

## Primary sources

- [Heads project](https://osresearch.net/).
- [Heads security model in the canonical repository](https://github.com/linuxboot/heads/blob/master/doc/security-model.md).
- [Heads hardware compatibility list](https://osresearch.net/Hardware-Compatibility/).
- [Heads installation and token prerequisites](https://osresearch.net/Prerequisites).
- [Heads threat model and per-board protection status](https://osresearch.net/Heads-threat-model/).
