# System Shutdown/Reboot Scenario

**Tags:** T1529

## Description

Adversaries may shutdown/reboot systems to interrupt access to, or aid in the destruction of, those systems. Operating systems may contain commands to initiate a shutdown/reboot of a machine or network device. In some cases, these commands may also be used to initiate a shutdown/reboot of a remote computer or network device via Network Device CLI (e.g. reload). Shutting down or rebooting systems may disrupt access to computer resources for legitimate users.

## Implementation

This scenario will create a new user called "kabiler_jake" on the main_workstation. The user will have a description and a password of s3#fds1 and will be added to the Administrators group.

References:

- https://attack.mitre.org/techniques/T1529/