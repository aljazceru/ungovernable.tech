---
title: "Semaphore"
slug: semaphore
type: deep-dive
pillars: ["zk", "identity"]
readiness: usable
description: "Semaphore lets a member of a group send a signal, such as a vote, proving membership in zero knowledge without revealing which member they are."
dek: "A small, focused ZK primitive: prove \"I am a member of this group, and here is a fresh signal\" without revealing which member you are. Built by Privacy & Scaling Explorations (PSE) at the Ethereum Foundation. The construction is two pieces — a Merkle inclusion proof of group membership and a nullifier that prevents the same identity from signaling twice on the same topic. Almost every \"anonymous voting\" or \"sybil-resistant pseudonym\" system on Ethereum traces back to Semaphore."
updated: 2026-04-26
created: 2026-04-26
origin: vault
source: "09-Zero-Knowledge/Semaphore.md"
aliases: ["Semaphore Protocol", "Anonymous Signaling"]
tags: ["zk", "semaphore", "anonymous-signaling", "group-membership", "pse", "deep-dive"]
---

## What Semaphore proves

Semaphore is a ZK proof system specialized for one task: **anonymous group signaling**.

A Semaphore proof attests three things at once:

1. The prover owns an *identity commitment* that is a leaf in a public Merkle tree (the group).
2. The prover is sending a *signal* (an arbitrary message or vote).
3. The prover has produced a *nullifier* that uniquely identifies "this identity, on this external topic" — preventing them from signaling twice.

The verifier learns the signal, the group root, the external topic (called the "external nullifier"), and the nullifier hash. The verifier does *not* learn which member of the group signaled.

That's the entire primitive. Everything else — anonymous voting, anonymous reputation, pseudonymous chat — is built by composing Semaphore with application logic.

## Construction

### Identity

A Semaphore identity is two secrets:

- `trapdoor` — a random scalar.
- `nullifier` — a random scalar (separate from the protocol-level nullifier hash).

The *identity commitment* is `Poseidon(trapdoor, nullifier)`. This commitment is what gets added to the group's Merkle tree.

### Group

A group is a Merkle tree (Poseidon-hashed) of identity commitments. The group root is public. Adding/removing members updates the root.

### Proving

To signal, the prover:

1. Computes the Merkle path from their identity commitment to the root.
2. Picks an *external nullifier* (the topic — a vote ID, a chat-room ID, a poll ID).
3. Computes `nullifierHash = Poseidon(externalNullifier, identityNullifier)`.
4. Generates a SNARK proving:
   - I know `trapdoor`, `nullifier` such that `Poseidon(trapdoor, nullifier)` is in the Merkle tree at root `R`.
   - `nullifierHash` is correctly computed from `externalNullifier` and `nullifier`.
   - The `signal` is bound to the proof (committed in the public inputs).

The proof is published with `(root, nullifierHash, externalNullifier, signal, proof)`. The verifier checks the SNARK and checks that `nullifierHash` hasn't been seen before for this `externalNullifier`.

### Proof system

Original Semaphore (v1-v3, 2019-2023): **Groth16** circuits via Circom, BN254. See [SNARKs](/kb/snarks/).

Semaphore v4 (2024): rewritten with a new circuit toolchain (Noir support, plus PLONK-derivative proving via Honk/UltraHonk for compatibility with newer SNARK stacks). The protocol-level construction is unchanged; the proof system is modernized for smaller proofs and faster client-side proving.

The migration to a more modern proof system also enabled mobile-friendly proving times — Semaphore v3 took several seconds on a phone; v4 is targeting sub-second proofs for typical group sizes.

## Group sizes and trade-offs

Semaphore's circuit is parameterized by the Merkle tree depth `d`. Larger `d` allows more members but increases prover time roughly linearly in `d`.

Typical depths:

| Depth | Max group size | Use case |
|-------|----------------|----------|
| 16 | ~65k | small DAOs, voting committees |
| 20 | ~1M | mid-size communities |
| 30 | ~1B | large pseudonymous systems |
| 32 | ~4B | hardware-limited maximum |

The group's commitment tree is stored on-chain (or in a publicly verifiable database); the depth is fixed at deployment.

## Applications

### Anonymous voting — MACI

**MACI** (Minimal Anti-Collusion Infrastructure, Buterin et al., 2019) uses Semaphore-style group commitments to enable anonymous, collusion-resistant voting. Voters publish encrypted ballots; a coordinator decrypts and tallies, while a SNARK proves the tally was computed correctly. MACI is used in Gitcoin grants and several DAO governance experiments.

The collusion resistance comes from a separate mechanism (key-rotation messages) on top of Semaphore-style identity proofs.

### Pseudonymous reputation — UniRep

**UniRep** (Liu et al., 2022, PSE) extends Semaphore into a *pseudonymous reputation* system. Each user has reputation that can be earned and proven about without linking actions to a single identity. Used as a primitive for "good-faith" pseudonymous accounts.

### Pseudonymous messaging — Heyanon, Sealcaster

Heyanon and Sealcaster let a user post messages signed as "a member of [group X]" — for example, "a Uniswap LP holder," "a Farcaster early user." The proof attests group membership without revealing which member. Useful for whistleblowing, anonymous endorsements, or pseudonymous community participation.

The signal is the message; the external nullifier is typically the topic or thread ID, so the same identity can post once per topic without being doxed across topics.

### Anonymous attestations and credentials

A common pattern: an issuer signs identity commitments for verified users (KYC'd, holds-an-NFT, has-attended-event). The user proves group membership to access something (a forum, a vote, a private channel). Semaphore is the building block; the issuer is the trust root.

### Historical adoption — proof-of-personhood signaling

Semaphore was used by an iris-scanning proof-of-personhood project (which this knowledge base does not endorse — see exclusions) for anonymous in-app signaling. Its presence is mentioned only as a historical adoption reference and is not a recommendation. For proof-of-personhood approaches this library recommends, see [Overview - Identity & Pseudonymity](/kb/identity-and-pseudonymity/) and projects like Idena, BrightID, or zkPassport.

## Comparison with related primitives

| Primitive | Group form | Anonymity set | Proof type | Notes |
|-----------|-----------|---------------|------------|-------|
| **Semaphore** | Merkle tree of commitments | Group size | SNARK | Universal, fixed circuit |
| **DID-key sets** (e.g. raw signature lists) | Public list of pubkeys | Group size | Standard signature | No anonymity — signature reveals signer |
| **BBS+ signatures** | Issuer-signed credentials | Set of credential holders | BBS+ ZKP | Selective disclosure, no nullifier |
| **Ring signatures** (Monero CLSAG) | Ad-hoc ring of pubkeys | Ring size (~16) | Ring sig | Ad-hoc, no Merkle scaling |
| **Group signatures** (e.g. PS) | Issuer-managed group | Group size | Pairing-based | Issuer can deanonymize (revocation) |
| **STARK-based group proofs** | Merkle tree | Group size | STARK | Larger proofs, no trusted setup |

What Semaphore gives you that the others don't:

- **Scalable group size** via Merkle trees (vs. ring signatures' ~16).
- **Built-in nullifier** for one-shot semantics on a topic (vs. plain BBS+).
- **No issuer power to deanonymize** (vs. group signatures with revocation).

What Semaphore lacks compared to the others:

- BBS+ has richer selective-disclosure semantics (prove "age > 18" from a credential).
- Monero ring signatures don't need a group registry (commitments are formed ad-hoc per transaction).
- Group signatures enable key-revocation by issuer.

Semaphore is the right tool when you have a known group, want anonymity within it, and need one-action-per-topic semantics.

## Trade-offs

### Strengths

- Tiny scope; easy to audit.
- Composable with any identity-issuance scheme.
- Mature library and tooling (PSE has maintained it since 2019).
- Mobile-feasible proving in v4.
- Used as the building block for several real systems (MACI, UniRep, anonymous DAO tooling).

### Limitations

- The group registry is a trust assumption. Whoever can add members controls who can speak.
- Anonymity set bounded by group size and *active* members (a 1M-member group with 5 active users gives at-most-5 anonymity).
- Same-identity-twice-on-same-topic is impossible by design — sometimes a feature, sometimes a constraint.
- The Merkle tree depth is fixed; very large groups need re-deployment.
- Proof size and prover cost scale with depth.

## Implementation notes

The primary implementation is `semaphore-protocol/semaphore` on GitHub, maintained by PSE. It includes:

- Solidity contracts for on-chain group management and verifier.
- JavaScript/TypeScript SDK for proof generation and verification.
- Circom circuits (v3) and a v4 circuit set with newer proving stacks.
- Mobile (React Native) and Rust prover bindings.

Integrating Semaphore is mostly: deploy the verifier contract, define your group-management logic, generate identity commitments client-side, generate proofs client-side, submit proofs to your application contract.

## Where to use it

| If you want… | Reach for |
|--------------|-----------|
| One person, one vote, anonymously | Semaphore + group registry |
| Pseudonymous posting in a known community | Semaphore (Heyanon-style) |
| Selective disclosure of identity attributes | BBS+ (not Semaphore) |
| Ad-hoc anonymity in a transaction (no group) | Ring signatures, mixer (see [Tornado and Privacy Pools](/kb/tornado-and-privacy-pools/)) |
| Reputation that accumulates across actions | UniRep (built on Semaphore) |

## Primary sources

- Semaphore Protocol — [semaphore.pse.dev](https://semaphore.pse.dev).
- Semaphore source — [github.com/semaphore-protocol/semaphore](https://github.com/semaphore-protocol/semaphore).
- PSE — [pse.dev](https://pse.dev).
- Buterin et al., *MACI: Minimal Anti-Collusion Infrastructure*, EthResearch 2019.
- Liu et al., *UniRep: Universal Reputation Protocol*, PSE 2022 — [github.com/Unirep](https://github.com/Unirep).
- Heyanon — [heyanon.xyz](https://heyanon.xyz).
- Sealcaster (Farcaster integration).
- Poseidon hash — Grassi, Khovratovich, Rechberger, Roy, Schofnegger, *Poseidon: A New Hash Function for Zero-Knowledge Proof Systems*, USENIX Security 2021.
