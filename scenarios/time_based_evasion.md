# System Owner/User Discovery Scenario

**Tags:** T1497.003

## Description

Adversaries may employ various time-based methods to detect and avoid virtualization and analysis environments. This may include enumerating time-based properties, such as uptime or the system clock, as well as the use of timers or other triggers to avoid a virtual machine environment (VME) or sandbox, specifically those that are automated or only operate for a limited amount of time.

Adversaries may employ various time-based evasions, such as delaying malware functionality upon initial execution using programmatic sleep commands or native system scheduling functionality (ex: Scheduled Task/Job). Delays may also be based on waiting for specific victim conditions to be met (ex: system time, events, etc.) or employ scheduled Multi-Stage Channels to avoid analysis and scrutiny.

## Implementation

This scenario will create a new user called "jake_jill" on the `main_workstation`. The user will have a description and a password of `dsa@d2#zs`.

References:

- https://attack.mitre.org/techniques/T1497/003/