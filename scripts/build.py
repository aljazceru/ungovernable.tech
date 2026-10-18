#!/usr/bin/env python3
"""Build the whole ungovernable.tech site into public/.

Reads content/ (pillars, entries, guides, briefings, paths, glossary,
directory, pages) plus templates/ and assets/, and renders every page:
home, pillar hubs, entries, guides, paths, briefings, directory, glossary,
sources, method, about, 404, plus sitemap.xml, robots.txt, feed.xml,
llms.txt, search index, favicons, Open Graph images and the legacy
redirect stubs. Output is deterministic: no timestamps except content dates.

Usage: python3 scripts/build.py
"""
import datetime
import hashlib
import html as htmlmod
import json
import math
import os
import re
import shutil
import urllib.parse

import markdown
import yaml
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, 'public')
SITE = os.environ.get('SITE_URL', 'https://ungovernable.tech')
REPO = 'https://github.com/aljazceru/ungovernable.tech'

TYPE_LABELS = {
    'explainer': 'Explainer', 'deep-dive': 'Deep dive', 'comparison': 'Comparison',
    'threat-model': 'Threat model', 'guide': 'Guide', 'reference': 'Reference',
    'map': 'Map', 'research-note': 'Research note',
}

# readiness: label, exact scale copy, filled bars (None = special rendering)
READINESS = {
    'battle-tested': {'label': 'Battle-tested', 'level': 5,
                      'full': 'Battle-tested: years of production use by people with '
                              'real adversaries; audited and well understood.',
                      'tail': 'Years of production use under real adversaries.'},
    'usable': {'label': 'Usable', 'level': 4,
               'full': 'Usable: in production and usable today, but younger, smaller '
                       'or with known caveats.',
               'tail': 'In production today, with caveats.'},
    'experimental': {'label': 'Experimental', 'level': 3,
                     'full': 'Experimental: working software, but early: small user '
                             'base, unaudited or changing fast.',
                     'tail': 'Working software, but early.'},
    'research': {'label': 'Research', 'level': 2,
                 'full': 'Research: papers and prototypes; not something to rely on yet.',
                 'tail': 'Papers and prototypes, not production.'},
    'historical': {'label': 'Historical', 'level': None,
                   'full': 'Historical: discontinued or superseded; kept for the lessons.',
                   'tail': 'Discontinued or superseded; kept for the lessons.'},
    'cautionary': {'label': 'Cautionary', 'level': None,
                   'full': 'Cautionary: works, but its trust model, governance or legal '
                           'exposure undermines what it claims.',
                   'tail': 'Works, but its trust model undermines it.'},
}
READINESS_ORDER = ['battle-tested', 'usable', 'experimental', 'research',
                   'historical', 'cautionary']

MD_EXTS = ['tables', 'fenced_code', 'toc', 'attr_list', 'footnotes',
           'sane_lists', 'def_list']

INLINE_SCRIPT = ('(function(){try{var t=localStorage.getItem("theme");'
                 'document.documentElement.setAttribute("data-theme",'
                 't==="light"?"light":"dark")}catch(e){'
                 'document.documentElement.setAttribute("data-theme","dark")}})();')

BUILTIN_METHOD = '''The library exists to answer practical questions under pressure: how to talk, move, publish and compute when someone is watching or interfering. Every entry is written the same way: what it does, what it protects against, what it trusts, and how ready it is. Nothing here is advice; everything here is meant to be checkable.

## Where entries come from

Entries are compiled from a running research log of primary sources: specifications, RFCs and FIPS documents, peer-reviewed papers, canonical repositories, and release notes read week by week in the [briefings](/briefings/). Marketing claims do not earn an entry; implementations do. When a claim matters, it links to where it came from — see [sources](/sources/) for the shared bibliography.

## How entries are written

Each entry answers four questions in order:

1. **What it is and what it does** — the mechanism, at the level a technically literate reader needs.
2. **What it protects against** — the adversary it defeats, stated as a threat model.
3. **What it trusts** — the assumptions underneath: operators, hardware vendors, consensus, key custody.
4. **Where it stands** — deployment status, attacks, and an honest readiness rating.

## The readiness scale {#readiness}

Every technology entry carries one of six ratings. They describe deployment reality, not promise.

- **Battle-tested** — Battle-tested: years of production use by people with real adversaries; audited and well understood.
- **Usable** — Usable: in production and usable today, but younger, smaller or with known caveats.
- **Experimental** — Experimental: working software, but early: small user base, unaudited or changing fast.
- **Research** — Research: papers and prototypes; not something to rely on yet.
- **Historical** — Historical: discontinued or superseded; kept for the lessons.
- **Cautionary** — Cautionary: works, but its trust model, governance or legal exposure undermines what it claims.

The first four render as a five-bar meter; historical renders hollow; cautionary carries a warning mark in the site's accent colour.

## Editorial rules

- **Primary sources first.** Specifications, papers, canonical repositories — not press releases.
- **Name the trust model.** A system is only as sovereign as its weakest trusted party; that party is named.
- **Experimental is not production.** The meter separates the two; treat anything below *usable* as something to watch or prototype with, not depend on.
- **No hype, no euphemism.** Seizures, raids and broken promises are described plainly.
- **The site is static and self-contained.** No trackers, no cookies, no third-party requests; fonts are served from this domain.

## Corrections

Wrong or out of date? Open an issue or pull request on [GitHub](REPO_URL); fixes are credited in the commit history. Research notes are dated, so you can judge for yourself how fresh a claim is.
'''

BUILTIN_ABOUT = '''ungovernable.tech is an independent reference library of the technologies people use to free themselves: anonymity networks, censorship circumvention, secure messaging, off-grid mesh, sovereign naming and money, decentralized storage and compute, confidential computing, privacy-enhancing cryptography, zero-knowledge, post-quantum keys, and the devices and habits that hold it together.

It is written for cypherpunks, activists and journalists under surveillance, people in censored countries, node runners and developers — anyone who would rather understand the machinery than trust a label on it.

## What makes it different

The world does not lack link lists. It lacks honest ones. This library keeps three disciplines:

1. **Every entry names its threat model.** What a tool protects against, and what it quietly trusts, is the whole game. Encryption without an honest account of metadata is a half-answer.
2. **Every entry carries a readiness rating** on a six-point scale from battle-tested to cautionary — see the [method](/method/). Experimental software is labelled experimental; dead software is kept for its lessons.
3. **No trackers, ever.** The site is static HTML with no analytics, no cookies and no third-party requests. What you read here is between you and your network.

## How it is built

The site is generated from a research vault of primary sources; the pipeline (importers, build, checks) is [open source](REPO_URL). A weekly briefing series records what changed, dated and unedited; the entries carry the current, edited view. The [directory](/directory/) keeps the legacy hand-checked link lists, with dead links marked rather than silently dropped.

## Contact and corrections

Suggestions: open an issue or PR on [GitHub](REPO_URL), or reach [aljaz@nostr.si](https://nostr.at/aljaz@nostr.si) over Nostr.
'''


def slugify(t):
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', str(t).lower())).strip('-')[:60]


def parse_doc(text):
    m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    if not m:
        return {}, text
    fm = yaml.safe_load(m.group(1)) or {}
    return fm, text[m.end():]


def render_md(text):
    md = markdown.Markdown(extensions=MD_EXTS)
    html = md.convert(text)
    return html, [t for t in md.toc_tokens if t['level'] == 2]


LINK_REWRITE = {}   # /kb/<guide>/ -> /guides/<guide>/ for hand-written bodies


def slugify_head(s):
    s = re.sub(r'[^a-z0-9]+', '-', str(s).lower()).strip('-')
    return re.sub(r'(?<=-)-0(\d)', r'-\1', re.sub(r'(?<=-)0(\d)', r'\1', s))


def fix_fragments(soup):
    """Point same-document #links at the generated heading ids; unwrap
    links whose target heading does not exist."""
    ids = {el['id'] for el in soup.find_all(id=True)}
    heads = []
    for h in soup.find_all(['h1', 'h2', 'h3', 'h4']):
        if h.get('id'):
            heads.append((slugify_head(h.get_text()), h['id']))
    for a in soup.find_all('a', href=True):
        href = a['href']
        if not href.startswith('#'):
            continue
        frag = href[1:]
        if not frag or frag in ids:
            if not frag:
                a.unwrap()
            continue
        sf = slugify_head(frag)
        for stext, hid in heads:
            if stext == sf or stext.startswith(sf) or sf.startswith(stext):
                a['href'] = '#' + hid
                break
        else:
            a.unwrap()
    return soup


def postprocess(html, wrap_tables=True):
    soup = BeautifulSoup(html, 'html.parser')
    # markdown's table alignment emits inline style attributes; CSP blocks
    # them, so translate the text-align ones to classes and drop the rest
    for tag in soup.find_all(True):
        st = tag.get('style')
        if not st:
            continue
        m = re.fullmatch(r'\s*text-align:\s*(right|left|center)\s*;?\s*', st)
        if m:
            tag['class'] = (tag.get('class') or []) + [
                {'right': 'ta-r', 'left': 'ta-l', 'center': 'ta-c'}[m.group(1)]]
        del tag['style']
    if wrap_tables:
        for tb in soup.find_all('table'):
            if tb.parent.name == 'div' and 'tw' in (tb.parent.get('class') or []):
                continue
            w = soup.new_tag('div')
            w['class'] = 'tw'
            tb.wrap(w)
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href in LINK_REWRITE:
            a['href'] = href = LINK_REWRITE[href]
        if href.startswith(('http://', 'https://')):
            rel = a.get('rel') or []
            for r in ('noopener', 'nofollow'):
                if r not in rel:
                    rel.append(r)
            a['rel'] = rel
    fix_fragments(soup)
    return soup.decode_contents(), soup


def text_of(html):
    return BeautifulSoup(html, 'html.parser').get_text(' ')


def datefmt(d):
    try:
        return datetime.date.fromisoformat(str(d)).strftime('%d %b %Y').lstrip('0')
    except ValueError:
        return str(d)


# ------------------------------------------------ presentation helpers
# Deterministic generative art: PGP armour, hex dumps, cipher grids and
# mirrored identicons, all derived from content hashes so the build stays
# byte-for-byte reproducible.

def armour_block(slugs, n_lines=10, width=64):
    """Base64 armour: a sha256 chain over the entry slugs, wrapped at 64."""
    import base64
    seed = ('\n'.join(slugs)).encode()
    buf = b''
    while len(buf) < n_lines * width * 3 // 4:
        seed = hashlib.sha256(seed).digest()
        buf += seed
    text = base64.b64encode(buf).decode()
    return [text[i:i + width] for i in range(0, n_lines * width, width)]


def hexdump(s, n_lines=6, width=8):
    """Classic hexdump rows (`width` bytes each) of a string."""
    out, b = [], s.encode()
    for i in range(n_lines):
        chunk = b[i * width:(i + 1) * width]
        if not chunk:
            break
        hx = ' '.join('%02x' % c for c in chunk)
        asc = ''.join(chr(c) if 32 <= c < 127 else '.' for c in chunk)
        out.append('%04x  %-*s  |%s|' % (i * width, width * 3 - 1, hx, asc))
    return out


def _grid_svg(seed, size, mirrored, density, levels, cls=''):
    """Pixel grid SVG from a sha256 of `seed`; rects at varying opacity."""
    h = hashlib.shake_256(seed.encode()).digest(size * size)
    cols = size // 2 if mirrored else size
    rects = []
    for y in range(size):
        for x in range(cols):
            v = h[(y * cols + x) % len(h)]
            if v < density:
                op = levels[v % len(levels)]
                xs = (x, size - 1 - x) if mirrored else (x,)
                for xx in xs:
                    rects.append('<rect x="%d" y="%d" width="1" height="1" '
                                 'opacity="%.2f"/>' % (xx, y, op))
    return ('<svg class="%s" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
            'shape-rendering="crispEdges" aria-hidden="true" focusable="false">'
            '%s</svg>') % (cls, size, size, ''.join(rects))


def cipher_grid(seed, size=16):
    """Hero cipher grid: sparse noise of signal pixels at 4 opacities."""
    return _grid_svg(seed, size, mirrored=False, density=0x66,
                     levels=[0.85, 0.5, 0.28, 0.14], cls='cipher-svg')


def identicon(key, size=12):
    """Mirrored pixel identicon for a pillar key, 3 opacity levels."""
    return _grid_svg('pillar/' + key, size, mirrored=True, density=0x60,
                     levels=[0.9, 0.55, 0.3], cls='identicon-svg')


def hexline(key, n=16):
    """First n bytes of sha256(key) as a spaced hex string."""
    return ' '.join('%02x' % b
                    for b in hashlib.sha256(key.encode()).digest()[:n])


def content_hash():
    """Short fingerprint of everything under content/, PGP-style."""
    h = hashlib.sha256()
    cdir = os.path.join(ROOT, 'content')
    for dirpath, _, fns in sorted(os.walk(cdir)):
        for fn in sorted(fns):
            p = os.path.join(dirpath, fn)
            h.update(os.path.relpath(p, cdir).encode())
            h.update(open(p, 'rb').read())
    hx = h.hexdigest()[:32].upper()
    return ' '.join(hx[i:i + 4] for i in range(0, 32, 4))


# ---------------------------------------------------------------- load

def load_all():
    data = {}
    pillars = yaml.safe_load(open(os.path.join(ROOT, 'content', 'pillars.yml'),
                                  encoding='utf-8'))
    data['pillars'] = pillars
    data['pillar_by_key'] = {p['key']: p for p in pillars}

    entries = {}
    edir = os.path.join(ROOT, 'content', 'entries')
    global LINK_REWRITE
    for f in sorted(os.listdir(edir)):
        if f.endswith('.md'):
            fm0, _ = parse_doc(open(os.path.join(edir, f), encoding='utf-8').read())
            if (fm0.get('type') == 'guide'):
                s0 = fm0.get('slug') or f[:-3]
                LINK_REWRITE['/kb/%s/' % s0] = '/guides/%s/' % s0
    for f in sorted(os.listdir(edir)):
        if not f.endswith('.md'):
            continue
        fm, body = parse_doc(open(os.path.join(edir, f), encoding='utf-8').read())
        e = dict(fm)
        e['body_md'] = body
        e['slug'] = fm.get('slug') or f[:-3]
        e['url'] = ('/guides/%s/' % e['slug']) if fm.get('type') == 'guide' \
            else ('/kb/%s/' % e['slug'])
        html, toc = render_md(body)
        e['body_html_raw'], _ = postprocess(html, wrap_tables=False)
        e['body_html'], soup = postprocess(html)
        e['toc'] = [{'id': t['id'], 'title': t['name']} for t in toc]
        words = len(text_of(e['body_html']).split())
        e['read_min'] = max(1, math.ceil(words / 230))
        ext = {a['href'] for a in soup.find_all('a', href=True)
               if a['href'].startswith(('http://', 'https://'))}
        e['n_sources'] = len(ext)
        entries[e['slug']] = e
    data['entries'] = entries

    # internal links out / backlinks in (for Related)
    out_links, backlinks = {}, {}
    for slug, e in entries.items():
        outs = []
        for a in BeautifulSoup(e['body_html'], 'html.parser').find_all('a', href=True):
            m = re.match(r'^/(?:kb|guides)/([a-z0-9-]+)/?$', a['href'])
            if m and m.group(1) != slug:
                outs.append(m.group(1))
        seen, ordered = set(), []
        for s in outs:
            if s not in seen:
                seen.add(s)
                ordered.append(s)
        out_links[slug] = ordered
        for s in ordered:
            backlinks.setdefault(s, [])
            if slug not in backlinks[s]:
                backlinks[s].append(slug)
    data['out_links'], data['backlinks'] = out_links, backlinks

    # briefings
    vmap = yaml.safe_load(open(os.path.join(ROOT, 'scripts', 'vault_map.yml'),
                               encoding='utf-8'))
    series_specs = {b['series']: b for b in (vmap.get('briefings') or [])}
    briefings = {}
    bdir = os.path.join(ROOT, 'content', 'briefings')
    if os.path.isdir(bdir):
        for series in sorted(os.listdir(bdir)):
            sdir = os.path.join(bdir, series)
            if not os.path.isdir(sdir):
                continue
            for f in sorted(os.listdir(sdir)):
                if not f.endswith('.md'):
                    continue
                fm, body = parse_doc(open(os.path.join(sdir, f), encoding='utf-8').read())
                b = dict(fm)
                b['series'] = fm.get('series') or series
                b['date'] = str(fm.get('date') or f[:-3])
                b['body_md'] = body
                html, _ = render_md(body)
                b['body_html'], _ = postprocess(html)
                b['read_min'] = max(1, math.ceil(
                    len(text_of(b['body_html']).split()) / 230))
                briefings.setdefault(b['series'], []).append(b)
    for lst in briefings.values():
        lst.sort(key=lambda b: b['date'])
    data['briefings'] = briefings
    data['series_specs'] = series_specs

    # paths
    paths = None
    pp = os.path.join(ROOT, 'content', 'paths.yml')
    if os.path.exists(pp):
        paths = yaml.safe_load(open(pp, encoding='utf-8'))
        for p in paths:
            for s in p['steps']:
                if s['slug'] not in entries:
                    raise SystemExit('paths: %s references unknown slug %r'
                                     % (p['key'], s['slug']))
    data['paths'] = paths

    # glossary
    glossary = []
    gp = os.path.join(ROOT, 'content', 'glossary.yml')
    if os.path.exists(gp):
        for t in yaml.safe_load(open(gp, encoding='utf-8')) or []:
            t['definition_html'] = markdown.markdown(
                t['definition_md'], extensions=['sane_lists'])
            t['see_urls'] = [entries[s]['url'] for s in t.get('see') or []
                             if s in entries] if entries else []
            t['see_pairs'] = [(entries[s]['url'], entries[s]['title'])
                              for s in t.get('see') or [] if s in entries]
            glossary.append(t)
    data['glossary'] = glossary

    # directory
    directory = {}
    ddir = os.path.join(ROOT, 'content', 'directory')
    if os.path.isdir(ddir):
        for f in sorted(os.listdir(ddir)):
            if f.endswith('.yml') and f != 'overrides.yml':
                d = yaml.safe_load(open(os.path.join(ddir, f), encoding='utf-8'))
                directory[d['pillar']] = d
    data['directory'] = directory

    # pages
    pages = {}
    pdir = os.path.join(ROOT, 'content', 'pages')
    for name in ('about', 'method'):
        p = os.path.join(pdir, name + '.md')
        if os.path.exists(p):
            fm, body = parse_doc(open(p, encoding='utf-8').read())
            html, _ = render_md(body)
            html, _ = postprocess(html)
            pages[name] = {'title': fm.get('title') or name.title(),
                           'body_html': html, 'dek': fm.get('dek')}
    data['pages'] = pages

    # sources page
    sp = os.path.join(ROOT, 'content', 'sources.md')
    if os.path.exists(sp):
        fm, body = parse_doc(open(sp, encoding='utf-8').read())
        html, _ = render_md(body)
        html, _ = postprocess(html)
        data['sources'] = {'title': fm.get('title') or 'Sources',
                           'body_html': html, 'dek': fm.get('dek')}
    else:
        data['sources'] = None
    # possible / what's possible map
    poss = None
    pp2 = os.path.join(ROOT, 'content', 'possible.yml')
    if os.path.exists(pp2):
        poss = yaml.safe_load(open(pp2, encoding='utf-8'))
        for sc in poss.get('scenarios', []):
            for sl in sc['blocks']:
                if sl not in entries:
                    raise SystemExit('possible: %s references unknown slug %r'
                                     % (sc['key'], sl))
            for pk in sc['pillars']:
                if pk not in data['pillar_by_key']:
                    raise SystemExit('possible: %s references unknown pillar %r'
                                     % (sc['key'], pk))
    data['possible'] = poss
    return data


# ---------------------------------------------------------------- render

def make_env(data):
    env = Environment(loader=FileSystemLoader(os.path.join(ROOT, 'templates')),
                      autoescape=select_autoescape(['html']))
    v = hashlib.md5(
        open(os.path.join(ROOT, 'assets', 'css', 'site.css'), 'rb').read() +
        open(os.path.join(ROOT, 'assets', 'js', 'site.js'), 'rb').read()
    ).hexdigest()[:8]

    entries = data['entries']
    total = (len(entries)
             + sum(len(v) for v in data['briefings'].values())
             + len(data['paths'] or []) + len(data['pillars'])
             + len(data['glossary']))

    n_links_total = sum(len(s['items'])
                        for d in (data['directory'] or {}).values()
                        for s in d['sections'])
    ctx = {
        'site': SITE, 'v': v, 'nav': None,
        'pillars': data['pillars'],
        'readiness': READINESS, 'readiness_order': READINESS_ORDER,
        'type_labels': TYPE_LABELS,
        'counts': {'total': total, 'entries': len(entries),
                   'guides': sum(1 for e in entries.values()
                                 if e.get('type') == 'guide'),
                   'briefings': sum(len(v) for v in data['briefings'].values()),
                   'links': n_links_total, 'trackers': 0},
        'armour': armour_block(sorted(entries)),
        'hexdump': hexdump('Technology for people who refuse to be governed '
                           'by surveillance.'),
        'hero_grid': cipher_grid('ungovernable.tech/hero/166'),
        'build_fp': content_hash(),
    }
    return env, ctx


def jsonld(d):
    return json.dumps(d, ensure_ascii=False).replace('<', '\\u003c')


def build_search_index(data):
    idx = []
    e_by_slug = data['entries']
    for slug in sorted(e_by_slug):
        e = e_by_slug[slug]
        pnames = [data['pillar_by_key'][k]['name']
                  for k in (e.get('pillars') or []) if k in data['pillar_by_key']]
        idx.append({'t': e['title'], 'u': e['url'], 'k': TYPE_LABELS.get(e['type'], e['type']),
                    'p': pnames, 'd': e.get('description', ''),
                    'a': ' '.join((e.get('aliases') or []) + (e.get('tags') or [])),
                    'h': ' · '.join(t['title'] for t in e['toc']),
                    'r': (READINESS.get(e.get('readiness')) or {}).get('label', '')})
    for p in data['paths'] or []:
        idx.append({'t': p['name'], 'u': '/paths/%s/' % p['key'], 'k': 'Path',
                    'p': [], 'd': p['intro'], 'a': p['who'], 'h': '', 'r': ''})
    for p in data['pillars']:
        idx.append({'t': p['name'], 'u': '/pillars/%s/' % p['key'], 'k': 'Pillar',
                    'p': [], 'd': p['intro'], 'a': p['question'], 'h': '', 'r': ''})
    for t in data['glossary']:
        idx.append({'t': t['term'], 'u': '/glossary/#%s' % t['slug'], 'k': 'Term',
                    'p': [], 'd': t['definition_md'], 'a': '', 'h': '', 'r': ''})
    if data.get('possible'):
        pz = data['possible']
        idx.append({'t': "What's Possible", 'u': '/possible/', 'k': 'Map',
                    'p': [], 'd': pz['dek'],
                    'a': ' '.join(sc['goal'] for sc in pz['scenarios']),
                    'h': '', 'r': ''})
    for series, lst in data['briefings'].items():
        name = data['series_specs'].get(series, {}).get('name', series)
        for b in lst:
            idx.append({'t': b['title'], 'u': '/briefings/%s/%s/' % (series, b['date']),
                        'k': 'Briefing', 'p': [name], 'd': b.get('description', ''),
                        'a': b.get('window', ''), 'h': '', 'r': ''})
    return idx


TAGLINE = 'Technology for people who refuse to be governed by surveillance.'

BG = (10, 13, 11)       # --bg #0a0d0b
INK = (223, 231, 225)   # --ink #dfe7e1
MUT = (133, 148, 138)   # --muted #85948a
SIGNAL = (60, 255, 143)  # --signal #3cff8f
GRID = (18, 30, 24)     # faint grid line on bg

# the 5x5 pixel-grid U mark (x, y cells), also used for the favicon
U_MARK = [(0, 0), (4, 0), (0, 1), (4, 1), (0, 2), (4, 2),
          (0, 3), (4, 3), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4)]


def draw_mark(d, x, y, cell, fill=SIGNAL, pad=True):
    """Draw the 5x5 pixel U at (x, y) with cells of `cell` px, 1-cell pad."""
    ox = x + (cell if pad else 0)
    oy = y + (cell if pad else 0)
    for cx, cy in U_MARK:
        d.rectangle([ox + cx * cell, oy + cy * cell,
                     ox + (cx + 1) * cell - 1, oy + (cy + 1) * cell - 1], fill=fill)


def og_images(pillars):
    """Default + per-pillar 1200x630 cards in the dark identity."""
    from PIL import Image, ImageDraw, ImageFont
    fdir = os.path.join(ROOT, 'scripts', 'fonts')
    big_p = os.path.join(fdir, 'Archivo-Bold.ttf')
    mono_p = os.path.join(fdir, 'IBMPlexMono-Medium.ttf')

    def F(path, size):
        return (ImageFont.truetype(path, size) if os.path.exists(path)
                else ImageFont.load_default())

    def base():
        img = Image.new('RGB', (1200, 630), BG)
        d = ImageDraw.Draw(img)
        for gx in range(40, 1200, 40):
            d.line([(gx, 0), (gx, 630)], fill=GRID, width=1)
        for gy in range(40, 630, 40):
            d.line([(0, gy), (1200, gy)], fill=GRID, width=1)
        d.text((64, 52), 'UNGOVERNABLE.TECH', font=F(mono_p, 26), fill=MUT)
        d.text((1050, 52), '0 TRACKERS', font=F(mono_p, 22), fill=MUT)
        draw_mark(d, 64, 104, 8)
        return img, d

    def wrap(d, text, font, maxw):
        lines, cur = [], ''
        for w in text.split(' '):
            t = (cur + ' ' + w).strip()
            if d.textlength(t, font=font) > maxw and cur:
                lines.append(cur)
                cur = w
            else:
                cur = t
        lines.append(cur)
        return lines

    def card(path, title, sub, kicker):
        img, d = base()
        big_size = 66 if len(title) > 34 else 96
        big = F(big_p, big_size)
        lines = wrap(d, title, big, 1000)
        if len(lines) >= 4:
            big_size, big = 56, F(big_p, 56)
            lines = wrap(d, title, big, 1000)
        elif len(lines) == 3 and big_size > 76:
            big_size, big = 76, F(big_p, 76)
        y0 = 260 if len(lines) <= 2 else (225 if len(lines) == 3 else 215)
        d.text((64, y0 - 52), kicker, font=F(mono_p, 26), fill=SIGNAL)
        y = y0
        for l in lines[:4]:
            d.text((64, y), l, font=big, fill=INK)
            y += big_size + 12
        d.rectangle([64, y + 8, 160, y + 13], fill=SIGNAL)
        mono = F(mono_p, 28)
        yy = y + 36
        for l in wrap(d, sub, mono, 1010)[:2]:
            d.text((64, yy), l, font=mono, fill=MUT)
            yy += 38
        img.save(path, 'PNG', optimize=True)

    ogdir = os.path.join(PUBLIC, 'assets', 'og')
    os.makedirs(ogdir, exist_ok=True)
    card(os.path.join(ogdir, 'default.png'), TAGLINE,
         'An independent library of anonymity, circumvention and sovereignty tools.',
         '// FIELD MANUAL')
    for i, p in enumerate(pillars, 1):
        card(os.path.join(ogdir, 'pillar-%s.png' % p['key']), p['name'],
             'Pillar %02d of 14 — %s' % (i, p['question']),
             '0x%02d / 14' % i)


def favicons():
    """The 5x5 pixel U mark as favicon.svg + Pillow-rendered icons."""
    rects = ''.join('<rect x="%d" y="%d" width="1" height="1"/>' % c
                    for c in U_MARK)
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 7 7" '
           'shape-rendering="crispEdges"><rect width="7" height="7" '
           'fill="#0a0d0b"/><g fill="#3cff8f" transform="translate(1,1)">'
           '%s</g></svg>') % rects
    open(os.path.join(PUBLIC, 'favicon.svg'), 'w', encoding='utf-8').write(svg)
    from PIL import Image, ImageDraw
    for size, name in [(32, 'favicon.ico'), (192, 'icon-192.png'),
                       (512, 'icon-512.png'), (512, 'icon-maskable-512.png')]:
        # mark occupies 5/7 of the canvas (safe zone for maskable too)
        cell = size / 7.0
        im = Image.new('RGB', (size, size), BG)
        d = ImageDraw.Draw(im)
        for cx, cy in U_MARK:
            x0 = round((cx + 1) * cell)
            y0 = round((cy + 1) * cell)
            x1 = round((cx + 2) * cell)
            y1 = round((cy + 2) * cell)
            d.rectangle([x0, y0, x1 - 1, y1 - 1], fill=SIGNAL)
        if name == 'favicon.ico':
            im.save(os.path.join(PUBLIC, name), sizes=[(32, 32)])
        else:
            im.save(os.path.join(PUBLIC, 'assets', name), 'PNG', optimize=True)
    manifest = {
        'name': 'ungovernable.tech', 'short_name': 'ungovernable',
        'description': 'A library of the technologies people use to free themselves.',
        'start_url': '/', 'scope': '/', 'display': 'minimal-ui',
        'background_color': '#0a0d0b', 'theme_color': '#0a0d0b',
        'icons': [
            {'src': '/assets/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
            {'src': '/assets/icon-512.png', 'sizes': '512x512', 'type': 'image/png'},
            {'src': '/assets/icon-maskable-512.png', 'sizes': '512x512',
             'type': 'image/png', 'purpose': 'maskable'},
        ],
    }
    open(os.path.join(PUBLIC, 'site.webmanifest'), 'w', encoding='utf-8').write(
        json.dumps(manifest, indent=1) + '\n')


STUB = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Moved — ungovernable.tech</title>
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={target}">
<link rel="canonical" href="{site}{target}">
</head>
<body>
<p>This page has moved to <a href="{target}">{target}</a>.</p>
</body>
</html>
'''


def main():
    if os.path.exists(PUBLIC):
        shutil.rmtree(PUBLIC)
    os.makedirs(os.path.join(PUBLIC, 'assets'))
    shutil.copytree(os.path.join(ROOT, 'assets'),
                    os.path.join(PUBLIC, 'assets'),
                    dirs_exist_ok=True)
    if os.path.isdir(os.path.join(ROOT, 'files')):
        shutil.copytree(os.path.join(ROOT, 'files'),
                        os.path.join(PUBLIC, 'files'), dirs_exist_ok=True)

    data = load_all()
    env, ctx = make_env(data)
    pillars, entries = data['pillars'], data['entries']
    pillar_by_key = data['pillar_by_key']
    for i, p in enumerate(pillars, 1):
        p['idx'] = i
        p['identicon'] = identicon(p['key'])
        p['hexline'] = hexline(p['key'])

    def w(rel, content):
        p = os.path.join(PUBLIC, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        mode = 'wb' if isinstance(content, bytes) else 'w'
        with open(p, mode) as f:
            f.write(content)

    def render(tpl, rel, **kw):
        page = env.get_template(tpl).render(**{**ctx, **kw})
        w(rel, page)

    # ---------- shared view models ------------------------------------
    def row_view(slug, also=False):
        e = entries[slug]
        v = {'title': e['title'], 'url': e['url'], 'type': e['type'],
             'readiness': e.get('readiness')}
        if also and e.get('pillars') and pillar_by_key.get(e['pillars'][0]):
            v['also'] = 'also in ' + pillar_by_key[e['pillars'][0]]['short'].lower()
        return v

    pillar_stats = []
    for p in pillars:
        k = p['key']
        kb = [e for e in entries.values()
              if k in (e.get('pillars') or []) and e['type'] != 'guide']
        gd = [e for e in entries.values()
              if k in (e.get('pillars') or []) and e['type'] == 'guide']
        ndir = sum(len(s['items']) for s in
                   (data['directory'].get(k) or {}).get('sections', []))
        pillar_stats.append(dict(p, n_entries=len(kb), n_guides=len(gd), n_links=ndir))

    guides = sorted([e for e in entries.values() if e['type'] == 'guide'],
                    key=lambda e: (str(e.get('updated') or ''), e['title']))
    kb_entries = [e for e in entries.values() if e['type'] != 'guide']
    readiness_counts = {r: sum(1 for e in entries.values()
                               if e.get('readiness') == r) for r in READINESS_ORDER}
    recent = sorted(entries.values(),
                    key=lambda e: (str(e.get('updated') or ''), e['title']),
                    reverse=True)[:8]
    recent = [dict(row_view(e['slug']), also=False) for e in recent]

    latest_briefings = []
    for series, lst in sorted(data['briefings'].items()):
        b = lst[-1]
        first = b.get('description', '')
        m = re.match(r'Weekly briefing for [^:]+:\s*(.*)', first)
        latest_briefings.append({'series': series, 'date': b['date'],
                                 'series_name': data['series_specs'].get(
                                     series, {}).get('name', series),
                                 'first_line': (m.group(1) if m else first)[:110]})

    start_guide = next((dict(title=g['title'], url=g['url'], dek=g.get('dek'),
                             time=g.get('time'), level=g.get('level'))
                        for g in reversed(guides) if g['slug'] == 'threat-modeling'),
                       None)

    total_rated = sum(readiness_counts.values()) or 1
    spec_segments = []
    x = 0.0
    for r in READINESS_ORDER:
        n = readiness_counts[r]
        seg_w = 1000.0 * n / total_rated
        spec_segments.append({'label': READINESS[r]['label'], 'n': n,
                              'x': round(x, 1), 'w': round(max(seg_w - 2, 0), 1)})
        x += seg_w
    spec_segments[-1]['w'] = round(max(1000 - spec_segments[-1]['x'], 0), 1)

    # ---------- home ----------------------------------------------------
    home_jsonld = jsonld({'@context': 'https://schema.org', '@type': 'WebSite',
                          'name': 'ungovernable.tech', 'url': SITE,
                          'description': 'An independent library of the tools, '
                          'protocols and cryptography that keep people private, '
                          'connected and sovereign.'})
    render('home.html', 'index.html',
           title='ungovernable.tech', nav='home',
           description='An independent library of the tools, protocols and cryptography '
                       'that keep people private, connected and sovereign: from Tor and '
                       'mesh radios to zero-knowledge proofs and post-quantum keys.',
           canonical='/', og_type='website',
           pillar_stats=pillar_stats, paths=data['paths'] or [],
           start_guide=start_guide,
           guides_new=[dict(title=g['title'], url=g['url'], dek=g.get('dek'),
                            level=g.get('level'), time=g.get('time'))
                       for g in reversed(guides[-6:])],
           recent=recent, latest_briefings=latest_briefings,
           readiness_counts=readiness_counts, spec_segments=spec_segments,
           jsonld=[home_jsonld])

    # ---------- pillars -------------------------------------------------
    render('pillars.html', 'pillars/index.html',
           title='Pillars', nav='pillars',
           description='The fourteen pillars of ungovernable.tech: anonymity networks, '
                       'censorship circumvention, secure messaging, off-grid mesh, '
                       'sovereign naming, identity, money, storage, compute, '
                       'confidential computing, cryptography, zero-knowledge, '
                       'post-quantum and operational security.',
           canonical='/pillars/', pillar_stats=pillar_stats)

    rsort = {r: i for i, r in enumerate(READINESS_ORDER)}
    for p in pillars:
        k = p['key']
        mine = [e for e in entries.values() if k in (e.get('pillars') or [])]
        start_here = [row_view(e['slug'], also=e['pillars'][0] != k)
                      for e in sorted(
                          [e for e in mine if e['type'] in ('explainer', 'map')
                           and e['pillars'][0] == k], key=lambda e: e['title'].lower())]
        gd = [dict(title=g['title'], url=g['url'], dek=g.get('dek'),
                   level=g.get('level'), time=g.get('time'))
              for g in sorted([e for e in mine if e['type'] == 'guide'],
                              key=lambda e: e['title'].lower())]
        tech = [row_view(e['slug'], also=e['pillars'][0] != k)
                for e in sorted([e for e in mine if e['type'] == 'deep-dive'],
                                key=lambda e: (rsort.get(e.get('readiness'), 9),
                                               e['title'].lower()))]
        ref = [row_view(e['slug'], also=e['pillars'][0] != k)
               for e in sorted([e for e in mine if e['type'] in
                                ('comparison', 'threat-model', 'reference',
                                 'research-note')],
                                key=lambda e: e['title'].lower())]
        directory = data['directory'].get(k)
        n_links = sum(len(s['items']) for s in directory['sections']) if directory else 0
        pseries = [dict(series=s,
                        name=(data['series_specs'].get(s) or {}).get('name', s),
                        n=len(lst), latest=lst[-1])
                   for s, lst in sorted(data['briefings'].items())
                   if k in (data['series_specs'].get(s) or {}).get('pillars', [])]
        series_key = series_name = None
        series_briefings = []
        if len(pseries) == 1:
            series_key = pseries[0]['series']
            series_name = pseries[0]['name']
            series_briefings = list(reversed(data['briefings'][series_key][-6:]))
        crumb_jsonld = jsonld({
            '@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE + '/'},
                {'@type': 'ListItem', 'position': 2, 'name': 'Pillars',
                 'item': SITE + '/pillars/'},
                {'@type': 'ListItem', 'position': 3, 'name': p['name'],
                 'item': '%s/pillars/%s/' % (SITE, k)}]})
        render('pillar.html', 'pillars/%s/index.html' % k,
               title='%s — Pillar' % p['name'], nav='pillars',
               description=('%s %s' % (p['question'], p['intro']))[:300],
               canonical='/pillars/%s/' % k,
               og_image='/assets/og/pillar-%s.png' % k,
               p=p, start_here=start_here, guides=gd, technologies=tech,
               reference=ref, directory=directory, n_links=n_links,
               pillar_series=pseries if len(pseries) != 1 else None,
               series_key=series_key, series_name=series_name,
               series_briefings=series_briefings, jsonld=crumb_jsonld)

    # ---------- what's possible map -------------------------------------
    if data.get('possible'):
        poss = data['possible']
        scn = []
        for sc in poss['scenarios']:
            blocks = [{'title': entries[sl]['title'], 'url': entries[sl]['url'],
                       'readiness': entries[sl].get('readiness'),
                       'type': entries[sl]['type']} for sl in sc['blocks']]
            pills = [{'key': k, 'short': pillar_by_key[k]['short'],
                      'name': pillar_by_key[k]['name']} for k in sc['pillars']]
            scn.append({'key': sc['key'], 'goal': sc['goal'], 'dek': sc['dek'],
                        'blocks': blocks, 'pillars': pills,
                        'pillar_keys': sc['pillars']})
        poss_crumb = jsonld({
            '@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Home',
                 'item': SITE + '/'},
                {'@type': 'ListItem', 'position': 2, 'name': "What's Possible",
                 'item': SITE + '/possible/'}]})
        render('possible.html', 'possible/index.html',
               title="What's Possible", nav='possible',
               description=('What you can do today by combining the technologies in '
                            'this library: real capabilities mapped to the working '
                            'building blocks that compose them.'),
               canonical='/possible/',
               dek=poss['dek'], intro=poss['intro'], scenarios=scn,
               art=cipher_grid('ungovernable.tech/possible/0x7'),
               jsonld=poss_crumb)

    # ---------- entries and guides ---------------------------------------
    for slug in sorted(entries):
        e = entries[slug]
        pk = (e.get('pillars') or [None])[0]
        primary = pillar_by_key.get(pk)
        pnames = [pillar_by_key[x]['name'] for x in (e.get('pillars') or [])
                  if x in pillar_by_key]
        rel_slugs = list(e.get('related') or [])
        for s in data['out_links'].get(slug, []):
            if s not in rel_slugs:
                rel_slugs.append(s)
        for s in data['backlinks'].get(slug, []):
            if s not in rel_slugs:
                rel_slugs.append(s)
        related = [row_view(s) for s in rel_slugs if s in entries][:12]
        also_pillars = [pillar_by_key[x] for x in (e.get('pillars') or [])[1:]
                        if x in pillar_by_key]
        origin_note = ('Compiled from the ungovernable.tech research notes.'
                       if e.get('origin') == 'vault'
                       else 'Written for ungovernable.tech.')
        art = {'@context': 'https://schema.org', '@type': 'TechArticle',
               'headline': e['title'], 'description': e.get('description', ''),
               'dateModified': str(e.get('updated') or ''),
               'datePublished': str(e.get('created') or e.get('updated') or ''),
               'url': SITE + e['url'], 'mainEntityOfPage': SITE + e['url'],
               'image': SITE + ('/assets/og/pillar-%s.png' % pk if pk else
                                '/assets/og/default.png'),
               'about': [{'@type': 'Thing', 'name': n} for n in pnames],
               'isPartOf': {'@type': 'WebSite', 'name': 'ungovernable.tech',
                            'url': SITE},
               'inLanguage': 'en'}
        if e.get('level'):
            art['proficiencyLevel'] = e['level']
        crumbs = [{'name': 'Home', 'item': SITE + '/'}]
        if primary:
            crumbs.append({'name': primary['name'],
                           'item': '%s/pillars/%s/' % (SITE, pk)})
        crumbs.append({'name': e['title'], 'item': SITE + e['url']})
        crumb_jsonld = jsonld({'@context': 'https://schema.org',
                               '@type': 'BreadcrumbList',
                               'itemListElement': [
                                   {'@type': 'ListItem', 'position': i + 1,
                                    'name': c['name'], 'item': c['item']}
                                   for i, c in enumerate(crumbs)]})
        render('entry.html', e['url'].lstrip('/') + 'index.html',
               title=e['title'], nav='guides' if e['type'] == 'guide' else 'pillars',
               description=e.get('description', ''), canonical=e['url'],
               og_type='article',
               og_image='/assets/og/pillar-%s.png' % pk if pk else None,
               e=e, toc=e['toc'], body_html=e['body_html'], related=related,
               also_pillars=also_pillars, primary_pillar=primary or
               {'name': 'Library', 'key': ''}, pillar_names=pnames,
               origin_note=origin_note,
               edit_url='https://github.com/aljazceru/ungovernable.tech/issues/new?title='
                        + urllib.parse.quote(e['title']),
               n_sources=e['n_sources'],
               jsonld_article=jsonld(art), jsonld_crumb=crumb_jsonld,
               body_class='on-entry')

    if guides:
        render('guides.html', 'guides/index.html', title='Guides', nav='guides',
               description='Practical guides from ungovernable.tech: threat modeling, '
                           'secure messengers, Tor, self-custody, off-grid meshes and '
                           'publishing sites that cannot be seized.',
               canonical='/guides/',
               guides=[dict(title=g['title'], url=g['url'], dek=g.get('dek'),
                            level=g.get('level'), time=g.get('time'))
                       for g in sorted(guides, key=lambda g: g['title'].lower())])

    # ---------- paths ------------------------------------------------------
    if data['paths']:
        render('paths.html', 'paths/index.html', title='Paths', nav='paths',
               description='Learning paths by persona: ordered reading lists for '
                           'people under surveillance, behind firewalls, holding '
                           'sovereign money, running infrastructure or building '
                           'freedom technology.',
               canonical='/paths/', paths=data['paths'])
        for i, p in enumerate(data['paths']):
            steps = []
            for s in p['steps']:
                t = entries[s['slug']]
                steps.append({'title': t['title'], 'url': t['url'],
                              'type': t['type'], 'readiness': t.get('readiness'),
                              'why': s['why']})
            nxt = data['paths'][(i + 1) % len(data['paths'])]
            render('path.html', 'paths/%s/index.html' % p['key'],
                   title='%s (path)' % p['name'], nav='paths',
                   description=('%s %s' % (p['who'], p['intro']))[:300],
                   canonical='/paths/%s/' % p['key'], p=dict(p, steps=steps),
                   next_path=nxt if len(data['paths']) > 1 else None)

    # ---------- briefings ----------------------------------------------------
    render('briefings.html', 'briefings/index.html', title='Briefings',
           nav='briefings',
           description='Dated weekly research briefings from ungovernable.tech: '
                       'releases, papers and governance changes across mix networks, '
                       'post-quantum, identity, naming, compute and PIR.',
           canonical='/briefings/',
           series=[dict(series=s,
                        name=(data['series_specs'].get(s) or {}).get('name', s),
                        n=len(lst), latest=lst[-1])
                   for s, lst in sorted(data['briefings'].items())])
    for series, lst in sorted(data['briefings'].items()):
        name = (data['series_specs'].get(series) or {}).get('name', series)
        sp = data['series_specs'].get(series) or {}
        pnames = [pillar_by_key[k]['name'] for k in sp.get('pillars', [])
                  if k in pillar_by_key]
        first_lines = []
        for b in lst:
            m = re.match(r'Weekly briefing for [^:]+:\s*(.*)', b.get('description', ''))
            first_lines.append((m.group(1) if m else b.get('description', ''))[:110])
        render('series.html', 'briefings/%s/index.html' % series,
               title='%s briefings' % name, nav='briefings',
               description='Weekly %s research briefings from ungovernable.tech, '
                           'newest first.' % name.lower(),
               canonical='/briefings/%s/' % series,
               s={'series': series, 'name': name}, pillar_names=pnames,
               briefings=[dict(b, first_line=fl) for b, fl in zip(reversed(lst),
                                                                  reversed(first_lines))])
        for i, b in enumerate(lst):
            art = {'@context': 'https://schema.org', '@type': 'Article',
                   'headline': b['title'], 'description': b.get('description', ''),
                   'datePublished': b['date'], 'dateModified': b['date'],
                   'url': '%s/briefings/%s/%s/' % (SITE, series, b['date']),
                   'mainEntityOfPage': '%s/briefings/%s/%s/' % (SITE, series, b['date']),
                   'isPartOf': {'@type': 'WebSite', 'name': 'ungovernable.tech',
                                'url': SITE},
                   'inLanguage': 'en'}
            crumb = jsonld({'@context': 'https://schema.org',
                            '@type': 'BreadcrumbList',
                            'itemListElement': [
                                {'@type': 'ListItem', 'position': 1, 'name': 'Home',
                                 'item': SITE + '/'},
                                {'@type': 'ListItem', 'position': 2,
                                 'name': 'Briefings', 'item': SITE + '/briefings/'},
                                {'@type': 'ListItem', 'position': 3, 'name': name,
                                 'item': '%s/briefings/%s/' % (SITE, series)},
                                {'@type': 'ListItem', 'position': 4, 'name': b['date'],
                                 'item': '%s/briefings/%s/%s/' % (SITE, series,
                                                                  b['date'])}]})
            render('briefing.html', 'briefings/%s/%s/index.html' % (series, b['date']),
                   title=b['title'], nav='briefings',
                   description=b.get('description', ''),
                   canonical='/briefings/%s/%s/' % (series, b['date']),
                   og_type='article', b=b, series_name=name, pillar_names=[
                       pillar_by_key[k] for k in sp.get('pillars', [])
                       if k in pillar_by_key],
                   body_html=b['body_html'],
                   prev=lst[i - 1] if i > 0 else None,
                   next=lst[i + 1] if i + 1 < len(lst) else None,
                   jsonld_article=jsonld(art), jsonld_crumb=crumb,
                   body_class='on-entry')

    # ---------- directory -----------------------------------------------------
    dir_pillars = []
    for p in pillars:
        d = data['directory'].get(p['key'])
        if not d:
            continue
        dir_pillars.append(dict(p, sections=d['sections'],
                                n=sum(len(s['items']) for s in d['sections'])))
    n_links = sum(p['n'] for p in dir_pillars)
    render('directory.html', 'directory/index.html', title='Directory',
           nav='directory',
           description='Curated outbound links from ungovernable.tech, grouped by '
                       'pillar and section: projects, specifications, papers and '
                       'tools, with dead and superseded links marked.',
           canonical='/directory/', pillars=dir_pillars, n_links=n_links)

    # ---------- glossary --------------------------------------------------------
    letters = sorted({t['term'][0].upper() for t in data['glossary']})
    groups = []
    for l in letters:
        groups.append((l, sorted([t for t in data['glossary']
                                  if t['term'][0].upper() == l],
                                 key=lambda t: t['term'].lower())))
    render('glossary.html', 'glossary/index.html', title='Glossary',
           nav='glossary',
           description='Definitions for the terms used across ungovernable.tech, '
                       'from attestation and AEAD to webs of trust and VDFs.',
           canonical='/glossary/', terms=data['glossary'], letters=letters,
           groups=groups)

    # ---------- about / method / sources ------------------------------------------
    pages = data['pages']
    about = pages.get('about') or {}
    about_body = about.get('body_html') or render_md(
        BUILTIN_ABOUT.replace('REPO_URL', REPO))[0]
    about_body, _ = postprocess(about_body)
    render('page.html', 'about/index.html', title=about.get('title', 'About'),
           nav=None,
           description='What ungovernable.tech is, who it is for, and how it is '
                       'maintained: an independent, tracker-free library of freedom '
                       'technology.',
           canonical='/about/', kicker='The library', crumb=[{'name': 'About'}],
           dek=about.get('dek'), body_html=about_body)

    method = pages.get('method') or {}
    method_body = method.get('body_html') or render_md(
        BUILTIN_METHOD.replace('REPO_URL', REPO))[0]
    method_body, _ = postprocess(method_body)
    render('page.html', 'method/index.html', title=method.get('title', 'Method'),
           nav=None,
           description='How ungovernable.tech entries are researched and rated: '
                       'primary sources, threat models named, and the six-point '
                       'readiness scale from battle-tested to cautionary.',
           canonical='/method/', kicker='Editorial method',
           crumb=[{'name': 'Method'}],
           dek=method.get('dek'), body_html=method_body)

    if data['sources']:
        render('page.html', 'sources/index.html', title='Sources', nav=None,
               description='The shared bibliography behind ungovernable.tech: '
                           'standards bodies, specifications, papers and canonical '
                           'repositories.',
               canonical='/sources/', kicker='Bibliography',
               crumb=[{'name': 'Sources'}],
               title_h='Sources', dek=data['sources'].get('dek'),
               body_html=data['sources']['body_html'])

    render('404.html', '404.html', title='Page not found',
           description='This page does not exist. Search the library or start '
                       'from a pillar.',
           canonical='/404.html')

    # ---------- search index ---------------------------------------------------
    idx = build_search_index(data)
    w('assets/search.json',
      json.dumps(idx, ensure_ascii=False, separators=(',', ':')))

    # ---------- sitemap / robots / feed / llms -----------------------------------
    urls = [('/', None), ('/pillars/', None), ('/directory/', None),
            ('/glossary/', None), ('/about/', None), ('/briefings/', None),
            ('/method/', None), ('/sources/', None)]
    if data.get('possible'):
        urls.append(('/possible/', None))
    if guides:
        urls.append(('/guides/', None))
    if data['paths']:
        urls.append(('/paths/', None))
        urls += [('/paths/%s/' % p['key'], None) for p in data['paths']]
    for e in entries.values():
        urls.append((e['url'], str(e.get('updated') or '')))
    for k in pillar_by_key:
        urls.append(('/pillars/%s/' % k, None))
    for series, lst in data['briefings'].items():
        urls.append(('/briefings/%s/' % series, None))
        for b in lst:
            urls.append(('/briefings/%s/%s/' % (series, b['date']), b['date']))
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, mod in urls:
        sm.append('<url><loc>%s%s</loc>%s</url>' % (
            SITE, loc, ('<lastmod>%s</lastmod>' % mod) if mod else ''))
    sm.append('</urlset>')
    w('sitemap.xml', '\n'.join(sm) + '\n')

    w('robots.txt', 'User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n' % SITE)

    feed_items = [(str(e.get('updated') or ''), e) for e in entries.values()]
    feed_items += [(b['date'], b) for lst in data['briefings'].values() for b in lst]
    feed_items.sort(key=lambda x: x[0], reverse=True)
    feed_items = feed_items[:40]
    updated = feed_items[0][0] if feed_items else '2026-01-01'
    atom = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<feed xmlns="http://www.w3.org/2005/Atom">',
            '<title>ungovernable.tech</title>',
            '<link href="%s/" rel="alternate" type="text/html"/>' % SITE,
            '<link href="%s/feed.xml" rel="self"/>' % SITE,
            '<id>%s/</id>' % SITE,
            '<updated>%sT00:00:00Z</updated>' % updated,
            '<subtitle>Technology for people who refuse to be governed by '
            'surveillance.</subtitle>']
    for dt, it in feed_items:
        is_briefing = 'series' in it
        url = ('%s/briefings/%s/%s/' % (SITE, it['series'], it['date'])
               if is_briefing else SITE + it['url'])
        atom.append('<entry>')
        atom.append('<title>%s</title>' % htmlmod.escape(it['title']))
        atom.append('<link href="%s" rel="alternate" type="text/html"/>' % url)
        atom.append('<id>%s</id>' % url)
        atom.append('<published>%sT00:00:00Z</published>' % dt)
        atom.append('<updated>%sT00:00:00Z</updated>' % dt)
        atom.append('<summary>%s</summary>' % htmlmod.escape(it.get('description', '')))
        atom.append('</entry>')
    atom.append('</feed>')
    w('feed.xml', '\n'.join(atom) + '\n')

    ll = ['# ungovernable.tech', '',
          '> An independent library of the tools, protocols and cryptography that keep '
          'people private, connected and sovereign: from Tor and mesh radios to '
          'zero-knowledge proofs and post-quantum keys. Every entry says what it '
          'protects against, what it trusts, and how ready it is.', '',
          'Readiness scale: battle-tested, usable, experimental, research, historical, '
          'cautionary. See [/method/](%s/method/) for the full definitions.' % SITE, '']
    ll.append('## Pillars')
    for p in pillars:
        ll.append('- [%s](%s/pillars/%s/): %s' % (p['name'], SITE, p['key'], p['intro']))
    ll.append('')
    ll.append('## Guides')
    for g in sorted(guides, key=lambda g: g['title'].lower()):
        ll.append('- [%s](%s%s): %s' % (g['title'], SITE, g['url'], g.get('description', '')))
    ll.append('')
    ll.append('## Entries')
    for e in sorted(kb_entries, key=lambda e: e['title'].lower()):
        ll.append('- [%s](%s%s): %s' % (e['title'], SITE, e['url'], e.get('description', '')))
    ll.append('')
    ll.append('## Also')
    ll.append('- [Directory](%s/directory/): curated outbound links' % SITE)
    ll.append('- [Glossary](%s/glossary/): short definitions' % SITE)
    ll.append('- [Briefings](%s/briefings/): dated weekly research logs' % SITE)
    ll.append('- [Sources](%s/sources/): shared bibliography' % SITE)
    ll.append('- [Feed](%s/feed.xml)' % SITE)
    w('llms.txt', '\n'.join(ll) + '\n')

    # ---------- legacy redirects ------------------------------------------------
    import import_directory
    for fname, pillar in sorted(import_directory.FILE_PILLAR.items()):
        base = fname[:-3]
        target = '/pillars/%s/#directory' % pillar
        for rel in ('%s.html' % base, '%s/index.html' % base):
            w(rel, STUB.format(site=SITE, target=target))
    if 'confidential-dvm' in entries:
        w('ConfidentialDVM.html',
          STUB.format(site=SITE, target='/kb/confidential-dvm/'))
        w('ConfidentialDVM/index.html',
          STUB.format(site=SITE, target='/kb/confidential-dvm/'))
    else:
        for rel in ('ConfidentialDVM.html', 'ConfidentialDVM/index.html'):
            w(rel, STUB.format(site=SITE, target='/pillars/confidential/#directory'))
    for rel in ('README.html', 'README/index.html'):
        w(rel, STUB.format(site=SITE, target='/'))

    # ---------- icons / og / csp ---------------------------------------------------
    favicons()
    og_images(pillars)
    w('.csp-hash', hashlib.sha256(INLINE_SCRIPT.encode()).hexdigest())

    print('built %d entries, %d guides, %d briefings, %d glossary terms, '
          '%d links' % (len(kb_entries), len(guides),
                        sum(len(v) for v in data['briefings'].values()),
                        len(data['glossary']), n_links))


if __name__ == '__main__':
    main()
