#!/usr/bin/env python3
"""Measure dimensionless gasket-photo landmarks; never use package dimensions."""
import argparse,json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image
from scipy.ndimage import label,binary_fill_holes,center_of_mass
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];PREFIX='intake-joint-online-20261003'

def extract(gray,threshold):
 labels,n=label(gray<threshold);sizes=np.bincount(labels.ravel());sizes[0]=0;mask=labels==sizes.argmax();holes=binary_fill_holes(mask)&~mask;hl,n=label(holes);features=[]
 for k in range(1,n+1):
  reg=hl==k;area=int(reg.sum())
  if area<100:continue
  y,x=center_of_mass(reg);yy,xx=np.where(reg);cov=np.cov(np.vstack([xx,yy]));eig=np.linalg.eigvalsh(cov)
  features.append({'center_px':[x,y],'area_px':area,'moment_axis_ratio':float(np.sqrt(eig[0]/eig[1])),'class':'port' if area>3000 else 'small_hole'})
 ports=sorted([p for p in features if p['class']=='port'],key=lambda p:p['center_px'][0]);small=[p for p in features if p['class']=='small_hole']
 valid=len(ports)==6 and len(small)==9;result={'threshold':threshold,'port_count':len(ports),'small_hole_count':len(small),'topology_valid':valid,'features':features}
 if valid:
  p=np.array([i['center_px'] for i in ports]);mean=p.mean(axis=0);_,_,v=np.linalg.svd(p-mean);direction=v[0]
  if direction[0]<0:direction=-direction
  station=(p-mean)@direction;gaps=np.diff(station)
  result.update(port_centers_left_to_right_px=p.tolist(),row_direction_px=direction.tolist(),gaps_left_to_right_px=gaps.tolist(),right_end_gap_over_other_mean=float(gaps[-1]/gaps[:-1].mean()),port_axis_ratios=[i['moment_axis_ratio'] for i in ports],normalized_stations_front_to_rear=((station[-1]-station[::-1])/(station[-1]-station[0])).tolist())
 return result

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--image',type=Path,required=True);a=ap.parse_args();blob=a.image.read_bytes();ledger=json.loads((ROOT/'reference/engine'/f'{PREFIX}-evidence.json').read_text());expected=next(x['sha256'] for x in ledger['sources'] if x['url'].endswith('ms-93838.jpg'));assert hashlib.sha256(blob).hexdigest()==expected, 'Source image changed; review and rebind explicitly';gray=np.asarray(Image.open(a.image).convert('L'));runs=[extract(gray,t) for t in [150,180,210,235]]
 assert not runs[0]['topology_valid'],'Low-threshold bad extraction control unexpectedly passed'
 assert all(r['topology_valid'] for r in runs[1:]),'Expected6+9 aperture topology failed'
 report={'schema':1,'image_url':'https://images.carid.com/fel-pro/items/ms-93838.jpg','image_sha256':hashlib.sha256(blob).hexdigest(),'image_size_px':list(Image.open(a.image).size),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'runs':runs,'units':'pixels and dimensionless ratios only','front_assignment':'inferred right photo end from short interval, paired small holes and opposite terminal ears matched to casting photos; not printed FRONT','limits':['identified replacement product photo, not dimensional drawing','no physical scale or gasket thickness','nine small holes do not prove nine retaining bolts','segmentation range is not manufacturing tolerance']}
 out=ROOT/'reference/engine';(out/(PREFIX+'-measurement.json')).write_text(json.dumps(report,indent=2)+'\n')
 run=runs[2];ports=np.array(run['port_centers_left_to_right_px']);origin=ports[-1];span=origin[0]-ports[0,0]
 fig,ax=plt.subplots(figsize=(12,3));
 for i,p in enumerate(ports[::-1]):
  x=(origin[0]-p[0])/span;y=(p[1]-origin[1])/span;ax.scatter(x,y,s=130,facecolor='white',edgecolor='#235f7b');ax.text(x,y+.025,str(i+1),ha='center')
 for f in run['features']:
  if f['class']=='small_hole':
   p=np.array(f['center_px']);ax.scatter((origin[0]-p[0])/span,(p[1]-origin[1])/span,s=24,color='#b25822')
 ax.set_aspect('equal');ax.set_xlim(-.10,1.15);ax.set_ylim(-.11,.13);ax.set_xlabel('Normalized first-to-last port span (dimensionless)');ax.set_title('MS93838 observed centers: six ports, nine small apertures\nFront-end mapping inferred; no millimeter scale or hardware function assigned');ax.grid(alpha=.15);fig.tight_layout();fig.savefig(out/(PREFIX+'-landmarks.png'),dpi=160)
 for r in runs:print(r['threshold'],r['port_count'],r['small_hole_count'],r.get('right_end_gap_over_other_mean'))
if __name__=='__main__':main()
