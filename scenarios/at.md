# AT Scenario

**Tags:** T1053.002

## Description

Adversaries may create a scheduled task or job on a system in order to execute arbitrary code or commands at a later time. This can be done through the use of built-in scheduling utilities, such as `at`, or by modifying the configuration of existing tasks or jobs.

## Implementation

This scenario will create a scheduled task called "echo_hello" on the `main_workstation`. The task will run the `cmd.exe` command with the arguments `/c "echo hello world!"` and will be set to run under the username and password of the "main_domain.domain_admin" user. The task is also enabled, which means it will run according to its schedule.

References:

- https://attack.mitre.org/techniques/T1053/002/
