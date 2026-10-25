---
title: "Passkeys and Security Keys"
slug: passkeys-and-security-keys
type: deep-dive
pillars: [endpoint, identity]
readiness: usable
description: "Passkeys bind sign-in to a service. Compare synced credentials and hardware security keys, their recovery paths, and the trust each requires."
dek: "Phishing-resistant sign-in still needs a plan for lost devices, account recovery and the software holding your keys."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [encrypting-files-and-backups, threat-modeling, suspected-device-compromise, heads-firmware]
tags: [passkeys, webauthn, fido2, security-keys]
---

## Summary

A passkey is a public-key credential for signing in to a particular service. The service stores a public key; an authenticator uses the corresponding private key to prove that you can sign in. A passkey can stay on one device, including a hardware security key, or be synced between devices. Those choices have different recovery and custody implications.

FIDO2 combines the browser-facing WebAuthn standard with FIDO's Client to Authenticator Protocol (CTAP). It supports both built-in authenticators and external security keys. Start here when choosing account protection alongside [file and backup encryption](/guides/encrypting-files-and-backups/).

## How it works

At registration, the service associates a credential's public key with your account. At sign-in, it sends a fresh challenge. The authenticator signs data that binds the response to that challenge and the service's relying-party identifier; the browser also supplies the origin. The service must verify these values and the signature.

This binding is the reason for phishing resistance: a lookalike site on an unrelated domain cannot request the real site's credential through a conforming browser. You do not type a reusable secret into that site's form. A PIN or biometric can authorize the authenticator locally; biometric data is not sent to the service. See [WebAuthn Level 3](https://www.w3.org/TR/webauthn-3/) for the protocol and verification requirements.

| Choice | Where the credential lives | Recovery planning |
|---|---|---|
| Device-bound passkey | Bound to one authenticator; not synced | Register another authenticator before the first is lost. |
| Synced passkey | Available on devices enrolled through a credential provider | Understand device enrollment, provider recovery and what happens if all devices are lost. |
| Hardware security key | A separate authenticator; FIDO2 keys can hold device-bound passkeys | Enroll a spare separately with each service that supports it. |

**FIDO2 and U2F are not interchangeable feature labels.** The older U2F protocol, now called CTAP1, provides a second factor. FIDO2/CTAP2 supports passwordless authentication as well. Check that a key and the service support the particular passkey workflow you need; a U2F-only key is not a passwordless passkey store. The [FIDO specifications overview](https://fidoalliance.org/specifications/) explains the distinction.

## Trust model

You trust the browser, operating system, authenticator and the service's verification code. For a synced passkey, also examine the provider's synchronization and recovery design. WebAuthn's backup-state flags describe whether a credential can be backed up and whether it is backed up; they are not an audit of a provider's cloud security.

**What can the sync provider do?** It supplies the synchronization service and its enrollment and recovery mechanisms. **What can it read?** That depends on its implementation. For a concrete example, [Apple documents](https://support.apple.com/en-us/102195) that iCloud Keychain encrypts passkeys end to end with keys unknown to Apple, and that recovery has additional checks beyond signing in to an Apple Account. In that documented design, storing the encrypted backup does not give Apple the private keys. Do not extend that claim to every provider or treat it as protection against compromised endpoint software.

## Recovery and spare keys

Register a spare key or another independent authenticator while you still have access, test it, and store it separately. A spare key needs its own registration; buying a second key does not enroll it in existing accounts. Keep any service-issued recovery codes somewhere you can reach without the lost device.

Review the service's password, email, SMS and help-desk recovery routes too. A strong sign-in method does not remove those alternate routes into the account. WebAuthn explicitly recommends additional authenticators or account recovery for credentials that cannot survive device loss. After a loss, use the service's credential-management controls to revoke the missing authenticator.

## Readiness

**Usable.** These are implemented authentication standards with documented platform support. The practical choice is which credential provider or hardware key fits your devices, services and recovery plan. Check compatibility before removing an existing sign-in method.

## Limits

Passkeys authenticate an account; they do not encrypt its stored messages or make its operator unable to suspend it. Origin binding assumes a trustworthy client. It is not a remedy for an already compromised device or stolen authenticated session. If that is the concern, use the [suspected device compromise guide](/guides/suspected-device-compromise/) before enrolling new credentials.

## Primary sources

- [W3C Web Authentication Level 3](https://www.w3.org/TR/webauthn-3/).
- [FIDO authentication specifications overview: FIDO2, CTAP and U2F](https://fidoalliance.org/specifications/).
- [FIDO passkey definitions and frequently asked questions](https://fidoalliance.org/passkeys/).
- [FIDO authentication specifications](https://fidoalliance.org/specifications/download/).
- [Apple: security, synchronization and recovery of passkeys](https://support.apple.com/en-us/102195).
