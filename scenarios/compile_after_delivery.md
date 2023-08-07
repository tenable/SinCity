# Compile After Delivery Scenario

**Tags:** T1027.004

## Description

Adversaries may attempt to make payloads difficult to discover and analyze by delivering files to victims as uncompiled code. Text-based source code files may subvert analysis and scrutiny from protections targeting executables/binaries. These payloads will need to be compiled before execution; typically via native utilities such as csc.exe or GCC/MinGW.

## Implementation

This scenario will create a new user called "jake_jill" on the `main_workstation`. The user will have a description and a password of `dsa@d2#zs`.

References:

- https://attack.mitre.org/techniques/T1027/004/
