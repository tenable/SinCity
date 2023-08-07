# Service File Permissions Weakness Scenario

**Tags:** T1574.010

## Description

Adversaries may execute their own malicious payloads by hijacking the binaries used by services. Adversaries may use flaws in the permissions of Windows services to replace the binary that is executed upon service start. These service processes may automatically execute specific binaries as part of their functionality or to perform other actions. If the permissions on the file system directory containing a target binary, or permissions on the binary itself are improperly set, then the target binary may be overwritten with another binary using user-level permissions and executed by the original process. If the original process and thread are running under a higher permissions level, then the replaced binary will also execute under higher-level permissions, which could include SYSTEM.

## Implementation

This scenario will create a new service called `SinCityWeakServiceLogger` which is stored under the directory `C:\Services`, that the `main_user` has full permissions to.

References:

- https://attack.mitre.org/techniques/T1574/010/