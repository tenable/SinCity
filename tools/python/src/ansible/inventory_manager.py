# Contains the 'all' vars section for each platform (if exists)
import os
INVENTORY_ALL_VARS = {"windows": """
ansible_user=root
ansible_password=Aa123456!
password=Aa123456!
ansible_connection=winrm
ansible_winrm_server_cert_validation=ignore
ansible_winrm_operation_timeout_sec=400
ansible_winrm_read_timeout_sec=500
enable_http_proxy=no
"""}


def save_inventories(root_dir: str, inventories: dict):
    """
    Save all of the inventories into their respective files.
    """

    for inventory_platform in inventories:
        output = ""

        for key in inventories[inventory_platform]:
            inventory_dict = inventories[inventory_platform]

            # Add another line if it is not the first
            if not key == 'all':
                output += '\n'

            output += f'[{key}]\n'

            for entry in inventory_dict[key]:
                output += entry + '\n'

            if key == 'all':
                if inventory_platform in INVENTORY_ALL_VARS:
                    all_vars = INVENTORY_ALL_VARS[inventory_platform]
                    output += f'\n[all:vars]{all_vars}'

        file_path = os.path.join(
            root_dir, 'ansible', inventory_platform, 'inventory')
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(output)
