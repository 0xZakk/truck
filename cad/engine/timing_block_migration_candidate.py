"""Isolated block reconstruction discovery; migration not implemented yet."""
from pathlib import Path
import ast
import build123d as b
ROOT=Path(__file__).resolve().parents[2]

def dipstick_block_only(block):
    """Execute only the original candidate's block-feature prefix, unaltered."""
    import dipstick_tube_candidate as tube
    tree=ast.parse(Path(tube.__file__).read_text())
    source=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='candidate')
    body=[]
    for node in source.body:
        body.append(node)
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='modified_block' for t in node.targets):break
    else:raise AssertionError('Dipstick block prefix changed; review extraction')
    body.append(ast.Return(value=ast.Name(id='modified_block',ctx=ast.Load())))
    fn=ast.FunctionDef(name='_block_feature',args=source.args,body=body,decorator_list=[])
    module=ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[]));ns=dict(vars(tube));exec(compile(module,str(tube.__file__),'exec'),ns)
    return ns['_block_feature'](block,None)

def baseline(stage=None):
    """Call current define_block_casting without exporter, then exact block hooks.

    Source imports retain read-only repo inputs. Shared builder outputs redirected
    defensively; main()/define()/install() exporters never execute.
    """
    import full_engine as f
    out=ROOT/'cad/engine/generated/timing-block-migration-candidate';out.mkdir(exist_ok=True)
    f.OUT=out/'meshes';f.STEP=out/'steps'
    captured={};saved=f.define
    def capture(identifier,shape,*args,**kwargs):
        assert identifier=='block';captured[identifier]=shape
    f.define=capture
    try:f.define_block_casting()
    finally:f.define=saved
    q=captured['block']
    if stage:stage('01-base-casting-with-direct-interfaces',q)
    # Ordered block-relevant define() hooks; identity adapters omitted.
    for name,fn in [('02-pan-joint',f.pan_joint.block_interface),('03-carrier1994',f.carrier94.block_interface),('04-pump-joint',lambda s:f.pump_joint.replacement('block',s))]:
        q=fn(q)
        if stage:stage(name,q)
    for mod in (f.manifold_lifting_eye,f.intake_locating_dowel,f.exhaust_front_profile,f.exhaust_rear_entries,f.rear_mounts,f.exhaust_outlets):
        assert 'block' not in mod.ADAPTERS, 'New ordered block adapter needs review'
    assert 'block' not in f.source_definitions.IDS
    q=dipstick_block_only(q)
    if stage:stage('05-dipstick-final',q)
    return q
