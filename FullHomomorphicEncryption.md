### Libraries and Tools

### Research
[Full Homomorphic Encryption resources](https://fhe.org/resources/) - tons of FHE resources

[Dark market implementation with FHE](https://www.zama.ai/post/dark-market-tfhe-rs) 

[IBM Research FHE](https://research.ibm.com/topics/fully-homomorphic-encryption) - IBM's comprehensive resource on Fully Homomorphic Encryption, addressing the security gap when processing data. Their implementation provides security and privacy for data at rest, in transit, and during processing. IBM's work builds on Craig Gentry's groundbreaking 2009 research that introduced the first plausible fully homomorphic scheme.

[Homomorphic Encryption at Scale](https://www.fau.edu/engineering/senior-design/projects/spring2024/homomorphic-encryption-at-scale/) - Florida Atlantic University's project exploring advancements in FHE, focusing on overcoming computational inefficiency challenges. Their research team has implemented bootstrapping techniques to reduce noise and incorporated parallel processing to enhance function optimization, particularly for linear regression models.

[CRYPTML](https://www.hes-so.ch/en/recherche-innovation/research-projects/detail-projet-recherche/cryptml-an-hybrid-machine-learning-model-using-homomorphic-encryption) - A hybrid machine learning model using homomorphic encryption developed at HES-SO. This project explores a hybrid client-server architecture enabling machine learning computation on encrypted data, addressing the challenges of preserving privacy in AI applications.


### Libraries and Tools

[google/heir](https://github.com/google/heir) - A compiler for homomorphic encryption from Google, enabling automatic compilation of programs to work on encrypted data

[OpenFHE](https://paperswithcode.com/paper/openfhe-open-source-fully-homomorphic) - A comprehensive open-source FHE software library incorporating design ideas from prior FHE projects like PALISADE, HElib, and HEAAN. OpenFHE includes features like automatic maintenance operations and hardware acceleration support through a standard Hardware Abstraction Layer (HAL).

[TFHE Library by Inpher](https://inpher.io/tfhe-library/) - One of the world's fastest open-source Fully Homomorphic Encryption libraries, maintained by Inpher's team with contributions from leading universities and privacy-first enterprises worldwide. The library implements the scheme described in the best paper from IACR's Asiacrypt 2016 conference.

[TenSEAL](https://sefiks.com/2023/04/10/a-step-by-step-fully-homomorphic-encryption-example-with-tenseal-in-python/) - A practical FHE library for Python that allows performing both addition and multiplication on encrypted data. Unlike partially homomorphic encryption algorithms like RSA, ElGamal, or Paillier, TenSEAL offers fully homomorphic capabilities for real-world applications.

[PostgreSQL Fully Homomorphic Encryption](https://github.com/FHE-Postgres/pg_fhe)

[The Transparent data encryption in PostgreSQL - Highgo Software Inc.](https://www.highgo.ca/2019/09/30/the-transparent-data-encryption-in-postgresql/)

[tfhe-rs](https://github.com/zama-ai/tfhe-rs) - TFHE-rs: A Pure Rust implementation of the TFHE Scheme for Boolean and Integer Arithmetics Over Encrypted Data.

[wgxli/simple-fhe](https://github.com/wgxli/simple-fhe) - A dead-simple library for full homomorphic encryption (FHE) in Python

[hung-ngm/fhe-darkpool](https://github.com/hung-ngm/fhe-darkpool) - Test implementation of dark pool using Full Homomorphic Encryption (FHE)

[FeanorTheElf/fheanor](https://github.com/FeanorTheElf/fheanor) - A modular library for designing and optimising homomorphic encryption schemes

[cipherflow-fhe/latti-ai](https://github.com/cipherflow-fhe/latti-ai) - Framework for performing AI model inference on encrypted data using FHE

[danieleschmidt/homomorphic-llm-proxy](https://github.com/danieleschmidt/homomorphic-llm-proxy) - GPU-accelerated gateway for FHE of LLM inference — process prompts on untrusted cloud infrastructure while maintaining complete privacy

[Lattigo](https://github.com/tuneinsight/lattigo) - Open-source lattice-based homomorphic encryption library in Go, maintained by Tune Insight (originally EPFL)

[OpenFHE](https://github.com/openfheorg/openfhe-development) - Comprehensive open-source FHE library supporting all major schemes (BGV, BFV, CKKS, FHEW, TFHE) with hardware acceleration HAL

[Fhenix Confidential Contracts](https://github.com/FhenixProtocol/fhenix-confidential-contracts) - Solidity smart contracts for confidential ERC-20 tokens using FHE on the Fhenix L2 network

#### FHE Ecosystem Updates
- [Zama $57M Series B](https://x.com/cxmrondlls/status/1978506404400136611) - Zama raised $57M B轮融资,估值超过$1B for FHE blockchain applications
- [Zama Confidential Blockchain Protocol](https://www.zama.org/post/announcing-the-zama-confidential-blockchain-protocol) - Mainnet launch December 2025 for confidential smart contracts on any L1/L2
- [Zama Confidential USDT Transfers](https://www.kucoin.com/news/articles/fhe-in-2026-computing-on-encrypted-data-and-the-projects-making-private-blockchains-a-reality) - First confidential USDT transfers on mainnet
- [ZAMA Token Launch](https://phemex.com/academy/what-is-zama) - ZAMA token launched February 2026 for protocol fees, staking, and operator incentives
- [Mind Network FHE A2A](https://cn.tradingview.com/news/panews:4ada7974fe3f9:0/) - Mind Network联合Zama推出首个基于FHE的A2A隐私解决方案,x402协议
- [Inco Network](https://blockeden.xyz/blog/2026/01/05/zama-protocol/) - Confidentiality-as-a-service using Zama's fhEVM for existing chains
- [FHE for Blockchain Privacy](https://finance.sina.com.cn/blockchain/roll/2025-12-05/doc-infzueru9730390.shtml) - Zama CEO访谈:FHE如何重塑区块链隐私,与ZK和MPC的对比
