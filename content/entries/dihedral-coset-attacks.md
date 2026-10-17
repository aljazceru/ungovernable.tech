---
title: "The Dihedral Coset Attack Line"
slug: dihedral-coset-attacks
type: deep-dive
pillars: ["pqc"]
readiness: research
description: "The dihedral coset problem and the line of quantum attacks on lattice cryptography it inspires: what has been claimed, refuted and still matters."
dek: "Deep-dive companion to Post-Quantum Saturday — August 22 2026 Weekly Update and Overview - Post-Quantum Cryptography. This note consolidates the twenty-year research program connecting the Dihedral Coset Problem to lattice problems and LWE — Regev 2004 → BKSW 2018 → Chen 2024 → Bai et al. 2025 → Wen–Zheng 2026 → Simon 2026 → GRZ 2026 — including what was claimed, what survived, and where the live edges are. Flagged as a needed deep-dive in the August 15 update (§Next Steps #4)."
updated: 2026-08-22
created: 2026-08-22
origin: vault
source: "10-Post-Quantum/The Dihedral Coset Attack Line.md"
aliases: ["DCP Attack Line", "Dihedral Coset Problem Attack Line", "The EDCP Research Program"]
tags: ["pqc", "post-quantum", "dcp", "edcp", "module-lwe", "lattice-cryptanalysis", "quantum-cryptanalysis", "simon-algorithm", "no-go-theorem", "regev", "kuperberg", "wen-zheng", "bai-et-al", "chen-2024", "attack-line", "freedom-tech"]
---

## Why this line matters

The single most important open question in quantum lattice cryptanalysis is whether dihedral hidden-subgroup-type techniques can solve lattice problems faster than classical BKZ. If yes, most deployed PQC (ML-KEM, ML-DSA, and much else) rests on weakened foundations. If no, the quantum threat to lattices remains "Shor-for-ECC/RSA plus nothing for lattices," and the migration calculus barely changes.

For twenty years the answer has been "no": the best quantum algorithm for the dihedral problem was Kuperberg's 2005 subexponential 2^O(√n), and for polynomial-factor approximate SVP nothing beat fully exponential. That was the load-bearing assumption under FIPS 203/204/206 and the entire NIST lattice portfolio.

Three attempts in three years (Chen 2024, Luo 2026, Simon 2026) have now pushed directly on this assumption. All three died under scrutiny. But each attempt narrowed the gap between the abstract problem and ML-KEM's exact mathematics, and the bridge paper that would make a future attempt consequential — Wen–Zheng — survived peer review at CRYPTO 2026. This note is the map of that territory.

## The problem chain, from scratch

**DCP (Dihedral Coset Problem).** Given quantum coset states for the dihedral group D_N = ℤ_N ⋊ ℤ_2, recover the hidden subgroup element s ∈ ℤ_N. The "extrapolated" variant (EDCP) allows multiple samples per coset and different moduli; "IP-M-EDCP" is Wen–Zheng's integer-polynomial module variant.

The connection to lattices runs one direction: quantum reductions *from* lattice problems *to* DCP-family problems. If someone builds a fast DCP solver, the reductions turn it into a lattice attack. If nobody does, the reductions are elegant mathematics with no customer. That asymmetry — twenty years of bridge-building waiting for a solver — is the shape of this whole research line.

```
   DEPLOYED CRYPTO                     ABSTRACT PROBLEMS                    SOLVERS
   ──────────────                      ────────────────                    ────────
   ML-KEM / ML-DSA          Wen–Zheng 2026 (↔, CRYPTO '26)
        Module-LWE  ───────────────────→  IP-M-EDCP
                                         (search, power-of-two      ↓
                                          cyclotomic, const rank)  EDCP   ←── Bai et al. 2025
                                                                    ↓        (quasi-poly, CRYPTO '25)
        plain LWE  ── BKSW 2018 (↔) ──────────────────────→        DCP    ←── Kuperberg 2005
        unique-SVP ── Regev 2004 (→)                                ↑        (subexp 2^O(√n))
                                                                    └──────── Simon 2026 (poly claim)
                                                                             REFUTED Aug 15 (GRZ no-go)
```

## The papers, in order

### Regev 2004 — the bridge is built

Oded Regev, "Quantum Computation and Lattice Problems," SIAM Journal on Computing 2004 (FOCS 2003 lineage). Polynomial-time **quantum reduction** from approximate unique-SVP (and related lattice problems) to the Dihedral Subgroup Problem — conditional on an efficient coherent solver for average-case modular subset-sum. No such solver existed. The result sat for twenty years as elegant mathematics with the attack-shaped hole where a solver should be.

**Why it still matters**: every subsequent paper in this line is either strengthening the reduction (BKSW, Wen–Zheng) or trying to fill the solver hole (Kuperberg-line, Chen, Bai, Simon).

### Kuperberg 2005 — the floor

Greg Kuperberg's subexponential 2^O(√n)-time algorithm for the dihedral hidden subgroup problem. Improved constants followed (Kuperberg 2011 ~2^(√2·√log N)), but the shape never changed: subexponential, not polynomial. For two decades this defined "the best a quantum computer does against the dihedral problem."

**Status 2026**: still the best actual algorithm. Unchanged in essence for 21 years.

### BKSW 2018 — the equivalence tightened

Brakerski, Kirshanova, Stehlé, Wen, "Learning With Errors and Extrapolated Dihedral Cosets," EUROCRYPT 2018. Proved LWE ⇄ EDCP quantum-polynomially for suitable parameters — deepening the connection from "lattice problems reduce to DCP" to "LWE and the extrapolated problem are essentially the same difficulty quantumly." Elena Kirshanova (co-author) became one of the central verifiers of the Simon claim in Aug 2026 — the same research program, continuing.

**Note**: Wen (Télécom Paris) is a co-author of both BKSW 2018 and Wen–Zheng 2026. This is one research lineage, not independent arrival.

### Chen 2024 — first poly-time claim, first death

Yilei Chen, "Quantum Algorithms for Lattice Problems," ePrint 2024/555 (April 2024). Claimed polynomial-time quantum algorithms for approximate SVP via a variant of EDCP. **Withdrawn within days**: Hongxun Wu and Thomas Vidick found the flaw (in the LWE-to-EDCP step's analysis of the Gaussian sampling subroutine). Vidick is thanked in Simon's acknowledgments — the community's failure-detection loop is tight and self-aware.

### Bai et al. 2025 — the real advance, honestly bounded

Bai, Jangir, Kirshanova, Ngo, Youmans, "A Quasi-Polynomial Quantum Algorithm for the Extrapolated Dihedral Coset Problem," CRYPTO 2025 (ePrint 2025/1046). A genuine algorithmic improvement: quasi-polynomial time for EDCP over power-of-two moduli. The authors' own constraints (sample counts, modulus bounds) prevent it from reaching standard LWE parameters. This is what a credible step forward in this line looks like: new algorithm, explicit parameter limits, no overclaim.

**Status 2026**: the strongest actual algorithmic result in the line. Un-refuted, bounded.

### Wen–Zheng 2026 — the bridge reaches ML-KEM's ring

Weiqiang Wen, Jinwei Zheng (Télécom Paris), "Module Learning With Errors and Structured Extrapolated Dihedral Cosets," CRYPTO 2026 (ePrint 2026/155).

- **Theorem 1**: quantum-polynomial **equivalence** between search Module-LWE and Gaussian IP-M-EDCP, for f(x) = x^d + 1 with d a power of two, module rank n = O(1), q = poly(d). *This is ML-KEM's exact setting*: ℤ_3329[x]/(x²⁵⁶+1), ranks 2/3/4.
- **Theorem 2**: IP-M-EDCP reduces to plain EDCP (dimension-modulus switching).
- **Sample amplification** via Lyubashevsky–Peikert–Regev regularity — why the result needs cyclotomics.
- **Limits, in the authors' own words**: search (not decision) Module-LWE; Rényi divergence "does not naturally extend to decision variants"; the converse of Theorem 2 unproven — IP-M-EDCP may be strictly easier than EDCP.
- **The invitation**: they name adapting Kuperberg and adapting Bai et al. as the two promising attack directions, and explicitly invite cryptanalysts to attack IP-M-EDCP.

**Why it survived the Simon refutation untouched**: it is a reduction, not a solver. Its truth does not depend on whether anyone has a fast DCP algorithm. Its *consequence* does — which is why the refutation demoted it from "route to a poly-time attack" back to "map waiting for a traveler."

### Simon 2026 — the claim that wasn't

Daniel R. Simon (AWS Cryptography), "A Polynomial-Time Quantum Algorithm for the Dihedral Coset Problem," ePrint 2026/1591 (submitted Aug 3, approved Aug 6; manuscript dated Jul 31). Claimed to replace Regev's subset-sum oracle requirement with Hadamard transforms plus a grouping strategy tolerating faulty-sample rates up to 1/O(log n), composing with Regev + BKSW to poly-time algorithms for approximate SVP (factor O(√n polylog n)) and LWE (α = O(√n polylog n)).

**Author credibility was maximal** — creator of Simon's algorithm (1994), the result Shor built on. Acknowledgments thanked Micciancio, Vaikuntanathan, Vidick, Ragavan, Menda. The final corollary rested on unpublished personal communications from Ragavan and Micciancio.

**Death by no-go theorem, Aug 15** (full timeline in the [August 22 update](/briefings/post-quantum/2026-08-22/) §1): Gupte–Ragavan–Zhandry (ePrint 2026/1693) proved the algorithm itself cannot work —

- after step 3 it never touches the classical Fourier labels, using them only via top log n bits of block inner products;
- implementable up to error poly(n)·2^(−n/3) from the top third of labels alone;
- any Regev-template algorithm keeping only that much cannot distinguish the secret's LSB (advantage ≤ poly(n)·2^(−n/3));
- discarding ω(log n) bits per label hides the answer information-theoretically;
- dichotomy: wrong, or Ω(2^(n/9)) runtime — not both subexponential and correct;
- **Lean 4 machine-check code released** (github.com/sragavan99/lean-ePrint-2026-1591-refutation).

Ragavan — a personal-communication source for Simon's corollary — co-authored the refutation. For the detailed nine-day verification arc (Discord, Overleaf, Apon's "The Search for Simon" AQSE paper, the Lemma-3 one-page counterexample, the Lemma-4 non-negativity substitution defect), see the August 22 update.

### GRZ 2026 — the refutation as a positive result

Read as more than a rebuttal, ePrint 2026/1693 contributes a reusable insight: **any DCP algorithm on Regev's template must make extensive use of the classical Fourier labels in the uncomputation stage**. That is a design constraint for every future attempt — it tells the next Simon where not to look. No-go theorems shape search spaces; this one is now the guardrail for the entire line, and it is machine-checked.

## Post-refutation exposure map

| Family / Scheme | Assumption | DCP-line exposure | Notes |
|---|---|---|---|
| **ML-KEM (FIPS 203)** | Module-LWE, power-of-two cyclotomic, rank 2/3/4 | **Bridge exists (Wen–Zheng), no solver** | Composition at real parameters unproven even before the refutation (decision vs search, CBD vs Gaussian, sample budget); now also solver-less |
| **ML-DSA (FIPS 204)** | Module-LWE/SIS + SelfTargetMSIS | One step removed | A Module-LWE break ≠ automatic forgery; forgery needs its own analysis |
| **FN-DSA / Falcon (FIPS 206 IPD)** | NTRU | **Not implicated by this path** | No published DCP-line reduction to NTRU; separate assessment required |
| FrodoKEM | plain LWE | Nearest Simon's direct corollary | The "conservative" unstructured choice sat closest to the (now-dead) claim — an inversion of the usual hierarchy worth remembering |
| **HQC** | quasi-cyclic codes | Untouched | Code-based; standard expected 2026–27; see the McEliece distinguisher backfill for the code-side margin story |
| Classic McEliece | binary Goppa codes | Untouched by DCP line | New quasipoly distinguisher (Aug 2026) is a separate, non-break development |
| **SLH-DSA, LMS/XMSS** | hash functions | Untouched | The conservative backbone assumption holds regardless |
| AES / SHA-2 / SHA-3 | symmetric | Untouched | Grover halvings only; 7-round AES-128 margin result is reduced-round |

## What would actually change the picture

Ordered by what a watcher should rank as signal:

1. **A repaired or new DCP solver that provably uses the Fourier labels extensively in uncomputation** — the GRZ constraint is the entry ticket. Anything claiming poly or quasi-poly time that doesn't address it is dead on arrival.
2. **Any composition result at ML-KEM's concrete parameters** — decision Module-LWE (not search), centered-binomial noise, fixed small sample budget, ℤ_3329[x]/(x²⁵⁶+1). Even a quasi-polynomial composed attack at real parameters would reprice risk.
3. **Bai et al. line extensions** — the 2025 quasi-poly EDCP result relaxing its sample/modulus constraints toward cryptographic parameters.
4. **IP-M-EDCP-specific attacks** — the Wen–Zheng open problem: is their structured variant strictly easier than EDCP? A yes with an algorithm attached is the next bridge to cross.
5. **Circuit-level resource estimates for any of the above** — without qubit counts and depth, nothing changes CRQC timelines (the mitten-codes lesson from the Aug 15 update: qLDPC overhead is compressible, uncertainty bands are wide).

## Historical pattern — the claim survival table

| Claim | Author stature | Venue | Survival | Time to death | Detected by |
|---|---|---|---|---|---|
| Poly-time quantum lattice (2024) | Yilei Chen (Tsinghua) | ePrint 2024/555 | ✗ Withdrawn | ~days | Wu & Vidick expert read |
| LWE attack (Jan 2026) | Luo | ePrint | ✗ Fatally flawed | ~days | Community |
| **Poly-time DCP (Aug 2026)** | **Daniel Simon (AWS)** | ePrint 2026/1591 | ✗ **No-go theorem** | **9 days** | Discord verification → Apon counterexample → GRZ theorem (Lean 4) |
| Quasi-poly EDCP (2025) | Bai et al. | CRYPTO 2025 | ✓ Standing (bounded) | — | — |
| Kuperberg subexp (2005) | Kuperberg | — | ✓ Standing (21 years) | — | — |

The pattern: extraordinary claims die fast and publicly; incremental honest results survive with explicit bounds. The 2024→2026 sequence also shows verification *accelerating* — from expert-read (days) to machine-checked no-go (nine days, with Lean). Assume the next extraordinary claim gets the same treatment on an even shorter clock, likely with AI assistance at the search stage (the HAWK/Mythos precedent from July).

## Deployment guidance (unchanged, now boringly so)

- **Transport**: hybrid `X25519MLKEM768` — now **RFC 10024** (Proposed Standard, Aug 2026). See [Hybrid KEM Migration](/guides/hybrid-kem-migration/).
- **Signatures**: hybrid Ed25519+ML-DSA for high-value long-lived keys (Bernstein's bug-economics argument, June 2026); SLH-DSA as conservative backup.
- **Diversification**: HQC when standardized (2026–27); SLH-DSA now. Keep the "entire estate = one assumption family" concentration risk on the register — the refutation removed the urgency, not the epistemics.
- **Crypto-agility**: architecture, not library swap. The nine-day arc is the argument: whatever the next claim is, the response window will be shorter than a procurement cycle.
- **What NOT to do**: pause migrations over cryptanalysis news. Every HNDL clock (2030/2031/2035 regulatory deadlines) runs through the debate.

## Open questions

1. Will Simon respond to the no-go — revision, withdrawal, or silence? (No statement as of Aug 22, 2026.)
2. Does anyone take Wen–Zheng's IP-M-EDCP invitation? Watch ePrint for 2026/1693-citing work.
3. Will the GRZ Lean artifact set precedent — machine-checked refutations as the new norm for extraordinary claims?
4. Does the AI-cryptanalysis economics shift ($100K/week per result) eventually get pointed at EDCP/IP-M-EDCP directly — the first AI-found solver in this line?
5. HQC standardization (2026–27): does the McEliece distinguisher line change NIST's code-based timing or messaging?

## Related

- [Post-Quantum Saturday — August 22 2026 Weekly Update](/briefings/post-quantum/2026-08-22/) — the refutation week in detail
- [Post-Quantum Saturday — August 15 2026 Weekly Update](/briefings/post-quantum/2026-08-15/) — Simon claim + Wen–Zheng first analysis
- [Post-Quantum Saturday — August 08 2026 Weekly Update](/briefings/post-quantum/2026-08-08/) — the Luo preprint; ML-DSA bug economics
- [Overview - Post-Quantum Cryptography](/kb/post-quantum-cryptography/) — standards and deployment context
- [ML-KEM](/kb/ml-kem/) / [ML-DSA](/kb/ml-dsa/) / [FN-DSA Falcon](/kb/fn-dsa-falcon/) / [HQC](/kb/hqc/) / [SLH-DSA](/kb/slh-dsa/) — the exposed algorithms
- [Hybrid KEM Migration](/guides/hybrid-kem-migration/) — operational playbook (RFC 10024)
- [Merkle Tree Certificates](/kb/merkle-tree-certificates/) — the PQ Web PKI track that proceeds regardless
- [PQC Deployment and Libraries Tracker](/kb/pqc-deployment-tracker/) — the deployment map

*Primary sources: ePrint 2026/1693 (GRZ no-go), 2026/1591 (Simon), 2026/155 (Wen–Zheng), 2025/1046 (Bai et al.), 2024/555 (Chen, withdrawn), Regev SIAM J. Comput. 2004, BKSW EUROCRYPT 2018, Kuperberg 2005/2011; github.com/sragavan99/lean-ePrint-2026-1591-refutation; github.com/a-as-plus-e/lemma3-objection; PostQuantum.com analyses (Ivezic, Aug 6/15); IACR News Aug 15, 2026. Links verified August 22, 2026.*
