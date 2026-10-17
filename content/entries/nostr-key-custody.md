---
title: "Nostr Key Custody and Recovery"
slug: nostr-key-custody
type: guide
pillars: ["identity", "endpoint"]
description: "Keeping a Nostr key safe and usable for years: signers, bunkers, hardware, backups, social recovery and what to do when a key is compromised."
dek: "The hard part of key-rooted identity is not generating a key. It is keeping the key usable for years without turning every phone, web app, browser extension, and backup file into an account-takeover risk. Nostr is the best live laboratory for this problem because the public key is the account."
updated: 2026-05-31
created: 2026-05-03
origin: vault
source: "11-Identity/Nostr Key Custody and Recovery.md"
aliases: ["Nostr Key Management", "Nostr Key Recovery", "NIP-46 Bunker", "Frostr"]
tags: ["nostr", "identity", "key-management", "frostr", "nip-46", "threshold-signatures", "pseudonymity"]
---

## Summary

[Nostr](/kb/nostr-identity/) makes identity radically simple: a user is a secp256k1 keypair, and every event is signed by that key. This removes platform registration, password reset, KYC onboarding, and account deletion as control points. It also removes the safety net. If the `nsec` leaks, the attacker can impersonate the user everywhere. If the `nsec` is lost, there is no administrator who can recover the account. If the user wants to rotate keys, social reputation and identifiers must be migrated manually.

The ecosystem is converging on three complementary custody models:

1. **App-local hot keys** — easiest onboarding, highest compromise risk. A mobile app or browser extension stores the `nsec` and signs directly.
2. **Remote signing / bunkers via NIP-46** — clients never see the private key. A phone, daemon, hardware device, or server signs requests over an encrypted Nostr channel.
3. **Threshold signing via Frostr / FROST** — the identity key is split into shares. Any threshold quorum can sign; one lost or compromised device is not enough to lose the identity.

The design direction is clear: serious Nostr identity wants the UX of OAuth, the portability of a raw keypair, and the security properties of hardware wallets / threshold custody. The mature pieces are NIP-07 browser signing, NIP-46 remote signing, and Android signer apps such as Amber. The emerging pieces are Frostr/Bifrost, Igloo server/app tooling, and better client-level permission prompts.

## Historical context

### Phase 1 — paste the `nsec` everywhere (2020–2023)

Early Nostr clients usually asked users to paste a raw private key or generate one in-app. That made the first user experience refreshingly simple, but it created a bad security norm: every client became a key custodian. A malicious or compromised client could exfiltrate the key once and own the user's identity forever.

This phase mirrors early Bitcoin wallet UX: sovereignty was technically available, but the default path encouraged users to put irreversible secrets into hot software without much ceremony.

### Phase 2 — browser signers and app-level wallets (2023–2025)

NIP-07 browser extensions moved signing out of each web client and into a local signer API exposed as `window.nostr`. This was a major improvement: a user could browse many web clients without pasting the `nsec` into each one. Android signers such as [Amber](https://github.com/greenart7c3/Amber) extended the same idea to mobile: apps request signatures from a dedicated signer, and the signer can approve, deny, or scope operations.

This model is close to a cryptocurrency wallet: the user-facing app prepares a message; the signer controls the key.

### Phase 3 — NIP-46 remote signing (2024–2026)

[NIP-46](https://nips.nostr.com/46) defines remote signing over Nostr itself. A client and remote signer communicate through relays using encrypted request/response events. The signer can be a phone, CLI daemon, server, hardware wallet, or bunker. The private key stays off the client device.

The important architectural move is that Nostr uses its own event transport for custody. A client can connect to a bunker by `bunker://` or `nostrconnect://` URI, request methods such as `get_public_key` or `sign_event`, and receive signatures without learning the user's secret key.

### Phase 4 — threshold custody with Frostr (2025–2026)

[Frostr](https://opensats.org/projects/frostr) applies FROST-style threshold Schnorr signatures to Nostr. The `nsec` is split into shares that live on different devices/services; any `t-of-n` quorum can jointly produce a standard Schnorr signature. OpenSats funded Frostr as part of its Nostr grants, and the project has been moving from a v1 app suite toward Bifrost v2 plus Igloo tooling.

The crucial property: clients and relays see ordinary Nostr signatures. Threshold custody is an implementation detail behind the identity key.

## Custody models compared

| Model | How it works | Maturity | Best for | Main risk |
|---|---|---:|---|---|
| In-app hot key | Client stores `nsec` and signs locally | Mature but unsafe default | Throwaway / low-value identities | Every app is trusted with account takeover |
| NIP-07 extension | Browser extension exposes signer API | Mature for web | Web-client hopping | Extension compromise; weak permissions UX |
| Android signer (Amber) | Mobile signer app handles requests from clients | Active / practical | Mobile-first users | Phone compromise; Android intent / app trust boundaries |
| NIP-46 bunker | Remote signer communicates over encrypted Nostr events | Active standard | Desktop/web clients, self-hosting, policy signing | Bunker availability; policy bugs; relay metadata |
| Hardware signing | Dedicated device signs events via USB/QR/app bridge | Emerging | High-value public identities | Slow UX; limited client support |
| Frostr / FROST threshold | `nsec` split into shares; quorum signs | Emerging / promising | Long-lived public pseudonyms, organizations, agents | More complex onboarding and liveness assumptions |
| Key rotation / migration | Publish new key and attest migration | Social convention, not protocol-native | Compromised or upgraded identities | Reputation continuity is not automatic |

## NIP-46 remote signing in detail

NIP-46 describes two-way communication between a client and a remote signer. The signer may be called a bunker. The protocol uses:

- **Request events**: kind `24133`.
- **Encryption**: NIP-44 encrypted content between the client key and signer key.
- **Connection URIs**: `bunker://...` and `nostrconnect://...` flows.
- **Explicit public-key discovery**: clients must call `get_public_key` after connecting because the remote signer communication key and the user's identity key can be different.
- **Permissions**: clients can request scoped capabilities such as `sign_event`, `nip44_encrypt`, and `nip44_decrypt`.

The best mental model is "SSH agent / hardware wallet for Nostr": apps ask a separate signer to perform cryptographic operations. The signer can enforce user prompts, rate limits, event-kind allowlists, relay policies, and expiry.

### Implementations and tooling

| Project | Role | GitHub / docs | Current signal |
|---|---|---|---|
| Amber | Android signer and identity wallet | [greenart7c3/Amber](https://github.com/greenart7c3/Amber) | Active; GitHub pushed 2026-04-29; ~301 stars; Kotlin; MIT |
| nostr-tools NIP-46 | JavaScript support | [nbd-wtf/nostr-tools](https://github.com/nbd-wtf/nostr-tools) | Widely used library surface for clients |
| rust-nostr signer | CLI NIP-46 signer | [rust-nostr/nostr-signer](https://github.com/rust-nostr/nostr-signer) | Archived; useful historical/reference code |
| bark | NIP-07 backed by NIP-46 | [forgesworn/bark](https://github.com/forgesworn/bark) | Bridges web apps expecting NIP-07 to any NIP-46 bunker |
| Bunker46 / nsecBunker-style tools | Remote signer services | ecosystem varies | Practical but requires careful trust and hosting choices |

### Trade-offs

Remote signing improves key isolation but does not magically solve trust. A malicious client cannot steal the key, but it can try to trick the signer into signing harmful events. A malicious signer cannot publish unless it has permission or the key, but if the signer holds the raw `nsec`, it is still a custodian. The frontier is **policyful signing**: event previews, kind-specific scopes, human confirmation for high-impact events, and short-lived connection secrets.

## Frostr and threshold identity

Frostr is a Nostr-specific threshold signing stack built around FROST-style Schnorr signatures. OpenSats describes the problem directly: putting one `nsec` on every device means one stolen phone or leaked backup can burn the user's public identity. Frostr splits the secret into shares and coordinates signing over Nostr relays. Each share can have its own Nostr identity and exchange encrypted messages with the other shares.

### Why it matters

Threshold custody changes the failure model:

- A single device compromise does not reveal the identity key.
- A single lost device does not kill the identity if enough shares remain.
- Shares can be rotated/replaced without rotating the user's public key.
- Organizations and AI agents can require multiple approvers for high-impact actions.
- A self-hosted signer can be hardened without making it the only custodian.

### Current project map

| Component | Repository / source | Role | Maturity signal |
|---|---|---|---|
| Frostr project | [frostr.org](https://frostr.org/) / [OpenSats grant](https://opensats.org/projects/frostr) | Nostr threshold signing initiative | OpenSats-funded; written spec in progress |
| Bifrost | [FROSTR-ORG/bifrost](https://github.com/FROSTR-ORG/bifrost) | Core signing protocol library | Active; pushed 2026-02-16; TypeScript; MIT |
| Igloo Server | [FROSTR-ORG/igloo-server](https://github.com/FROSTR-ORG/igloo-server) | Self-hostable Frostr server/signing client | Active; pushed 2026-03-09; TypeScript; MIT |
| Igloo app suite | FROSTR-ORG repositories | Desktop/browser/mobile/server clients | Emerging; v2-native suite replacing v1 clients |
| FROST paper | [Komlo & Goldberg, FROST](https://eprint.iacr.org/2020/852) | Underlying threshold Schnorr construction | Research foundation, widely cited |

### Open questions

- How should users back up shares without recreating the original single-secret problem?
- What is the best default threshold for normal people: 2-of-3, 3-of-5, phone + laptop + home server?
- Can onboarding explain threshold signing without sounding like enterprise key management?
- How should clients display that a signature came from a policy-controlled threshold signer rather than a raw hot key?
- What is the recovery story if a user loses enough shares but still controls a known social graph?

## Key rotation and migration

Nostr has no global account registry, so there is no authoritative "rotate this account to a new key" operation. Rotation is social and application-level:

1. The old key signs an announcement pointing to the new key.
2. The new key signs a reciprocal announcement pointing back.
3. Clients, relays, and WoT tools decide whether to follow the migration.
4. The user updates NIP-05 / ENS / website / Lightning address / profile links.
5. Friends and communities re-follow or import the migration.

This is workable for low-stakes identities but fragile for high-reputation public keys. The deeper conclusion is that key custody matters more in Nostr than in platform identity: there is no centralized mapping layer that can quietly update the user's underlying account identifier.

Possible mitigation patterns:

- **Cold root + hot delegates**: use NIP-26 or app-specific delegation where supported.
- **Bunker root**: put the main key behind NIP-46 with strict policies.
- **Threshold root**: use Frostr for the main identity and per-device authorization for daily apps.
- **Pinned aliases**: maintain a website, NIP-05 record, ENS name, and OpenPGP/Keyoxide proof that can help humans discover a rotation.
- **WoT-assisted migration**: ask trusted peers to countersign the new key.

## AI agents and organizational identities

Key custody is not only a human UX issue. AI agents, bots, services, and organizations also need sovereign identities. A bot that holds a raw `nsec` in a `.env` file has the same problem as a human pasting a private key into every client.

Emerging patterns:

- **Agent-specific keys**: each agent has its own public-key identity and reputation history.
- **Delegated keys**: a human or organization authorizes an agent to publish only certain event kinds or only for a time window.
- **Remote signer policies**: a bunker approves/rejects actions based on event kind, budget, relay, or destination.
- **Threshold org keys**: multiple operators or devices must cooperate for high-impact posts, releases, or payments.
- **Keychat / OpenClaw**: [keychat-io/keychat-openclaw](https://github.com/keychat-io/keychat-openclaw) shows the direction: E2E encrypted agent communication with each agent represented by a sovereign cryptographic key.

For ungovernable infrastructure, this is important because agents will increasingly operate relays, moderation bots, market makers, zaps, watchtowers, and research feeds. Their identities should be revocable, scoped, and auditable without depending on a platform account.

## Evidence at a glance
## Evidence at a glance
|| Item | Type | Evidence / maturity | Freedom-tech relevance ||
|---|---|---|---|
| NIP-46 | Nostr optional standard | Documented at `nips.nostr.com/46`; implemented by signer apps and libraries | Removes raw-key exposure from clients |
| Amber | Android signer | Active GitHub development through 2026-04; ~301 stars | Practical mobile Nostr identity wallet |
| Frostr | Threshold signing stack | OpenSats-funded; Bifrost/Igloo projects active in 2026 | Solves single-device compromise/loss for long-lived nyms |
| Bifrost | Core Frostr library | Active repo; MIT; TypeScript | Building block for independently implemented threshold custody |
| Igloo Server | Self-hostable signer | Active repo; MIT; TypeScript | Home-server custody without making the server the whole secret |
| NIP-07 | Browser signer interface | Widely deployed | Lowest-friction web-client interoperability |
| RFC 9591 (FROST) | Threshold Schnorr spec | IRTF stable since June 2024 | Normative reference for Frostr library implementations; nonce reuse is the critical implementation footgun |
| NIP-26 revocation (issue #654) | Delegation revocation | Open NIP proposal | Root-key-signed revocation certificate would close the delegation expiry gap; currently no revocation mechanism |
| rust-nostr/nostr-signer | CLI signer | Archived reference | Historical implementation; not the active path |
| Keychat OpenClaw | Agent identity / E2EE | Early, AGPL, small repo | Shows agent-public-key pattern beyond human social clients |
| FROST NIST submission | EdDSA threshold standard | Active NIST Threshold Call; MPTS 2026 preview | Path toward government-standardized threshold EdDSA; relevant for Frostr auditability |
| Hermine | PQ threshold signatures | eprint 2026/419; MPTS 2026; hermine-th.org | PQ FROST-like scheme; proactive refresh; PQ migration path for Frostr; targets NIST standardization |
| Bitcoin 2026 Conference | Nostr real-world use cases | May 15, 2026 panel; YouTube archive | Demonstrates custody solutions powering P2P exchange, AI agents, and decentralized infrastructure |

## Practical notes

### For a normal low-stakes pseudonym

- Generate the key in a reputable signer, not in a random web client.
- Use NIP-07 or Amber rather than pasting `nsec` into multiple apps.
- Back up the key offline.
- Use NIP-05 for discoverability, but remember it is an alias, not the account.

### For a high-reputation public identity

- Treat the `nsec` like a Bitcoin seed.
- Prefer NIP-46 or hardware/phone signing so daily clients never see the key.
- Consider Frostr/threshold custody once the app suite is stable enough for the threat model.
- Keep an out-of-band identity page that can publish emergency migration statements.
- Build social recovery norms: known peers should know how to verify a new key announcement.

### For organizations and agents

- Do not put the root key in CI secrets unless compromise is acceptable.
- Use scoped delegates for automation.
- Use policy signers for event kinds that affect funds, releases, or moderation.
- Consider threshold signing for public organizational keys.

## Trade-offs

| Benefit | Cost |
|---|---|
| No platform can reset, freeze, or sell the account | No platform can recover a lost key |
| A single key can work across many clients | A single leaked key compromises the whole identity |
| Remote signing hides the key from clients | Signer availability and policy UX become critical |
| Threshold signing removes single-device failure | More moving parts, harder onboarding |
| Pseudonyms can build durable reputation | Linkage attacks become easier as history accumulates |
| Agents can own keys directly | Agent key storage becomes infrastructure security |

## Early-June 2026 Developments

### Amber: 314 stars, pushed 2026-05-30 — most active signer

Amber (greenart7c3/Amber) hit 314 stars with a push on 2026-05-30, confirming active maintenance as the highest-starred dedicated Nostr signer. The Android app continues to be the reference implementation for NIP-07 browser signer API on mobile and NIP-46 remote signing flows. Its architecture — event previews, per-app permission prompts, and approval UI on Android — remains the practical model for how signing UX should work.

### Igloo Server + Frostr v2: self-hosted threshold custody maturing

FROSTR-ORG/igloo-server (8 stars, pushed 2026-05-28) is transitioning toward a v2 direction that combines self-hosting with NIP-46 bunker compatibility. The architectural goal is a server that holds Frostr threshold shares and presents a standard NIP-46 interface to clients — so clients don't need special Frostr support, they just talk to a bunker. This is the right design for liveness: a self-hosted server that combines threshold-custody security with the availability characteristics of a hosted service.

### Bifrost: 10 stars, pushed 2026-02-16 — likely in spec phase

FROSTR-ORG/bifrost shows a commit gap from February to May 2026. This likely reflects the v2 architectural work being done at the spec/design level rather than active code development. The OpenSats Frostr grant remains active, RFC 9591 is stable, and the Igloo Server v2 direction depends on Bifrost being correct. The commit gap is a normal pattern for library code between major versions.

### bark: NIP-07 backed by NIP-46 (0 stars, pushed 2026-05-25)

[forgesworn/bark](https://github.com/forgesworn/bark) is a small but notable project: it bridges web apps that expect the NIP-07 `window.nostr` API to any NIP-46 bunker. This means any existing NIP-07 web client can immediately use a NIP-46 signer without code changes. The bridge pattern is important because it means the ecosystem doesn't need every client to implement NIP-46 natively — they just use NIP-07, and the bunker handles the NIP-46 protocol. Last push 2026-05-25 confirms active maintenance.

### NIP-26 revocation: still open, still the critical gap

GitHub issue nostr-protocol/nips#654 remains open. The proposed root-key-signed revocation certificate for NIP-26 delegation is the right design: it lets a compromised delegate key be burned immediately via a signed event distributed to relays, rather than waiting for natural expiry. This matters most in the NIP-46 remote signing flow where delegation keys are commonly used for UX convenience. Until this lands as a NIP, the practical mitigations are short-expiry delegations and monitoring for unexpected delegation use.

### Threshold signing for AI agents and organizations

The custody patterns documented in this file apply equally to AI agents operating on Nostr. An agent with a raw `nsec` in a `.env` file has the same single-point-of-failure problem as a human pasting a key into every app. The emerging pattern: scoped delegate keys for agents (NIP-26), policy signers that approve or reject specific event kinds, and threshold custody for organizational Nostr identities where multiple operators must cooperate for high-impact posts or payments.

### FROST at NIST MPTS 2026 — EdDSA threshold submission active

FROST was submitted to the NIST Threshold Call (NIST IR 8214C) in 2026, with a preview presentation at MPTS 2026 (NIST Workshop on Multi-Party Threshold Schemes, January 2026). The FROST Team — including Chelsea Komlo, Ian Goldberg, Jonathan Katz, and Mary Maller among others — published a preview writeup (version 0.1, 2026-03-19) targeting Category N1.1 (Threshold EdDSA Signing). The talk covered the preparatory status of the submission, design choices, security properties relative to other threshold schemes, and new results in adaptive security of threshold Schnorr signatures. A key discussion point: FROST deliberately does not require single-party EdDSA-style determinism, which avoids unintended vulnerabilities introduced when requiring determinism in multi-party settings — a finding relevant to all threshold signature implementations, including Frostr.

For Nostr's Frostr ecosystem, this is directly relevant: FROST is the cryptographic basis for Frostr threshold Nostr identity, RFC 9591 is the stable IRTF spec, and the NIST submission represents the path toward government-standardized threshold EdDSA. If FROST is standardized by NIST, it would provide a normative reference that Frostr library implementations could be audited against.

### Hermine: post-quantum FROST-like threshold signatures

A notable 2026 development is [Hermine](https://hermine-th.org) (eprint 2026/419, presented at MPTS 2026), a post-quantum lattice-based threshold signature scheme that offers the full feature set of FROST under standard lattice assumptions:

- **Design**: FROST-like, partially non-interactive, two-round signing (one preprocessing round + one message-dependent round).
- **Scale**: Designed for medium-scale deployments (N ≤ 64 parties), producing ~11KB signatures.
- **Advanced properties**: Identifiable aborts, proactive share refresh (periodic share renewal without changing the public key), and distributed key generation.
- **Security basis**: Standard lattice assumptions; targets alignment with NIST PQC standardization.
- **Significance**: If FROST is the classical threshold Schnorr solution, Hermine is the post-quantum counterpart. For Nostr's Frostr ecosystem, Hermine represents the long-term migration path: a PQ-ready threshold signing scheme that could replace FROST once standardized. The proactive refresh property is especially valuable for long-lived Nostr identities where share compromise over time is a real risk.

The Hermine team (including Guilhem Niot and collaborators) submitted Hermine as its own package to the NIST Threshold Call. Its existence alongside FROST in the NIST process means the threshold cryptography ecosystem is actively bifurcating into classical and post-quantum tracks — relevant for anyone planning the custody architecture of high-value Nostr identities beyond the 5-10 year horizon.

### Bitcoin 2026 Conference: Nostr identity beyond social

The Bitcoin 2026 Conference (May 15, 2026) featured a panel on "Protocol vs Platform: Nostr's Utility Beyond Social Media" covering Nostr-powered AI integrations, MLS encrypted messaging, WoT curation, decentralized GitHub alternatives, and the "Notes and Other Stuff" ecosystem. Panelists included William Casarin (Damus), Jeff Gardner (White Noise), and David Strayhorn (NosFabrica). The discussion specifically addressed how Nostr's key-based identity model extends beyond microblogging to decentralized exchange (Mostro P2P Bitcoin trading), AI agent identity, and open internet infrastructure — directly connecting custody solutions (NIP-46 bunkers, Amber, Frostr) to real-world use cases where losing the key means losing the business relationship.

## Primary sources
- [NIP-46 — Nostr Remote Signing](https://nips.nostr.com/46)
- [NIP-07 — `window.nostr` browser signer API](https://nips.nostr.com/07)
- [NIP-26 — Delegated Event Signing](https://nips.nostr.com/26)
- [NIP-44 — Versioned Encryption](https://nips.nostr.com/44)
- [NIP-85 — Trusted Assertions](https://nips.nostr.com/85)
- [Frostr OpenSats project page](https://opensats.org/projects/frostr)
- [FROSTR-ORG/bifrost](https://github.com/FROSTR-ORG/bifrost)
- [FROSTR-ORG/igloo-server](https://github.com/FROSTR-ORG/igloo-server)
- [greenart7c3/Amber](https://github.com/greenart7c3/Amber)
- [forgesworn/bark](https://github.com/forgesworn/bark)
- [Komlo and Goldberg — FROST: Flexible Round-Optimized Schnorr Threshold Signatures](https://eprint.iacr.org/2020/852)
- [RFC 9591 — FROST Protocol](https://datatracker.ietf.org/doc/rfc9591/) — IRTF stable specification
- [FROST NIST MPTS 2026 preview writeup](https://csrc.nist.gov/csrc/media/Projects/threshold-cryptography/documents/TCall-1/FROST-PW01.pdf) — FROST Team preview, version 0.1, March 2026
- [Hermine: An Efficient Lattice-based FROST-like Threshold Signature](https://eprint.iacr.org/2026/419) — eprint 2026/419
- [Hermine project website](https://hermine-th.org)
- [nostr-protocol/nips#654](https://github.com/nostr-protocol/nips/issues/654) — NIP-26 delegation revocation proposal
- [keychat-io/keychat-openclaw](https://github.com/keychat-io/keychat-openclaw)
- [Bitcoin 2026 Conference — Nostr Beyond Social panel](https://www.youtube.com/watch?v=wrlE0DMoTSc)
