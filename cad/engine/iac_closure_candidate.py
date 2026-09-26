"""Illustrative formed-lip IAC closure, not identified Ford construction.

IAC-local mm. A recessed flanged metal plug has continuous geometric contact;
separate elastomer, press interference and leak-rate claims are intentionally
absent. Assembled lip shape does not simulate forming or disassembly.
"""
import build123d as b
PARAMS=dict(body_front_x=-24.,lip_back_x=-23.7,shoulder_x=-23.3,spring_seat_x=-23.,
            bore_radius=8.5,flange_radius=9.2,old_plug_radius=8.4)
def cx(radius,left,right):return b.Pos((left+right)/2,0,0)*b.Rot(0,90,0)*b.Cylinder(radius,right-left)
def build(body,radial_gap=0.):
    """Return revised body and placed plug in the IAC frame.

    radial_gap is a checker fault parameter, not a selectable production fit.
    The assembled lip captures the flange in both axial directions. Real lip
    formation, material strain, spring preload and hermetic performance unknown.
    """
    p=PARAMS
    body=body-cx(p['flange_radius'],p['lip_back_x'],p['shoulder_x'])
    plug=cx(p['flange_radius']-radial_gap,p['lip_back_x'],p['shoulder_x'])+cx(p['bore_radius']-radial_gap,p['shoulder_x'],p['spring_seat_x'])
    return {'iac-valve-body':body,'iac-end-plug':plug}
