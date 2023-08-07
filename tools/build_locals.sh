#!/bin/bash

# This script will sync up all of the terraform 'locals.tf'
# from the `network.json` file to contain the updated code.
# This should be running after updating the 'network.json' file.

# Get the current working directory
cwd=$(pwd)
cd ./tools/python/src
# Run the build_locals.py as module
network_locals=$(python3 -m terraform.build_locals)

# Now go back
cd $cwd

if [ $? -ne 0 ]; then
    echo "Failed to update locals inventory!"
    exit 1
fi

# Create locals files to all providers
touch ./terraform/aws/locals.tf

# Replace all locals
for file in $(ls ./terraform/**/locals.tf); do
    echo "$network_locals" >$file
done

echo "Successfully updated locals!"
