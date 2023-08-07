# Application Window Discovery Scenario

**Tags:** T1010

## Description

Adversaries may enumerate the open application windows on a system in order to gather information about the systems and applications in use on a network, or to identify potential targets for further exploitation. This can be done through various methods, such as using system utilities or API calls to retrieve information about the applications and windows that are currently open on a system.

## Implementation

This scenario will create a new user called `kabiler_jake` under the `main_workstation`. The user will be added to the group `Administrators` which will allow kabiler to be a local admin on this machine.

References:

- https://attack.mitre.org/techniques/T1010/
