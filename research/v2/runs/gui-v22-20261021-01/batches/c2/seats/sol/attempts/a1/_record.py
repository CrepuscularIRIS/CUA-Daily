"""Local assembly/check input; not a scorer or shared project code."""
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/home/lingxufeng/GUI/cua-architecture-radar')
OUT = Path(__file__).parent
MANIFEST = json.loads((ROOT / 'research/v2/runs/gui-v22-20261021-01/batches/c2/manifest.json').read_text())
EXPECT = json.loads((ROOT / '.forge/domains/cua-agents/v1/profile/expectations.json').read_text())['expectations']
CONDITIONS = json.loads((ROOT / 'research/patterns/conditions.json').read_text())
TAX = json.loads((ROOT / 'research/patterns/taxonomy.json').read_text())
WEIGHTS = dict(zip(['G','M','X','E.measurement','E.causality','E.holdout','E.statistics','E.cost'], [15,25,20,10,10,10,5,5]))
PARENTS = dict(l.split('\t') for l in (ROOT/'research/reference/researchstudio-15-31/PARENTS.tsv').read_text().splitlines()[1:] if l)

def material(key, complete=True, sections=None):
    p = ROOT / f'research/fulltext/review-runs/gui-v22-20261021-01/fulltext/{key}.txt'
    return {'material_id': 'arxiv:'+key, 'url': 'https://arxiv.org/html/'+key, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'path': str(p.relative_to(ROOT)), 'sections_read': sections or ['entire fixed HTML text: abstract, methods, experiments, references, all rendered appendices'], 'complete':complete, 'missing_sections':[]}

def ev(key, eid, line, quote, why, kind='author_report'):
    p = ROOT / f'research/fulltext/review-runs/gui-v22-20261021-01/fulltext/{key}.txt'
    text=p.read_text(); lines=text.splitlines()
    assert quote in lines[line-1], (eid,line,quote)
    return {'evidence_id':eid,'material_id':'arxiv:'+key,'material_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'locator':f'L{line}','quote':quote,'support_explanation':why,'kind':kind}

def signature(sid,obj,info,op,output,feedback,selection,persistence,later,effect,boundary,ids):
    return dict(sig_id=sid,object=obj,information=info,operation=op,output=output,conditions='See operation, information and failure boundary; no unspecified privileged information assumed.',feedback=feedback,selection_rule=selection,selection_data=selection,persistence=persistence,later_use=later,claimed_effect=effect,failure_boundary=boundary,evidence_ids=ids)

def rs(main, sub, role, fit, steps, checks, ids, reason):
    assert sub is None or PARENTS[sub]==main
    return dict(main_id=main,sub_id=('rs:'+sub if sub else None),role=role,fit=fit,tactic_steps_checked=steps,success_failure_checks=checks,evidence_ids=ids,reason=reason)

def domain(main,sub,fit,checks,ids):
    assert sub is None or TAX['sub'][sub]['main']==main
    supplied = {a:(b,c) for a,b,c in checks}
    cc=[]
    for kind, items in CONDITIONS[main].items():
        for item in items:
            code=item['id']
            status,reason=supplied.get(code,('not_applicable','This condition concerns a different tactic under this main, not the operation or claim executed here; no score denominator is removed.'))
            cc.append(dict(id=code,type=kind,name=item['name'],status=status,reason=reason,evidence_ids=ids if status!='not_applicable' else []))
    return dict(namespace='gui',main=main,sub=sub,version='fixed-2026-10-21:'+MANIFEST['asset_hashes']['domain_taxonomy']['sha256'],fit=fit,condition_checks=cc,evidence_ids=ids)

def claim(cid,text,setting,baseline,split,result,ids,counter,conclusion):
    return dict(claim_id=cid,text=text,setting=setting,baseline_control=baseline,selection_vs_test=split,result=result,denominator=result,evidence_ids=ids,counterevidence=counter,allowed_conclusion=conclusion)

def emit(key,claim_type,central,evidence,signatures,gap,rsm,domains,mapping,expectations,claims,level,support,strongest,unresolved,rating_rows,rationale,extra_materials=()):
    paper=next(p for p in MANIFEST['papers'] if p['paper_key']==key)
    assets=MANIFEST['asset_hashes']; ids={e['evidence_id'] for e in evidence}
    ex=[]
    assert len(expectations)==35 and set(expectations)=={x['id'] for x in EXPECT}
    for item in EXPECT:
        st,reason,eids,axes=expectations[item['id']]
        ex.append(dict(id=item['id'],version='cua-agents/v1-fixed-2026-10-21',source_strength=item['strength'],source_refs=item['evidence'],applies_when=item['applies_when'],requirement=item['text'],applicable=st!='not_applicable',status=st,reason=reason,evidence_ids=eids,score_item=axes))
    ratings={}
    for axis,(num,reason,eids,counter,scope) in zip(WEIGHTS,rating_rows):
        ratings[axis]=dict(status='unknown' if num is None else ('not_reported' if num==0 and scope else 'resolved'),rating=num,reason=reason,evidence_ids=eids,counterevidence_ids=counter,search_scope=scope)
    assert len(ratings)==8
    lower=sum(WEIGHTS[k]*(v['rating'] or 0)/4 for k,v in ratings.items())
    upper=sum(WEIGHTS[k]*(4 if v['rating'] is None else v['rating'])/4 for k,v in ratings.items())
    coverage=sum(WEIGHTS[k] for k,v in ratings.items() if v['rating'] is not None)/100
    raw=lower if coverage==1 else None
    record=dict(schema_version='radar-review-v2.2',run_id=MANIFEST['run_id'],batch_id='c2',attempt_id='a1',seat='sol',paper=dict(paper_key=key,paper_id=paper['arxiv'],title=paper['title'],version=paper['version'],claim_type=claim_type,central_claim=central),provenance=dict(input_hash=MANIFEST['input_bundle_sha256'],rubric_version='v2.2-draft_uncalibrated',rubric_hash=assets['rubric']['sha256'],rs_manifest_hash=assets['rs_cards_manifest']['sha256'],domain_cards_hash=assets['domain_taxonomy']['sha256'],domain_conditions_hash=assets['domain_conditions']['sha256'],expectations_hash=assets['expectations']['sha256'],model_type='sonnet',actual_model='gpt-6.1-sol',session_id=None,receipt_ref=None,unavailable_reason='The invoking tool context provides model identity but no stable session ID or receipt path; no model probing performed.',timestamp=datetime.now(timezone.utc).isoformat(),asset_hashes=assets,scoring_boundary='Independent initial review under manifest-bound v2.2 proposed weights; rubric says draft_uncalibrated. These are provisional calibration judgments, not frozen/accepted_final production scores.'),materials=[dict(material(key),url='https://arxiv.org/html/'+paper['version'],asserted_version=paper['version'],version_binding='Version supplied by batch manifest; cached SOURCE URL is unversioned, no independent fetch/version verification performed.')]+list(extra_materials),evidence=evidence,signatures=signatures,gap=gap,rs_pattern=dict(primary=rsm[0]['main_id'] if rsm else None,supporting=[x['main_id'] for x in rsm[1:]],matches=rsm,outside_taxonomy=not bool(rsm),reason=rationale,executes_pattern=bool(rsm),resolves_problem=False),domain_pattern=dict(namespace='gui',matches=domains,unassigned=not bool(domains),revision_proposals=[]),pattern_mapping=mapping,expectations=ex,claims=claims,assessment=dict(evidence_level=level,claim_support=support,strongest_supported_claim=strongest,unresolved=unresolved,replication='author-reported results only; no code execution or independent reproduction'),ratings=ratings,score=dict(raw=raw,display=round(raw,1) if raw is not None else None,lower=lower,upper=upper,coverage=coverage,rubric_hash=assets['rubric']['sha256'],provisional=True),status='reviewed' if coverage==1 else 'needs_evidence',reason=rationale,readable_rationale=rationale)
    def check_refs(obj):
        if isinstance(obj,dict):
            for k,v in obj.items():
                if k in ('evidence_ids','counterevidence_ids'): assert all(i in ids for i in v),(key,k,v)
                check_refs(v)
        elif isinstance(obj,list):
            for v in obj: check_refs(v)
    check_refs(record)
    assert [p['material_sha256'] for p in [paper]][0] == record['materials'][0]['sha256']
    assert not (OUT/f'{key}.json').exists(), 'Do not overwrite a completed record'
    tmp=OUT/f'.{key}.json.tmp'
    tmp.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    assert json.loads(tmp.read_text())==record
    os.replace(tmp,OUT/f'{key}.json')
    print(key,'validated, atomically written',record['status'], 'score',raw)
