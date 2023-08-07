#!/bin/sh

# Give run permissions to sincity
chmod +x ./sincity.sh

cd tools/python
python3 -m pip install -r requirements.txt
