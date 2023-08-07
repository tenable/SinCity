# Domain User with Email Scenario

**Tags:** T1486

## Description

Adversaries may encrypt data on target systems or on large numbers of systems in a network to interrupt availability to system and network resources. They can attempt to render stored data inaccessible by encrypting files or data on local and remote drives and withholding access to a decryption key. This may be done in order to extract monetary compensation from a victim in exchange for decryption or a decryption key (ransomware) or to render data permanently inaccessible in cases where the key is not saved or transmitted.

## Implementation

This scenario will set the email address of the `main_user` under the `main_domain` to `harry.potter@hogwarts.com`.

References:

- https://attack.mitre.org/techniques/T1486/
