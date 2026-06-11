#!/usr/bin/env bash
# Reproducibly download the 1994 Ford F-150 (4.9L I6, 2WD) manual library.
# Sources are free/legitimate. See manuals/INDEX.md for details.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
M="$ROOT/manuals"
mkdir -p "$M/factory-service-manual" "$M/owners-manual" "$M/brochures"

echo "==> 1/3  Factory service manual (charm.li, ~66MB zip -> ~125MB)"
FSM="$M/factory-service-manual"
if [ ! -d "$FSM/1994 Ford F 150 2WD Pickup L6-300 4.9L" ]; then
  curl -L --fail "https://charm.li/bundle/long-names/Ford/1994/F%20150%202WD%20Pickup%20L6-300%204.9L/" \
    -o "$FSM/fsm-bundle.zip"
  ( cd "$FSM" && unzip -o -q fsm-bundle.zip && rm -f fsm-bundle.zip )
else
  echo "    already present, skipping"
fi

echo "==> 2/3  Owner guide (1996 F-Series, same generation; fordservicecontent.com)"
curl -L --fail "https://www.fordservicecontent.com/Ford_Content/catalog/owner_guides/96f23og1e.pdf" \
  -o "$M/owners-manual/1996-Ford-F-Series-Owner-Guide-(same-gen-as-1994).pdf"

echo "==> 3/3  1994 sales brochures (xr793.com)"
curl -L --fail "https://xr793.com/wp-content/uploads/2022/12/1994-Ford-Trucks.pdf" \
  -o "$M/brochures/1994-Ford-Trucks-Sales-Brochure.pdf"
curl -L --fail "https://xr793.com/wp-content/uploads/2022/12/1994-Ford-Pickups-Chassis.pdf" \
  -o "$M/brochures/1994-Ford-Pickups-Chassis-Brochure.pdf"

echo "==> Done. See manuals/INDEX.md"
