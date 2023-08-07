# Indicator Removal From Tools Scenario

**Tags:** T1027.005

## Description

Adversaries may remove indicators from tools if they believe their malicious tool was detected, quarantined, or otherwise curtailed. They can modify the tool by removing the indicator and using the updated version that is no longer detected by the target's defensive systems or subsequent targets that may use similar systems.

## Implementation

This scenario will create a new user called "jake_jill" on the `main_workstation`. The user will have a description and a password of `dsa@d2#zs`.

References:

- https://attack.mitre.org/techniques/T1027/005/