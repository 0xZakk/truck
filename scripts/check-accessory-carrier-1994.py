"""Frozen independent1994 carrier topology/fit check; never installs candidate."""
import hashlib,itertools,json,sys,tempfile
from pathlib import Path
import build123d as cad
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import accessory_carrier_1994 as c
from assembly_math import transforms
raw=(ROOT/'inventory/engine/full-assembly.json').read_bytes();m=json.loads(raw);poses=transforms(m);defs={d['id']:d for d in m['definitions']}
paths=[Path(c.__file__),ROOT/'cad/engine/accessory_brackets.py',ROOT/'cad/engine/tensioner_arm.py',ROOT/'cad/engine/tensioner_pulley.py',ROOT/'cad/engine/tensioner_engine_support.py',Path(__file__)]
frozen={str(p.relative_to(ROOT)):p.read_bytes() for p in paths}
parts=c.parts();cache={};adapted={};additions={}
for identifier,adapter in [('block',c.block_interface),('cylinder-head',c.head_interface)]:
 old=cad.import_step(ROOT/defs[identifier]['step'].lstrip('/'))
 new=adapter(old);adapted[identifier]=new.moved(poses[identifier]);addition=new-old
 if addition:additions[identifier+'-added-bosses']=cad.Compound(addition.solids()).moved(poses[identifier])
print('Built candidate',len(parts),'parts',flush=True)
roundtrips=[]
with tempfile.TemporaryDirectory(prefix='truck-carrier94-') as tmp:
 for k,s in {**parts,**adapted}.items():
  assert s.is_valid and len(s.solids())==1,k
  p=Path(tmp)/(k+'.step');cad.export_step(s,p);restored=cad.import_step(p)
  assert restored.is_valid and len(restored.solids())==1,k
  assert abs(restored.volume-s.volume)<max(.01,s.volume*1e-6),k
  roundtrips.append(k)
print('STEP round trips',len(roundtrips),flush=True)
checks=0;hits=[];bounds={}
def check(a,sa,b,sb):
 global checks
 for k,s in [(a,sa),(b,sb)]:
  if k not in bounds:bounds[k]=s.bounding_box()
 ba,bb=bounds[a],bounds[b]
 if any(min(getattr(ba.max,v),getattr(bb.max,v))-max(getattr(ba.min,v),getattr(bb.min,v))<=.01 for v in 'XYZ'):return
 checks+=1;inter=sa.intersect(sb);volume=sum(x.volume for x in inter.solids()) if inter else 0
 if volume>.01:
  h={'a':a,'b':b,'volume_mm3':volume};hits.append(h);print('Overlap',h,flush=True)
for (a,sa),(b,sb) in itertools.combinations(parts.items(),2):check(a,sa,b,sb)
for a,sa in parts.items():
 for b,sb in adapted.items():check(a,sa,b,sb)
skipped=set(parts)|set(adapted)|set(c.REPLACE_IDS)
for o in m['occurrences']:
 if o['id'] in skipped:continue
 d=o['definition']
 if d not in cache:cache[d]=cad.import_step(ROOT/defs[d]['step'].lstrip('/'))
 shape=cache[d].moved(poses[o['id']])
 for a,sa in {**parts,**additions}.items():check(a,sa,o['id'],shape)
assert (ROOT/'inventory/engine/full-assembly.json').read_bytes()==raw
for p,v in frozen.items():assert (ROOT/p).read_bytes()==v,p
r={'passed':not hits,'verified_production_fit':False,'manifest_sha256':hashlib.sha256(raw).hexdigest(),'source_sha256':{p:hashlib.sha256(v).hexdigest() for p,v in frozen.items()},'part_count':len(parts),'step_round_trips':len(roundtrips),'exact_intersections':checks,'overlaps':hits,'replaces_existing_occurrences':c.REPLACE_IDS,'topology':'One shared P/S–A/C–tensioner casting; front head bolt, side head bolt, two block studs/nuts.','limits':c.GAPS}
(ROOT/'inventory/engine/accessory-carrier-1994-validation.json').write_text(json.dumps(r,indent=2)+'\n')
print('RESULT',r['passed'],'checks',checks,'overlaps',len(hits),flush=True)
