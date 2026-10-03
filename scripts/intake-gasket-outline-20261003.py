"""Extract an authored outline; never redistribute the reference image."""
from pathlib import Path
import argparse, hashlib, json
import numpy as np
from PIL import Image
from scipy.ndimage import label, binary_fill_holes
from scipy.spatial import cKDTree
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path as PlotPath

ROOT = Path(__file__).resolve().parents[1]
PREFIX = 'intake-gasket-outline-20261003'

def simplify(points, tolerance):
    if len(points) <= 2:
        return points
    a, b = points[0], points[-1]
    v = b-a
    t = np.clip((points-a)@v/max(v@v, 1e-30), 0, 1)
    distance = np.linalg.norm(points-(a+t[:, None]*v), axis=1)
    i = int(distance.argmax())
    if distance[i] <= tolerance:
        return points[[0, -1]]
    return np.vstack((simplify(points[:i+1], tolerance)[:-1], simplify(points[i:], tolerance)))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--image',type=Path,required=True);args=ap.parse_args()
    blob=args.image.read_bytes()
    assert hashlib.sha256(blob).hexdigest()=='de5ea8c38f38609b3e1185de40826e2c6b408ed35bba548c13881cd28963c3f3'
    gray=np.asarray(Image.open(args.image).convert('L'))
    measure=json.loads((ROOT/'reference/engine/intake-joint-online-20261003-measurement.json').read_text())
    run=next(r for r in measure['runs'] if r['threshold']==210)
    ports=np.array(run['port_centers_left_to_right_px']);origin=ports[-1]
    u=(ports[0]-origin);span=np.linalg.norm(u);u=u/span;v=np.array([-u[1],u[0]])
    contours={}
    for threshold in [180,210,235]:
        labels,_=label(gray<threshold);sizes=np.bincount(labels.ravel());sizes[0]=0
        filled=binary_fill_holes(labels==sizes.argmax())
        fig,ax=plt.subplots();c=ax.contour(filled.astype(float),levels=[.5]);contours[threshold]=max(c.allsegs[0],key=len);plt.close(fig)
    nominal=contours[210];mid=len(nominal)//2
    polygon=np.vstack((simplify(nominal[:mid+1],.75)[:-1],simplify(nominal[mid:],.75)))
    # Verify directed source-boundary to polygon-segment distance without sampling shortcuts.
    a=polygon[:-1];delta=np.diff(polygon,axis=0)
    offsets=nominal[:,None,:]-a[None,:,:]
    t=np.clip(np.einsum('nki,ki->nk',offsets,delta)/np.sum(delta*delta,axis=1),0,1)
    errors=np.linalg.norm(offsets-t[:,:,None]*delta,axis=2).min(axis=1)
    uv=np.column_stack(((polygon-origin)@u,(polygon-origin)@v))/span
    xy=np.column_stack((284.48-568.96*uv[:,0],-228-568.96*uv[:,1]))
    params=json.loads((ROOT/'cad/engine/intake-joint-candidate-20261003-parameters.json').read_text())
    tests=[];angles=np.linspace(0,2*np.pi,1440,endpoint=False);path=PlotPath(xy)
    circles=[]
    for i,station in enumerate(params['port_stations']):circles.append((f'P{i+1}',np.array([284.48-568.96*station,-228]),25.5))
    for h in params['holes']:circles.append((h['feature_id'],np.array([284.48-568.96*h['normalized_uv'][0],-228-568.96*h['normalized_uv'][1]]),5.5))
    for name,center,radius in circles:
        samples=center+radius*np.column_stack((np.cos(angles),np.sin(angles)))
        tests.append({'id':name,'samples':len(samples),'outside':int((~path.contains_points(samples)).sum())})
    bad=circles[0][1]+[0,100]+25.5*np.column_stack((np.cos(angles),np.sin(angles)))
    assert not path.contains_points(bad).all()
    out={'scope':'source-derived outline at estimated existing scale; no installed acceptance','source_sha256':hashlib.sha256(blob).hexdigest(),'pixel_frame':{'origin':origin.tolist(),'u':u.tolist(),'v':v.tolist(),'span':float(span)},'simplification':{'tolerance_px':.75,'actual_max_px':float(errors.max()),'vertices':len(polygon)},'threshold_sensitivity_max_nearest_vertex_px':{str(t):float(cKDTree(nominal).query(c)[0].max()) for t,c in contours.items()},'nominal_polygon_px':polygon.tolist(),'world_xy_mm':xy.tolist(),'fixed_aperture_checks':tests,'shifted_control_rejected':True,'limits':['threshold sensitivity is not factory tolerance','568.96mm span/1.5mm thickness inherited estimates','single photo perspective remains uncalibrated','aperture circles are prior estimates; mismatch is not silently fixed']}
    assert errors.max()<=.75+1e-9
    dest=ROOT/'reference/engine';(dest/(PREFIX+'-contour.json')).write_text(json.dumps(out,indent=2)+'\n')
    fig,ax=plt.subplots(figsize=(15,4));ax.fill(xy[:,0],xy[:,1],color='#a1b2be',alpha=.6,label='Full traced silhouette')
    for name,center,radius in circles:
        ax.add_patch(plt.Circle(center,radius,facecolor='white',edgecolor='#a53723'));ax.text(*center,name,ha='center',va='center',fontsize=7)
    ax.set_aspect('equal');ax.set_xlabel('Engine X mm — inherited estimated scale');ax.set_ylabel('Engine Y mm');ax.set_title('Source-derived gasket outline; fixed candidate apertures checked separately');ax.grid(alpha=.2);fig.tight_layout();fig.savefig(dest/(PREFIX+'-review.png'),dpi=150);plt.close(fig)
    print(json.dumps({k:out[k] for k in ['simplification','threshold_sensitivity_max_nearest_vertex_px','fixed_aperture_checks','shifted_control_rejected']},indent=2))

if __name__=='__main__':main()
