#!/usr/bin/env node
// Publish vault content to the live site.
//
//   npm run publish [-- --force] [-- --no-push]
//
// Steps:
//   1. Refuse if the working tree has uncommitted code changes outside
//      src/content/docs/ (use --force to override).
//   2. Run the vault sync.
//   3. If nothing changed under src/content/docs/, exit 0 with a no-op message.
//   4. Otherwise: stage src/content/docs/ only, commit with a message that
//      includes the vault's git short-SHA when available, and push.

import { execSync, spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const VAULT = process.env.VAULT_PATH || '/home/lio/s/obsidian/para/agents/UngovernableTech';
const CONTENT_PREFIX = 'src/content/docs/';

const args = process.argv.slice(2);
const FORCE = args.includes('--force');
const NO_PUSH = args.includes('--no-push');

function sh(cmd) {
  return execSync(cmd, { cwd: ROOT, encoding: 'utf8' }).trim();
}

function run(cmd) {
  execSync(cmd, { cwd: ROOT, stdio: 'inherit' });
}

function shTry(cmd) {
  try { return sh(cmd); } catch { return null; }
}

function preflight() {
  // Don't trim — porcelain lines start with a status prefix ("XY ") where X
  // or Y can be a literal space. Trimming the first space would shift the
  // path slice off by one.
  const raw = execSync('git status --porcelain', { cwd: ROOT, encoding: 'utf8' });
  const dirtyOutsideContent = raw
    .split('\n')
    .filter(Boolean)
    .map((line) => line.slice(3))
    .filter((p) => p && !p.startsWith(CONTENT_PREFIX));
  if (dirtyOutsideContent.length && !FORCE) {
    console.error('refusing to publish: uncommitted changes outside content:');
    for (const p of dirtyOutsideContent) console.error('  ' + p);
    console.error('\ncommit or stash them first, or pass --force to bundle them.');
    process.exit(1);
  }
}

function vaultRef() {
  if (!existsSync(join(VAULT, '.git'))) return null;
  const sha = shTry(`git -C "${VAULT}" rev-parse --short HEAD`);
  return sha || null;
}

function main() {
  preflight();

  console.log('▸ syncing vault → src/content/docs/');
  spawnSync('node', ['scripts/sync-vault.mjs'], { cwd: ROOT, stdio: 'inherit' });

  sh(`git add ${CONTENT_PREFIX}`);
  const staged = shTry('git diff --cached --quiet');
  // git diff --cached --quiet returns exit 1 when there are staged changes;
  // shTry returns null in that case (which is what we want — there is a diff).
  if (staged === '') {
    console.log('✓ nothing to publish — content is up to date.');
    return;
  }

  const sha = vaultRef();
  const msg = sha ? `content: sync vault @ ${sha}` : 'content: sync vault';
  run(`git commit -m "${msg}"`);
  console.log(`✓ committed: ${msg}`);

  if (NO_PUSH) {
    console.log('skipping push (--no-push). run `git push` when ready.');
    return;
  }
  console.log('▸ pushing…');
  run('git push');
  console.log('✓ pushed. CI will rebuild and deploy.');
}

main();
