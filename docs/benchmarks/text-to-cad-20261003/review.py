"""Independent saved-artifact acceptance; run with the repository CAD interpreter."""
from pathlib import Path
import argparse, hashlib, json, math
import build123d as b
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[3]
R, H = 52.578 / 2, 8.7122

def expected(rad, z):
    if z < 0 or z > H:
        return False
    outer = R if z >= 1.5 else R - 1.5 + math.sqrt(max(0, 1.5**2-(z-1.5)**2))
    if rad > outer:
        return False
    if z < 1:
        return True
    inner = R-1 if z >= 1.5 else R-1.5 + math.sqrt(max(0, .5**2-(z-1.5)**2))
    return rad >= inner

def main():
    ap=argparse.ArgumentParser();ap.add_argument('step',type=Path);ap.add_argument('glb',type=Path);ap.add_argument('report',type=Path);a=ap.parse_args()
    s=b.import_step(a.step);bb=s.bounding_box()
    checks={'valid_one_solid':s.is_valid and len(s.solids())==1 and s.volume>0}
    bounds=np.array([tuple(bb.min),tuple(bb.max)])
    checks['step_envelope']=bool(np.max(np.abs(bounds-np.array([[-R,-R,0],[R,R,H]])))<.025)
    # Includes floor, void, straight wall, outer and inner corner bands, at 8 azimuths.
    probes=[]
    for z in [-.1,.2,.7,.95,1.1,1.3,1.6,4.2,8.5,8.9]:
        for rad in [0,10,R-2,R-1.4,R-1.1,R-.8,R-.3,R+.1]:
            for t in np.arange(8)*math.pi/4:
                p=(rad*math.cos(t),rad*math.sin(t),z)
                probes.append((p,expected(rad,z)))
    bad=[{'point':p,'expected':e} for p,e in probes if bool(s.is_inside(p))!=e]
    checks['analytic_section_probes']=not bad
    floor_missing=s-b.Pos(0,0,-1)*b.Cylinder(8,3,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
    closed=s+b.Pos(0,0,H-1)*b.Cylinder(R-.5,1,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
    checks['floor_control']=not floor_missing.is_inside((0,0,.5)) and s.is_inside((0,0,.5))
    checks['opening_control']=closed.is_inside((0,0,H-.5)) and not s.is_inside((0,0,H-.5))
    m=trimesh.load(a.glb,force='mesh');m.merge_vertices(digits_vertex=8)
    checks['mesh_topology']=bool(m.is_watertight and m.is_winding_consistent and m.volume>0 and len(m.split())==1)
    vv=m.vertices[:,[0,2,1]]*[1,-1,1]*1000
    error=float(np.max(abs(np.array([vv.min(0),vv.max(0)])-bounds)))
    checks['mesh_bounds']=error<.025
    volume_error=abs(m.volume*1e9-s.volume)/s.volume
    checks['mesh_volume']=bool(volume_error<.005)
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    report={'scope':'isolated assumed-section replacement candidate only','checks':checks,'pass':all(checks.values()),'probe_count':len(probes),'failed_probes':bad,'mesh_bounds_error_mm':error,'step_volume_mm3':s.volume,'relative_mesh_volume_error':volume_error,'hashes':{str(p.relative_to(ROOT)):sha(p) for p in [a.step.resolve(),a.glb.resolve(),Path(__file__).resolve()]},'installed_interfaces':'NOT RUN','browser_engine_integration':'NOT RUN','factory_section_fidelity':'UNKNOWN'}
    a.report.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));assert report['pass']

if __name__=='__main__':main()
