"""The site's Content-Security-Policy, in one place.

build.py bakes the meta-tag policy (no ``frame-ancestors`` — the meta
form does not support it) into every page and writes ``public/.csp-hash``
with the base64 sha256 of INLINE_SCRIPT. serve.py rebuilds its response
header policy (with ``frame-ancestors``) from that same file, so the two
can never drift. CSP ``'sha256-...'`` hashes are the base64 of the raw
sha256 digest — never the hex digest.

Stdlib only, so serve.py can import it without the build dependencies.
"""
import base64
import hashlib

# The single inline <script> in <head> (templates/base.html): sets the
# colour theme before first paint to avoid a flash of the wrong theme.
INLINE_SCRIPT = ('(function(){try{var t=localStorage.getItem("theme");'
                 'document.documentElement.setAttribute("data-theme",'
                 't==="light"?"light":"dark")}catch(e){'
                 'document.documentElement.setAttribute("data-theme","dark")}})();')


# Cookieless, self-hosted Plausible analytics (no cookie banner needed).
# The script is loaded from and reports events to this origin.
PLAUSIBLE_ORIGIN = 'https://analytics.cypherpunk.cloud'
PLAUSIBLE_SCRIPT = PLAUSIBLE_ORIGIN + '/js/script.js'
PLAUSIBLE_DOMAIN = 'ungovernable.tech'


def script_hash(script=INLINE_SCRIPT):
    """base64 of the raw sha256 digest — the form CSP requires."""
    return base64.b64encode(hashlib.sha256(script.encode()).digest()).decode()


def csp_policy(script_hash_b64=None, frame_ancestors=False):
    """The site policy. `script_hash_b64` is the base64 sha256 of the one
    allowed inline script; `frame_ancestors` only in the header form."""
    parts = ["default-src 'self'", "img-src 'self' data:", "style-src 'self'",
             "script-src 'self' " + PLAUSIBLE_ORIGIN]
    if script_hash_b64:
        parts[-1] += " 'sha256-%s'" % script_hash_b64
    parts += ["connect-src 'self' " + PLAUSIBLE_ORIGIN,
              "base-uri 'none'", "form-action 'none'"]
    if frame_ancestors:
        parts.append("frame-ancestors 'self'")
    return '; '.join(parts)
