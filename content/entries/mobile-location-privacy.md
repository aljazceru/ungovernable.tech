---
title: "Mobile location privacy"
slug: mobile-location-privacy
type: explainer
pillars: ["endpoint", "anonymity"]
readiness: usable
description: "Understand subscriber and device identifiers, cell-site location, Wi-Fi and Bluetooth address randomization, airplane mode and radio shielding limits."
dek: "An encrypted conversation can still travel from a phone whose network and nearby observers can locate it."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: ["grapheneos", "browser-and-network-privacy", "metadata-resistance", "threat-modeling"]
---

## Summary

Phone location can be exposed through the cellular network, nearby Wi-Fi or Bluetooth observations, and applications receiving location data. These are separate channels. Restricting an app's location permission does not remove the cellular network's ability to locate a connected subscriber.

## Identifiers and cell sites

An **IMSI** identifies a mobile subscription; an **IMEI** identifies mobile equipment. They are different from a Wi-Fi or Bluetooth MAC address. Changing a local wireless address does not change the subscription or equipment identifiers used by the cellular system.

EFF describes how a carrier can estimate a connected phone's location from its network interactions, and how cell-site simulators can detect phones in an area. This page makes no universal claim about location accuracy or immunity to those systems. Plan separately for network records, nearby observers and apps.

## Wi-Fi and Bluetooth

Apple documents private Wi-Fi addresses that differ between networks and can rotate. Android documents Wi-Fi MAC randomization, including randomized addresses when probing and when connecting on supported versions. Check the selected network's setting and the behavior of your actual device.

For Bluetooth Low Energy, Apple's security guide describes rotating private addresses and identity-resolving keys exchanged during pairing. A known peer can resolve those private addresses. Address randomization therefore reduces one tracking handle; it does not promise that paired devices, accounts or application behavior cannot identify you.

## Airplane mode and shielding

Apple's airplane-mode instructions say Bluetooth remains enabled, and Wi-Fi can be used again in airplane mode. Inspect the individual radio controls instead of assuming the airplane icon means every transmitter is disabled.

A Faraday bag is a radio-isolation tool, not a deletion tool. NIST's mobile-forensics guidance warns that shielding can attenuate rather than completely eliminate signals, and that poor closure or attached cables can defeat isolation. Test the actual closed bag with the actual device and required radios; one failed incoming call is not proof that every radio path is blocked.

## Trust model / threat model

Decide which observer matters before choosing controls. Reduce unnecessary app location access, keep private wireless addressing enabled where supported, and turn off radios you do not need. For especially sensitive movement, consider whether carrying the phone is necessary at all. None of those steps erases records already collected.

## Readiness and limits

**Usable, with device-specific behavior.** These controls exist, but they are not a single anonymity switch. Continue with [GrapheneOS](/guides/grapheneos/), [browser and network privacy](/guides/browser-and-network-privacy/) and [metadata resistance](/kb/metadata-resistance/). Use [threat modeling](/guides/threat-modeling/) to decide which exposure matters in your situation.

## Primary sources

- [EFF: mobile-phone location tracking](https://ssd.eff.org/module/mobile-phones-location-tracking)
- [Apple private Wi-Fi addresses](https://support.apple.com/en-us/102509)
- [Android Wi-Fi MAC randomization](https://source.android.com/docs/core/connect/wifi-mac-randomization)
- [Apple Bluetooth Low Energy privacy](https://support.apple.com/guide/security/bluetooth-security-sec82597d97e/web)
- [Apple airplane-mode radio behavior](https://support.apple.com/en-us/108785)
- [NIST SP 800-101 Rev. 1: identifiers and radio-isolation limitations](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-101r1.pdf)
