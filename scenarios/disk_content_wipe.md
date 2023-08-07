# Disk Content Wipe Tools Scenario

**Tags:** T1561.001

## Description

Adversaries may erase the contents of storage devices on specific systems or in large numbers in a network to interrupt availability to system and network resources.

Adversaries may partially or completely overwrite the contents of a storage device rendering the data irrecoverable through the storage interface.[1][2][3] Instead of wiping specific disk structures or files, adversaries with destructive intent may wipe arbitrary portions of disk content. To wipe disk content, adversaries may acquire direct access to the hard drive in order to overwrite arbitrarily sized portions of disk with random data.[2] Adversaries have been observed leveraging third-party drivers like RawDisk to directly access disk content.[1][2] This behavior is distinct from Data Destruction because sections of the disk are erased instead of individual files.

## Implementation

There is no implementation for this scenario.

References:

- T1561.001
