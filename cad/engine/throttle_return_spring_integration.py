"""Illustrative single spring with stationary and moving captured hooks.

This records teaching geometry, not Ford spring count or production dimensions.
"""
from pathlib import Path
import hashlib
import build123d as b
import throttle_return_spring_candidate as candidate
ROOT=Path(__file__).resolve().parents[2]
NEW_IDS={'throttle-return-spring-illustrative'}
CHANGED_IDS=NEW_IDS|{'accelerator-cable-bracket','throttle-lever-estimated'}
SOURCE_ID='throttle-return-spring-study'
GAPS=['One illustrative torsion spring explains fixed/moving anchors; actual Ford spring count, tang construction, dimensions and stops remain unverified.',
      'Wire motion preserves geometric length; no preload, spring rate, stress, fatigue, friction or guaranteed return force is simulated.',
      'Cable-end compression spring is a separate factory-documented component and is not represented by this torsion spring.',
      'Bracket and lever anchor holes, wire diameter and retention hooks are inferred; attachment strength and installation flexure are unverified.']

def install(define,add,definitions,occurrences,shapes):
    old={d['id']:d for d in definitions}
    shaft=shapes.get('throttle-shaft')
    if shaft is None:shaft=b.import_step(ROOT/old['throttle-shaft']['step'].lstrip('/'))
    fixed,moving=candidate.seats(shaft)
    pieces={'accelerator-cable-bracket':fixed['accelerator-bracket-spring-seat-estimated'],
            'throttle-lever-estimated':moving['throttle-lever-spring-seat-estimated'],
            'throttle-return-spring-illustrative':candidate.spring(0)}
    definitions[:]=[d for d in definitions if d['id'] not in CHANGED_IDS]
    occurrences[:]=[o for o in occurrences if o['id'] not in NEW_IDS]
    for ident,shape in pieces.items():
        previous=old.get(ident,{})
        define(ident,shape,previous.get('name','Throttle return spring · illustrative'),
               previous.get('function','Shows a torsion spring winding between a fixed bracket hook and a rotating lever hook as the throttle opens.'),
               'induction',previous.get('color','#bc995a'),
               list(dict.fromkeys(previous.get('sources',[])+[SOURCE_ID])),GAPS)
        if ident in NEW_IDS:
            add(ident,ident,'throttle-assembly',explode=(0,150,50))
            occurrences[-1]['throttle_spring']={'model':'illustrative-single-v1','angle_min_deg':0,'angle_max_deg':90}

def sources():
    path=ROOT/'reference/engine/throttle-return-spring-review.json'
    return {SOURCE_ID:{'title':'Factory spring-function evidence and illustrative shaft-spring scope',
                      'path':'/reference/engine/throttle-return-spring-review.json',
                      'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}}
