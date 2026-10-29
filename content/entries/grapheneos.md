---
title: "Hardening a Phone with GrapheneOS"
slug: grapheneos
type: guide
pillars: [endpoint]
readiness: battle-tested
description: "Why GrapheneOS is the strongest option for a private, hardened Android phone, how to install and verify it, and which settings matter most."
dek: "Your phone knows more about you than anyone. GrapheneOS is a hardened, de-Googled Android that keeps it working for you."
updated: 2026-10-25
created: 2026-10-17
origin: original
level: intermediate
time: "1 hour"
related: [threat-modeling, choosing-a-secure-messenger, apple-secure-enclave, tails-qubes-whonix, compare-android-app-stores, zapstore]
---

GrapheneOS is a free, open-source operating system based on the Android Open Source Project, focused on privacy and security hardening. It removes Google services from the core system, adds exploit mitigations and gives you finer control over what apps can access. For people whose threat model includes commercial spyware, device seizure or pervasive app tracking, it is the most widely recommended phone setup.

## Why it is different

- **Exploit mitigations.** A hardened memory allocator (hardened_malloc), stricter sandboxing and other changes make whole classes of memory-corruption exploits harder.
- **No Google services in the OS.** If you need Google Play apps, *sandboxed Google Play* installs Play services as ordinary apps with no special privileges, inside a profile you choose.
- **Extra permission controls.** A *Network* permission to cut an app off from the internet entirely; a *Sensors* permission; *Storage Scopes* and *Contact Scopes* to give an app only the files or contacts you pick.
- **Protection against device seizure.** Automatic reboot after a period without unlocking (returning the phone to its fully encrypted state), a *duress PIN or password* that wipes the device when entered, USB-C port controls to block data connections while locked, and a PIN scrambling option.
- **Profiles.** Separate user profiles act as compartments: a work profile, an activism profile, a profile for the apps that insist on Google Play.
- **Verified boot with your own trust anchor.** After installation the bootloader is re-locked, so the device verifies the OS on every boot. The *Auditor* app can use hardware attestation to check that the OS has not been tampered with.

## Which phones

GrapheneOS supports a specific list of Google Pixel phones, because they allow the bootloader to be re-locked with a custom OS and provide the hardware security features GrapheneOS relies on (including a secure element and timely firmware updates). Check the current list at <https://grapheneos.org/faq#supported-devices> before buying. Buying the phone with cash in a shop avoids linking it to your identity.

## Installation

The official **web installer** (<https://grapheneos.org/install/web>) works from a Chromium-based browser on any desktop OS; a command-line install is also documented.

1. Update the stock OS once, then enable *OEM unlocking* in developer options.
2. Boot to the bootloader and connect over USB.
3. Follow the web installer: unlock the bootloader, flash GrapheneOS, **re-lock the bootloader**. Re-locking is not optional; it is what gives you verified boot.
4. On first boot, disable OEM unlocking again.
5. Optionally verify with the *Auditor* app, using a second device.

Install only from grapheneos.org. Pre-installed "GrapheneOS phones" from third-party sellers require trusting the seller.

## Settings worth changing

- **Strong passphrase**, not a short PIN. Biometric unlock is convenient, but you can be compelled to provide a fingerprint; know how to switch to passcode-only quickly (lockdown from the power menu).
- **Auto-reboot** timer set short (for example, a few hours) if device seizure is part of your threat model.
- **Duress PIN** if coercion is a realistic risk. Understand that it wipes everything.
- **USB-C port** set to charging-only while locked.
- **Network permission** off for apps that do not need the internet.
- **Separate profiles** for identities that must not be linked.
- **Install apps** from sources you trust: the GrapheneOS App Store for its own apps, F-Droid or Accrescent for open-source apps, sandboxed Play Store only if needed.

## What it does not fix

GrapheneOS secures the device; it does not anonymise you. Your mobile carrier still sees the phone's location and identity through the SIM. Apps you install and accounts you log into still learn what you tell them. Combine it with a messenger that does not need your number ([Choosing a Secure Messenger](/guides/choosing-a-secure-messenger/)), Tor or a VPN, and careful compartmentalisation.

**If you use an iPhone,** Apple's *Lockdown Mode* is the closest equivalent: it disables many attack surfaces used by spyware at some cost in convenience.

If you suspect the phone is already compromised, start with [Responding to Suspected Device Compromise](/guides/suspected-device-compromise/) before reinstalling or changing evidence. For account credentials and recovery planning, see [Passkeys and Security Keys](/kb/passkeys-and-security-keys/).

## Sources

- GrapheneOS, *Features overview*: <https://grapheneos.org/features>
- GrapheneOS, *Usage guide* (sandboxed Google Play, profiles, duress, USB-C control): <https://grapheneos.org/usage>
- GrapheneOS, *FAQ* (supported devices): <https://grapheneos.org/faq>
- GrapheneOS, *Web installer*: <https://grapheneos.org/install/web>
- Apple, *About Lockdown Mode*: <https://support.apple.com/en-us/105120>

Continue with [Mobile location privacy](/kb/mobile-location-privacy/) and [Verify software before installing it](/guides/verifying-software/).
