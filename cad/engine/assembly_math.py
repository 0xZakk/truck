"""CAD-space transforms shared by assembly export and geometric verification."""
import math
import build123d as b


def transforms(manifest, degrees=0):
    result={}
    radius=manifest['mechanism']['stroke_mm']/2
    length=manifest['mechanism']['rod_length_mm']
    for a in manifest['assemblies']:
        loc=b.Pos(*a.get('position_cad_mm',[0,0,0]))
        motion=a.get('motion')
        if motion:
            t=math.radians(degrees+motion.get('phase_deg',0))
            jy=-radius*math.sin(t);jz=radius*math.cos(t)
            if motion['type']=='crank':loc*=b.Rot(degrees,0,0)
            if motion['type']=='cam':loc*=b.Rot(-degrees/2,0,0)
            if motion['type']=='piston':loc*=b.Pos(0,0,jz+math.sqrt(length**2-jy**2))
            if motion['type']=='rod':loc*=b.Pos(0,jy,jz)*b.Rot(math.degrees(math.asin(jy/length)),0,0)
        result[a['id']]=result.get(a['parent'],b.Location())*loc
    return {o['id']:result[o['parent']]*b.Pos(*o['position_cad_mm'])*b.Rot(*o.get('rotation_cad_deg',[0,0,0])) for o in manifest['occurrences']}
