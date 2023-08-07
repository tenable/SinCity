# Authentication Packages Scenario

**Tags:** T1547.002

## Description

Adversaries may modify authentication packages in order to bypass authentication controls or to capture and replay authentication credentials. This can be done through the modification of registry keys or by injecting malicious code into existing authentication packages.

## Implementation

This scenario will modify the "Authentication Packages" registry key under the `HKLM:\SYSTEM\CurrentControlSet\Control\Lsa` path on the `main_workstation`. The registry key will be set to a data value of `1` and a type of `multistring`.

References:

- https://attack.mitre.org/techniques/T1547/002/
