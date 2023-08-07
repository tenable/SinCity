# Path Interception by Path Environment Variable Scenario

**Tags:** T1574.007

## Description

Adversaries may manipulate the PATH environment variable to cause a system to execute malicious programs instead of legitimate ones. This can be done by adding the directory containing the malicious program to the PATH environment variable and ensuring that the directory is earlier in the path than the legitimate directory.

## Implementation

This scenario will set the PATH environment variable on the `main_workstation` to `c:\users`.

References:

- https://attack.mitre.org/techniques/T1574/007/
