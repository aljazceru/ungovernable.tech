---
title: "Run a private circumvention server for people you know"
slug: self-hosted-circumvention-server
type: guide
pillars: [circumvention, anonymity]
readiness: usable
description: "Set up Outline or WireGuard for a trusted group, test routing and revocation, and compare running a Tor bridge or Snowflake proxy instead."
dek: "Choose who can connect, explain what you can observe, and practise replacing the server before someone depends on it."
updated: 2026-10-25
created: 2026-10-25
origin: original
level: intermediate
time: "An afternoon, plus ongoing maintenance"
related: [outline, wireguard, pluggable-transports, psiphon, ooni, censorship-circumvention, internet-shutdown-preparedness, running-freedom-infrastructure]
tags: [self-hosting, outline, wireguard, tor, bridges, guide]
---

## Summary

The goal is a working route for a small group, with an operator they know and a recovery plan they can use. [Outline](/kb/outline/) provides a manager and shareable access keys. [WireGuard](/kb/wireguard/) provides an encrypted IP tunnel with explicit peer and routing configuration. A [Tor bridge or Snowflake proxy](/kb/pluggable-transports/) contributes an entry route into Tor instead of serving as the group's internet exit.

## Choose the role

| Option | Choose it when | Responsibility you accept |
|---|---|---|
| **Outline** | You want Manager-assisted deployment and individual access keys. | Run the host, manage keys and explain the server's visibility into connections. |
| **WireGuard** | UDP and the WireGuard protocol work on the users' networks, and you can administer routing and DNS. | Configure each peer and check that intended traffic actually uses the tunnel. Standard WireGuard has no built-in obfuscation. |
| **Tor bridge** | You want to offer a Tor entry point. | Maintain the bridge and its transport, check reachability and handle bridge distribution. |
| **Snowflake proxy** | You want to donate connectivity with a browser extension or a standalone proxy. | Keep the proxy available; it helps users selected by the Snowflake system, rather than issuing private access keys to friends. |

First read [Getting Around Internet Censorship](/guides/censorship-circumvention/) and look at existing [OONI measurements](/kb/ooni/). Do not ask someone to run probes without first discussing OONI's [documented risks](https://ooni.org/about/risks/).

## Before you rent a server

Choose a host with internet access outside the blocking you are trying to bypass. Check its terms for proxy or VPN operation, the cost of outbound traffic and the account-recovery process. Use a separate server for this role, keep its system supported and updated, and restrict administrative access. Agree who will pay, maintain it and contact users if it stops working.

Explain the trust model before sharing access: an Outline or WireGuard gateway receives client connections and forwards traffic to destinations. It can observe connection metadata and unencrypted application traffic; HTTPS remains separately encrypted. Minimise diagnostic logging and tell users what you retain. An operator policy is not a technical guarantee against observation by the host.

## Option 1: Outline Manager

Follow [Outline's server setup instructions](https://support.getoutline.org/manager/server-setup/setup-server) alongside these steps.

1. **Install Manager on your computer.** Use the official [Get started page](https://getoutline.org/get-started/). Manager administers the server; the people connecting use Outline Client.
2. **Create the server.** Select a supported cloud setup flow, or the option for your own Linux infrastructure. For the latter, follow Manager's instructions for connecting to the machine and running its installation script. Read the script before running it with administrative privileges.
3. **Complete registration in Manager.** For a manual installation, the installer returns management configuration containing `apiUrl` and `certSha256`. Enter that configuration where Manager requests it, and store it privately. It is not a client invitation.
4. **Check the firewall.** Follow the ports reported by the installer: the management API uses TCP; access-key traffic needs TCP and UDP. Where practical, restrict the management port to your administration connection. Check both the host firewall and the provider's network firewall. The [official installer](https://raw.githubusercontent.com/Jigsaw-Code/outline-server/master/src/server_manager/install_scripts/install_server.sh) documents these requirements.
5. **Create a key per person or device.** Set data limits if needed. Send each invitation through an existing private channel. The recipient installs Client, imports the key and connects. Avoid a shared key that would require revoking the whole group at once.
6. **Test revocation before rollout.** Create a disposable key, connect with it, delete it in Manager, and check that a fresh connection using it fails. Keep your administrative configuration out of screenshots and group messages.

Review the [Outline privacy policy](https://getoutline.org/policies/privacy/) as well: automatic crash reports and optional server metrics are separate from any logs you or the hosting provider keep.

## Option 2: a WireGuard gateway

Use this only after confirming that ordinary WireGuard works on the intended network. Its [known limitations](https://www.wireguard.com/known-limitations/) explicitly leave traffic disguise to another layer. If it is fingerprinted or blocked, compare Outline, [Psiphon](/kb/psiphon/) or Tor transports before investing in a standard WireGuard deployment.

For an Ubuntu server and Linux client, follow Canonical's [VPN as the default gateway](https://documentation.ubuntu.com/server/how-to/wireguard-vpn/vpn-as-the-default-gateway/) procedure. It includes both sides of the connection, forwarding, source NAT and DNS. The sequence matters:

1. **Install and generate separate keys.** Use the [official installation instructions](https://www.wireguard.com/install/) for each system. On Ubuntu, install `wireguard`. On each peer, generate its own keypair as in the [quick start](https://www.wireguard.com/quickstart/):

        umask 077
        wg genkey > privatekey
        wg pubkey < privatekey > publickey

   Exchange public keys through an authenticated channel. Keep each private key on its own device, in a protected configuration location; never send it to the other peer.

2. **Create the peer configurations.** Assign non-overlapping tunnel addresses. The server's peer entry gets the client's public key and that client's tunnel address in `AllowedIPs`. The client's peer entry gets the server's public key, reachable address and UDP port. For an IPv4 internet gateway, its `AllowedIPs` is `0.0.0.0/0`. Use the [wg manual](https://git.zx2c4.com/wireguard-tools/about/src/man/wg.8) for the exact fields and Canonical's complete example for file placement. Give additional clients distinct keys and addresses.
3. **Make the server a gateway.** Allow the chosen UDP port through both firewalls. Enable IP forwarding, add source NAT for the tunnel subnet where required, and allow forwarding between the tunnel and internet interface. Follow the distribution's persistent firewall configuration so this survives a reboot. A handshake without forwarding does not provide internet access.
4. **Set DNS and decide on IPv6.** Select a resolver deliberately and route its queries through the tunnel. Canonical documents `resolvectl` configuration; [wg-quick](https://git.zx2c4.com/wireguard-tools/about/src/man/wg-quick.8) also has DNS configuration support. `0.0.0.0/0` covers only IPv4. Either configure IPv6 addressing, forwarding and `::/0` routing too, or block IPv6 outside the tunnel on the client. Do not assume an IPv4-only example protects IPv6 traffic.
5. **Bring up and verify both ends.** Use `wg-quick up` with the interface names from your configuration. Inspect `wg show` for a recent handshake and changing transfer counters; then test actual traffic as below. Configure startup using your operating system's service management and repeat the tests after reboot.
6. **Revoke a test peer.** Remove its peer entry from the server's saved configuration and running interface, then check that it can no longer connect. The `wg` manual documents `peer <public-key> remove`. If you require traffic to stop when the tunnel fails, configure and test a firewall policy; the `wg-quick` manual supplies a kill-switch example, with separate IPv6 considerations.

## Option 3: help people enter Tor

**An obfs4 bridge.** Follow the [Tor Project's bridge setup guide](https://community.torproject.org/relay/setup/bridge/), selecting the instructions for your system. Configure the bridge role and transport, open the required ports, and use the [post-install checks](https://community.torproject.org/relay/setup/bridge/post-install/) to retrieve and test the complete bridge line in Tor Browser. If you will distribute the address yourself, set `BridgeDistribution none` in `torrc` before starting the bridge. The [Tor manual packaged by Debian](https://manpages.debian.org/trixie/tor/tor.1.en.html) documents that this asks BridgeDB not to distribute the address; the default lets BridgeDB choose. This controls distribution, not who can connect once they have the bridge details. Do not post private bridge lines publicly.

**A WebTunnel bridge.** The [WebTunnel guide](https://community.torproject.org/relay/setup/webtunnel/) adds a domain, a valid TLS certificate and a web server that forwards a secret URL path to the transport. Choose this if you can also maintain that website and certificate.

**A Snowflake proxy.** Follow the [Snowflake operator guide](https://community.torproject.org/relay/setup/snowflake/): install and enable the browser extension, or choose the standalone deployment. Check its status for connection errors. The extension helps other users; to use Snowflake yourself, select it in Tor Browser. This is a contribution to the shared system, not a private server assigned to your group.

The [Tor relay-role guide](https://community.torproject.org/relay/types-of-relays/) explains why bridge and exit operation differ. These instructions are for an entry route; an exit relay has different operational and legal responsibilities.

## Verify with one willing user

- **Test from the affected network.** Success from the server operator's uncensored connection does not establish reachability for the people who need it.
- **Test routing, not just the connection indicator.** Check the public address seen by a service you trust, the resolver used for DNS, and both IPv4 and IPv6. Compare with the intended route without sharing sensitive browsing history.
- **Test failure.** Interrupt the tunnel and observe whether applications reconnect directly. Check the behaviour after sleep, network changes and reboot. Explain any gaps before someone relies on it.
- **Test recovery.** Practise revoking a key and issuing a replacement. Record how to recreate the server, restore administration and contact users through an independent channel.

## Limits and ongoing care

Keep software updated, review access when someone leaves, and monitor capacity without collecting browsing histories. Keep an alternative transport ready. Outline's FAQ explicitly anticipates replacing a blocked server; a new address is a recovery option, not a guarantee against the same blocking technique.

These options need a surviving internet path. Keep [Internet Shutdown Preparedness](/guides/internet-shutdown-preparedness/) beside the server plan, and use [Running Infrastructure for Freedom](/guides/running-freedom-infrastructure/) to choose other ways to contribute.

## Primary sources

- [Outline setup flow](https://getoutline.org/get-started/), [server setup](https://support.getoutline.org/manager/server-setup/setup-server), [installer](https://raw.githubusercontent.com/Jigsaw-Code/outline-server/master/src/server_manager/install_scripts/install_server.sh), [FAQ](https://getoutline.org/faq/) and [privacy policy](https://getoutline.org/policies/privacy/).
- [WireGuard installation](https://www.wireguard.com/install/), [quick start](https://www.wireguard.com/quickstart/), [limitations](https://www.wireguard.com/known-limitations/), [wg manual](https://git.zx2c4.com/wireguard-tools/about/src/man/wg.8) and [wg-quick manual](https://git.zx2c4.com/wireguard-tools/about/src/man/wg-quick.8).
- [Canonical's complete WireGuard gateway procedure](https://documentation.ubuntu.com/server/how-to/wireguard-vpn/vpn-as-the-default-gateway/).
- [Tor bridge setup](https://community.torproject.org/relay/setup/bridge/), [post-install verification](https://community.torproject.org/relay/setup/bridge/post-install/), [WebTunnel setup](https://community.torproject.org/relay/setup/webtunnel/), [Snowflake operation](https://community.torproject.org/relay/setup/snowflake/) and [relay roles](https://community.torproject.org/relay/types-of-relays/).
- [Tor manual: BridgeDistribution](https://manpages.debian.org/trixie/tor/tor.1.en.html).
- [Snowflake's user and volunteer roles](https://snowflake.torproject.org/) and [OONI's probe risks](https://ooni.org/about/risks/).
