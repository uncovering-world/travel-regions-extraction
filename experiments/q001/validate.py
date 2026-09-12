#!/usr/bin/env python3
"""Validate Q001 references, witness discipline, open-world fixtures, blind payload and dates."""
import json,pathlib,re
p=pathlib.Path(__file__).resolve().parent
load=lambda f:json.loads((p/f).read_text())
u={x['id']:x for x in (json.loads(f.read_text()) for f in (p/'facts').glob('*.json'))}
e={x['id']:x for x in load('evidence.json')['evidence']};s={x['id']:x for x in load('sources.json')['sources']}
c=load('comparisons.yaml')['comparisons'];b=load('blind-comparisons.yaml');key=load('blind-answer-key.json')
fixtures=load('evaluator-fixtures.yaml')['fixtures']
checks=[]
def ok(condition,message):
 assert condition,message
 checks.append(message)
def walk(x):
 yield x
 if isinstance(x,dict):
  for v in x.values():yield from walk(v)
 elif isinstance(x,list):
  for v in x:yield from walk(v)
ok(len(c)==49 and len(u)==56,'49 cases / 56 supporting factual units')
ok(len(b['comparisons'])==12,'12 blind comparisons')
for x in e.values():
 ok(bool(x['source_refs']) and all(i in s for i in x['source_refs']),f"{x['id']}: source provenance")
 ok(x['checked_on']=='2026-09-11' and bool(x['observed_as_of']),f"{x['id']}: check and observation dates separate")
for x in u.values():
 ok(x['temporal']['as_of']=='2026-09-11',f"{x['id']}: snapshot")
 for v in walk(x):
  if not isinstance(v,dict):continue
  if 'value' in v:ok(v['value']=='unknown' or bool(v.get('evidence_refs')),f"{x['id']}: substantive field provenance")
  for r in v.get('evidence_refs',[]):ok(r in e,f'{r}: existing evidence')
  for r in v.get('source_refs',[]):ok(r in s,f'{r}: existing source')
for x in c:
 ok(x['a'] in u and x['b'] in u,f"{x['id']}: endpoints")
 ok(x['questions']['territorial_identity_candidate']=='unresolved',f"{x['id']}: identity unresolved")
 ok(x['questions']['regime_difference']!='false',f"{x['id']}: no unsourced global equality")
 ok('Q001' in x['model_questions'],f"{x['id']}: general identity question is Q001")
 if x['questions']['regime_difference'] is True:
  ok(bool(x['witnesses']),f"{x['id']}: positive witness")
  for w in x['witnesses']:
   ok(w['decision_a']!=w['decision_b'] and w['status']=='verified',f"{x['id']}: verified differing component")
   ok(all(k in w['context'] for k in ['nationality','document','authorisations','residence_permit','arrival_mode','route_class']),f"{x['id']}: specified context")
forbidden=['canonical_region','canonical_verdict','merge_decision','split_decision','country']
for x in list(u.values())+c:
 ok(not any(k in d for d in walk(x) if isinstance(d,dict) for k in forbidden),'No country or canonical decision field')
required={('de','fr'),('fi','ax'),('it','sic'),('pt','mad'),('uk','je'),('uk','bm'),('fr','re'),('ma','wsw'),('cn','tar'),('in','ld'),('pk','gb'),('cn','ac')}
disputed_q006={'C031','C032','C033','C034','C035','C036','C037','C038','C039','C040','C042','C043','C044','C045','C046','C047','C048','C049'}
ok({x['id'] for x in c if 'Q006' in x['model_questions']}==disputed_q006,'Q006 restricted to disputed/status comparisons')
reverse={v:k for k,v in key['unit_ids'].items()}
ok({(reverse[x['a']],reverse[x['b']]) for x in b['comparisons']}==required,'Blind mandatory coverage exact')
strings='\n'.join(x for x in walk(b) if isinstance(x,str))
ok('http' not in strings.lower(),'Blind payload has no source URLs')
for name in key['entity_aliases']:
 ok(re.search(r'(?<!\w)'+re.escape(name)+r'(?!\w)',strings,re.I) is None,f'Blind name removed: {name}')
# Structure and literal booleans/numbers are preserved under aliasing.
def shape(x):
 if isinstance(x,dict):return {k:shape(v) for k,v in x.items()}
 if isinstance(x,list):return [shape(v) for v in x]
 return '<str>' if isinstance(x,str) else x
original={x['id']:x for x in c}
for old,new in key['comparison_ids'].items():
 blind=next(x for x in b['comparisons'] if x['id']==new)
 ok(shape(original[old])==shape(blind),f'{old}: blind structure preserved')
for old,new in key['unit_ids'].items():
 blind=next(x for x in b['units'] if x['id']==new)
 ok(shape(u[old])==shape(blind),f'{old}: blind fact structure preserved')
ok(10 <= len(fixtures) <= 20,'10–20 evaluator fixtures')
allowed_results={'must_separate','may_merge','separation_not_proven','model_unresolved','data_unknown','rule_conflict'}
for f in fixtures:
 ok(bool(f['id']) and bool(f.get('expected')),f"{f['id']}: fixture identity and oracle")
 for profile,expected in f['expected'].items():
  ok(profile in {'P1','P2','P3'} and expected['result'] in allowed_results,f"{f['id']}/{profile}: valid pairwise outcome")
  sig=expected.get('signature',{})
  if expected['result']=='may_merge' and sig:
   ok(sig.get('a_complete') is True and sig.get('b_complete') is True and sig.get('equal') is True,f"{f['id']}/{profile}: may_merge requires complete equal signature")
result={'status':'PASS','checks_passed':len(checks),'comparison_count':len(c),'unit_count':len(u),'positive_regime_witness_comparisons':[x['id'] for x in c if x['questions']['regime_difference'] is True],'scope':'Structural and editorial invariants; not independent legal verification.'}
print(json.dumps(result,ensure_ascii=False,indent=2))
