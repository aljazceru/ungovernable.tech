---
title: "Building a ZK membership proof"
slug: building-a-zk-membership-proof
type: guide
pillars: [zk, identity]
readiness: usable
description: "Build a Semaphore v4 membership proof, verify its group and scope, reject repeat submissions, and understand which inputs remain private."
dek: "Prove that an accepted group member submitted a message without naming the member."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [semaphore, zero-knowledge-proofs, proof-of-personhood, identity-and-pseudonymity]
level: intermediate
---

## Summary

[Semaphore](/kb/semaphore/) combines identity commitments, a Merkle-tree group and a zero-knowledge proof. This walkthrough uses the documented **v4** JavaScript API. The verifier must apply application policy as well as check the proof.

## 1. Create an identity and group

In a Node.js project, install the v4 packages and save the example below as `membership.mjs`:

```sh
npm install @semaphore-protocol/identity@4 @semaphore-protocol/group@4 @semaphore-protocol/proof@4
```

An identity has a private key, public key and commitment. Publish only the commitment to the group manager. The [identity guide](https://docs.semaphore.pse.dev/guides/identities) documents export/import for recovery; keep an exported identity secret. The [group guide](https://docs.semaphore.pse.dev/guides/groups) documents adding commitments and deriving the root.

## 2. Generate and verify a proof

This example creates two disposable members. In a real application, members generate their own identities and the admission process supplies the approved commitment list.

```js
import { Identity } from "@semaphore-protocol/identity"
import { Group } from "@semaphore-protocol/group"
import { generateProof, verifyProof } from "@semaphore-protocol/proof"

const identity = new Identity()
const otherMember = new Identity()
const group = new Group([identity.commitment, otherMember.commitment])
const scope = 42n // Example application action ID, fixed by the verifier.
const message = 1n // Example public vote.
const proof = await generateProof(identity, group, message, scope)

// Verifier policy is configured independently of the incoming proof.
const approvedRoot = group.root.toString()
const approvedScope = scope.toString()
const spent = new Set()

async function accept(candidate) {
    if (candidate.merkleTreeRoot !== approvedRoot) {
        throw new Error("Unapproved group")
    }
    if (candidate.scope !== approvedScope) {
        throw new Error("Wrong action")
    }
    if (!["0", "1"].includes(candidate.message)) {
        throw new Error("Invalid vote")
    }
    if (!(await verifyProof(candidate))) {
        throw new Error("Invalid proof")
    }
    // Canonicalize: "0123" and "123" are the same field element to the verifier.
    const key = `${candidate.scope}:${BigInt(candidate.nullifier).toString()}`
    if (spent.has(key)) throw new Error("Already submitted")
    spent.add(key)
    return candidate.message
}

console.log("Accepted public message:", await accept(proof))
try {
    await accept(proof)
    throw new Error("Replay was accepted")
} catch (error) {
    if (error.message !== "Already submitted") throw error
    console.log("Replay rejected")
}
try {
    await accept({ ...proof, nullifier: "0" + proof.nullifier })
    throw new Error("Re-encoded replay was accepted")
} catch (error) {
    if (error.message !== "Already submitted") throw error
    console.log("Re-encoded replay rejected")
}
process.exit(0) // End this command-line demo, including proof-library workers.
```

Run `node membership.mjs`. Proof generation may retrieve proving artifacts; the example is not an offline-install recipe. The [proof guide](https://docs.semaphore.pse.dev/guides/proofs) documents `generateProof(identity, group, message, scope)` and `verifyProof(proof)`.

## 3. Enforce the application boundary

The reference `verifyProof` checks the cryptographic statement supplied in the proof. It does not decide whether your application approves that group or scope, or store spent nullifiers. The checks above make those decisions explicit.

For deployment, persist acceptance and the `(scope, nullifier)` uniqueness check in one database transaction, keyed on the canonical integer form of the nullifier. The in-memory set is only a demonstration. Configure a stable scope for each action; accepting arbitrary scopes lets the same member submit under different nullifiers. Define which historical group roots remain acceptable when membership changes.

## What is private and public?

The [v4 circuit reference](https://docs.semaphore.pse.dev/technical-reference/circuits) identifies the secret scalar and membership path as private inputs. The root, scope, nullifier and message are public. Publishing a proof does not encrypt the message or conceal the sender's network connection.

## Trust model / threat model

Trust the admission process to define the intended group, and the verifier to enforce its policy. Membership is not proof of a unique human; see [proof of personhood](/kb/proof-of-personhood/) and [Sybil resistance](/glossary/#sybil-resistance). The tiny example group offers no useful anonymity for sensitive use.

## Readiness and limits

**Usable for supported v4 integrations.** Protect identity backups, review proving artifacts and verifier dependencies, and test rejected roots, scopes, altered messages and replay before accepting real submissions. Do not send the identity private key to a remote prover merely to simplify the client.

## Primary sources

- [Semaphore v4 identities](https://docs.semaphore.pse.dev/guides/identities)
- [Semaphore v4 groups](https://docs.semaphore.pse.dev/guides/groups)
- [Semaphore v4 proof generation and verification](https://docs.semaphore.pse.dev/guides/proofs)
- [Semaphore v4 circuit inputs and outputs](https://docs.semaphore.pse.dev/technical-reference/circuits)
- [Reference proof type](https://raw.githubusercontent.com/semaphore-protocol/semaphore/main/packages/proof/src/types/index.ts)
- [Reference verifier](https://raw.githubusercontent.com/semaphore-protocol/semaphore/main/packages/proof/src/verify-proof.ts)
- [Reference generator and artifact loading](https://raw.githubusercontent.com/semaphore-protocol/semaphore/main/packages/proof/src/generate-proof.ts)
