---
title: "nsite (NIP-5A): Static Websites on Nostr and Blossom"
slug: nsite
type: deep-dive
pillars: [apps, storage]
readiness: experimental
description: "An nsite is a static website published as a signed Nostr event mapping paths to SHA-256 hashes, with files on Blossom servers. How NIP-5A works and its limits."
dek: "Publish a website with no host account and no registrar: a signed Nostr event lists every file by hash, the files sit on interchangeable Blossom servers, and any gateway can serve the site under your npub."
updated: 2026-10-29
created: 2026-10-29
origin: original
related: [sovereign-applications, napplet, blossom, nostr-protocol, uncensorable-website, ipfs-and-filecoin, ipns-dnslink, compare-storage]
aliases: ["nsite", "nsites", "NIP-5A", "Nostr static sites", "Pubkey static websites"]
tags: ["nsite", "nostr", "nip-5a", "blossom", "static-site", "publishing", "deep-dive"]
---

An **nsite** is a static website whose table of contents is a signed Nostr event. Each file (HTML, CSS, JavaScript, images) is stored as a blob on one or more [Blossom](/kb/blossom/) servers under its SHA-256 hash, and a **site manifest** event maps each path to a hash. Because the site is addressed by the author's public key rather than a domain, no registrar can seize the name and no single host holds the only copy. The format is **NIP-5A**, a draft NIP merged into the Nostr NIPs repository. Napplets ([NIP-5D](/kb/napplet/)) use the same building blocks for sandboxed apps.

## How it works

**Manifest.** A root site uses replaceable event kind `15128`, one per pubkey. Named sites, which work like subdomains under the same key, use addressable kind `35128` with a short `d` tag. The manifest carries one `path` tag per file, `["path", "/index.html", "<sha256>"]`, optional `server` tags hinting which Blossom servers hold the blobs, and optional `title`, `description` and `source` tags. An `x` tag can carry an **aggregate hash** of all the path tags, so identical site versions published by different keys can be recognised as the same site.

**Snapshots and copies.** A kind `5128` snapshot captures a site version at a point in time, so history stays addressable even after the replaceable manifest is updated. Copied sites record their parent (`a`) and origin (`A`) for provenance.

**Serving.** Browsers do not speak Nostr, so a **host server** (gateway) resolves the site. The canonical forms are `<npub>.gateway` for a root site and a base36 pubkey followed by the `d` tag for named sites. The gateway finds the manifest on relays, looks up the requested path, fetches the blob from the listed servers (or the author's Blossom server list), and returns it. The spec says it **should** check that each blob's hash matches the manifest and treat mismatches as not found. Public gateways such as [nsite.lol](https://nsite.lol/) exist, and anyone can run one, including on their own machine, with open-source code such as [nsite-gateway](https://github.com/hzrd149/nsite-gateway).

**Publishing.** Tools such as [nsyte](https://github.com/sandwichfarm/nsyte) (MIT) upload the files to Blossom servers and sign and publish the manifest with your key or a remote signer.

## What it protects against

- **Name seizure.** The address is your key. There is no domain to suspend, although a gateway's own domain can still be blocked.
- **Host takedown.** Files are content-addressed, so any Blossom server holding the same bytes can serve them, and you can mirror to as many as you like.
- **Silent tampering by servers.** A verifying gateway or client rejects files that do not match the signed hashes.
- **Lost history.** Snapshots keep earlier versions addressable.

## What it trusts, and the limits

- **The gateway, unless you verify yourself.** Visiting an nsite through someone else's gateway means trusting that gateway to verify hashes honestly and not to log your visits. Running a local gateway removes that trust.
- **Gateway domains are chokepoints.** Censors can block well-known gateways by DNS or IP, even though the site itself survives elsewhere.
- **Your key.** Whoever holds the key can replace the site. Lose it and you cannot update the site; leak it and someone else can. See [Nostr key custody](/kb/nostr-key-custody/).
- **Retention.** Relays and Blossom servers can delete data or go offline. Nothing pays anyone to keep your files, so publish to several of each.
- **Static only.** An nsite is static files. Dynamic behaviour has to come from client-side code talking to relays, or from separate services.
- **No moderation layer, by design.** Anyone can publish, and public gateway listings show plenty of spam. Discovery and curation are left to clients and webs of trust.

## Readiness

**Experimental.** NIP-5A is a merged draft with several gateways, publishing tools and many live sites, from personal pages to Nostr clients. The format is still being refined (aggregate hashes and snapshots were added in 2026), gateway behaviour varies, and visitors usually depend on a third-party gateway. It works today for publishing static content that should outlive any one host.

## Primary sources

- NIP-5A specification: https://github.com/nostr-protocol/nips/blob/master/5A.md
- Aggregate hash and snapshots change (merged): https://github.com/nostr-protocol/nips/pull/2287
- Blossom specification: https://github.com/hzrd149/blossom
- nsite-gateway (MIT): https://github.com/hzrd149/nsite-gateway
- nsyte publishing CLI (MIT): https://github.com/sandwichfarm/nsyte
- nsite CLI (AGPL-3.0): https://github.com/lez/nsite
- Public gateway and site listing: https://nsite.lol/
