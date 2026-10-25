---
title: "Kiwix"
slug: kiwix
type: deep-dive
pillars: [storage, circumvention]
readiness: usable
description: "Kiwix reads Wikipedia and other ZIM archives offline, while kiwix-serve shares a local library with browsers during outages or shutdowns."
dek: "Download a reference library while you have connectivity, then keep reading when the internet disappears."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [bittorrent-archives, internet-shutdown-preparedness, private-file-sync-and-backup, compare-storage, community-networks]
tags: [kiwix, zim, offline, archives, circumvention]
---

## Summary

Kiwix makes downloaded reference material usable offline. Its readers open **ZIM archives**, including Wikipedia and other collections of web content. You keep the archive locally and browse it without a live connection to the original website.

For shutdown preparedness, that changes the problem from reaching a blocked service to having a usable copy already present. It supplies reference material rather than live communication or access to pages you did not download.

## How it works

ZIM packages web content into a compressed archive. Kiwix Reader opens that archive as a browsable library. The openZIM project's **libzim** is the reference library for reading and writing the format.

The Kiwix catalog offers different collections and variants. For Wikipedia, documented variants include **mini** with article introductions and infoboxes, **nopic** with full articles without images, and **maxi** with the full version. Select the language and content variant you actually need, then check its listed size against available storage.

**kiwix-serve** is an HTTP server for ZIM files, supplied in `kiwix-tools`. A computer with the archives can serve nearby devices over a local network; readers use ordinary browsers. The server and local network must stay available, but their internet uplink need not be working.

For example, after installing the tools and obtaining a ZIM file:

```sh
kiwix-serve -p 8080 /path/to/archive.zim
```

Replace the path with the downloaded archive. Test browser access from another device on the intended local network before depending on it.

## Trust model / threat model

Choose the archive publisher as carefully as the source website: offline availability does not establish the accuracy or completeness of its contents. Keep the reader and archive together in your preparation plan, and inspect the archive's date and included material.

Local serving introduces a host and network that can observe requests. The server documentation states that kiwix-serve speaks HTTP without TLS; it recommends a reverse proxy for deployments needing HTTPS. Treat an ordinary shared local server as a reference service, not a confidential browsing channel.

## Readiness

**Usable** for offline reading and local reference servers, with downloadable readers, archives and documented server tools. Readiness during an outage depends on preparation: obtain the files, open them and test the equipment while connectivity is still available.

## Limits

An archive is a snapshot. It will not acquire new articles or corrections while disconnected. Missing images or omitted articles cannot be supplied by the reader. Devices still need storage, working hardware and power; a shared library also depends on its server.

Use [Internet Shutdown Preparedness](/guides/internet-shutdown-preparedness/) to plan the wider outage setup. [BitTorrent for Archive Distribution](/kb/bittorrent-archives/) covers distributing fixed copies, and [Private File Sync and Backup](/guides/private-file-sync-and-backup/) covers keeping a separate offline archive of your own files.

## Primary sources

- [Kiwix Reader: ZIM archives, Wikipedia variants and offline use](https://get.kiwix.org/applications/kiwix-reader/).
- [Kiwix Server: local serving, command syntax and HTTP limitations](https://get.kiwix.org/applications/kiwix-server/).
- [Kiwix command-line tools](https://github.com/kiwix/kiwix-tools).
- [openZIM libzim reference implementation](https://github.com/openzim/libzim).
