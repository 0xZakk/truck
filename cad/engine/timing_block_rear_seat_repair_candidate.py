"""Explicit distributive CSG repair; frozen invalid fixed-stock trial retained."""
from pathlib import Path
import ast
import build123d as b
import timing_block_fixed_stock_candidate as fixed
DELTA=fixed.DELTA

def operands(cam_bore_radius):
 import expansion_plugs as source
 tree=ast.parse(Path(source.__file__).read_text());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='machine_block_seat')
 assert isinstance(fn.body[-1],ast.Return)
 fn.body[-1]=ast.Return(value=ast.Tuple(elts=[ast.Name(id=x,ctx=ast.Load()) for x in ['boss','tunnel','seat']],ctx=ast.Load()))
 ns=dict(vars(source));exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),str(source.__file__),'exec'),ns)
 return ns['machine_block_seat'](None,cam_bore_radius)

def machine_block_seat(block,cam_bore_radius):
 boss,tunnel,seat=operands(cam_bore_radius)
 # Distribute the exact same two source cutters over the two source summands.
 # This avoids cutting a merged long tunnel face with nested coincident wires.
 stock=block.cut(tunnel).cut(seat)
 support=boss.cut(tunnel).cut(seat)
 return stock.fuse(support)

def regenerate(delta=DELTA,stage=None,feature_capture=None):
 import full_engine as f
 original=f.machine_block_seat;f.machine_block_seat=machine_block_seat
 try:return fixed.regenerate(delta,stage,feature_capture)
 finally:f.machine_block_seat=original
