# Account Access Removal Scenario

**Tags:** T1531

## Description

Adversaries may remove or disable access to accounts on a system or network in order to disrupt normal operations or maintain unauthorized access. This can be done through various methods, such as deleting user accounts, modifying account permissions or privileges, or disabling or blocking access to accounts through the use of credentials or other authentication methods.

## Implementation

This scenario will create a new user called `jordan_pete` under the `main_workstation`. The user will be added to a new group called the `Local Administrators` group, which is part of the  `Administrators` group.

References:

- https://attack.mitre.org/techniques/T1531/
