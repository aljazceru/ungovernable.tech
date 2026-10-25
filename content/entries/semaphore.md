---
title: "Semaphore"
slug: semaphore
type: deep-dive
pillars: ["zk", "identity"]
readiness: usable
description: "Semaphore lets a member of a group send a signal, such as a vote, proving membership in zero knowledge without revealing which member they are."
dek: "A small, focused ZK primitive: prove \"I am a member of this group, and here is a fresh signal\" without revealing which member you are. Built by Privacy & Scaling Explorations (PSE) at the Ethereum Foundation. The construction is two pieces — a Merkle inclusion proof of group membership and a nullifier that prevents the same identity from signaling twice on the same topic. Almost every \"anonymous voting\" or \"sybil-resistant pseudonym\" system on Ethereum traces back to Semaphore."
updated: 2026-10-25
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

In Semaphore v4, the verifier learns the message, the group root, the scope and the nullifier. The verifier does *not* learn which member of the group signaled.

That's the entire primitive. Everything else — anonymous voting, anonymous reputation, pseudonymous chat — is built by composing Semaphore with application logic.

## Construction

### Identity

A Semaphore v4 identity contains an EdDSA private key, its public key and an identity commitment. The commitment is the Poseidon hash of the public key and is the value added to the group’s Merkle tree. Keep the private key secret; the commitment is public.

### Group

A group is a Merkle tree of identity commitments. A membership proof shows that the prover’s commitment belongs to the tree without revealing which leaf it is.

### Proving

The circuit takes the EdDSA secret scalar derived from the private key and a private Merkle path. It derives the public key, hashes it into the identity commitment, and checks membership against the public Merkle root.

The public `scope` identifies the topic on which a member may act once. The circuit hashes the secret scalar with the scope to produce the `nullifier`, and binds the public `message` to the proof. The application checks the proof and rejects a nullifier already used for that scope.

### Proof system

The reference v4 implementation uses a Circom circuit and Groth16 proof generation through snarkjs. Its identity construction differs from the older trapdoor/nullifier identity model. See [SNARKs](/kb/snarks/) for the proof-system trade-offs.

## Group sizes and trade-offs

Proof generation selects artifacts for a circuit depth that accommodates the membership path. When no depth is supplied, the reference API chooses it from the actual Merkle proof length, with a minimum depth of one. It pads the path to the selected circuit depth before generating the proof.

This makes circuit capacity and the available proving artifacts relevant to group size; it does not require the group to remain at a single fixed tree depth throughout its lifetime.

## Applications

### Anonymous voting — MACI

**MACI** (Minimal Anti-Collusion Infrastructure, Buterin et al., 2019) uses Semaphore-style group commitments to enable anonymous, collusion-resistant voting. Voters publish encrypted ballots; a coordinator decrypts and tallies, while a SNARK proves the tally was computed correctly. MACI is used in Gitcoin grants and several DAO governance experiments.

The collusion resistance comes from a separate mechanism (key-rotation messages) on top of Semaphore-style identity proofs.

### Pseudonymous reputation — UniRep

**UniRep** (Liu et al., 2022, PSE) extends Semaphore into a *pseudonymous reputation* system. Each user has reputation that can be earned and proven about without linking actions to a single identity. Used as a primitive for "good-faith" pseudonymous accounts.

### Pseudonymous messaging — Heyanon, Sealcaster

Heyanon and Sealcaster let a user post messages signed as "a member of [group X]" — for example, "a Uniswap LP holder," "a Farcaster early user." The proof attests group membership without revealing which member. Useful for whistleblowing, anonymous endorsements, or pseudonymous community participation.

The message is public; the scope can be a topic or thread ID. The verifier uses the scope-bound nullifier to reject repeated actions from the same identity.

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
- The membership path must fit the selected circuit depth and proving artifacts.
- Proving requires the circuit artifacts for the selected depth.

## Implementation notes

The primary implementation is `semaphore-protocol/semaphore` on GitHub, maintained by PSE. It includes:

- Solidity contracts for on-chain group management and verifier.
- JavaScript/TypeScript SDK for proof generation and verification.
- Circom circuits and Groth16 proof generation for v4.
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

- [Semaphore v4 identities](https://docs.semaphore.pse.dev/guides/identities)
- [Semaphore v4 circuit inputs and outputs](https://docs.semaphore.pse.dev/technical-reference/circuits)
- [Semaphore reference proof generation](https://github.com/semaphore-protocol/semaphore/blob/main/packages/proof/src/generate-proof.ts)
- [Semaphore v4 identity commitment implementation](https://github.com/semaphore-protocol/semaphore/blob/main/packages/identity/src/index.ts)
- [Semaphore v4 Circom circuit](https://github.com/semaphore-protocol/semaphore/blob/main/packages/circuits/src/semaphore.circom)
