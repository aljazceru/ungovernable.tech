---
title: "Nostr VPN"
slug: nostr-vpn
type: deep-dive
pillars: ["mesh", "identity"]
readiness: experimental
description: "Nostr VPN, a Tailscale-style private mesh network that uses Nostr keys for identity and WireGuard for transport: design and experimental status."
dek: "Tailscale-style private mesh VPN built on Nostr cryptographic identity + FIPS mesh data plane. No central coordination servers, no third-party accounts, no email sign-up. Your npub is your identity and address across social and networking planes."
updated: 2026-06-22
created: 2026-06-22
origin: vault
source: "05-Off-Grid-Networks/Nostr VPN.md"
aliases: ["nvpn", "NostrVPN"]
tags: ["nostr-vpn", "fips", "mesh", "vpn", "nostr", "tailscale-alternative", "off-grid", "overlay", "deep-dive"]
---

## What it is and why it matters

Nostr VPN (by Martti Malmi, early Bitcoin contributor) applies Bitcoin/Nostr design principles (permissionless, self-sovereign keys, no trusted third parties) to the VPN / overlay networking problem.

Traditional VPNs: central server (or Tailscale-style coordination server + third-party auth like Google/Microsoft) sees metadata or becomes a subpoena target / single point of failure / censorship vector.

Nostr VPN eliminates the central coordination point:
- Identity: pure Nostr keypair (npub). No registration, no email.
- Discovery / signaling / NAT traversal: via public Nostr relays using encrypted gift-wrapped messages (NIP-17 style patterns).
- Data plane: FIPS (see [FIPS](/kb/fips-mesh/)) for self-organizing encrypted mesh routing across heterogeneous transports (UDP, TCP, Ethernet, Tor, Bluetooth).
- Tunnels: WireGuard (boringtun) with hop-by-hop + independent E2E encryption layers and periodic rekeying for forward secrecy.
- Fallback: Nostr-based multihop routing when direct NAT hole-punching fails.

Result: a private mesh that "just works" for your devices (and friends' devices) using only keys you already control for Nostr.

Native apps / packages for macOS, Linux, Windows, Android; CLI (cargo install nvpn); Umbrel and StartOS packages. Active releases into mid-2026.

## Architecture highlights

- Two encryption layers: FIPS hop-by-hop (peers on the mesh) + independent E2E between your endpoints.
- MagicDNS and simple management UX in the apps.
- Peer discovery and route setup orchestrated via Nostr relays (censorship-resistant signaling).
- When internet is available it provides global mesh reach; when constrained it can leverage whatever transports FIPS supports (including BLE for local).
- Exit nodes and "paid exit" experiments exist but core is private LAN-style mesh between your nodes.

It turns your self-hosted services (Umbrel node, homelab, laptops) into a sovereign Tailscale replacement.

## Trade-offs

### Strengths (sovereignty angle)
- No company, no account, no central anything that can log, block, or be compelled.
- Single keypair works for Nostr social + this mesh (composes beautifully with [Nostr](/kb/nostr-identity/) and [FIPS](/kb/fips-mesh/)).
- Works across platforms + self-hosted app stores (Umbrel/StartOS).
- Graceful fallback via Nostr multihop.
- Open source (MIT per releases), driven by cypherpunk ethos.

### Limitations
- Still younger than Tailscale/WireGuard ecosystems (fewer polished enterprise features, smaller node count for relay density in some regions).
- Performance depends on FIPS mesh quality + relay latency for signaling; not a drop-in for high-bandwidth always-on corporate use yet.
- Requires Nostr relay connectivity for initial discovery / certain fallbacks (though once peered, direct paths dominate).
- iOS public availability lagged behind other platforms in early releases (TestFlight betas existed).

## Attack surface & trust model

- **Adversary at relays**: sees only encrypted gift-wrapped discovery traffic (Nostr-side privacy applies). No data plane visibility.
- **FIPS mesh peers**: see hop-by-hop encrypted traffic; cannot correlate your full flows without breaking both layers.
- **Endpoint compromise**: same as any WG-based VPN — keys on device.
- **Nostr key compromise**: catastrophic for both identity and this mesh (single keypair design).
- **Sybil / spam in discovery**: mitigated by Nostr WoT patterns and gift-wrapping; rate limits apply.
- **Quantum**: inherits from secp256k1 + whatever FIPS/WG crypto uses today (track [Overview - Post-Quantum Cryptography](/kb/post-quantum-cryptography/) migration).

Trust assumptions are radically lower than any commercial or even "mesh" VPN with a control plane company.

## Common compositions

- Pair with [Nostr](/kb/nostr-identity/) identity and [Blossom](/kb/blossom/) / self-hosted services for full sovereign personal cloud access from anywhere.
- Run on Umbrel/StartOS alongside Bitcoin/LN node for remote private access without exposing ports.
- Combine with [Mix Networks](/kb/mix-networks/) (Tor transport inside FIPS) for extra metadata resistance on public links.
- Local fallback: BLE transport for air-gapped-ish or internet-down scenarios within physical proximity.

See also [MOC - Composing Primitives](/kb/map-composing-primitives/) and [MOC - Censorship Resistance](/kb/map-censorship-resistance/) for stacking patterns.

## Evidence & Status (2026)

- GitHub: mmalmi/nostr-vpn (mirror of canonical git.iris.to); frequent releases (4.0.x series through June 2026), multi-platform binaries, Docker, packaging for self-hosted nodes.
- Umbrel integration highlighted as "major advancement in sovereign infrastructure".
- X / Nostr discussion positions it explicitly as response to centralized VPN trust models and potential regulatory pressure on commercial VPNs.
- Backed by real engineering from Bitcoin early contributor; aligns with ungovernable primitives (keys, relays, mesh).

## Sources

- Repo + README: https://github.com/mmalmi/nostr-vpn (and git.iris.to equivalent)
- Releases, changelog, AGENTS.md / CONTRIBUTING for process.
- FIPS: https://github.com/jmcorgan/fips (and KB [FIPS](/kb/fips-mesh/) note)
- Community signals: recent X posts on multi-platform launch, Umbrel, resistance to central control.

*Verify latest release notes and transport matrix before production reliance; the project moves fast.*
