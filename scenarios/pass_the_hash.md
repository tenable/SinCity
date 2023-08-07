# Pass The Hash Scenario

**Tags:** T1550.002

## Description

Adversaries may "pass the hash" using stolen password hashes to move laterally within an environment, bypassing normal system access controls. Pass the hash (PtH) is a method of authenticating as a user without having access to the user's cleartext password. This method bypasses standard authentication steps that require a cleartext password, moving directly into the portion of the authentication that uses the password hash.

## Implementation

This scenario will will create a local user on `main_workstation` and `main_dc` called: `alpha_root` which is a local administrator.

References:

- https://attack.mitre.org/techniques/T1550/002/