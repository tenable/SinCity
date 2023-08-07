# Logon Script Scenario

**Tags:** T1037.001

## Description

Adversaries may use Windows logon scripts automatically executed at logon initialization to establish persistence. Windows allows logon scripts to be run whenever a specific user or group of users log into a system.This is done via adding a path to a script to the HKCU\Environment\UserInitMprLogonScript Registry key.

## Implementation

This scenario has no implementation.

References:

- https://attack.mitre.org/techniques/T1037/001/