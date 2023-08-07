# Make and Impersonate Token Scenario

**Tags:** T1134.003

## Description

Adversaries may make and impersonate tokens to escalate privileges and bypass access controls. If an adversary has a username and password but the user is not logged onto the system, the adversary can then create a logon session for the user using the LogonUser function. The function will return a copy of the new session's access token and the adversary can use SetThreadToken to assign the token to a thread.

## Implementation

This scenario has no implementation.

References:

- T1134.003