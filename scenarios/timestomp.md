# Timestomp Scenario

**Tags:** T1070.006

## Description

Adversaries may modify file time attributes to hide new or changes to existing files. Timestomping is a technique that modifies the timestamps of a file (the modify, access, create, and change times), often to mimic files that are in the same folder. This is done, for example, on files that have been modified or created by the adversary so that they do not appear conspicuous to forensic investigators or file analysis tools.

Timestomping may be used along with file name Masquerading to hide malware and tools.

## Implementation

This scenario will create a new user called "kabiler_jake" on the main_workstation. The user will have a description and a password of s3#fds1 and will be added to the Administrators group.

References:

- https://attack.mitre.org/techniques/T1070/006/