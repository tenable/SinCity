# Hidden Files And Directories Scenario

**Tags:** T1564.001

## Description

Adversaries may set files and directories to be hidden to evade detection mechanisms. To prevent normal users from accidentally changing special files on a system, most operating systems have the concept of a ‘hidden’ file. These files don’t show up when a user browses the file system with a GUI or when using normal commands on the command line. Users must explicitly ask to show the hidden files either via a series of Graphical User Interface (GUI) prompts or with command line switches (dir /a for Windows and ls –a for Linux and macOS).

## Implementation

There is not implementation for this scenario.

References:

- https://attack.mitre.org/techniques/T1564/001/