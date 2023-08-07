# Direct Volume Access Scenario

**Tags:** T1006

## Description

Adversaries may directly access a volume to bypass file access controls and file system monitoring. Windows allows programs to have direct access to logical volumes. Programs with direct access may read and write files directly from the drive by analyzing file system data structures. This technique bypasses Windows file access controls as well as file system monitoring tools


## Implementation

This scenario will create a new user called "kabiler_jake" on the main_workstation. The user will have a description and a password of s3#fds1 and will be added to the Administrators group.

References:

- T1006
