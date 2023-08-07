# Password Cracking Scenario

**Tags:** T1110.002

## Description

Adversaries may use password cracking to attempt to recover usable credentials, such as plaintext passwords, when credential material such as password hashes are obtained. OS Credential Dumping can be used to obtain password hashes, this may only get an adversary so far when Pass the Hash is not an option. Further, adversaries may leverage Data from Configuration Repository in order to obtain hashed credentials for network devices.

## Implementation

This scenario will change the `main_user` under the `main_domain` to have a simple to crack password.

References:

- https://attack.mitre.org/techniques/T1110/002/