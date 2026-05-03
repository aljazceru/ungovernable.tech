#### Signal Protocol
- [Signal Protocol](https://signal.org/docs/) - Open protocol providing end-to-end encryption with forward secrecy and post-compromise security
- [libsignal](https://github.com/signalapp/libsignal) - Official Signal Protocol library (Java, C, Rust)
- [Double Ratchet Specification](https://signal.org/docs/specifications/doubleratchet/) - Signal's core key derivation and message encryption algorithm
- [X3DH Key Agreement](https://signal.org/docs/specifications/x3dh/) - Extended Triple Diffie-Hellman for establishing shared secrets
- [x3dh-ratchet](https://github.com/ekkolon/x3dh-ratchet) - Crypto primitives based on the Signal Protocol for secure async messaging
- [2key-ratchet](https://github.com/PeculiarVentures/2key-ratchet) - Double Ratchet and X3DH implementation in JavaScript
- [Signal SPQR Post-Quantum Ratchet](https://csrc.nist.gov/csrc/media/events/2025/sixth-pqc-standardization-conference/post-quantum%20ratcheting%20for%20signal.pdf) - Sparse Post-Quantum Ratchet (SPQR) integrating ML-KEM (2025)

#### Matrix Protocol
- [Matrix.org](https://matrix.org/) - Open protocol for decentralized, federated real-time communication
- [Olm](https://gitlab.matrix.org/matrix-org/olm) - Double Ratchet implementation for 1:1 Matrix encryption
- [Megolm](https://gitlab.matrix.org/matrix-org/olm/blob/master/docs/megolm.md) - Sender-key ratchet for efficient group encryption in Matrix
- [Matrix E2EE Implementation Guide](https://matrix.org/docs/matrix-concepts/end-to-end-encryption/) - Official guide to Matrix's end-to-end encryption architecture
- [Element](https://element.io/) - Flagship Matrix client for web, desktop, and mobile

#### Messaging Layer Security (MLS)
- [RFC 9420: MLS Protocol](https://www.rfc-editor.org/rfc/rfc9420) - IETF standard for efficient group end-to-end encryption
- [MLS Architecture](https://messaginglayersecurity.rocks/mls-architecture/) - Architecture document for MLS deployment
- [TreeKEM](https://eprint.iacr.org/2025/229.pdf) - External-Operations TreeKEM and the security of MLS in RFC 9420
- [MLS RFC Overview](https://blog.phnx.im/rfc-9420-mls/) - Detailed walkthrough of RFC 9420 design and security properties

#### Metadata-Resistant Messaging
- [SimpleX Chat](https://github.com/simplex-chat/simplex-chat) - First messaging network operating without user identifiers of any kind
- [SimpleX Messaging Protocol](https://github.com/simplex-chat/simplexmq/blob/stable/protocol/simplex-messaging.md) - Transport-agnostic protocol for distributed secure unidirectional messaging
- [SimpleX v6.4.1](https://simplex.chat/blog/) - July 2025 release with contact management and group protection features
- [SimpleX Security Audit](https://simplex.chat/blog/20241014-simplex-network-v6-1-security-review-better-calls-user-experience.html) - Trail of Bits cryptographic design review for v6.1
- [Cwtch](https://docs.cwtch.im/) - Decentralized, metadata-resistant messaging over Tor v3 onion services
- [Briar](https://briarproject.org/) - Peer-to-peer encrypted messaging via Tor, Bluetooth, and WiFi
- [Briar Desktop 0.6.0-beta](https://briarproject.org/news/2023-briar-desktop-0.6.0-released/) - Beta desktop client adding blogs support to secure P2P messaging
- [Briar 1.5.17](https://code.briarproject.org/briar/briar/-/tree/release-1.5.17) - March 2026 Android release with improved connectivity
- [Session Desktop](https://github.com/session-foundation/session-desktop) - Decentralized onion-routed messenger using service nodes for offline storage and IP protection

#### Modern Encryption Tools
- [age](https://github.com/FiloSottile/age) - Simple, modern file encryption tool (Go) — a GPG replacement
- [minisign](https://github.com/jedisct1/minisign) - Minimalistic tool for signing files and verifying signatures
- [OpenPGP.js](https://github.com/openpgpjs/openpgpjs) - OpenPGP implementation in JavaScript (maintained by Proton Mail)
- [Sequoia PGP](https://sequoia-pgp.org/) - Modern OpenPGP implementation in Rust
- [Gopenpgp](https://github.com/ProtonMail/gopenpgp) - Go wrapper around GPG for high-performance OpenPGP operations

#### Privacy Infrastructure
- [Oblivious HTTP (OHTTP)](https://en.wikipedia.org/wiki/Oblivious_HTTP) - IETF protocol for anonymous HTTP transactions via relay
- [Oblivious DoH (ODoH)](https://blog.cloudflare.com/oblivious-dns/) - DNS resolution via oblivious relay to hide client identity from resolver
- [RFC 9458: OHTTP](https://www.rfc-editor.org/rfc/rfc9458) - IETF standard for Oblivious HTTP
