---
title: "Internet Shutdown Preparedness"
slug: internet-shutdown-preparedness
type: guide
pillars: [circumvention, mesh, messaging]
description: "What to set up before the network goes dark: offline-capable messengers, mesh radios, offline maps and knowledge, saved bridges and a plan for your group."
dek: "When the network is switched off, the only tools that work are the ones you installed, tested and shared before it happened."
updated: 2026-10-17
created: 2026-10-17
origin: original
level: beginner
time: "1-2 hours to prepare"
related: [off-grid-messaging, briar, bitchat, meshtastic, building-a-mesh, censorship-circumvention]
---

Governments shut down the internet during protests, elections, exams and conflicts. Access Now's #KeepItOn coalition documents hundreds of shutdowns every year, from regional mobile data cuts to nationwide blackouts lasting weeks. Shutdowns are rarely total and rarely instant: often mobile data goes first, then specific apps, then everything. Preparation is what separates a group that can still coordinate from one that cannot.

## Understand what kind of shutdown you face

- **Platform blocks.** Specific apps or sites are blocked; the internet still works. Circumvention tools solve this ([Getting Around Internet Censorship](/guides/censorship-circumvention/)).
- **Throttling.** Connections are slowed until video and images fail. Text-only tools and low-bandwidth transports keep working longer.
- **Allowlisting.** Only approved domestic services work. Very little gets out; local, offline communication becomes essential.
- **Mobile data shutdown.** Mobile data is cut while fixed broadband and SMS may continue. Wi-Fi from fixed lines becomes valuable.
- **Full shutdown.** Nothing works. Only local radio, local mesh and physical exchange remain.

## Before: install and test

Do this while the internet works, and do it with the people you need to reach.

1. **A messenger that works without the internet.** [Briar](/kb/briar/) syncs over Bluetooth and Wi-Fi when there is no internet, and over Tor when there is. [Bitchat](/kb/bitchat/) relays messages over a Bluetooth Low Energy mesh between nearby phones. Both need the other person nearby (or a chain of people). Exchange contacts in advance; you cannot add someone you cannot reach.
2. **Mesh radios.** LoRa radios running [Meshtastic](/kb/meshtastic/) or [MeshCore](/kb/meshcore/) carry short text messages for kilometres between devices, without any infrastructure, paired to your phone over Bluetooth. A few radios on rooftops can cover a neighbourhood. See [Building a Local Mesh Network](/guides/building-a-mesh/).
3. **Ways to share apps offline.** App stores may be unreachable. F-Droid's *Nearby* feature and Briar's built-in "share this app" let you pass installers phone to phone. Keep installer files on a USB stick.
4. **Circumvention tools and private bridges, saved.** Partial shutdowns often leave some routes open. Install two or three tools and store private Tor bridge lines offline.
5. **Offline maps and knowledge.** Download offline maps (Organic Maps, OsmAnd) for your area. Kiwix (<https://kiwix.org/>) serves Wikipedia and other references offline, including first-aid and medical material.
6. **Power.** Power banks, solar chargers and spare cables. A radio or phone that is dead is no use.
7. **A broadcast receiver.** Shortwave and FM radio still reach people when everything else is down; some international broadcasters increase shortwave service during crises.

## Make a plan with your group

- Agree on **where and when to meet** if all communication fails.
- Agree on a **chain of contacts** so that one message can reach everyone by Bluetooth or radio hops.
- Decide **who holds which equipment** and who knows how to use it.
- Keep **a written list** of the essentials (names, meeting points, radio channel settings) in a form you are willing to have searched, or memorise it.

## Satellite and long-distance options

Satellite internet terminals have kept people connected during shutdowns, but they are physical objects that can be detected, confiscated or criminalised, and the operator, not you, controls the service. Satellite messengers and newer phone-to-satellite messaging work for short texts but are tied to a provider and an account. Amateur HF radio can cross continents without infrastructure, but needs skill, equipment and, in most countries, a licence; encryption is not allowed on amateur bands. See [Satellite IoT](/kb/satellite-iot/) and [HF Radio Data Modes](/kb/hf-data-modes/).

## During: reduce risk

- **Assume radio is visible.** Transmissions can be located with direction-finding equipment. Transmit briefly and only when needed.
- **Assume devices can be searched.** Lock phones with a strong passcode, not just biometrics, and use disappearing messages.
- **Document.** Note times, locations and what stopped working. Groups such as OONI and Access Now use reports from the ground to prove and publicise shutdowns.

## After

Write down what worked and what did not, and fix the gaps before the next one. Shutdowns tend to repeat.

## Sources

- Access Now, *#KeepItOn* campaign and shutdown reports: <https://www.accessnow.org/campaign/keepiton/>
- OONI, *Internet shutdowns and network measurement*: <https://ooni.org/>
- Briar Project, *How it works*: <https://briarproject.org/how-it-works/>
- Meshtastic documentation: <https://meshtastic.org/docs/introduction/>
- F-Droid documentation, *Nearby swap*: <https://f-droid.org/docs/>
- Kiwix: <https://kiwix.org/>
