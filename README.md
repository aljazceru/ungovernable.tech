# ungovernable.tech

An evolving knowledge base of building blocks for a freer internet — confidential
computing, cryptography, decentralized DNS and compute, off-grid networking,
financial sovereignty, encrypted messaging, mix networks, ZK, post-quantum, and
identity.

Live at [ungovernable.tech](https://ungovernable.tech).

## Stack

- [Astro](https://astro.build) + [Starlight](https://starlight.astro.build)
- [Pagefind](https://pagefind.app) for client-side search (built at compile time)
- Deployed to GitHub Pages via Actions
- Content authored in an [Obsidian](https://obsidian.md) vault and synced into
  `src/content/docs/` by `scripts/sync-vault.mjs`

## Local development

```sh
npm install
VAULT_PATH=/path/to/UngovernableTech npm run sync   # populate content
npm run dev                                          # http://localhost:4321
```

`npm run build` runs the sync, builds the site, and generates the Pagefind
search index.

## Contributing

Suggestions, corrections, and additions are welcome — open a PR or issue, or
ping [aljaz@nostr.si](https://nostr.at/aljaz@nostr.si).
