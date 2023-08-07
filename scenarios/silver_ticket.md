# Silver Ticket Scenario

**Tags:** T1558.002

## Description

Adversaries who have the password hash of a target service account (e.g. SharePoint, MSSQL) may forge Kerberos ticket granting service (TGS) tickets, also known as silver tickets. Kerberos TGS tickets are also known as service tickets.

## Implementation

This scenario will create a new user called `kabiler_jake` under the `main_workstation`. The user will be added to the `Administrators` group.

References:

- https://attack.mitre.org/techniques/T1558/002/