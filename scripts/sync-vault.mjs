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
// Files we skip
const SKIP_FILES = new Set(['README.md']);

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

  // Build basename → target path map for wikilink resolution
  const linkMap = new Map();
  const plan = [];

  for (const abs of mdFiles) {
    const rel = relative(VAULT, abs);
    const parts = rel.split('/');
    const fileName = parts.pop();
    if (SKIP_FILES.has(fileName)) continue;
    if (parts.some((p) => SKIP_DIRS.has(p))) continue;
    if (fileName.startsWith('_')) continue; // _Index.md handled below as folder index

    const folderSlug = parts.length ? folderToSlug(parts[0]) : '';
    const fileSlug = fileToSlug(fileName);
    const target = folderSlug ? `${folderSlug}/${fileSlug}` : fileSlug;

    const baseKey = fileName.replace(/\.md$/i, '');
    linkMap.set(baseKey, '/' + target);
    linkMap.set(baseKey.toLowerCase(), '/' + target);

    plan.push({ abs, rel, folderSlug, fileSlug, target, fileName });
  }

  // Also map _Index.md files to their folder root
  for (const abs of mdFiles) {
    const rel = relative(VAULT, abs);
    const parts = rel.split('/');
    if (parts.length === 2 && parts[1] === '_Index.md') {
      const folderSlug = folderToSlug(parts[0]);
      linkMap.set(parts[0], '/' + folderSlug);
    }
  }

  let written = 0;
  const copies = [];
  for (const item of plan) {
    const raw = await readFile(item.abs, 'utf8');
    const { data, body } = parseFrontmatter(raw);

    // Rewrite wikilinks: [[Page]] or [[Page|Alt]]
    let content = body.replace(/\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]+))?\]\]/g, (_m, page, alt) => {
      const key = page.trim();
      const target = linkMap.get(key) || linkMap.get(key.toLowerCase());
      const label = (alt || page).trim();
      return target ? `[${label}](${target})` : `**${label}**`;
    });

    // Drop the H1 if it duplicates the title (Starlight renders title from frontmatter)
    const rawTitle = data.title || item.fileName.replace(/\.md$/i, '').replace(/[-_]/g, ' ');
    const title = rawTitle.replace(/^\d+\s*[-—–]\s*/, '').trim();
    content = content.replace(/^\s*#\s+.+\n+/, '');

    // Compute a clean sidebar label that strips noisy prefixes.
    // "Overview - Confidential Computing" → "Overview"
    // "01 — Confidential Computing"        → "Confidential Computing"
    // Plain titles unchanged.
    const folderTitle = item.folderSlug.replace(/-/g, ' ');
    let sidebarLabel = title
      .replace(/^Overview\s*[-:–—]\s*/i, '')
      .replace(/\s*\(.*?\)\s*$/, '') // drop trailing parentheticals
      .trim();
    if (!sidebarLabel) sidebarLabel = title;

    // Hide redundant "Overview - <FolderName>" files — _Index.md serves as the
    // section's canonical overview, so listing both is duplication.
    const isRedundantOverview =
      /^Overview\s*[-:–—]/i.test(title) &&
      title.replace(/^Overview\s*[-:–—]\s*/i, '').trim().toLowerCase() === folderTitle;

    const sidebar = isRedundantOverview
      ? { hidden: true }
      : { label: sidebarLabel };

    const out = {
      title,
      description: data.description || undefined,
      ...(data.tags && data.tags.length ? { tags: data.tags } : {}),
      sidebar,
    };

    const outAbs = join(OUT, item.target + '.md');
    await mkdir(dirname(outAbs), { recursive: true });
    await writeFile(outAbs, stringifyFrontmatter(out) + content.trimStart() + '\n', 'utf8');
    written++;
  }

  // Write category index pages from _Index.md files
  for (const abs of mdFiles) {
    const rel = relative(VAULT, abs);
    const parts = rel.split('/');
    if (parts.length === 2 && parts[1] === '_Index.md') {
      const folderSlug = folderToSlug(parts[0]);
      const raw = await readFile(abs, 'utf8');
      const { data, body } = parseFrontmatter(raw);
      const content = body
        .replace(/\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]+))?\]\]/g, (_m, page, alt) => {
          const key = page.trim();
          const target = linkMap.get(key) || linkMap.get(key.toLowerCase());
          const label = (alt || page).trim();
          return target ? `[${label}](${target})` : `**${label}**`;
        })
        .replace(/^\s*#\s+.+\n+/, '');
      const rawTitle = data.title || parts[0].replace(/^\d+\s*[-_]?\s*/, '').trim();
      const title = rawTitle.replace(/^\d+\s*[-—–]\s*/, '').trim();
      const outAbs = join(OUT, folderSlug, 'index.md');
      await mkdir(dirname(outAbs), { recursive: true });
      await writeFile(
        outAbs,
        stringifyFrontmatter({
          title,
          ...(data.tags && data.tags.length ? { tags: data.tags } : {}),
          sidebar: { label: 'Overview', order: 0 },
        }) +
          content.trimStart() +
          '\n',
        'utf8',
      );
      written++;
    }
  }

  console.log(`Synced ${written} pages from ${VAULT}`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
