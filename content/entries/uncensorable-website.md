---
title: "Publishing an Uncensorable Website"
slug: uncensorable-website
type: guide
pillars: [naming, anonymity, storage]
description: "How to publish so that no single registrar, host or government can take you offline: onion services, content-addressed mirrors, independent naming and multiple jurisdictions."
dek: "Every single point of control is a point of censorship. Remove them one by one: the host, the domain, the location of the server, the format."
updated: 2026-10-17
created: 2026-10-17
origin: original
level: advanced
time: "half a day"
related: [onion-and-i2p-naming, decentralized-dns, ipfs-and-filecoin, arweave, ens, handshake, pkarr, censorship-circumvention]
---

A conventional website can be taken down at many points: the domain registrar or registry suspends the name, the hosting company deletes the server, a CDN drops the account, the ISP blocks the IP address, a court orders search engines to delist it. Resilient publishing means having more than one answer at each of those points.

## The layers of control

| Layer | Who can censor | How to route around |
|---|---|---|
| Domain name | Registrar, registry, ICANN-level pressure | Onion address; ENS, Handshake or PKARR names; several domains in different TLDs ([Decentralized DNS](/kb/decentralized-dns/)) |
| Host | Hosting company, its government | Self-hosting; several hosts in different jurisdictions; content-addressed storage |
| Server location | Anyone who can find the IP | Tor onion service: the server's location is hidden |
| Network path | ISPs and national firewalls | Onion service (reachable through Tor and bridges); mirrors |
| Format | Platforms and app stores | Static files that anyone can copy, mirror and reseed |

## 1. Make the site static

A static site (plain HTML, CSS and images, generated once) can be copied, mirrored, hashed, pinned and served by anything. It has no database to breach and no server-side code to exploit. This site is built that way.

## 2. Publish an onion service

A Tor onion service is reachable only through Tor, hides the server's location, and has a self-authenticating address derived from its public key: nobody can seize or reassign it. On a server with Tor installed, add to `torrc`:

```
HiddenServiceDir /var/lib/tor/mysite/
HiddenServicePort 80 127.0.0.1:8080
```

Restart Tor; the address appears in `/var/lib/tor/mysite/hostname`. Serve your static files on `127.0.0.1:8080` only, so the server is not also exposed directly. **Back up the `hs_ed25519_secret_key` file** in that directory: it *is* the address. If you also run a clearnet site, add an **Onion-Location** HTTP header so Tor Browser users are offered the onion version automatically. For high-risk services, read the Tor Project's onion service security guidance, including the *vanguards* defences against guard discovery.

## 3. Add content-addressed mirrors

With **IPFS**, content is addressed by its hash (a CID), so any node holding the files can serve them and nobody can alter them without changing the address. Publish the site directory, then make sure it is **pinned on several independent nodes** (your own, friends', pinning services in different countries): content that nobody pins disappears. Use IPNS or DNSLink to point a stable name at the latest version. See [IPFS and Filecoin](/kb/ipfs-and-filecoin/).

For permanence, **Arweave** stores data with an up-front payment intended to fund storage indefinitely ([Arweave](/kb/arweave/)). For distribution among people who already trust each other, a **BitTorrent** magnet link or a signed archive works with tools millions already have.

## 4. Use names that cannot be seized

- Your **onion address** cannot be seized, only blocked or forgotten.
- An **ENS name** can point to an IPFS content hash (ENSIP-7 `contenthash`); it is controlled by your Ethereum key, though it depends on Ethereum and its gateways ([ENS](/kb/ens/)).
- **Handshake** names are owned on their own blockchain and resolved without ICANN ([Handshake](/kb/handshake/)).
- **PKARR** publishes DNS records signed by your key into the BitTorrent Mainline DHT, so a public key becomes a domain ([PKARR](/kb/pkarr/)).
- Keep **ordinary domains** too, in several TLDs and with registrars in different jurisdictions; most readers still arrive that way.

Publish all your addresses together, signed by a key your readers know, so people can tell a real mirror from an impostor.

## 5. Spread across jurisdictions

Host mirrors with providers in different countries with different laws, paid for in ways that do not all trace back to one account. Use providers that accept anonymous payment if the site's existence is itself dangerous to you.

## 6. Make it easy to mirror

Publish a downloadable archive of the whole site and its checksum, signed with your key. The more copies exist in the hands of readers, the less any takedown matters. Nostr long-form posts (NIP-23) are another way to get text onto many independent relays at once.

## 7. Protect the publisher

Censorship resistance protects the content; it does not by itself protect the author. If your identity is the risk, keep publishing infrastructure separate from your personal identity, administer it over Tor, and pay for it anonymously. Start with [Threat Modeling](/guides/threat-modeling/).

## Sources

- Tor Project, *Set up your onion service*: <https://community.torproject.org/onion-services/setup/>
- Tor Project, *Onion-Location*: <https://community.torproject.org/onion-services/advanced/onion-location/>
- Tor Project, *Advanced onion service topics*: <https://community.torproject.org/onion-services/advanced/>; vanguards add-on: <https://github.com/mikeperry-tor/vanguards>
- IPFS documentation, *Host a single-page website* and *Pinning*: <https://docs.ipfs.tech/>
- DNSLink: <https://dnslink.dev/>
- ENSIP-7, *Contenthash field*: <https://docs.ens.domains/ensip/7>
- NIP-23, *Long-form content*: <https://github.com/nostr-protocol/nips/blob/master/23.md>
