---
title: "Choosing a private messenger"
slug: compare-messengers
type: comparison
pillars: [messaging, anonymity, mesh]
description: "Compare private messengers by identifiers, servers, metadata, encryption defaults, offline operation and readiness, including the limits of radio meshes."
dek: "Start with who can identify you, who delivers the messages, and whether the network you need will be available."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [choosing-a-secure-messenger, encrypted-messaging, metadata-resistance, delta-chat, xmpp-omemo, jami, meshtastic, meshcore]
---

## Summary

Choose a messenger against a concrete threat model. End-to-end encryption protects message content; it does not by itself hide account identifiers, connection patterns or radio transmissions. The tables separate those questions and distinguish **delivery to someone who reconnects later** from **communication without internet access**. For a step-by-step decision, use [Choosing a secure messenger](/guides/choosing-a-secure-messenger/) and [threat modeling](/guides/threat-modeling/).

## Identifiers, servers and metadata

| Tool | Identifier needed | Servers / delivery infrastructure | Metadata exposure and trust boundary |
|---|---|---|---|
| [Signal](/kb/signal-protocol/) (the app) | Phone number to register; optional username for contact | Signal's service queues encrypted messages | Registration number and delivery destination remain relevant; sealed sender reduces sender information exposed to the service. A username does not remove registration. |
| [SimpleX](/kb/simplex/) | No global user ID; invitation and per-connection queue addresses | Selectable messaging relays | Relays handle queue traffic. Removing a shared user identifier reduces correlation; padding and queue rotation mitigate traffic analysis rather than abolish it. |
| [Session](/kb/session-messenger/) | Account ID; no phone number or email | Distributed nodes and onion requests | Routing separates origin from destination across nodes. Push-notification choices expose additional tokens and account information; inspect those settings. |
| [Briar](/kb/briar/) | Local account; exchanged contact links or QR codes | Direct connections over Tor or local links | Contact lists stay on devices. Tor addresses online relationship privacy; local links still have a nearby network observer to consider. |
| [Cwtch](/kb/cwtch/) | Locally generated key / onion-service profile | Peer-to-peer over Tor; untrusted servers for group storage | Group servers hold ciphertext; Tor and ephemeral fetching reduce relationship exposure. Participants and their devices remain trusted endpoints. |
| [Delta Chat](/kb/delta-chat/) | Mail address, randomly generated with a default chatmail profile | Chatmail or compatible mail relays | Relays see sender and recipient addresses, sizes and connecting IPs; encrypted group details do not remove that delivery metadata. |
| [XMPP / OMEMO](/kb/xmpp-omemo/) | XMPP address at a chosen server | Federated XMPP servers | Your server stores the roster; participating servers handle addresses and traffic. OMEMO explicitly excludes metadata protection. |
| [Jami](/kb/jami/) | Device-held cryptographic account / Jami ID; optional username | OpenDHT discovery; bootstrap, proxy and TURN services as needed | Peers exchange network-address candidates. Distributed accounts do not make contacts anonymous to each other. |
| [Matrix](/kb/matrix/) | Account at a homeserver; registration requirements vary | Federated homeservers | Participating servers synchronise room events and handle membership and routing. Encrypting message bodies does not hide the room's existence from them. |
| [White Noise](/kb/white-noise/) | Public-key identity; no phone number or email | Nostr relays; media servers | Relay operators can see connecting IPs; public profiles remain public. Encrypted conversations are a separate layer. |
| [Bitchat](/kb/bitchat/) | Device keys and nickname; no account registration | Bluetooth peers; Nostr relays for the internet path | Stable mesh IDs and announcements expose local presence; the Nostr envelope exposes the recipient key. |
| [Meshtastic](/kb/meshtastic/) | Radio node identity and channel settings | LoRa nodes; optional internet gateways | Packet headers remain visible; the default channel key is public. Radio operation is not an anonymity guarantee. |
| [MeshCore](/kb/meshcore/) | Radio node key and channel settings | LoRa repeaters; optional room servers | Adverts disclose node keys and optional identity/location data; routing headers remain visible. The default public-channel key is published. |

## Encryption, offline operation and readiness

“Encrypted” below refers to message content for the stated conversation type. Public rooms and default radio channels need separate treatment. “Usable” is an editorial assessment of practical deployment, not a certification.

| Tool | Encryption default and important exception | Offline / mesh capability | Readiness |
|---|---|---|---|
| Signal | End-to-end encrypted messages and calls | Needs the service; server queues allow later delivery | Battle-tested |
| SimpleX | End-to-end encrypted private conversations | Needs reachable relays; queued delivery is not a local radio mesh | Usable |
| Session | End-to-end encrypted private conversations; the current FAQ says forward secrecy is still planned | Needs its node network; no local transport documented here | Usable; assess calls separately |
| Briar | End-to-end encrypted device connections | Bluetooth and Wi-Fi without internet; Tor online | Usable; **maintenance mode since July 9, 2026** |
| Cwtch | End-to-end encryption over Tor; group content encrypted for members | Tor connectivity; servers can hold group messages for later delivery | Usable for peer chat; server hosting requires experiments |
| Delta Chat | Default chatmail relays enforce end-to-end encryption; classic mail can be unencrypted | Needs reachable mail relays | Usable; current FAQ says no perfect forward secrecy |
| XMPP / OMEMO | Depends on client and conversation settings; confirm OMEMO and verify devices | Needs reachable XMPP servers | Usable clients; XEP-0384 remains Experimental |
| Jami | TLS/SRTP protect connections and media; signed swarm history | IP-network peer-to-peer; history needs a reachable holder | Usable; test connectivity and linked devices |
| Matrix | Element's documented private-room flow enables encryption; do not assume every room is encrypted | Needs reachable homeservers | Battle-tested; room and client choices matter |
| White Noise | End-to-end encrypted conversations | Needs reachable relays; no local radio transport documented here | Experimental / beta |
| Bitchat | Private messages encrypted; public broadcasts are public; stored-mail paths lack forward secrecy | Bluetooth mesh and couriers; Nostr when online | Experimental |
| Meshtastic | Private-key direct messages; channel privacy needs a secret channel key, **not the published default** | LoRa mesh without internet; separate radio hardware | Usable for off-grid text |
| MeshCore | Encrypted direct/private-channel payloads; **default public channel is readable** | LoRa with dedicated repeaters; separate radio hardware | Usable for off-grid text |

Briar's [maintenance announcement](https://briarproject.org/news/2026-maintenance-mode/) says the project remains active with essential security updates and bug fixes. Maintenance mode is not abandonment, but it changes expectations for new features.

## Trust model / threat model

**Account privacy:** distinguish not giving a phone number to a contact from not registering one with a service. Signal usernames address the former. SimpleX avoids a global user identifier. Jami and Cwtch create cryptographic identities locally, with different network exposure.

**Server privacy:** federation gives a choice of operators; it does not hide the routing information those operators need. Compare [Delta Chat](/kb/delta-chat/), [XMPP/OMEMO](/kb/xmpp-omemo/) and [Matrix](/kb/matrix/) with the approaches in [metadata resistance](/kb/metadata-resistance/).

**Shutdown resilience:** prepare the equipment and contacts before losing connectivity. [Meshtastic](/kb/meshtastic/) and [MeshCore](/kb/meshcore/) require radios; [Bitchat](/kb/bitchat/) and [Briar](/kb/briar/) use local phone connections in different ways. The [off-grid messaging overview](/kb/off-grid-messaging/) and [building a mesh](/guides/building-a-mesh/) cover that preparation.

## Limits

This is a comparison of documented architectures and defaults, not a ranking by a single privacy score. A compromised endpoint or an untrustworthy recipient remains a problem across these designs. Check the actual conversation mode and client instead of extending a private-chat guarantee to every feature of an app.

Other choices have narrower roles: [Tox](/kb/tox/) and [Quiet](/kb/quiet/) carry explicit experimental or unaudited warnings; [Veilid](/kb/veilid/) is an application framework. For anonymous submissions, distinguish [OnionShare](/kb/onionshare/)'s host-operated service from [SecureDrop](/kb/securedrop/)'s newsroom infrastructure and isolated viewing workflow.

## Primary sources

- Signal: [service and privacy policy](https://signal.org/legal/), [phone-number privacy and usernames](https://signal.org/blog/phone-number-privacy-usernames/), [sealed sender](https://signal.org/blog/sealed-sender/).
- SimpleX: [network and identifiers](https://simplex.chat/), [queues, encryption and traffic-analysis mitigations](https://simplex.chat/docs/glossary.html).
- Session: [official FAQ, routing, encryption and notification trade-offs](https://getsession.org/faq).
- Briar: [design and local transports](https://briarproject.org/how-it-works/), [local accounts and contact exchange](https://briarproject.org/manual/), [maintenance status](https://briarproject.org/news/2026-maintenance-mode/).
- Cwtch: [security overview](https://docs.cwtch.im/security/intro), [profiles](https://docs.cwtch.im/docs/profiles/introduction), [untrusted group servers and experimental status](https://docs.cwtch.im/docs/servers/introduction).
- Delta Chat: [current encryption and metadata guarantees](https://delta.chat/en/help).
- XMPP: [OMEMO specification](https://xmpp.org/extensions/xep-0384.html), [server-held rosters](https://www.rfc-editor.org/rfc/rfc6121.html).
- Jami: [accounts and network security](https://docs.jami.net/en_US/user/faq.html), [OpenDHT](https://docs.jami.net/en_US/user/jami-distributed-network.html), [swarm history](https://docs.jami.net/en_US/developer/jami-concepts/swarm.html).
- Matrix: [account and provider choice](https://matrix.org/docs/chat_basics/matrix-for-im/), [federated room events](https://matrix.org/docs/matrix-concepts/elements-of-matrix/), [private-room encryption](https://matrix.org/docs/chat_basics/private-group-chat/).
- White Noise: [identity, relays, encryption and beta status](https://www.whitenoise.chat/faq).
- Bitchat: [protocol and documented metadata exposure](https://github.com/permissionlesstech/bitchat/blob/main/WHITEPAPER.md).
- [Meshtastic encryption and public channel keys](https://meshtastic.org/docs/overview/encryption/); MeshCore: [roles and public-channel key](https://github.com/meshcore-dev/MeshCore/blob/main/docs/faq.md), [packet headers](https://github.com/meshcore-dev/MeshCore/blob/main/docs/packet_format.md), [node adverts and encrypted payloads](https://github.com/meshcore-dev/MeshCore/blob/main/docs/payloads.md).
