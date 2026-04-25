---
title: "Research Methodology"
tags:
  - "meta"
  - "methodology"
  - "evidence"
---
## How We Evaluate Claims

Every technology in this knowledge base is evaluated against a rigorous framework. We prioritize:

---

## Primary Source Hierarchy

| Level | Source Type | Weight |
|-------|------------|--------|
| 1 | Peer-reviewed cryptography papers (ePrint, IACR) | Highest |
| 2 | Audited open-source implementations | High |
| 3 | Production specifications (IETF RFCs) | High |
| 4 | Active open-source projects | Medium |
| 5 | Whitepapers, blog posts | Medium-Low |
| 6 | Marketing materials | Skip |

---

## Evaluation Criteria

### 1. Cryptographic Soundness

- Is the underlying crypto well-studied?
- Are there known attacks or weaknesses?
- Has it been audited by reputable firms?
- Are there formal proofs where applicable?

### 2. Trust Model Analysis

- Who or what must you trust?
- What happens if that trust is betrayed?
- Can you verify the system independently?
- What's the key management story?

### 3. Attack Surface

- What are the practical attack vectors?
- How does the system degrade under attack?
- Are there metadata leaks?
- What's the worst-case compromise?

### 4. Decentralization Claims

- How many entities control the network?
- What's the Sybil resistance mechanism?
- Can the network be shut down?
- Are there backdoors or kill switches?

### 5. Operational Complexity

- What's the user experience?
- How easy to get wrong?
- What's the recovery story?
- Are there good defaults?

---

## Evidence Tags

Each file includes evidence assessment:

```yaml
evidence:
  cryptographic: strong|moderate|weak|experimental
  implementation: production|beta|experimental
  audits: independent|internal|none
  track_record: years|months|new|unknown
```

---

## Claims We Are Skeptical Of

- "Decentralized" but requires permission to join
- "Private" but leaks metadata
- "Uncensorable" but has admin keys
- "Trustless" but requires trusted setup
- "Anonymous" but requires ID verification

---

## Key Questions for Each Technology

1. **What problem does this solve?**
2. **What's the trust assumption?**
3. **What's the failure mode?**
4. **What's the operational complexity?**
5. **What's the legal risk?**

---

## Status Legend

Every content file's `status:` frontmatter must use one of these values. The legend is closed — proposals to add values go in [CHANGELOG](/meta/changelog).

| Status | Meaning | Minimum content |
|--------|---------|-----------------|
| **stub** | Title and frontmatter only; placeholder for planned work | YAML frontmatter, intent statement |
| **draft** | Substantive notes; structure may be incomplete; claims unverified | Overview, at least one cited source |
| **active** | Topic under active research; structure complete but content evolving | Full sections, multiple sources, links to related files |
| **mature** | Stable; reviewed; cross-referenced; threat model and trade-offs included | All required sections, primary sources, attack surface, trade-offs |
| **archived** | Superseded or no longer applicable; kept for historical reference | Original content + `superseded_by:` link in frontmatter |

### Required sections by status

| Section | stub | draft | active | mature |
|---------|------|-------|--------|--------|
| Frontmatter | ✓ | ✓ | ✓ | ✓ |
| Overview | — | ✓ | ✓ | ✓ |
| Historical context | — | — | ✓ | ✓ |
| Trade-offs | — | — | ✓ | ✓ |
| Attack Surface / Threat Model | — | — | — | ✓ |
| Primary Sources | — | ✓ | ✓ | ✓ |
| Related Files (wikilinks) | — | — | ✓ | ✓ |

---

## Tag Taxonomy

Tags use `lowercase-kebab-case`. Use only tags from the controlled vocabulary or extend it via [CHANGELOG](/meta/changelog). Each file should carry **2-6 tags** drawn from:

- **Topic family** — `confidential-computing`, `cryptography`, `networking`, `financial`, `messaging`, `identity`, `dns`, `mix-networks`, `zk`, `pqc`
- **Technology** — `tee`, `sgx`, `tdx`, `sev-snp`, `fhe`, `pir`, `lightning`, `coinjoin`, `nostr`, `signal`, `tor`, `i2p`, `meshtastic`, `reticulum`, `ml-kem`, `ml-dsa`
- **Property** — `privacy`, `anonymity`, `metadata-resistance`, `censorship-resistance`, `self-custody`, `attestation`, `forward-secrecy`
- **Document type** — `overview`, `deep-dive`, `comparison`, `threat-model`, `pattern`, `glossary`, `meta`
