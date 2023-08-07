# DCSync Scenario

**Tags:** T1003.006

## Description

Adversaries may attempt to access credentials and other sensitive information by abusing a Windows Domain Controller's application programming interface to simulate the replication process from a remote domain controller using a technique called DCSync.

## Implementation

This scenario will modify the `main_user` under the `main_domain` and add it the GenericAll ACL to the domain.

References:

- https://attack.mitre.org/techniques/T1003/006/