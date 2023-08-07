# Masquerade Task or Service Scenario

**Tags:** T1036.004

## Description

Adversaries may make and impersonate tokens to escalate privileges and bypass access controls. If an adversary has a username and password but the user is not logged onto the system, the adversary can then create a logon session for the user using the LogonUser function. The function will return a copy of the new session's access token and the adversary can use SetThreadToken to assign the token to a thread.

## Implementation

This scenario will create a new user called "jordan_pete" on the `main_workstation`. The user will have a description and a password of `zs@dkf13@` and will be added to the `Local Administrators` and `Administrators` groups.

References:

- T1036.004