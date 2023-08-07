# Code Signing Scenario

**Tags:** T1553.002

## Description

Adversaries may use code signing to sign malicious code to make it appear legitimate and bypass security warnings and controls. This can be done by obtaining a valid code signing certificate or by compromising a legitimate certificate through social engineering, exploitation, or by purchasing a valid certificate from a third party.

## Implementation

This scenario will create a new user called "jordan_pete" on the `main_workstation`. The user will have a description and a password of `zs@dkf13@` and will be added to the `Local Administrators` and `Administrators` groups.

References:

- https://attack.mitre.org/techniques/T1553/002/
