---
title: "Build a post-quantum cryptographic inventory"
slug: pqc-cryptographic-inventory
type: explainer
pillars: ["pqc"]
readiness: usable
description: "Inventory protocols, libraries, keys and certificates before a post-quantum migration. Use official guidance to prioritize dependencies and data lifetimes."
dek: "Find where cryptography lives, who can change it and which secrets must remain protected longest."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: ["post-quantum-cryptography", "hybrid-kem-migration", "pqc-deployment-tracker", "hardware-supply-chain-trust"]
---

## Summary

The joint CISA, NSA and NIST quantum-readiness guidance recommends a migration roadmap, cryptographic discovery, a useful inventory and engagement with suppliers. Start by finding dependencies, not by replacing one algorithm name in a configuration file.

## What to record

The following is a practical inventory template based on that guidance. Adapt it to the systems you actually operate; it is not a mandated agency form.

| Record | Questions to answer |
|---|---|
| System and owner | Which service, device or product depends on the cryptography? Who can authorize a change? |
| Protocol and purpose | Is it protecting transport, stored data, authentication, signatures or software updates? |
| Implementation | Which library, product, hardware module and installed version implement it? |
| Algorithms and parameters | What is configured, and what is actually negotiated in use? |
| Keys and certificates | Where are they generated, stored, rotated and validated? Which trust roots and peers depend on them? |
| Protected information | How long must confidentiality or signature validation remain useful? |
| Dependencies | Which vendors, counterparties, firmware updates or certificate services must change first? |
| Evidence and status | When was the record checked, by which method, and what migration test remains? |

Record key identifiers and custody arrangements, not private-key material in the spreadsheet.

## How to use the inventory

1. Assign an owner and scope for discovery. Include externally supplied services as well as your own code.
2. Combine technical discovery with questions to system owners and suppliers. Ask vendors for their cryptographic dependencies and migration plans.
3. Prioritize long-lived sensitive data and systems that take a long time to replace. The joint guidance explains the risk of collecting encrypted data now for later decryption.
4. Track a tested replacement path, including compatibility, performance and rollback decisions. An inventory item is not migrated merely because a supplier announced support.
5. Keep the inventory current as systems, dependencies and certificates change.

## Trust model / threat model

A vendor response is evidence to assess, not proof of what a deployed endpoint negotiates. Keep documentation and measurements connected to the same system record. Use [hybrid KEM migration](/guides/hybrid-kem-migration/) when planning protocol transitions.

## Readiness

**Usable now.** Discovery and dependency mapping do not require waiting for every product to support new algorithms. CISA's quantum initiative explicitly includes inventory and migration planning.

## Limits

The cited NIST IR 8547 page labels that publication an **Initial Public Draft**. Its proposed transition approach is not treated here as a final mandatory deadline. This page does not predict a quantum-computer arrival date or imply that every cryptographic primitive needs the same replacement. Continue with [post-quantum cryptography](/kb/post-quantum-cryptography/) and the [deployment tracker](/kb/pqc-deployment-tracker/).

## Primary sources

- [CISA, NSA and NIST quantum-readiness guidance](https://www.cisa.gov/resources-tools/resources/quantum-readiness-migration-post-quantum-cryptography)
- [Joint factsheet: inventory, priorities and vendor engagement](https://www.cisa.gov/sites/default/files/2023-08/Quantum%20Readiness_Final_CLEAR_508c%20%283%29.pdf)
- [CISA quantum initiative](https://www.cisa.gov/quantum)
- [NIST IR 8547 Initial Public Draft](https://csrc.nist.gov/pubs/ir/8547/ipd)
