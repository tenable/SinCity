# Archive via Custom Method Scenario

**Tags:** T1560.003

## Description

Adversaries may compress and archive data using custom or non-standard methods in order to reduce the size of data for exfiltration or to obscure the contents of the data. This can be done through the use of custom utilities or scripts that are designed to compress and archive data in a specific way, or by modifying the behavior of standard archiving utilities.

## Implementation

This scenario will create a new user called `visa_martin` under the `main_workstation`. The user will be added to the `Administrators` group.

References:

- https://attack.mitre.org/techniques/T1560/003/
