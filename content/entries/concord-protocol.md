---
title: "Concord Protocol"
slug: concord-protocol
type: deep-dive
pillars: ["messaging"]
readiness: experimental
description: "Concord, an open MIT-licensed specification for end-to-end encrypted communities on Nostr: its design, how it uses MLS ideas, and its maturity."
dek: "An MIT-licensed, open specification for end-to-end encrypted communities over Nostr — Discord/Slack-shaped (channels, roles, moderation) but bound to Nostr keys, portable across clients, and with no operator in the middle. The second major encrypted-group architecture on Nostr after Marmot Protocol, optimized for communities rather than conversation groups."
updated: 2026-08-23
created: 2026-08-23
origin: vault
source: "07-Encrypted-Messaging/Concord Protocol.md"
aliases: ["Concord", "CORD", "Concord encrypted communities"]
tags: ["concord", "nostr", "e2ee", "communities", "group-messaging", "moderation", "deep-dive"]
---

## What Concord is

Concord ([github.com/concord-protocol/concord](https://github.com/concord-protocol/concord)) defines encrypted communities whose entire state — membership, moderation actions, configuration, channels, invites — is carried as Nostr events signed by member keys. The spec is organized as numbered **CORD** documents (CORD-01 … CORD-09 and growing), each merged through pull requests like a NIP.

Design goals, as evidenced by the spec's trajectory:

- **Community state as portable identity state.** Every operation binds to Nostr npubs; a community survives any single client leaving (Vector, Armada, Amethyst, NoorNote, Nostria all implement or consume it).
- **Epoch-based rekeying.** Membership changes rotate encryption keys through epochs — the MLS group-safety property (forward secrecy across membership churn), applied to a community-shaped object.
- **Authority as keyholding, scope as derivation.** Who may write control-plane state, who may moderate, who may invite — each is a separate signing capability, not a database flag on a server.
- **Relay-agnostic.** Communities live across ordinary relays; no dedicated server required (contrast [Matrix and E2EE](/kb/matrix/)).

Status: **actively maturing at high velocity** (2026). Vector 0.4.0 moved its group chats from Marmot to Concord as the default transport (July 2026); Amethyst shipped a clean-room, wire-compatible implementation days later; Armada (Soapbox) is a co-equal client. The spec has moved from "proposal" to "the encrypted-community layer of the Nostr stack" within a year.

## Architecture: the CORD documents

| Document | Scope | Status (Aug 2026) |
|---|---|---|
| **CORD-01** | Core community model: genesis, epochs, membership | Merged |
| **CORD-02** | Control plane: metadata entity, `control_root` write-gates, relays, `av_brokers` (proposed) | §2 merged Aug 6–7 ([PR #15](https://github.com/concord-protocol/concord/pull/15)); [PR #22](https://github.com/concord-protocol/concord/pull/22) open |
| **CORD-04** | Message handling; §7 provable, rotation-proof pinning | Merged Aug 4 ([PR #13](https://github.com/concord-protocol/concord/pull/13)) |
| **CORD-05** | Invites: encrypted invite lists, lifecycle; §1 root-authentication at accept | Base merged; [PR #23](https://github.com/concord-protocol/concord/pull/23) codifying root-auth open |
| **CORD-07** | Audio/video rendezvous (broker selection) | Merged; being extended by PR #22 |
| **CORD-08** | Disappearing messages | Merged Aug 4 ([PR #14](https://github.com/concord-protocol/concord/pull/14)) |
| **CORD-09** | Blinded mention locators (private mentions without pubkey leakage) | Open ([PR #16](https://github.com/concord-protocol/concord/pull/16)) |
| **Community signals** | Pause signal (suspend chat without message loss) | Open ([PR #17](https://github.com/concord-protocol/concord/pull/17)) |
| **Sharded community list** | Membership list across **kind 33302** shards; removes the 50-member cap | **Merged Aug 15** ([PR #18](https://github.com/concord-protocol/concord/pull/18)) |

### The authority model

The 2026 hardening arc formalized **who may do what** as separate capabilities:

- **Members** hold derived read/verify keys — they can decrypt and verify all community state but cannot write control-plane changes.
- **`control_root` holders** (owners/staff) alone may write control-plane events (CORD-02 §2, merged Aug 6). This is explicitly framed as a spam barrier layered *over* the inner actor signatures — defense in depth, not a replacement for the signature model.
- **Invite links** are per-link revocable (tombstones), survive community refounding, and carry ban checks on recovery paths (Amethyst [PR #3888](https://github.com/vitorpamplona/amethyst/pull/3888) completed the lifecycle).
- **Community-owned configuration outranks member-asserted configuration** wherever the two could disagree — PR #22's principle, stated against routing on member-asserted broker tags: it "lets a fellow member's untrusted input outrank the community's own instruction."

### Scaling: sharding

Until August 2026 a single encrypted community list capped at ~50 memberships (relay size limits). PR #18 shards the list across **kind 33302** events with pruning of retired entries, removing the cap. Vector and Armada did a cross-client review pass (identical tie-breaking, no republishing unchanged data, renames don't inflate the list) *before* the merge — two implementations agreeing on semantics as a precondition is the convergence discipline that separates spec-text from spec-truth. Discord-scale communities are now spec-complete; production behavior under thousands of shards is the open empirical question.

### Moderation as amortized rekeying

Vector 0.4.2 (Aug 15) established the cost model: rapid bans **queue, stack, and settle as a single operation** — banning a wave of accounts costs one key rotation (one epoch) instead of one per account. Moderation economics under E2EE are rekeying economics; batching is what makes moderation survivable under spam.

## Timeline

- **2025** — Concord emerges as an MIT-licensed community protocol; Armada (Soapbox) adopts it.
- **Jul 8 2026** — Marmot spec marked adopted; but Vector (Jul 15, v0.4.0) retires Marmot as default group-chat transport in favor of Concord, shipping Concord v2 days later (slash-command bots, self-destruct timers, NIP-58 badges). Amethyst merges a clean-room wire-compatible implementation the same week.
- **Aug 4 2026** — CORD-04 §7 (message pinning) and CORD-08 (disappearing messages) merge.
- **Aug 6–7 2026** — **CORD-02 §2 merges**: control-plane writes gated by `control_root`.
- **Aug 15 2026** — **PR #18 merges**: sharded community lists (kind 33302), 50-member cap removed. Vector 0.4.2/0.4.3 ship the client half with cross-client review vs. Armada.
- **Aug 16–23 2026** — PR #22 (community-owned `av_brokers`) and PR #23 (CORD-05 §1 root authentication at accept — codifying what Vector/Armada already enforced, "never a live vulnerability, but never *required*") open. NoorNote 1.3.4/1.3.5 join via invite-link addon; Nostria 4.1.67 adds dissolution/admin administration.

## Why it matters for ungovernable tech

1. **Community without an operator.** The Discord-shaped object — the most commercially captive social form in existence — reconstructed as signed events on open relays. Exit is trivial: the community's state travels to any relay set; the members' keys are the root of trust.
2. **Authority never pools.** Delete/report/mediate authority decomposes into scoped signing capabilities (owner, staff, member, invite-holder), each independently revocable. Compare the NIP-09/NIP-56 authority split (author deletes own content; reports are allegations weighted by the verifier's trust graph — see [Overview - Web of Trust](/kb/web-of-trust/)).
3. **MLS-class safety, Nostr-class portability.** Rekeying epochs give membership-change forward secrecy without a delivery server; npub binding gives cross-client portability without an account system.
4. **The spec earns trust by codifying deployed behavior.** PR #23's honesty ("Vector already refused, Armada already dropped, but nothing *required* it") is the pattern: implementations lead, the spec follows what survived contact.

Trade-offs and open questions: relay dependence for availability (a community's events live wherever relays will store them); sharding at Discord scale is spec-complete but production-unproven; moderation under E2EE still leans on client cooperation for enforcement (the crypto guarantees non-members can't read, not that members behave); and the >50-member production data doesn't exist yet (merged Aug 15).

## Evidence at a glance

| Dimension | State (Aug 2026) |
|---|---|
| Spec | [concord-protocol/concord](https://github.com/concord-protocol/concord), MIT, CORD-01..09 + extensions; 7 PRs merged since Aug 4 |
| Clients | Vector (desktop+Android), Armada (Soapbox), Amethyst (clean-room), NoorNote (addon), Nostria (admin) |
| Maturity | Production for small/mid communities; sharding merged, >50-member deployments pending |
| Key kinds | 33302 sharded community lists; encrypted invite lists (CORD-05); NIP-78 encrypted community records (themes) |
| Authority model | `control_root` write-gates; member read keys; per-link revocable invites; community-signed config > member-asserted |
| Moderation | Batched bans → single epoch rekey; pause signal proposed (PR #17); blinded mentions proposed (CORD-09) |
| Watch next | PR #22/#23 merges; first >50-member communities; relay pagination under shard fan-out |
