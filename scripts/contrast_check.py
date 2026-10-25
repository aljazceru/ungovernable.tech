#!/usr/bin/env python3
"""Assert WCAG AA contrast for the site's CSS custom properties, in BOTH
themes (dark default and light opt-in).

Parses the token blocks in assets/css/site.css and checks the key pairs:
ink/bg, ink-2/bg, muted/bg, prose/bg, signal/bg (links), signal/surface,
badge text/badge background for each readiness badge, and the on-fill inks.
Body-size text pairs must reach 4.5:1; anything that only ever renders as
large text or UI chrome would be allowed 3:1, but every pair asserted here
is used at body size somewhere, so all are held to 4.5:1.

Usage: python3 scripts/contrast_check.py   (exit 1 on any failure)
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS = os.path.join(ROOT, 'assets', 'css', 'site.css')

# (foreground token, background token) — all held to 4.5:1
PAIRS = [
    ('ink', 'bg'), ('ink-2', 'bg'), ('muted', 'bg'), ('prose', 'bg'),
    ('signal', 'bg'), ('signal', 'surface'), ('signal', 'raised'),
    ('muted', 'surface'), ('ink', 'surface'), ('ink-2', 'surface'),
    # readiness badges: text on its own badge background
    ('signal-ink', 'signal'),      # battle-tested (solid signal fill)
    ('signal', 'bg'),              # usable (outline)
    ('amber', 'bg'),               # experimental (outline)
    ('cyan', 'bg'),                # research (outline)
    ('grey', 'bg'),                # historical (outline)
    ('red-ink', 'red'),            # cautionary (solid red fill)
    ('red', 'bg'),                 # cautionary text used standalone
]

THEMES = [
    ('dark (default)', r':root\s*\{([^}]*)\}'),
    ('light', r':root\[data-theme="light"\]\s*\{([^}]*)\}'),
]


def luminance(hexcolor):
    h = hexcolor.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

    def lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast(fg, bg):
    l1, l2 = luminance(fg), luminance(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def tokens(block):
    out = {}
    for name, value in re.findall(r'(--[\w-]+)\s*:\s*([^;]+);', block):
        m = re.match(r'#([0-9a-fA-F]{3,6})\b', value.strip())
        if m:
            out[name[2:]] = '#' + m.group(1)
    return out


def main():
    css = open(CSS, encoding='utf-8').read()
    problems, rows = [], []
    for theme_name, pattern in THEMES:
        m = re.search(pattern, css)
        if not m:
            problems.append('could not find token block for %s theme' % theme_name)
            continue
        tok = tokens(m.group(1))
        for fg, bg in PAIRS:
            if fg not in tok:
                problems.append('%s: token --%s missing' % (theme_name, fg))
                continue
            if bg not in tok:
                problems.append('%s: token --%s missing' % (theme_name, bg))
                continue
            ratio = contrast(tok[fg], tok[bg])
            ok = ratio >= 4.5
            rows.append((theme_name, fg, bg, tok[fg], tok[bg], ratio, ok))
            if not ok:
                problems.append('%s: %s on %s = %.2f:1 (need 4.5)'
                                % (theme_name, fg, bg, ratio))
    w = max(len(r[1]) for r in rows) if rows else 4
    for theme_name, fg, bg, fgv, bgv, ratio, ok in rows:
        print('%-16s %-*s on %-12s %s on %s  %6.2f:1  %s'
              % (theme_name, w, fg, bg, fgv, bgv, ratio, 'ok' if ok else 'FAIL'))
    print('%d pairs checked, %d problems' % (len(rows), len(problems)))
    for p in problems:
        print('BAD', p)
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
