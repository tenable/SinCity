# Group Policy Modification Scenario

**Tags:** T1484.001

## Description

Adversaries may modify Group Policy Objects (GPOs) to subvert the intended discretionary access controls for a domain, usually with the intention of escalating privileges on the domain. Group policy allows for centralized management of user and computer settings in Active Directory (AD). GPOs are containers for group policy settings made up of files stored within a predicable network path \<DOMAIN>\SYSVOL\<DOMAIN>\Policies\.

## Implementation

This scenario will create a new GPO called `vul_gpo_modification` and add the `main_user` under the `main_domain` to the provided GPO.

References:

- https://attack.mitre.org/techniques/T1484/001/
