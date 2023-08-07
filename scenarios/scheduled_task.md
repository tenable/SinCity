# Scheduled Task Scenario

**Tags:** T1053.005

## Description

Adversaries may abuse the Windows Task Scheduler to perform task scheduling for initial or recurring execution of malicious code. There are multiple ways to access the Task Scheduler in Windows. The schtasks utility can be run directly on the command line, or the Task Scheduler can be opened through the GUI within the Administrator Tools section of the Control Panel. In some cases, adversaries have used a .NET wrapper for the Windows Task Scheduler, and alternatively, adversaries have used the Windows netapi32 library to create a scheduled task.

## Implementation

This scenario will create a scheduled task called `echo_hello` and will change the registry key `HKLM:\SYSTEM\CurrentControlSet\Control\Lsa\scheduled_task_force_authenticated_account` to 1.

References:

- https://attack.mitre.org/techniques/T1053/005/