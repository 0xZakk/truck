"""Estimated add-only outlet exterior; installed interfaces and gas space retained."""
import build123d as b
import exhaust_rear_collector_candidate as collector
import exhaust_front_profile as front
import exhaust_rear_entries as rear

# Estimated Z / X radius / Y radius. No source pixel scaling or dimensional claim.
SECTIONS = [(150.2, 27., 27.), (158., 28., 27.5), (174., 33., 28.5),
            (190., 43., 29.), (207., 56., 29.), (220., 62., 25.),
            (240., 45., 15.)]

def envelope():
    return b.loft([b.Plane(origin=(rear.PORTS[1], -180, z))*b.Ellipse(rx, ry)
                   for z, rx, ry in SECTIONS], ruled=False)

def protected_regions():
    regions = collector.protected_regions()
    # Neck study intentionally changes exterior above flange; the exact flange,
    # seat and outlet endpoint remain protected through Z=150.2. Gas space is
    # independently protected over the entire outlet/collector, not this mask.
    regions['outlet_and_flange'] = b.Pos(-145,-180,100.1)*b.Box(500,200,100.2)
    return regions

def build(baseline):
    addition = envelope() - collector.collector(collector.WALL)
    addition -= b.Pos(rear.PORTS[1], -180, 175)*b.Cylinder(20,86)
    for x in rear.PORTS:
        addition -= front.runner_void(x)
    for region in protected_regions().values():
        addition = collector.compound(addition-region)
    return baseline.fuse(addition)
