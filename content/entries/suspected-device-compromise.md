---
title: "Responding to Suspected Device Compromise"
slug: suspected-device-compromise
type: guide
pillars: [endpoint]
readiness: usable
description: "Respond to a suspected phone or computer compromise: use a trusted device, preserve evidence, seek expert help and plan account and device recovery."
dek: "Move sensitive activity somewhere safer, record what happened and get help before making changes that could erase evidence or alert an attacker."
updated: 2026-10-25
created: 2026-10-25
origin: original
level: intermediate
related: [threat-modeling, grapheneos, tails-qubes-whonix, passkeys-and-security-keys, hardware-supply-chain-trust, encrypting-files-and-backups]
tags: [incident-response, devices, forensics, recovery]
---

## Summary

Unexpected battery drain, crashes or unfamiliar behavior do not by themselves prove surveillance. The [Coalition Against Stalkerware](https://stopstalkerware.org/stalkerware-detection-removal-and-prevention/) notes that unusual behavior can have other explanations, and that monitoring can occur without obvious symptoms. Treat a suspicion as a reason to assess what happened, not as a diagnosis.

The immediate aim is to keep sensitive activity off the suspect device, get appropriate help and preserve your options. If there is a personal-safety risk, plan technical changes with trusted support rather than treating cleanup as the only priority.

## 1. Use a separate trusted device

Contact help and coordinate your response from a different phone or computer that you have reason to trust. Do not type new passwords, hold sensitive conversations or discuss the investigation on the suspect device. [EFF's malware guidance](https://ssd.eff.org/module/how-do-i-protect-myself-against-malware) explains that an infected computer may expose keystrokes and recommends changing credentials from a computer believed to be safe.

**Avoid tipping off someone who may be monitoring you.** In stalking or coercive-control situations, deleting monitoring software or making conspicuous changes can be noticed and increase danger. The Coalition recommends making a safety plan on a safer device before removal. Do not confront a suspected attacker or announce your response through a channel they may control.

For confirmed computer malware, EFF recommends stopping use and disconnecting Wi-Fi. If you need forensic support, ask the responder how to handle power and network state. Explain any immediate safety or data-loss concern so containment and evidence preservation can be considered together.

## 2. Record observations and preserve evidence

Write down the dates, exact alerts, unexpected account activity and actions already taken. Keep copies of relevant messages and notifications where the suspect device cannot alter them. Record observations separately from guesses about their cause.

Before deleting an app, resetting, reinstalling or running cleanup tools, ask the responder what to preserve. The Coalition explicitly warns that deleting stalkerware also deletes related evidence. If immediate safety requires a change, record what changed and when; do not delay essential protection merely to collect more material.

Do not upload a device backup or suspicious files to a public forum. Amnesty's [forensics support information](https://securitylab.amnesty.org/get-help/) explains that an investigation can require access to sensitive device contents. Agree on the scope and a secure transfer method with the people helping you.

## 3. Get qualified help

- [Access Now's Digital Security Helpline](https://www.accessnow.org/help/) provides free technical support and incident response for civil society, including journalists, activists and human rights defenders. It checks whether a request falls within its mandate.
- [Amnesty International's Security Lab](https://securitylab.amnesty.org/get-help/) provides spyware-related resources and information about forensic support and secure contact.
- For a work device, contact your organization's security team through a trusted channel. For interpersonal monitoring, include a survivor-support organization in the safety plan.

Give the responder a short timeline, the device and operating system involved, any concrete warning, and whether you still have physical control of the device. Let them guide collection rather than installing a succession of scanners.

## 4. Understand what MVT can tell you

The [Mobile Verification Toolkit](https://github.com/mvt-project/mvt) helps investigators gather forensic traces from Android and iOS devices and compare available evidence with indicators of known spyware activity. It is intended for technologists and investigators, not end-user self-assessment.

The project is explicit: **public indicators are insufficient to establish that a device is clean**. New attacks or missing evidence can escape those checks, and reliable investigation may require non-public threat information. A match needs interpretation; no match is not an all-clear. MVT is an investigative tool, not a repair procedure or a general-purpose computer malware scanner.

## 5. Recover accounts from a clean device

Once the safety and evidence plan allows it, change credentials that may have been exposed. Start with accounts that control recovery of others, such as email and the password manager. Review recovery contacts, enrolled authenticators, active devices and sessions, and remove access you cannot account for.

For a vendor-specific example, [Google's compromised-account guidance](https://support.google.com/accounts/answer/6294825?hl=en) covers unfamiliar devices, security events, changed recovery information and mail-forwarding rules. Use the equivalent controls documented by each service. Do not assume that changing one password addresses all those settings.

Enroll [passkeys or security keys](/kb/passkeys-and-security-keys/) from a trusted device, with a tested spare or recovery route. Avoid immediately signing back in on the suspect device.

## 6. Plan device recovery and hardening

With a responder, decide whether to rebuild, reset or replace the device. EFF notes that an operating-system reinstall removes most malware but is not a guarantee against every form of persistence; restoring files from after an infection can also reintroduce it. Preserve necessary evidence first and choose restoration data carefully.

Use the device maker's recovery instructions and supported updates. For a computer, include firmware in the recovery discussion if the evidence warrants it; an OS reinstall is not a firmware reflash. Check [Hardware and Firmware Supply-Chain Trust](/kb/hardware-supply-chain-trust/) for that separate layer. Do not infer a firmware implant merely from ordinary glitches or a failed scan.

After agreeing how to preserve evidence, consider the platform's hardening options:

- **Apple Lockdown Mode** restricts features to reduce exposure to targeted attacks. On iPhone or iPad, Apple's [instructions](https://support.apple.com/en-us/105120) use Settings → Privacy & Security → Lockdown Mode and require a restart. Review the feature restrictions first.
- **Android Advanced Protection** has a device-protection setting distinct from Google Account protection. Google's [instructions](https://support.google.com/android/answer/16339980?hl=en) describe enabling Device protection under Advanced Protection. It blocks installation and updates from unknown app sources and may require a restart. Check availability and restrictions on the actual device.

These are protective settings, not findings that the device is infected or certificates that it has been cleaned. For longer-term choices, compare [GrapheneOS](/guides/grapheneos/) and [Tails, Qubes OS and Whonix](/guides/tails-qubes-whonix/).

## Readiness and limits

**Usable as a response workflow, not a diagnostic test.** Tools and expert analysis have limits, and the safest sequence depends on the evidence and the person's circumstances. Record what remains uncertain and agree with the responder which device and accounts can be used for sensitive work.

## Primary sources

- [Coalition Against Stalkerware: symptoms, safer devices, safety planning and evidence](https://stopstalkerware.org/stalkerware-detection-removal-and-prevention/).
- [EFF: malware response, credential changes and reinstall limits](https://ssd.eff.org/module/how-do-i-protect-myself-against-malware).
- [Access Now Digital Security Helpline](https://www.accessnow.org/help/).
- [Amnesty International Security Lab: help and forensic privacy](https://securitylab.amnesty.org/get-help/).
- [MVT's intended use and limits of public indicators](https://github.com/mvt-project/mvt).
- [Google: recover and secure a compromised account](https://support.google.com/accounts/answer/6294825?hl=en).
- [Apple: Lockdown Mode](https://support.apple.com/en-us/105120).
- [Google: Advanced Protection for Android devices](https://support.google.com/android/answer/16339980?hl=en).
