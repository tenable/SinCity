# Domain Groups Scenario

**Tags:** T1069.002

## Description

Adversaries may attempt to find domain-level groups and permission settings. The knowledge of domain-level permission groups can help adversaries determine which groups exist and which users belong to a particular group. Adversaries may use this information to determine which users have elevated permissions, such as domain administrators.

## Implementation

This scenario will add a new user called `dummy.user` under the `main_domain` to a new group called `Dummy Group`.

References:

- https://attack.mitre.org/techniques/T1069/002/