# Remote Desktop Protocol Scenario

**Tags:** T1021.001

## Description

Adversaries may use Valid Accounts to log into a computer using the Remote Desktop Protocol (RDP). The adversary may then perform actions as the logged-on user.

## Implementation

This scenario will add the `main_user` under the `main_domain` to the `Remote Dekstop Protocol` group.

References:

- https://attack.mitre.org/techniques/T1021/001/
