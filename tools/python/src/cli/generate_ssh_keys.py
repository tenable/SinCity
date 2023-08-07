from common import run_command
from typing import TypedDict
from common import find_root_dir, get_file_contents, write_file_contents
from os import path
import os
import yaml
import logging


class SSHKeys(TypedDict):
    private_key: str
    public_key: str


def _create_key_files() -> SSHKeys:
    key_files_path = path.join(
        find_root_dir(), 'ansible', 'linux', 'server_keys')

    private_key_path = path.join(key_files_path, 'sincity')
    public_key_path = private_key_path + '.pub'

    # If the SSH directory does not exist, create it
    if not path.exists(key_files_path):
        os.mkdir(key_files_path)
    else:
        # First let's delete the existing keys, if we have any
        if path.exists(private_key_path):
            os.remove(private_key_path)

        if path.exists(public_key_path):
            os.remove(public_key_path)

    # Generate the ssh keys using the 'ssh-keygen' command
    exit_code = run_command(
        f'ssh-keygen -f {private_key_path} -P "" -C "sincity_lab_key"')

    # Verify the command went successfully
    if exit_code == 0:
        logging.info('Successfully generated new SSH keys!')

        # Now read the SSH keys generated
        private_key = get_file_contents(path.join(private_key_path))
        public_key = get_file_contents(path.join(public_key_path))

        # Return the generated keys
        return {'private_key': private_key, 'public_key': public_key}

    else:
        logging.error(
            'Failed to generate SSH keys! got exit code %d', exit_code)


def generate_ssh_keys(skip_confirmation: bool = False) -> None:
    if not skip_confirmation:
        user_input = input(
            'Are you sure you want to generate a new SSH key? this will overwrite existing ones and any servers you currently have will not be accessible! (y/N)')

        # Don't continue if the user didn't confirm
        if not (user_input.lower() == 'yes' or user_input.lower() == 'y'):
            return

    # First create the key files
    key_files = _create_key_files()

    # If no key files returned, don't do anything
    if not key_files:
        return

    # Now update the assets with the new public key
    public_key = key_files['public_key']

    # Read the pre-assets file and replace the public ssh key in it
    root_dir = find_root_dir()
    pre_assets_path = path.join(root_dir, 'assets', '__pre_assets.yml')

    if not path.exists(pre_assets_path):
        logging.error(
            'Assets are missing the __pre_assets,yml file! failed to overwrite public key!')

    else:
        pre_asset_file = get_file_contents(pre_assets_path)
        assets_dict: dict[str, any] = yaml.safe_load(pre_asset_file)

        if 'variables' in assets_dict and 'keypair' in assets_dict['variables']:
            assets_dict['variables']['keypair']['public_key'] = public_key
            # Now dump the YAML back so we can save it
            dumped_yaml = yaml.dump(assets_dict)

            # Write the dump
            write_file_contents(pre_assets_path, dumped_yaml)
            logging.info('Successfully created new ssh key!')

        else:
            logging.error('Failed to find public SSH key in %s',
                          pre_assets_path)
