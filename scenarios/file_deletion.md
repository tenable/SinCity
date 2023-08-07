# File Deletion Scenario

**Tags:** T1070.004

## Description

Adversaries may delete files left behind by the actions of their intrusion activity. Malware, tools, or other non-native files dropped or created on a system by an adversary (ex: Ingress Tool Transfer) may leave traces to indicate to what was done within a network and how. Removal of these files can occur during an intrusion, or as part of a post-intrusion process to minimize the adversary's footprint.

## Implementation

This scenario will create a new user called "jordan_pete" on the `main_workstation`. The user will have a description and a password of `zs@dkf13@` and will be added to the `Local Administrators` and `Administrators` groups.

References:

- https://attack.mitre.org/techniques/T1070/004/