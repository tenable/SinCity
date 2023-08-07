# Service Stop Scenario

Tags: T1489

## Description

Adversaries may stop or disable services on a system to render those services unavailable to legitimate users. Stopping critical services or processes can inhibit or stop response to an incident or aid in the adversary's overall objectives to cause damage to the environment.

## Implementation

This scenario will create a new user called "kabiler_jake" on the main_workstation. The user will have a description and a password of s3#fds1 and will be added to the Administrators group.

References:

- https://attack.mitre.org/techniques/T1489/