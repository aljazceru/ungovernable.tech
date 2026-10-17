---
title: "Threat Modeling for Sovereign Individuals"
slug: threat-modeling
type: guide
pillars: [endpoint, anonymity, messaging]
description: "Start here. A practical way to decide what you are protecting, from whom, and which tools on this site are worth the effort for you."
dek: "Before choosing a single tool, write down what you are protecting, who you are protecting it from, and what failure would cost you."
updated: 2026-10-17
created: 2026-10-17
origin: original
level: beginner
time: "45 minutes"
related: [map-threat-models, metadata-resistance, choosing-a-secure-messenger, using-tor-safely, tails-qubes-whonix]
---

Most security advice fails because it is generic. A journalist protecting a source inside a ministry, a Bitcoin holder worried about a home invasion, and a developer running a relay in a country that criminalises it face completely different adversaries. The tools overlap; the priorities do not. A threat model is the short written answer to "what am I defending, against whom, and how much effort is it worth?" Everything else on this site is easier to use once you have one.

> Rule of thumb: name the adversary, name the asset, and name what you are trusting. If you cannot write those three things down, you do not have a threat model yet, only a feeling.

## The five questions

The Electronic Frontier Foundation's *Surveillance Self-Defense* project frames threat modeling as five questions. They are worth answering on paper.

1. **What do I want to protect?** Your assets: messages, contacts, location, identity, files, funds, the fact that you talk to a particular person at all.
2. **Who do I want to protect it from?** Your adversaries: an abusive partner, an employer, a data broker, a local police force, a national intelligence service, a criminal gang.
3. **How bad are the consequences if I fail?** Embarrassment, a lost job, a frozen account, prison, physical harm to you or to people who trusted you.
4. **How likely is it that I will need to protect it?** A capability is not the same as an intention. Most people are not individually targeted; some are.
5. **How much trouble am I willing to go through?** Security that you abandon after a week protects nothing.

## Know what your adversary can actually do

Adversaries differ by capability, not just by motivation. Roughly, from weakest to strongest:

| Adversary | Typical capabilities | What usually stops them |
|---|---|---|
| Opportunistic attacker | Phishing, password reuse, stolen or unlocked devices | Password manager, unique passwords, hardware security keys, device encryption with a strong passcode |
| Platforms and data brokers | Everything you give them, plus tracking across sites and apps | Privacy-respecting browsers, blockers, fewer accounts, not handing over a phone number |
| Someone with physical access | Unlocked phone, laptop left open, coercion | Strong passcode, auto-lock, encrypted storage, duress or auto-reboot features |
| Local ISP or employer network | Sees which sites and services you connect to and when | Encrypted DNS, VPN or Tor, depending on who you trust more |
| Police with legal process | Compel platforms to hand over account data and metadata; seize devices | Services that hold as little as possible, end-to-end encryption, full-disk encryption, minimal stored history |
| National censor | Block IPs and domains, fingerprint protocols, throttle or shut down the network | Circumvention tools, Tor bridges, mesh and offline tools ([Censorship Circumvention](/pillars/circumvention/)) |
| Global passive adversary | Observe large parts of the internet backbone and correlate traffic timing | Mix networks with cover traffic; Tor alone is not designed to resist this ([Defending Against a Global Passive Adversary](/kb/global-passive-adversary/)) |
| Targeted attacker with exploits | Commercial spyware delivered to your phone | Hardened OS, Lockdown Mode or GrapheneOS, rapid updates, fewer apps, compartmentalised devices |

Be honest about which rows apply. Overestimating the adversary leads to unusable setups; underestimating it gets people hurt.

## Content versus metadata

Encryption protects *what* you say. It usually does not hide *that* you said it, to whom, when, from where and how often. That second category, metadata, is often what investigators and intelligence agencies actually use. A messenger can have flawless end-to-end encryption and still give a court your full contact graph. When you evaluate any tool on this site, ask both questions separately: who can read the content, and who can see the metadata? See [Metadata Resistance](/kb/metadata-resistance/) and [Map: Metadata Privacy](/kb/map-metadata-privacy/).

## Who are you trusting?

Every tool moves trust somewhere; none removes it entirely.

- A VPN moves trust from your ISP to the VPN operator.
- Tor spreads trust across three relays chosen from thousands, so that no single one sees both who you are and where you go.
- A trusted execution environment (TEE) moves trust from the cloud operator to the chip vendor and its attestation service ([Confidential Computing](/kb/confidential-computing/)).
- A hardware wallet moves trust from your laptop to the device's firmware and supply chain ([Hardware Wallets](/kb/hardware-wallets/)).
- Open-source, reproducibly built software lets other people check your trust for you; closed software asks you to take it on faith.

Write down, for each tool you adopt, who you now depend on and what happens if they are compromised, coerced or simply disappear.

## Your endpoint is the foundation

If the phone or laptop is compromised, nothing above it matters: the attacker reads your messages before they are encrypted. Start with the device. Keep it updated, use a strong passcode, remove apps you do not need and consider a hardened operating system if your adversary includes spyware vendors ([Hardening a Phone with GrapheneOS](/guides/grapheneos/), [Tails, Qubes OS and Whonix](/guides/tails-qubes-whonix/)).

## Compartmentalise

The most effective habit in operational security is separation. Keep identities that must never be linked on different devices, accounts, browsers or at least different profiles; never let them share a phone number, payment method, email address, writing style or time-of-day pattern. Assume anything you link once is linked forever.

## A worked example

An organiser in a country that monitors activists might write:

- **Assets:** member list, meeting locations, her own identity as organiser.
- **Adversaries:** local police with legal powers over domestic telecoms; possibly a national agency that buys commercial spyware.
- **Consequences:** arrest of members; that is severe.
- **Likelihood:** moderate and rising.
- **Effort budget:** high for her, low for most members.

Her plan: a dedicated phone running a hardened OS; a messenger that does not need phone numbers for the group; disappearing messages; no member list stored anywhere online; Tor Browser with bridges ready in case the network is censored; and a short, simple checklist for members rather than an ideal setup nobody follows. The tools come last, and they follow from the model.

## Revisit it

Threat models expire. Revisit yours when your work changes, when you cross a border, when laws change, or when a tool you rely on changes ownership, jurisdiction or business model.

## Where to go next

- If you are worried about surveillance of your communications, follow the [Under Surveillance](/paths/under-surveillance/) path.
- If the internet around you is censored or being shut down, follow [Behind the Firewall](/paths/behind-the-firewall/).
- If you want to hold money nobody can freeze, follow [Sovereign Money](/paths/sovereign-money/).

## Sources

- Electronic Frontier Foundation, *Surveillance Self-Defense: Your Security Plan*: <https://ssd.eff.org/module/your-security-plan>
- Privacy Guides, *Threat Modeling*: <https://www.privacyguides.org/en/basics/threat-modeling/>
- Adam Shostack, *Threat Modeling: Designing for Security* (Wiley, 2014), and the Threat Modeling Manifesto: <https://www.threatmodelingmanifesto.org/>
