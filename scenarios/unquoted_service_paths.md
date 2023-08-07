# Unquoted Service Paths Scenario

**Tags:** T1574.009

## Description

Adversaries may execute their own malicious payloads by hijacking vulnerable file path references. Adversaries can take advantage of paths that lack surrounding quotations by placing an executable in a higher level directory within the path, so that Windows will choose the adversary's executable to launch.

## Implementation

This scenario will copy a new service called `SinCityLogger` to the `main_workstation` and run it under a specific domain user account.

References:

- https://attack.mitre.org/techniques/T1574/009/
