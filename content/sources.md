---
title: "Sources"
origin: vault
source: "Sources/Sources.md"
description: "Canonical bibliography for this library: papers, RFCs, standards and notable repositories behind the entries."
updated: 2026-04-28
---

Canonical bibliography for this library — papers, RFCs, books, and notable repositories. Per-section sub-headers anchor the references each topic file's "Primary Sources" pulls from. Cite with the section anchor: `[Sources § Confidential Computing](/sources/)`.

## Standards Bodies & Aggregators

- **IACR ePrint** — [eprint.iacr.org](https://eprint.iacr.org/) — peer-reviewed cryptography preprints.
- **arXiv cs.CR** — [arxiv.org/list/cs.CR/recent](https://arxiv.org/list/cs.CR/recent) — security/crypto preprints.
- **IETF Datatracker** — [datatracker.ietf.org](https://datatracker.ietf.org) — RFCs and drafts.
- **W3C** — [w3.org/TR](https://www.w3.org/TR/) — DIDs, VCs, Web Crypto.
- **NIST CSRC** — [csrc.nist.gov](https://csrc.nist.gov) — FIPS, SP, PQC competition.
- **CCC (Confidential Computing Consortium)** — [confidentialcomputing.io](https://confidentialcomputing.io).
- **Bitcoin BIPs** — [github.com/bitcoin/bips](https://github.com/bitcoin/bips).
- **Lightning BOLTs** — [github.com/lightning/bolts](https://github.com/lightning/bolts).
- **Nostr NIPs** — [github.com/nostr-protocol/nips](https://github.com/nostr-protocol/nips).

## Confidential Computing

Foundational + currently-relevant references for [Overview - Confidential Computing](/kb/confidential-computing/) and the deep-dives.

- McKeen et al., *Innovative Instructions and Software Model for Isolated Execution*, HASP 2013 — original SGX paper.
- Costan & Devadas, *Intel SGX Explained*, IACR 2016/086.
- AMD, *SEV-SNP Whitepaper: Strengthening VM Isolation with Integrity Protection and More*, 2020.
- Cheng et al., *Intel TDX Whitepaper*, 2021.
- ARM, *Confidential Compute Architecture (CCA) Software Stack*, 2022.
- Birrell et al., *Apple Private Cloud Compute*, 2024 (architectural overview).
- RFC 9334, *Remote ATtestation procedureS (RATS) Architecture*, 2023.
- Van Bulck et al., *Foreshadow* (USENIX Security 2018), and subsequent SGX side-channel papers (LVI, ÆPIC Leak, CacheWarp, Hertzbleed).
- NVIDIA, *Confidential Computing on Hopper Architecture*, 2023.
- Confidential Containers (CoCo) project — [github.com/confidential-containers](https://github.com/confidential-containers).

### Implementations

- Gramine — [github.com/gramineproject/gramine](https://github.com/gramineproject/gramine)
- Occlum — [github.com/occlum/occlum](https://github.com/occlum/occlum)
- Constellation (Edgeless) — [github.com/edgelesssys/constellation](https://github.com/edgelesssys/constellation)
- Trustee / KBS — [github.com/confidential-containers/trustee](https://github.com/confidential-containers/trustee)
- Phala TEE Cloud — [github.com/Phala-Network/phala-cloud](https://github.com/Phala-Network/phala-cloud)
- Marlin Oyster — [github.com/marlinprotocol/oyster-monorepo](https://github.com/marlinprotocol/oyster-monorepo)

## Cryptography (FHE / PIR / WoT)

For [Overview - Fully Homomorphic Encryption](/kb/fully-homomorphic-encryption/), [Overview - Private Information Retrieval](/kb/private-information-retrieval/), [Overview - Web of Trust](/kb/web-of-trust/).

### FHE

- Rivest, Adleman, Dertouzos, *On Data Banks and Privacy Homomorphisms*, 1978.
- Gentry, *A Fully Homomorphic Encryption Scheme*, Stanford PhD thesis, 2009.
- Brakerski, Gentry, Vaikuntanathan, *Fully Homomorphic Encryption without Bootstrapping*, ITCS 2012.
- Fan & Vercauteren, *Somewhat Practical Fully Homomorphic Encryption*, IACR 2012/144.
- Cheon et al., *Homomorphic Encryption for Arithmetic of Approximate Numbers* (CKKS), ASIACRYPT 2017.
- Chillotti et al., *Faster Fully Homomorphic Encryption: Bootstrapping in less than 0.1 Seconds* (TFHE), ASIACRYPT 2016.
- OpenFHE — [openfhe.org](https://www.openfhe.org)
- Zama Concrete / fhEVM — [zama.ai](https://www.zama.ai)
- Microsoft SEAL — [github.com/microsoft/SEAL](https://github.com/microsoft/SEAL)

### PIR

- Chor, Goldreich, Kushilevitz, Sudan, *Private Information Retrieval*, JACM 1998.
- Aguilar-Melchor & Gaborit, *Lattice-based PIR* (XPIR), 2015.
- Angel et al., *PIR with Compressed Queries and Amortized Query Processing* / SealPIR, IEEE S&P 2018.
- Mughees, Chen, Ren, *OnionPIR: Response-Efficient Single-Server PIR*, ACM CCS 2021.
- Menon & Wu, *Spiral: Fast, High-Rate Single-Server PIR via FHE Composition*, ePrint 2022/368 / IEEE S&P 2023.
- Davidson, Pestana, Celi et al., *FrodoPIR: Simple, Scalable, Single-Server Private Information Retrieval*, ePrint 2022/981 / PoPETS 2023.
- Henzinger et al., *One Server for the Price of Two: Simple and Fast Single-Server Private Information Retrieval*, ePrint 2022/949 / USENIX Security 2023.
- Li, Micciancio, Raykova, Schultz-Wu, *Hintless Single-Server Private Information Retrieval*, ePrint 2023/1733.
- Menon & Wu, *YPIR: High-Throughput Single-Server PIR with Silent Preprocessing*, USENIX Security 2024.
- Apple, *Swift Homomorphic Encryption* and PIR / PNNS docs — [github.com/apple/swift-homomorphic-encryption](https://github.com/apple/swift-homomorphic-encryption).

### Web of Trust

- Zimmermann, *PGP User's Guide*, 1991.
- Ulrich, Holz, Hauck, Carle, *An Investigation of the OpenPGP Web of Trust*, ESORICS 2011.
- Stiegler, *An Introduction to Petname Systems*, 2005.

## Decentralized DNS

For [Overview - Decentralized DNS](/kb/decentralized-dns/).

- Aiello, Hartshorn et al., *PKARR — Public-Key-Addressable Resource Records over Mainline DHT*, 2023.
- ENS Core Team, *ENS Documentation*, [docs.ens.domains](https://docs.ens.domains).
- Handshake, *handshake.org*, 2018-.
- Schanzenbach et al., *The GNU Name System*, RFC 9498, 2023.
- Maymounkov & Mazières, *Kademlia: A Peer-to-Peer Information System Based on the XOR Metric*, IPTPS 2002.

## Decentralized Compute

For [Overview - Decentralized Compute](/kb/decentralized-compute/).

- Akash Documentation — [akash.network](https://akash.network)
- Phala Network Whitepaper.
- Marlin Protocol — [marlin.org](https://marlin.org)
- Bacalhau — [bacalhau.org](https://bacalhau.org)
- io.net, Render, Aethir public docs.

## Decentralized Storage

For [Overview - Decentralized Storage](/kb/decentralized-storage/) and the 12 deep-dives.

- Benet, *IPFS - Content Addressed, Versioned, P2P File System*, arXiv 2014.
- Protocol Labs, *Filecoin: A Decentralized Storage Network*, 2017.
- IPFS Docs — [docs.ipfs.tech](https://docs.ipfs.tech/)
- Filecoin Docs — [docs.filecoin.io](https://docs.filecoin.io/)
- Williams, *Arweave: A Protocol for Economically Sustainable Information Permanence*, 2018.
- Arweave Docs — [docs.arweave.org](https://docs.arweave.org/)
- Vorick and Champine, *Sia: Simple Decentralized Storage*, 2014.
- Sia Docs — [docs.sia.tech](https://docs.sia.tech/)
- Storj Labs, *Storj: A Decentralized Cloud Storage Network Framework*, 2018.
- Storj Docs — [docs.storj.io](https://docs.storj.io/)
- Swarm Docs — [docs.ethswarm.org](https://docs.ethswarm.org/)
- Bee client — [github.com/ethersphere/bee](https://github.com/ethersphere/bee)
- Blossom BUD specifications — [github.com/hzrd149/blossom](https://github.com/hzrd149/blossom)
- Nostr NIPs — [github.com/nostr-protocol/nips](https://github.com/nostr-protocol/nips)

## Off-Grid / Mesh

For [Overview - Off-Grid Networks](/kb/off-grid-networks/), [Off-Grid Messaging](/kb/off-grid-messaging/), and the deep-dives.

- LoRa Alliance, *LoRaWAN 1.1 Specification*.
- Markqvist, *Reticulum Network Stack Specification* — [reticulum.network/manual](https://reticulum.network/manual)
- Reticulum source — [github.com/markqvist/Reticulum](https://github.com/markqvist/Reticulum)
- LXMF — [github.com/markqvist/LXMF](https://github.com/markqvist/LXMF)
- Meshtastic — [meshtastic.org](https://meshtastic.org); firmware [github.com/meshtastic/firmware](https://github.com/meshtastic/firmware)
- MeshCore — [meshcore.io](https://meshcore.io/); firmware/library [github.com/meshcore-dev/MeshCore](https://github.com/meshcore-dev/MeshCore); flasher + docs on site.
- Yggdrasil Network — [yggdrasil-network.github.io](https://yggdrasil-network.github.io/); source [github.com/yggdrasil-network/yggdrasil-go](https://github.com/yggdrasil-network/yggdrasil-go)
- Briar Project, *Briar Protocol Specification* — [briarproject.org](https://briarproject.org)
- Bitchat — [bitchat.free](https://bitchat.free); source [github.com/permissionlesstech/bitchat](https://github.com/permissionlesstech/bitchat); technical wiki [deepwiki.com/permissionlesstech/bitchat](https://deepwiki.com/permissionlesstech/bitchat).
- FIPS — [github.com/jmcorgan/fips](https://github.com/jmcorgan/fips); public docs [fips.network](https://fips.network); design docs in `docs/design/`.
- Nostr VPN — [github.com/mmalmi/nostr-vpn](https://github.com/mmalmi/nostr-vpn) (mirror); canonical at git.iris.to; builds on FIPS.
- Blackout Comms — [chatters.io](https://www.chatters.io/); comparisons and firmware details on site.
- Noise Protocol Framework — [noiseprotocol.org](https://noiseprotocol.org/)
- IETF DTNRG, *Bundle Protocol*, RFC 5050 / 9171.

## Financial Sovereignty (Bitcoin / Lightning)

For [Overview - Financial Sovereignty](/kb/financial-sovereignty/) and the 06 deep-dives.

### Bitcoin foundations

- Nakamoto, *Bitcoin: A Peer-to-Peer Electronic Cash System*, 2008.
- Antonopoulos, *Mastering Bitcoin*, 3rd ed., O'Reilly 2023.
- BIPs — [github.com/bitcoin/bips](https://github.com/bitcoin/bips), notably BIP-32 (HD), BIP-39 (mnemonics), BIP-174 (PSBT), BIP-340/341/342 (Taproot).

### Lightning

- Poon & Dryja, *The Bitcoin Lightning Network*, 2016. [lightning.network/lightning-network-paper.pdf](https://lightning.network/lightning-network-paper.pdf)
- BOLT specs — [github.com/lightning/bolts](https://github.com/lightning/bolts).
- Riard, *Channel Jamming Attacks*, lightning-dev 2020-.

### Privacy

- Maxwell, *CoinJoin: Bitcoin privacy for the real world*, bitcointalk.org 2013.
- Móczár & Ficsór, *WabiSabi: Centrally Coordinated CoinJoins with Variable Amounts*, IACR 2021/206.
- BIP-78 *Payjoin*.
- Chaum, *Blind Signatures for Untraceable Payments*, 1982/83 (foundational for Cashu ecash).
- Cashu protocol + NIP-60/61 — [github.com/cashubtc](https://github.com/cashubtc), nostr-protocol/nips.
- Fedimint — federated threshold variant.
- TEE Cashu mint research (2026) — public notes from calle (Cashu); attestation patterns cross-ref Confidential Computing sources.

## Encrypted Messaging

For [Overview - Encrypted Messaging](/kb/encrypted-messaging/) and the 07 deep-dives.

- Marlinspike & Perrin, *X3DH Key Agreement*, 2016.
- Perrin & Marlinspike, *Double Ratchet Algorithm*, 2016.
- Kret & Marlinspike, *PQXDH Key Agreement*, 2023.
- Cohn-Gordon et al., *A Formal Security Analysis of the Signal Messaging Protocol*, EuroS&P 2017.
- RFC 9420, *MLS — Messaging Layer Security*, 2023.
- Matrix Specification — [spec.matrix.org](https://spec.matrix.org).
- fiatjaf, *Nostr Protocol*, 2020.
- NIPs registry — [github.com/nostr-protocol/nips](https://github.com/nostr-protocol/nips).
- Marmot Protocol — [github.com/marmot-protocol/marmot](https://github.com/marmot-protocol/marmot) (MIP-00 through MIP-05).
- RFC 9750, *MLS Protocol Architecture*, IETF, 2024.
- OpenMLS — [github.com/openmls/openmls](https://github.com/openmls/openmls).
- mls-rs — [github.com/awslabs/mls-rs](https://github.com/awslabs/mls-rs).
- Cohn-Gordon et al., *On Ends-to-Ends Encryption: Asynchronous Group Messaging with Strong Security Guarantees* (TreeKEM origin), CCS 2018.
- Poberezkin, *SimpleX Messaging Protocol*, 2021.
- van den Hooff et al., *Vuvuzela*, SOSP 2015.
- Angel & Setty, *Pung*, OSDI 2016.

## Mix Networks

For [Overview - Mix Networks](/kb/mix-networks/) and [Mix Networks Friday - Global Passive Adversary Defense and Research Frontier](/kb/global-passive-adversary/).

### Foundational

- Chaum, *Untraceable Electronic Mail, Return Addresses, and Digital Pseudonyms*, CACM 1981.
- Möller et al., *Mixmaster Protocol Version 2*, IETF draft.
- Danezis, Dingledine, Mathewson, *Mixminion: Design of a Type III Anonymous Remailer Protocol*, IEEE S&P 2003.
- Dingledine, Mathewson, Syverson, *Tor: The Second-Generation Onion Router*, USENIX Security 2004.
- Danezis & Goldberg, *Sphinx: A Compact and Provably Secure Mix Format*, IEEE S&P 2009.
- Piotrowska et al., *The Loopix Anonymity System*, USENIX Security 2017.
- Chen et al., *HORNET: High-speed Onion Routing at the Network Layer*, ACM CCS 2015 / arXiv:1507.05724.

### Production implementations

- Nym Technologies — [nymtech.net](https://nymtech.net); whitepaper at [nymtech.net/nym-whitepaper.pdf](https://nymtech.net/nym-whitepaper.pdf).
- Sonnino et al., *Coconut: Threshold Issuance Selective Disclosure Credentials*, NDSS 2019 (zk-nym basis).
- Katzenpost — [katzenpost.network](https://katzenpost.network); source [github.com/katzenpost/katzenpost](https://github.com/katzenpost/katzenpost).
- Katzenpost, *Mixnet Threat Model* — [katzenpost.network/docs/Threat_Model.pdf](https://katzenpost.network/docs/Threat_Model.pdf).
- Katzenpost, *Mixnet Research Literature Overview* — [katzenpost.network/research/Literature_overview__website_version.pdf](https://katzenpost.network/research/Literature_overview__website_version.pdf).
- I2P documentation — [geti2p.net](https://geti2p.net); i2pd — [i2pd.website](https://i2pd.website).
- Tor Project — [torproject.org](https://torproject.org); spec [spec.torproject.org](https://spec.torproject.org); Arti [gitlab.torproject.org/tpo/core/arti](https://gitlab.torproject.org/tpo/core/arti).
- HOPR Association — [hoprnet.org](https://hoprnet.org); yellowpaper at [hoprnet.org/papers](https://hoprnet.org/papers).

### Post-quantum mixnet research

- *CTIDH: Faster Constant-Time CSIDH*, IACR 2021/633 (Katzenpost PQ KEM).
- Rial, Piotrowska et al., *Outfox: A Postquantum Packet Format for Layered Mixnets*, ACM SIGCOMM 2025. [arxiv.org/html/2412.19937](https://arxiv.org/html/2412.19937v2)
- Mahdi Rahimi, *MOCHA: Mixnet Optimization Considering Honest Client Anonymity*, ePrint 2025/861 / IH&MMSEC 2025. [eprint.iacr.org/2025/861](https://eprint.iacr.org/2025/861)
- *Nox: A Sphinx Mixnet for Anonymous Blockchain Transaction Relay*, 2024-2025. [papers.hisoka.io/nox.pdf](https://papers.hisoka.io/nox.pdf)

### Sphinx libraries

- sphinxcrypto (Rust) — [docs.rs/sphinxcrypto](https://docs.rs/sphinxcrypto)
- sphinx-rs (Rust) — [crates.io/crates/sphinx-rs](https://crates.io/crates/sphinx-rs)
- applied-mixnetworks/sphinxmixcrypto (Python) — [github.com/applied-mixnetworks/sphinxmixcrypto](https://github.com/applied-mixnetworks/sphinxmixcrypto)
- google-deepmind/loopix-messaging (experimental) — [github.com/google-deepmind/loopix-messaging](https://github.com/google-deepmind/loopix-messaging)

## Zero-Knowledge

For [Overview - Zero-Knowledge Proofs](/kb/zero-knowledge-proofs/).

- Goldwasser, Micali, Rackoff, *The Knowledge Complexity of Interactive Proof Systems*, SICOMP 1989.
- Groth, *On the Size of Pairing-Based Non-Interactive Arguments* (Groth16), EUROCRYPT 2016.
- Gabizon, Williamson, Ciobotaru, *PLONK*, IACR 2019/953.
- Ben-Sasson et al., *Scalable, transparent, and post-quantum secure computational integrity* (STARKs), 2018.
- Bowe et al., *Halo: Recursive Proof Composition without a Trusted Setup*, 2019.

## Post-Quantum

For [Overview - Post-Quantum Cryptography](/kb/post-quantum-cryptography/).

- NIST PQC project — [csrc.nist.gov/projects/post-quantum-cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography).
- FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA).
- Bernstein et al., *Kyber* and *Dilithium* original submissions.
- Castryck & Decru, *An efficient key recovery attack on SIDH*, EUROCRYPT 2023 (the SIKE break).

## Identity

For [Overview - Decentralized Identity](/kb/decentralized-identity/) and [Overview - Identity & Pseudonymity](/kb/identity-and-pseudonymity/).

- W3C, *DID Core* — [w3.org/TR/did-core](https://www.w3.org/TR/did-core/).
- W3C, *Verifiable Credentials Data Model* — [w3.org/TR/vc-data-model](https://www.w3.org/TR/vc-data-model/).
- IETF SD-JWT — draft-ietf-oauth-selective-disclosure-jwt.
- Decentralized Identity Foundation (DIF) — [identity.foundation](https://identity.foundation).
- ISO 18013-5, *Mobile driving licence (mDL)*.
- Maram et al., *CanDID: Can-Do Decentralized Identity*, IEEE S&P 2021.
- Pubky — [github.com/pubky/pubky](https://github.com/pubky/pubky); pkarr [github.com/pubky/pkarr](https://github.com/pubky/pkarr); pkdns [github.com/pubky/pkdns](https://github.com/pubky/pkdns); docs.pubky.org.
- Komlo & Goldberg, *FROST: Flexible Round-Optimized Schnorr Threshold Signatures*, IACR 2020/852 (multi-party Nostr custody).

## Books

- Schneier, *Applied Cryptography*, 20th-anniversary ed.
- Boneh & Shoup, *A Graduate Course in Applied Cryptography* — [toc.cryptobook.us](https://toc.cryptobook.us/).
- Katz & Lindell, *Introduction to Modern Cryptography*, 3rd ed.
- Antonopoulos, *Mastering Bitcoin*, 3rd ed.
- Antonopoulos & Osuntokun, *Mastering the Lightning Network*, O'Reilly 2021.

## Curated External Indices

- [ungovernable.tech](https://ungovernable.tech) — link directory (the project this library systematizes).
- [awesome-nostr](https://github.com/aljazceru/awesome-nostr).
- [awesome-meshtastic](https://github.com/ajmcquilkin/awesome-meshtastic).
- [awesome-zk](https://github.com/ventali/awesome-zk).
- [awesome-bitcoin](https://github.com/igorbarinov/awesome-bitcoin).

## Primary sources

- [MOCHA: ePrint 2025/861](https://eprint.iacr.org/2025/861)
