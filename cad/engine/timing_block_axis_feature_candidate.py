"""New isolated feature revision; baseline discovery module remains frozen."""
from pathlib import Path
import ast,math
import build123d as b
import timing_block_migration_candidate as baseline_source
ROOT=Path(__file__).resolve().parents[2]
DELTA=(0.,121.8*90/math.hypot(90,72)-90,121.8*72/math.hypot(90,72)-72)

def regenerate(delta=DELTA,stage=None):
    import full_engine as f
    tree=ast.parse(Path(f.__file__).read_text());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='define_block_casting')
    class Edit(ast.NodeTransformer):
        counts={'stock':0,'guides':0,'tunnel':0}
        def visit_Call(self,node):
            self.generic_visit(node)
            if isinstance(node.func,ast.Attribute) and isinstance(node.func.value,ast.Name) and node.func.value.id=='b' and node.func.attr=='Pos' and len(node.args)==3:
                x,y,z=node.args
                if isinstance(y,ast.Constant) and y.value==90 and isinstance(z,ast.Constant):
                    name='stock' if isinstance(x,ast.Constant) and x.value==0 and z.value==84 else 'tunnel' if isinstance(x,ast.Constant) and x.value==0 and z.value==72 else 'guides' if isinstance(x,ast.BinOp) and ast.unparse(x)=='x + dx' and z.value==150 else None
                    if name:
                        self.counts[name]+=1;node.args[1]=ast.Constant(value=90+delta[1]);node.args[2]=ast.Constant(value=z.value+delta[2])
            return node
    edit=Edit();fn=edit.visit(fn);assert edit.counts=={'stock':1,'guides':1,'tunnel':1},edit.counts
    namespace=dict(vars(f));capture={}
    namespace['define']=lambda ident,shape,*args,**kwargs:capture.update({ident:shape})
    def shifted(feature):
        def apply(shape,*args):return b.Pos(*delta)*feature(b.Pos(*[-v for v in delta])*shape,*args)
        return apply
    for name in ['machine_block_bolts','machine_block_seat','oil_drive_block_interface']:namespace[name]=shifted(namespace[name])
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),str(f.__file__),'exec'),namespace)
    namespace['define_block_casting']();q=capture['block']
    if stage:stage('01-feature-regenerated',q)
    for name,feature in [('02-pan-joint',f.pan_joint.block_interface),('03-carrier1994',f.carrier94.block_interface),('04-pump-joint',lambda s:f.pump_joint.replacement('block',s)),('05-dipstick',baseline_source.dipstick_block_only)]:
        q=feature(q)
        if stage:stage(name,q)
    return q,edit.counts

def protected_masks():
    """Fixed named guards declared before inspecting migrated differences."""
    import full_engine as f
    import oil_filter_adapter as filt
    import dipstick_tube_candidate as dip
    masks={};specs={}
    def add(name,q,description):masks[name]=q;specs[name]=description
    for i,x in enumerate(f.MAINS,1):
        add(f'main-journal-{i}',b.Pos(x,0,0)*f.cx(f.MAIN_R+7,35),{'x':x,'axis':'X','radius_mm':f.MAIN_R+7,'width_mm':35})
        for y in [-56,56]:add(f'main-cap-socket-{i}-{y}',b.Pos(x,y,27)*b.Cylinder(8.5,62),{'center':[x,y,27],'radius_mm':8.5,'height_mm':62})
        for y in [-67,67]:add(f'head-bolt-{i}-{y}',b.Pos(x,y,237)*b.Cylinder(10,38),{'center':[x,y,237],'radius_mm':10,'height_mm':38})
    for i,x in enumerate(f.CYLINDERS,1):add(f'cylinder-wall-{i}',b.Pos(x,0,169)*b.Cylinder(f.P['bore']/2+7,170),{'center':[x,0,169],'radius_mm':f.P['bore']/2+7,'height_mm':170})
    deck=b.Pos(0,-12,253)*b.Box(f.LENGTH,242,2)
    for x in f.CYLINDERS:
        for dx in [-25,25]:
            for dy in [0,DELTA[1]]:deck-=b.Pos(x+dx,90+dy,253)*b.Cylinder(f.LIFTER_BORE_R+2,4)
    add('deck-outside-declared-guide-openings',deck,{'z_range':[252,254],'excluded':'old/new twelve guide cylinders, bore radius+2mm'})
    add('side-cover-rail-and-fastener-region',b.Pos(0,112.5,185)*b.Box(674,19,112),{'bounds':[[-337,103,129],[337,122,241]]})
    for y,z in [(90,220),(-100,220),(-100,90),(-125,140)]:add(f'accessory-front-{y}-{z}',b.Pos(361,y,z)*f.cx(13,26),{'center':[361,y,z],'axis':'X','radius_mm':13,'width_mm':26})
    for x,z in f.carrier94.BLOCK_STATIONS:add(f'carrier-side-{x}',f.carrier94.sideways(15,33,x,119.5,z),{'center':[x,119.5,z],'axis':'Y','radius_mm':15,'length_mm':33})
    add('filter-boss-and-gallery-interface',filt.boss_addition(),{'source':'oil_filter_adapter.boss_addition, entire existing boss envelope'})
    add('dipstick-receiver',dip.axial_cylinder(11,-51,9.5),{'source':'dipstick receiver frame, radius11, local axial−51..9.5'})
    for i,(x,y,z) in enumerate(f.pan_joint.STATIONS,1):add(f'pan-socket-{i}',b.Pos(x,y,z+17)*b.Cylinder(12,26),{'center':[x,y,z+17],'radius_mm':12,'height_mm':26})
    add('pan-front-end-land',b.Pos(373,0,-51)*b.Box(18,132,32),{'bounds':[[364,-66,-67],[382,66,-35]]})
    add('pan-rear-end-land',b.Pos(-373,0,-51)*b.Box(18,114,32),{'bounds':[[-382,-57,-67],[-364,57,-35]]})
    add('water-pump-front-interface',b.Pos(365,-32,170)*f.cx(85,20),{'center':[365,-32,170],'axis':'X','radius_mm':85,'width_mm':20})
    return masks,specs

def declared_change_roi():
    import full_engine as f
    masks=[]
    for dy,dz in [(0,0),(DELTA[1],DELTA[2])]:
        masks += [b.Pos(0,90+dy,84+dz)*b.Box(f.LENGTH+.002,55.002,110.002),b.Pos(0,90+dy,72+dz)*f.cx(f.CAM_BORE_R+.001,f.LENGTH+2.002)]
        for x in f.CYLINDERS:
            for dx in [-25,25]:masks.append(b.Pos(x+dx,90+dy,150+dz)*b.Cylinder(f.LIFTER_BORE_R+.001,235.002))
    # Declared feature envelopes cover both old/new feature operands; they do
    # not exempt unrelated critical guards from exact comparison.
    masks += [b.Pos(-367,95,76)*b.Box(32,85,85),b.Pos(367,95,76)*b.Box(16,22,90),b.Pos(227.5,120,5)*b.Box(125,180,320)]
    return b.Compound(children=masks)
