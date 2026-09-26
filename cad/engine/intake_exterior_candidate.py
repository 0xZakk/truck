"""Source-compared exterior detail; all new dimensions and typography inferred."""
from pathlib import Path
import build123d as b
import upper_intake_clearance_candidate as core
ROOT=Path(__file__).resolve().parents[2]
FONTS={
 'caption':Path('/System/Library/Fonts/Supplemental/Arial Bold.ttf'),
 'word':Path('/System/Library/Fonts/Supplemental/Brush Script.ttf'),
}

def air_volume(paths):
    air=b.Pos(0,25,490)*core.rounded_box(392,137,82,21)
    for x,path in zip(core.PORTS,paths):
        wire=b.Wire([b.Line((x,-228,354),path@0),path])
        air+=b.sweep(b.Plane(origin=wire@0,z_dir=wire%0)*b.Circle(16.5),path=wire)
    return air

def parts(base=None,lettering=True):
    original,paths=core.candidate() if base is None else (base,core.candidate()[1])
    top=[e for e in original.edges() if abs(e.bounding_box().min.Z-535)<1e-5 and abs(e.bounding_box().max.Z-535)<1e-5]
    rounded=b.fillet(top,radius=6)
    features={}
    for index,y in enumerate((-8,64),1):
        features[f'raised-border-{index}']=b.Pos(0,y,534.6)*b.extrude(b.RectangleRounded(350,3,1.4),amount=2)
    features['oval-border']=b.Pos(-119,27,534.6)*b.extrude(b.Ellipse(51,19)-b.Ellipse(49.5,17.5),amount=1.7)
    if lettering:
        for path in FONTS.values():
            if not path.is_file():raise FileNotFoundError('Explicit font dependency unavailable: '+str(path))
        for word,y in [('ELECTRONIC',42),('FUEL INJECTION',14)]:
            features['raised-'+word.lower().replace(' ','-')]=b.Pos(57,y,534.6)*b.extrude(b.Text(word,22,font_path=str(FONTS['caption'])),amount=1.8)
        features['raised-ford-word']=b.Pos(-119,27,534.6)*b.extrude(b.Text('Ford',37,font_path=str(FONTS['word'])),amount=1.8)
    # Broad, smoothly changing root shoulders, not separate annular rings.
    # Their radii/locations are estimates of visible cast transitions.
    for index,path in enumerate(paths,1):
        sections=[b.Plane(origin=path@t,z_dir=path%t)*b.Circle(radius) for t,radius in [(.64,22),(.82,25),(1.,24)]]
        features[f'runner-root-shoulder-{index}']=b.loft(sections)
    air=air_volume(paths)
    result=rounded
    for name,feature in features.items():
        if name.startswith('runner-root'):feature=feature-air
        result+=feature
    return result,original,paths,features,air
