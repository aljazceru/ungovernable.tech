---
title: "SecureDrop"
slug: securedrop
type: deep-dive
pillars: [anonymity]
readiness: battle-tested
description: "SecureDrop lets newsrooms receive documents from anonymous sources over Tor. Its safety depends on dedicated servers, isolated viewing and careful use."
dek: "A newsroom submission system with separate source and journalist interfaces, and a workflow designed to isolate sensitive documents."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [onionshare, tor, tails-qubes-whonix, threat-modeling, using-tor-safely]
---

## Summary

SecureDrop is the Freedom of the Press Foundation's open-source whistleblower submission system. A newsroom operates its own installation to receive documents and exchange messages with sources through Tor onion services. It is a deployed system and an operating procedure, not an ordinary messenger account. The [project overview](https://docs.securedrop.org/en/stable/what_is_securedrop.html) explains its purpose and deployment.

## How it works

The documented **Tails and air-gap architecture** separates these roles:

- **Application Server:** hosts the public Source Interface and authenticated Journalist Interface. It receives submissions and encrypts them for storage.
- **Monitor Server:** runs monitoring and generates alerts about the installation.
- **Journalist and Admin Workstations:** use Tails to reach the appropriate authenticated onion services.
- **Secure Viewing Station:** remains offline, boots its dedicated Tails drive and holds the submission decryption key. Encrypted submissions arrive on transfer media.

This is the air-gapped workflow described in the installation documentation; the role separation matters more than treating every machine as interchangeable.

## Source and journalist flows

A source uses Tor Browser to reach the newsroom's verified onion address, obtains a generated codename, and submits documents or messages. The codename lets the source return to read replies. Follow the [source instructions](https://docs.securedrop.org/en/stable/source/how_to_submit.html) for that flow.

A journalist downloads encrypted submissions on the online workstation, carries them to the [Secure Viewing Station](https://docs.securedrop.org/en/stable/admin/installation/set_up_svs.html), and decrypts and examines them there. Publication and export require deliberate handling of the documents and their metadata.

## Trust model / threat model

**The Application Server sees incoming plaintext before encrypting submissions.** Tor protects the connection to that server; this is not browser-to-journalist encryption that bypasses the server. The [threat model](https://docs.securedrop.org/en/stable/threat_model/threat_model.html) describes how server compromise, stolen credentials and compromised workstations can expose data.

The air gap helps contain malicious documents and protects the decryption key from an online workstation compromise. It cannot erase identifying facts inside a document or protect a source using an already compromised device. The [source preparation guidance](https://docs.securedrop.org/en/stable/source/before_you_submit.html) warns about employer hardware and networks, and about local traces of Tor use.

## Readiness

**Battle-tested, with substantial operational requirements.** The project documents deployed use, audits and a maintained installation procedure. That rating describes maturity, not automatic safety: trained staff, maintained servers, protected credentials and disciplined document handling are part of the system.

## Limits

SecureDrop cannot promise protection from every adversary or a source's own identifying disclosures. A seized or compromised viewing station can expose its keys and decrypted material. For a smaller, temporary file exchange, compare [OnionShare](/kb/onionshare/); first work through [threat modeling](/guides/threat-modeling/).

## Primary sources

- [SecureDrop overview, stewardship and architecture](https://docs.securedrop.org/en/stable/what_is_securedrop.html).
- [Secure Viewing Station setup and transfer workflow](https://docs.securedrop.org/en/stable/admin/installation/set_up_svs.html).
- [Source submission and reply workflow](https://docs.securedrop.org/en/stable/source/how_to_submit.html).
- [Source preparation and operational risks](https://docs.securedrop.org/en/stable/source/before_you_submit.html).
- [SecureDrop threat model and compromise consequences](https://docs.securedrop.org/en/stable/threat_model/threat_model.html).
