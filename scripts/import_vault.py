#!/usr/bin/env python3
"""Import the research vault into content/ (entries, briefings, glossary, sources).

Reads scripts/vault_map.yml (the editorial map), transforms the Obsidian
markdown into site markdown (wikilinks resolved to site URLs, vault-internal
sections dropped, callouts and highlights converted), and writes:

  content/entries/<slug>.md            one file per mapped entry (origin: vault)
  content/briefings/<series>/<date>.md dated weekly briefings
  content/glossary.yml                 terms from 00 - Meta/Glossary.md
  content/sources.md                   Sources/Sources.md with links resolved
  scripts/vault_state.json             the vault HEAD commit used
  scripts/IMPORT_REPORT.md             counts and content problems found

Hand-written pages (origin: original) are never overwritten or deleted.
Running twice produces no diff.

Usage: python3 scripts/import_vault.py --vault /path/to/vault [--dry-run]
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP_PATH = os.path.join(ROOT, 'scripts', 'vault_map.yml')

# ---------------------------------------------------------------- constants

# vault folder number -> pillar key (for [[NN-Folder]] and [[NN-Folder/_Index]])
FOLDER_PILLAR = {
    '01': 'confidential', '02': 'cryptography', '03': 'naming', '04': 'compute',
    '05': 'mesh', '06': 'money', '07': 'messaging', '08': 'anonymity', '09': 'zk',
    '10': 'pqc', '11': 'identity', '12': 'storage', '13': 'cryptography',
}

# H2 sections that are vault navigation, not article content
DROP_HEAD = re.compile(
    r'^(related files|cross-references|vault section status|'
    r'next steps for ungovernable\.tech|status|see also)\b', re.I)
DROP_HEAD_BRIEF = re.compile(r'^(open questions|watches|standing-watch)\b', re.I)

# vault-internal language -> library language (ordered; lowercase "vault" only)
VAULT_LANG = [
    ('For the vault:', 'Why it matters:'),
    ('in the vault', 'in this library'),
    ('this vault', 'this library'),
    ('the vault', 'this library'),
    ("vault's", "library's"),
]

WIKILINK = re.compile(r'\[\[([^\]]+?)\]\]')

# Wikilink targets that have no mapped vault note but a good real-world home:
# existing site pages, briefings, or authoritative external URLs (all verified
# to return 200 at authoring time). Keyed by the wikilink's final name segment.
WIKILINK_OVERRIDES = {
    # existing site entries / pillars / briefings
    'FROST': '/kb/threshold-signatures/',
    'Hardware Signers': '/kb/hardware-wallets/',
    'World ID': '/kb/proof-of-personhood/',
    'Worldcoin': '/kb/proof-of-personhood/',
    'Nostr-WoT': '/kb/nostr-web-of-trust/',
    'Nostr-WoT extension': '/kb/nostr-web-of-trust/',
    'nostr-wot-extension': '/kb/nostr-web-of-trust/',
    'bunker 1.0.0': '/kb/remote-signing/',
    'ENS Foundation': '/kb/ens/',
    'Cryptographic Agility': '/kb/hybrid-kem-migration/',
    'nym.com/blog/nymvpn-network-upgrade': 'https://nym.com/blog/nymvpn-network-upgrade',
    'Identity': '/pillars/identity/',
    'Migration Plan — PQ Encryption for Existing Nostr-Clients': '/pillars/pqc/',
    'Post-Quantum Saturday': '/briefings/post-quantum/',
    'Post-Quantum Saturday — August 29 2026 Weekly Update': '/briefings/post-quantum/',
    'Identity Sunday — September 13 2026 Weekly Update': '/briefings/identity/2026-09-13/',
    'WoT Thursday — September 03 2026 Weekly Update': '/briefings/web-of-trust/2026-09-03/',
    # authoritative external URLs
    'NIPs': 'https://github.com/nostr-protocol/nips',
    'NIP-17 key-decoupling proposal (fiatjaf)': 'https://github.com/nostr-protocol/nips/blob/master/17.md',
    'NIP-42': 'https://github.com/nostr-protocol/nips/blob/master/42.md',
    'NIP-45': 'https://github.com/nostr-protocol/nips/blob/master/45.md',
    'NIP-78': 'https://github.com/nostr-protocol/nips/blob/master/78.md',
    'NIP-89': 'https://github.com/nostr-protocol/nips/blob/master/89.md',
    'NIP-90': 'https://github.com/nostr-protocol/nips/blob/master/90.md',
    'NIP-A3': 'https://github.com/nostr-protocol/nips/blob/master/A3.md',
    'NIP-AC': 'https://github.com/nostr-protocol/nips',
    'NIP-F4 podcasts': 'https://github.com/nostr-protocol/nips/blob/master/F4.md',
    'Amethyst': 'https://github.com/vitorpamplona/amethyst',
    'Amber': 'https://github.com/greenart7c3/Amber',
    'Citrine': 'https://github.com/greenart7c3/Citrine',
    'Damus': 'https://damus.io',
    'Coracle': 'https://coracle.social',
    'Ditto': 'https://github.com/soapbox-pub/ditto',
    'Mostro': 'https://mostro.network',
    'Iris Stack': 'https://iris.to',
    'Arti': 'https://tpo.pages.torproject.net/core/arti/',
    'liboqs': 'https://github.com/open-quantum-safe/liboqs',
    'mldsa-native': 'https://github.com/pq-code-package/mldsa-native',
    'ENSIP-28 Name Owned Accounts': 'https://docs.ens.domains/ensip/28',
    'ENSIP-31 Payment Preferences': 'https://docs.ens.domains/ensip/31',
    'W3C': 'https://www.w3.org',
    'uWebSockets': 'https://github.com/uNetworking/uWebSockets',
    'strfry': 'https://github.com/hoytech/strfry',
    'Farcaster': 'https://www.farcaster.xyz',
    'Nous Research': 'https://nousresearch.com',
    'BobWallet': 'https://github.com/kyokan/bob-wallet',
    'ngit-cli': 'https://github.com/DanConwayDev/ngit-cli',
}

# Wikilink targets deliberately rendered as plain prose (no accurate link
# target exists): ambiguous code symbols, draft notes, numeric fragments.
WIKILINK_PLAIN = {
    'MOCHA', 'Outfox', 'Lewes Protocol', 'DNS-AID', 'KSK', 'DCP', 'MDK',
    'Disclosure', 'relayer', 'FiltersCounter', 'Chama', 'Clave', 'CHANGELOG',
    'Nomentum Labs Grails SPP3 Marketplace RFP',
    'Endowment permissions to KPK Update', 'open', '42',
    '300,60,14', '540,108,18', '975, 195, ≤24', '975,195,≤24',
}

_WL_OVR_CI = {k.lower(): v for k, v in WIKILINK_OVERRIDES.items()}

# Persistent editorial cross-links appended to generated vault entries, so
# they survive importer re-runs without hand-editing the generated files.
# Keyed by entry slug; value is markdown appended as a final paragraph.
ENTRY_APPEND = {
    'metadata-resistance': 'For the specific technique of hiding *when* and '
        '*how much* you send, see [Cover Traffic and Constant-Rate Padding]'
        '(/kb/cover-traffic/).',
    'off-grid-networks': 'For internet access built and owned by its users '
        'rather than a telco, see [Community Networks](/kb/community-networks/).',
}

_WL_PLAIN_CI = {k.lower() for k in WIKILINK_PLAIN}


def wikilink_override(name):
    """-> ('url', url) | ('plain', None) | None for a wikilink name segment."""
    n = (name or '').strip()
    if n in WIKILINK_OVERRIDES:
        return 'url', WIKILINK_OVERRIDES[n]
    if n in WIKILINK_PLAIN:
        return 'plain', None
    nl = n.lower()
    if nl in _WL_OVR_CI:
        return 'url', _WL_OVR_CI[nl]
    if nl in _WL_PLAIN_CI:
        return 'plain', None
    return None

HEADING_DATE = re.compile(r'([A-Z][a-z]+) (\d{1,2}) (\d{4})')
MONTHS = {m: i for i, m in enumerate(
    ['January', 'February', 'March', 'April', 'May', 'June', 'July',
     'August', 'September', 'October', 'November', 'December'], 1)}


def slugify(t):
    s = re.sub(r'[^a-z0-9]+', '-', str(t).lower()).strip('-')
    return re.sub(r'-+', '-', s)[:60]


def norm_date(d):
    """Vault frontmatter dates arrive as date objects or strings; normalise."""
    if d is None:
        return None
    if isinstance(d, (datetime.date, datetime.datetime)):
        return d.strftime('%Y-%m-%d')
    s = str(d).strip()
    m = re.match(r'^(\d{4})-(\d{2})-(\d{2})', s)
    if m:
        return m.group(0)
    return s


def yq(s):
    """Quote a string for hand-written YAML frontmatter (JSON quoting is valid YAML)."""
    return json.dumps(str(s), ensure_ascii=False)


def ylist(items):
    return '[' + ', '.join(yq(i) for i in items) + ']'


# ---------------------------------------------------------------- vault model

class Vault:
    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.notes = {}          # rel path (posix) -> raw text
        for root, dirs, files in os.walk(self.path):
            if '.git' in root.split(os.sep):
                continue
            for f in files:
                if f.endswith('.md'):
                    p = os.path.join(root, f)
                    rel = os.path.relpath(p, self.path).replace(os.sep, '/')
                    self.notes[rel] = open(p, encoding='utf-8').read()
        self.head = self._git_head()

    def _git_head(self):
        try:
            r = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=self.path,
                               capture_output=True, text=True)
            return r.stdout.strip() or None
        except OSError:
            return None


def parse_note(text):
    m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    if not m:
        return {}, text
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        fm = {}
    return fm, text[m.end():]


# ---------------------------------------------------------------- link index

class LinkIndex:
    """Resolves [[wikilink]] targets to site URLs."""

    def __init__(self, vmap, vault):
        self.entries = {}      # vault path -> entry spec
        self.brief_specs = vmap.get('briefings') or []
        self.vault = vault
        for path, spec in (vmap.get('entries') or {}).items():
            self.entries[path] = dict(spec, path=path)
        # stem -> paths (two basenames are duplicated across folders)
        self.stem_paths = defaultdict(list)
        for path in self.entries:
            stem = os.path.basename(path)[:-3]
            self.stem_paths[stem].append(path)
        # duplicated basenames: prefer the 13-/11- folder versions by default
        self.stem_prefer = {}
        for stem, paths in self.stem_paths.items():
            if len(paths) > 1:
                for p in paths:
                    if p.split('/')[0].split('-')[0] in ('13', '11'):
                        self.stem_prefer[stem] = p
        # briefing notes: stem -> (series, date, title, path)
        self.briefings = {}
        for rel, text in vault.notes.items():
            stem = os.path.basename(rel)[:-3]
            spec = self._brief_match(stem)
            if spec:
                fm, _ = parse_note(text)
                date = norm_date(fm.get('created')) or self._date_from_title(stem)
                self.briefings[stem] = {'series': spec['series'], 'date': date,
                                        'title': fm.get('title') or stem, 'path': rel}
        # aliases / titles of mapped entries -> path (lowercase key)
        self.aliases = {}
        for path, spec in self.entries.items():
            fm, _ = parse_note(vault.notes.get(path, ''))
            names = []
            if fm.get('title'):
                names.append(str(fm['title']))
            for a in (fm.get('aliases') or []):
                names.append(str(a))
            for n in names:
                self.aliases.setdefault(n.strip().lower(), path)

    def _brief_match(self, stem):
        for spec in self.brief_specs:
            if re.match(spec['pattern'], stem):
                return spec
        return None

    @staticmethod
    def _date_from_title(stem):
        m = HEADING_DATE.search(stem)
        if m and m.group(1) in MONTHS:
            return '%04d-%02d-%02d' % (int(m.group(3)), MONTHS[m.group(1)], int(m.group(2)))
        return None

    # -- resolution ------------------------------------------------------

    def entry_url(self, spec):
        if spec['type'] == 'guide':
            return '/guides/%s/' % spec['slug']
        return '/kb/%s/' % spec['slug']

    @staticmethod
    def folder_key(folder):
        """'08-Mix-Networks' / '08 - Mix Networks' -> '08'."""
        m = re.match(r'\s*(\d+)', folder)
        return m.group(1).zfill(2) if m else None

    def resolve(self, target):
        """-> ('url', url) | ('text',) unresolved; plus display text decided by caller."""
        t = target.split('#')[0].strip()
        if t.endswith('.md'):
            t = t[:-3]
        folder, name = (t.split('/', 1) + [''])[:2] if '/' in t else ('', t)
        name = name.strip()
        if not name and not folder:
            return None
        # vault meta notes
        if name in ('Glossary',) and not folder:
            return 'url', '/glossary/'
        if name in ('Sources',) and not folder:
            return 'url', '/sources/'
        if name == 'Research Methodology' and not folder:
            return 'url', '/method/'
        if name == 'README' and not folder:
            return 'url', '/about/'
        if name == 'CHANGELOG' and not folder:
            return 'plain', None
        fkey = self.folder_key(folder) if folder else None
        if not fkey and re.match(r'^\d+\s*-\s*\S', name):
            # [[08-Mix-Networks]] / [[08 - Mix Networks]]: a section folder link
            fkey = self.folder_key(name)
        if fkey:
            pillar = FOLDER_PILLAR.get(fkey)
            if pillar and name in ('', '_Index', '_index', 'Index'):
                return 'url', '/pillars/%s/' % pillar
            if pillar and fkey and not folder and self.folder_key(name) == fkey:
                return 'url', '/pillars/%s/' % pillar
        # mapped entries: exact stem, honouring folder hints
        if name in self.stem_paths:
            paths = self.stem_paths[name]
            path = None
            if fkey:
                path = next((p for p in paths if self.folder_key(p.split('/')[0]) == fkey), None)
            if path is None and len(paths) > 1:
                path = self.stem_prefer.get(name, sorted(paths)[0])
            elif path is None:
                path = paths[0]
            return 'url', self.entry_url(self.entries[path])
        # briefing notes
        if name in self.briefings:
            b = self.briefings[name]
            return 'url', '/briefings/%s/%s/' % (b['series'], b['date'])
        # briefing notes referenced by a shortened series name ("Identity Sunday — …")
        if len(name) > 12:
            hits = {(b['series'], b['date']) for s, b in self.briefings.items()
                    if (s.endswith(name) or name.endswith(s))
                    and (not fkey or self.folder_key(b['path'].split('/')[0]) == fkey)}
            if len(hits) == 1:
                s, d = next(iter(hits))
                return 'url', '/briefings/%s/%s/' % (s, d)
        # aliases and vault titles of mapped entries
        if not folder:
            p = self.aliases.get(name.lower())
            if p:
                return 'url', self.entry_url(self.entries[p])
        ov = wikilink_override(name) or wikilink_override(t)
        if ov:
            return ov
        return 'text', None


# ---------------------------------------------------------------- transforms

def strip_wikilinks_text(s):
    """[[Note|Alias]] -> Alias for display text."""
    def sub(m):
        t = m.group(1).split('#')[0]
        if '|' in t:
            t = t.split('|', 1)[1]
        else:
            t = t.rsplit('/', 1)[-1]
            if t.endswith('.md'):
                t = t[:-3]
        return t.strip()
    return WIKILINK.sub(sub, s)


def vault_lang(s):
    for a, b in VAULT_LANG:
        s = s.replace(a, b)
    return s


def plain_md(s):
    """Markdown-ish text -> plain text (links, marks, emphasis)."""
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'\1', s)
    s = re.sub(r'\*([^*]+)\*', r'\1', s)
    s = re.sub(r'`([^`]+)`', r'\1', s)
    s = strip_wikilinks_text(s)
    return ' '.join(s.split())


def split_sentences(text):
    """Sentence split that does not break on '1. Word' list numbering."""
    frags = [s for s in re.split(r'(?<=[.!?])\s+', text.strip()) if s]
    out = []
    for f in frags:
        if out and re.search(r'(?<!\S)\d{1,2}\.$', out[-1]) and f[:1].isupper():
            out[-1] = out[-1] + ' ' + f
        else:
            out.append(f)
    return out


def make_description(pool, log, slug):
    """Meta description: 70-160 chars, ends with a full stop, cut at a boundary."""
    sents = []
    for p in pool:
        sents.extend(split_sentences(p))
    # whole sentences first: stop as soon as we are >= 70 chars
    acc = ''
    for s in sents:
        cand = (acc + ' ' + s).strip() if acc else s
        if len(cand) > 160:
            break
        acc = cand
        if len(acc) >= 70:
            return acc.replace('"', '')
    # first sentence too long (or all too short): accumulate clause atoms
    atoms = []
    for s in sents:
        atoms.extend(re.split(r'(?<=[,;:])\s+|(?<=\s)[—–]\s+', s))
    acc = ''
    for a in atoms:
        cand = (acc + ' ' + a).strip() if acc else a
        if len(cand) > 160:
            break
        acc = cand
        if len(acc) >= 70:
            break
    acc = acc.rstrip(' ,;:—–')
    if not (70 <= len(acc) <= 160):
        # last resort: hard word cut of the full text
        text = ' '.join(sents)
        acc = text[:157].rsplit(' ', 1)[0].rstrip(' ,;:—–')
        for _ in range(3):
            if acc.rsplit(' ', 1)[-1].lower() in ('and', 'or', 'with', 'for', 'that', 'of', 'to', 'a', 'an', 'the', 'in', 'on'):
                acc = acc.rsplit(' ', 1)[0]
            else:
                break
    if not acc.endswith('.'):
        acc += '.'
    log.append(slug)
    return acc.replace('"', '')


COMMENT = re.compile(r'<!--.*?-->', re.S)
CALLOUT = re.compile(r'^> ?\[!([a-z-]+)\]([^\n]*)$')


def transform_body(body, index, drop_extra=None):
    """Vault markdown -> site markdown. Returns (body, dek, unresolved_counter)."""
    unresolved = Counter()
    lines = body.split('\n')

    # strip HTML comments (may span lines)
    body = COMMENT.sub('', '\n'.join(lines))
    lines = body.split('\n')

    # drop the first H1
    for i, l in enumerate(lines):
        if l.strip():
            if l.startswith('# '):
                lines = lines[i + 1:]
            break

    # italic one-line summary -> dek
    dek = None
    for i, l in enumerate(lines):
        s = l.strip()
        if not s:
            continue
        if re.match(r'^\*[^*\n]+\*$', s):
            dek = strip_wikilinks_text(s[1:-1]).strip()
            lines = lines[:i] + lines[i + 1:]
        break
    # drop vault-internal H2 sections
    drop_re = DROP_HEAD
    if drop_extra:
        drop_re = re.compile(DROP_HEAD.pattern + '|' + drop_extra.pattern, re.I)
    out, dropping = [], False
    for l in lines:
        if l.startswith('## '):
            dropping = bool(drop_re.match(l[3:].strip()))
            if dropping:
                continue
        if not dropping:
            out.append(l)
    lines = out

    # vault-internal language
    text = '\n'.join(lines)
    for a, b in VAULT_LANG:
        text = text.replace(a, b)
    lines = text.split('\n')
    if dek:
        dek = vault_lang(dek)

    # drop decorative '---' separators (they would render as setext headings)
    lines = [l for i, l in enumerate(lines)
             if not (re.match(r'^(-{3,}|\*{3,}|_{3,})$', l.strip()) )]

    # wikilinks, callouts, highlights outside code fences
    out = []
    fence = False
    callout = None  # (kind, title, buf_lines)
    for l in lines:
        if l.lstrip().startswith('```'):
            fence = not fence
            out.append(l)
            continue
        if fence:
            out.append(l)
            continue
        m = CALLOUT.match(l)
        if m and callout is None:
            callout = (m.group(1).lower(), m.group(2).strip(), [])
            continue
        if callout is not None:
            if l.startswith('>'):
                callout[2].append(re.sub(r'^> ? ?', '', l))
                continue
            out.extend(render_callout(callout, index, unresolved))
            callout = None
        l = re.sub(r'==([^=\n]+)==', r'<mark>\1</mark>', l)
        out.append(resolve_line(l, index, unresolved))
    if callout is not None:
        out.extend(render_callout(callout, index, unresolved))

    # collapse >2 consecutive blank lines
    body = re.sub(r'\n{3,}', '\n\n', '\n'.join(out)).strip() + '\n'
    return body, dek, unresolved


MDLINK = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')


def resolve_line(l, index, unresolved):
    """Resolve [[wikilinks]] and vault-relative [label](note.md) links."""
    def sub(m):
        target = m.group(1)
        alias = None
        if '|' in target:
            target, alias = target.split('|', 1)
        target = target.strip()
        alias = (alias or '').strip()
        stem_text = strip_wikilinks_text('[[' + target + ']]')
        disp = alias or stem_text
        if not target.split('#')[0].strip():
            return disp
        r = index.resolve(target)
        if r and r[0] == 'url':
            return '[%s](%s)' % (disp, r[1])
        if r and r[0] == 'plain':
            return disp or stem_text
        unresolved[re.sub(r'\.md$', '', target.split('#')[0].rsplit('/', 1)[-1])] += 1
        return disp or stem_text

    def sub_md(m):
        label, url = m.group(1), m.group(2)
        if re.match(r'^[a-z][a-z0-9+.-]*:', url, re.I):
            return m.group(0)                     # absolute URL: leave alone
        if url.startswith(('#', '/',)):
            return m.group(0)                     # site/fragment link: build handles
        if url.startswith('./files'):
            return '[%s](/files%s)' % (label, url[7:])
        import urllib.parse
        name = urllib.parse.unquote(url)
        r = index.resolve(name) or index.resolve(name.rsplit('#', 1)[0])
        if r and r[0] == 'url':
            return '[%s](%s)' % (label, r[1])
        if r and r[0] == 'plain':
            return label
        unresolved[re.sub(r'\.md$', '', name.rsplit('/', 1)[-1].split('#')[0])] += 1
        return label                              # unwrap dead vault links

    l = WIKILINK.sub(sub, l)
    l = MDLINK.sub(sub_md, l)
    # remaining '[['/']]' are literal double-bracket tags in source text
    return l.replace('[[', '[').replace(']]', ']')


def render_callout(callout, index, unresolved):
    import markdown
    kind, title, buf = callout
    inner = markdown.markdown('\n'.join(buf), extensions=['tables', 'fenced_code', 'sane_lists'])
    inner = resolve_line(inner, index, unresolved)
    h = ['<aside class="callout callout-%s">' % kind]
    if title:
        h.append('<p class="callout-title">%s</p>' % title)
    h.append(inner)
    h.append('</aside>')
    return h


def first_paragraph(body_md):
    """First non-heading, non-fence paragraph as markdown text."""
    paras = []
    cur = []
    fence = False
    for l in body_md.split('\n'):
        if l.lstrip().startswith('```'):
            fence = not fence
            cur.append(l)
            continue
        if fence:
            cur.append(l)
            continue
        if not l.strip():
            if cur:
                paras.append('\n'.join(cur))
                cur = []
            continue
        if l.startswith('#') or l.startswith('<aside') or l.startswith('|'):
            if cur:
                paras.append('\n'.join(cur))
                cur = []
            continue
        cur.append(l)
    if cur:
        paras.append('\n'.join(cur))
    for p in paras:
        t = plain_md(p)
        if len(t) > 40:
            return t
    return ''


# ---------------------------------------------------------------- briefings

def briefing_description(body, window, date, log, key):
    """'Weekly briefing for <window>: <first headline sentence>.' <= 160 chars."""
    tldr = ''
    m = re.search(r'^## (TL;DR|TL;DR — .*?)\s*$(.*?)(?=^## |\Z)', body, re.S | re.M)
    if m:
        tldr = plain_md(m.group(2))
    if not tldr:
        # no TL;DR section: use the first substantive paragraph
        tldr = first_paragraph(body)
    first = split_sentences(tldr)[0] if tldr else ''
    first = re.sub(r'^[-*]\s*', '', first)
    first = re.sub(r'^\d{1,2}\.\s+', '', first)
    win = window or ('the week of %s' % date)
    if not first:
        first = title
    d = 'Weekly briefing for %s: %s' % (win, first)
    if len(d) > 160:
        # trim the headline sentence at a word boundary
        room = 160 - len('Weekly briefing for %s: ' % win) - 1
        cut = first[:max(40, room)].rsplit(' ', 1)[0].rstrip(' ,;:')
        d = 'Weekly briefing for %s: %s.' % (win, cut)
    if not d.endswith('.'):
        d += '.'
    if not (70 <= len(d) <= 160):
        log.append(key)
    return d


# ---------------------------------------------------------------- glossary

def parse_glossary(text, index, unresolved):
    fm, body = parse_note(text)
    terms = []
    for l in body.split('\n'):
        s = l.strip()
        m = re.match(r'^\*\*(.+?)\*\*\s*[—–-]\s*(.+)$', s)
        if not m:
            continue
        term = m.group(1).strip()
        definition = m.group(2).strip()
        see = []
        def sub(mm):
            target = mm.group(1)
            alias = None
            if '|' in target:
                target, alias = target.split('|', 1)
            target, alias = target.strip(), (alias or '').strip()
            disp = alias or strip_wikilinks_text('[[' + target + ']]')
            r = index.resolve(target)
            if r and r[0] == 'url':
                for path, spec in index.entries.items():
                    if index.entry_url(spec) == r[1]:
                        see.append(spec['slug'])
                return '[%s](%s)' % (disp, r[1])
            if r and r[0] == 'plain':
                return disp
            unresolved[target] += 1
            return disp
        definition_md = WIKILINK.sub(sub, definition)
        terms.append({'term': term, 'slug': slugify(term),
                      'definition_md': definition_md, 'see': see})
    return terms


# ---------------------------------------------------------------- main

def emit_entry_fm(e):
    fm = ['---',
          'title: %s' % yq(e['title']),
          'slug: %s' % e['slug'],
          'type: %s' % e['type'],
          'pillars: %s' % ylist(e['pillars'])]
    if e.get('readiness'):
        fm.append('readiness: %s' % e['readiness'])
    fm.append('description: %s' % yq(e['description']))
    fm.append('dek: %s' % yq(e['dek']))
    if e.get('updated'):
        fm.append('updated: %s' % e['updated'])
    if e.get('created'):
        fm.append('created: %s' % e['created'])
    fm.append('origin: vault')
    fm.append('source: %s' % yq(e['source']))
    if e.get('aliases'):
        fm.append('aliases: %s' % ylist(e['aliases']))
    if e.get('tags'):
        fm.append('tags: %s' % ylist(e['tags']))
    fm.append('---')
    return '\n'.join(fm) + '\n\n'


def clean_title(t):
    t = str(t).strip()
    return re.sub(r'^Overview\s*[-—–]\s*', '', t)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--vault', required=True)
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()

    vmap = yaml.safe_load(open(MAP_PATH, encoding='utf-8'))
    vault = Vault(a.vault)
    index = LinkIndex(vmap, vault)

    writes = {}   # rel output path -> content
    stats = {'entries': Counter(), 'types': Counter(), 'readiness': Counter(),
             'briefings': Counter()}
    unresolved_all = Counter()
    synthesized = []
    no_sources = []
    brief_keep = {}  # (series, date) -> (size, filename, content)

    _dp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'descriptions.yml')
    HAND_DESCRIPTIONS = (yaml.safe_load(open(_dp, encoding='utf-8')) or {}) if os.path.exists(_dp) else {}
    # ---- entries ---------------------------------------------------------
    for path in sorted(index.entries):
        spec = index.entries[path]
        if path not in vault.notes:
            print('WARN: mapped note missing in vault: %s' % path, file=sys.stderr)
            continue
        fm, raw = parse_note(vault.notes[path])
        body, dek, unresolved = transform_body(raw, index)
        body = re.sub(r'\b([Aa])s of this run\b', lambda m: ('A' if m.group(1) == 'A' else 'a') + 't last review', body)
        unresolved_all.update(unresolved)
        title = clean_title(spec.get('title') or fm.get('title') or os.path.basename(path)[:-3])
        first_para = first_paragraph(body)
        if not dek:
            dek = split_sentences(first_para)[0] if first_para else title
        pool = [dek] + ([first_para] if plain_md(first_para) != plain_md(dek) else [])
        description = HAND_DESCRIPTIONS.get(spec['slug']) or \
            make_description([plain_md(p) for p in pool if p], synthesized, spec['slug'])
        if 'http' not in body:
            no_sources.append(title)
        e = {
            'title': title,
            'slug': spec['slug'],
            'type': spec['type'],
            'pillars': spec['pillars'],
            'readiness': spec.get('readiness'),
            'description': description,
            'dek': dek,
            'updated': norm_date(fm.get('updated')) or norm_date(fm.get('created')),
            'created': norm_date(fm.get('created')),
            'source': path,
            'aliases': [str(x) for x in (fm.get('aliases') or [])],
            'tags': [str(x) for x in (fm.get('tags') or [])],
        }
        body_out = body.strip()
        extra = ENTRY_APPEND.get(spec['slug'])
        if extra and extra not in body_out:
            body_out = body_out + '\n\n' + extra
        writes[os.path.join('content', 'entries', spec['slug'] + '.md')] = \
            emit_entry_fm(e) + body_out + '\n'
        for p in spec['pillars']:
            stats['entries'][p] += 1
        stats['types'][spec['type']] += 1
        if spec.get('readiness'):
            stats['readiness'][spec['readiness']] += 1

    # ---- briefings ---------------------------------------------------------
    for stem, b in sorted(index.briefings.items()):
        path = next(p for p in vault.notes if os.path.basename(p)[:-3] == stem)
        fm, raw = parse_note(vault.notes[path])
        body, _, unresolved = transform_body(
            raw, index, drop_extra=DROP_HEAD_BRIEF)
        unresolved_all.update(unresolved)
        # remove the companion preamble and "this run" paragraphs
        body = re.sub(r'^\*Companion to.*?\*\s*$', '', body.strip(), flags=re.M)
        body = '\n\n'.join(
            p for p in re.split(r'\n\n+', body)
            if not re.search(r'\bthis run\b|\bcontract for this run\b', p))
        window = fm.get('window')
        title = str(fm.get('title') or stem)
        desc_log = []
        description = briefing_description(body, window, b['date'], desc_log, b['series'])
        if desc_log:
            synthesized.append('%s (%s)' % (title, b['date']))
        fm_out = ['---',
                  'title: %s' % yq(title),
                  'series: %s' % b['series'],
                  'date: %s' % b['date']]
        if window:
            fm_out.append('window: %s' % yq(window))
        fm_out.append('pillars: %s' % ylist(next(
            (s['pillars'] for s in index.brief_specs if s['series'] == b['series']), [])))
        fm_out.append('description: %s' % yq(description))
        fm_out.append('origin: vault')
        fm_out.append('source: %s' % yq(path))
        fm_out.append('---')
        content = '\n'.join(fm_out) + '\n\n' + body.strip() + '\n'
        key = (b['series'], b['date'])
        if key in brief_keep and len(brief_keep[key][0]) >= len(content):
            continue
        brief_keep[key] = (content, os.path.join('content', 'briefings', b['series'],
                                                 b['date'] + '.md'))
        stats['briefings'][b['series']] += 1
    for content, fname in brief_keep.values():
        writes[fname] = content

    # ---- glossary ----------------------------------------------------------
    gloss_unresolved = Counter()
    terms = parse_glossary(vault.notes.get('00 - Meta/Glossary.md', ''), index, gloss_unresolved)
    unresolved_all.update(gloss_unresolved)
    writes[os.path.join('content', 'glossary.yml')] = yaml.safe_dump(
        terms, sort_keys=False, allow_unicode=True, default_flow_style=False)

    # ---- sources -------------------------------------------------------------
    src = vault.notes.get('Sources/Sources.md', '')
    fm, raw = parse_note(src)
    body, _, unresolved = transform_body(raw, index)
    unresolved_all.update(unresolved)
    body = re.sub(r'^#\s+Sources\s*$', '', body, flags=re.M)
    writes[os.path.join('content', 'sources.md')] = (
        '---\ntitle: "Sources"\norigin: vault\nsource: "Sources/Sources.md"\n'
        'description: "Canonical bibliography for this library: papers, RFCs, standards '
        'and notable repositories behind the entries."\nupdated: %s\n---\n\n%s'
        % (norm_date(fm.get('updated')) or '2026-04-28', body.strip() + '\n'))

    # ---- state + report ----------------------------------------------------
    state = {'vault_head': vault.head, 'entries': len(index.entries),
             'briefings': sum(stats['briefings'].values()),
             'glossary_terms': len(terms)}
    writes[os.path.join('scripts', 'vault_state.json')] = json.dumps(state, indent=2) + '\n'

    report = build_report(vmap, stats, unresolved_all, synthesized, no_sources,
                          len(index.entries), sum(stats['briefings'].values()), len(terms))
    writes[os.path.join('scripts', 'IMPORT_REPORT.md')] = report

    if a.dry_run:
        for p in sorted(writes):
            print('would write %s (%d bytes)' % (p, len(writes[p])))
        return

    # never touch hand-written files
    for rel, content in sorted(writes.items()):
        out = os.path.join(ROOT, rel)
        if rel.startswith('content/') and os.path.exists(out):
            try:
                existing_fm, _ = parse_note(open(out, encoding='utf-8').read())
                if existing_fm.get('origin') == 'original':
                    print('skip (origin: original): %s' % rel)
                    continue
            except Exception:
                pass
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'w', encoding='utf-8').write(content)

    # remove stale vault-generated files whose source left the map
    for sub in ('entries',):
        d = os.path.join(ROOT, 'content', sub)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if not f.endswith('.md'):
                continue
            p = os.path.join(d, f)
            fm, _ = parse_note(open(p, encoding='utf-8').read())
            if fm.get('origin') == 'vault' and fm.get('slug') not in \
                    {s['slug'] for s in index.entries.values()}:
                os.remove(p)
                print('removed stale: %s' % f)
    d = os.path.join(ROOT, 'content', 'briefings')
    if os.path.isdir(d):
        keep = set()
        for rel in writes:
            if rel.startswith('content/briefings/'):
                keep.add(os.path.normpath(os.path.join(ROOT, rel)))
        for root, _, files in os.walk(d):
            for f in files:
                p = os.path.normpath(os.path.join(root, f))
                fm, _ = parse_note(open(p, encoding='utf-8').read())
                if p not in keep and fm.get('origin') == 'vault':
                    os.remove(p)
                    print('removed stale: %s' % os.path.relpath(p, ROOT))

    print('entries: %d  briefings: %d  glossary terms: %d  unresolved links: %d'
          % (len(index.entries), sum(stats['briefings'].values()), len(terms),
             sum(unresolved_all.values())))
    if sum(unresolved_all.values()):
        print('ERROR: unresolved wikilinks (no link target and not in '
              'WIKILINK_PLAIN):', file=sys.stderr)
        for name, n in sorted(unresolved_all.items(), key=lambda kv: (-kv[1], kv[0])):
            print('  - %s (%d)' % (name, n), file=sys.stderr)
        sys.exit(1)


def build_report(vmap, stats, unresolved, synthesized, no_sources, n_entries, n_brief, n_terms):
    L = ['# Import report', '',
         'Generated by `scripts/import_vault.py` from the research vault.',
         'Re-running the importer refreshes this file.', '',
         '## Counts', '',
         '- Entries: **%d**' % n_entries,
         '- Briefings: **%d**' % n_brief,
         '- Glossary terms: **%d**' % n_terms, '',
         '### By pillar', '']
    for k in [p['key'] for p in (yaml.safe_load(open(os.path.join(ROOT, 'content', 'pillars.yml')).read()))]:
        L.append('- %s: %d' % (k, stats['entries'].get(k, 0)))
    L += ['', '### By type', '']
    for t in ('explainer', 'deep-dive', 'comparison', 'threat-model', 'guide',
              'reference', 'map', 'research-note'):
        if stats['types'].get(t):
            L.append('- %s: %d' % (t, stats['types'][t]))
    L += ['', '### By readiness', '']
    for r in ('battle-tested', 'usable', 'experimental', 'research', 'historical', 'cautionary'):
        if stats['readiness'].get(r):
            L.append('- %s: %d' % (r, stats['readiness'][r]))
    L += ['', '## Unresolved wikilinks', '',
          'Vault links with no site target; rendered as plain text (%d occurrences).'
          % sum(unresolved.values()), '']
    for name, n in sorted(unresolved.items(), key=lambda kv: (-kv[1], kv[0])):
        L.append('- %s — %d' % (name, n))
    L += ['', '## Synthesised descriptions (%d)' % len(synthesized), '',
          'Entries whose meta description could not be taken verbatim from the dek '
          '(first sentence too long or too short; cut at a clause boundary instead):', '']
    for s in sorted(set(synthesized)):
        L.append('- %s' % s)
    L += ['', '## Entries with no external links in the body (%d)' % len(no_sources), '']
    for s in sorted(set(no_sources)):
        L.append('- %s' % s)
    L.append('')
    return '\n'.join(L) + '\n'


if __name__ == '__main__':
    main()
