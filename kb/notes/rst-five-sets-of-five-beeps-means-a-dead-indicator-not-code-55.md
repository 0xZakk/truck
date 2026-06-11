---
title: "Five sets of five beeps means a dead air bag indicator with a fault present, not code 55"
kind: troubleshooting
source: "[[sources/rst-air-bag-diagnostic-monitor|Air Bag Diagnostic Monitor and Trouble Codes — Description, Operation, and Diagnostics (FSM)]]"
related:
  - "[[notes/rly-air-bag-monitor-flashes-two-digit-codes-and-beeps-if-the-lamp-is-dead|The air bag monitor self-tests the indicator for six seconds and flashes two-digit trouble codes within 30 seconds, or beeps five sets of five if the lamp is dead]]"
tags:
  - air-bag
  - warning-chime
  - tone-generator
  - diagnosis
---

The SRS has a backup audible alert for the case where the warning lamp itself has failed. If a system fault
exists AND the air bag indicator is inoperative, the tone generator sounds a series of five sets of five
beeps. The FSM explicitly warns this is NOT a diagnostic trouble code 55 — it simply tells you two things at
once: the air bag indicator is dead and there is an unserviced fault in the system.

The practical implication during diagnosis is to not chase a "code 55" that does not exist. Instead, treat
the tone as a prompt to first restore the indicator lamp circuit (so codes can actually be read) and then
diagnose the underlying fault the monitor is holding. Because the audible path is separate from the visual
one, the system can still signal trouble in the `interior` cabin even with a burned-out cluster bulb.

> "The tone is a series of five sets of five beeps. This does not indicate a diagnostic trouble code 55. If
> the tone is heard, the air bag indicator is inoperative and a system fault that requires service is present."

## Related Concepts

- [[notes/rly-air-bag-monitor-flashes-two-digit-codes-and-beeps-if-the-lamp-is-dead|The air bag monitor self-tests the indicator for six seconds and flashes two-digit trouble codes within 30 seconds, or beeps five sets of five if the lamp is dead]]
- [[notes/rst-thermal-fuse-disables-deployment-and-must-not-be-jumpered|The diagnostic monitor's thermal fuse disables deployment and must never be jumpered]]

## Source

- [[sources/rst-air-bag-diagnostic-monitor|Air Bag Diagnostic Monitor and Trouble Codes — Description, Operation, and Diagnostics (FSM)]]
