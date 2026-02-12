# Web of Trust

## Research
[Webs of Trust:Choosing Who to Trust on the Internet](./files/webs-of-trust-choosing-who-to-trust-on-the-internet.pdf) research paper

## Implementations

### Nostr Web of Trust

[nostr-wot-sdk](https://github.com/nostr-wot/nostr-wot-sdk) - JavaScript/TypeScript SDK for Nostr Web of Trust. Query trust distance, check network membership, and compute trust scores. Works with browser extension (recommended) or remote oracle mode for querying social distance between pubkeys.

[nostr-wot-extension](https://github.com/nostr-wot/nostr-wot-extension) - Browser extension for Nostr Web of Trust. Downloads your follow graph locally and works across all websites. Query social distance between pubkeys via remote oracle or local graph. Provides persistent, client-side trust computation without relying on centralized servers.

### Applications

[0xchat-app](https://github.com/0xchat-app/0xchat-app) - Security-focused chat application built on Nostr. Leverages Nostr's decentralized protocol for censorship-resistant, end-to-end encrypted communication.

[kukuri](https://github.com/KingYoSun/kukuri) - Fully decentralized, topic-first social app built on Nostr, iroh-gossip, and BitTorrent Mainline DHT. A Tauri desktop application that enables topic-based social sharing without relying on central servers. Uses iroh-gossip for fast event distribution and DHT-based discovery for peer connectivity, with Nostr-compatible events as the data model. Monorepo includes desktop app (React + Tauri) and community node services for P2P bootstrap/relay functionality.

