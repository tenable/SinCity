# Security Support Provider Scenario

**Tags:** T1547.005

## Description

Adversaries may abuse security support providers (SSPs) to execute DLLs when the system boots. Windows SSP DLLs are loaded into the Local Security Authority (LSA) process at system start. Once loaded into the LSA, SSP DLLs have access to encrypted and plaintext passwords that are stored in Windows, such as any logged-on user's Domain password or smart card PINs.

## Implementation

This scenario will .

References:

- https://attack.mitre.org/techniques/T1547/005/