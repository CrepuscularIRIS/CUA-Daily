"""Read-only consistency checks for frozen pattern assets; not a semantic/research review."""
import json
import sys
from pathlib import Path


def check(root: Path) -> list[str]:
    errors = []
    base = root / 'research/patterns'
    taxonomy = json.loads((base / 'taxonomy.json').read_text())
    view = json.loads((base / 'taxonomy_view.json').read_text())
    conditions = json.loads((base / 'conditions.json').read_text())
    mains = [m['id'] for m in taxonomy['main']]
    parents = {}
    if len(mains) != len(set(mains)):
        errors.append('duplicate main pattern id')
    for main in taxonomy['main']:
        for sub in main['subs']:
            if sub in parents:
                errors.append(f'duplicate sub pattern id: {sub}')
            parents[sub] = main['id']
    for folder, expected in [('main', set(mains)), ('sub', set(parents))]:
        actual = {p.stem for p in (root / 'patterns' / folder).glob('*.md')}
        if actual != expected:
            errors.append(f'{folder} cards mismatch: missing={sorted(expected-actual)}, extra={sorted(actual-expected)}')
    if set(conditions) != set(mains):
        errors.append('conditions main ids differ from taxonomy')
    seen = set()
    for row in view:
        sub = row['sub']
        if sub in seen or parents.get(sub) != row['main']:
            errors.append(f'taxonomy_view duplicate or wrong parent: {sub}')
        seen.add(sub)
    if seen != set(parents):
        errors.append('taxonomy_view sub ids differ from taxonomy')
    for main, groups in conditions.items():
        path = root / 'patterns/main' / f'{main}.md'
        if not path.exists():
            continue
        text = path.read_text()
        for group in ['S', 'F']:
            items = groups.get(group, [])
            if not items or [x['id'] for x in items] != [f'{group}{i+1}' for i in range(len(items))]:
                errors.append(f'{main}: empty or nonsequential {group} ids')
            for item in items:
                if not item.get('name') or item['name'] not in text:
                    errors.append(f'{main}/{item["id"]}: condition name missing from card')
    return errors


def main() -> int:
    if len(sys.argv) > 1:
        print('This checker is read-only and accepts no mutation flags.', file=sys.stderr)
        return 2
    root = Path(__file__).resolve().parents[1]
    try:
        errors = check(root)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'Invalid or missing pattern inputs: {exc}', file=sys.stderr)
        return 1
    for error in errors:
        print(error)
    print(f'Pattern structure: {len(errors)} problems; no semantic or outcome-label validation claimed.')
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
