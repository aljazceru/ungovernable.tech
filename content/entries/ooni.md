---
title: "OONI"
slug: ooni
type: deep-dive
pillars: [circumvention]
readiness: usable
description: "OONI Probe measures website, messaging and circumvention-tool reachability. Learn to read its public data and assess the risks of running tests."
dek: "Evidence about network interference, with public measurements that require care both to collect and to interpret."
updated: 2026-10-25
created: 2026-10-25
origin: original
related: [pluggable-transports, psiphon, outline, wireguard, censorship-circumvention, internet-shutdown-preparedness, map-censorship-resistance]
tags: [ooni, measurement, censorship, open-data]
---

## Summary

The Open Observatory of Network Interference (OONI) develops OONI Probe to measure internet censorship and other network interference. Probe makes test connections; OONI Explorer publishes and helps analyse the resulting measurements. Use it to investigate what failed, where and when. It does not itself give a blocked connection a way around censorship.

## How it works

**Probe apps.** OONI provides mobile apps for Android and iOS, desktop apps for Windows and macOS, and a command-line tool for Linux and macOS. Its [test catalogue](https://ooni.org/nettest/) covers websites; messaging services including Signal, WhatsApp, Telegram and Facebook Messenger; and circumvention tools including Tor, Snowflake and [Psiphon](/kb/psiphon/). These tests check service reachability, not the confidentiality of messages sent with those services.

**Web Connectivity.** The test performs DNS lookups, attempts TCP connections and makes web requests, comparing observations on the tested network with a control vantage point. Differences can indicate DNS tampering, connection blocking or HTTP interference. OONI's [test description](https://ooni.org/nettest/web-connectivity/) also explains false positives caused by ordinary DNS variation, differing website responses and failures unrelated to censorship.

**Open data.** Measurements are published by default. [OONI Explorer](https://explorer.ooni.org/) offers search and aggregate views; OONI also provides an API and bulk-data access. Publication makes independent analysis possible, but changes the risk of running a test.

## How to read a measurement

Start with the [Explorer user guide](https://ooni.org/support/ooni-explorer/) and an existing measurement rather than immediately generating a new one.

1. **Check the context.** Note the tested service, test name, country, network's Autonomous System Number (ASN), and UTC timestamp. A result describes that observation on that network, not every connection in a country.
2. **Read the status carefully.** An *anomaly* is potential interference, not a confirmed censorship finding. *Confirmed blocked* website measurements match known blocking fingerprints, such as a recognised block page. *OK* records successful accessibility under that test's criteria.
3. **Open the details.** Inspect DNS answers, connection failures and HTTP responses. The raw JSON and its `test_keys` field expose the observations behind the summary. A timeout by itself does not identify who caused it.
4. **Compare a pattern.** Look for the same failure across repeated tests, dates and relevant networks. Compare anomalies with the total measurement count. OONI recommends aggregate analysis to reduce false positives; missing measurements do not establish that a service is reachable.

## Trust model / threat model

**Running Probe is visible.** OONI warns that an ISP, government or employer monitoring the connection can see testing activity. Tested services also see the connecting IP address. Tests may access sensitive or locally prohibited websites.

OONI's [risk statement](https://ooni.org/about/risks/) warns that running Probe can expose users to prosecution, fines or imprisonment in some jurisdictions, and recommends local legal advice before use. These are OONI's stated potential risks, not a claim about the law where you live.

**Publication can identify more than intended.** OONI tries to avoid publishing probe IP addresses, but warns that a determined ISP could identify users through public measurements. Country, network, timing and tested URLs still reveal context. The apps allow users to opt out of publication; that does not hide the test connections from the local network. Review test selection and publication settings before running anything.

## Readiness

**Usable.** The apps, public Explorer and data interfaces support practical measurement and investigation. The limitation is interpretation and local risk, not a missing deployment path. Reading existing results is a useful first step when collecting new measurements would expose someone.

## Limits

- Test results concern particular services and network conditions. An anomaly is not a complete diagnosis or evidence that every circumvention tool fails.
- Coverage depends on where people run Probe and what they test. An empty search is a coverage gap, not proof that there is no censorship.
- A measurement does not guarantee that a tool will work later. Keep a separate access plan with [pluggable transports](/kb/pluggable-transports/), [Outline](/kb/outline/) or [Psiphon](/kb/psiphon/), and an [offline preparation plan](/guides/internet-shutdown-preparedness/).

## Primary sources

- [OONI](https://ooni.org/) and [OONI Probe downloads](https://ooni.org/install/).
- [Test catalogue](https://ooni.org/nettest/) and [Web Connectivity methodology](https://ooni.org/nettest/web-connectivity/).
- [Risks of running OONI Probe](https://ooni.org/about/risks/).
- [OONI Explorer](https://explorer.ooni.org/) and [Explorer user guide](https://ooni.org/support/ooni-explorer/).
- [API and bulk-data access](https://ooni.org/data/).
