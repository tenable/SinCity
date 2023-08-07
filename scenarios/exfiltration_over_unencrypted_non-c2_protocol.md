# Exfiltration Over Unencrypted Non-C2 Protocol Scenario

**Tags:** T1048.003

## Description

Adversaries may exfiltrate data from an environment over an unencrypted non-command and control (C2) protocol in order to transfer data out of an environment using a protocol that is not normally used for C2 communication. This technique may be necessary in certain situations where encryption is not possible or practical, but it can also make the exfiltration more detectable.

## Implementation

This scenario will run a process called `dummy_unsecured_connection.ps1` on the `main_workstation`, which will create network requests.

References:

- https://attack.mitre.org/techniques/T1048/003/
