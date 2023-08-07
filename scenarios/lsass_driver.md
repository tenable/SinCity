# Boot or Logon Autostart Execution: LSASS Driver Scenario

**Tags:** T1547.008

## Description

Adversaries may modify or add LSASS drivers to obtain persistence on compromised systems. The Windows security subsystem is a set of components that manage and enforce the security policy for a computer or domain. The Local Security Authority (LSA) is the main component responsible for local security policy and user authentication. The LSA includes multiple dynamic link libraries (DLLs) associated with various other security functions, all of which run in the context of the LSA Subsystem Service (LSASS) lsass.exe process.[1]

## Implementation

This scenario will change the registry keys:

- HKLM:\SYSTEM\CurrentControlSet\Control\Lsa\RunAsPPL to 1.
- HKLM:\SYSTEM\CurrentControlSet\Control\Lsa\LsaCfgFlags to 1.

References:

- https://attack.mitre.org/techniques/T1547/008/