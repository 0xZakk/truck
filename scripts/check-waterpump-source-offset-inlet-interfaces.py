from pathlib import Path
import sys,json,math
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import waterpump_source_offset_inlet_candidate as c
from cooling_connections import cylinder
oldrear=b.import_step(c.FROZEN_REAR);cover=b.import_step(c.rear.O/'cover.step');gasket=b.import_step(c.rear.O/'pump-gasket.step');inputs=[Path(__file__),Path(c.__file__),c.FROZEN_REAR,c.rear.O/'cover.step',c.rear.O/'pump-gasket.step'];rows={}
def vol(s):return sum(abs(q.volume)for q in s.solids())if s else 0.
for name,angle in [('nominal',c.NOMINAL),('low-offset',min(c.ANGLES)),('high-offset',max(c.ANGLES))]:
 p=c.O/(name+'-housing.step');inputs.append(p);s=b.import_step(p);loc=c.FRAME*b.Rot(c.ANGLE,0,0);probe=loc*c.open_probe(angle);ring=loc*(c.cy(23.9,105,139,angle)-c.cy(20.1,104,140,angle));port=loc*c.cy(19.9,100,146,angle)
 # Positive-radius probe joins an independentlyinside-chamberstart to beyondneckmouth.
 a=math.radians(c.ANGLE);entry=(420,-32+10*math.cos(a)-angle*math.sin(a),170+10*math.sin(a)+angle*math.cos(a));plug=b.Pos(*entry)*b.Sphere(3)
 rows[name]={'angle_deg':c.ANGLE,'offset_mm':angle,'fluid_probe_obstruction_mm3':vol(s.intersect(probe)),'blocked_probe_negative_control_mm3':vol(b.Compound([s,plug]).intersect(probe)),'neck_bore_obstruction_mm3':vol(s.intersect(port)),'nominal3_8mm_wall_missing_mm3':vol(ring.cut(s)),'rear_belowX389_added_mm3':vol(b.Compound(list(s.cut(oldrear).solids())).intersect(b.Pos(350,0,0)*b.Box(78,1000,1000))),'rear_belowX389_removed_mm3':vol(b.Compound(list(oldrear.cut(s).solids())).intersect(b.Pos(350,0,0)*b.Box(78,1000,1000))),'pump_gasket_contact_reuse':'Exactrearstockproof only; frozenrearcontactreport remainsbound','pump_tools':[],'main_tools':[]}
 for n,pt in enumerate(c.pump.MOUNTING,1):
  y,z=pt[0]-32,pt[1]+170;tool=c.pump.cx(10.5,389,449,y,z);rows[name]['pump_tools'].append({'station':n,'housing_overlap_mm3':vol(tool.intersect(s))})
 for n,pt in enumerate(c.rear.main.AXES,1):
  y,z=pt;tool=c.pump.cx(10.5,379.8,435,y,z);rows[name]['main_tools'].append({'station':n,'housing_overlap_mm3':vol(tool.intersect(s))})
 print(name,rows[name],flush=True)
r={'status':'Diagnosticinterface gates, preserveallaccessfailures','variants':rows,'inputs':{str(p.relative_to(R)):c.rear.sha(p)for p in inputs},'limits':['OpenR2probe andwallstock establishnominalgeometricpassage, notfullvoluteorflowcapacity.','Alltool envelopes remainR10.5; no silent reduction.','Photo-normalized offset trial; all dimensional and perspective uncertainty retained.']};(R/'inventory/engine/waterpump-source-offset-inlet-interfaces.json').write_text(json.dumps(r,indent=2)+'\n')
