# The apps directory

This directory contains the apps that SinCity uses:

- dockerapp - A simple NodeJS based API that has only a single endpoint called `test` which will be used under k8s.
- SinCityLogger - A simple service that writes a log into `c:\sincity_logger.txt` file every minute.