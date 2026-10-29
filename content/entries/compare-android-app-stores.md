---
title: "Android App Sources Compared: F-Droid, Accrescent, Obtainium, Zapstore"
slug: compare-android-app-stores
type: comparison
pillars: [apps, endpoint]
readiness: usable
description: "How F-Droid, Accrescent, Obtainium, Zapstore and Google Play differ in who signs your apps, what gets verified and who can remove an app."
dek: "Every app source answers the same questions differently: who builds the APK, who holds the signing key, what the installer checks, and who can make an app disappear."
updated: 2026-10-29
created: 2026-10-29
origin: original
related: [zapstore, verifying-software, grapheneos, sovereign-applications, hardware-supply-chain-trust, threat-modeling]
aliases: ["Android app stores", "F-Droid vs Accrescent", "Obtainium", "Accrescent", "F-Droid"]
tags: ["android", "app-store", "f-droid", "accrescent", "obtainium", "zapstore", "reproducible-builds", "comparison"]
---

## Summary

On Android you can choose where your apps come from, and the choice decides whom you trust. The important differences are not the catalogue size. They are **who builds the APK**, **who holds the signing key**, **what the installer verifies**, and **who can remove an app**. Android itself adds one universal protection: an update must be signed with the same key as the installed app, so the first install is the moment that matters most.

## At a glance

| | Who builds the APK | Who signs it | What is checked | Who can remove an app | Account |
|---|---|---|---|---|---|
| [F-Droid](https://f-droid.org/) | F-Droid builds from source | F-Droid's key, or the developer's key when F-Droid reproduces the developer's build exactly | Free-software review; reproducible builds for many apps | F-Droid maintainers (others can run repositories) | No |
| [Accrescent](https://accrescent.app/) | The developer | The developer; no remote signing | Signing key pinned on first install; signed repository metadata | Accrescent | No |
| [Obtainium](https://obtainium.imranr.dev/) | The developer | The developer | Android's same-key update rule; optional external verification | Nobody centrally; the source host (for example GitHub) can | No |
| [Zapstore](/kb/zapstore/) | The developer | The developer, linked to a Nostr key | APK hash and signing certificate against signed Nostr releases | Nobody centrally; relays and file hosts can withhold | No |
| Google Play (baseline) | The developer | Usually Google, through Play App Signing | Google's review and scanning | Google, worldwide | Yes |

## The options

**F-Droid** is the longest-running free-software store. It builds every app from published source on its own build servers, so what you install corresponds to code anyone can read. By default F-Droid signs the result with its own key. For apps set up for **reproducible builds**, F-Droid rebuilds the app, confirms it is byte-for-byte identical to the developer's signed APK, and then publishes the developer-signed version. That is the strongest guarantee on this list: the binary demonstrably matches the source. The cost is delay between a developer's release and F-Droid's build, a free-software-only catalogue, and trust in F-Droid's build infrastructure and signing keys for the apps it signs itself.

**Accrescent** is a security-focused store, currently in alpha, that runs on Android 10 and up and is offered through the GrapheneOS App Store. Developers keep their own signing keys. Accrescent pins each app's signing key so even the first install is checked rather than trusted on first use, signs its repository metadata against tampering, and handles unattended updates without privileged system access on Android 12 and up. Its catalogue is small and curated by the project.

**Obtainium** is not a store. It watches the places developers already publish, such as GitHub, GitLab, Codeberg, F-Droid repositories and others, and installs and updates apps straight from those release pages. It removes the store middleman entirely, but the trust moves to the release page and the first download. The project recommends a separate app, Privacy Guides' Verified Apps, which checks installed apps' signing certificates against a database of known-good fingerprints.

**Zapstore** distributes developer-signed APKs announced as Nostr events and checks each download's hash and certificate against those events. Anyone can publish without approval, which is both the point and the risk. See [the Zapstore entry](/kb/zapstore/).

## What none of them guarantee

- **That an app is benign.** Signatures and reproducible builds prove origin and correspondence to source. Neither proves the code is safe. See [Verify software before installing it](/kb/verifying-software/).
- **Network privacy.** Each source sees which apps you fetch. Fetching over Tor reduces what it learns.
- **The operating system's honesty.** A store cannot protect you from the OS or firmware underneath. That is the job of a hardened OS such as [GrapheneOS](/kb/grapheneos/).

## The policy change to watch

From 30 September 2026, Google's **Android developer verification** requires apps installed on certified Android devices in Brazil, Indonesia, Singapore and Thailand to come from developers who have registered with Google and proved their identity, starting with installs from seven large stores including Google Play and Samsung Galaxy Store. Google plans to extend the rule to all certified devices in 2027. Unregistered apps can still be installed through ADB or an "advanced flow" that requires developer options, a restart, re-authentication and a 24-hour wait. Developers who publish anonymously, as many freedom-tech developers do, are the ones this squeezes. Google describes the requirement as applying to certified devices, so an operating system without Google certification is outside it as written.

## How to choose

- **You want the binary to match public source code:** F-Droid, preferring apps marked reproducible.
- **You want developer keys and strict first-install checks:** Accrescent, especially on GrapheneOS.
- **You want apps straight from the developer's own releases:** Obtainium, with signing-certificate checks.
- **You want permissionless publishing and Nostr-native identity:** Zapstore.

Mixing sources is normal. Because of Android's same-key rule, an app installed from one source usually cannot be updated from another that signs it with a different key.

## Primary sources

- F-Droid reproducible builds: https://f-droid.org/docs/Reproducible_Builds/
- Accrescent: https://accrescent.app/ · source: https://github.com/accrescent/accrescent
- Obtainium: https://github.com/ImranR98/Obtainium · wiki: https://wiki.obtainium.imranr.dev/
- Verified Apps (Privacy Guides): https://github.com/privacyguides/verified-apps-android
- Zapstore: https://zapstore.dev/ · https://github.com/zapstore/zapstore
- Play App Signing: https://support.google.com/googleplay/android-developer/answer/9842756
- Android developer verification: https://developer.android.com/developer-verification/guides
