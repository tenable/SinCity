# Archive via Standard Utility Scenario

**Tags:** T1560.001

## Description

Adversaries may compress and archive data using standard utilities, such as `zip`, `tar`, or `rar`, in order to reduce the size of data for exfiltration or to obscure the contents of the data. This can be done through the command line or using built-in archiving features in operating systems or applications.

## Implementation

This scenario will create a new user called `anshi_lora` under the `main_workstation`. The user will be added to the `Administrators` group.

References:

- https://attack.mitre.org/techniques/T1560/001/
