#!/usr/bin/env python3
"""Actual fullcam/distributor checks at interstitial event and endplay endpoints."""
from pathlib import Path
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import crossed_oil_drive_endplay_candidate as poses
from cad_metrics import solid_volume
cp=R/'cad/engine/generated/cam-composed-drive-candidate/camshaft-local.step';dp=R/'cad/engine/generated/crossed-oil-drive-corrected-pair/distributor-drive-gear-local.step';cam=b.import_step(cp);dist=b.import_step(dp);rows=[]
for axial in [0.,-.1]:
 f=poses.frames(11.25,axial);a=f['cam']*b.Pos(-227.584,0,0)*cam;z=f['distributor']*dist;distance=a.distance_to(z);common=a.intersect(z)if distance<1e-7 else None;volume=solid_volume(common)if common is not None else 0
 row={'event_degrees':11.25,'axial_mm':axial,'distance_mm':distance,'overlap_mm3':volume};rows.append(row);print(row,flush=True);assert distance>1e-7 and volume==0
paths=[Path(__file__),Path(poses.__file__),cp,dp,R/'cad/engine/oil_drive_layout.py',R/'cad/engine/timing_coupled_core_candidate.py'];r={'scope':'Two fullcam/distributor interstitial snapshots, no whole-engine collision inference','rows':rows,'input_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths}};(R/'inventory/engine/cam-composed-drive-pair-review.json').write_text(json.dumps(r,indent=2)+'\n')
