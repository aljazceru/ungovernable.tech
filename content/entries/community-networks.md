---
title: "Community Networks"
slug: community-networks
type: explainer
pillars: [mesh]
description: "Internet access can be built and owned by the people who use it. How community networks like Guifi.net, Freifunk and NYC Mesh work, and how to start one."
dek: "Connectivity does not have to come from a telco. Community networks are internet infrastructure built, owned and governed by the people who use it."
updated: 2026-10-18
created: 2026-10-18
origin: original
related: [off-grid-networks, building-a-mesh, running-freedom-infrastructure, resilient-infrastructure, reticulum, internet-shutdown-preparedness]
---

Most people reach the internet through a handful of commercial providers who own the wires, set the prices, keep the logs and can be ordered to cut you off. A **community network** is the alternative: internet infrastructure that the users build, own and govern themselves, as a commons rather than a product. These are not toy meshes — some have been running for two decades and carry tens of thousands of real users — and they are the most mature answer to the question of who controls access at the physical layer.

## How they work

Community networks are usually built from ordinary off-the-shelf radios and fibre, assembled bottom-up:

- **Rooftop links.** Members mount Wi-Fi or point-to-point radios on rooftops with line of sight to a neighbour, forming a mesh or a tree of high-capacity links across a city or valley.
- **Supernodes and backhaul.** A few well-placed, well-connected nodes aggregate traffic and connect the community network to the wider internet, often by sharing one or more donated or jointly-bought uplinks.
- **Peering, not customers.** Participants agree to carry each other's traffic under a shared pact. In [Guifi.net](https://guifi.net/) this is codified as a "network commons licence" that anyone may join as long as they relay others' traffic in turn.
- **Open firmware.** Routers typically run community firmware — [LibreMesh](https://libremesh.org/) or Freifunk's [Gluon](https://gluon.readthedocs.io/) on top of [OpenWrt](https://openwrt.org/) — so the whole stack is auditable and the network is not at the mercy of a vendor.

The result is infrastructure with no single owner to coerce, cut off or surveil wholesale, and whose coverage grows wherever a member is willing to put up an antenna.

## Who is doing it

- **[Guifi.net](https://guifi.net/)** (Catalonia, since 2004) is the largest, with tens of thousands of active nodes and its own commons governance and economic model ([overview](https://en.wikipedia.org/wiki/Guifi.net)).
- **[Freifunk](https://freifunk.net/)** is a decentralized German movement of hundreds of local community networks sharing the Gluon firmware.
- **[NYC Mesh](https://www.nycmesh.net/)** is a volunteer-run network bringing cheap, neutral connectivity to New York City via rooftop installs and a few supernodes.
- **[AlterMundi](https://altermundi.net/)** builds community networks in rural Argentina and co-develops LibreMesh.

The engineers behind these projects meet and interoperate through gatherings like the [Wireless Battle of the Mesh](https://www.battlemesh.org/), and the model is recognized as legitimate infrastructure by bodies such as the [Internet Society](https://www.internetsociety.org/issues/community-networks/).

## Why it matters for sovereignty

A community network changes who holds the leverage over the physical layer:

- **Resilience.** Local traffic stays local and keeps flowing even when upstream links or the national internet are disrupted — a direct complement to [shutdown preparedness](/guides/internet-shutdown-preparedness/) and [off-grid networks](/kb/off-grid-networks/).
- **No central chokepoint.** There is no single company to serve with a blocking or logging order for the whole network.
- **Affordability and reach.** Communities underserved by commercial providers get connectivity at cost.
- **Auditable by design.** Open firmware means the people running it can see and change what it does.

## Starting or joining one

- **Join first.** If a Freifunk, Guifi or similar network already covers your area, putting up a node is the fastest contribution; the hard parts (backhaul, governance, firmware) are already solved.
- **Start small.** A single rooftop link between two willing neighbours is a working community network; growth is incremental.
- **Use community firmware.** LibreMesh and Gluon are built for exactly this and spare you from reinventing mesh routing and configuration.
- **Agree the rules early.** The durable networks all have an explicit peering pact covering who carries whose traffic, how uplinks are funded, and how disputes are handled.

For the radio and hardware details of building the links themselves, see [Building a Local Mesh Network](/guides/building-a-mesh/); for running the servers and relays a community depends on, see [Resilient and Relocatable Infrastructure](/guides/resilient-infrastructure/) and [Running Infrastructure for Freedom](/guides/running-freedom-infrastructure/).
