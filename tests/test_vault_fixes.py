"""Persistent corrections must fail on stale source text and survive re-import."""
import hashlib
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('vault_import', ROOT / 'scripts/import_vault.py')
importer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(importer)


@pytest.mark.parametrize('heading', ['Primary sources', 'Sources', None])
def test_fixes_replace_metadata_and_sources_without_removing_next_section(heading):
    body = 'Old claim.\n\n'
    if heading:
        body += f'## {heading}\n\nOld bibliography.\n\n### Detail\n\nOld detail.\n\n'
    body += '## Limits\n\nKeep this section.\n'
    entry = {'dek': 'Old claim.', 'description': 'Context. Old claim.'}
    fix = {
        'replace': [{'old': 'Old claim.', 'new': 'Verified claim.'}],
        'sources': [{'title': 'Specification', 'url': 'https://example.org/'}],
        'updated': '2026-10-25',
    }
    result = importer.apply_fixes(body, entry, fix, 'sample')
    assert result.count('## Primary sources') == 1
    assert '- [Specification](https://example.org/)' in result
    assert 'Old bibliography' not in result and 'Old detail' not in result
    assert '## Limits\n\nKeep this section.' in result
    assert entry == {'dek': 'Verified claim.', 'description': 'Context. Verified claim.',
                     'updated': '2026-10-25'}


def test_metadata_only_match_is_valid_and_stale_fix_names_target():
    entry = {'dek': 'Old subtitle.', 'description': 'Other description.'}
    fix = {'replace': [{'old': 'Old subtitle.', 'new': 'New subtitle.'}]}
    assert importer.apply_fixes('Body.', entry, fix, 'sample') == 'Body.'
    assert entry['dek'] == 'New subtitle.'
    with pytest.raises(ValueError, match='sample: old string not found'):
        importer.apply_fixes('Body.', entry, fix, 'sample')


def test_empty_sources_section_at_end_is_replaced():
    fix = {'sources': [{'title': 'Specification', 'url': 'https://example.org/'}]}
    result = importer.apply_fixes('Body.\n\n## Sources', {}, fix, 'sample')
    assert result == 'Body.\n\n## Primary sources\n\n- [Specification](https://example.org/)'


@pytest.fixture
def import_checkout(tmp_path):
    for rel in ('scripts/import_vault.py', 'scripts/vault_map.yml',
                'scripts/descriptions.yml', 'content/vault_fixes.yml',
                'content/vault_aux_fixes.yml', 'content/pillars.yml',
                'content/entries/meshcore.md'):
        destination = tmp_path / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, destination)
    return tmp_path


def snapshot(path):
    return {str(p.relative_to(path)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in path.rglob('*') if p.is_file()}


def run_import(path):
    vault = Path(os.environ.get('VAULT_PATH', '/workspace/ungovernable-tech-vault'))
    if not vault.is_dir():
        pytest.skip('Set VAULT_PATH to run corrections against the read-only source vault')
    return subprocess.run(['python3', str(path / 'scripts/import_vault.py'),
                           '--vault', str(vault)], cwd=path, capture_output=True, text=True)


def test_all_site_fixes_apply_to_vault_and_import_is_idempotent(import_checkout):
    """Every configured old string is checked against fresh transformed source."""
    original = (import_checkout / 'content/entries/meshcore.md').read_bytes()
    first = run_import(import_checkout)
    assert first.returncode == 0, first.stderr
    before = snapshot(import_checkout)
    second = run_import(import_checkout)
    assert second.returncode == 0, second.stderr
    assert snapshot(import_checkout) == before
    assert (import_checkout / 'content/entries/meshcore.md').read_bytes() == original
    # Existing hooks remain visible even when the final bibliography is replaced.
    briar = (import_checkout / 'content/entries/briar.md').read_text()
    assert importer.ENTRY_APPEND['briar'] in briar
    mesh = (import_checkout / 'content/entries/off-grid-networks.md').read_text()
    fm, _ = importer.parse_note(mesh)
    assert fm['related'] == importer.ENTRY_RELATED['off-grid-networks']
    glossary = yaml.safe_load((import_checkout / 'content/glossary.yml').read_text())
    lora = next(term for term in glossary if term['slug'] == 'lora')
    assert lora['definition_md'] == importer.GLOSSARY_DEF['lora']
    assert 'meshcore' in lora['see']


@pytest.mark.parametrize('case', ['stale', 'unknown-slug', 'original'])
def test_invalid_fix_exits_nonzero_before_writing(import_checkout, case):
    fixes = import_checkout / 'content/vault_fixes.yml'
    if case == 'stale':
        data = {'briar': {'replace': [{'old': 'This deliberately missing sentence must fail.',
                                     'new': 'Never written.'}]}}
        expected = 'old string not found'
    elif case == 'unknown-slug':
        data = {'no-such-vault-slug': {'updated': '2026-10-25'}}
        expected = 'no mapped vault source'
    else:
        data = {'briar': {'updated': '2026-10-25'}}
        (import_checkout / 'content/entries/briar.md').write_text(
            '---\norigin: original\nslug: briar\n---\nKeep this original.\n')
        expected = 'origin: original'
    fixes.write_text(yaml.safe_dump(data))
    before = snapshot(import_checkout)
    result = run_import(import_checkout)
    assert result.returncode != 0
    assert 'WARN:' in result.stderr and expected in result.stderr
    assert snapshot(import_checkout) == before
