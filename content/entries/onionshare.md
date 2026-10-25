---
title: "OnionShare"
slug: onionshare
type: deep-dive
pillars: [anonymity, storage]
readiness: usable
description: "OnionShare shares and receives files, hosts static websites and runs chat rooms over Tor. Understand host trust, access keys and document risks."
dek: "Turn your computer into a temporary onion service, with no separate hosting provider holding the files."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [securedrop, tor, using-tor-safely, encrypting-files-and-backups, compare-messengers]
---

## Summary

OnionShare starts a web service on your computer and exposes it through a [Tor](/kb/tor/) onion service. Its documented modes **share files, receive files and messages, host a static website, and run a chat room**. Visitors connect with Tor Browser. The [feature documentation](https://docs.onionshare.org/2.6/en/features.html) explains each mode.

## How it works

By default, an onion address and a private access key are needed to reach the service. You distribute those to the intended visitors. A public service can disable the key requirement. Your computer must stay online and keep OnionShare running for the service to remain available.

File transfers go directly between the visitor and your service through Tor. Website mode serves static files. Chat mode uses the onion connection to deliver messages to the host, which forwards them to the room's visitors; OnionShare adds no separate participant-to-participant encryption layer.

## Trust model / threat model

Tor encrypts the connection between Tor Browser and the onion service. A third-party file host is unnecessary, but **the OnionShare host is an endpoint**. For a chat room, that host receives the messages in plaintext before forwarding them. Trust it accordingly.

The [security documentation](https://docs.onionshare.org/2.6/en/security.html) also makes address distribution part of the threat model. An identifying channel used to share an address can identify the host. Leaking both address and key gives someone access while the service is running. Chat nicknames do not authenticate participants.

## Readiness

**Usable.** Suitable for a deliberate file exchange or temporary onion service when you can keep the host available and share access information safely. See [Using Tor safely](/guides/using-tor-safely/) before relying on anonymity.

## Limits

Receiving a file does not make it safe to open. OnionShare explicitly provides no protection against malicious uploaded documents. Its chat does not save history, but that cannot stop participants from making their own copies. A newsroom needing isolated document handling should examine [SecureDrop](/kb/securedrop/) and its operational requirements.

## Primary sources

- [OnionShare modes, availability, chat encryption and malicious-file warning](https://docs.onionshare.org/2.6/en/features.html).
- [OnionShare security design and limits](https://docs.onionshare.org/2.6/en/security.html).

Continue with [Magic Wormhole](/kb/magic-wormhole/).
