"""Local record assembly and deterministic checks for this attempt only."""
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/home/lingxufeng/GUI/cua-architecture-radar')
OUT = ROOT / 'research/v2/runs/gui-v22-20261021-01/batches/p1/seats/sol/attempts/a1'
MANIFEST = json.loads((ROOT / 'research/v2/runs/gui-v22-20261021-01/batches/p1/manifest.json').read_text())
EXPECTATIONS = json.loads((ROOT / '.forge/domains/cua-agents/v1/profile/expectations.json').read_text())['expectations']
WEIGHTS = dict(zip(['G', 'M', 'X', 'E.measurement', 'E.causality', 'E.holdout', 'E.statistics', 'E.cost'], [15,25,20,10,10,10,5,5]))
TAXONOMY = json.loads((ROOT / 'research/patterns/taxonomy.json').read_text())


def evidence(paper: dict, specs: list) -> list:
    """Bind hand-selected continuous quotations to exact material lines."""
    text = (ROOT / paper['fulltext_path']).read_text()
    result = []
    for i, (quote, explanation) in enumerate(specs, 1):
        assert quote in text, (paper['paper_key'], quote)
        start = text.index(quote)
        line = text[:start].count('\n') + 1
        end = line + quote.count('\n')
        result.append(dict(evidence_id=f'E{i:03d}', material_id=paper['version'], material_sha256=paper['material_sha256'], locator=f'{paper["fulltext_path"]}:L{line}-L{end}', quote=quote, support_explanation=explanation, kind='author_report'))
    return result


def signature(number: int, obj: str, information: str, operation: str, output: str, conditions: str, feedback: str, selection: str, persistence: str, later_use: str, effect: str, failure: str, ids: list) -> dict:
    return dict(sig_id=f'S{number}', object=obj, information=information, operation=operation, output=output, conditions=conditions, feedback=feedback, selection_rule=selection, selection_data=feedback, persistence=persistence, later_use=later_use, claimed_effect=effect, failure_boundary=failure, evidence_ids=ids)


def rs_match(main: str, sub: str | None, role: str, fit: str, steps: list, checks: list, ids: list, reason: str) -> dict:
    return dict(main_id=main, sub_id=sub, role=role, fit=fit, tactic_steps_checked=steps, success_failure_checks=checks, evidence_ids=ids, reason=reason)


def domain(main: str, sub: str | None, fit: str, checks: list, ids: list) -> dict:
    return dict(main=main, sub=sub, version='manifest-bound-2026-10-21', fit=fit, condition_checks=checks, evidence_ids=ids)


def claim(number: int, text: str, setting: str, control: str, split: str, result: str, denominator: str, ids: list, counter: list, conclusion: str) -> dict:
    return dict(claim_id=f'C{number}', text=text, setting=setting, baseline_control=control, selection_vs_test=split, result=result, denominator=denominator, evidence_ids=ids, counterevidence=counter, allowed_conclusion=conclusion)


def expectation_records(decisions: dict, exclusions: dict, default_reason: str) -> list:
    """Keep every fixed expectation; judgments remain paper-specific inputs."""
    results = []
    for x in EXPECTATIONS:
        ident = x['id']
        if ident in decisions:
            status, reason, refs, item = decisions[ident]
            applicable = True
        else:
            status = 'not_applicable'
            reason = exclusions.get(ident, default_reason + ' Specific trigger not present: ' + x['applies_when'] + '.')
            refs, item, applicable = [], 'X', False
        results.append(dict(id=ident, version='manifest-bound-2026-10-21', source_strength=x['strength'], source_refs=x['evidence'], source_interpretation='Fixed-profile paper practices/limitations, not actual reviews of this paper; cited originals not all independently reread.', applies_when=x['applies_when'], applicable=applicable, status=status, reason=reason, evidence_ids=refs, score_item=item))
    assert len(results) == 35
    return results


def write_record(key: str, content: dict, quote_specs: list, rating_specs: list) -> dict:
    paper = next(x for x in MANIFEST['papers'] if x['paper_key'] == key)
    assert hashlib.sha256((ROOT / paper['fulltext_path']).read_bytes()).hexdigest() == paper['material_sha256']
    a = MANIFEST['asset_hashes']
    for asset in a.values():
        assert hashlib.sha256((ROOT / asset['path']).read_bytes()).hexdigest() == asset['sha256']
    ratings = {}
    for axis, (number, reason, refs, counters) in zip(WEIGHTS, rating_specs):
        ratings[axis] = dict(status='unknown' if number is None else 'resolved', rating=number, reason=reason, evidence_ids=refs, counterevidence_ids=counters, search_scope=[paper['fulltext_path'] + ': entire textual body, experiments, limitations, references and available appendices'])
    assert len(rating_specs) == 8
    lower = sum(WEIGHTS[k] * (v['rating'] or 0) / 4 for k, v in ratings.items())
    upper = sum(WEIGHTS[k] * (4 if v['rating'] is None else v['rating']) / 4 for k, v in ratings.items())
    coverage = sum(WEIGHTS[k] for k, v in ratings.items() if v['rating'] is not None) / 100
    score = dict(raw=lower if coverage == 1 else None, display=round(lower, 1) if coverage == 1 else None, lower=lower, upper=upper, coverage=coverage, rubric_hash=a['rubric']['sha256'], interpretation='Independent seat judgment under the assigned hash-bound draft v2.2 weights; calibration changes require a new rubric version and affected-paper re-review.')
    record = dict(schema_version='radar-review-v2.2', run_id=MANIFEST['run_id'], batch_id='p1', attempt_id='a1', seat='sol')
    record['paper'] = dict(paper_key=key, paper_id=paper['arxiv'], title=paper['title'], version=paper['version'], claim_type=content.pop('claim_type'), central_claim=content.pop('central_claim'))
    record['provenance'] = dict(input_hash=MANIFEST['input_bundle_sha256'], rubric_version='radar-review-v2.2 draft_uncalibrated', rubric_hash=a['rubric']['sha256'], rs_manifest_hash=a['rs_cards_manifest']['sha256'], domain_cards_hash=a['domain_taxonomy']['sha256'], domain_conditions_hash=a['domain_conditions']['sha256'], expectations_hash=a['expectations']['sha256'], pattern_protocol_hash=a['pattern_protocol']['sha256'], model_type='sonnet', actual_model='gpt-6.1-sol', actual_model_source='Environment explicitly reports gpt-6.1-sol; no model probing performed.', session_id='681194da-49f5-4ad4-8eb4-573b45384076', receipt_ref='/home/lingxufeng/.claude-kimi/projects/-home-lingxufeng-GUI/681194da-49f5-4ad4-8eb4-573b45384076.jsonl', timestamp=datetime.now(timezone.utc).isoformat(), rubric_caveat='Supplied SCORE_SPEC remains draft_uncalibrated. Controller directs parallel calibration/production with these hash-bound weights; any changed anchors require affected papers to be reviewed under a new version.', material_version_caveat='SHA256 matches assigned manifest. Source header is unversioned arXiv HTML; manifest version retained, exact HTML-to-version correspondence not independently established.')
    record['materials'] = [dict(material_id=paper['version'], url='https://arxiv.org/abs/' + paper['version'], version=paper['version'], path=paper['fulltext_path'], sha256=paper['material_sha256'], sections_read=content.pop('sections_read'), complete=True, missing_sections=[], visual_asset_caveat='Text render contains captions and tables; plotted/diagrammed images were not independently viewed. Unrendered numerical values are not inferred.', version_verified=False)]
    record['materials'][0].update(content.pop('material_overrides', {}))
    record['evidence'] = evidence(paper, quote_specs)
    record.update(content)
    record['ratings'] = ratings
    record['score'] = score
    record.setdefault('status', 'reviewed')
    record.setdefault('reason', 'Complete supplied textual paper reviewed independently; evidence is scoped and author-reported, not a reproduction. Rubric version is hash-bound.')
    validate(record)
    target = OUT / (key + '.json')
    assert not target.exists(), 'Do not silently replace an existing completed record'
    temp = OUT / (key + '.json.tmp')
    temp.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    json.loads(temp.read_text())
    os.replace(temp, target)
    return record


def validate(record: dict) -> None:
    ids = {e['evidence_id'] for e in record['evidence']}
    assert len(ids) == len(record['evidence'])
    for s in record['signatures']:
        assert set(s['evidence_ids']) <= ids
    assert len(record['expectations']) == 35
    assert {x['id'] for x in record['expectations']} == {x['id'] for x in EXPECTATIONS}
    for x in record['expectations']:
        assert x['reason'] and set(x['evidence_ids']) <= ids
    for x in record['ratings'].values():
        assert x['reason'] and set(x['evidence_ids'] + x['counterevidence_ids']) <= ids
        assert x['rating'] is None or (type(x['rating']) is int and 0 <= x['rating'] <= 4)
        assert (x['status'] == 'unknown') == (x['rating'] is None)
    assert record['domain_pattern']['namespace'] == 'gui'
    for x in record['domain_pattern']['matches']:
        assert x['main'] in {m['id'] for m in TAXONOMY['main']}
        if x['sub'] is not None:
            assert TAXONOMY['sub'][x['sub']]['main'] == x['main']
    parents = {}
    for line in (ROOT / 'research/reference/researchstudio-15-31/PARENTS.tsv').read_text().splitlines():
        parts = line.split('\t')
        if len(parts) >= 2:
            parents[parts[0]] = parts[1]
    rs = record['rs_pattern']
    assert len(rs['supporting']) <= 2
    if rs['outside_taxonomy']:
        assert rs['primary'] is None and not rs['matches'] and not rs['supporting'] and rs['reason']
    for x in rs['matches']:
        if x['sub_id'] is not None:
            assert parents[x['sub_id']] == x['main_id'], (x, parents)
    for x in record['claims']:
        assert set(x['evidence_ids']) <= ids
    assert sum(WEIGHTS.values()) == 100
