---
title: "Jami"
slug: jami
type: deep-dive
pillars: [messaging]
readiness: usable
description: "Jami uses distributed discovery and device-held identities for calls and chat. Explore OpenDHT, encrypted connections, swarm history and network limits."
dek: "A distributed communications app whose accounts live on devices, with practical dependencies on discovery and connectivity services."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [compare-messengers, tox, quiet, xmpp-omemo, metadata-resistance]
---

## Summary

Jami offers messaging and calls without a central account or message server. An account is a cryptographic identity stored on the user's devices; its Jami ID identifies the public key. No phone number or email address is required. A human-readable username is optional. The [official FAQ](https://docs.jami.net/en_US/user/faq.html) documents these distinctions.

## How it works

**Discovery.** [OpenDHT](https://docs.jami.net/en_US/user/jami-distributed-network.html) provides a distributed key-value network used for connectivity establishment and message distribution. A bootstrap node introduces a new device to that network. Users can configure another bootstrap node or run one themselves.

**Connections.** Jami negotiates connections between peers. Its FAQ documents TLS for secure connections and SRTP for media. TURN relays can help when a direct connection cannot be established; a DHT proxy can handle discovery on behalf of a device, including mobile notification workflows.

**Conversation history.** [Swarm conversations](https://docs.jami.net/en_US/developer/jami-concepts/swarm.html) use replicated Git repositories. Signed commits carry messages and membership changes; peers validate commits before accepting them. Swarm history is synchronised between participants and linked devices. It is not simply a mailbox stored in the DHT.

## Trust model / threat model

Trust rests on device keys, the intended contacts and the software validating their messages. Distributed discovery removes a central account authority, but bootstrap nodes, proxies and relays still perform useful network roles. The FAQ describes peers exchanging IP-address candidates: **serverless does not mean anonymous to contacts**.

Swarm membership determines who receives history. Encryption does not stop a legitimate member from keeping or redistributing it. Compare [Quiet](/kb/quiet/) for a team-chat design using Tor, and [metadata resistance](/kb/metadata-resistance/) for the distinction between content privacy and hiding relationships.

## Readiness

**Usable.** The project distributes clients and documents messaging, calls and linked-device operation. Test the actual devices and networks your group will use, especially delivery when devices are not online together.

## Limits

History synchronisation needs a reachable peer holding that history. NAT traversal and mobile background operation introduce dependencies even without a central messaging service. Jami is not a substitute for a radio mesh during an internet shutdown; see the [messenger comparison](/kb/compare-messengers/).

## Primary sources

- [Jami project and clients](https://jami.net/).
- [Jami FAQ: accounts, TLS/SRTP, proxies, TURN and synchronisation](https://docs.jami.net/en_US/user/faq.html).
- [Distributed network and OpenDHT](https://docs.jami.net/en_US/user/jami-distributed-network.html).
- [Swarm conversation design](https://docs.jami.net/en_US/developer/jami-concepts/swarm.html).
