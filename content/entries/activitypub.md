---
title: "ActivityPub"
slug: activitypub
type: deep-dive
pillars: [identity, messaging]
readiness: usable
description: "ActivityPub connects social servers through actors and inboxes. Learn what federation, account migration and instance moderation actually provide."
dek: "Federation lets independently operated services exchange activity; the account still has a home server."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [decentralized-identity, nostr-protocol, at-protocol, radicle, identity-and-pseudonymity]
---

## Summary

ActivityPub is a W3C Recommendation for social-network communication. It specifies both a client-to-server API and server-to-server federation, using ActivityStreams data. Implementations may support either layer or both; federation support does not imply support for the standard client API.

## How it works

An **actor** represents a participant, such as a person or application. Its **outbox** exposes activities it has published; its **inbox** receives activities addressed to it. In federation, a sending server delivers activities to recipients' inboxes. Activities include creating a post, following an actor and undoing an earlier action.

The [ActivityPub Recommendation](https://www.w3.org/TR/activitypub/) defines delivery and authorization behavior. Applications still need agreement about object types and behavior beyond the base protocol. [ForgeFed](/kb/radicle/) applies this model to code collaboration.

## Trust model / threat model

The server serving an account handles its storage, access and delivery. Federation distributes those responsibilities among operators; it does not remove them. ActivityPub's security considerations explicitly discuss trusting servers and the difficulty of ensuring remote copies are deleted. Choose an instance as part of [identity and pseudonymity](/kb/identity-and-pseudonymity/) planning.

### Account migration has specific limits

ActivityStreams defines a general **Move** activity. It is not a universal account-backup format. [Mastodon's migration documentation](https://docs.joinmastodon.org/user/moving/) describes a particular workflow: prepare the destination account, alias the old account there, then initiate the move from the old account. Followers move when their software supports Move. Posts do not move; follows and other supported lists require separate export and import.

Prepare while you can still access the old account. Do not promise recovery from a vanished or uncooperative server merely because it federates.

### Defederation is an operator decision

Mastodon supports domain-level moderation. A domain suspension removes existing follow relationships between local accounts and accounts on that domain; reversing the block does not restore them. A domain limit has different effects. These are [Mastodon moderation rules](https://docs.joinmastodon.org/admin/moderation/), not a single mandatory policy imposed by ActivityPub.

## Readiness

**Usable.** A published standard and documented operational implementations support practical federation. Check the specific services' object support, moderation rules and migration behavior before depending on interoperability.

## Limits

Treat migration, content backup and availability as separate tasks. Federation also does not turn a public post into confidential communication; use the [messaging comparison](/guides/choosing-a-secure-messenger/) when that is the requirement.

## Primary sources

- [W3C ActivityPub Recommendation](https://www.w3.org/TR/activitypub/)
- [W3C ActivityStreams vocabulary, including Move](https://www.w3.org/TR/activitystreams-vocabulary/)
- [Mastodon account migration](https://docs.joinmastodon.org/user/moving/)
- [Mastodon moderation](https://docs.joinmastodon.org/admin/moderation/)
