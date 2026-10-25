---
title: "Unstoppable Domains"
slug: unstoppable-domains
type: deep-dive
pillars: ["naming"]
readiness: cautionary
description: "Unstoppable Domains offers blockchain-based names: resolution choices, contract trust and what its deactivation patent does and does not establish."
dek: "Blockchain-based names with public resolution software and a published deactivation patent application; contract authority and deployed behavior need separate evaluation."
updated: 2026-10-25
created: 2026-06-22
origin: vault
source: "03-Decentralized-DNS/Unstoppable Domains.md"
aliases: ["UD", "Unstoppable", ".crypto", ".wallet", ".nft", ".x", ".bitcoin"]
tags: ["unstoppable-domains", "web3", "naming", "takedown", "centralization", "deep-dive"]
---

## Summary

Unstoppable Domains provides blockchain-based names and software for resolving their records. Its resolution library supports reading blockchain data through configured providers. Resolution therefore does not inherently require the company’s hosted resolver, although hosted interfaces and RPC providers can still be practical dependencies.

The relevant distinction is between ownership records, contract authority, resolution software and the interfaces a user chooses. Compare [ENS](/kb/ens/), [Handshake](/kb/handshake/) and [Namecoin](/kb/namecoin/) in the [decentralized naming overview](/kb/decentralized-dns/).

## How it works

Applications use resolution software to obtain records such as cryptocurrency addresses and content locations associated with a name. The library documents supported naming systems and provider configuration. A user’s dependency on a hosted API depends on the chosen integration; it is not a universal protocol requirement.

## The deactivation patent application

US20250274481A1, titled *Deactivation of decentralized domains*, was filed on February 28, 2024 and published on August 28, 2025. It describes a proposed deactivation process involving signed requests, wallet-related thresholds and a reviewing authority.

This is evidence of a proposed mechanism. A patent application does not establish that the mechanism is implemented, deployed or enabled for existing names. It also does not prove that an operator can unilaterally deactivate every name. Those questions require examining the relevant deployed contracts and resolution behavior.

## Trust model / threat model

- Check the contract and naming system used by the particular name.
- Distinguish control over a token or record from control over a website, gateway or hosted API.
- A resolver can refuse to answer without changing the underlying blockchain record.
- An independent resolver reduces dependence on a hosted service but still needs a reliable view of chain state.

## Readiness

Resolution software and integration documentation are public. Evaluate the supported chain, provider and client combination for the intended application. The patent application alone supplies no deployment-readiness evidence for its proposed deactivation process.

## Comparison and limits

[Handshake](/kb/handshake/) names require renewal: its implementation defines an approximately two-year mainnet renewal window and enforces expiry. Blockchain storage does not imply perpetual availability or identical renewal rules across naming systems.

The Oxford Information Labs and AFNIC study examines blockchain-domain providers as a diverse market. Its findings should not be treated as proof that every provider uses the same contracts or governance.

For a censorship-resistance assessment, inspect the current contracts, resolver path and client behavior. Marketing language, a token record and a patent filing each describe different parts of that assessment.

## Primary sources

- [Deactivation of decentralized domains: patent application US20250274481A1](https://patents.google.com/patent/US20250274481A1/en)
- [Oxford Information Labs and AFNIC: blockchain domain provider study](https://oxil.uk/news/mapping-blockchain-domain-providers-10-key-findings-from-oxford-information-labs-and-afnic/)
- [Handshake mainnet renewal window](https://github.com/handshake-org/hsd/blob/master/lib/protocol/networks.js)
- [Handshake name-expiry rule](https://github.com/handshake-org/hsd/blob/master/lib/covenants/namestate.js)
- [Handshake RENEW covenant validation](https://github.com/handshake-org/hsd/blob/master/lib/blockchain/chain.js)
- [Unstoppable Domains documentation](https://docs.unstoppabledomains.com/)
- [Unstoppable resolution library](https://github.com/unstoppabledomains/resolution)
