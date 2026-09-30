"""Fixed-stock revision; earlier failed migration and proofs remain frozen."""
from pathlib import Path
import ast,math
import build123d as b
import timing_block_migration_candidate as baseline_source
ROOT=Path(__file__).resolve().parents[2]
DELTA=(0.,121.8*90/math.hypot(90,72)-90,121.8*72/math.hypot(90,72)-72)

def regenerate(delta=DELTA,stage=None,feature_capture=None):
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
                    if name and name!='stock':
                        self.counts[name]+=1;node.args[1]=ast.Constant(value=90+delta[1]);node.args[2]=ast.Constant(value=z.value+delta[2])
            return node
    edit=Edit();fn=edit.visit(fn);assert edit.counts=={'stock':0,'guides':1,'tunnel':1},edit.counts
    namespace=dict(vars(f));capture={}
    namespace['define']=lambda ident,shape,*args,**kwargs:capture.update({ident:shape})
    def shifted(feature):
        def apply(shape,*args):return b.Pos(*delta)*feature(b.Pos(*[-v for v in delta])*shape,*args)
        return apply
    for name in ['machine_block_bolts','machine_block_seat','oil_drive_block_interface']:namespace[name]=shifted(namespace[name])
    def observed(name,feature):
        def apply(shape,*args):
            before=shape;after=feature(shape,*args)
            if feature_capture:feature_capture(name,before,after)
            return after
        return apply
    for name in ['block_interface_shape','filter_block_interface']:
        namespace[name]=observed(name,namespace[name])
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),str(f.__file__),'exec'),namespace)
    namespace['define_block_casting']();q=capture['block']
    if stage:stage('01-feature-regenerated',q)
    for name,feature in [('02-pan-joint',f.pan_joint.block_interface),('03-carrier1994',f.carrier94.block_interface),('04-pump-joint',lambda s:f.pump_joint.replacement('block',s)),('05-dipstick',baseline_source.dipstick_block_only)]:
        q=observed(name,feature)(q) if name=='03-carrier1994' else feature(q)
        if stage:stage(name,q)
    return q,edit.counts

from timing_block_axis_feature_candidate import protected_masks,declared_change_roi
