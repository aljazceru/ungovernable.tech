#!/usr/bin/env python3
"""Check the built site in public/: broken internal links and anchors,
pages missing title/description/canonical/h1, redirect stubs, sitemap
exactness and duplicate titles.

Exits non-zero and prints every problem found.
"""
import glob
import json
import os
import re
import sys
from collections import Counter

from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, 'public')
SITE = os.environ.get('SITE_URL', 'https://ungovernable.tech')

EXTERNAL = re.compile(r'^(https?:|mailto:|tel:|javascript:|data:)')


def is_stub(path):
    return 'http-equiv="refresh"' in open(path, encoding='utf-8').read(3000)


def stub_target(path):
    m = re.search(r'url=([^"\'\s>]+)', open(path, encoding='utf-8').read(3000))
    return m.group(1) if m else None


def html_files():
    out = []
    for f in glob.glob(os.path.join(PUBLIC, '**', '*.html'), recursive=True):
        out.append(f)
    return sorted(out)


def resolve(href, base):
    """Resolve an internal href/src to a public/ path; None = not internal."""
    if EXTERNAL.match(href):
        return None
    href = href.split('#')[0].split('?')[0]
    if not href:
        return None
    p = os.path.join(PUBLIC, href.lstrip('/')) if href.startswith('/') \
        else os.path.normpath(os.path.join(base, href))
    if p.endswith('/'):
        p += 'index.html'
    elif os.path.isdir(p):
        p = os.path.join(p, 'index.html')
    return p


def main():
    files = set()
    for dirpath, _, fns in os.walk(PUBLIC):
        if os.sep + '.' in dirpath:
            continue
        for fn in fns:
            files.add(os.path.normpath(os.path.join(dirpath, fn)))
    docs = {}

    def doc_for(path):
        p = os.path.normpath(path)
        if p not in docs:
            docs[p] = BeautifulSoup(open(p, encoding='utf-8').read(), 'html.parser')
        return docs[p]

    problems = []
    titles = Counter()
    stubs, live = [], []
    for f in html_files():
        rel = os.path.relpath(f, PUBLIC)
        if is_stub(f):
            stubs.append(rel)
            continue
        live.append(rel)
        s = doc_for(f)
        t = s.find('title')
        d = s.find('meta', attrs={'name': 'description'})
        c = s.find('link', rel='canonical')
        h1 = s.find_all('h1')
        if not t or not t.get_text(strip=True):
            problems.append('%s: missing <title>' % rel)
        else:
            titles[t.get_text(strip=True)] += 1
        if not d or not (d.get('content') or '').strip():
            problems.append('%s: missing meta description' % rel)
        if not c or not (c.get('href') or '').strip():
            problems.append('%s: missing canonical' % rel)
        if len(h1) != 1:
            problems.append('%s: %d h1 elements' % (rel, len(h1)))

    for t, n in titles.items():
        if n > 1:
            problems.append('duplicate title (%d pages): %s' % (n, t))

    # stubs land one hop on a live page
    for rel in stubs:
        t = stub_target(os.path.join(PUBLIC, rel))
        p = resolve(t, os.path.dirname(os.path.join(PUBLIC, rel))) if t else None
        if p is None or not os.path.isfile(p) or is_stub(p):
            problems.append('stub %s does not land on a live page (%s)' % (rel, t))

    # broken internal links and fragments
    for f in html_files():
        rel = os.path.relpath(f, PUBLIC)
        s = doc_for(f)
        base = os.path.dirname(f)
        for tag in s.find_all(['a', 'link', 'script', 'img', 'source']):
            href = tag.get('href') or tag.get('src')
            if not href:
                continue
            p = resolve(href, base)
            if p is not None and os.path.normpath(p) not in files:
                problems.append('%s -> %s (missing file)' % (rel, href))
            frag = href.split('#', 1)[1] if '#' in href else ''
            if not frag:
                continue
            if href.startswith('#'):
                doc = s
            elif p is not None and os.path.normpath(p) in files:
                doc = doc_for(p)
            else:  # external link with a fragment: not ours to check
                continue
            if not doc.find(id=frag):
                problems.append('%s -> #%s (missing anchor)' % (rel, frag))

    # sitemap lists exactly the live pages
    sm = open(os.path.join(PUBLIC, 'sitemap.xml'), encoding='utf-8').read()
    locs = set(re.findall(r'<loc>%s([^<]*)</loc>' % re.escape(SITE), sm))
    expected = {'/' + rel[:-10] for rel in live
                if rel.endswith('index.html') and rel != '404.html'}
    expected |= {'/' + rel[:-5] for rel in live
                 if not rel.endswith('index.html') and rel != '404.html'}
    expected.discard('/404.html')
    if locs != expected:
        problems.append('sitemap: %d urls vs %d pages; missing=%s extra=%s'
                        % (len(locs), len(expected),
                           sorted(expected - locs)[:6], sorted(locs - expected)[:6]))

    # search index parses and has no dead urls
    si = json.load(open(os.path.join(PUBLIC, 'assets', 'search.json'), encoding='utf-8'))
    for it in si:
        p = resolve(it['u'], PUBLIC)
        if p is None or not os.path.isfile(p):
            problems.append('search.json -> %s (missing page)' % it['u'])

    # link-like-but-unclickable: bare URLs in visible text, and leftover
    # wiki-link brackets. All real links must be <a> elements.
    BARE_URL = re.compile(r"(?<![\"'=])(https?://|www\.)[^\s<>()\[\]\"']+", re.I)
    for f in html_files():
        rel = os.path.relpath(f, PUBLIC)
        if is_stub(os.path.join(PUBLIC, rel)):
            continue
        s2 = doc_for(f)
        body = s2.find('body') or s2
        for tag in body.find_all(['script', 'style']):
            tag.decompose()
        for node in body.find_all(string=BARE_URL):
            if node.find_parent(['a', 'code', 'pre']):
                continue
            m = BARE_URL.search(str(node))
            problems.append('%s: bare URL not linked (%s)'
                            % (rel, m.group(0)[:60]))
        txt = body.get_text(' ')
        if '[[' in txt or ']]' in txt:
            problems.append('%s: leftover wiki-link brackets in text' % rel)

    for p in problems:
        print('BAD', p)
    print('checked %d pages (%d stubs), sitemap %d urls, problems: %d'
          % (len(html_files()), len(stubs), len(locs), len(problems)))
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
