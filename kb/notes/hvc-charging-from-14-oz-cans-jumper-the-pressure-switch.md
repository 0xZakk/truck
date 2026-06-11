---
title: "Charge from cans by jumpering the pressure switch and running the A/C to 2.0 lb"
kind: procedure
source: "[[sources/hvc-system-service-procedures|A/C System Service — Recovery, Evacuation, Charging, Oil and Leak Detection (FSM)]]"
related:
  - "[[notes/hvc-evacuate-to-28-29-in-hg-adjusting-for-altitude|Evacuate the A/C system to 28–29.5 in Hg at sea level]]"
  - "[[notes/hvc-the-pressure-switch-protects-the-clutch-coil-at-low-suction|The refrigerant pressure switch cuts the clutch coil below 24.5 psi suction]]"
  - "[[notes/hvc-system-uses-r-134a-and-pag-oil|The A/C system holds 2.0 lb of R-134a and 7.0 oz of PAG oil]]"
tags: [hvac, charging, refrigerant, clutch-cycling-switch]
---

When recharging the 1994 F-150 (inventory id `hvac`) from 14 oz cans, the trick is getting the
compressor clutch to run on an empty system. After connecting the can adapter and purging air
from the center hose, disconnect the clutch-cycling pressure switch and install a jumper wire
across its connector — otherwise the low-pressure switch would keep the clutch from engaging.

Open the low-side valve to draw refrigerant in; once it stops drawing on its own, start the
engine, set the control to A/C with the blower on high, and let the running compressor pull in
the rest until 2.0 lb is in the system. Remove the jumper, reconnect the switch, then verify
operating pressures. A high-volume fan on the condenser during charging prevents excessive
pressure and overheating.

## Related Concepts

- [[notes/hvc-evacuate-to-28-29-in-hg-adjusting-for-altitude|Evacuate the A/C system to 28–29.5 in Hg at sea level]]
- [[notes/hvc-the-pressure-switch-protects-the-clutch-coil-at-low-suction|The refrigerant pressure switch cuts the clutch coil below 24.5 psi suction]]
- [[notes/hvc-system-uses-r-134a-and-pag-oil|The A/C system holds 2.0 lb of R-134a and 7.0 oz of PAG oil]]
- [[notes/hvc-recover-refrigerant-until-vacuum-holds-two-minutes|Recover refrigerant until the system holds vacuum for two minutes]]
- [[notes/hvc-the-wot-relay-cuts-ac-at-wide-open-throttle|The WOT A/C relay drops the compressor clutch at wide-open throttle]]
- [[notes/hvc-pcm-trims-idle-air-when-the-ac-clutch-engages|The PCM raises idle air when the A/C clutch engages to keep idle speed from sagging]]

## Source

- [[sources/hvc-system-service-procedures|A/C System Service — Recovery, Evacuation, Charging, Oil and Leak Detection (FSM)]]
