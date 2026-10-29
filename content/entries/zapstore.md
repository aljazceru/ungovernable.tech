---
title: "Zapstore: An Android App Store on Nostr"
slug: zapstore
type: deep-dive
pillars: [apps, endpoint]
readiness: usable
description: "Zapstore is an open Android app store where developers publish signed releases over Nostr and the app checks each APK's hash and signing key before install."
dek: "No review queue and no listing fee: developers publish releases as signed Nostr events, the app checks each APK against them before installing, and users decide which publishers and catalogs to trust."
updated: 2026-10-29
created: 2026-10-29
origin: original
related: [compare-android-app-stores, sovereign-applications, verifying-software, grapheneos, nostr-protocol, nostr-web-of-trust, napplet]
aliases: ["Zapstore", "zap.store", "zsp"]
tags: ["zapstore", "android", "app-store", "nostr", "apk", "distribution", "deep-dive"]
---

Zapstore is an open-source (MIT) Android app store whose listings, releases and publisher identities are Nostr events instead of rows in a company database. A developer publishes directly, without approval or listing fees, and users install from their phones with signature and hash checks. Its site lists OpenSats and the Human Rights Foundation among its donors and reports more than 4,000 active users.

## How it works

**Publishing.** Developers use [zsp](https://github.com/zapstore/zsp), an MIT-licensed command-line tool. It fetches an APK from GitHub, GitLab, Codeberg, F-Droid, a web page or a local file, extracts the package name, version and signing-certificate fingerprint, enriches the listing from sources such as Fastlane metadata, uploads icons and screenshots to [Blossom](/kb/blossom/) servers, signs the application, release and asset events with the developer's Nostr key (or a NIP-46 remote signer), and publishes them to relays.

**Linking two keys.** Android apps are signed with the developer's Android signing certificate; Zapstore events are signed with a Nostr key. zsp's **C1 proof** binds the two, proving that the Android certificate belongs to the Nostr identity. The zsp documentation tells developers to do this step by hand and never to give an agent their keystore, password or `nsec`.

**Installing.** The Android app syncs listings and publisher identities from relays. Before installing, it verifies the downloaded APK's file hash and signing certificate against the signed release. Users have reported installs refused because hashes did not match, which is the check working.

**Trust and curation.** Curated app lists ("stacks") and optional social features sit on top of Nostr profiles. The site describes catalogs that anyone can run and that users choose between; its roadmap still lists opening catalogs to communities as in progress, along with installable web apps and an iOS app.

## What it protects against

- **Store takedowns.** No company can remove an app from Nostr. Releases live on relays and files on servers the developer chooses.
- **Tampering between developer and phone.** A mirror or download server that swaps the APK fails the hash and certificate check.
- **Impersonation.** A release signed by a different key or certificate than the publisher's does not pass as theirs.
- **Accounts and tracking.** Browsing and installing do not require an account. A profile is optional.

## What it trusts, and the limits

- **The developer, not the code.** A valid signature proves who published an APK, not that it is safe. There is no review queue, so a malicious developer can publish malware under their own key. Choose publishers as carefully as you would choose apps.
- **Builds are not reproduced.** Zapstore distributes the developer's own APK. Unlike F-Droid, it does not rebuild from source, so "matches the developer's release" is the guarantee, not "matches the source code". See [Verify software before installing it](/kb/verifying-software/).
- **Key compromise.** Whoever steals a developer's Nostr key and Android signing key can ship a convincing update.
- **Relays and file hosts.** They can withhold data, and they see which listings you request.
- **The installer permission.** Like any store, Zapstore needs Android's permission to install apps, so it is itself part of what you trust.
- **Android policy.** Google's developer-verification rules took effect on 30 September 2026 for certified devices in Brazil, Indonesia, Singapore and Thailand, initially for installs from seven large stores, and Google plans to extend them to all certified devices in 2027. How that affects independent stores is the open question for every option in [Android app sources compared](/kb/compare-android-app-stores/).

## Readiness

**Usable.** Zapstore has a stable Android 1.0 release, an active developer community and thousands of users. It is a practical way to get Nostr, Bitcoin and other freedom-tech apps straight from their developers. It is Android-only for now, and its trust model is "trust the publisher's key", which you have to apply yourself.

## Primary sources

- Zapstore: https://zapstore.dev/ · docs: https://zapstore.dev/docs
- Android app (MIT): https://github.com/zapstore/zapstore
- zsp publishing CLI (MIT): https://github.com/zapstore/zsp
- Google, Android developer verification: https://developer.android.com/developer-verification/guides
