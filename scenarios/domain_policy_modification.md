# Domain Policy Modification Scenario

**Tags:** T1484

## Description

Adversaries may modify the configuration settings of a domain to evade defenses and/or escalate privileges in domain environments. Domains provide a centralized means of managing how computer resources (ex: computers, user accounts) can act, and interact with each other, on a network. The policy of the domain also includes configuration settings that may apply between domains in a multi-domain/forest environment. Modifications to domain settings may include altering domain Group Policy Objects (GPOs) or changing trust settings for domains, including federation trusts.

## Implementation

This scenario will create a new user called `jorli_manic` and will give permission to the `main_user` called `GenericAll`.

References:

- https://attack.mitre.org/techniques/T1484/