# Disable or Modify System Firewall Scenario

**Tags:** T1562.004

## Description

Adversaries may disable or modify system firewalls in order to bypass controls limiting network usage. Changes could be disabling the entire mechanism as well as adding, deleting, or modifying particular rules. This can be done numerous ways depending on the operating system, including via command-line, editing Windows Registry keys, and Windows Control Panel.

## Implementation

This scenario will disable the firewall on the `main_workstation`. It's not clear from the configuration how the firewall will be modified or what communication will be allowed through the firewall.

References:

- https://attack.mitre.org/techniques/T1562/004/
