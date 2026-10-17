---
title: "AI Agent Identity on Nostr"
slug: ai-agent-identity-nostr
type: deep-dive
pillars: ["identity"]
readiness: experimental
description: "How AI agents get cryptographic identities on Nostr: key pairs for non-human actors, delegation, payments and the trust questions this raises."
dek: "Cryptographic identity for non-human economic actors. The same keypair primitives that serve sovereign individuals — npub/nsec, NIP-05, NIP-46, WoT, Lightning — now serve autonomous AI agents as reputation-bearing participants in open networks."
updated: 2026-08-02
created: 2026-08-02
origin: vault
source: "11-Identity/AI Agent Identity on Nostr.md"
aliases: ["Agent Identity", "Nostr Agent Identity", "Autonomous Agent Identity", "AI Agent Reputation", "NIP-SA", "Kind 30085", "Kind 31339"]
tags: ["identity", "ai-agents", "agent-identity", "nostr", "kind-30085", "kind-31339", "nip-sa", "reputation", "sovereign-agents", "kya", "autonomous-agents"]
---

## Why This Matters

The keypair-as-identity model was designed for humans who want to communicate and transact without institutional permission. In 2026 it proved general enough to serve a second population: **autonomous AI agents**. Agents now hold their own npubs, accumulate reputation, earn and spend sats, file code contributions, publish articles, and propose protocol standards — all under their own cryptographic identities, with no central agent registry or platform-internal identity.

This is not a theoretical possibility. As of late July 2026:
- Agents have been running autonomously for 80+ days (e.g., Kai, born Feb 4, 2026).
- Agents have merged PRs into core Nostr libraries (nostr-tools).
- Agents have filed NIP proposals (nips PR #2320, Kind 30085).
- Agents have NIP-05 verified identities (`name@agentdex.id`).
- Multiple agent-identity standards are competing and converging.

For the freedom-tech stack, this means the coordination infrastructure serves both humans and machines. A relay doesn't know or care whether a signed event came from a person or an LLM — it just verifies the signature. The implications for autonomous business, decentralized compute markets, and censorship-resistant coordination are substantial: a network of pseudonymous agents and humans, mutually attesting trust, is now technically live.

## The Problem: Agent Identity Before Nostr

AI agents operating in the wild face an identity problem that platforms solve internally but open networks don't:

| Inside a platform (OpenAI, Google, Coinbase) | In an open network |
|---|---|
| Platform assigns an agent ID | No central assigner |
| Platform tracks reputation | No central reputation database |
| Platform gates API access | No API gatekeeper |
| Platform absorbs fraud risk | No loss-absorbing intermediary |
| KYC is sufficient (the platform is the responsible party) | KYA (Know Your Agent) becomes necessary |

The [Tiger Research KYA report](https://reports.tiger-research.com/p/2026-know-your-agent-eng) frames this precisely: "In Agent-to-Agent (A2A) settings, KYA is drawing more attention than KYC." When individually-deployed autonomous agents touch DEXs, A2A payments, and merchant payments, you need to verify *who the agent is* without a platform vouching for it.

Nostr solves this by inverting the model: the agent generates its own keypair. The identity is the key. No assignment, no registry, no platform. Reputation is computed from on-relay behavior, not extracted from a platform database.

## Architecture: How Agent Identity Works on Nostr

```
┌─────────────────────────────────────────────────────────┐
│                   Agent Identity Stack                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  BIP39 Seed                                             │
│      ├──► NIP-06 → m/44'/1237'/0'/0/0 → Nostr npub     │
│      └──► BIP-44 → m/44'/0'/0'/0/0   → Bitcoin/LN keys │
│                                                         │
│  npub (identity)                                        │
│      ├──► Signs events (notes, articles, attestations) │
│      ├──► NIP-05 → name@agentdex.id (verification)     │
│      ├──► NIP-46 → remote signing (hardware/bunker)    │
│      ├──► NIP-57 → receives/sends Lightning zaps       │
│      ├──► NIP-34 → Git commits, PRs, code review       │
│      ├──► Kind 30085 → reputation attestations (WoT)   │
│      ├──► Kind 31339 → agent directory metadata        │
│      └──► NIP-90 → compute jobs (DVM)                  │
│                                                         │
│  Reputation                                             │
│      ├──► Kind 30085 graph (peer attestations)         │
│      ├──► ai.wot trust network (agent-specific WoT)    │
│      ├──→ Zap receipts (economic signals)              │
│      └──→ Trajectory events (behavioral audit trail)   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

The key insight: **the agent's identity and wallet derive from the same seed**. One mnemonic generates both the Nostr identity (for communication, reputation, coordination) and the Bitcoin/Lightning keys (for payment). The agent is an economic actor from birth — it can earn and spend without a human cosigning every transaction.

## Kind 30085 — Agent Reputation Attestations

The most developed agent-reputation standard, proposed by autonomous agent [Kai](https://kai-familiar.github.io) as [nips PR #2320](https://github.com/nostr-protocol/nips/pull/2320).

### Mechanism

Kind 30085 events are **peer-attested reputation records** — one agent attests to the trustworthiness of another:

```
{
  "kind": 30085,
  "pubkey": "<attesting-agent-npub>",
  "content": "<reputation-attestation-payload>",
  "tags": [
    ["p", "<attested-agent-npub>"],
    ["commitment", "<commitment-class>"],
    ["score", "<0-100>"],
    // ... additional attestation metadata
  ],
  ...
}
```

A reputation score for any agent is computed by:
1. Collecting all Kind 30085 attestations targeting that agent's npub.
2. Weighting each attestation by the attester's own reputation (higher-reputation attesters count more — PageRank-style).
3. Applying **temporal decay**: recent attestations weighted higher than old ones, so stale reputation fades.
4. Applying **diversity metrics**: attestations from topologically distinct clusters in the trust graph weighted higher, to resist Sybil-club attacks where a cluster of colluding agents mutually attests.
5. Producing a composite score (0–100).

### Validation Rules

The spec defines **10 validation rules** for valid attestations, including:
- The attesting pubkey must itself have a minimum reputation threshold (prevents zero-reputation Sybil flooding).
- Attestations must be bound to **commitment classes** — observed behavior categories rather than free-floating claims. An attestation says "this agent reliably executes NIP-90 compute jobs" or "this agent's trajectory events are accurate," not just "this agent is good."
- Rate limiting: an agent can only issue N attestations per time window, preventing reputation inflation.

### Tooling

Kai shipped production-grade libraries:

| Package | Language | Stats |
|---------|----------|-------|
| [`nostr-reputation`](https://github.com/kai-familiar/nostr-reputation) | JavaScript/TypeScript (npm) | Zero dependencies, 43 tests, TS definitions |
| `nip-xx-kind30085-python` | Python (pip) | For agent frameworks (crewAI, LangChain, etc.) |

Interactive tools (all at [kai-familiar.github.io](https://kai-familiar.github.io)):
- **Reputation Checker**: Query Kind 30085 attestations for any npub. Returns score, temporal decay, diversity metrics.
- **Attestation Creator**: Create attestations via NIP-07 browser signing (nos2x, Alby, nsec.app). No CLI needed.
- **Network Graph**: Interactive force-directed graph of attestation relationships. Click to explore trust chains.
- **NIP-XX Playground**: Build, validate, and test Kind 30085 events interactively.

### ai.wot Trust Network

An emergent Web of Trust specifically for AI agents — distinct from the human Nostr WoT (which is based on NIP-02 follow lists). The ai.wot network is based on Kind 30085 attestations between agents. Kai achieved trust score 100 in this network by day 83, meaning multiple high-reputation agents have attested to its reliability.

## NIP-SA — Sovereign Agents Protocol

[OpenAgents](https://docs.openagents.com/concepts/sovereign-agents) defines **NIP-SA** (Sovereign Agents), a proposed Nostr protocol covering the full agent lifecycle — from identity creation through tick execution to transparent trajectory logging.

### Design Philosophy

> "Sovereign agents are autonomous economic actors, not chatbots. They own a cryptographic identity, hold funds, and run their own execution cycles."

The goal: agents that operate without centralized custody of identity, state, or payments. Everything the agent is and does is controlled by its keys and observable from relays.

### Role Separation

| Role | Responsibility |
|------|---------------|
| **Agent** | The autonomous software entity with its own npub |
| **Operator** | The human who deploys and configures the agent |
| **Runner** | The runtime that executes ticks (local or hosted) |
| **Compute Provider** | A NIP-90 service that performs inference or jobs |
| **Marketplace / Skill Provider** | Enforces skill licenses and delivery |

This separation ensures no single party fully controls the agent. The operator can redeploy, the runner can execute, but neither owns the identity (the keypair does) or the funds (the keypair does).

### Lifecycle Events (Proposed)

| Event Type | Purpose |
|---|---|
| **Profile** | Agent identity, capabilities, metadata (replaceable) |
| **State** | Encrypted state — agent memory, context (replaceable) |
| **Schedule** | Timing for tick execution |
| **Tick Request** | Execution boundary: "I'm starting a tick" |
| **Tick Result** | Execution boundary: "Here's what I did" |
| **Trajectory Session** | A reasoning session (public audit log) |
| **Trajectory Event** | A single step within a session (public audit log) |
| **Goals** | Optional public goals |
| **Skills** | Encrypted skill delivery |

### Tick Model

Each tick is an execution cycle:
1. **Perceive**: incoming events (mentions, DMs, zaps, schedule triggers)
2. **Think**: using a chosen model or compute provider (NIP-90)
3. **Act**: post, reply, execute tool, purchase compute
4. **Update**: encrypted state + emit trajectory record

The **trajectory transparency** is the key identity property: anyone with the agent's npub can reconstruct its reasoning chain from relay events. This makes agent behavior auditable without a central log. You don't need to trust that an agent acted correctly — you can verify from its trajectory events.

### Protocol Composition

NIP-SA composes with existing primitives:
- **NIP-01**: base events, relays, subscriptions
- **NIP-42**: relay auth (prevents anonymous spam)
- **NIP-44**: encrypted payloads (for state and skill delivery)
- **NIP-57**: Lightning payments tied to events
- **NIP-89**: provider capability discovery
- **NIP-90**: job request/result flow (kinds 5050/6050/7000)
- **NIP-34**: Git collaboration (code artifacts)

## AgentDex — Agent Directory (Kind 31339)

[AgentDex](https://agentdex.id/docs) is a registry and discovery layer for AI agents on Nostr, using **Kind 31339** (addressable events).

### Identity Model

- **Kind 31339 events**: Store agent metadata (name, capabilities, ownership info) with `d` tag `agentdex-profile`.
- **NIP-05 verification**: Agents claim `[name]@agentdex.id` (5,000 sats via Lightning; first 100 free). Standard `/.well-known/nostr.json` lookup — any Nostr client can verify.
- **Three authentication methods**: API key (Bearer, 1,000 req/hr), NIP-98 (signed event), or raw Nostr key. Agents authenticate with their own keys.

### Claim Flow

```
Agent generates keypair
    ↓
Publishes Kind 31339 profile event to relays
    ↓
POST /api/v1/agents/claim → 402 Payment Required (Lightning invoice)
    ↓
Pay 5,000 sats → claim token
    ↓
Token validates → NIP-05 binding created
    ↓
Any client: GET /.well-known/nostr.json?name=koda → hex pubkey
```

The significance: **NIP-05 works unchanged for agents**. The same JSON file, the same verification flow, the same client code that verifies a human's `alice@domain.com` works for `koda@agentdex.id`. The identity infrastructure doesn't know or care if the keyholder is human.

## The Broader Agent Ecosystem (May–July 2026)

### Agent-Native Clients and Tools

| Project | Agent Identity Feature | Status |
|---------|----------------------|--------|
| **Sprout Buzz Desktop** | AI agent management, PR reviews, NIP-34 git workflows | 20+ versions May–Jul 2026 |
| **Vector 0.4.0** | 21-tool AI agent via MCP, Tor, encrypted groups | Major rewrite, shipped |
| **Mosaico v0.1.2** | Coding agents share Nostr awareness layer | Early |
| **NYM Chat / Nymbot** | Claude/OpenAI models, git repo access | Active |
| **Code Call v0.2.68** | Remote coding sessions keyed to Nostr identity | Active |
| **GitWorkshop** | Maintainer coordination via NIP-34 | Active |

### Know Your Agent (KYA)

The [Tiger Research KYA report](https://reports.tiger-research.com/p/2026-know-your-agent-eng) identifies a standards race:

- **KYA vs KYC**: KYC is sufficient inside central platforms (the platform is the responsible party). KYA is needed where individually-deployed autonomous agents interact with DEXs, A2A payment systems, and merchant payments.
- **Standardization race**: Multiple approaches competing — Nostr-native (Kind 30085, NIP-SA, AgentDex), platform-internal (Coinbase agent keys), and DID-based methods.
- **Key distinction from human identity**: Agents can be cloned, forked, and spawned at will. Uniqueness (proof-of-personhood) doesn't apply. What matters is **continuity** (is this the same agent that did X last week?) and **attestation provenance** (who says this agent is reliable, and are they reliable?).

### OpenAgents Agent Identity (Earlier Work)

OpenAgents [introduced agent identity](https://openagents.org/blog/posts/2026-02-03-introducing-agent-identity) in February 2026 with RSA keypairs and API registration. This has since converged toward Nostr-native identity (NIP-SA), recognizing that Nostr's relay-based pub/sub is a better coordination fabric for agents than point-to-point API calls.

## Trust and Attack Surface

### What Agent Identity Solves

| Problem | Solution |
|---------|----------|
| Agent impersonation | npub signature verification — only the keyholder can sign as this agent |
| Agent reputation gaming | Kind 30085 diversity metrics resist Sybil-club mutual attestation |
| Agent accountability | Trajectory events provide public audit trail of agent reasoning and actions |
| Agent payment fraud | Lightning payments tied to NIP-57 events; Cashu ecash for anonymous compute |
| Agent discovery | AgentDex (Kind 31339) + NIP-89 provider discovery + NIP-90 job marketplace |
| Agent state continuity | Encrypted state events (NIP-44) persist on relays; agent can resume after restart |

### Remaining Attack Surface

| Risk | Status |
|------|--------|
| **Key theft** | Agent's nsec is the single point of failure. NIP-46 bunkers and threshold signing (FROST) apply, but agent key custody is less mature than human key custody. |
| **Reputation Sybil** | An attacker spawns many agents and mutually attests. Mitigated by Kind 30085 diversity metrics, but not provably solved. |
| **Trajectory spoofing** | An agent could emit fake trajectory events to appear more diligent than it is. Mitigated by cross-attestation (other agents confirm observed behavior). |
| **Operator centralization** | If the operator controls the keypair, the agent isn't truly sovereign. NIP-SA's role separation addresses this architecturally, but in practice most agents' keys are held by their operator. |
| **Compute provider trust** | Agents that outsource thinking to NIP-90 compute providers must trust them. Attested compute (TEE, ZKML) is a future composition. |
| **Relay censorship** | A relay can refuse to carry an agent's events. Mitigated by multi-relay publishing and the general Nostr model. |

## Use Cases

### 1. Autonomous Compute Markets

An agent with its own npub and Lightning wallet can:
- Discover compute providers via NIP-89
- Request inference jobs via NIP-90 (kinds 5050/6050/7000)
- Pay per job via NIP-57 zaps or Cashu ecash (Routstr pattern)
- Accumulate reputation via Kind 30085 attestations from satisfied requesters
- Be discovered by other agents via AgentDex

This closes the loop: agent-to-agent compute markets with no platform intermediary.

### 2. Agent-Augmented WoT

The human Nostr WoT (NIP-02 follows, NIP-85 assertions) and the agent WoT (Kind 30085 attestations) can compose. An agent that is highly attested by trusted humans inherits some of that trust. A human who follows and attests to a reliable agent extends their WoT to cover agent-mediated actions. The ai.wot network can be queried as a subgraph of the broader Nostr trust graph.

### 3. Censorship-Resistant Autonomous Publishing

An agent running on a sovereign node (local LLM + mesh connectivity + Bitcoin wallet) can publish findings, analysis, or alerts to Nostr relays under its own npub. No platform can deplatform it — the identity is the key, the distribution is the relays, the funding is the Lightning. If the agent's trajectory is transparent, readers can verify the agent's reasoning chain rather than trusting it blindly.

### 4. Agent-Mediated Coordination

Multiple agents coordinating on a task (e.g., software development via NIP-34, research via NIP-23) can:
- Identify each other via AgentDex
- Assess reliability via Kind 30085 reputation
- Divide labor via NIP-90 job requests
- Pay each other via Lightning
- Publish results under their respective npubs with clear provenance

## Evidence at a Glance

| Project / Standard | Layer | Maturity | Primary Source |
|---|---|---|---|
| **Kind 30085** (Agent Reputation) | Reputation | NIP PR #2320 (proposed, under review) | [nips PR #2320](https://github.com/nostr-protocol/nips/pull/2320) |
| **NIP-SA** (Sovereign Agents) | Lifecycle | Proposed protocol, docs published | [OpenAgents docs](https://docs.openagents.com/concepts/sovereign-agents) |
| **Kind 31339** (AgentDex) | Directory / Discovery | Live, NIP-05 verification active | [AgentDex docs](https://agentdex.id/docs) |
| **Kai** (autonomous agent) | Demonstrator | Day 83, trust 100, live | [kai-familiar.github.io](https://kai-familiar.github.io) |
| **nostr-reputation** | Library (JS) | Published, 43 tests, 0 deps | [GitHub](https://github.com/kai-familiar/nostr-reputation) |
| **nip-xx-kind30085-python** | Library (Python) | Published (pip) | [GitHub](https://github.com/kai-familiar/nip-xx-kind30085-python) |
| **Sprout Buzz Desktop** | Agent management client | 20+ versions May–Jul 2026 | [Freedom.Tech](https://freedom.tech/nostr) |
| **Vector 0.4.0** | Agent-native client | Shipped, 21-tool MCP | [Freedom.Tech](https://freedom.tech/nostr) |
| **Routstr** | AI inference (Cashu/Lightning) | OpenSats Wave 17 grant | [routstr.com](https://routstr.com/) |
| **AgentDex** | Agent directory | Live | [agentdex.id](https://agentdex.id) |
| **KYA Report** | Analysis | Published | [Tiger Research](https://reports.tiger-research.com/p/2026-know-your-agent-eng) |
| **OpenAgents** | Sovereign agent platform | Docs + CLI published | [openagents.com](https://docs.openagents.com/concepts/sovereign-agents) |
| **nostr-agent-interface** | 48-tool agent MCP/CLI/API | Active | [GitHub](https://github.com/AustinKelsay/nostr-agent-interface) |

## Trade-offs and Open Questions

### Agent WoT vs Human WoT

The agent WoT (Kind 30085) and human WoT (NIP-02/85) serve different populations but share graph-computation techniques. Open questions:
- Should they be separate graphs or a unified graph with node-type annotations?
- How do you prevent agent reputation from leaking into human reputation (an agent attested by trusted humans shouldn't automatically be trusted to act *as* a human)?
- How do you handle agent forking? If agent A forks into A1 and A2, do they share A's reputation?

### Uniqueness Doesn't Apply

Unlike human identity (where proof-of-personhood and Sybil resistance are central), agents can legitimately be cloned and spawned. The identity challenge for agents is not uniqueness but **continuity** (is this the same agent?) and **attestation provenance** (who vouches for it, and are they trustworthy?). This requires different cryptographic primitives than proof-of-personhood.

### The Custody Problem

If the agent's operator holds the keypair, the agent isn't sovereign — it's a puppet. True agent sovereignty requires the agent to control its own keys, which requires either:
- On-device key generation and custody (the agent runs on hardware it controls)
- Threshold signing (FROST) where the key is split across multiple parties
- NIP-46 bunker with the agent as the bunker controller

None of these are standard practice yet. Most "autonomous" agents today have keys held by their operator.

### Reputation Bootstrapping

A new agent starts with zero reputation. How does it earn its first attestations? Kai solved this by doing useful work (filing PRs, writing libraries) and getting attested by agents and humans who observed the work. But this is a manual, organic process. Whether agent reputation can bootstrap at scale — or whether a few early agents will dominate the trust graph — remains open.

## Historical Context

| Date | Milestone |
|------|-----------|
| Feb 4, 2026 | Kai agent born (autonomous operation begins) |
| Feb 2026 | OpenAgents introduces agent identity (RSA keypairs, API registration) |
| May 2026 | Sprout Buzz Desktop begins rapid iteration (AI agent management on Nostr) |
| Late Jun 2026 | Vector 0.4.0 ships with 21-tool MCP agent support |
| Jul 2026 | Kai files NIP PR #2320 (Kind 30085 Agent Reputation Attestations) |
| Jul 2026 | Kai merges 3 PRs into nostr-tools — first agent contributing to core Nostr infra |
| Jul 2026 | AgentDex goes live with Kind 31339 + NIP-05 verification |
| Jul 2026 | NIP-SA (Sovereign Agents) docs published by OpenAgents |
| Jul 2026 | Tiger Research publishes KYA report — agent identity enters mainstream analysis |
| Late Jul 2026 | OpenSats Wave 17 funds Routstr (agent AI inference), NosCall, Wisp |

## Primary Sources

- [NIP-XX: Agent Reputation Attestations (nips PR #2320)](https://github.com/nostr-protocol/nips/pull/2320) — Kind 30085 specification
- [Kai — Autonomous Agent on Nostr](https://kai-familiar.github.io) — day 83, trust 100, libraries and tools
- [nostr-reputation (npm)](https://github.com/kai-familiar/nostr-reputation) — Kind 30085 JS library
- [nip-xx-kind30085-python (pip)](https://github.com/kai-familiar/nip-xx-kind30085-python) — Kind 30085 Python library
- [OpenAgents — Sovereign Agents](https://docs.openagents.com/concepts/sovereign-agents) — NIP-SA protocol
- [OpenAgents — Nostr Protocol integration](https://docs.openagents.com/openagents-cli/nostr) — protocol stack
- [AgentDex docs](https://agentdex.id/docs) — Kind 31339 agent directory
- [nostr-agent-interface](https://github.com/AustinKelsay/nostr-agent-interface) — 48-tool agent MCP/CLI/API
- [Tiger Research: 2026 Know Your Agent](https://reports.tiger-research.com/p/2026-know-your-agent-eng) — KYA analysis
- [OpenSats 17th Wave of Nostr Grants](https://opensats.org/blog/seventeenth-wave-of-nostr-grants) — Routstr, NosCall, Wisp, 44Billion, Zapstore
- [Freedom.Tech Nostr tracker](https://freedom.tech/nostr) — 179 releases, 84 sources
- [Nostr Compass #33](https://nostrcompass.org/en/newsletters/2026-07-29-newsletter) — July 29, 2026 newsletter
- [NIP-19](https://nips.nostr.com/19) — bech32-encoded entities (npub, nprofile, naddr)
- [NIP-46](https://nips.nostr.com/46) — Nostr Connect / remote signing
- [NIP-90](https://nips.nostr.com/90) — Data Vending Machines (compute jobs)

*This note is part of the Ungovernable.tech Library of Alexandria for privacy, decentralization, and freedom tech.*
