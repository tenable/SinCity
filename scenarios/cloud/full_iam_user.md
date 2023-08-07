# Full IAM User Scenario

**Tags:** None

## Description

An adversary may add additional roles or permissions to an adversary-controlled cloud account to maintain persistent access to a tenant. For example, they may update IAM policies in cloud-based environments or add a new global administrator in Office 365 environments.

With sufficient permissions, a compromised account can gain almost unlimited access to data and settings (including the ability to reset the passwords of other admins).

## Implementation

This scenario will create an admin with full access to AWS.

References:

- https://confluence.eng.tenable.com/pages/viewpage.action?spaceKey=CR&title=Additional+Cloud+Roles