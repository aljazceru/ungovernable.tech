# Batch 1 factual audit — 25 October 2026

All corrected facts below were checked against primary-source bodies fetched with curl. Every linked source below returned HTTP 200 using the required redirect-following command and Firefox user agent. This is a repository audit record, not site content.

## Implementation

- `scripts/import_vault.py` loads `content/vault_fixes.yml`, keyed by entry slug. It validates records, applies exact replacements to generated bodies/deks/descriptions, replaces or appends source sections, and supports an updated date. Stale replacements and invalid targets fail before writing. Existing append, related and glossary hooks remain active.
- `content/vault_aux_fixes.yml` applies the same strict corrections to generated briefings and the bibliography. This keeps repeated errors fixed without editing the read-only vault.
- `tests/test_vault_fixes.py` checks source-section handling, metadata replacements, stale/missing/original targets, preservation of existing hooks and original entries, and full import idempotence against the source vault. `README.md` documents the format.
- Directory changes are in `content/directory/overrides.yml`; `money.yml` is regenerated. Original entries are edited directly. Every changed entry has `updated: 2026-10-25`.

## Verified facts and affected entries

### Mutiny

Removed Mutiny from current wallet recommendations and marked its directory listing discontinued as a hosted wallet; the shutdown notice points remaining users to self-hosting.

Entry files: `content/entries/lightning-network.md`, `content/entries/hardware-wallets.md`.

- [Mutiny Wallet shutdown announcement](https://blog.mutinywallet.com/mutiny-wallet-is-shutting-down/) — HTTP 200.

### Taproot

P2TR publishes the tweaked public key at output creation, including for key-path spending. Removed it from hash-protected address categories and dropped an unsupported exposure percentage.

Entry files: `content/entries/bitcoin-post-quantum-migration.md`.

- [BIP 341: Taproot output keys and key-path validation](https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki) — HTTP 200.

### Cashu

NUT-00 specifies BDHKE on secp256k1, not RSA.

Entry files: `content/entries/cashu-ecash.md`.

- [Cashu NUT-00: BDHKE on secp256k1](https://github.com/cashubtc/nuts/blob/main/00.md) — HTTP 200.

### Handshake

hsd proof of work combines BLAKE2b and SHA3. Names require renewal through the RENEW covenant; mainnet expiry uses (2 × 365) × blocksPerDay after renewal, approximately two years. Corrected both renewal comparison tables.

Entry files: `content/entries/handshake.md`, `content/entries/pkarr.md`, `content/entries/namecoin.md`, `content/entries/decentralized-dns.md`, `content/entries/unstoppable-domains.md`.

- [hsd block-header proof-of-work hash](https://github.com/handshake-org/hsd/blob/master/lib/primitives/abstractblock.js) — HTTP 200.
- [hsd mainnet name-renewal window](https://github.com/handshake-org/hsd/blob/master/lib/protocol/networks.js) — HTTP 200.
- [hsd name-expiry rule](https://github.com/handshake-org/hsd/blob/master/lib/covenants/namestate.js) — HTTP 200.
- [hsd RENEW covenant validation](https://github.com/handshake-org/hsd/blob/master/lib/blockchain/chain.js) — HTTP 200.

### Onion encoding

The v3 checksum is the first two bytes of SHA3-256 over the checksum prefix, public key and version. The address encodes the public key, checksum and version; it is not a hash of the public key.

Entry files: `content/entries/onion-and-i2p-naming.md`, `content/entries/cwtch.md`.

- [Tor specification: encoding v3 onion addresses](https://spec.torproject.org/rend-spec/encoding-onion-addresses.html) — HTTP 200.

### Briar

Maintenance mode was announced on 9 July 2026: essential security updates and bug fixes continue. Account backup and file attachments remain missing; the manual supplies no account recovery after uninstalling or losing the password. The cited desktop release is beta, not stable.

Entry files: `content/entries/briar.md`, `content/entries/cwtch.md`, `content/entries/off-grid-networks.md`.

- [Briar maintenance-mode announcement, 9 July 2026](https://briarproject.org/news/2026-maintenance-mode/) — HTTP 200.
- [Briar manual: account storage and recovery](https://briarproject.org/manual/) — HTTP 200.
- [Briar Desktop beta release announcement](https://briarproject.org/news/2023-briar-desktop-0.6.0-released/) — HTTP 200.

### Cwtch

The official supported-platform and download lists include Android and desktop platforms, without an iOS client.

Entry files: `content/entries/cwtch.md`.

- [Cwtch supported platforms](https://docs.cwtch.im/docs/getting-started/supported_platforms) — HTTP 200.
- [Tor v3 onion-address encoding](https://spec.torproject.org/rend-spec/encoding-onion-addresses.html) — HTTP 200.
- [Briar maintenance-mode announcement](https://briarproject.org/news/2026-maintenance-mode/) — HTTP 200.
- [Cwtch downloads for Android and desktop](https://cwtch.im/download/) — HTTP 200.

### Nostr custody

Amber is a local Android signer keeping keys in a dedicated app. NIP-26 is unrecommended. NIP-46 remote signing does not depend on NIP-26 delegation. Removed delegation recommendations and misleading custody comparisons.

Entry files: `content/entries/nostr-identity.md`, `content/entries/nostr-protocol.md`, `content/entries/nostr-key-custody.md`, `content/entries/identity-and-pseudonymity.md`, `content/entries/web-of-trust-survey.md`, `content/entries/nostr-web-of-trust.md`, `content/entries/at-protocol.md`.

- [Amber: local Android signer](https://github.com/greenart7c3/Amber) — HTTP 200.
- [NIP-55: Android signer interface](https://github.com/nostr-protocol/nips/blob/master/55.md) — HTTP 200.
- [NIP-46: remote signing](https://github.com/nostr-protocol/nips/blob/master/46.md) — HTTP 200.
- [NIPs README: NIP-26 status](https://github.com/nostr-protocol/nips) — HTTP 200.

### DVM status

The NIPs README marks NIP-90 unrecommended and prefers use-case-specific microstandards; the research note and overview now state that status.

Entry files: `content/entries/confidential-dvm.md`, `content/entries/ai-agent-identity-nostr.md`.

- [NIPs README: NIP-90 status](https://github.com/nostr-protocol/nips) — HTTP 200.

### OpenSSH and age

OpenSSH added mlkem768x25519-sha256 in 9.9 and made it the default in 10.0 (April 2025); explicit configuration examples include it. age 1.3.0 added native hybrid ML-KEM-768 recipients, generated with age-keygen -pq, with a compatibility plugin for older clients.

Entry files: `content/entries/hybrid-kem-migration.md`, `content/entries/age-encryption.md`, `content/entries/ml-kem.md`, `content/entries/pqc-deployment-tracker.md`, `content/entries/post-quantum-cryptography.md`.

- [OpenSSH post-quantum cryptography](https://www.openssh.com/pq.html) — HTTP 200.
- [age v1.3.0 release: native hybrid post-quantum recipients](https://github.com/FiloSottile/age/releases/tag/v1.3.0) — HTTP 200.

### Semaphore v4

Identities contain an EdDSA private key, public key and Poseidon commitment to the public key. Proofs use the derived secret scalar, public scope and nullifier. The reference uses Circom/Groth16; artifact depth can follow the actual Merkle path.

Entry files: `content/entries/semaphore.md`.

- [Semaphore v4 identities](https://docs.semaphore.pse.dev/guides/identities) — HTTP 200.
- [Semaphore v4 circuit inputs and outputs](https://docs.semaphore.pse.dev/technical-reference/circuits) — HTTP 200.
- [Semaphore reference proof generation](https://github.com/semaphore-protocol/semaphore/blob/main/packages/proof/src/generate-proof.ts) — HTTP 200.
- [Semaphore v4 identity commitment implementation](https://github.com/semaphore-protocol/semaphore/blob/main/packages/identity/src/index.ts) — HTTP 200.
- [Semaphore v4 Circom circuit](https://github.com/semaphore-protocol/semaphore/blob/main/packages/circuits/src/semaphore.circom) — HTTP 200.

### SimpleX groups

Groups are client-defined profiles and sets of pairwise connections. The protocol describes introductions and temporary forwarding, not relay-owned group membership or a shared sender-key group.

Entry files: `content/entries/simplex.md`.

- [SimpleX Chat protocol: decentralized group design](https://simplex.chat/docs/protocol/simplex-chat.html) — HTTP 200.

### US radio rules

GMRS §95.1733(a)(3) prohibits coded/hidden-meaning messages, except 10 codes. FRS §95.533 restricts one-way communications. MURS §95.2733 prohibits repeaters/signal boosters including store-and-forward packet operation. The latter sections do not establish blanket encryption permission.

Entry files: `content/entries/hf-data-modes.md`.

- [47 CFR 95.1733: prohibited GMRS uses](https://www.ecfr.gov/current/title-47/chapter-I/subchapter-D/part-95/subpart-E/section-95.1733) — HTTP 200.
- [47 CFR 95.533: prohibited FRS uses](https://www.ecfr.gov/current/title-47/chapter-I/subchapter-D/part-95/subpart-B/section-95.533) — HTTP 200.
- [47 CFR 95.2733: prohibited MURS uses](https://www.ecfr.gov/current/title-47/chapter-I/subchapter-D/part-95/subpart-J/section-95.2733) — HTTP 200.

### ENS

The Surge proposal is dated 17 November 2025. ENS announced on 6 February 2026 that ENSv2 would remain exclusively on Ethereum L1 and Namechain development would cease. Removed the unsupported August–September revival narrative.

Entry files: `content/entries/ens.md`.

- [ENS is staying on Ethereum, 6 February 2026](https://ens.domains/blog/post/ens-staying-on-ethereum) — HTTP 200.
- [Earlier Namechain/Surge proposal, 17 November 2025](https://ens.domains/blog/post/namechain-nethermind-surge) — HTTP 200.

### Tor Browser

Removed hard current-version recommendations from maintained references and linked the official platform download page. Historical release references in dated briefings are not treated as the current version.

Entry files: `content/entries/tor.md`, `content/entries/mix-networks.md`, `content/entries/mix-networks-tracker.md`.

- [Tor Browser downloads](https://www.torproject.org/download/) — HTTP 200.

### Google migration date

Google’s 25 March 2026 post sets a 2029 PQC migration target, with authentication a priority. It does not date Q-Day, provide the attributed qubit count, or establish a three-year decryption countdown.

Entry files: `content/entries/post-quantum-cryptography.md`.

- [Google: Quantum frontiers may be closer than they appear, 25 March 2026](https://blog.google/innovation-and-ai/technology/safety-security/cryptography-migration-timeline/) — HTTP 200.
- [OpenSSH post-quantum defaults](https://www.openssh.com/pq.html) — HTTP 200.

### Readiness

Yggdrasil calls itself experimental and alpha-stage. GNUnet describes its software as early alpha. Retained experimental frontmatter ratings and corrected conflicting production/stable descriptions and tables, including briefings.

Entry files: `content/entries/off-grid-networks.md`, `content/entries/yggdrasil.md`, `content/entries/mesh-naming.md`, `content/entries/fips-mesh.md`, `content/entries/gnu-name-system.md`, `content/entries/decentralized-dns.md`.

- [Yggdrasil project status](https://yggdrasil-network.github.io/) — HTTP 200.
- [GNUnet: early-alpha software status](https://www.gnunet.org/en/about.html) — HTTP 200.

### SimplePIR

The paper uses LWE dimension n = 1024. Removed the unverified n = 22 / d = 2048 optimum claim.

Entry files: `content/entries/simplepir-doublepir.md`.

- [Henzinger et al.: One Server for the Price of Two, USENIX Security 2023](https://www.usenix.org/system/files/usenixsecurity23-henzinger.pdf) — HTTP 200.

### Marlin Oyster

The CVM payment token is USDC. Operators stake the token defined as POND on Arbitrum One or through Symbiotic vaults on Ethereum. Removed every OAT token reference.

Entry files: `content/entries/marlin-oyster.md`.

- [Oyster CVM definitions: payment token and staking token](https://docs.marlin.org/oyster/protocol/cvm/definitions) — HTTP 200.
- [Oyster CVM actors and operator staking](https://docs.marlin.org/oyster/protocol/cvm/actors) — HTTP 200.

### Apple PIR

Apple publishes the Swift HE/PIR library and a functional PIR service example. Their code is available for inspection; the example explicitly is not for production. This does not establish publication of every deployed component.

Entry files: `content/entries/pir-use-cases.md`.

- [Apple Swift Homomorphic Encryption, including PIR](https://github.com/apple/swift-homomorphic-encryption) — HTTP 200.
- [Apple PIR Service Example and deployment limits](https://github.com/apple/pir-service-example) — HTTP 200.

### MOCHA

Corrected the paper identifier to ePrint 2025/861 and the listed author to Mahdi Rahimi, including repeated briefings and the bibliography.

Entry files: `content/entries/loopix.md`, `content/entries/mix-networks-tracker.md`, `content/entries/global-passive-adversary.md`.

- [MOCHA: ePrint 2025/861](https://eprint.iacr.org/2025/861) — HTTP 200.

### NIP-59

The outer gift-wrap p tag identifies the recipient. Sender and content encryption do not hide recipient and timing metadata from an observer who can see the outer event.

Entry files: `content/entries/marmot-protocol.md`, `content/entries/white-noise.md`, `content/entries/nostr-protocol.md`.

- [NIP-59: visible recipient tags](https://github.com/nostr-protocol/nips/blob/master/59.md) — HTTP 200.

### GPU confidentiality

Hopper HBM is unencrypted and protected by isolation/access controls. CPU–GPU data uses encrypted bounce buffers. Hopper PPCIe leaves NVLink unencrypted; Blackwell multi-GPU CC encrypts NVLink. Removed blanket HBM-encryption claims from related entries.

Entry files: `content/entries/nvidia-gpu-tee.md`, `content/entries/phala-and-0g.md`, `content/entries/private-llm-inference-patterns.md`.

- [NVIDIA H100 confidential computing: bounce buffers and unencrypted HBM](https://developer.nvidia.com/blog/confidential-computing-on-h100-gpus-for-secure-and-trustworthy-ai/) — HTTP 200.
- [NVIDIA confidential VM threat model and interconnect limits](https://docs.nvidia.com/confidential-computing/virtual-machines/threat-model) — HTTP 200.
- [NVIDIA Hopper and Blackwell confidential-computing whitepaper](https://docs.nvidia.com/nvidia-secure-ai-with-blackwell-and-hopper-gpus-whitepaper.pdf) — HTTP 200.

### Sideband

Official platform lists cover Android, Linux, macOS and Windows, without an iOS app.

Entry files: `content/entries/reticulum.md`.

- [Sideband README and supported platforms](https://github.com/markqvist/Sideband) — HTTP 200.
- [Official Sideband site](https://unsigned.io/sideband/) — HTTP 200.

## Not confirmed; omitted

- Blanket encryption permission for FRS/MURS from the cited sections.
- A 2026 Namechain revival based on the November 2025 Surge post.
- The qubit count and Q-Day date previously attributed to Google’s migration announcement.
- SimplePIR’s alleged optimum at d = 2048.
- A blanket claim that GPU HBM is encrypted across Hopper and Blackwell; the stated protections are specific to architecture, mode and path.
- Stable Briar Desktop, recoverable Briar account backups, Cwtch/Sideband iOS apps, and OAT as a Marlin asset were removed in favor of the confirmed official descriptions.
- The ePrint PDF fetch for SimplePIR failed; the USENIX publisher PDF was fetched successfully and confirms n = 1024. No failed link was added.

## Added URL audit

Each URL newly introduced into an edited Markdown document is listed here, including URLs already used elsewhere on the site. The fixture URL is not site content.

| URL | HTTP code |
|---|---|
| [blog.google/innovation-and-ai/technology/safety-security/cryptography-migration-timeline/](https://blog.google/innovation-and-ai/technology/safety-security/cryptography-migration-timeline/) | 200 |
| [blog.mutinywallet.com/mutiny-wallet-is-shutting-down/](https://blog.mutinywallet.com/mutiny-wallet-is-shutting-down/) | 200 |
| [briarproject.org/manual/](https://briarproject.org/manual/) | 200 |
| [briarproject.org/news/2023-briar-desktop-0.6.0-released/](https://briarproject.org/news/2023-briar-desktop-0.6.0-released/) | 200 |
| [briarproject.org/news/2026-maintenance-mode/](https://briarproject.org/news/2026-maintenance-mode/) | 200 |
| [cwtch.im/download/](https://cwtch.im/download/) | 200 |
| [developer.nvidia.com/blog/confidential-computing-on-h100-gpus-for-secure-and-trustworthy-ai/](https://developer.nvidia.com/blog/confidential-computing-on-h100-gpus-for-secure-and-trustworthy-ai/) | 200 |
| [docs.cwtch.im/docs/getting-started/supported_platforms](https://docs.cwtch.im/docs/getting-started/supported_platforms) | 200 |
| [docs.marlin.org/oyster/protocol/cvm/actors](https://docs.marlin.org/oyster/protocol/cvm/actors) | 200 |
| [docs.marlin.org/oyster/protocol/cvm/definitions](https://docs.marlin.org/oyster/protocol/cvm/definitions) | 200 |
| [docs.nvidia.com/confidential-computing/virtual-machines/threat-model](https://docs.nvidia.com/confidential-computing/virtual-machines/threat-model) | 200 |
| [docs.nvidia.com/nvidia-secure-ai-with-blackwell-and-hopper-gpus-whitepaper.pdf](https://docs.nvidia.com/nvidia-secure-ai-with-blackwell-and-hopper-gpus-whitepaper.pdf) | 200 |
| [docs.semaphore.pse.dev/guides/identities](https://docs.semaphore.pse.dev/guides/identities) | 200 |
| [docs.semaphore.pse.dev/technical-reference/circuits](https://docs.semaphore.pse.dev/technical-reference/circuits) | 200 |
| [ens.domains/blog/post/ens-staying-on-ethereum](https://ens.domains/blog/post/ens-staying-on-ethereum) | 200 |
| [ens.domains/blog/post/namechain-nethermind-surge](https://ens.domains/blog/post/namechain-nethermind-surge) | 200 |
| [eprint.iacr.org/2025/861](https://eprint.iacr.org/2025/861) | 200 |
| [example.org/](https://example.org/) | 200 |
| [github.com/FiloSottile/age/releases/tag/v1.3.0](https://github.com/FiloSottile/age/releases/tag/v1.3.0) | 200 |
| [github.com/apple/pir-service-example](https://github.com/apple/pir-service-example) | 200 |
| [github.com/apple/swift-homomorphic-encryption](https://github.com/apple/swift-homomorphic-encryption) | 200 |
| [github.com/bitcoin/bips/blob/master/bip-0341.mediawiki](https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki) | 200 |
| [github.com/cashubtc/nuts/blob/main/00.md](https://github.com/cashubtc/nuts/blob/main/00.md) | 200 |
| [github.com/greenart7c3/Amber](https://github.com/greenart7c3/Amber) | 200 |
| [github.com/handshake-org/hsd/blob/master/lib/blockchain/chain.js](https://github.com/handshake-org/hsd/blob/master/lib/blockchain/chain.js) | 200 |
| [github.com/handshake-org/hsd/blob/master/lib/covenants/namestate.js](https://github.com/handshake-org/hsd/blob/master/lib/covenants/namestate.js) | 200 |
| [github.com/handshake-org/hsd/blob/master/lib/primitives/abstractblock.js](https://github.com/handshake-org/hsd/blob/master/lib/primitives/abstractblock.js) | 200 |
| [github.com/handshake-org/hsd/blob/master/lib/protocol/networks.js](https://github.com/handshake-org/hsd/blob/master/lib/protocol/networks.js) | 200 |
| [github.com/markqvist/Sideband](https://github.com/markqvist/Sideband) | 200 |
| [github.com/nostr-protocol/nips](https://github.com/nostr-protocol/nips) | 200 |
| [github.com/nostr-protocol/nips/blob/master/46.md](https://github.com/nostr-protocol/nips/blob/master/46.md) | 200 |
| [github.com/nostr-protocol/nips/blob/master/55.md](https://github.com/nostr-protocol/nips/blob/master/55.md) | 200 |
| [github.com/nostr-protocol/nips/blob/master/59.md](https://github.com/nostr-protocol/nips/blob/master/59.md) | 200 |
| [github.com/nostr-protocol/nips/blob/master/90.md](https://github.com/nostr-protocol/nips/blob/master/90.md) | 200 |
| [github.com/semaphore-protocol/semaphore/blob/main/packages/circuits/src/semaphore.circom](https://github.com/semaphore-protocol/semaphore/blob/main/packages/circuits/src/semaphore.circom) | 200 |
| [github.com/semaphore-protocol/semaphore/blob/main/packages/identity/src/index.ts](https://github.com/semaphore-protocol/semaphore/blob/main/packages/identity/src/index.ts) | 200 |
| [github.com/semaphore-protocol/semaphore/blob/main/packages/proof/src/generate-proof.ts](https://github.com/semaphore-protocol/semaphore/blob/main/packages/proof/src/generate-proof.ts) | 200 |
| [simplex.chat/docs/protocol/simplex-chat.html](https://simplex.chat/docs/protocol/simplex-chat.html) | 200 |
| [spec.torproject.org/rend-spec/encoding-onion-addresses.html](https://spec.torproject.org/rend-spec/encoding-onion-addresses.html) | 200 |
| [unsigned.io/sideband/](https://unsigned.io/sideband/) | 200 |
| [www.ecfr.gov/current/title-47/chapter-I/subchapter-D/part-95/subpart-B/section-95.533](https://www.ecfr.gov/current/title-47/chapter-I/subchapter-D/part-95/subpart-B/section-95.533) | 200 |
| [www.ecfr.gov/current/title-47/chapter-I/subchapter-D/part-95/subpart-E/section-95.1733](https://www.ecfr.gov/current/title-47/chapter-I/subchapter-D/part-95/subpart-E/section-95.1733) | 200 |
| [www.ecfr.gov/current/title-47/chapter-I/subchapter-D/part-95/subpart-J/section-95.2733](https://www.ecfr.gov/current/title-47/chapter-I/subchapter-D/part-95/subpart-J/section-95.2733) | 200 |
| [www.gnunet.org/en/about.html](https://www.gnunet.org/en/about.html) | 200 |
| [www.openssh.com/pq.html](https://www.openssh.com/pq.html) | 200 |
| [www.torproject.org/download/](https://www.torproject.org/download/) | 200 |
| [www.usenix.org/system/files/usenixsecurity23-henzinger.pdf](https://www.usenix.org/system/files/usenixsecurity23-henzinger.pdf) | 200 |
| [yggdrasil-network.github.io/](https://yggdrasil-network.github.io/) | 200 |

## Files changed

- `README.md`
- `content/briefings/identity/2026-09-20.md`
- `content/briefings/mix-networks/2026-06-19.md`
- `content/briefings/mix-networks/2026-09-04.md`
- `content/briefings/mix-networks/2026-09-11.md`
- `content/briefings/mix-networks/2026-09-18.md`
- `content/briefings/mix-networks/2026-09-25.md`
- `content/briefings/naming/2026-07-27.md`
- `content/briefings/naming/2026-08-03.md`
- `content/briefings/naming/2026-08-10.md`
- `content/briefings/naming/2026-08-31.md`
- `content/briefings/naming/2026-09-07.md`
- `content/briefings/naming/2026-09-14.md`
- `content/briefings/naming/2026-09-21.md`
- `content/briefings/naming/2026-09-28.md`
- `content/briefings/naming/2026-10-05.md`
- `content/briefings/post-quantum/2026-07-18.md`
- `content/briefings/post-quantum/2026-08-01.md`
- `content/briefings/post-quantum/2026-10-03.md`
- `content/directory/money.yml`
- `content/directory/overrides.yml`
- `content/entries/age-encryption.md`
- `content/entries/ai-agent-identity-nostr.md`
- `content/entries/at-protocol.md`
- `content/entries/bitcoin-post-quantum-migration.md`
- `content/entries/briar.md`
- `content/entries/cashu-ecash.md`
- `content/entries/confidential-dvm.md`
- `content/entries/cwtch.md`
- `content/entries/decentralized-dns.md`
- `content/entries/ens.md`
- `content/entries/fips-mesh.md`
- `content/entries/global-passive-adversary.md`
- `content/entries/gnu-name-system.md`
- `content/entries/handshake.md`
- `content/entries/hardware-wallets.md`
- `content/entries/hf-data-modes.md`
- `content/entries/hybrid-kem-migration.md`
- `content/entries/identity-and-pseudonymity.md`
- `content/entries/lightning-network.md`
- `content/entries/loopix.md`
- `content/entries/marlin-oyster.md`
- `content/entries/marmot-protocol.md`
- `content/entries/mesh-naming.md`
- `content/entries/mix-networks-tracker.md`
- `content/entries/mix-networks.md`
- `content/entries/ml-kem.md`
- `content/entries/namecoin.md`
- `content/entries/nostr-identity.md`
- `content/entries/nostr-key-custody.md`
- `content/entries/nostr-protocol.md`
- `content/entries/nostr-web-of-trust.md`
- `content/entries/nvidia-gpu-tee.md`
- `content/entries/off-grid-networks.md`
- `content/entries/onion-and-i2p-naming.md`
- `content/entries/phala-and-0g.md`
- `content/entries/pir-use-cases.md`
- `content/entries/pkarr.md`
- `content/entries/post-quantum-cryptography.md`
- `content/entries/pqc-deployment-tracker.md`
- `content/entries/private-llm-inference-patterns.md`
- `content/entries/reticulum.md`
- `content/entries/semaphore.md`
- `content/entries/simplepir-doublepir.md`
- `content/entries/simplex.md`
- `content/entries/tor.md`
- `content/entries/unstoppable-domains.md`
- `content/entries/web-of-trust-survey.md`
- `content/entries/white-noise.md`
- `content/entries/yggdrasil.md`
- `content/sources.md`
- `content/vault_aux_fixes.yml`
- `content/vault_fixes.yml`
- `scripts/FACT_CHECK_BATCH1.md`
- `scripts/IMPORT_REPORT.md`
- `scripts/import_vault.py`
- `tests/test_vault_fixes.py`

## Validation

The required import → directory import → build → site_check → pytest sequence passed after the final corrections. `site_check` checked 355 pages and reported **0 problems**; **21 pytest tests passed**. The additional importer run changed none of the 379 tracked/untracked file hashes, and `git status --short` was identical before and after it. All 49 changed entries have descriptions of 110–160 characters ending in a full stop, the requested update date, and valid related slugs; technology entries retain readiness ratings. All 43 newly introduced external URLs in site Markdown returned HTTP 200. No commit, push or deployment was performed.
