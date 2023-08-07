# Windows Management Instrumentation Event Subscription Scenario

**Tags:** T1546.003

## Description

Adversaries may establish persistence and elevate privileges by executing malicious content triggered by a Windows Management Instrumentation (WMI) event subscription. WMI can be used to install event filters, providers, consumers, and bindings that execute code when a defined event occurs. Examples of events that may be subscribed to are the wall clock time, user logging, or the computer's uptime.

## Implementation

There is no implementation for this scenario.

References:

- https://attack.mitre.org/techniques/T1546/003/