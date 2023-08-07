# Exfiltration Over Symmetrically Encrypted Non-C2 Protocol Scenario

**Tags:** T1048.001, T1048.002

## Description

Adversaries may exfiltrate data from an environment over a symmetrically encrypted non-command and control (C2) protocol in order to conceal their actions and evade detection. This technique can be used to transfer data out of an environment in a secure and covert manner, potentially using a protocol that is not normally used for C2 communication.

## Implementation

This scenario will run a process called `dummy_secured_connection.ps1` on the `main_workstation`, which will create network requests.

References:

- https://attack.mitre.org/techniques/T1048/001/
- https://attack.mitre.org/techniques/T1048/002/
