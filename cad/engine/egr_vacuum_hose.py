"""Source-supported EVR-to-valve connection with provisional hose geometry."""
import build123d as b
SOURCES=['ford-evr-factory','truck-egr-evtm']
GAPS=['Routing, hose material, wall thickness and diameters are provisional; this smooth reducing envelope connects the current provisional nipples.',
 'No production hose identity, molded end geometry, hose compression or vacuum-flow simulation is established. Source-vacuum plumbing and retainers remain unfinished.']

def shape():
 start=(-420,-41,410);a=(-420,-25,410);end=(-412,85,537)
 route=b.Bezier(start,(-420,10,410),(-520,15,425),(-490,120,510),(-412,135,537),end)
 plane=b.Plane(origin=start,z_dir=(0,1,0))
 tube=b.sweep(plane*b.Circle(6),path=route,is_frenet=True)-b.sweep(plane*b.Circle(4.2),path=route,is_frenet=True)
 mount=b.Pos(*end)*b.Rot(90,0,0)
 taper=b.Cone(6,3.85,12,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))-b.Cone(4.2,2.05,12,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
 tip=b.Pos(0,0,12)*b.extrude(b.Circle(3.85)-b.Circle(2.05),amount=10)
 return tube+mount*(taper+tip)

def build(api):
 define,add,group=api
 group('egr-vacuum-lines','EGR vacuum hoses','egr')
 define('egr-control-vacuum-hose',shape(),'EGR controlled-vacuum hose','Carries the regulator output vacuum from its upper nipple to the EGR diaphragm chamber. Shape and reducing ends are provisional.','induction','#3d4140',SOURCES,GAPS)
 add('egr-control-vacuum-hose','egr-control-vacuum-hose','egr-vacuum-lines',explode=(-100,70,0))
