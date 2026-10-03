from pathlib import Path
import re,requests,json,hashlib
R=Path(__file__).resolve().parents[1];O=R/'reference/engine/pump-junction-online-20261002-captures';O.mkdir(exist_ok=True)
s=(R/'reference/engine/pump-metric-20261002-captures/carter.html').read_text().replace('\\/','/')
urls=sorted(set(re.findall(r'https://[^\s"<>]+(?:jpg|png|jpeg)',s)))
urls=[u for u in urls if 'fa68fca6ec37c26ea1b32d9f7f3ab3be/W/9/W9046M_'in u or '/360/W9046M/W9046M_1.jpg'in u]
r=[]
for u in urls:
 p=O/u.rsplit('/',1)[1];res=requests.get(u,timeout=40);res.raise_for_status();p.write_bytes(res.content);r.append({'url':u,'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':len(res.content)});print(p.name,len(res.content),flush=True)
(R/'reference/engine/pump-junction-online-20261002-captures.json').write_text(json.dumps({'manufacturer_page':'https://carterengineered.com/engine-water-pump-w9046m','images':r,'source_originals_local_only':True},indent=2)+'\n')
