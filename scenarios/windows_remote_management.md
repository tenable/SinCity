# Windows Remote Management Secnario

**Tags:** T1021.006

## Description

Adversaries may use Valid Accounts to interact with remote systems using Windows Remote Management (WinRM). The adversary may then perform actions as the logged-on user.

## Implementation

This scenario will add the `main_user` under the `main_workstation` to the local group `Remote Management Users`.

References:

- https://attack.mitre.org/techniques/T1021/006/
