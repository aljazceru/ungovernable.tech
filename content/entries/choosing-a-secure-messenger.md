---
title: "Choosing a Secure Messenger"
slug: choosing-a-secure-messenger
type: guide
pillars: [messaging, anonymity]
description: "Signal, SimpleX, Session, Briar, Cwtch, Matrix and others compared by what they actually protect: content, identifiers, metadata and availability."
dek: "Every serious messenger encrypts content. They differ in what they require from you, what their servers learn, and whether they work when the internet does not."
updated: 2026-10-19
created: 2026-10-17
origin: original
level: beginner
time: "15 minutes"
related: [encrypted-messaging, signal-protocol, simplex, session-messenger, briar, cwtch, matrix, metadata-resistance, mls-wire]
---

End-to-end encryption is no longer what separates good messengers from bad ones; most mainstream apps have it. The questions that matter now are about **identifiers** (what do you have to hand over to sign up?), **metadata** (what does the service learn about who talks to whom, and when?), **architecture** (one company's servers, federated servers, or no servers at all?) and **resilience** (does it still work under censorship or a shutdown?).

## At a glance

For the expanded comparison, including [Delta Chat](/kb/delta-chat/), [XMPP with OMEMO](/kb/xmpp-omemo/), [Jami](/kb/jami/) and the off-grid choices, see [Choosing a private messenger](/kb/compare-messengers/). For document submissions, compare [OnionShare](/kb/onionshare/) and [SecureDrop](/kb/securedrop/).

| | Signal | SimpleX | Session | Briar | Cwtch | Matrix (Element) |
|---|---|---|---|---|---|---|
| Sign-up needs | Phone number | Nothing | Nothing (random ID) | Nothing | Nothing | Account on a homeserver (email optional) |
| User identifier | Phone number; optional username | None: per-contact queues | Session ID (public key) | Key, exchanged in person or by link | Onion address | @user:server |
| Content encryption | Signal Protocol (double ratchet, PQXDH) | Double ratchet with post-quantum key exchange | Session protocol (see note) | Bramble protocols, end-to-end | End-to-end over Tor | Olm/Megolm; MLS in development |
| Who sees metadata | Signal's servers see little by design (sealed sender) but you are tied to a phone number | Relays see per-queue traffic, not identities or contact lists | Onion-routed through Session network nodes | No servers; peers connect directly over Tor | No central servers; Tor onion services | Homeservers store room membership and timing |
| Architecture | Centralised (Signal Foundation) | Relays anyone can run; you can choose them | Decentralised node network | Peer-to-peer | Peer-to-peer over Tor | Federated |
| Works without internet | No | No | No | Yes: Bluetooth and Wi-Fi | No | No |
| Groups | Yes, large | Yes | Yes | Yes, small | Yes | Yes, very large |
| Platforms | Android, iOS, desktop | Android, iOS, desktop | Android, iOS, desktop | Android; desktop beta | Android, desktop | All |
| Readiness | [Battle-tested](/kb/signal-protocol/) | [Usable](/kb/simplex/) | [Usable](/kb/session-messenger/) | [Battle-tested](/kb/briar/) | [Usable](/kb/cwtch/) | [Battle-tested](/kb/matrix/) |

Note on Session: when Session forked from Signal in 2020 it replaced the Signal double ratchet with a simpler protocol and lost forward secrecy as a result. Check Session's current protocol documentation before relying on it for sensitive work.

## Recommendations by situation

**For most people, most of the time: Signal.** It has the strongest and most studied cryptography, a large user base (so using it is unremarkable), disappearing messages, and a service designed to hold almost nothing about you: Signal has published the subpoena responses showing it could provide only account creation date and last connection time. The weak point is the phone number. Since 2024 you can hide your number behind a username, but you still need one to register.

**When you must not be linked to a phone number or identity: SimpleX.** SimpleX has no user identifiers at all: each contact is reached through separate, one-way message queues on relays, so no server holds your contact list. You can choose or self-host relays. It has had independent security reviews by Trail of Bits. Its user base is smaller, which makes its use more noticeable.

**When the internet may be cut: Briar.** Briar connects peers directly over Tor when online, and over Bluetooth or Wi-Fi when not. Messages are stored on devices, not servers. It needs both parties to be online (or a Briar Mailbox to hold messages). Android only for practical purposes. See [Internet Shutdown Preparedness](/guides/internet-shutdown-preparedness/).

**For metadata-resistant groups over Tor: Cwtch.** Cwtch, from Open Privacy, builds peer-to-peer and group messaging on Tor onion services with the explicit goal of hiding metadata from servers. It is less polished than the others.

**For communities and organisations that want to run their own servers: Matrix.** Federation means no single company controls the network, and you can host your own homeserver. The trade-off is metadata: homeservers see who is in which room and when, and federated rooms copy that to every participating server.

**For Nostr users: White Noise, Cordn and NIP-17.** Encrypted messaging on Nostr is developing quickly. [White Noise](/kb/white-noise/) is the most mature option: MLS group chat over relays you choose, built on [Marmot](/kb/marmot-protocol/), audited, but still beta. [Cordn](/kb/cordn/) takes a different path, routing each group through one coordinator you can self-host anywhere. Both are experimental, so pair them with a battle-tested messenger for sensitive work. See also [Getting Started on Nostr Safely](/guides/nostr-getting-started/).

## What to avoid for sensitive work

- **Telegram** chats are not end-to-end encrypted by default; only one-to-one "secret chats" are, and groups never are. Telegram's servers can read everything else.
- **SMS and ordinary phone calls** are readable by the carrier and anyone with access to it.
- **Email** is not end-to-end encrypted unless both sides use PGP or a similar tool, and its metadata (who, when, subject lines) is always exposed.
- **WhatsApp** uses the Signal Protocol for content, but Meta collects extensive metadata and links it to your phone number and contacts.

## Settings that matter more than the app

- Turn on **disappearing messages** for sensitive conversations.
- Use a **registration lock** or PIN where offered (Signal has one) to prevent account takeover through your phone number.
- **Verify safety numbers** or keys in person with your most important contacts.
- Protect the **device**: a messenger cannot protect messages on an unlocked or compromised phone ([Threat Modeling](/guides/threat-modeling/), [GrapheneOS](/guides/grapheneos/)).
- Remember that **anyone in the chat** can screenshot, forward or be arrested with their phone.

## Sources

- Signal, *Signal Protocol documentation* and *PQXDH specification*: <https://signal.org/docs/>
- Signal, *Government requests* (published subpoena responses): <https://signal.org/bigbrother/>
- Signal, *Keep your phone number private with Signal usernames* (2024): <https://signal.org/blog/phone-number-privacy-usernames/>
- SimpleX Chat, *Security reviews* and protocol documentation: <https://simplex.chat/docs/protocol/simplex-chat.html>
- Session, *Session protocol and whitepaper*: <https://getsession.org/whitepaper>
- Briar Project, *How it works*: <https://briarproject.org/how-it-works/>
- Cwtch documentation: <https://docs.cwtch.im/>
- Matrix, *End-to-end encryption*: <https://matrix.org/docs/matrix-concepts/end-to-end-encryption/>
- Telegram FAQ, *Secret chats*: <https://telegram.org/faq#secret-chats>
