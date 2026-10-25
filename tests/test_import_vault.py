"""Persistent site glossary additions must survive repeated vault imports."""
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import import_vault


def test_site_glossary_terms_override_matching_vault_slug_without_duplicates():
    note = '**Bridge** — A source definition to replace.\n' \
           '**Unrelated** — Preserve this definition.\n'
    first = import_vault.parse_glossary(note, None, Counter())
    assert first == import_vault.parse_glossary(note, None, Counter())
    assert len([t for t in first if t['slug'] == 'bridge']) == 1
    terms = {t['slug']: t for t in first}
    assert terms['bridge']['see'] == ['tor', 'pluggable-transports']
    assert 'public relay directory' in terms['bridge']['definition_md']
    assert terms['unrelated']['definition_md'] == 'Preserve this definition.'
    assert 'deep-packet-inspection-dpi' in terms
    assert 'pluggable-transport' in terms
    # Parsing must not expose mutable editorial constants to its callers.
    terms['bridge']['see'].clear()
    assert next(t for t in import_vault.parse_glossary(note, None, Counter())
                if t['slug'] == 'bridge')['see'] == ['tor', 'pluggable-transports']
