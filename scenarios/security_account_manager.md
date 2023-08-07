# Security Account Manager Scenario

**Tags:** T1003.002

## Description

Adversaries may attempt to extract credential material from the Security Account Manager (SAM) database either through in-memory techniques or through the Windows Registry where the SAM database is stored.

## Implementation

This scenario will add a new user called "locally" under the `main_workstation`.

References:

- https://attack.mitre.org/techniques/T1003/002/
