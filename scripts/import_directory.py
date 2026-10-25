#!/usr/bin/env python3
"""Import the legacy GitHub Pages link pages into content/directory/<pillar>.yml.

The legacy pages are the *.md link lists at the root of branch `main` (read via
`git show main:<file>` so the script keeps working after they move to legacy/).
Each becomes one pillar's curated directory: headings become section titles,
`[Name](url) - description` lines become items, duplicates by URL are merged
within a pillar, and content/directory/overrides.yml is applied last
(remove / replace / annotate / add).

Idempotent. Usage: python3 scripts/import_directory.py
"""
import os
import re
import subprocess
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# legacy page -> pillar key
FILE_PILLAR = {
    'AtomicSwaps.md': 'money',
    'CoinJoin.md': 'money',
    'ConfidentialComputing.md': 'confidential',
    'DecentralizedCompute.md': 'compute',
    'DecentralizedDNS.md': 'naming',
    'DecentralizedMarketplaces.md': 'money',
    'EncryptedMessaging.md': 'messaging',
    'FullHomomorphicEncryption.md': 'cryptography',
    'LightningNetwork.md': 'money',
    'LiquidNetwork.md': 'money',
    'MixNetworks.md': 'anonymity',
    'MultiPartyComputation.md': 'cryptography',
    'Nostr.md': 'identity',
    'OffGridNetworks.md': 'mesh',
    'PostQuantumCryptography.md': 'pqc',
    'PrivateInformationRetrieval.md': 'cryptography',
    'SelfSovereignIdentity.md': 'identity',
    'SurveillanceCountermeasures.md': 'endpoint',
    'Web-Of-Trust.md': 'identity',
    'ZeroKnowledgeProofs.md': 'zk',
}

# readable page-topic labels used to prefix section titles when a pillar has
# more than one source file ("Lightning: Discreet Log Contracts (DLCs)")
PAGE_TOPIC = {
    'AtomicSwaps.md': 'Atomic Swaps',
    'CoinJoin.md': 'CoinJoin',
    'LightningNetwork.md': 'Lightning',
    'LiquidNetwork.md': 'Liquid',
    'DecentralizedMarketplaces.md': 'Marketplaces',
    'FullHomomorphicEncryption.md': 'FHE',
    'MultiPartyComputation.md': 'MPC',
    'PrivateInformationRetrieval.md': 'PIR',
    'Nostr.md': 'Nostr',
    'SelfSovereignIdentity.md': 'Identity',
    'Web-Of-Trust.md': 'Web of Trust',
}

LINK = re.compile(r'^\s*(?:[-*]\s+)?\[([^\]]+)\]\(([^)]+)\)\s*(.*)$')
SEP = re.compile(r'^(?:[-–—:]\s+|\s+)(.*)$')


def git_show(path):
    r = subprocess.run(['git', 'show', 'main:%s' % path], cwd=ROOT,
                       capture_output=True, text=True)
    if r.returncode != 0:
        print('WARN: git show main:%s failed' % path, file=sys.stderr)
        return ''
    return r.stdout


def norm_url(url):
    u = url.strip()
    u = u.split('#')[0]
    if u.endswith('/'):
        u = u[:-1]
    return u


def local_url(url):
    """Rewrite repo-relative legacy URLs to site URLs."""
    u = url.strip()
    if u.startswith('./'):
        u = u[1:]
    if u.startswith('/files/'):
        return u
    return url


def readable_filename(fname):
    base = fname[:-3] if fname.endswith('.md') else fname
    return re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', base)


def parse_page(text, fname, topic=None):
    """-> [(section_title, [(name, url, desc), ...]), ...]; the file's own topic
    heading ("#### Lightning Network" in LightningNetwork.md) stays a section."""
    sections = []
    cur_title, cur = None, None

    def flush():
        nonlocal cur_title, cur
        if cur_title is not None and cur:
            for t, items in sections:
                if t.lower() == cur_title.lower():
                    items.extend(cur)   # merge repeated section titles
                    break
            else:
                sections.append((cur_title, cur))
        cur_title, cur = None, None

    for line in text.split('\n'):
        s = line.rstrip()
        if not s.strip():
            continue
        h = re.match(r'^(#{1,6})\s+(.*?)\s*$', s)
        if h:
            flush()
            cur_title = h.group(2).strip().rstrip(':').strip()
            cur = []
            continue
        m = LINK.match(s)
        if not m:
            continue
        if cur_title is None:
            # link before the first heading: file it under the page topic
            cur_title, cur = topic or readable_filename(fname), []
        name, url, rest = m.group(1).strip(), m.group(2).strip(), m.group(3)
        d = SEP.match(rest)
        desc = d.group(1).strip() if d else ''
        if url.startswith('./') or url.startswith('/files/'):
            url = local_url(url)
        cur.append({'name': name, 'url': url, 'desc': desc})
    flush()
    return sections


def main():
    by_pillar = {}   # pillar -> list of (fname, page_topic, sections)
    for fname, pillar in sorted(FILE_PILLAR.items()):
        text = git_show(fname)
        if not text.strip():
            continue
        topic = PAGE_TOPIC.get(fname) or readable_filename(fname)
        sections = parse_page(text, fname, topic)
        by_pillar.setdefault(pillar, []).append((fname, topic, sections))

    overrides = {}
    op = os.path.join(ROOT, 'content', 'directory', 'overrides.yml')
    if os.path.exists(op):
        overrides = yaml.safe_load(open(op, encoding='utf-8')) or {}

    remove = {norm_url(u) for u in (overrides.get('remove') or [])}
    replace = {norm_url(k): v for k, v in (overrides.get('replace') or {}).items()}
    annotate = {norm_url(k): v for k, v in (overrides.get('annotate') or {}).items()}
    add = overrides.get('add') or {}
    # insert_after: url -> [items] placed immediately after that item, same section
    insert_after = {norm_url(k): v for k, v in (overrides.get('insert_after') or {}).items()}
    # move_after: pillar -> {section title: title of the section it should follow}
    move_after = overrides.get('move_after') or {}

    outdir = os.path.join(ROOT, 'content', 'directory')
    os.makedirs(outdir, exist_ok=True)

    written = 0
    for pillar in sorted({p['key'] for p in yaml.safe_load(
            open(os.path.join(ROOT, 'content', 'pillars.yml'), encoding='utf-8'))}):
        files = by_pillar.get(pillar) or []
        if not files and not add.get(pillar):
            continue
        multi = len(files) > 1
        sections = []
        seen_titles = {}
        seen_urls = set()
        for fname, topic, secs in files:
            for title, items in secs:
                if multi and title.lower() == topic.lower():
                    full = topic
                else:
                    full = '%s: %s' % (topic, title) if multi else title
                # merge repeated section titles across/within files
                if full in seen_titles:
                    target = sections[seen_titles[full]]
                else:
                    seen_titles[full] = len(sections)
                    target = {'title': full, 'items': []}
                    sections.append(target)
                for it in items:
                    nu = norm_url(it['url'])
                    if nu in seen_urls or nu in remove:
                        continue
                    if nu in replace:
                        rep = replace[nu]
                        it = dict(it, url=rep.get('url', it['url']))
                        if rep.get('name'):
                            it['name'] = rep['name']
                        if rep.get('desc'):
                            it['desc'] = rep['desc']
                        nu = norm_url(it['url'])
                        if nu in seen_urls:
                            continue
                    if nu in annotate:
                        it = dict(it, status=annotate[nu].get('status'),
                                  note=annotate[nu].get('note'))
                    seen_urls.add(nu)
                    target['items'].append(it)
                    for extra in insert_after.get(nu, []):
                        en = norm_url(extra['url'])
                        if en in seen_urls or en in remove:
                            continue
                        seen_urls.add(en)
                        target['items'].append({'name': extra['name'], 'url': extra['url'],
                                                'desc': extra.get('desc', '')})
        for item in add.get(pillar) or []:
            nu = norm_url(item['url'])
            if nu in seen_urls:
                continue
            seen_urls.add(nu)
            title = item.get('section') or 'Curated'
            if title not in seen_titles:
                seen_titles[title] = len(sections)
                sections.append({'title': title, 'items': []})
            sections[seen_titles[title]]['items'].append(
                {'name': item['name'], 'url': item['url'], 'desc': item.get('desc', '')})
        sections = [s for s in sections if s['items']]
        for title, after in (move_after.get(pillar) or {}).items():
            idx = {s['title']: n for n, s in enumerate(sections)}
            if title in idx and after in idx:
                sec = sections.pop(idx[title])
                pos = [s['title'] for s in sections].index(after)
                sections.insert(pos + 1, sec)
        doc = {'pillar': pillar, 'sections': sections}
        out = os.path.join(outdir, pillar + '.yml')
        body = yaml.safe_dump(doc, sort_keys=False, allow_unicode=True,
                              default_flow_style=False)
        open(out, 'w', encoding='utf-8').write(body)
        written += 1
        n = sum(len(s['items']) for s in sections)
        print('%-14s %2d sections %3d links' % (pillar, len(sections), n))

    print('wrote %d pillar directories' % written)


if __name__ == '__main__':
    main()
