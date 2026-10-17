---
title: "Getting Started on Nostr Safely"
slug: nostr-getting-started
type: guide
pillars: [identity, messaging]
description: "Create a Nostr identity you control, keep your private key out of web apps with a signer, choose relays and clients, and understand what Nostr makes public."
dek: "On Nostr your identity is a key pair, not an account. Nobody can ban you from the protocol, and nobody can recover your key if you lose it."
updated: 2026-10-17
created: 2026-10-17
origin: original
level: beginner
time: "30 minutes"
related: [nostr-protocol, nostr-identity, nostr-key-custody, remote-signing, nostr-web-of-trust, marmot-protocol, blossom]
---

Nostr ("Notes and Other Stuff Transmitted by Relays") is a simple open protocol. You have a key pair. You sign messages ("events") with your private key and send them to relays, which are servers anyone can run. Anyone who knows your public key can fetch your events from those relays and verify that you wrote them. If one relay bans you, you post to others; your followers find you by key, not by server. The design is explained in [Nostr: The Protocol](/kb/nostr-protocol/) and [Nostr as an Identity Layer](/kb/nostr-identity/).

## 1. Understand your keys

- Your **public key** (shown as an `npub1…` string) is your identity. Share it freely.
- Your **private key** (`nsec1…`) *is* your account. Anyone who has it can post as you, forever. It cannot be reset or changed.

There is no password reset on Nostr. Treat the private key like the seed of a Bitcoin wallet. Long-term custody and recovery options are covered in [Nostr Key Custody and Recovery](/kb/nostr-key-custody/).

## 2. Keep the private key in a signer, not in apps

The most common way people lose Nostr identities is by pasting their `nsec` into many websites and apps. Instead, keep it in one place that signs on request:

- **Browser extension signers (NIP-07)** such as nos2x or Alby hold the key and let web clients request signatures.
- **Android signer apps (NIP-55)** such as Amber hold the key for other apps on the phone.
- **Remote signers ("bunkers", NIP-46)** hold the key on a separate device or service and sign over Nostr itself; clients receive a connection string, never the key. See [Remote Signing](/kb/remote-signing/).
- If you must store the key as text, use the **password-encrypted format (NIP-49, `ncryptsec1…`)**.

Back up the key offline, on paper or metal, before you build an audience you would hate to lose.

## 3. Pick a client

Popular clients include Damus (iOS), Amethyst (Android), Primal (web and mobile), and Coracle, noStrudel and Snort (web). They differ in features and in how many relays they contact. Amethyst can route connections through Tor.

## 4. Choose your relays

Clients come with default relays. Publish a **relay list (NIP-65)** so others know where to find your posts ("outbox" relays) and where to send you mentions ("inbox" relays). Use a few well-run public relays plus, ideally, one you control or pay for. Paid relays tend to have less spam.

## 5. Optional: a readable name and payments

- **NIP-05** maps an internet identifier like `name@example.com` to your key. It is convenient but relies on DNS and on whoever runs that domain; your key remains the real identity.
- **Zaps (NIP-57)** let people send you Lightning payments tied to posts; you need a Lightning address. **Nostr Wallet Connect (NIP-47)** lets a client use a wallet you control.

## 6. Know what is public

- **Posts, follows, reactions and profile data are public** and signed. Relays and anyone who copies them can keep them forever; deletion requests (NIP-09) are only requests.
- **Relays see your IP address** unless you connect through Tor or a VPN.
- **Old-style direct messages (NIP-04) leak metadata:** the sender, recipient and timing are visible to relays even though the content is encrypted. Use clients that support **private direct messages (NIP-17)**, which encrypt with NIP-44 and hide sender and timing inside "gift-wrapped" events (NIP-59). For group chats, see [Marmot: MLS over Nostr](/kb/marmot-protocol/).
- **Use separate keys** for identities that must not be linked. One key per persona.

## 7. Filtering and trust

Nostr has no central moderation. Clients use your follow graph and "web of trust" signals to filter spam and abuse. See [Web of Trust on Nostr](/kb/nostr-web-of-trust/).

## Sources

- Nostr Implementation Possibilities (NIPs) repository: <https://github.com/nostr-protocol/nips>
- NIP-01 (basic protocol), NIP-07, NIP-17, NIP-19, NIP-44, NIP-46, NIP-49, NIP-55, NIP-57, NIP-59, NIP-65 in the same repository
- nostr.how, beginner documentation: <https://nostr.how/>
- Amber signer: <https://github.com/greenart7c3/Amber>
