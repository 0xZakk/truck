"""Index current truck references without inheriting legacy 'modeled' claims."""
from pathlib import Path
from urllib.parse import unquote,quote
import hashlib,json
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
MANUAL=ROOT/'manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L'
URL='https://charm.li/Ford/1994/F%20150%202WD%20Pickup%20L6-300%204.9L/'
SYSTEMS=[
('engine','Engine','Engine, Cooling and Exhaust','Engine','engine.html','Long block, induction, fuel injection and engine-mounted components.'),
('cooling','Cooling','Engine, Cooling and Exhaust','Cooling System',None,'Pump, thermostat, radiator, heater circuit, fan and hoses.'),
('exhaust','Exhaust','Engine, Cooling and Exhaust','Exhaust System',None,'Manifolds, pipe joints, catalyst, muffler and hangers.'),
('transmission','Transmission & driveline','Transmission and Drivetrain',None,None,'M5OD-R2, clutch, driveshaft, differential, axle shafts and bearings.'),
('starting','Starting & charging','Starting and Charging',None,None,'Starter, alternator, battery and their electrical connections.'),
('controls','Ignition & engine controls','Powertrain Management',None,None,'Distributor, EEC-IV, sensors, fuel delivery, vacuum and emissions controls.'),
('brakes','Brakes','Brakes and Traction Control',None,None,'Pedal, booster, master cylinder, hydraulic circuits and wheel brakes.'),
('steering','Steering','Steering and Suspension','Steering',None,'Steering column, gear, pump, lines and linkage.'),
('suspension','Suspension','Steering and Suspension','Suspension',None,'2WD front suspension, rear springs, shocks and mounting hardware.'),
('body','Body & frame','Body and Frame',None,None,'SuperCab body, frame, bed, doors, mounts and structural interfaces.'),
('hvac','Heating & air conditioning','Heating and Air Conditioning',None,None,'Heater, blower, ducts and air-conditioning equipment where fitted.'),
('electrical','Wiring & power distribution','Power and Ground Distribution',None,None,'Harnesses, grounds, fuses, splices and connectors.'),
('lighting','Lighting','Lighting and Horns',None,None,'Exterior lamps, switches, horn and circuits.'),
('interior','Instruments & interior controls','Instrument Panel, Gauges and Warning Indicators',None,None,'Cluster, gauges, warning lamps and driver controls.'),
('restraints','Restraints','Restraints and Safety Systems',None,None,'Seat belts and applicable restraint components.')]
rows=[]
for sid,name,category,branch,viewer,scope in SYSTEMS:
 sources=[]
 for p in sorted(MANUAL.rglob('index.html')):
  rel=p.relative_to(MANUAL); labels=[unquote(v) for v in rel.parts[:-1]]
  if len(labels)<3 or labels[0]!='Repair and Diagnosis' or labels[1]!=category:continue
  if branch and (len(labels)<3 or labels[2]!=branch):continue
  if not any(x in labels for x in ['Description and Operation','Service and Repair','Specifications','Testing and Inspection','Diagrams','Locations']):continue
  if sid=='transmission' and any(token in ' / '.join(labels) for token in ['Automatic Transmission','A/T','Transfer Case','Four Wheel Drive','4WD','ZF']):continue
  raw=p.read_bytes(); soup=BeautifulSoup(raw,'html.parser'); main=soup.select_one('.main')
  if not main:continue
  text=main.get_text(' ',strip=True)
  # Navigation-only pages can be useful but do not count as reviewed evidence.
  sources.append({'title':' / '.join(labels[2:]),'path':str(p.relative_to(ROOT)),'url':URL+'/'.join(quote(unquote(v),safe='') for v in rel.parts[:-1])+'/','sha256':hashlib.sha256(raw).hexdigest(),'images':len(main.select('img')),'review_status':'indexed, applicability and detail not yet reviewed'})
 rows.append({'id':sid,'name':name,'scope':scope,'viewer':viewer,'status':'provisional component model' if viewer else 'reference collection; modeling pending','sources':sources})
out=ROOT/'inventory/truck';out.mkdir(exist_ok=True)
(out/'systems.json').write_text(json.dumps({'vehicle':'1994 F-150 XLT SuperCab · 2WD · 4.9L · M5OD-R2','policy':'Reference counts are not part counts or completion percentages. Manual sections may contain options not installed on this truck. Legacy prototype modeled flags are not carried forward.','systems':rows},indent=2)+'\n')
for r in rows:print(r['id'],len(r['sources']))
