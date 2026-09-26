"""Provisional front crankshaft attachment study; hardware dimensions unverified."""
import build123d as b
CENTER=454.56
FRONT=CENTER+71.12/2

def cx(r,h,x):return b.Pos(x,0,0)*b.Rot(0,90,0)*b.Cylinder(r,h)
def key():return b.Pos(465,0,21)*b.Box(40,6,4)
def key_cut():return b.Pos(465,0,21)*b.Box(40.1,6.1,4.1)
def washer():return cx(28,3.2,FRONT+1.6)-cx(8.5,5.2,FRONT+1.6)
def bolt():
 return cx(8,35,FRONT+3.2-17.5)+b.Pos(FRONT+3.2,0,0)*b.extrude(b.Plane.YZ*b.RegularPolygon(13,6),amount=8)
def crank_interface(crank):
 # Extend the inherited short snout to support the hub, keeping a small axial gap
 # beneath the retaining washer. Neither snout length nor thread is sourced.
 crank+=cx(21,56,462)
 crank-=cx(8.1,40,FRONT-16)
 return crank-key_cut()
def hub_interface(hub):return hub-b.Pos(-CENTER,0,0)*key_cut()
def build(api):
 define,add,group=api
 gaps=['Key, washer, bolt, thread bore and extended crank nose dimensions are assumed fit-study geometry, not factory dimensions. Key shape/index and production thread/grade are unverified.']
 for id,shape,name,function in [
 ('damper-key',key(),'Crankshaft damper key','Locates the damper angularly on the crankshaft. The rectangular key and its pockets illustrate the joint; actual key shape and dimensions remain unverified.'),
 ('damper-washer',washer(),'Damper retaining washer','Spreads the center-bolt clamping load onto the damper hub face. Diameter and thickness are provisional.'),
 ('damper-bolt',bolt(),'Damper retaining bolt','Clamps the damper against its crankshaft seat. The smooth shank illustrates the fastener; thread, grade and installed engagement remain unverified.')]:
  define(id,shape,name,function,'rotating','#969da1',['dorman-594-152'],gaps)
  add(id,id,'damper-assembly',(-CENTER,0,0),(200,0,30 if id=='damper-key' else 0))
