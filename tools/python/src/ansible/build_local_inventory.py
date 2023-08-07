# This script builds the inventory file from the 'network.json' so it would be easier to deploy
# our infrastructure using a simple JSON file.
# Pay attention that the IP addresses are only the local addresses
# and not the public ones

from common import get_network_dict, find_root_dir
from ansible.inventory_manager import save_inventories


def generate_local_inventory(root_dir: str = None):
    """
    Generate a local inventory from the 'network.json' file with the local ip addresses.
    """
    inventories = {"linux": {}, "windows": {}}

    if not root_dir:
        root_dir = find_root_dir()

    # Get the network dictionary
    network = get_network_dict(root_dir)

    # Check that the 'network.json' file is correct
    if not 'hosts' in network:
        raise "Hosts are missing from the network file!"

    # Get all of the hosts
    hosts = network['hosts']

    # Go over all of the hosts
    for hostname in hosts:
        host = hosts[hostname]

        # Get the host type so we will be able to pick the correct inventory
        type = host['type']

        # Create the entry to save into the inventory
        row = f'{hostname}   ansible_host={host["ip"]}'

        # Get the correct sections for the inventory we are working with
        sections = inventories[type]

        # Insert the entry to the 'all' section in the inventory
        sections.setdefault('all', [])
        sections['all'] += [row]

        # Add this entry into the sections of this party of the inventory
        section = sections.get(host['role'], [])

        section += [row]
        sections[f"{host['role']}_servers"] = section

    save_inventories(root_dir, inventories)


if __name__ == '__main__':
    generate_local_inventory()
