#!/usr/bin/env bash
set -euo pipefail
# Run from repository root; argument is a prepared Python interpreter.
PYTHON_BIN=${1:-.venv-cad-plugin/bin/python}
ARM=docs/benchmarks/text-to-cad-20261003/plugin
export CADGEN_DAEMON=0
export CADGEN_CACHE_DIR=${CADGEN_CACHE_DIR:-"$(pwd)/cad/engine/generated/text-to-cad-20261003/plugin/.cache"}
"$PYTHON_BIN" "$ARM/block_core_cup_mps59a.py" --json > "$ARM/logs/reproduced-build.log" 2>&1
"$PYTHON_BIN" "$ARM/check.py" > "$ARM/logs/reproduced-check.log" 2>&1
"$PYTHON_BIN" -m cadgen.cli step snapshot --job "$ARM/snapshot.json" > "$ARM/logs/reproduced-cad-snapshot.log" 2>&1
"$PYTHON_BIN" -m cadgen.cli step snapshot cad/engine/generated/text-to-cad-20261003/plugin/block_core_cup_mps59a.step "$ARM/cad-section.png" --mode section --section XZ > "$ARM/logs/reproduced-section.log" 2>&1
"$PYTHON_BIN" -m cadgen.cli glb snapshot cad/engine/generated/text-to-cad-20261003/plugin/block_core_cup_mps59a.glb "$ARM/mesh-opening.png" > "$ARM/logs/reproduced-mesh-snapshot.log" 2>&1
