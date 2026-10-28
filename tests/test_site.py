"""Quality bar for the built site: idempotent build, per-page head contract,
tables wrapped, no external assets, site_check green, search index complete,
legacy redirects present, no placeholder text."""
import hashlib
import json
import os
import re
import subprocess

import pytest
import yaml
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, 'public')
SITE = 'https://ungovernable.tech'
sys_path_hack = ROOT + '/scripts'


def run_build():
    r = subprocess.run(['python3', os.path.join(ROOT, 'scripts', 'build.py')],
                       capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stderr[-3000:]


@pytest.fixture(scope='module', autouse=True)
def built():
    run_build()
    yield


def snap():
    out = {}
    for dp, _, fns in os.walk(PUBLIC):
        for fn in fns:
            p = os.path.join(dp, fn)
            out[os.path.relpath(p, PUBLIC)] = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    return out


def entries():
    out = {}
    edir = os.path.join(ROOT, 'content', 'entries')
    for f in sorted(os.listdir(edir)):
        if not f.endswith('.md'):
            continue
        t = open(os.path.join(edir, f), encoding='utf-8').read()
        m = re.match(r'^---\n(.*?)\n---\n', t, re.S)
        fm = yaml.safe_load(m.group(1))
        out[fm['slug']] = fm
    return out


def is_stub(path):
    return 'http-equiv="refresh"' in open(path, encoding='utf-8').read(3000)


def html_files():
    out = []
    for dp, _, fns in os.walk(PUBLIC):
        for fn in fns:
            if fn.endswith('.html'):
                out.append(os.path.join(dp, fn))
    return sorted(out)


def test_build_is_idempotent():
    s1 = snap()
    run_build()
    assert s1 == snap()


def test_circumvention_directory_renders_in_both_locations():
    """A pillar populated only by overrides must reach both directory views."""
    with open(os.path.join(ROOT, 'content', 'directory', 'overrides.yml')) as f:
        expected = {item['url'] for item in yaml.safe_load(f)['add']['circumvention']}
    assert expected
    for page, selector in [('pillars/circumvention/index.html', '#directory'),
                           ('directory/index.html', '#circumvention')]:
        with open(os.path.join(PUBLIC, page)) as f:
            section = BeautifulSoup(f.read(), 'html.parser').select_one(selector)
        assert section is not None, page
        links = {a['href'] for a in section.select('a[href^="https://"]')}
        assert links == expected, page


def test_entry_pages_head_contract():
    for slug, fm in entries().items():
        p = os.path.join(PUBLIC, 'guides' if fm['type'] == 'guide' else 'kb',
                         slug, 'index.html')
        assert os.path.isfile(p), slug
        s = BeautifulSoup(open(p, encoding='utf-8').read(), 'html.parser')
        assert len(s.find_all('h1')) == 1, slug
        can = s.find('link', rel='canonical')
        assert can and can['href'] == SITE + (
            '/guides/%s/' if fm['type'] == 'guide' else '/kb/%s/') % slug, slug
        d = s.find('meta', attrs={'name': 'description'})
        assert d and d.get('content'), slug
        c = d['content']
        lo, hi = (70, 160) if fm.get('origin') == 'vault' else (70, 180)
        assert lo <= len(c) <= hi and c.endswith('.'), '%s: %d %r' % (slug, len(c), c)
        lds = s.find_all('script', type='application/ld+json')
        assert lds, slug
        for sc in lds:
            json.loads(sc.string)
        types = {json.loads(sc.string).get('@type') for sc in lds}
        assert 'TechArticle' in types, slug
        assert 'BreadcrumbList' in types, slug


def test_tables_wrapped():
    for f in html_files():
        if is_stub(f):
            continue
        s = BeautifulSoup(open(f, encoding='utf-8').read(), 'html.parser')
        for tb in s.find_all('table'):
            assert tb.find_parent('div', class_='tw'), \
                '%s: bare table' % os.path.relpath(f, PUBLIC)


def test_no_external_assets():
    pat = re.compile(r'<(?:script src|iframe src|link rel=stylesheet href|img src)'
                     r'=["\']?https?://', re.I)
    raw = re.compile(r'(?:script|iframe)[^>]+src=["\']https?://|'
                     r'link[^>]+href=["\']https?://.*\.css|'
                     r'img[^>]+src=["\']https?://', re.I)
    # The one allowed third-party asset: cookieless self-hosted Plausible.
    plausible = ('<script defer data-domain="ungovernable.tech" '
                 'src="https://analytics.cypherpunk.cloud/js/script.js"></script>')
    for f in html_files():
        t = open(f, encoding='utf-8').read()
        if not is_stub(f):
            assert t.count(plausible) == 1, \
                '%s: missing Plausible' % os.path.relpath(f, PUBLIC)
        t = t.replace(plausible, '')
        assert not pat.search(t) and not raw.search(t), os.path.relpath(f, PUBLIC)


def test_site_check_passes():
    import sys
    sys.path.insert(0, os.path.join(ROOT, 'scripts'))
    import site_check
    assert site_check.main() == 0


def test_search_index_has_every_entry():
    idx = json.load(open(os.path.join(PUBLIC, 'assets', 'search.json'),
                         encoding='utf-8'))
    urls = {it['u'] for it in idx}
    for slug, fm in entries().items():
        want = ('/guides/%s/' if fm['type'] == 'guide' else '/kb/%s/') % slug
        assert want in urls, slug
    for it in idx:
        assert all(k in it for k in ('t', 'u', 'k', 'p', 'd', 'a', 'h', 'r'))


def test_legacy_redirect_stubs_exist():
    import import_directory
    for fname in import_directory.FILE_PILLAR:
        base = fname[:-3]
        for rel in ('%s.html' % base, '%s/index.html' % base):
            p = os.path.join(PUBLIC, rel)
            assert os.path.isfile(p), rel
            assert is_stub(p), rel
    for rel in ('README.html', 'ConfidentialDVM.html'):
        assert os.path.isfile(os.path.join(PUBLIC, rel)), rel
        assert is_stub(os.path.join(PUBLIC, rel)), rel


def test_stub_contract():
    """Every stub: meta refresh, absolute canonical, noindex, meta CSP,
    and a visible plain link to the target (for non-refresh clients)."""
    for f in html_files():
        if not is_stub(f):
            continue
        rel = os.path.relpath(f, PUBLIC)
        t = open(f, encoding='utf-8').read()
        m = re.search(r'<meta http-equiv="refresh" content="0; url=([^"]+)">', t)
        assert m, rel
        target = m.group(1)
        assert ('<link rel="canonical" href="%s%s">' % (SITE, target)) in t, rel
        assert '<meta name="robots" content="noindex">' in t, rel
        assert 'http-equiv="Content-Security-Policy"' in t, rel
        assert ('<a href="%s">%s</a>' % (target, target)) in t, rel


def _csp():
    import sys
    sys.path.insert(0, sys_path_hack)
    import csp
    return csp


def test_meta_csp_matches_inline_script():
    """The home page's meta CSP carries base64(sha256()) of the inline
    script actually present in the HTML, and precedes that script."""
    import base64
    csp = _csp()
    html = open(os.path.join(PUBLIC, 'index.html'), encoding='utf-8').read()
    s = BeautifulSoup(html, 'html.parser')
    meta = s.find('meta', attrs={'http-equiv': 'Content-Security-Policy'})
    assert meta and meta.get('content'), 'no meta CSP on home page'
    pol = meta['content']
    assert pol == csp.csp_policy(csp.script_hash())
    assert 'frame-ancestors' not in pol  # not supported in meta CSP
    m = re.search(r"'sha256-([^']+)'", pol)
    assert m, pol
    inline = [sc for sc in s.find_all('script')
              if not sc.get('src') and sc.get('type') != 'application/ld+json']
    assert len(inline) == 1
    want = base64.b64encode(
        hashlib.sha256(inline[0].string.encode()).digest()).decode()
    assert m.group(1) == want
    # the hash file serve.py reads must hold the same base64 hash
    assert open(os.path.join(PUBLIC, '.csp-hash'), encoding='utf-8').read().strip() \
        == want
    # meta policy sits before the first (inline) script it allows
    assert html.index('<meta http-equiv="Content-Security-Policy"') \
        < html.index('<script>')


def test_every_page_has_csp_and_no_stray_inline_scripts():
    """Every built page (stubs included) carries the meta CSP, and no page
    contains an inline executable <script> other than the theme script
    (ld+json blocks are data, not executable)."""
    csp = _csp()
    want = csp.csp_policy(csp.script_hash())
    for f in html_files():
        rel = os.path.relpath(f, PUBLIC)
        s = BeautifulSoup(open(f, encoding='utf-8').read(), 'html.parser')
        meta = s.find('meta', attrs={'http-equiv': 'Content-Security-Policy'})
        assert meta and meta.get('content') == want, rel
        for sc in s.find_all('script'):
            if sc.get('src') or sc.get('type') == 'application/ld+json':
                continue
            assert sc.string == csp.INLINE_SCRIPT, rel


def test_404_page_urls_are_root_absolute():
    """GitHub Pages serves /404.html at any depth, so nothing inside it
    may be a relative URL."""
    s = BeautifulSoup(open(os.path.join(PUBLIC, '404.html'), encoding='utf-8').read(),
                      'html.parser')
    for tag in s.find_all(['a', 'link', 'script', 'img', 'source']):
        u = tag.get('href') or tag.get('src')
        if not u:
            continue
        assert u.startswith(('/', '#')) or re.match(
            r'^(https?:|mailto:)', u), '%s=%s' % (tag.name, u)


BAD_STRINGS = ('lorem', 'TODO', 'FIXME', '{{', '[[')
WORD_BOUND = re.compile(r'\b(lorem|todo|fixme)\b', re.I)


def visible_text(s):
    for tag in s.find_all(['script', 'style', 'code', 'pre']):
        tag.decompose()
    return s.get_text(' ', strip=True)


def test_no_placeholder_text():
    for f in html_files():
        if is_stub(f):
            continue
        s = BeautifulSoup(open(f, encoding='utf-8').read(), 'html.parser')
        t = visible_text(s)
        assert not WORD_BOUND.search(t), \
            '%s contains a placeholder word (%s)' % (os.path.relpath(f, PUBLIC),
                                                    WORD_BOUND.search(t).group(0))
        low = t.lower()
        for bad in ('{{', '[['):
            assert bad not in low, \
                '%s contains %r' % (os.path.relpath(f, PUBLIC), bad)


def test_readiness_scale_copy():
    """The exact readiness scale sentences appear on /method/ (the hand-written
    method page uses 'Label — sentence'; the built-in one 'Label: sentence')."""
    s = BeautifulSoup(open(os.path.join(PUBLIC, 'method', 'index.html'),
                           encoding='utf-8').read(), 'html.parser')
    t = s.get_text(' ', strip=True)
    for sentence in ('years of production use by people with real adversaries; '
                     'audited and well understood.',
                     'in production and usable today, but younger, smaller '
                     'or with known caveats.',
                     'working software, but early: small user base, '
                     'unaudited or changing fast.',
                     'papers and prototypes; not something to rely on yet.',
                     'discontinued or superseded; kept for the lessons.',
                     'works, but its trust model, governance or legal '
                     'exposure undermines what it claims.'):
        assert sentence in t, sentence[:40]


def test_no_horizontal_scroll_at_360():
    """No element may force the page wider than the viewport at 360px.
    Tables are exempt: they live inside .tw (overflow-x:auto) wrappers and
    scroll within the wrapper only."""
    css = open(os.path.join(PUBLIC, 'assets', 'css', 'site.css'),
               encoding='utf-8').read()
    for rule in re.finditer(r'([^{}]+)\{([^}]*)\}', css):
        sel, body = rule.group(1), rule.group(2)
        if '.tw table' in sel:
            continue
        for m in re.finditer(r'min-width:\s*([\d.]+)(px|rem)', body):
            val = float(m.group(1)) * (16 if m.group(2) == 'rem' else 1)
            assert val <= 480, '%s: %s' % (sel.strip(), m.group(0))


def test_all_links_clickable():
    """No link-like text should be unclickable: no bare URLs in visible text,
    no leftover wiki-link brackets. Enforced site-wide via site_check."""
    import sys
    sys.path.insert(0, os.path.join(ROOT, 'scripts'))
    import importlib, site_check
    importlib.reload(site_check)
    assert site_check.main() == 0

    bare = re.compile(r"(?<![\"'=])(https?://|www\.)[^\s<>()\[\]\"']+", re.I)
    for f in html_files():
        if is_stub(f):
            continue
        s = BeautifulSoup(open(f, encoding='utf-8').read(), 'html.parser')
        for tag in s(['script', 'style']):
            tag.decompose()
        body = s.find('body') or s
        for node in body.find_all(string=bare):
            if node.find_parent(['a', 'code', 'pre']):
                continue
            raise AssertionError('%s: bare URL %r' % (
                os.path.relpath(f, PUBLIC), bare.search(str(node)).group(0)[:50]))
        assert '[[' not in body.get_text(' '), os.path.relpath(f, PUBLIC)
