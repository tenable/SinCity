# Rename System Utilities Scenario

Tags: T1036.003

## Description

Adversaries may rename legitimate system utilities to try to evade security mechanisms concerning the usage of those utilities. Security monitoring and control mechanisms may be in place for system utilities adversaries are capable of abusing. It may be possible to bypass those security mechanisms by renaming the utility prior to utilization (ex: rename rundll32.exe). An alternative case occurs when a legitimate utility is copied or moved to a different directory and renamed to avoid detections based on system utilities executing from non-standard paths.

## Implementation

This scenario will create a new user called "kabiler_jake" on the main_workstation. The user will have a description and a password of s3#fds1 and will be added to the Administrators group.

References:

- https://attack.mitre.org/techniques/T1036/003/