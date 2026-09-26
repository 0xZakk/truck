"""Orthographic shaded triangle review using bundled NumPy/Pillow."""
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[3];out=R/'cad/engine/pilot/oil-cap';a=np.load(out/'review-meshes.npz');pos=np.array([240,-12,419])
im=Image.new('RGB',(2100,790),'#f7f9fb');d=ImageDraw.Draw(im)
font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',24)
d.text((30,20),'Oil cap candidate: Ford production dimensions unverified',fill='#24303c',font=font)
for i,(elev,azim,title) in enumerate([(28,-45,'Top / grips'),(-30,-45,'Underside / screw / seal'),(18,-65,'Frozen cover datum')]):
 e,z=np.radians([elev,azim]);view=np.array([np.cos(e)*np.cos(z),np.cos(e)*np.sin(z),np.sin(e)]);right=np.array([-np.sin(z),np.cos(z),0]);up=np.cross(view,right)
 items=[]
 for key,col in [('cap',np.array([68,82,98])),('seal',np.array([154,120,64]))]+([('cover',np.array([185,193,197]))] if i==2 else []):
  xyz=a[key+'_v'].copy();faces=a[key+'_f']
  if key=='cover':
   xyz-=pos
  tri=xyz[faces];norm=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);norm/=np.maximum(np.linalg.norm(norm,axis=1)[:,None],1e-8)
  shade=.4+.6*np.abs(norm@np.array([.3,-.4,.866]));uv=np.stack([tri@right,-tri@up],axis=-1)*(5 if i==2 else 6.5)+np.array([i*700+350,430]);depth=(tri@view).mean(1)
  for pts,dep,s in zip(uv,depth,shade):items.append((dep,pts,tuple((col*s).astype(int))))
 for dep,pts,col in sorted(items,key=lambda t:t[0]):d.polygon([tuple(p) for p in pts],fill=col)
 d.text((i*700+55,90),title,fill='#24303c',font=font)
d.text((35,730),'Male screw thread and separate seal; smooth baseline hole cannot retain the cap.',fill='#74351f',font=font)
im.save(out/'review.png')
