---
title: "Verify software before installing it"
slug: verifying-software
type: guide
pillars: ["endpoint", "cryptography"]
readiness: usable
description: "Check downloads with project signing keys, understand what checksums prove, and use reproducible builds without confusing them with a security audit."
dek: "Confirm who signed the bytes you will run, then ask whether those bytes can be rebuilt from the published source."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: ["grapheneos", "tails-qubes-whonix", "using-tor-safely", "hardware-supply-chain-trust"]
level: intermediate
---

## Summary

A checksum compares bytes. A digital signature additionally binds signed bytes to a signing key. Reproducible builds address a further question: whether the stated source, environment and instructions produce the same artifact. These checks answer different questions, and none establishes that the program is harmless.

## Before downloading

Use the project's official installation documentation to identify the supported release, platform and verification method. Record the expected signing-key identity through a channel you already trust. A checksum or key supplied only by an untrusted mirror gives that mirror too much control over the check.

## Verify the release

1. **Download the artifact and its verification material.** Keep the exact filename and matching signature together. Tor Browser documents detached OpenPGP `.asc` signatures for its download files.
2. **Authenticate the expected signer.** Follow the project's published key-discovery and fingerprint instructions. A tool reporting a valid signature under an unexpected key is not a successful publisher check.
3. **Run the documented verifier.** Follow the current platform instructions, including the actual files you downloaded. Avoid copying example release numbers from an old guide.
4. **Stop on a mismatch.** Check that you selected the correct release and platform, then obtain fresh files through the official route. Do not bypass a failed check to finish installation.
5. **Preserve the security checks after installation.** Update through the project's supported mechanism and review key-change instructions when they occur.

## Project-specific workflows

**Tor Browser** publishes GnuPG instructions and explains how to verify its detached signatures. **Tails** offers browser-based download verification and also publishes checksums and OpenPGP material; use the method its current installation page recommends for you.

**GrapheneOS** documents signature verification in its command-line installation guide and a separate web installer. Its installation instructions also require relocking the bootloader to restore full verified boot. Download verification and verified boot protect different stages. Read [GrapheneOS](/guides/grapheneos/) before changing a phone's operating system.

## Reproducible builds

The Reproducible Builds definition requires the same specified artifacts from the same source, build environment and instructions. F-Droid documents rebuilding APKs and comparing them using upstream signature copying; check the individual app's build metadata rather than assuming every listed app has a verified reproducible build.

## Trust model / threat model

This workflow checks provenance and, where available, correspondence between source and binaries. It still depends on the expected signing key, the verification tool and a trustworthy device performing the check. For the wider chain, read [hardware supply-chain trust](/kb/hardware-supply-chain-trust/).

## Readiness and limits

**Usable.** The linked projects publish working verification procedures. A successful check does not replace reviewing application permissions, updating software or assessing whether the program belongs in your threat model. See [Tails, Qubes and Whonix](/guides/tails-qubes-whonix/) for isolation choices.

## Primary sources

- [Tor Browser signature verification](https://support.torproject.org/tbb/how-to-verify-signature/)
- [Tails download verification](https://tails.net/install/download/index.en.html)
- [GrapheneOS command-line installation and signatures](https://grapheneos.org/install/cli)
- [GrapheneOS web installation and verified boot](https://grapheneos.org/install/web)
- [Reproducible Builds definition](https://reproducible-builds.org/docs/definition/)
- [F-Droid reproducible builds and APK signatures](https://f-droid.org/docs/Reproducible_Builds/)
- [RFC 9580: OpenPGP signatures and verification](https://www.rfc-editor.org/rfc/rfc9580.html)
