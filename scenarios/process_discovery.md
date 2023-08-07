# Process Discovery Scenario

Tags: T1057

## Description

Adversaries may attempt to list running processes on a system as a means of identifying legitimate processes to target and/or as a means of identifying anomalous or suspicious processes that could potentially be used for malicious purposes.

## Implementation

This scenario uses the action create_local_admin to create a local administrator user on the main_workstation. The scenario then demonstrates how to list running processes on the system using tools such as tasklist or ps.

References:

- https://attack.mitre.org/techniques/T1057/