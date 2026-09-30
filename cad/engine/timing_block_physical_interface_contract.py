"""Predeclared supplemental contact/support guards; original 79 stay binding.

Support margins below are explicit review proposals, not Ford thickness specs.
No candidate-dependent mask shrinking or machining is performed here.
"""
import build123d as b

def physical_masks():
 import pushrod_cover as side
 import oil_filter_adapter as filt
 import full_engine as f
 import dipstick_tube_candidate as dip
 from timing_block_axis_feature_candidate import protected_masks
 broad,_=protected_masks();m={};spec={}
 def add(name,shape,why):m[name]=shape;spec[name]=why
 profile=b.RectangleRounded(side.LENGTH,side.HEIGHT,10)-b.RectangleRounded(side.LENGTH-18,side.HEIGHT-18,8)
 add('side-cover-sealing-land',side.MOUNT*(b.Pos(0,0,-3.5)*b.extrude(profile,amount=3.6)),{'source':'pushrod_cover gasket profile','local_z_mm':[-3.5,.1],'support':'2 mm existing material behind block seat at local−1.5; estimated minimum proposal'})
 for i,x in enumerate(side.STATIONS,1):
  add(f'side-cover-fastener-web-{i}',side.MOUNT*(b.Pos(x,0,-20.75)*b.Box(16,side.HEIGHT-16,38.5)),{'source':'entire existing fastener web and blind socket, no wall reduction'})
 # Retain exact adapter seat/port envelopes with explicitly declared 2 mm walls.
 add('filter-insert-seat-wall',filt.FRAME*filt.cylinder(16.05,-24,2),{'source':'stepped insert seat radius14.05, 2 mm radial/axial material guard'})
 add('filter-gasket-face',filt.FRAME*filt.cylinder(39,-2,.1),{'source':'entire existing boss face plus 2 mm backing'})
 add('filter-inlet-annulus-wall',filt.FRAME*(filt.cylinder(32,-6,3)-filt.cylinder(20,-7,4)),{'source':'inlet annulus radius22..30, local−4..1; 2 mm surrounding wall guard'})
 add('filter-inlet-feed-wall',filt.FRAME*(b.Pos(0,27,0)*filt.cylinder(6,-18,3)),{'source':'radius4 inlet feed, 2 mm wall guard'})
 add('filter-inlet-boundary-wall',filt.FRAME*b.Solid.make_cylinder(6,46,b.Plane(origin=(-44,27,-12),z_dir=(1,0,0))),{'source':'radius4 inlet boundary, 2 mm wall and endpoint guard'})
 add('filter-outlet-center-wall',filt.FRAME*filt.cylinder(8.4,-36,15),{'source':'radius6.4 clean outlet, 2 mm wall guard'})
 add('filter-outlet-boundary-wall',filt.FRAME*b.Solid.make_cylinder(8.4,46,b.Plane(origin=(-2,0,-29),z_dir=(1,0,0))),{'source':'radius6.4 outlet boundary, 2 mm wall/endpoint guard'})
 for x,z in f.carrier94.BLOCK_STATIONS:
  add(f'carrier-entire-support-{x}',f.carrier94.sideways(14,31,x,119.5,z),{'source':'entire existing support boss, including socket and all existing wall material'})
 add('dipstick-entire-receiver',broad['dipstick-receiver'],{'source':'unchanged original receiver guard'})
 for name,shape in broad.items():
  if name.startswith(('pan-','main-','head-','cylinder-','accessory-','water-','deck-')):add(name,shape,{'source':'unchanged original broad guard'})
 return m,spec
