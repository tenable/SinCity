# Image File Execution Options Injection Scenario

**Tags:** T1546.012

## Description

Adversaries may establish persistence and/or elevate privileges by executing malicious content triggered by Image File Execution Options (IFEO) debuggers. IFEOs enable a developer to attach a debugger to an application. When a process is created, a debugger present in an application’s IFEO will be prepended to the application’s name, effectively launching the new process under the debugger (e.g., C:\dbg\ntsd.exe -g notepad.exe). 

## Implementation

There is not implementation for this scenario.

References:

- https://attack.mitre.org/techniques/T1546/012/