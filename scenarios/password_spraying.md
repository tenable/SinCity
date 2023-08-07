# Password Spraying Scenario

**Tags:** T1110.003

## Description

Adversaries may use a single or small list of commonly used passwords against many different accounts to attempt to acquire valid account credentials. Password spraying uses one password (e.g. 'Password01'), or a small list of commonly used passwords, that may match the complexity policy of the domain. Logins are attempted with that password against many different accounts on a network to avoid account lockouts that would normally occur when brute forcing a single account with many passwords.

## Implementation

This scenario will change the `main_user` and `sec_user` domain account (under the `main_domain`) passwords to be the same password.

References:

- https://attack.mitre.org/techniques/T1110/003/