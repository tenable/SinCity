# System Owner/User Discovery Scenario

**Tags:** T1033

## Description

Adversaries may attempt to identify the primary user, currently logged in user, set of users that commonly uses a system, or whether a user is actively using the system. They may do this, for example, by retrieving account usernames or by using OS Credential Dumping. The information may be collected in a number of different ways using other Discovery techniques, because user and username details are prevalent throughout a system and include running process ownership, file/directory ownership, session information, and system logs. Adversaries may use the information from System Owner/User Discovery during automated discovery to shape follow-on behaviors, including whether or not the adversary fully infects the target and/or attempts specific actions.

## Implementation

This scenario will create a new user called "jake_jill" on the `main_workstation`. The user will have a description and a password of `dsa@d2#zs`.

References:

- https://attack.mitre.org/techniques/T1033/