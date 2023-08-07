# Network Logon Script Scenario

**Tags:** T1037.003

## Description

Adversaries may manipulate the network logon script path for a target user in order to gain access to additional resources or escalate privileges. This can be achieved by modifying the logon process for the target user.

## Implementation

This scenario will modify the access control list (ACL) for the `main_domain` and grant the `Ext-Edit-Script-Path` right to the user specified by the `main_user` variable for the user specified by the `sec_user` variable. The inheritance for this ACL is set to "Descendents".

References:

- https://attack.mitre.org/techniques/T1037/003/
