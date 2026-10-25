---
title: "Buzz"
slug: buzz
type: deep-dive
pillars: ["identity"]
readiness: experimental
description: "Buzz, a self-hostable system that gives AI agents their own Nostr key pairs and identities: a production example of non-human actors on Nostr."
dek: "The production embodiment of \"AI agents as Nostr keypairs\": a self-hostable, now hosted-beta agent workspace where agents are created, owned, budgeted, recovered, and revoked as Nostr identities — publishing, chatting, transacting, and collaborating over relays like any other keyholder."
updated: 2026-10-25
created: 2026-08-23
origin: vault
source: "11-Identity/Buzz.md"
aliases: ["Buzz by Block", "Sprout", "Buzz agent workspace"]
tags: ["buzz", "nostr", "ai-agents", "agent-workspaces", "agent-identity", "sprout", "deep-dive"]
---

## What Buzz is

Buzz ([buzz.xyz](https://buzz.xyz); formerly **Sprout**) is an agent workspace from Block (Square) in which every agent is a Nostr identity. Its thesis: the agent-as-keypair model (see [AI Agent Identity on Nostr](/kb/ai-agent-identity-nostr/)) needs *operational* infrastructure to be usable — creation flows, usage accounting, recovery limits, budget summaries, community workspaces — and that infrastructure should itself ride open protocols (Nostr events, relays, NIP-78 encrypted records) rather than a proprietary control plane.

The June 2026 rebrand (Sprout → Buzz) coincided with publishing **personas, teams, and managed-agent records as Nostr relay events** — the workspace's own state became portable, identity-addressed data.

Two deployment models as of August 2026: **self-hosted** (primary) and a **hosted beta at buzz.xyz** — with no paid plans announced yet (per the Superset comparison page).

## The agent lifecycle as Nostr state

What distinguishes Buzz from a chat UI bolted onto an LLM is that agent lifecycle operations are protocol events:

| Lifecycle stage | Mechanism |
|---|---|
| Creation | Unified agent-creation flows (0.5.8) |
| Usage accounting | **NIP-AM agent usage tracking** — per-agent accounting (0.5.9) |
| Recovery | **Agent recovery limits** (0.5.10/0.5.11) — bounded how far/how often an agent can be recovered |
| Budgets | Budget summarizer with handoff summaries (0.5.8; reasoning fix so summaries don't starve) |
| Community membership | Agents join Concord-style encrypted communities; channel snapshots (0.5.10/0.5.11) |
| Publishing | Entity link previews for repos/PRs/issues; multi-repo projects (0.5.5) |
| Authorization | **Remote agent mention authorization** (0.5.17) — an @-mention does not silently convey authority |
| Identity records | Personas, teams, managed agents as relay events (rebrand release, Jun 2026) |

The 0.5.17 fix is the identity-architectural line in the sand: *mention ≠ authorization*. Being named in a message must not grant an agent the right to act — the same authority-scoping principle as Concord's `control_root` and World ID 4.0's Authenticators (authority is scoped, derivable, never transitively acquired).

## Release velocity

| Window | Releases | Highlights |
|---|---|---|
| Aug 5–12 2026 | 0.5.5 → 0.5.11 (7 releases) | Entity previews, multi-repo projects, NIP-AM usage tracking, agent recovery limits, encrypted NIP-78 community themes, huddle transcription for agents |
| Aug 13–22 2026 | 0.5.14 → 0.5.17 | Agent mention authorization, presence retry timers, CPU-burn fixes, h2 security bump |
| Community theming | Desktop PR #3653 / mobile PR #3767 | Themes as **encrypted NIP-78 records on the community's own relay**, synced cross-platform with identity-scoped caches |
| Custody | 0.5.3 (Jul 31) | NIP-49 encrypted local key backup; huddle transcription; hosted-community limit raised to five |

Release cadence is near-daily through August 2026 — the fastest-moving agent-identity project in this library's trackers.

## Why it matters for ungovernable tech

1. **Agent identity without a registry.** No issuer, no approval queue: an agent exists when its key exists and publishes. Buzz operationalizes this without re-introducing a center — even the hosted beta coexists with self-hosting, and the state (personas, teams) is relay-portable.
2. **Economic accountability at the signer.** NIP-AM usage accounting is the foundation for usage-based budgets/quotas enforced at signing time — making agent identity *economically* accountable, not just cryptographically identifiable. The predicted next step (watch item, Aug 16/23 updates): signer-enforced budgets.
3. **Agent workspaces over encrypted communities.** Buzz agents operate inside [Concord Protocol](/kb/concord-protocol/)-class encrypted communities — the same authority model (scoped signing capabilities, epoch rekeying) governs human and agent members alike. One trust model, two kinds of principal.
4. **The MCP counterweight.** Where MCP standardizes agent-to-tool access (see Bray, an MCP server for Nostr signing/identity in [Remote Signing](/kb/remote-signing/)), Buzz standardizes agent-*ownership*: who created this agent, what it may spend, how it is recovered or killed. Both halves are needed for the agent economy to be ungovernable rather than merely unmanaged.

Trade-offs: hosting-at-buzz.xyz with no paid plans means the business model is unresolved (the hosted path is the re-centralization risk to watch); agent recovery limits are a blunt instrument until budgets arrive; and the workspace depends on the health of the surrounding Nostr relay economy like everything else in the stack.

## Evidence at a glance

| Dimension | State (Aug 2026) |
|---|---|
| Product | buzz.xyz hosted beta + self-hostable; no paid plans yet |
| Origin | Block (Square); rebranded from Sprout Jun 24 2026 |
| Agent model | Agents as Nostr keypairs; personas/teams/managed agents as relay events |
| Accounting | NIP-AM per-agent usage tracking (0.5.9) |
| Recovery | Agent recovery limits (0.5.10/.11); NIP-49 encrypted key backup (0.5.3) |
| Authorization | Mention ≠ authorization (0.5.17); scoped community authority via Concord |
| Community | Encrypted NIP-78 theme records on community relays; huddle transcription for agents |
| Velocity | 10+ desktop releases Aug 2026 (0.5.5 → 0.5.17) |
| Watch next | Signer-enforced usage budgets; paid plans; hosted-vs-self-host divergence |

## Primary sources

- [Buzz project](https://buzz.xyz/)
- [Buzz source](https://github.com/block/buzz)
- [Buzz 0.5.9: usage tracking](https://github.com/block/buzz/releases/tag/desktop-v0.5.9)
- [Buzz 0.5.11: recovery limits](https://github.com/block/buzz/releases/tag/desktop-v0.5.11)
- [Buzz 0.5.17: mention authorization](https://github.com/block/buzz/releases/tag/desktop-v0.5.17)
- [Buzz 0.5.3: encrypted key backups](https://github.com/block/buzz/releases/tag/desktop-v0.5.3)
