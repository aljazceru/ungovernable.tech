---
title: "Compare fully homomorphic encryption libraries"
slug: compare-fhe-libraries
type: comparison
pillars: ["confidential", "cryptography"]
readiness: usable
description: "Compare OpenFHE, TFHE-rs, Microsoft SEAL, Lattigo and HElib by schemes, implementation language, license and documented bootstrapping support."
dek: "Choose by the computation and security parameters you need, then benchmark the actual circuit."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: ["fully-homomorphic-encryption", "fhe-bootstrapping-and-verification", "confidential-computing"]
---

## Summary

These libraries expose different kinds of encrypted computation. Integer arithmetic, approximate arithmetic and Boolean or lookup-table evaluation are not interchangeable workloads. The table follows the cited upstream repositories; it does not rank speed or imply that default examples are suitable security parameters for a new application.

## Comparison

| Library | Main implementation | Documented schemes | License | Bootstrapping documented upstream |
|---|---|---|---|---|
| [OpenFHE](https://github.com/openfheorg/openfhe-development) | C++ | BFV, BGV, CKKS; FHEW/TFHE-family and related Boolean/lookup-table schemes | BSD 2-Clause | Approximate CKKS bootstrapping, Boolean/functional bootstrapping and scheme switching. |
| [TFHE-rs](https://github.com/zama-ai/tfhe-rs) | Rust, with C and client-side WebAssembly interfaces | TFHE variant for Boolean and integer operations | BSD 3-Clause Clear | Programmable bootstrapping. |
| [Microsoft SEAL](https://github.com/microsoft/SEAL) | C++, with .NET components | BFV, BGV, CKKS | MIT | Not provided: a maintainer states in the linked issue that there are no plans to add it. |
| [Lattigo](https://github.com/tuneinsight/lattigo) | Go | BFV/BGV and CKKS; multiparty variants and lower-level primitives | Apache 2.0 | CKKS bootstrapping; separate interactive multiparty refresh protocols. |
| [HElib](https://github.com/homenc/HElib) | C++ | BGV and CKKS | Apache 2.0 | BGV bootstrapping. The cited overview does not establish CKKS bootstrapping. |

The TFHE-rs license expressly grants no patent rights. Do not read the word “BSD” alone as a complete account of its terms. Consult the license at the revision you plan to use.

## How to choose

Start with [fully homomorphic encryption](/kb/fully-homomorphic-encryption/) and [bootstrapping and verification](/kb/fhe-bootstrapping-and-verification/). Write down whether the result must be exact or approximate, which operations dominate, who holds decryption keys, and whether interaction with key holders is acceptable.

Prototype the whole computation, including key generation, ciphertext transfer and decryption. Keep the security level, precision, hardware and circuit identical when comparing measurements. A library name or one bootstrapping benchmark is not a performance budget.

## Trust model / threat model

Microsoft SEAL's documentation distinguishes encrypted computation from running an arbitrary encrypted program and warns about operation and efficiency constraints. Do not infer that an encrypted result proves the evaluator followed the intended computation. Define result validation separately and review the library's security guidance, especially where decryption results may be exposed.

Multiparty protocols also change the trust model: Lattigo documents secret-shared keys and interactive operations. Count those participants and their availability requirements rather than treating the arrangement as an ordinary single-key service.

## Readiness

**Usable for specialist development.** The libraries publish working APIs and examples. A production application still needs parameter selection, implementation review and workload-specific testing.

## Limits

No release numbers, throughput rankings or blanket production-security claims are made here. Licenses and APIs should be checked at a pinned revision. Compare [confidential computing](/kb/confidential-computing/) when deciding whether hardware isolation or encrypted computation matches the workload.

## Primary sources

- [OpenFHE schemes and examples](https://github.com/openfheorg/openfhe-development)
- [TFHE-rs interfaces and programmable bootstrapping](https://github.com/zama-ai/tfhe-rs)
- [TFHE-rs BSD 3-Clause Clear license and patent exclusion](https://github.com/zama-ai/tfhe-rs/blob/main/LICENSE)
- [Microsoft SEAL schemes, language and limitations](https://github.com/microsoft/SEAL)
- [Lattigo schemes, CKKS bootstrapping and multiparty protocols](https://github.com/tuneinsight/lattigo)
- [HElib schemes, BGV bootstrapping and license](https://github.com/homenc/HElib)
- [HElib C++ build requirements](https://github.com/homenc/HElib/blob/master/INSTALL.md)
- [Microsoft SEAL maintainer on bootstrapping support](https://github.com/microsoft/SEAL/issues/616)
