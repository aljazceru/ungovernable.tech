---
title: "Authenticated Data Structures"
slug: authenticated-data-structures
type: explainer
pillars: ["cryptography"]
description: "Merkle trees, accumulators and vector commitments: data structures that let anyone verify membership or non-membership against a short digest."
dek: "Data structures that commit to a set or map with a short digest, then let a prover demonstrate inclusion (or non-inclusion, or update) without sending the whole set. The trade-offs sit on a four-axis surface: proof size, verifier cost, update cost, and post-quantum status."
updated: 2026-04-26
created: 2026-04-26
origin: vault
source: "02-Cryptography/Authenticated Data Structures.md"
aliases: ["Cryptographic Accumulators", "Commitment Trees", "Authenticated Data Structures"]
tags: ["merkle", "verkle", "accumulator", "kzg", "transparency", "cryptography", "deep-dive"]
---

## What we want

For a set or key-value map `D`:

- A short *commitment* `c` that fixes `D` (collision-resistant).
- An *opening* `π_x` proving `x ∈ D` (or `x ∉ D`, or `D[x] = v`) given only `c`.
- Cheap verification.
- Reasonable update cost when `D` changes.
- Ideally, batched openings (one proof for many elements).

These properties trade against each other. Picking a structure means picking which axis to optimize.

## The classical landscape

### Merkle tree (Merkle, 1979)

Binary hash tree. Each leaf is `H(x_i)`; each internal node is `H(left || right)`. Commitment is the root.

- Inclusion proof: `O(log n)` hashes.
- Non-inclusion: requires a sorted Merkle tree (sparse or sorted-leaf) — vanilla Merkle trees do not support efficient non-inclusion.
- Update: `O(log n)` hashes.
- Post-quantum: yes, security reduces to hash collision resistance.

Merkle, *A Certified Digital Signature*, CRYPTO 1989 (the construction predates the paper, RSA Labs internal 1979).

### Sparse Merkle Tree (Dahlberg, Pulls, Peeters, 2016)

Conceptually a Merkle tree over `2^k` leaves indexed by a hash of the key, where most leaves are empty (default value). With path compression and empty-subtree shortcuts, an SMT supports both inclusion and non-inclusion proofs in `O(k)`. Used by:

- Ethereum's pre-Verkle state trees (a Merkle Patricia Trie variant with sparse semantics).
- Plasma / rollup commitment schemes.
- Trillian's verifiable map (Google).
- Certificate Transparency v2 maps.

Reference: Dahlberg, Pulls, Peeters, *Efficient Sparse Merkle Trees*, NordSec 2016.

### Merkle Patricia Trie (MPT)

Ethereum's pre-Verkle state structure. Hybrid of a radix trie and Merkle tree, with extension nodes to compress single-child paths. Quirks: the four-node-type encoding (leaf, extension, branch, NULL) makes proofs larger than necessary, and the trie depth is data-dependent, which has been a sustained source of state-growth pain in Ethereum.

### Verkle tree (Kuszmaul, 2019)

Vector commitment-based trie. Each internal node commits to its `k` children using a polynomial commitment (KZG or IPA). Witness for one leaf: one commitment opening per level — a single curve point regardless of branching factor.

For `k = 256`, depth at `n = 2^32` keys is ~4 levels, vs ~32 for a binary Merkle tree. Witness size is `O(depth × commitment_size)` ≈ a few hundred bytes for a state of millions of entries.

Ethereum has had Verkle on the roadmap since 2021. As of 2026 the production target is **Verkle migration in a future fork**, with extensive testing in Kaustinen testnet and stateless-client work continuing. The migration is large because every node operator must rebuild state. Date estimates have slipped multiple times; treat as "planned" not "imminent".

Reference: Kuszmaul, *Verkle Trees*, MIT 2019; Buterin's Ethereum-specific design notes (2021–2024); EIP-6800 family.

### RSA accumulator (Camacho, Hevia, 2010)

Membership in a set committed by `acc = g^(prod of primes for elements)` mod `N`. Inclusion proof: a witness `w` such that `w^p_x = acc`. Non-membership: a Bezout-coefficient pair.

- Constant-size proofs (one group element).
- Constant-size commitment.
- Update cost involves recomputing witnesses for all elements (mitigated by batched protocols like Boneh-Bünz-Fisch 2019).
- Requires trusted setup or class-group setup.
- Quantum: broken (Shor on the underlying RSA group).

Used in privacy-preserving cryptocurrencies (Zerocoin original construction), some IoT identity systems, and as a primitive inside larger ZK circuits.

Reference: Camacho, Hevia, *On the Impossibility of Batch Update for Cryptographic Accumulators*, LATIN 2010 (negative result on batch updates); foundational construction is older (Benaloh, de Mare, EUROCRYPT 1993).

### KZG-based vector commitments

KZG (Kate, Zaverucha, Goldberg, 2010) commits to a polynomial `f(X)` with a single elliptic-curve point. Opening `f(z) = y` requires one pairing check.

For a vector `(v_0, …, v_{n-1})`, encode as the polynomial `f(X) = Σ v_i · L_i(X)` where `L_i` are Lagrange basis polynomials. Then:

- Commitment: 1 elliptic-curve point.
- Single-element opening: 1 EC point.
- Batch opening of `k` elements: 1 EC point (a witness polynomial commit).
- Updates: `O(n)` to update the witness for any element after a single change (the *KZG amortization* problem).
- Trusted setup: yes, the *powers of tau* ceremony (an MPC). See [Multi-Party Computation](/kb/multi-party-computation/).
- Quantum: broken on standard pairing-friendly curves.

Used in:

- Ethereum **EIP-4844 / blobs** (production since Mar 2024 Dencun fork). Each blob is a 4096-element KZG commitment over BLS12-381.
- Verkle trees at each internal node.
- PLONK-family proving systems (the polynomial commitment is the workhorse).
- Aztec, Aleo, zkSync proof systems.

Reference: Kate, Zaverucha, Goldberg, *Constant-Size Commitments to Polynomials and Their Applications*, ASIACRYPT 2010.

### IPA (inner product argument) commitments

Bulletproofs-style polynomial commitment without trusted setup. Larger proofs (`O(log n)` field elements) but no MPC ceremony required. Used in Halo2 (Zcash) and earlier Verkle prototypes.

### Lattice-based / FRI commitments

Reed-Solomon + Merkle = FRI (Fast Reed-Solomon IOP of Proximity). Used in [STARKs](/kb/starks/). Hash-based, post-quantum, larger proofs (~50 KB for typical applications).

## Comparison

| Structure | Commitment | Inclusion proof | Non-inclusion | Update | PQ-safe | Setup |
|-----------|------------|-----------------|---------------|--------|---------|-------|
| Merkle tree | 32 B | `O(log n)` × 32 B | needs sorting | `O(log n)` hashes | yes | none |
| Sparse Merkle | 32 B | `O(k)` × 32 B | yes | `O(k)` hashes | yes | none |
| Patricia trie | 32 B | `O(log n)` × few hundred B | depends | `O(log n)` | yes | none |
| Verkle (KZG) | 48 B | ~200–500 B | yes | `O(n)` witness reseed | no | trusted setup |
| Verkle (IPA) | 32 B | `O(log n) × 32 B` | yes | similar | no | none |
| RSA accumulator | ~256 B | 1 group element | yes | hard to batch | no | trusted or class group |
| KZG vector | 48 B | 48 B | requires extra | `O(n)` for any element | no | trusted setup |
| FRI / STARK commit | 32 B | tens of KB | yes | rebuild | yes | none |

Numbers are rough; exact sizes depend on curve and parameter choices.

## Applications

### Blockchain state roots

- **Bitcoin** uses a Merkle tree for the transaction set in each block (`txroot`).
- **Ethereum pre-Verkle** uses a Merkle Patricia Trie for `stateRoot`, `transactionsRoot`, and `receiptsRoot`. Witness size for stateless clients is the pain point driving Verkle.
- **Cosmos SDK / Tendermint** uses an IAVL+ tree (an AVL-Merkle hybrid).
- **Diem / Aptos / Sui** use Jellyfish Merkle Trees (a sparse Merkle variant).

### Transparency logs

- **Certificate Transparency** (RFC 9162, Dec 2021) uses a Merkle tree to commit to the log of issued TLS certificates. Auditors verify inclusion and consistency proofs.
- **Sigstore Rekor** uses a Trillian-backed Merkle log for code-signing transparency.
- **Go module checksum database** uses the same primitive.
- **Binary transparency** efforts (Mozilla, Debian rebuilds) follow the same model.

The Merkle tree is the right tool here because logs are append-only — the update pattern is friendly to hash trees, and post-quantum safety is desired.

### Verifiable maps and key transparency

- **WhatsApp Auditable Key Directory** and **Apple Contact Key Verification** (2023) use a verifiable map (sparse Merkle tree variant) so users can audit that the server reports the same public key for an account to everyone.
- **Keybase merkle tree** (predecessor of the above patterns).

### ZK proof systems

KZG is the polynomial commitment inside PLONK, Halo2 (with IPA option), Marlin, and most production SNARKs. STARKs use FRI. The choice of authenticated data structure deeply affects proof size and prover/verifier cost. See [SNARKs](/kb/snarks/) and [STARKs](/kb/starks/).

### Privacy-preserving credentials

RSA accumulators historically appear in Zerocoin, Idemix, and some VC schemes for revocation lists. Modern designs typically use cryptographic accumulators or sorted Merkle trees with ZK proofs of (non-)membership.

## Trade-offs

### Pick Merkle when

- Append-only.
- Post-quantum required.
- No need for compact proofs.
- No setup ceremony tolerated.

### Pick Verkle / KZG vector commit when

- Witness size dominates verifier cost (stateless clients).
- Trusted setup is acceptable (and a ceremony exists).
- PQ migration is planned but not blocking.

### Pick RSA accumulator when

- Fixed-size proofs matter and class-group setup is acceptable.
- Update churn is low (or batched protocols available).

### Pick FRI when

- PQ safety required *and* compact proofs not strictly necessary.
- Verifier hardware is constrained (hashing only).

## Pitfalls

- **Second-preimage vs collision resistance.** Merkle proofs need second-preimage resistance for the *combiner* and collision resistance for the leaves; a hash that's collision-resistant for short inputs may be weak under length extension if used naively.
- **Domain separation.** Hash leaf and internal nodes with different prefixes (`0x00 || leaf` vs `0x01 || left || right`) — a longstanding Merkle pitfall (RFC 6962 mandates this for CT).
- **Non-inclusion requires sortedness or sparseness.** Vanilla unsorted Merkle trees cannot prove non-membership efficiently.
- **KZG witness updates are not free.** Touching one entry invalidates all witnesses; batched precomputation and amortized-update protocols mitigate but don't eliminate.
- **Trusted setup in KZG.** A compromised Powers of Tau ceremony breaks soundness. The Ethereum KZG ceremony (2023, ~140k contributors) sets the bar.

## Primary sources

- Merkle, *A Certified Digital Signature*, CRYPTO 1989.
- Benaloh, de Mare, *One-Way Accumulators: A Decentralized Alternative to Digital Signatures*, EUROCRYPT 1993.
- Kate, Zaverucha, Goldberg, *Constant-Size Commitments to Polynomials and Their Applications*, ASIACRYPT 2010.
- Dahlberg, Pulls, Peeters, *Efficient Sparse Merkle Trees*, NordSec 2016.
- Kuszmaul, *Verkle Trees*, MIT 2019.
- Boneh, Bünz, Fisch, *Batching Techniques for Accumulators with Applications to IOPs and Stateless Blockchains*, CRYPTO 2019.
- Laurie, Messeri, Stradling, *Certificate Transparency Version 2.0*, RFC 9162 (Dec 2021).
- Ethereum Verkle EIPs: EIP-6800 family.
- Ethereum KZG ceremony: [ceremony.ethereum.org](https://ceremony.ethereum.org).
- Trillian: [github.com/google/trillian](https://github.com/google/trillian).
- Sigstore Rekor: [github.com/sigstore/rekor](https://github.com/sigstore/rekor).
