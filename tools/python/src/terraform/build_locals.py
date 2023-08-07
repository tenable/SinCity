# This script builds the locals.tf output string from the 'network.json' for Terraform, so it would be easier to deploy
# our infrastructure using a simple JSON file.
# Run the './tools/build_local.sh' to actually generate the JSON files.
# THIS SCRIPT WILL ONLY OUTPUT THE 'local.tf' JSON string to stdout

import json

from common import get_network_dict
network = get_network_dict()

# The final output to be written in the locals.tf file
output = ""


def save_into_variable(name: str, value):
    global output
    if type(value) is dict:
        output += f"{name} = {json.dumps(value, indent=4, sort_keys=True)}"
    elif type(value) is list:
        output += f"{name} = {json.dumps(value, indent=4, sort_keys=True)}"
    else:
        output += f"{name} = {value}"

    output += "\n"


def generate_subnet_variables(subnets: dict, hosts: dict):
    # Save the subnets variable as is
    save_into_variable("subnets", subnets)

    # The servers output
    hosts_list = []
    # Generates an array of all subnets
    subnets_list = []

    subnet_index = 0
    # Now also generate the server variables
    for key in subnets:
        # Go through all of the hosts and find only hosts within this subnet
        for host_name in hosts:
            host = hosts[host_name]

            found_subnet = host['domain'].split(
                '.')[0] if 'domain' in host else host['subnet']

            if found_subnet == key:
                hosts_list += [{
                    **host,
                    "subnet_index": subnet_index,
                    "subnet_name": found_subnet
                }]

        subnets_list += [{"name": key, **subnets[key]}]
        subnet_index += 1

    save_into_variable("subnets_list", subnets_list)
    save_into_variable("hosts_list", hosts_list)


for key in network:
    if key == 'subnets':
        generate_subnet_variables(network.get(
            'subnets', {}), network.get('hosts', {}))
    else:
        save_into_variable(key, network[key])


output = "locals {\n" + output + "}"
print(output)
