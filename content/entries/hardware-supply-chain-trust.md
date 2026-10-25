---
title: "Hardware and Firmware Supply-Chain Trust"
slug: hardware-supply-chain-trust
type: explainer
pillars: [endpoint]
description: "Assess the hardware and firmware beneath your operating system, with measured boot, open firmware and explicit limits on what those checks establish."
dek: "Your software is only as trustworthy as the firmware under it and the silicon under that. This is how that trust is earned, checked, and sometimes broken."
updated: 2026-10-25
created: 2026-10-18
origin: original
related: [grapheneos, tails-qubes-whonix, remote-attestation, open-source-tees, encrypting-files-and-backups, threat-modeling, building-a-mesh]
---

Encryption, hardened operating systems and careful operational security all rest on an assumption that is rarely examined: that the machine running them does what its manufacturer says it does. Underneath your operating system sits firmware — the BIOS/UEFI on a laptop, the bootloader on a phone, the OS image on a router — and underneath that sits silicon with its own microcode and management engines. Each layer loads the next, so a compromise low in the stack defeats everything above it, including full-disk encryption and a perfectly audited application. This entry is about how much to trust those lower layers, and what makes that trust checkable rather than assumed.

## The threat: implants below the operating system

Firmware and hardware are attractive targets precisely because almost nobody inspects them. Real, documented cases:

- **LoJax** (2018) was the first UEFI rootkit found in the wild, writing itself into the SPI flash chip so it survived operating-system reinstalls and even disk replacement ([ESET analysis](https://www.welivesecurity.com/2018/09/27/lojax-first-uefi-rootkit-found-wild-courtesy-sednit-group/)).
- **Thunderstrike** (2015) showed an Apple laptop's boot ROM could be rewritten over a Thunderbolt port, installing a bootkit that could not be removed by normal means ([write-up](https://trmm.net/Thunderstrike/)).
- Consumer routers are a recurring weak point: embedded Linux firmware is rarely updated, often ships with memory-safety bugs, and sits directly on the network path where it can read or redirect traffic.

The common thread is persistence and invisibility. A supply-chain implant can be introduced at manufacture, in a malicious update, or by an attacker with brief physical access, and it operates beneath the layer most defences watch.

## Reproducible builds: proving the binary matches the source

Open source only helps if the binary you run was actually built from the source you can read. **[Reproducible builds](https://reproducible-builds.org/)** make compilation deterministic, so that anyone can rebuild a release and get a bit-for-bit identical artifact. When many independent builders agree on the same hash, a backdoor inserted into the official binary — but not the public source — becomes detectable. This is the single most important defence against a compromised build or distribution server, and projects from Tor to GrapheneOS to Debian treat it as a baseline.

## Verified boot and measured boot

Two related mechanisms let a device reason about its own integrity at startup:

| | Verified boot | Measured boot |
|---|---|---|
| Question it answers | "Is each stage signed by a key I trust?" | "What exactly booted?" |
| Mechanism | Each stage checks the next against a public key before executing it | Each stage hashes the next into a tamper-evident log (a TPM's PCRs) before executing it |
| On mismatch | Refuses to boot, or boots a recovery path | Boots anyway, but the measurement differs, so secrets stay sealed |
| Example | [Android Verified Boot](https://source.android.com/docs/security/features/verifiedboot) | TPM-sealed disk keys; [remote attestation](/kb/remote-attestation/) |

Verified boot stops unauthorized code from running. Measured boot does not stop it, but it records it, so a key sealed to a known-good measurement will not unseal on a tampered device, and a remote verifier can tell the difference. The two combine: a phone like [GrapheneOS](/guides/grapheneos/) uses verified boot with a user-controllable key, while server and confidential-computing stacks lean on measurement and [attestation](/kb/remote-attestation/).

## Open firmware: moving the trusted root into the open

The firmware itself can be free software you can read, build reproducibly and in some cases re-flash:

- **[coreboot](https://www.coreboot.org/)** replaces the proprietary BIOS/UEFI on supported machines with a minimal open-source payload loader.
- **[Heads](https://osresearch.net/)** builds on coreboot to turn the boot firmware into a tamper-evident root of trust, using a TPM and a hardware token so the laptop can prove to *you* that its firmware is unchanged before you type a password.
- **[OpenWrt](https://openwrt.org/)** replaces vendor router firmware with a maintained, auditable Linux distribution, which is often the only way to keep a home router patched and free of vendor backdoors.
- **[OpenTitan](https://opentitan.org/)** and **[Trusted Firmware](https://www.trustedfirmware.org/)** push the same idea into silicon: an open-source hardware root of trust and open reference firmware for Arm secure worlds.

These do not eliminate trust — you still trust the silicon vendor, and much low-level code remains closed — but they shrink the opaque surface and make the parts that matter inspectable.

## What it trusts, and the limits

For board-specific boot checks and token requirements, see [Heads Firmware](/kb/heads-firmware/). For router compatibility, packages and upgrades, see [OpenWrt](/kb/openwrt/).

No consumer device is trustworthy "all the way down". Even with open firmware you typically still trust: the CPU microcode and any management engine (Intel ME, AMD PSP), the baseband on a phone, and the fab that made the chip. Hardware attacks with physical access — chip decapping, flash readback, cold-boot and side-channel attacks — remain possible against a well-resourced adversary. Guidance on how to reason about which of these actually apply to you is in [threat modeling](/guides/threat-modeling/).

Practical takeaways:

- Prefer devices with **user-controllable verified boot** and official **reproducible builds**.
- Replace unmaintained vendor firmware (routers especially) with **open, patched** firmware.
- Treat **brief physical access** as a real compromise for high-risk work; a measured-boot device with a hardware token makes tampering detectable.
- Keep secrets **sealed to measurements** or on a separate [hardware token](/kb/hardware-wallets/) rather than trusting the host blindly.

Continue with [Verify software before installing it](/guides/verifying-software/).
