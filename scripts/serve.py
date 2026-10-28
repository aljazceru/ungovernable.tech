#!/usr/bin/env python3
"""Production static server for ungovernable.tech (stdlib + scripts/csp.py).

Adds what `python3 -m http.server` lacks: gzip, Cache-Control, ETag/304,
real 301s for the legacy redirect stubs (one hop), correct MIME types,
a real 404 status with the 404 page, and security headers including a
Content-Security-Policy built by scripts/csp.py from the hash of the
single inline theme script (public/.csp-hash, written by build.py;
base64 of the raw sha256 digest).

Usage: python3 serve.py [--port 8000] [--root public]
"""
import argparse
import email.utils
import gzip
import hashlib
import mimetypes
import os
import posixpath
import re
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import csp  # scripts/csp.py — the one place the policy is defined

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TYPES = {'.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8',
         '.js': 'text/javascript; charset=utf-8', '.json': 'application/json; charset=utf-8',
         '.xml': 'application/xml; charset=utf-8', '.txt': 'text/plain; charset=utf-8',
         '.md': 'text/markdown; charset=utf-8', '.svg': 'image/svg+xml',
         '.webmanifest': 'application/manifest+json; charset=utf-8', '.woff2': 'font/woff2',
         '.png': 'image/png', '.ico': 'image/x-icon', '.jpg': 'image/jpeg', '.webp': 'image/webp'}
COMPRESS = {'.html', '.css', '.js', '.json', '.xml', '.txt', '.md', '.svg', '.webmanifest'}
REFRESH = re.compile(rb'<meta http-equiv="refresh" content="0; url=([^"]+)"')
CACHE = {}  # path -> (mtime, size, body, gz, etag, redirect)


def load_csp(root):
    """Header CSP for serve.py: the shared policy plus frame-ancestors
    (header-only; the meta form in the built pages omits it). The script
    hash comes from public/.csp-hash so build and serve cannot drift."""
    hp = os.path.join(root, '.csp-hash')
    h = open(hp, encoding='utf-8').read().strip() if os.path.exists(hp) else ''
    return csp.csp_policy(h or None, frame_ancestors=True)


def load(path):
    st = os.stat(path)
    hit = CACHE.get(path)
    if hit and hit[0] == st.st_mtime and hit[1] == st.st_size:
        return hit
    body = open(path, 'rb').read()
    ext = os.path.splitext(path)[1]
    redirect = None
    if ext == '.html' and len(body) < 2000:
        m = REFRESH.search(body)
        if m:
            redirect = m.group(1).decode()
    gz = gzip.compress(body, 6, mtime=0) if ext in COMPRESS and len(body) > 512 else None
    etag = '"' + hashlib.md5(body).hexdigest()[:16] + '"'
    CACHE[path] = hit = (st.st_mtime, st.st_size, body, gz, etag, redirect)
    return hit


class H(BaseHTTPRequestHandler):
    server_version = 'ungovernable'
    protocol_version = 'HTTP/1.1'
    sys_version = ''
    root = '.'
    csp = ''

    def log_message(self, fmt, *a):
        pass

    def do_HEAD(self):
        self.serve(head=True)

    def do_GET(self):
        self.serve()

    def resolve(self, upath):
        p = posixpath.normpath(urllib.parse.unquote(upath))
        if '\x00' in p:
            return None
        parts = [x for x in p.split('/') if x and x not in ('.', '..')]
        return os.path.join(self.root, *parts)

    def common(self):
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'strict-origin-when-cross-origin')
        self.send_header('X-Frame-Options', 'SAMEORIGIN')
        self.send_header('Content-Security-Policy', self.csp)
        self.send_header('Permissions-Policy',
                         'interest-cohort=(), camera=(), microphone=(), geolocation=()')

    def redirect(self, loc):
        self.send_response(301)
        self.send_header('Location', loc)
        self.send_header('Cache-Control', 'public, max-age=86400')
        self.send_header('Content-Length', '0')
        self.common()
        self.end_headers()

    def serve(self, head=False):
        url = urllib.parse.urlsplit(self.path)
        host = (self.headers.get('Host') or '').split(':')[0].lower()
        # one canonical host: www -> apex, path and query kept
        if host.startswith('www.') and host.endswith('ungovernable.tech'):
            return self.redirect('https://%s%s%s' % (
                host[4:], url.path, ('?' + url.query) if url.query else ''))
        fs = self.resolve(url.path)
        if fs and os.path.isdir(fs):
            if not url.path.endswith('/'):
                return self.redirect(url.path + '/' + (('?' + url.query) if url.query else ''))
            fs = os.path.join(fs, 'index.html')
        status = 200
        if not fs or not os.path.isfile(fs):
            status, fs = 404, os.path.join(self.root, '404.html')
        mtime, size, body, gz, etag, redirect = load(fs)
        if redirect and status == 200:
            return self.redirect(urllib.parse.urljoin(url.path, redirect))
        ext = os.path.splitext(fs)[1]
        if status == 200 and self.headers.get('If-None-Match') == etag:
            self.send_response(304)
            self.send_header('ETag', etag)
            self.common()
            self.end_headers()
            return
        rel = os.path.relpath(fs, self.root).replace(os.sep, '/')
        if status == 404:
            cc = 'no-store'
        elif rel.startswith(('assets/fonts/', 'assets/og/')) or \
                (url.query.startswith('v=') and ext in ('.css', '.js')):
            cc = 'public, max-age=31536000, immutable'
        elif ext in ('.css', '.js', '.png', '.ico', '.svg', '.webmanifest'):
            cc = 'public, max-age=86400'
        elif ext == '.html':
            cc = 'public, max-age=300, must-revalidate'
        else:
            cc = 'public, max-age=3600'
        use_gz = gz is not None and 'gzip' in (self.headers.get('Accept-Encoding') or '')
        data = gz if use_gz else body
        self.send_response(status)
        self.send_header('Content-Type',
                         TYPES.get(ext) or mimetypes.guess_type(fs)[0] or 'application/octet-stream')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', cc)
        if status == 200:
            self.send_header('ETag', etag)
            self.send_header('Last-Modified', email.utils.formatdate(mtime, usegmt=True))
        if gz is not None:
            self.send_header('Vary', 'Accept-Encoding')
        if use_gz:
            self.send_header('Content-Encoding', 'gzip')
        if rel in ('llms.txt', 'robots.txt') or rel.startswith('assets/search'):
            self.send_header('Access-Control-Allow-Origin', '*')
        self.common()
        self.end_headers()
        if not head:
            self.wfile.write(data)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--port', type=int, default=8000)
    ap.add_argument('--bind', default='0.0.0.0')
    ap.add_argument('--root', default=os.path.join(ROOT, 'public'))
    a = ap.parse_args()
    H.root = os.path.abspath(a.root)
    H.csp = load_csp(H.root)
    ThreadingHTTPServer((a.bind, a.port), H).serve_forever()


if __name__ == '__main__':
    main()
