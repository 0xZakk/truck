"""Separate raw-seat interpretation and access sequence evidence; no geometry edits."""
from pathlib import Path
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common,BRepAlgoAPI_Cut
import timing_pump_rear_flange_candidate as c
old,paths,m,poses=c.load();defs={q['id']:q for q in m['definitions']};housing=b.import_step(c.O/'housing.step');cover=b.import_step(c.O/'cover.step');p=R/defs['water-pump-mounting-screw']['step'].lstrip('/');male=b.import_step(p)
def op(kind,a,z):
 q=kind(a.wrapped,z.wrapped);q.Build();assert q.IsDone();return b.Compound(q.Shape())
def faces(s):return b.Compound(list(s.faces()))
def vol(s):return sum(abs(q.volume)for q in s.solids())if s else 0.
rows=[]
for n,a in enumerate(c.pump.MOUNTING,1):
 placed=poses[f'water-pump-mounting-screw-{n}']*male;f=b.Compound([q for q in placed.faces()if abs(q.normal_at().X)>.999 and abs(q.center().X-389)<1e-5]);y,z=a[0]-32,a[1]+170
 bearing=op(BRepAlgoAPI_Cut,f,c.cx(4.3,388,390,y,z));missing=op(BRepAlgoAPI_Cut,bearing,faces(housing));oldmissing=op(BRepAlgoAPI_Cut,bearing,faces(old['housing']));tool=c.cx(10.5,389,449,y,z)
 rows.append({'station':n,'raw_headface_area_mm2':f.area,'clearance_hole_excluded_area_mm2':f.area-bearing.area,'required_bearing_face_area_mm2':bearing.area,'required_bearing_missing_mm2':missing.area,'old_required_bearing_missing_mm2':oldmissing.area,'old_tool_housing_overlap_mm3':vol(tool.intersect(old['housing'])),'new_tool_housing_overlap_mm3':vol(tool.intersect(housing))})
sweep=[]
for n in [3,4]:
 a=c.main.AXES[n-1];envelope=c.cx(8.75,357.575,455,*a);sweep.append({'station':n,'method':'ConservativeR8.75 axialboundingcylinder covers actual screw during+Xwithdrawal until headrearX449.7; exact cylinder/actualpump intersection','envelope_pump_overlap_mm3':vol(envelope.intersect(housing))})
p4=R/'cad/engine/generated/timing-cover-seven-fastener-candidate/main-cover-screw-4.step';s4=b.import_step(p4)
actualwithdrawal=[{'dx_mm':dx,'actual_screw_pump_overlap_mm3':vol((b.Pos(dx,0,0)*s4).intersect(housing))}for dx in [0,10,20,30,40]]
base=R/'manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Engine%2C%20Cooling%20and%20Exhaust/Engine';sourcepaths=[base/'Timing%20Components/Timing%20Cover/Service%20and%20Repair/index.html',base/'Water%20Pump/Service%20and%20Repair/index.html',R/'reference/engine/ford-1986-main-cover-fastener-comparison.json']
sequence={'verdict':'NOT JUSTIFIED; retain in-place tool FAIL','1994_cover':'Steps1..6 remove coolant, shroud/radiator, belt and PS/ACassembly, damper, pan/frontcover screws then cover; no pump removal prerequisite stated.','1994_pump':'Separately removes fan/pulley/hoses then pump bolts/pump; does not establish cover-before-pump assemblyorder.','1986_comparison':'PDF70, printed21-11-17 has separate pump and frontcover procedures. Frontcover removal lists belts/fan/pulleys/damper then screws/cover, no pump prerequisite. Historical comparison only.','limit':'Missing instruction is not proof universal access is possible; it supplies no justification to waive a blocked declared envelope. No exacttoolOD supplied.','physical_vs_tool':'Main3 installedmale is clear and its fullwithdrawal boundingcylinder can establish positivephysicalcorridor independently; R10.5tool remainsblocked. Main4forwardinlet is separate openfailure.'}
inputs=[Path(__file__),Path(c.__file__),p,c.O/'housing.step',c.O/'cover.step',*paths.values(),*sourcepaths,p4];r={'status':'FAIL access unresolved; nominal bearing support passes','pump_bearing_faces':rows,'screw_withdrawal':sweep,'main4_actual_withdrawal_samples':actualwithdrawal,'sequence_evidence':sequence,'inputs':{str(p.relative_to(R)):c.sha(p)for p in inputs},'explanation':'Raw7.8225657mm² headface gap is theR4shaft-toR4.3clearance annulus, present onall4oldheads. Required bearing region excludes declaredclearance opening; preserve rawfailure asdiagnostic, notstockloss.'};(R/'inventory/engine/timing-pump-rear-flange-access-evidence.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
