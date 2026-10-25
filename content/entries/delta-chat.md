---
title: "Delta Chat"
slug: delta-chat
type: deep-dive
pillars: [messaging]
readiness: usable
description: "Delta Chat carries encrypted conversations over email protocols. Learn what chatmail guarantees, what mail servers see, and where protection ends."
dek: "Email transport with a chat interface: encryption belongs to the devices, while delivery still passes through mail relays."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [compare-messengers, xmpp-omemo, simplex, metadata-resistance, encrypted-messaging]
---

## Summary

Delta Chat is a messenger built on email transport: IMAP receives messages and SMTP sends them. Its current default is a profile on a **chatmail relay**, with a randomly generated address, rather than an existing personal mailbox. Mobile and desktop clients are available. The transport standards are documented in the [chatmail core repository](https://github.com/chatmail/core/blob/main/standards.md); the [current help](https://delta.chat/en/help) explains profiles and relay choice.

## How it works

Autocrypt distributes encryption information, OpenPGP protects message contents, and **Secure-Join** establishes contacts through QR codes or invite links. These are separate jobs: opportunistic key exchange alone does not authenticate a contact against a malicious mail provider.

Delta Chat's [guaranteed encryption announcement](https://delta.chat/en/2023-11-23-jumbo-42) explains the extension of its earlier verified-group model to direct chats: a verified connection must not silently fall back to plaintext. Groups formed from verified contacts inherit that protection. The [subsequent security analysis and fixes](https://delta.chat/en/2024-03-25-crypto-analysis-securejoin) cover attacks on that setup and group membership information. These older announcements explain the guarantee; their interface markers are not instructions for today's app.

The current rule is clearer: **default chatmail relays reject messages without end-to-end encryption**. A classic email server can still carry unencrypted messages, which Delta Chat marks with an email icon. Do not extend chatmail's guarantee to arbitrary email correspondence. [Chatmail's relay documentation](https://chatmail.at/doc/relay/faq.html) also distinguishes encrypted message forwarding from a conventional mailbox.

## Trust model / threat model

The devices and the contact invitation are the trust boundary for content. Mail relays still see sender and recipient addresses and message sizes; the relay you connect to also sees your IP address. Group details and attachments are inside the encrypted message. This reduces exposed metadata without making the transport anonymous; compare [metadata resistance](/kb/metadata-resistance/) and [SimpleX](/kb/simplex/).

## Readiness

**Usable.** Documented mobile, desktop and multi-device workflows make this a practical messenger. Start with a chatmail profile and establish contacts using the documented invitation flow.

## Limits

The current FAQ explicitly says **perfect forward secrecy is not yet supported**. A leaked private decryption key can expose previously recorded ciphertext. Planned Autocrypt changes are not a present guarantee. Endpoint compromise and recipients retaining messages also remain outside transport encryption's protection.

For the broader choice, see [Choosing a private messenger](/kb/compare-messengers/).

## Primary sources

- [Delta Chat help: encryption, metadata, profiles and forward secrecy](https://delta.chat/en/help).
- [Transport and encryption standards used by chatmail](https://github.com/chatmail/core/blob/main/standards.md).
- [Guaranteed encryption and verified groups](https://delta.chat/en/2023-11-23-jumbo-42).
- [Secure-Join security analysis and fixes](https://delta.chat/en/2024-03-25-crypto-analysis-securejoin).
- [Chatmail relay guarantees and interoperability](https://chatmail.at/doc/relay/faq.html).
