# Password Policy Discovery Scenario

**Tags:** T1201

## Description

Adversaries may "pass the hash" using stolen password hashes to move laterally within an environment, bypassing normal system access controls. Pass the hash (PtH) is a method of authenticating as a user without having access to the user's cleartext password. This method bypasses standard authentication steps that require a cleartext password, moving directly into the portion of the authentication that uses the password hash.

## Implementation

This scenario will create a new domain user called `tom_hanks` under the `main_domain`.

References:

- https://attack.mitre.org/techniques/T1201/