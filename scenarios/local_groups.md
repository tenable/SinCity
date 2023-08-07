# Local Groups Scenario

**Tags:** T1069.001

## Description


Adversaries may attempt to find local system groups and permission settings. The knowledge of local system permission groups can help adversaries determine which groups exist and which users belong to a particular group. Adversaries may use this information to determine which users have elevated permissions, such as the users found within the local administrators group.

Commands such as net localgroup of the Net utility, dscl . -list /Groups on macOS, and groups on Linux can list local groups.

## Implementation

This scenario will create a local group called 'Howard Guys' and a user called 'alex_george' under it.

References:

- https://attack.mitre.org/techniques/T1069/001/