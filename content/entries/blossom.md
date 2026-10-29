---
title: "Blossom: Blob Storage on Nostr"
slug: blossom
type: deep-dive
pillars: ["storage", "identity"]
readiness: experimental
description: "Blossom stores files addressed by SHA-256 hash on ordinary HTTP servers, with Nostr keys for authorisation: simple, mirrorable blob storage for Nostr."
dek: "A pragmatic storage protocol for Nostr media: blobs are addressed by SHA-256, stored on ordinary HTTP media servers, and managed with Nostr-key authorization. Blossom makes files portable across Nostr clients without pretending that every media server is a blockchain or a global DHT."
updated: 2026-04-28
created: 2026-04-28
origin: vault
source: "12-Decentralized-Storage/Blossom.md"
aliases: ["Blossom Protocol", "Blobs stored simply on mediaservers"]
tags: ["blossom", "nostr", "decentralized-storage", "media", "blobs", "deep-dive"]
---

## What Blossom Is

Blossom stands for "Blobs stored simply on mediaservers." It specifies HTTP endpoints for storing and retrieving binary blobs from publicly accessible servers. Users authenticate with Nostr keys, and clients can discover the user's preferred servers through a replaceable Nostr event.

Core pieces:

- **Blob.** Binary data addressed by its SHA-256 hash.
- **Server.** HTTP endpoint that stores and serves blobs.
- **Authorization.** Nostr-signed authorization events, currently kind `24242` in the Blossom specs.
- **User server list.** Nostr replaceable event kind `10063`, listing the Blossom servers a user uses.
- **BUDs.** Blossom Upgrade Documents that define endpoints and optional features.

Blossom is not a storage blockchain. It is closer to "Nostr-authenticated object storage with content-addressed URLs."

## Protocol Shape

Important endpoints from the BUD specs:

| Endpoint | Purpose |
|----------|---------|
| `GET /<sha256>` | Retrieve blob bytes |
| `HEAD /<sha256>` | Check blob existence and metadata |
| `PUT /upload` | Upload raw blob bytes |
| `DELETE /<sha256>` | Delete a blob where policy permits |
| `PUT /mirror` | Ask a server to mirror a remote blob |
| `PUT /media` | Media-specific upload / optimization path |

Blob descriptors include:

- `url`
- `sha256`
- `size`
- `type`
- `uploaded`

BUD-02 requires upload servers to hash the exact bytes received. That lets users re-upload the same blob to another server and keep the same identifier.

## User Server Lists

BUD-03 defines a Nostr event kind `10063` that advertises the servers a user trusts for their blobs:

```json
{
  "kind": 10063,
  "content": "",
  "tags": [
    ["server", "https://cdn.self.hosted"],
    ["server", "https://cdn.satellite.earth"]
  ]
}
```

Clients can use this list when the original media URL fails: extract the 64-character SHA-256 hash from the URL, fetch the author's server list, then try the listed Blossom servers in order.

This is the key Nostr-native property: media availability follows the author, not the original CDN URL.

## Blossom vs NIP-96 and NIP-94

| Spec | Role |
|------|------|
| Blossom BUDs | HTTP blob server protocol |
| NIP-94 | Nostr file metadata event |
| NIP-96 | HTTP file storage server API for Nostr |

Blossom overlaps with NIP-96 but is intentionally content-hash centered. BUD-08 maps Blossom blobs to Nostr file metadata tags so clients can interoperate with NIP-94-style metadata.

## Where It Fits

| Use case | Fit |
|----------|-----|
| Nostr avatars and images | Strong |
| Podcast clips / short video | Strong if server limits allow |
| Client-portable media posts | Strong |
| Large private backups | Poor; use encrypted object storage |
| Immutable public archive | Pair with Arweave or IPFS |
| High-censorship publishing | Mirror across many Blossom servers plus IPFS/Arweave |

Blossom's practical job is making Nostr media less brittle. It does not remove the need for mirrors, payments, or local encryption.

## Threat Model

Blossom improves:

- **Integrity.** The URL contains a SHA-256 hash; clients can verify bytes.
- **Identity binding.** Upload and management actions use Nostr-key authorization.
- **Portability.** Users can advertise several servers and move media across them.
- **Mirroring.** BUD-04 gives a protocol path for copying blobs between servers.

Blossom does not automatically provide:

- **Confidentiality.** Blobs are public unless encrypted before upload.
- **Guaranteed retention.** Each server has its own limits, terms, quotas, and payment policy.
- **Anonymity.** Uploads and retrievals are HTTP requests visible to servers and network observers unless routed through privacy layers.
- **Global replication.** Mirroring is explicit client/server behavior, not an automatic swarm.

## Operational Pattern

For a robust Nostr media identity:

1. Run or pay for a primary Blossom server.
2. Publish kind `10063` with two or more server URLs.
3. Upload important media to all listed servers or use BUD-04 mirroring.
4. Include NIP-94 metadata for media-rich clients.
5. Mirror public high-value artifacts to IPFS or Arweave.
6. Strip EXIF and encrypt sensitive files before upload.

## Attack Surface

| Attack | Mitigation |
|--------|------------|
| Server deletes blob | Mirror to several servers; publish kind `10063` |
| Server swaps bytes | Verify SHA-256 from URL / descriptor |
| Key compromise | Rotate Nostr identity or delegate upload keys carefully |
| Metadata leak | Strip EXIF; avoid uploading sensitive media raw |
| Server logs retrievals | Use Tor/VPN or fetch through privacy-preserving clients |
| CDN/domain takedown | Use multiple Blossom servers and content-hash fallback |

## Primary Sources

- Blossom specification and BUDs — [github.com/hzrd149/blossom](https://github.com/hzrd149/blossom)
- BUD-01, *Server requirements and blob retrieval*.
- BUD-02, *Blob upload*.
- BUD-03, *User Server List*.
- BUD-04, *Mirroring blobs*.
- BUD-08, *Nostr File Metadata Tags*.
- BUD-11, *Nostr Authorization*.
- Nostr NIPs — [github.com/nostr-protocol/nips](https://github.com/nostr-protocol/nips)

Compare the storage and replication choices in [Choosing Decentralized Storage](/kb/compare-storage/) and [Hypercore and Hyperdrive](/kb/hypercore/).

Blossom also hosts the files behind [nsites](/kb/nsite/) and [napplets](/kb/napplet/), which list their blobs by hash in signed Nostr manifests.
