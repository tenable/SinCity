# Windows Command Shell Scenario

**Tags:** T1059.003

## Description

Adversaries may abuse the Windows command shell for execution. The Windows command shell (cmd) is the primary command prompt on Windows systems. The Windows command prompt can be used to control almost any aspect of a system, with various permission levels required for different subsets of commands. The command prompt can be invoked remotely via Remote Services such as SSH.

## Implementation

This scenario will change the registry key `HKLM:\Software\Policies\Microsoft\Windows\System\DisableCMD` to 1.

References:

- https://attack.mitre.org/techniques/T1059/003/