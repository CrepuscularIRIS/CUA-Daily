"""Local atomic record assembly; does not execute research code."""
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/home/lingxufeng/GUI/cua-architecture-radar')
OUT = ROOT / 'research/v2/runs/gui-v22-20261021-01/batches/c1/seats/sol/attempts/a1'
MAN = json.loads((ROOT / 'research/v2/runs/gui-v22-20261021-01/batches/c1/manifest.json').read_text())
EXPS = json.loads((ROOT / '.forge/domains/cua-agents/v1/profile/expectations.json').read_text())['expectations']
WEIGHTS = {'G':15,'M':25,'X':20,'measurement':10,'causality':10,'holdout':10,'statistics':5,'cost':5}

def base(key, claim_type=None, central_claim=None):
    p = next(p for p in MAN['papers'] if p['paper_key'] == key)
    assets = MAN['asset_hashes']
    return {'schema_version':'radar-review-v2.2','run_id':MAN['run_id'],'batch_id':'c1','attempt_id':'a1','seat':'sol',
      'paper':{'paper_key':key,'paper_id':p['arxiv'],'title':p['title'],'version':p['version'],'claim_type':claim_type,'central_claim':central_claim},
      'provenance':{'input_hash':MAN['input_bundle_sha256'],'rubric_version':'v2.2 draft_uncalibrated','rubric_hash':assets['rubric']['sha256'],'rs_manifest_hash':assets['rs_cards_manifest']['sha256'],'domain_cards_hash':assets['domain_taxonomy']['sha256'],'domain_conditions_hash':assets['domain_conditions']['sha256'],'expectations_hash':assets['expectations']['sha256'],'asset_hashes':assets,'model_type':'sonnet','actual_model':'gpt-6.1-sol','session_id':None,'receipt_ref':None,'unavailable_reason':'Session identifier and invocation receipt are not exposed in this worker context. Actual model is supplied in the system environment.','timestamp':datetime.now(timezone.utc).isoformat(),'score_use':'Independent provisional calibration assessment; not a frozen production ranking.'},
      'materials':[{'material_id':'P','url':'https://arxiv.org/html/'+p['version'],'sha256':p['material_sha256'],'path':p['fulltext_path'],'material_status':p['material_status'],'sections_read':[],'complete':False,'missing_sections':[]}],
      'evidence':[],'signatures':[],'gap':{},'rs_pattern':{},'domain_pattern':{'namespace':'gui','matches':[],'unassigned':[],'revision_proposals':[]},'pattern_mapping':[],'expectations':[],'claims':[],'assessment':{},'ratings':{},'score':None}

def ev(r, eid, line, quote=None, explanation='', end=None):
    text = (ROOT / r['materials'][0]['path']).read_text()
    lines = text.splitlines()
    q = quote if quote is not None else '\n'.join(lines[line-1:(end or line)])
    assert q and q in text, (eid, q)
    assert q in '\n'.join(lines[line-1:(end or line)]), (eid, line)
    r['evidence'].append({'evidence_id':eid,'material_id':'P','material_hash':r['materials'][0]['sha256'],'locator':f'L{line}'+(f'-L{end}' if end else ''),'quote':q,'support_explanation':explanation,'kind':'author_report'})

def expect(r, answers, na_reason):
    for e in EXPS:
        a = answers.get(e['id'])
        r['expectations'].append({'id':e['id'],'version':'cua-agents/v1','source_strength':e['strength'],'source_refs':e['evidence'],'applies_when':e['applies_when'],'applicable':a is not None,'status':a[0] if a else 'not_applicable','reason':a[1] if a else na_reason[e['id']] if isinstance(na_reason,dict) else na_reason,'evidence_ids':a[2] if a else [],'score_item':a[3] if a else []})

def rate(r, vals):
    rr={}
    for k,(n,reason,ids,counter) in vals.items():
        rr[k]={'status':'resolved','rating':n,'reason':reason,'evidence_ids':ids,'counterevidence_ids':counter,'search_scope':[{'material_id':'P','scope':'Entire fixed full text, including all rendered methods, experiments, references and appendices; no paper code executed.'}]}
    r['ratings']={k:rr[k] for k in ['G','M','X']}
    r['ratings']['E']={k:rr[k] for k in ['measurement','causality','holdout','statistics','cost']}
    raw=sum(WEIGHTS[k]*rr[k]['rating'] for k in WEIGHTS)/4
    r['score']={'raw':raw,'display':float(f'{raw:.1f}'),'lower':raw,'upper':raw,'coverage':1.0,'rubric_hash':MAN['asset_hashes']['rubric']['sha256'],'provisional':True}

def save(r):
    p=next(p for p in MAN['papers'] if p['paper_key']==r['paper']['paper_key'])
    if p['fulltext_path']:
        assert hashlib.sha256((ROOT/p['fulltext_path']).read_bytes()).hexdigest()==p['material_sha256']
    assert len(r['expectations'])==35 or r['status']=='needs_fulltext'
    ids={e['evidence_id'] for e in r['evidence']}
    for e in r['expectations']: assert set(e['evidence_ids'])<=ids
    data=json.dumps(r,ensure_ascii=False,indent=2)+'\n'
    tmp=OUT/(p['paper_key']+'.json.tmp')
    dest=OUT/(p['paper_key']+'.json')
    assert not dest.exists(), 'Do not overwrite an already completed record'
    tmp.write_text(data)
    assert json.loads(tmp.read_text())==r
    os.replace(tmp,dest)
