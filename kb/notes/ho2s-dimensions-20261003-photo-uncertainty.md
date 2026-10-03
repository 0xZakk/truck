---
title: "A known hex size does not remove perspective uncertainty"
kind: how-it-works
source: "[[sources/ho2s-dimensions-20261003-photo-scale|Bosch photograph projection analysis]]"
related:
  - "[[notes/ho2s-online-20261003-exterior|Exterior topology and missing fit evidence]]"
tags: [engine, oxygen-sensor, reconstruction]
---

The Bosch 22 mm hex provides a useful scale anchor, but a hex's projected width changes with rotation. A silhouette can span 22 mm across flats or about 25.4 mm across corners even before perspective and image-pick uncertainty. Axial measurements are additionally shortened when the sensor points toward the camera.

The committed analysis keeps these assumptions explicit. Its thread pitch range includes both 1.25 mm and1.5 mm, so choosing 1.5 mm for an illustrative model is an engineering assumption rather than a measurement. Connector estimates use wider depth/foreshortening scenarios because it is not established coplanar with the hex. Future source changes or a calibrated camera fit must regenerate the estimates.

## Related Concepts

- [[notes/ho2s-online-20261003-exterior|Exterior topology and missing fit evidence]]

## Source

[[sources/ho2s-dimensions-20261003-photo-scale|Bosch photograph projection analysis]]
