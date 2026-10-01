"""Compose two reviewed disjoint changes; no new estimated dimensions."""
from pathlib import Path
import json
import build123d as b
import timing_valvetrain_inclined_candidate as deck
ROOT=Path(__file__).resolve().parents[2]
FOOT=ROOT/'cad/engine/generated/timing-pump-foot-faceted-candidate/block.step'
DECK=ROOT/'cad/engine/generated/timing-valvetrain-inclined-candidate/block.step'
def build():
    original=b.import_step(FOOT)
    manifest=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text())
    return deck.block_adapter(original,manifest),original
