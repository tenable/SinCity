import boto3
import os
from aws.lib.InventoryItem import InventoryItem
from ansible.inventory_manager import save_inventories

# This script will generate the 'inventory' files required for ansible to work by pulling all of the instances
# from the AWS infrastructure that have the label 'sincity_lab' within the project


def fetch_inventory_items(regions: list[str]) -> list[InventoryItem]:
    """
    Returns all of the ec2 instances formatted as an inventory item.
    """

    inventory_items: list[InventoryItem] = []

    try:
        for region in regions:
            print(f'Fetching ec2 instances for region {region}...')
            ec2 = boto3.resource('ec2', region_name=region)

            for instance in ec2.instances.all():
                inventory_items.append(InventoryItem(instance))

        print("Fetched all ec2 instances")
        return inventory_items
    except Exception as e:
        print(f'Failed to fetch ec2 instances, check boto3 documentation and make sure you have AWS CLI installed and configured')
        raise e


def generate_simple_inventory_files(root_dir: str, inventory_items: list[InventoryItem]) -> str:
    inventories = {"linux": {}, "windows": {}}

    for item in inventory_items:
        if item.project == 'sincity_lab' and item.instance_ip != None:
            inventory_dict = inventories[item.operating_system]
            inventory_dict.setdefault('all', [])
            inventory_dict['all'] += [item.inventory_entry]

            # Also creates a 'role' group, for example:
            # [dc]
            # 10.20.30.40
            # 50.60.70.80

            key_name = f'{item.application_role}_servers'
            role_dict = inventory_dict.setdefault(key_name, [])
            role_dict += [item.inventory_entry]

    save_inventories(root_dir, inventories)


def update_inventory_files(root_dir: str, regions: list[str]):
    generate_simple_inventory_files(root_dir, fetch_inventory_items(regions))


if __name__ == '__main__':
    # Setup all of the regions we want to grab the instances from
    regions = ['us-east-1']

    # Update the inventory with new files
    # update_inventory(fetch_inventory_items(regions))
    update_inventory_files(os.path.join(os.getcwd(), '../../../'), regions)
