#!/bin/zsh
# Export a build123d CAD source to STEP (+ viewer GLB in models/).
#
# Usage: scripts/cad_export.sh cad/<part>.py [more sources...]
#
# Pipeline (text-to-cad skill, build123d on OpenCASCADE):
#   cad/<part>.py --[scripts/step]--> cad/<part>.step + models/<part>.glb
#
# CONVENTIONS (must match viewer + inventory/schema.md):
#   * 1 build123d unit = 1 INCH (sources read like the FSM dimensions).
#   * Build with +X forward, +Z up, +Y LEFT; origin = the part record's position.
#   * cadpy GLB export divides by 1000 (treats units as mm -> meters) and bakes
#     the Z-up -> Y-up swap into vertices, so the part record needs
#     "model": { "kind": "gltf", "src": "../models/<part>.glb", "glbScale": 1000 }
set -euo pipefail
cd "$(dirname "$0")/.."

SKILL="$HOME/.claude/plugins/cache/text-to-cad/cad/0.3.0/skills/cad"
PY="../../.venv-cad/bin/python"

for src in "$@"; do
  name="$(basename "$src" .py)"
  "$PY" "$SKILL/scripts/step" "$src" --glb "$name.glb"
  mv "cad/$name.glb" "models/$name.glb"
  echo "exported models/$name.glb"
done
