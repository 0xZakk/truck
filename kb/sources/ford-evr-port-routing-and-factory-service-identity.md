---
title: "Ford EVR port routing and factory service identity"
source: reference/engine/evr-factory-capture.txt
type: local
date: 2026-09-24
author: "Ford service information, archived by Operation CHARM"
tags: [engine, egr, vacuum, electrical]
processed: false
---

## Summary

The archived 1994 4.9L service description identifies the EGR vacuum regulator as the electromagnetic device that regulates vacuum delivered to the EGR valve. Manifold vacuum supplies it, and the PCM varies its duty cycle to change the output vacuum.

The external illustration labels the upper hose nipple as the EGR-valve connection and the lower nipple as the vacuum-source connection. It shows a side electrical connector, mounting ear and round upper cap. It supplies no internal section or dimensional scale. The vehicle-selected parts table prints the service number as `FOTZ9J459A`; the letter O versus digit zero is preserved here rather than silently corrected.

## Key Points

- The vacuum source and controlled output are distinct ports.
- Increasing command duty cycle increases the described vacuum signal.
- Electrical circuit evidence is separately captured in [[sources/the-4-9l-evtm-separates-egr-vacuum-command-and-position-feedback|4.9L EVTM EGR circuits]].
- Standard VS52 appears in retailer cross-references and remains a lead pending manufacturer verification.

## Captured Content

`reference/engine/evr-factory-reviewed.json` records archived paths, hashes and image observations. Normalized text is in `kb/.raw/ford-evr-port-routing-and-factory-service-identity.txt`.
