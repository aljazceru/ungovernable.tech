---
title: "Satellite broadband and direct-to-cell"
slug: satellite-broadband
type: explainer
pillars: ["mesh", "circumvention"]
readiness: usable
description: "Compare satellite terminals and direct-to-cell access through Starlink, OneWeb and Amazon Leo, including accounts, operator control and location limits."
dek: "A satellite path can bypass a damaged terrestrial link while retaining commercial, geographic and account dependencies."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: ["satellite-iot", "blockstream-satellite", "community-networks", "internet-shutdown-preparedness"]
---

## Summary

Satellite broadband and satellite-to-phone service solve different access problems. Broadband systems use dedicated terminals; direct-to-cell connects compatible cellular phones through a mobile-service arrangement. Neither makes the satellite operator, account or service authorization disappear. Compare [satellite IoT](/kb/satellite-iot/) for narrowband messaging and telemetry.

## How it works

| System | What the official source establishes | What to check before relying on it |
|---|---|---|
| Starlink broadband | Published service terms describe a Starlink kit, recurring service and installation with a clear view of the sky. | The current plan, authorized location, power, mounting and account access. |
| Eutelsat OneWeb | Eutelsat describes a low-Earth-orbit network with fixed and mobile services and a range of user terminals. | The service arrangement and terminal suitable for the actual site or vehicle. |
| Amazon Leo, formerly Project Kuiper | Amazon's FAQ uses the new name, describes an enterprise preview begun in November 2025 and a wider rollout during 2026. | A rollout statement is not confirmation that service can be ordered at your address. |
| Starlink direct-to-cell with T-Mobile | Starlink's published service notice documents satellite messaging for T-Mobile customers using 4G LTE phones. | Current device, subscription, territory and supported-service requirements; the notice is not a current feature matrix. |

## Trust model / threat model

**Operator and account control.** The cited Starlink terms allow suspension or termination for reasons including government requests, technical problems, missing authorizations and nonpayment. A terminal can provide another physical route while its service remains dependent on an operator's systems and decisions.

**Geographic restrictions.** Starlink's published September 2024 terms explicitly allow suspension when a roaming location is outside authorized territory. That is evidence of a location-dependent service policy, not a promise about today's plan in every country. Check the current contract and authorization for the intended location before deployment.

**Location exposure.** The terms link service to an account and address and regulate changes of location. Do not treat possession of a terminal as anonymous access. This entry does not infer precise telemetry collection or retention from those clauses.

## Readiness

**Usable, depending on network and location.** Starlink and Eutelsat publish service and equipment documentation; Amazon's own rollout language should remain distinct from confirmed local availability. Direct-to-cell messaging should not be equated with the capacity or application support of a broadband terminal.

## Limits

Plan for power, sky visibility, account recovery and a way to communicate when the satellite service itself is unavailable. For community backhaul, include it in a [community network](/kb/community-networks/) plan. For continuity, read [internet-shutdown preparedness](/guides/internet-shutdown-preparedness/); [Blockstream Satellite](/kb/blockstream-satellite/) describes a separate Bitcoin-data service.

## Primary sources

- [Starlink published service terms: kit, accounts and termination](https://starlink.com/public-files/Starlink_ToS_4.28.25.pdf)
- [Starlink published September 2024 terms: location restrictions](https://www.starlink.com/public-files/Starlink_ToS_9.10.24.pdf)
- [Eutelsat OneWeb constellation and services](https://www.eutelsat.com/satellite-network/oneweb-leo-constellation)
- [Eutelsat LEO terminal range](https://www.eutelsat.com/satellite-network/oneweb-leo-constellation/leo-equipment)
- [Amazon Leo FAQ: former Kuiper name and rollout status](https://www.aboutamazon.com/news/innovation-at-amazon/what-is-amazon-project-kuiper)
- [Starlink direct-to-cell service notice naming T-Mobile](https://starlink.com/public-files/DIRECT_TO_CELL_SERVICE_FEB_25.pdf)
