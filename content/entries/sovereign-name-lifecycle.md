---
title: "Sovereign name lifecycle"
slug: sovereign-name-lifecycle
type: explainer
pillars: ["naming"]
readiness: usable
description: "Compare renewal, expiry and recovery for ENS, Handshake, Namecoin, Pkarr and onion services. Owning a key still leaves operational duties."
dek: "A name can depend on renewals, republishing or a permanent secret key; recovery begins before any of those fails."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: ["ens", "handshake", "namecoin", "pkarr", "onion-and-i2p-naming"]
---

## Summary

Naming systems make different promises about persistence. Some registrations expire unless renewed on a chain. Some records disappear unless republished. An onion-service address instead depends on its identity key. Treat renewal, publication and key backup as separate jobs.

## How it works

| System | Lifecycle in the cited documentation | Operational consequence |
|---|---|---|
| [ENS](/kb/ens/) `.eth` registration | Registration has an expiry; the registrar documents a 90-day grace period before a temporary premium auction. Anyone can pay to renew a name. | Monitor the registration's expiry and renew before it. This rule does not describe every ENS name or subname. |
| [Handshake](/kb/handshake/) | `hsd` mainnet sets `renewalWindow` to `(2 * 365) * blocksPerDay`: roughly two years expressed in blocks. | Monitor the chain's name state and renew well before the window closes. Wall-clock estimates are not the consensus rule. |
| [Namecoin](/kb/namecoin/) | The FAQ specifies semi-expiry after 31,968 blocks without an update or renewal, then final expiry after another 4,032 blocks. | Semi-expiry stops resolution while retaining ownership; after final expiry anyone may register the name. |
| [Pkarr](/kb/pkarr/) | DHT records are ephemeral and require periodic republishing. | Keep a publisher running and retain the key needed to sign fresh records. |
| [Onion services](/kb/onion-and-i2p-naming/) | Tor stores the service's identity keys in `HiddenServiceDir`; its setup guide requires protecting that directory. | Back up the service keys securely if the same address must survive a host loss. |

## Trust model / threat model

The renewal wallet and publication key are high-value credentials. Tor explicitly warns that someone obtaining an onion service's keys can impersonate it. A backup must therefore be both recoverable and protected from disclosure.

A renewal and a record update are not interchangeable across these systems. ENS permits another account to pay a renewal without making that account the owner. Namecoin's FAQ distinguishes update/renewal from re-registration after expiry. Use the actual state transition for the system you operate.

## A maintenance plan

Keep an inventory of names, controlling keys, renewal or republishing obligations and a recovery contact. Set reminders with enough time to fix a funding or signing problem. Rehearse restoring a noncritical name or test service before relying on a backup for a public address. For Pkarr, test resolution after restarting the publisher; for an onion service, confirm that restoring the key directory restores the expected address.

## Readiness

**Usable.** These mechanisms are documented, but each has its own maintenance model. There is no universal recovery desk behind a key-controlled name.

## Limits

This covers the named registration and publication mechanisms, not every wallet's recovery feature or every subname policy. A name can resolve correctly while its destination is unavailable. Plan naming and hosting recovery together.

## Primary sources

- [ENS ETH registrar, renewal and grace period](https://docs.ens.domains/registry/eth/)
- [Handshake hsd mainnet renewal parameters](https://github.com/handshake-org/hsd/blob/master/lib/protocol/networks.js)
- [Namecoin FAQ: semi-expiry, expiry and wallet backup](https://www.namecoin.org/docs/faq/)
- [Pkarr record lifetime and republishing](https://github.com/pubky/pkarr)
- [Tor onion-service setup and key protection](https://community.torproject.org/onion-services/setup/)
