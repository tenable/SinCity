# Create Process With Token Scenario

**Tags:** T1134.002, T1134.001

## Description

Adversaries may create a new process with a different token to escalate privileges and bypass access controls. Processes can be created with the token and resulting security context of another user using features such as CreateProcessWithTokenW and runas.

## Implementation

This scenario will create a new user called `indiana_jones` under the `main_workstation`. The user will be added to the `Administrators` group and will then start a process called `dummy_process.bat`.

References:

- https://attack.mitre.org/techniques/T1134/002/