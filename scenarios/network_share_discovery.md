# Network Share Discovery Scenario

**Tags:** T1135

## Description

Adversaries may look for folders and drives shared on remote systems as a means of identifying sources of information to gather as a precursor for Collection and to identify potential systems of interest for Lateral Movement. Networks often contain shared network drives and folders that enable users to access file directories on various systems across a network.

## Implementation

This scenario will add a new share under the `main_workstation`.

References:

- https://attack.mitre.org/techniques/T1135/