# Netsh Helper DLL Scenario

**Tags:** T1546.007

## Description

Adversaries may establish persistence by executing malicious content triggered by Netsh Helper DLLs. Netsh.exe (also referred to as Netshell) is a command-line scripting utility used to interact with the network configuration of a system. It contains functionality to add helper DLLs for extending functionality of the utility.The paths to registered netsh.exe helper DLLs are entered into the Windows Registry at HKLM\SOFTWARE\Microsoft\Netsh.

## Implementation

This scenario has no implementation.

References:

- https://attack.mitre.org/techniques/T1546/007/