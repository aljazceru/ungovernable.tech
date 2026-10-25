"""Editorial additions must work without a legacy page for their pillar."""
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import import_directory


@pytest.mark.parametrize('missing_legacy', [False, True])
def test_additions_without_legacy_preserve_existing_output(tmp_path, monkeypatch,
                                                         missing_legacy):
    directory = tmp_path / 'content' / 'directory'
    directory.mkdir(parents=True)
    (tmp_path / 'content' / 'pillars.yml').write_text(
        '- key: anonymity\n- key: circumvention\n- key: empty\n')
    mapping = {'Tor.md': 'anonymity'}
    if missing_legacy:
        mapping['Missing.md'] = 'circumvention'
    monkeypatch.setattr(import_directory, 'ROOT', str(tmp_path))
    monkeypatch.setattr(import_directory, 'FILE_PILLAR', mapping)
    monkeypatch.setattr(import_directory, 'git_show', lambda name:
                        '## Tor\n[Tor](https://www.torproject.org/) - Tor project\n'
                        if name == 'Tor.md' else '')

    import_directory.main()
    legacy_bytes = (directory / 'anonymity.yml').read_bytes()
    assert not (directory / 'circumvention.yml').exists()

    (directory / 'overrides.yml').write_text(yaml.safe_dump({'add': {
        'circumvention': [
            {'section': 'Bridges', 'name': 'Bridge distribution',
             'url': 'https://bridges.torproject.org/', 'desc': 'Request a bridge'},
            {'section': 'Duplicate', 'name': 'Same URL',
             'url': 'https://bridges.torproject.org'},
            {'name': 'WireGuard', 'url': 'https://www.wireguard.com/'},
        ]}}))
    import_directory.main()
    assert (directory / 'anonymity.yml').read_bytes() == legacy_bytes
    assert not (directory / 'empty.yml').exists()
    result = yaml.safe_load((directory / 'circumvention.yml').read_text())
    assert result == {'pillar': 'circumvention', 'sections': [
        {'title': 'Bridges', 'items': [
            {'name': 'Bridge distribution', 'url': 'https://bridges.torproject.org/',
             'desc': 'Request a bridge'}]},
        {'title': 'Curated', 'items': [
            {'name': 'WireGuard', 'url': 'https://www.wireguard.com/', 'desc': ''}]},
    ]}
    before = {p.name: p.read_bytes() for p in directory.glob('*.yml')}
    import_directory.main()
    assert {p.name: p.read_bytes() for p in directory.glob('*.yml')} == before
