"""Piecewise-linear educational explode offsets shared with viewer helper.

Stages describe display separation, never a validated removal procedure.
"""
def explode_offset(occurrence, amount):
    amount=max(0.,min(1.,float(amount)))
    stages=occurrence.get('explode_stages')
    if not stages:return tuple(amount*x for x in occurrence.get('explode_cad_mm',(0,0,0)))
    assert len(stages)>=2 and stages[0]['at']==0 and stages[-1]['at']==1
    assert all(a['at']<c['at'] for a,c in zip(stages,stages[1:]))
    assert all(len(s['offset_cad_mm'])==3 for s in stages)
    for a,c in zip(stages,stages[1:]):
        if amount<=c['at']:
            t=(amount-a['at'])/(c['at']-a['at'])
            return tuple(x+(y-x)*t for x,y in zip(a['offset_cad_mm'],c['offset_cad_mm']))
    return tuple(stages[-1]['offset_cad_mm'])

def pan_hardware_stages(final_offset):
    dx,dy,dz=final_offset
    return [{'at':0,'offset_cad_mm':[0,0,0]},
            {'at':.35,'offset_cad_mm':[0,0,-137]},
            {'at':.6,'offset_cad_mm':[dx,dy,-217]},
            {'at':1,'offset_cad_mm':[dx,dy,dz]}]
