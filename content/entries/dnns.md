---
title: "DNNS"
slug: dnns
type: deep-dive
pillars: ["naming"]
readiness: experimental
description: "DNNS, an experimental programmable identity and routing layer introduced in 2026: what it proposes, how it differs from DNS, and open questions."
dek: "DNNS is a programmable identity and routing layer introduced by Lithosphere in March–April 2026. It replaces traditional centralized DNS with an on-chain naming framework designed for Web4 environments — where autonomous agents, decentralized services, and AI-readable identity require persistent, verifiable names that persist across blockchain networks and environments. See Overview - Decentralized DNS for how it fits in the broader naming landscape."
updated: 2026-05-18
created: 2026-05-18
origin: vault
source: "03-Decentralized-DNS/DNNS.md"
aliases: ["Decentralized Naming System (Lithosphere)", "Lithosphere DNNS"]
tags: ["dnns", "lithosphere", "naming", "decentralized-dns", "web4", "blockchain", "deep-dive"]
---

## Summary

DNNS (Decentralized Naming System) is Lithosphere's answer to the question: what naming system do you build when the consumers of the namespace are not just humans browsing websites, but autonomous agents, AI systems, and cross-chain applications that need machine-readable, programmatically enforceable identity?

Rather than competing with ENS, Handshake, or PKARR, DNNS targets a different layer — it is an **on-chain programmable identity layer** built natively into the Lithosphere protocol, where names are not merely resolved but can carry programmable rules, routing logic, and cross-chain bindings.

The project is very new (announced March 31, 2026, with follow-on routing announcement April 21, 2026). It has press coverage and a conceptual description but limited public repository evidence as of the knowledge cutoff. Treat it as a tracked experimental development, not as production infrastructure.

## Historical context

Decentralized naming has moved through several eras:

|| Era | Systems | Limitation |
|-----|--------|---------|-----------|
| 2011–2017 | Namecoin, ENS | Single-chain, human-centric resolution |
| 2018–2022 | Handshake, GNS | Root-zone replacement or petname privacy |
| 2023–2025 | PKARR/Pubky, Nostr NIP-05 | Key-rooted, fee-free, social |
| 2026 | DNNS (Lithosphere) | On-chain programmable identity for Web4 agents |

DNNS arrives in the 2026 wave alongside the broader Web4/AI-agent infrastructure narrative. The thesis: as AI agents begin operating autonomously across decentralized networks, they need naming systems that are:

- Persistent (not dependent on a single chain's liveness)
- Machine-readable (AI-interpretable identity metadata)
- Programmatically enforceable (routing rules, capability grants embedded in the name record)
- Sovereign (user-controlled, not platform-controlled)

DNNS tries to address all four.

## Architecture

DNNS is built into the Lithosphere protocol. The public descriptions emphasize:

### On-chain naming

Names are registered and updated on the Lithosphere blockchain. The name record is not just a pointer — it contains programmable metadata that can specify:

- Routing rules (how to reach the named entity across networks)
- Capability grants (what operations this identity is authorized to perform)
- Cross-chain bindings (pointers to identities on other chains)
- AI-readable descriptors (structured data AI agents can interpret)

### Programmable identity layer

The distinction Lithosphere draws: traditional DNS resolves a name to an IP address. DNNS resolves a name to a **programmable identity** — a bundle of routing information, authorization rules, and metadata that a system or agent can act on directly.

### On-chain routing

The April 2026 announcement expanded DNNS with **on-chain routing**: interactions between applications, services, and agents can be directed within the protocol itself, rather than relying on external resolution.

### Cross-chain model

DNNS is described as blockchain-agnostic at the identity layer — it is built on Lithosphere but positions itself as a naming system that works across decentralized networks, not just within one chain ecosystem.

## Evidence at a glance

|| Claim | Evidence | Confidence |
|-------|--------|----------|------------|
| Lithosphere announced DNNS in March 2026 | Globe and Mail / Newsfile Corp press release, March 31, 2026 | High |
| DNNS is on-chain programmable identity | Press release describes "programmable identity layer" and "AI-readable identity architecture" | High |
| On-chain routing announced April 2026 | Globe and Mail / Newsfile Corp, April 21, 2026 follow-on release | High |
| Targets Web4 / autonomous agents | Press releases explicitly frame DNNS for AI agents and Web4 infrastructure | High |
| GitHub repository public | Not found in search; no confirmed public repo as of 2026-05-18 | Low — no confirmed public code |
| Mainstream adoption | No evidence yet; described as announced, not deployed | N/A |

**Key gap:** No public GitHub repository was found for Lithosphere DNNS. The only sources are press releases from Globe and Mail / Newsfile Corp. This is typical for very new announcements but means the technical claims cannot be independently verified yet.

## Maturity assessment

DNNS is currently at **announced / early development** stage — roughly equivalent to where Handshake was in its 2018 testnet phase.

### Positive indicators

- Funded project with public announcements and ongoing development (follow-on routing announcement April 21, 2026, shows continued work).
- Positions itself in a real market need (AI-agent naming / Web4 identity).
- On-chain model means resolution can leverage existing blockchain infrastructure.
- Cross-chain framing is differentiated from ENS (single-chain) and PKARR (off-chain DHT).

### Caution indicators

- **No public repository found.** Cannot verify implementation claims.
- Press-release-only disclosure makes technical due diligence impossible.
- Lithosphere itself is a less-prominent blockchain project — the DNNS ecosystem depends on Lithosphere's continued development.
- AI-agent/Web4 framing is aspirational; actual agent deployments using DNNS are not documented.
- No testnet, no documented adoption.

## How DNNS compares

|| System | Registry | Human-readable | Programmable | AI-agent ready | Maturity |
|--------|---------|----------------|-------------|----------------|-----------|
| [ENS](/kb/ens/) | Ethereum L1 | Yes | Limited (CCIP-Read) | Emerging | High (EVM ecosystem) | Production |
| [Handshake](/kb/handshake/) | Handshake PoW | Yes | No | No | No | Niche but live |
| [PKARR](/kb/pkarr/) / [Pubky](/kb/pubky/) | Mainline DHT | No | No | No | Possible | Emerging |
| [GNS](/kb/gnu-name-system/) | GNUnet DHT | Local petnames | No | No | No | Niche |
| [Nomen](/kb/nomen/) | Bitcoin + Nostr | Yes | No | No | No | Experimental |
| [Cardano DNS](/kb/cardano-dns/) | Handshake + Cardano | Yes | Via Cardano contracts | Possible | Possible | Experimental |
| DNNS | Lithosphere L1 | Yes | Yes (on-chain) | Designed for | Very early |

DNNS's closest conceptual neighbor is Cardano DNS — both are blockchain-native naming systems with programmable second layers — but DNNS is newer and explicitly targets AI-agent routing rather than DNS marketplace functionality.

## Trade-offs

### Strengths

- **Programmable name records.** Unlike static DNS records, DNNS records can carry routing rules, capability grants, and AI-readable metadata. This is a genuine architectural advance over flat name-to-address systems.
- **On-chain authority.** Blockchain-backed names avoid the registrar seizure path; ownership is determined by chain state.
- **Cross-chain framing.** Positioning as chain-agnostic is compelling if realized — a DNNS name could unify identity across EVM, Solana, Cosmos, etc.
- **AI-agent native.** The design goal is names that AI agents can read, interpret, and act on without human mediation.

### Limitations

- **Chain dependency.** Like ENS (Ethereum), DNNS inherits Lithosphere's liveness and finality properties. If Lithosphere goes down, so does DNNS resolution.
- **No public code.** Impossible to independently audit, verify, or adopt without a repository.
- **New chain risk.** Lithosphere is not Bitcoin or Ethereum — it lacks the security track record and decentralization of those systems.
- **Adoption chicken-and-egg.** AI agents and Web4 infrastructure are not yet deployed at scale; DNNS's primary use case depends on a future that hasn't arrived.
- **Governance unclear.** How are conflicts resolved? How are squatting and migration handled? No published policy.

## Primary sources

- Lithosphere DNNS announcement (March 31, 2026) — Globe and Mail / Newsfile Corp.
- Lithosphere DNNS routing announcement (April 21, 2026) — Globe and Mail / Newsfile Corp.
- Lithosphere protocol — lithosphere.tech (no specific DNNS documentation URL found as of 2026-05-18).
- Newsfile Corp coverage — [newsfilecorp.com/release/290630](https://www.newsfilecorp.com/release/290630/Lithosphere-Introduces-DNNS-The-Decentralized-Naming-System-Powering-Web4-Infrastructure).
