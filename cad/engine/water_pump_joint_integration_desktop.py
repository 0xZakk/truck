"""Idempotent builder hooks for the checked provisional pump mounting candidate."""
import build123d as b
import water_pump_joint_candidate as pump
import water_pump_inlet_v3_candidate as inlet
import water_pump_thermactor_foot_candidate as support
IDS=('block','water-pump-housing','water-pump-gasket','water-pump-shaft','water-pump-impeller','thermactor-support-bracket','thermactor-engine-bolt-2')
SOURCES=list(dict.fromkeys(pump.SOURCES))
GAPS=pump.GAPS+['The provisional Thermactor upper support foot and blind socket move together to Y-125/Z140; casting, load capacity and production coordinates remain unverified.']

def replacement(identifier, shape):
    if identifier=='block': return pump.block_interface(support.block_interface(shape))
    if identifier=='water-pump-housing': return inlet.housing_interface(pump.housing_interface(shape))
    if identifier=='water-pump-gasket': return pump.gasket_shape()
    if identifier=='water-pump-shaft': return pump.shaft_shape()
    if identifier=='water-pump-impeller':
        # Original disk rearX-12 moves59mm rearward. Absolute datum prevents
        # a repeated refresh from translating the already installed impeller again.
        return b.Pos(-71-shape.bounding_box().min.X,0,0)*shape
    if identifier=='thermactor-support-bracket': return support.support()
    if identifier=='thermactor-engine-bolt-2': return support.upper_bolt()
    return shape

def annotate(assemblies, occurrences):
    for a in assemblies:
        if a['id']=='water-pump-assembly':a['position_cad_mm']=list(pump.PUMP_POSITION)
        elif a['id']=='fan-clutch-assembly':a['position_cad_mm']=[530,-32,170]
    for o in occurrences:
        if o['id']=='heater-pump-return-elbow':o['position_cad_mm']=[0,-32,0]
