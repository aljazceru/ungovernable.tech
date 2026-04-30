#### Tor Network
- [Tor Project](https://www.torproject.org/) - Free software and decentralized network for anonymous communication
- [Tor Browser](https://www.torproject.org/download/) - Hardened Firefox browser configured for Tor
- [Onion Services](https://community.torproject.org/onion-services/) - Hidden services accessible only within the Tor network
- [Tor Pluggable Transports](https://tb-manual.torproject.org/circumvention/) - Censorship circumvention via obfs4, snowflake, and meek bridges
- [Snowflake](https://snowflake.torproject.org/) - WebRTC-based pluggable transport for Tor censorship resistance
- [Snowflake 2.0](https://ubos.tech/news/tors-2025-anti%E2%80%91censorship-strategies-lessons-from-iran-and-russia/) - Major 2025 update with improved obfuscation and scalability for high-censorship regions
- [WebTunnel](https://gitlab.torproject.org/tpo/anti-censorship/pluggable-transports/webtunnel) - HTTP-based obfuscation transport simulating regular HTTPS traffic
- [Conjure](https://github.com/net4people/bbs/issues/124) - New pre-alpha pluggable transport available in Tor Browser nightlies
- [Tor2web](https://tor2web.org/) - Access .onion services from a regular browser (trade-off: no anonymity)
- [Onion-Location](https://community.torproject.org/onion-services/onion-location/) - HTTP header for revealing .onion sites via regular browsers
- [Tor Network Documentation](https://tb-manual.torproject.org/) - Comprehensive manual for using Tor effectively
- [Tor Browser: Unblocking Tor](https://support.torproject.org/tor-browser/circumvention/unblocking-tor/) - Official guide to obfs4, meek, Snowflake, WebTunnel, bridges, and Lyrebird
- [Tor daemon bridge setup](https://support.torproject.org/little-t-tor/circumvention/using-bridges/) - torrc examples for obfs4, Snowflake, and WebTunnel pluggable transports

#### I2P (Invisible Internet Project)
- [I2P](https://geti2p.net/) - Fully decentralized, self-organizing overlay network for anonymous communication
- [i2p.i2p GitHub](https://github.com/i2p/i2p.i2p) - I2P Java implementation
- [I2Pd](https://github.com/PurpleI2P/i2pd) - Lightweight C++ implementation of I2P client
- [I2P Botnet](https://i2pbot.net/) - Community resources and services on I2P
- [I2P 2.11.0 Release](https://i2p.net/) - Latest release with improved NTCP2 resistance to probing attacks
- [I2P 2.9.0 Release](https://i2p.net/en/blog/2025/06/02/i2p-2.9.0-release/) - June 2025 release with thread and performance improvements

#### Mix Networks
- [Nym](https://nym.com/) - Decentralized noise-generating mixnet providing network-level anonymity
- [Nym GitHub](https://github.com/nymtech/nym) - Rust monorepo for Nym nodes, gateways, clients, SDKs, wallet, explorer, and network services
- [NymVPN](https://github.com/nymtech/nym-vpn-client) - Cross-platform VPN application leveraging Nym's 5-hop mixnet for traffic privacy
- [NymVPN v2026.7](https://nym.com/blog/nymvpn.v2026.7) - Split tunneling (beta), post-quantum Lewes protocol, improved macOS authentication (April 2026)
- [NymVPN vs VPNs vs Tor vs I2P vs dVPNs](https://nym.com/blog/nymvpn-v-vpns-v-tor-v-i2p-v-dvpns) - Detailed comparison of anonymity solutions
- [Nym NEAR Integration](https://www.theblock.co/post/260369/nym-privacy-protections-near-ecosystem) - Nym mixnet privacy for NEAR blockchain ecosystem
- [Nym 2026 Roadmap](https://nym.com/blog/nym-roadmap-2026) - Plans for enhanced censorship resistance and privacy features
- [NymVPN Censorship Resistance 2026](https://nym.com/blog/nym-censorship-resistance-2026) - Building decentralized VPN network for bypassing censorship
- [NymVPN dApp Mode](https://nym.com/blog/nymvpn-dapp-mode) - Route wallet traffic through mixnet via SOCKS5 proxy for blockchain metadata privacy
- [Katzenpost](https://katzenpost.network/) - Mix network research project and protocol specification
- [Katzenpost Mix Spec](https://katzenpost.network/docs/specs/mixspec.html) - Formal mix network protocol specification
- [Katzenpost GitHub](https://github.com/katzenpost/katzenpost) - Open source mix network implementation with post-quantum cryptography
- [Loopix Anonymity System](https://arxiv.org/abs/1703.00536) - Piotrowska et al. (2017) — low-latency mixnet with cover traffic and provider-based anonymous messaging
- [Loopix Messaging](https://github.com/google-deepmind/loopix-messaging) - Experimental Go implementation of anonymous messaging using mix networks
- [Mixnet and ACN Research](https://github.com/lehnberg/mixnet-and-acn-research) - Curated bibliography for mixnets and anonymous communication networks
- [Katzenpost FOSDEM 2025](https://archive.fosdem.org/2025/schedule/event/fosdem-2025-5475-katzenpost-developing-privacy-software-in-go/) - Post-quantum mixnet implementation in Go
- [Katzenpost Threat Model](https://katzenpost.network/docs/threat_model/) - Security assumptions and attack scenarios for the mixnet design
- [Katzenpost Admin Guide](https://katzenpost.network/docs/) - Running Katzenpost servers including local Docker mixnet setups
- [HOPR](https://hoprnet.org/) - Decentralized, metadata-private point-to-point data exchange protocol based on an incentivized mixnet

#### Related Privacy Infrastructure
- [Oblivious HTTP (OHTTP)](https://en.wikipedia.org/wiki/Oblivious_HTTP) - IETF protocol for anonymous HTTP transactions via relay
- [Oblivious DoH (ODoH)](https://blog.cloudflare.com/oblivious-dns/) - DNS resolution via oblivious relay to hide client identity from resolver
- [RFC 9458: OHTTP](https://www.rfc-editor.org/rfc/rfc9458) - IETF standard for Oblivious HTTP
