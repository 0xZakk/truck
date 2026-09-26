"""Index engine-mounted systems outside the original Engine chapter, without inventing a BOM."""
from pathlib import Path
from urllib.parse import unquote,quote
import json,hashlib
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
MANUAL=ROOT/'manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L'
base='https://charm.li/Ford/1994/F%20150%202WD%20Pickup%20L6-300%204.9L/'
parts={'Ignition Coil':'ignition-coil','Ignition Control Module':'ignition-module','Exhaust Manifold':'exhaust','Fuel Injector':'injector','Fuel Rail':'fuel-rail','Fuel Pressure Regulator':'fuel-regulator','Throttle Position Sensor':'tps','Idle Speed/Throttle Actuator - Electronic':'iac','Distributor':'distributor','Spark Plug':'spark-plug','Water Pump':'water-pump','Thermostat':'thermostat','EGR Valve':'egr','PCV Valve':'pcv','Crankshaft Damper':'damper','Flywheel':'flywheel','Oil Filter':'oil-filter'}
rows=[]
for p in sorted(MANUAL.rglob('index.html')):
 rel=p.relative_to(MANUAL); labels=[unquote(x) for x in rel.parts[:-1]]
 if len(labels)<3 or labels[-1] not in ['Description and Operation','Service and Repair','Parts Information','Specifications']:continue
 if labels[-2] not in parts:continue
 # Prefer canonical powertrain paths over duplicated maintenance/sensor links.
 if 'Maintenance' in labels or 'Tune-up and Engine Performance Checks' in labels or labels[0]=='Diagrams':continue
 raw=p.read_bytes();soup=BeautifulSoup(raw,'html.parser');content=soup.select_one('.main')
 if content is None:continue
 sid='system-'+hashlib.sha256(str(rel).encode()).hexdigest()[:12]
 images=[]
 for im in content.find_all('img'):
  ip=(p.parent/unquote(im['src'])).resolve()
  if ip.is_file() and ip.is_relative_to(ROOT):images.append({'path':str(ip.relative_to(ROOT)),'sha256':hashlib.sha256(ip.read_bytes()).hexdigest()})
 rows.append({'id':sid,'component':parts[labels[-2]],'title':' / '.join(labels[1:]),'path':str(p.relative_to(ROOT)),'url':base+'/'.join(quote(unquote(x),safe='') for x in rel.parts[:-1])+'/','sha256':hashlib.sha256(raw).hexdigest(),'text':content.get_text('\n',strip=True),'images':images,'review_status':'indexed-not-dimensionally-validated'})
(ROOT/'inventory/engine/system-references.json').write_text(json.dumps({'scope':'Selected engine-mounted systems; service categories are not individual physical parts.','sources':rows},indent=2)+'\n')
print(f'Indexed {len(rows)} pages for {len(set(r["component"] for r in rows))} component families.')
for r in rows:
 if r['component'] in ['injector','fuel-rail','fuel-regulator','iac','tps'] and r['title'].endswith('Description and Operation'):print(r['component'],r['id'],r['title'])
