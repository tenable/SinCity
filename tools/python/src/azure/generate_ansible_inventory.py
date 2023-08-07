from typing import List

from azure.mgmt.compute import ComputeManagementClient
from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient

from ansible.inventory_manager import save_inventories
from azure.inventoryitem import InventoryItem


def fetch_inventory_items(subscription_id: str) -> list[InventoryItem]:
    """
    Returns all of the ec2 instances formatted as an inventory item.
    """
    inventory_list = []
    credential = DefaultAzureCredential()
    compute_client = ComputeManagementClient(credential, subscription_id)
    network_client = NetworkManagementClient(credential, subscription_id)
    # Get all VMs in the subscription
    for vm in compute_client.virtual_machines.list_all():
        if vm.tags and vm.tags.get("Project") == 'sincity_lab':
            network_interface_id = vm.network_profile.network_interfaces[0].id
            network_interface_name = network_interface_id.split('/')[-1]
            resource_group = vm.id.split('/resourceGroups/')[1].split("/")[0]
            network_interfaces = list(
                network_client.network_interface_ip_configurations.list(resource_group, network_interface_name))
            ip = network_client.public_ip_addresses.get(resource_group,
                                                        network_interfaces[0].public_ip_address.id.split("/")[
                                                            -1]).ip_address

            inventory_list.append(InventoryItem(name=vm.name, operating_system=vm.storage_profile.os_disk.os_type,
                                                role=vm.tags.get("Role"), ip=ip))
    return inventory_list


def generate_simple_inventory_files(root_dir: str, inventory_items: list[InventoryItem]) -> str:
    inventories = {"linux": {}, "windows": {}}
    for item in inventory_items:
        inventory_dict = inventories[item.operating_system.lower()]
        inventory_dict.setdefault('all', [])
        inventory_dict['all'] += [f'{item.name}   ansible_host={item.ip}']
        key_name = f'{item.role}_servers'
        role_dict = inventory_dict.setdefault(key_name, [])
        role_dict += [f'{item.name}   ansible_host={item.ip}']

    save_inventories(root_dir, inventories)


def update_inventory_files(root_dir: str, subscription:str):
    generate_simple_inventory_files(root_dir, fetch_inventory_items(subscription))
