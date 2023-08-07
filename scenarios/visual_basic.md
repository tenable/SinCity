# Visual Basic Scenario

**Tags:** T1059.005

## Description

Adversaries may abuse Visual Basic (VB) for execution. VB is a programming language created by Microsoft with interoperability with many Windows technologies such as Component Object Model and the Native API through the Windows API. Although tagged as legacy with no planned future evolutions, VB is integrated and supported in the .NET Framework and cross-platform .NET Core.[

## Implementation

This scenario will change the registry key `HKLM:\SYSTEM\CurrentControlSet\Control\Lsa\scheduled_task_force_authenticated_account` to 1.

References:

- https://attack.mitre.org/techniques/T1059/005/