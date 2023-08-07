# Indicator Blocking Scenario

**Tags:** T1027.005

## Description

Adversaries may remove indicators from tools if they believe their malicious tool was detected, quarantined, or otherwise curtailed. They can modify the tool by removing the indicator and using the updated version that is no longer detected by the target's defensive systems or subsequent targets that may use similar systems.

## Implementation

This scenario will create a new user called `jordan_pete` under the `main_workstation`. The user will be added to a new group called the `Local Administrators` group, which is part of the  `Administrators` group.

References:

- T1562.006