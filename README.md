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

## Publishing vault updates

After editing notes in the Obsidian vault, run:

```sh
npm run publish
```

This syncs the vault, commits the content delta with the vault's git short-SHA
in the message, and pushes. CI handles the rest.

Flags:
- `--force`   — allow committing even if there are unrelated working-tree
  changes (they'll be left untouched)
- `--no-push` — commit but don't push, in case you want to inspect first

If nothing changed under `src/content/docs/`, the script exits cleanly with
"nothing to publish".

## Contributing

Suggestions, corrections, and additions are welcome — open a PR or issue, or
ping [aljaz@nostr.si](https://nostr.at/aljaz@nostr.si).
