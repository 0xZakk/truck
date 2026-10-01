"""Coordinated estimated pan21 Y-95 revision; frozen inputs remain immutable."""
from pathlib import Path
import hashlib
import build123d as b
import timing_cover_seven_fastener_candidate as main
import timing_cover_attachment_v2 as owner
ROOT=Path(__file__).resolve().parents[2]
COVER=ROOT/'cad/engine/generated/timing-cover-seven-fastener-candidate/cover.step'
PAN=ROOT/'cad/engine/generated/timing-pan-expanded-seat-v2-candidate/pan.step'
GASKET=PAN.with_name('pan-gasket.step')
FEMALE=ROOT/'cad/engine/generated/pan-fastener-thread-candidate/female-test-coupon.step'
MALE=FEMALE.with_name('pan-screw.step');WASHER=FEMALE.with_name('existing-pan-washer.step')
OLD=(390.,-110.,-32.1);NEW=(390.,-95.,-32.1)
INPUT_HASHES={COVER:'6239fde960aa95f357a2f5482c7be232a271a4f6b7a141915014ef00f5d52017',PAN:'d7f495ec95b0cc465880c72ae38f6e873f5ee30cdbebecf4a1613a7cbe6e5b3f',GASKET:'8e968afca78cf09e81e678307b24d59a78cbe251210983a4eb5f6981619d6936'}
def norm(s):return b.Compound(children=list(s))if isinstance(s,b.ShapeList)else s
def stock(p):return b.Pos(*p)*owner.cz(10,7.6,23.6)
def build():
 for p,h in INPUT_HASHES.items():assert hashlib.sha256(p.read_bytes()).hexdigest()==h,p
 old={k:b.import_step(p)for k,p in [('cover',COVER),('pan',PAN),('pan-gasket',GASKET)]}
 a,z=OLD[2]+7.6,OLD[2]+23.6;oldguard=stock(OLD);newguard=stock(NEW)
 # Restore only declared 10mm upper dry band in the retired socket neighborhood.
 band=main.front.front_blank(0,10)[0];restore=norm(oldguard.intersect(band))
 cover=norm(old['cover'].cut(oldguard));cover=norm(cover.fuse(restore,newguard))
 female=b.Pos(*NEW)*b.import_step(FEMALE)
 bore=b.Pos(*NEW)*owner.cz(4.15,6.6,22.6)
 cavity=norm(bore.cut(female));cover=norm(cover.fuse(female));cover=norm(cover.cut(cavity))
 # Former socket21 no longer obstructs main1; protect the newly declared sockets.
 access=main.front.c.cx(main.ACCESS_RADIUS,main.SEAT,435,*main.AXES[0]);pocket=access
 guards=main.pan_socket_guards();guards[21]=newguard
 for g in guards.values():pocket=norm(pocket.cut(g))
 cover=norm(cover.cut(pocket))
 parts={'cover':cover}
 for name,lo,hi in [('pan',-30.5,-26.5),('pan-gasket',-26.5,-24.5)]:
  fill=b.Pos(OLD[0],OLD[1])*owner.cz(4.31,lo,hi)
  hole=b.Pos(NEW[0],NEW[1])*owner.cz(4.3,lo-1,hi+1)
  parts[name]=norm(old[name].fuse(fill));parts[name]=norm(parts[name].cut(hole))
 return parts,{'old':old,'oldguard':oldguard,'newguard':newguard,'access':access,'pocket':pocket,'female':female,'cavity':cavity,'male':b.Pos(*NEW)*b.import_step(MALE),'washer':b.Pos(*NEW)*b.import_step(WASHER)}
