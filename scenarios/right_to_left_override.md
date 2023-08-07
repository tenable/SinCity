# Right To Left Scenario

**Tags:** T1036.002

## Description

Adversaries may abuse the right-to-left override (RTLO or RLO) character (U+202E) to disguise a string and/or file name to make it appear benign. RTLO is a non-printing Unicode character that causes the text that follows it to be displayed in reverse. For example, a Windows screensaver executable named March 25 \u202Excod.scr will display as March 25 rcs.docx. A JavaScript file named photo_high_re\u202Egnp.js will be displayed as photo_high_resj.png.

## Implementation

This scenario will create a new user called "jake_jill" on the `main_workstation`. The user will have a description and a password of `dsa@d2#zs`.

References:

- https://attack.mitre.org/techniques/T1036/002/