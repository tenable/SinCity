# Firmware Corruption Scenario

**Tags:** T1495

## Description

Adversaries may overwrite or corrupt the flash memory contents of system BIOS or other firmware in devices attached to a system in order to render them inoperable or unable to boot, thus denying the availability to use the devices and/or the system. Firmware is software that is loaded and executed from non-volatile memory on hardware devices in order to initialize and manage device functionality. These devices may include the motherboard, hard drive, or video cards.

## Implementation

This scenario will disable BitLocker on the `main_workstation`.

References:

- https://attack.mitre.org/techniques/T1495/