---
title: "Running Infrastructure for Freedom"
slug: running-freedom-infrastructure
type: guide
pillars: [anonymity, circumvention, mesh, money]
description: "Ways to contribute capacity to free networks, from a Snowflake proxy in your browser to Tor bridges and relays, Nostr relays, Bitcoin nodes and solar mesh repeaters."
dek: "Every one of these networks is only as strong as the number of independent people running it. Here is how to become one of them."
updated: 2026-10-17
created: 2026-10-17
origin: original
level: intermediate
time: "10 minutes to a weekend"
related: [tor, using-tor-safely, building-a-mesh, bitcoin-self-custody, nostr-getting-started, i2p, reticulum, nym]
---

Decentralised networks are not decentralised by design alone; they are decentralised because many independent people run parts of them, in many countries, on many providers. If you live somewhere with an open internet and some spare bandwidth, you can give people behind firewalls a way out, and make every network on this site harder to capture.

Start with the lowest-risk, lowest-effort options and work up.

## Ten minutes: a Snowflake proxy

Snowflake lets censored Tor users connect through short-lived connections to volunteers. Running a proxy is as simple as installing the Snowflake browser extension, or running the standalone proxy on a server. Your IP address is never an exit: you only relay encrypted traffic into the Tor network. <https://snowflake.torproject.org/>

## An afternoon: a Tor bridge

A bridge is an unlisted Tor entry point. It carries no exit traffic, so the legal exposure is low, and because bridge addresses are distributed carefully, each new bridge helps people whose known bridges have been blocked. obfs4 and WebTunnel bridges are the most needed. A small VPS or home server with a stable IP address is enough. Guides: <https://community.torproject.org/relay/setup/bridge/>

## A weekend: a Tor relay

Middle (non-exit) relays add capacity and diversity to the network. They need a stable connection with decent bandwidth and an operator who keeps them updated. **Exit relays** are what the network most lacks, but they carry real legal exposure because abuse complaints arrive at the exit's address; run one only with a provider that allows it, ideally with a legal entity behind you, after reading the Tor Project's exit guidelines. Diversity matters: relays in under-represented countries and hosting providers are worth more than another relay in the largest data centres. <https://community.torproject.org/relay/>

## Other anonymity networks

- **I2P routers** relay traffic for others automatically once running, and help the network more the longer they stay up ([I2P](/kb/i2p/)).
- **Nym nodes** and **HOPR nodes** are staked, incentivised node roles in mixnets ([Nym](/kb/nym/), [HOPR](/kb/hopr/)). Read the operator documentation carefully; these involve tokens, bonding and uptime requirements.

## A Bitcoin node

A full node verifies every rule of Bitcoin itself and, if it accepts inbound connections, serves the blockchain to others. Running it over Tor as well as clearnet helps users connect privately. Bitcoin Core runs on modest hardware; packaged systems such as Umbrel and Start9 make it easier ([Bitcoin Self-Custody](/guides/bitcoin-self-custody/)).

## A Nostr relay

A relay is a small server that stores and forwards signed events. Running one for your community, your organisation or yourself reduces dependence on the large public relays. strfry and nostr-rs-relay are common implementations. Decide in advance who may write to it and how you will handle abuse and legal requests.

## A mesh repeater

A LoRa repeater on a rooftop or hilltop, powered by a small solar panel, can link a whole neighbourhood's Meshtastic or MeshCore radios ([Building a Local Mesh Network](/guides/building-a-mesh/)). A **Reticulum transport node** can bridge radio meshes to the internet and to each other ([Reticulum](/kb/reticulum/)).

## Storage and mirrors

Pin content that matters to you on IPFS, seed torrents of archives at risk of deletion, or host a mirror of a censored site in your jurisdiction ([Publishing an Uncensorable Website](/guides/uncensorable-website/)).

## Good operator habits

- **Keep software updated** and subscribe to the project's announcement list.
- **Separate it** from your personal machines and accounts.
- **Know your provider's terms** and your country's law before running anything that forwards other people's traffic.
- **Be transparent where it helps:** Tor exit operators commonly publish contact information and an explanation page, which resolves most abuse complaints.

## Sources

- Tor Project, *Snowflake*: <https://snowflake.torproject.org/>
- Tor Project, *Relay operations* (bridges, middle and exit relays, legal guidance): <https://community.torproject.org/relay/>
- I2P, *Getting started*: <https://geti2p.net/en/>
- Bitcoin Core, *Running a full node*: <https://bitcoin.org/en/full-node>
- strfry relay: <https://github.com/hoytech/strfry>
- Reticulum manual, *Transport nodes*: <https://reticulum.network/manual/>
