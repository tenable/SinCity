# Services Registry Permissions Weakness Scenario

**Tags:** T1574.011

## Description

Adversaries may execute their own malicious payloads by hijacking the Registry entries used by services. Adversaries may use flaws in the permissions for Registry keys related to services to redirect from the originally specified executable to one that they control, in order to launch their own code when a service starts.

## Implementation

This scenario will add a new user called "locally" under the `main_workstation`.

References:

- https://attack.mitre.org/techniques/T1574/011/
