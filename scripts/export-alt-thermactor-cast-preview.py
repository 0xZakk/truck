from pathlib import Path
import json,sys,numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import alt_thermactor_cast_surface_candidate as c
s=c.carrier();v,f=s.tessellate(.25,.25)
np.savez_compressed('/private/tmp/truck-alt-ap-cast.npz',vertices=np.array([tuple(x) for x in v]),faces=np.array(f))
