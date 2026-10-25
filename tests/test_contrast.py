"""WCAG AA contrast for the theme tokens, both themes (see
scripts/contrast_check.py, which parses assets/css/site.css)."""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_contrast_both_themes():
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, 'scripts', 'contrast_check.py')],
        capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stdout + r.stderr
    # sanity: both themes actually checked
    assert 'dark (default)' in r.stdout and 'light' in r.stdout
    assert '0 problems' in r.stdout
