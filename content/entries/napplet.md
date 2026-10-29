---
title: "Napplets (NIP-5D): Sandboxed Nostr Applets"
slug: napplet
type: deep-dive
pillars: [apps, identity]
readiness: experimental
description: "Napplets are small sandboxed Nostr web apps that never touch your keys: a trusted shell brokers signing, relays and storage. How NIP-5D works and its limits."
dek: "Turn the Nostr client inside out: a trusted shell holds the keys and the relay connections, and small single-purpose applets run in a browser sandbox and ask the shell for everything. Published as signed, content-addressed Nostr events, so anyone can host them and any compatible shell can run them."
updated: 2026-10-29
created: 2026-10-29
origin: original
related: [sovereign-applications, nsite, blossom, nostr-protocol, nostr-key-custody, object-capabilities, zapstore]
aliases: ["napplet", "NIP-5D", "Nostr Web Applets", "Nostr Applet Protocol", "NAP"]
tags: ["napplet", "nostr", "nip-5d", "sandbox", "capabilities", "applets", "deep-dive"]
---

A **napplet** (Nostr applet) is a small web app that does one thing, such as a feed, a chat window, a profile editor or a relay manager, and runs inside a host application called a **shell**. The napplet never holds your signing key, never opens a relay connection and never reads the shell's storage. It sends typed messages to the shell, and the shell decides whether to sign, fetch, store or refuse. The protocol is **NIP-5D**, an open draft proposal to the Nostr NIPs repository. The project site is [napplet.run](https://napplet.run/).

The problem it targets is that Nostr clients are monoliths. Each client re-implements feeds, DMs, profiles and relay handling, and each one asks for direct access to your key. Installing a client means trusting all of its code with your identity. NIP-5D splits that: one shell you trust holds the authority, and everything else runs contained and composable.

## How it works

**Sandbox.** On the web, a napplet runs in an iframe with `sandbox="allow-scripts"` and, by rule, **without** `allow-same-origin`. That gives it an opaque origin: no `localStorage`, `IndexedDB`, cookies or service workers of its own, and no way to read the shell's. The spec forbids shells from exposing `window.nostr` (the NIP-07 signer interface) to napplets. Signing and encryption are only ever done by the shell. Because a sandboxed `srcdoc` document cannot carry an HTTP Content-Security-Policy header, the draft tells shells to inject a strict CSP `meta` tag (by default `connect-src 'none'`) so a napplet cannot simply open its own network connections.

**Messages.** The shell injects a `window.napplet` object holding only the capability domains it has granted. Calls travel over `postMessage` as JSON envelopes of the form `{ "type": "domain.action", ...payload }`. The shell identifies the sender by `MessageEvent.source`, the browser's unforgeable reference to the iframe window, and silently drops messages from any window it did not create. Unknown message types are ignored, so a napplet cannot probe for capabilities it was not given.

**Capability domains (NAPs).** NIP-5D itself is a thin core: envelope, sandbox and identity rules. What a napplet can actually ask for is defined by separate **NAP** (Nostr Applet Protocol) specs, one per domain, such as relay access, identity, intents for opening another napplet by role, inter-napplet communication and theming. They live in the [NAPs registry](https://github.com/napplet/naps). A napplet's manifest lists the domains it requires (`R` tags) and can use (`O` tags). These are declarations, never grants: the shell decides what to expose, and a napplet must degrade gracefully when a domain is missing.

**Publishing and identity.** A napplet is a single self-contained `index.html`. The author publishes a signed Nostr **manifest event** (kinds `5129`, `15129` or `35129` in the current draft) whose `x` tag is the SHA-256 of that file, plus hints for the [Blossom](/kb/blossom/) servers that store it. Before running anything, the shell fetches the manifest from relays, verifies its signature, downloads the blob by hash, checks the hash, and loads the verified bytes into the iframe. The napplet's identity is the pair (manifest `d` tag, artifact hash), computed from the bytes that actually run. A gateway may serve the file faster, but the draft says its output must be verified and it is never trusted. Static sites published the same way are [nsites](/kb/nsite/) (NIP-5A).

**Software.** The applet-side SDK (`@napplet/core`, `@napplet/shim`, `@napplet/sdk`, a Vite plugin that hashes and signs the manifest, a CLI and conformance tools) is MIT-licensed at [github.com/napplet/napplet](https://github.com/napplet/napplet). [Kehto](https://github.com/kehto/web) is the first host runtime and shell, with packages for ACLs, dispatch, services and a browser playground. The NIP-5D proposal lists further implementations, including Amethyst, the Grimoire web OS and several game and app platforms. The model is transport-agnostic by design: the web iframe is the first "projection", and native-process and WebAssembly bindings are described as possible.

## What it protects against

- **Every app holding your key.** Napplets never see the key or a signer interface. A malicious or buggy feed widget cannot sign as you; it can only ask the shell, which can refuse.
- **Tampered or swapped code.** The shell runs only bytes whose hash matches a manifest signed by the author's key, so a hosting server or gateway cannot alter a napplet unnoticed.
- **Lock-in to one client.** A napplet written to NIP-5D can run in any compatible shell, and a shell can host napplets from many authors. Features stop being welded to a single client.
- **Silent exfiltration through the network.** With the recommended CSP, a napplet cannot open its own connections; relay traffic goes through the shell.

## What it trusts, and the limits

- **The shell.** It holds the keys and brokers every request. A malicious or careless shell defeats the model. NIP-5D explicitly does not protect against a compromised browser, a malicious shell, side channels or social engineering.
- **The browser sandbox.** Isolation rests on the browser's iframe sandbox. A shell that adds `allow-same-origin` or skips the CSP breaks the guarantees.
- **The author's key.** Verification proves the bytes came from whoever holds the manifest's key, not that the napplet is honest. The optional `source` tag points to source code but, as the draft says, does not attest that the source reproduces the artifact.
- **Consent fatigue.** The shell asks the user to approve sensitive requests. Users who approve everything gain little.
- **Availability.** Manifests live on relays and blobs on Blossom servers; both can drop data. Mirroring across several helps.
- **A moving target.** The NIP is an open draft, NAPs are not final, and the SDK and Kehto both describe themselves as alpha: "for adventurers only".

## Readiness

**Experimental.** The design is careful and the security reasoning is written into the spec, but NIP-5D is an unmerged draft (opened April 2026), its capability contracts are still changing, and the tooling warns of breakage. It is worth following, and worth building on if you accept churn. Do not treat any shell as audited.

## Primary sources

- Project site: https://napplet.run/
- NIP-5D draft (pull request to nostr-protocol/nips): https://github.com/nostr-protocol/nips/pull/2303
- NAP capability registry: https://github.com/napplet/naps
- Napplet SDK (MIT): https://github.com/napplet/napplet
- Kehto runtime and shell: https://github.com/kehto/web · demo: https://kehto.github.io/web/
- NIP-5A (nsites, the static-site sibling): https://github.com/nostr-protocol/nips/blob/master/5A.md
- NIP-07 (browser signer interface that napplets must not receive): https://github.com/nostr-protocol/nips/blob/master/07.md
