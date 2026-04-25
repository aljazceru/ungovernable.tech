#!/usr/bin/env node
// Syncs an Obsidian vault into src/content/docs/ for Astro Starlight.
//
// - Maps "01-Confidential-Computing" → "confidential-computing"
// - Rewrites [[Wikilinks]] using a basename → slug map
// - Strips Obsidian-specific frontmatter, keeps Starlight-friendly fields
// - Skips Templates/, attachments, and untitled drafts
//
// Configure source via VAULT_PATH env var. Defaults to a local path used in dev.

import { readFile, writeFile, mkdir, rm, readdir, stat, copyFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { join, dirname, relative, basename, extname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const VAULT = process.env.VAULT_PATH ||
  '/home/lio/s/obsidian/para/agents/UngovernableTech';
const OUT = join(ROOT, 'src', 'content', 'docs');

// Folder name → slug
function folderToSlug(name) {
  return name
    .replace(/^\d+\s*[-_]?\s*/, '')   // strip leading "01-" or "00 - "
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

// Curated, human-set section titles. Keyed by folderSlug.
const SECTION_TITLES = {
  'meta': 'Meta',
  'confidential-computing': 'Confidential Computing',
  'cryptography': 'Cryptography',
  'decentralized-dns': 'Decentralized DNS',
  'decentralized-compute': 'Decentralized Compute',
  'off-grid-networks': 'Off-Grid Networks',
  'financial-sovereignty': 'Financial Sovereignty',
  'encrypted-messaging': 'Encrypted Messaging',
  'mix-networks': 'Mix Networks',
  'zero-knowledge': 'Zero-Knowledge',
  'post-quantum': 'Post-Quantum',
  'identity': 'Identity',
};

// File basename (no .md) → slug
function fileToSlug(name) {
  return name
    .replace(/\.md$/i, '')
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

// Folders we skip entirely
const SKIP_DIRS = new Set(['Templates', 'Sources', '.obsidian', '.trash']);
// Files we skip by basename
const SKIP_FILES = new Set([
  'README.md',
  'CHANGELOG.md',           // requested: drop from Meta
  'Research Methodology.md', // requested: drop from Meta
]);
// Statuses that mark unfinished work — never publish. "draft" is allowed
// through: drafts in this vault are real, substantive notes still being
// edited, not placeholders. Only true placeholders (stub/planned/todo) skip.
const SKIP_STATUSES = new Set(['stub', 'planned', 'todo']);

function cleanTitle(s) {
  return String(s || '')
    .replace(/^\d+\s*[-—–]\s*/, '')        // "01 — Foo" → "Foo"
    .replace(/^Overview\s*[-:–—]\s*/i, '') // "Overview - Foo" → "Foo"
    .replace(/^MOC\s*[-:–—]\s*/i, '')      // "MOC - Foo" → "Foo"
    .trim();
}

// Normalize Obsidian quirks the standard markdown renderer can't handle.
// - `|| ... |` table rows (Obsidian "Advanced Tables" extension) → `| ... |`
function normalizeMarkdown(src) {
  return src
    .split('\n')
    .map((line) => {
      if (/^\s*\|\|/.test(line)) {
        return line.replace(/^(\s*)\|\|/, '$1|').replace(/\|\|\s*$/, '|');
      }
      return line;
    })
    .join('\n');
}

async function walk(dir, acc = []) {
  const entries = await readdir(dir, { withFileTypes: true });
  for (const e of entries) {
    if (e.name.startsWith('.')) continue;
    const full = join(dir, e.name);
    if (e.isDirectory()) {
      if (SKIP_DIRS.has(e.name)) continue;
      await walk(full, acc);
    } else if (e.isFile()) {
      acc.push(full);
    }
  }
  return acc;
}

// Parse simple YAML frontmatter (good enough for our vault format)
function parseFrontmatter(src) {
  const m = src.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);
  if (!m) return { data: {}, body: src };
  const data = {};
  const lines = m[1].split('\n');
  let key = null;
  let listKey = null;
  for (const line of lines) {
    if (/^\s*-\s+/.test(line) && listKey) {
      data[listKey].push(line.replace(/^\s*-\s+/, '').replace(/^["']|["']$/g, '').trim());
      continue;
    }
    listKey = null;
    const km = line.match(/^([a-zA-Z0-9_-]+):\s*(.*)$/);
    if (!km) continue;
    key = km[1];
    const val = km[2].trim();
    if (val === '') {
      data[key] = [];
      listKey = key;
    } else if (val.startsWith('[') && val.endsWith(']')) {
      data[key] = val
        .slice(1, -1)
        .split(',')
        .map((s) => s.trim().replace(/^["']|["']$/g, ''))
        .filter(Boolean);
    } else {
      data[key] = val.replace(/^["']|["']$/g, '');
    }
  }
  return { data, body: m[2] };
}

function stringifyFrontmatter(data) {
  const lines = ['---'];
  for (const [k, v] of Object.entries(data)) {
    if (v == null || v === '') continue;
    if (Array.isArray(v)) {
      if (v.length === 0) continue;
      lines.push(`${k}:`);
      for (const item of v) lines.push(`  - ${JSON.stringify(item)}`);
    } else {
      lines.push(`${k}: ${JSON.stringify(v)}`);
    }
  }
  lines.push('---', '');
  return lines.join('\n');
}

async function main() {
  if (!existsSync(VAULT)) {
    console.error(`Vault not found at ${VAULT}. Set VAULT_PATH env var.`);
    process.exit(1);
  }

  // Clean only synced category directories. Hand-authored files at the docs
  // root (e.g. index.mdx) are preserved.
  await mkdir(OUT, { recursive: true });
  const existing = await readdir(OUT, { withFileTypes: true });
  for (const e of existing) {
    if (e.isDirectory()) await rm(join(OUT, e.name), { recursive: true });
  }

  const files = await walk(VAULT);
  const mdFiles = files.filter((f) => f.toLowerCase().endsWith('.md'));

  // ── Pass 1: parse frontmatter for every file, classify, filter ──────────────
  // For each folder, choose the section-index source. Prefer `Overview - X.md`
  // (richer content in this vault), fall back to `_Index.md`. Other files are
  // regular pages.
  const parsed = [];
  for (const abs of mdFiles) {
    const rel = relative(VAULT, abs);
    const parts = rel.split('/');
    const fileName = parts.pop();
    if (SKIP_FILES.has(fileName)) continue;
    if (parts.some((p) => SKIP_DIRS.has(p))) continue;

    const raw = await readFile(abs, 'utf8');
    const { data, body } = parseFrontmatter(raw);

    if (data.status && SKIP_STATUSES.has(String(data.status).toLowerCase())) continue;

    const folder = parts[0] || '';
    const folderSlug = folder ? folderToSlug(folder) : '';
    parsed.push({ abs, rel, folder, folderSlug, fileName, data, body });
  }

  // Per-folder index selection. Priority:
  //   1. `Overview - <FolderTopic>.md`  (matches the section's actual subject)
  //   2. `_Index.md`                    (vault-style section landing)
  // Other `Overview - X.md` files (where X is a sub-topic, not the folder) are
  // treated as regular pages — they live as their own entry in the sidebar.
  const norm = (s) =>
    s.toLowerCase().replace(/[-_]+/g, ' ').replace(/\s+/g, ' ').trim();
  const indexByFolder = new Map(); // folderSlug → parsed item
  const sectionIndexAbs = new Set();
  for (const item of parsed) {
    if (!item.folderSlug) continue;
    const base = item.fileName.replace(/\.md$/i, '');
    const m = base.match(/^Overview\s*[-:–—]\s*(.+)$/i);
    if (!m) continue;
    const folderTopic = norm(item.folder.replace(/^\d+[-_]/, '').replace(/^\d+\s*[—–]\s*/, ''));
    const fileTopic = norm(m[1]);
    // Match if the file's topic equals or starts with the folder topic.
    // "Post-Quantum" folder accepts "Overview - Post-Quantum Cryptography".
    // "Identity" folder accepts "Overview - Identity & Pseudonymity".
    const matches = fileTopic === folderTopic || fileTopic.startsWith(folderTopic + ' ');
    if (matches && !indexByFolder.has(item.folderSlug)) {
      indexByFolder.set(item.folderSlug, item);
    }
  }
  for (const item of parsed) {
    if (!item.folderSlug) continue;
    if (item.fileName === '_Index.md' && !indexByFolder.has(item.folderSlug)) {
      indexByFolder.set(item.folderSlug, item);
    }
  }
  for (const v of indexByFolder.values()) sectionIndexAbs.add(v.abs);

  // ── Pass 2: build linkMap so wikilinks can resolve ──────────────────────────
  const linkMap = new Map();
  const plan = [];
  for (const item of parsed) {
    const baseKey = item.fileName.replace(/\.md$/i, '');
    if (sectionIndexAbs.has(item.abs)) {
      linkMap.set(baseKey, '/' + item.folderSlug);
      linkMap.set(baseKey.toLowerCase(), '/' + item.folderSlug);
      // Also map the parent folder name to the section
      linkMap.set(item.folder, '/' + item.folderSlug);
      continue;
    }
    if (item.fileName === '_Index.md') continue; // unused index
    if (item.fileName.startsWith('_')) continue;

    const fileSlug = fileToSlug(item.fileName);
    const target = item.folderSlug ? `${item.folderSlug}/${fileSlug}` : fileSlug;
    linkMap.set(baseKey, '/' + target);
    linkMap.set(baseKey.toLowerCase(), '/' + target);
    plan.push({ ...item, fileSlug, target });
  }

  const rewriteWikilinks = (s) =>
    normalizeMarkdown(s).replace(
      /\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]+))?\]\]/g,
      (_m, page, alt) => {
        const key = page.trim();
        const target = linkMap.get(key) || linkMap.get(key.toLowerCase());
        const label = (alt || page).trim();
        return target ? `[${label}](${target})` : `**${label}**`;
      },
    );

  // ── Pass 3: render regular pages ────────────────────────────────────────────
  let written = 0;
  for (const item of plan) {
    const content = rewriteWikilinks(item.body).replace(/^\s*#\s+.+\n+/, '');
    const title = cleanTitle(item.data.title) ||
      cleanTitle(item.fileName.replace(/\.md$/i, '').replace(/[-_]/g, ' '));

    const out = {
      title,
      description: item.data.description || undefined,
      ...(item.data.tags && item.data.tags.length ? { tags: item.data.tags } : {}),
    };

    const outAbs = join(OUT, item.target + '.md');
    await mkdir(dirname(outAbs), { recursive: true });
    await writeFile(outAbs, stringifyFrontmatter(out) + content.trimStart() + '\n', 'utf8');
    written++;
  }

  // ── Pass 4: render section index pages ──────────────────────────────────────
  for (const item of indexByFolder.values()) {
    const content = rewriteWikilinks(item.body).replace(/^\s*#\s+.+\n+/, '');
    // Section landing title = the folder's clean name (drop "Overview - " and
    // numeric prefixes), so the page heading reads "Confidential Computing"
    // rather than "Overview - Confidential Computing" or "01 — ...".
    // Section title comes from the curated map — small, deliberate, correct.
    const title = SECTION_TITLES[item.folderSlug] || cleanTitle(item.data.title);
    const outAbs = join(OUT, item.folderSlug, 'index.md');
    await mkdir(dirname(outAbs), { recursive: true });
    await writeFile(
      outAbs,
      stringifyFrontmatter({
        title,
        ...(item.data.tags && item.data.tags.length ? { tags: item.data.tags } : {}),
        sidebar: { label: 'Overview', order: 0 },
      }) + content.trimStart() + '\n',
      'utf8',
    );
    written++;
  }

  console.log(`Synced ${written} pages from ${VAULT}`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
