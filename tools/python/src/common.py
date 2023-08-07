import json
import os
import subprocess
import logging
import sys
import shutil
from shutil import which

# A list of all supported providers
SUPPORTED_PROVIDERS = ('aws', 'azure')

# A list of all required deps
REQUIRED_DEPS = {
    'terraform': 'v1.2.5',
    'ansible': 'v2.11.12'
}

# The directory where all backups are stored
BACKUPS_DIR = 'backups'


def get_dependencies_with_versions() -> str:
    """
    Returns a string with all of the dependencies and their versions.
    """
    output = ''

    for dep_name in REQUIRED_DEPS:
        output += f'{dep_name} - {REQUIRED_DEPS[dep_name]}\n'

    return output


def check_requirements(verbose: bool = False) -> bool:
    """
    Checks if the running system has the required dependencies.
    """
    for dep_name in REQUIRED_DEPS:
        version = REQUIRED_DEPS[dep_name]

        if not which(dep_name):
            logging.error(
                f'The dependency {dep_name}, version {version} is missing')

            exit(1)

    if verbose:
        logging.info(
            f'All dependencies exist, to make sure sincity is fully functional, make sure they have the following versions:\n{get_dependencies_with_versions()}')


def find_path_with_backtrack(path_name: str, root_dir: str = None, max_back: int = 4) -> str:
    """
    Returns correct path for the provided path_name (can be either directory name or file name).
    If not found, will step back to the previous directory until the 'max_back' is reached.
    """

    found_path = None

    for i in range(0, max_back):
        back = '../' * i
        found_path = os.path.join(root_dir, back, path_name)

        if not os.path.exists(found_path):
            if i == max_back:
                logging.error(f'The path {path_name} does not exist!')
                exit(1)
        # If we found the 'network.json' file
        else:
            return found_path


def get_network_file_path(root_dir: str = None) -> str:
    """
    Returns the 'network.json' file in the directory. If not found, will step back to the previous directory until the 'max_back' is reached.
    """

    if not root_dir:
        root_dir = find_root_dir(root_dir)

    return os.path.join(root_dir, 'network.json')


def get_network_dict(root_dir: str = None) -> dict:
    """
    Return the dictionary from the json file called `network.json`.
    """
    if not root_dir:
        root_dir = find_root_dir()

    # Find 'network.json' file in the hierarchy, if not found, go to the previous directory until the 4th folder
    network_file = get_network_file_path(root_dir)

    # Open the network.json file for read
    network = get_json_dict(network_file, True)

    return network['network'] if 'network' in network else {}


def write_network_json(network: dict, root_dir: str = None, backup: bool = True) -> None:
    if not root_dir:
        root_dir = os.getcwd()

    root_dir = find_root_dir(root_dir)
    network_file = get_network_file_path(root_dir)

    # If we are backing up
    if (backup):
        from datetime import datetime
        timestr = datetime.now().strftime('%d.%m.%y-%H:%M:%S')
        backups_dir = os.path.join(root_dir, BACKUPS_DIR)

        # Create the backups directory if not exists
        os.makedirs(backups_dir, exist_ok=True)

        # Now create the backup path
        backup_path = os.path.join(
            backups_dir, f'network-{timestr}.json')

        # And copy the file if it exists
        if os.path.exists(network_file):
            # Copy the network.json file to the backup
            shutil.copy(network_file, backup_path)

    with open(network_file, 'w', encoding='utf-8') as f:
        json_output = json.dumps(network, indent=4)
        f.write(json_output)


def get_json_dict(path: str, return_empty_if_not_exists=False) -> dict:
    """
    Returns a JSON dictionary object from a file.
    """

    # Return empty dictionary if the file does not exist
    if return_empty_if_not_exists and not os.path.exists(path):
        return {}

    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
        output = json.loads(text)

    return output


def get_file_contents(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def write_file_contents(path: str, contents: any) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(contents)


def is_provider_supported(provider: str) -> bool:
    """
    Returns true if the provider specific is supported.
    """
    return provider in SUPPORTED_PROVIDERS


def run_command(cmd: str, **kwargs) -> int:
    """
    Runs the specified command in a separate process, wait it for it to end and return the error code.
    """

    logging.debug(f"Running command: '{cmd}'")

    # Get the current working directory if exists.
    cwd = kwargs.get('cwd', os.getcwd())

    # Now popup te new process and attach the outputs into stdout and stderror
    with subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr,
                          cwd=cwd, shell=True) as proc:
        returncode = proc.wait()
        return returncode


def get_generic_templates_dir() -> str:
    return os.path.join(find_root_dir(), 'templates')


def get_terraform_provider_templates_dir(provider: str) -> str:
    return os.path.join(get_terraform_provider_dir(f'{provider}_templates'), )


def get_terraform_provider_dir(provider: str) -> str:
    return os.path.join(find_root_dir(), 'terraform', provider)


def get_ansible_dir() -> str:
    return os.path.join(find_root_dir(), 'ansible')


def get_ansible_env_dir(env: str) -> str:
    return os.path.join(get_ansible_dir(), env)


def find_root_dir(base_dir: str = None, max_back: int = 4) -> str:
    """
    Finds sincity root directory by going back directories until finding the '.anchor' file.
    """

    current_dir = os.getcwd() if not base_dir else base_dir

    for i in range(0, max_back):
        back = '../' * i
        found_path = os.path.join(current_dir, back, '.anchor')

        if not os.path.exists(found_path):
            if i == max_back:
                logging.error(
                    f'Couldn\'t find sincity root dir! Please make sure .anchor file was not removed')
                exit(1)
        # If we found the root directory, return it
        else:
            return os.path.join(current_dir, back)
