# Network Share Connection Removal Scenario

**Tags:** T1070.005

## Description

Adversaries may remove share connections that are no longer useful in order to clean up traces of their operation. Windows shared drive and SMB/Windows Admin Shares connections can be removed when no longer needed. Net is an example utility that can be used to remove network share connections with the net use \system\share /delete command.

## Implementation

This scenario will create a new user called "jordan_pete" on the `main_workstation`. The user will have a description and a password of `zs@dkf13@` and will be added to the `Local Administrators` and `Administrators` groups.

References:

- https://attack.mitre.org/techniques/T1070/005/