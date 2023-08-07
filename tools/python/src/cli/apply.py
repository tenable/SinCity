import logging
from time import sleep
from config import get_sincity_config
from common import run_command, get_ansible_env_dir, get_terraform_provider_dir
from builder.build import update_ansible_inventory, build_infrastructure
from terraform.api import apply_terraform


def apply_sincity(arguments: dict):
    cfg = get_sincity_config()

    if not cfg:
        logging.error(
            'Config not found, please run: "sincity setup <provider>"')
        exit(1)

    # Check which logic should we run or we should run them all
    logic = arguments['--only']
    ansible_tags = arguments['--ansible-tags']

    # If provision or configurations was provided, translate them to terraform or ansible accordingly
    if logic == 'provision':
        logic = 'terraform'
    elif logic == 'configure':
        logic = 'ansible'

    # If terraform was selected and ansible_tags were provided, raise error
    if logic == 'terraform' and ansible_tags:
        logging.error('Cannot apply terraform logic with ansible tags!')
        exit(1)

    build_infrastructure(arguments)

    # If the logic that was provided is 'terraform', or none, apply it
    if not ansible_tags and (not logic or logic == 'terraform'):
        apply_terraform_infrastructure(cfg)

        # If we are not only applying terraform, wait for things to go up and then continue
        if (logic != 'terraform'):
            wait = int(arguments['--wait'])
            logging.info(
                f'Waiting {wait} seconds before we continue...')

            # Now wait a timeout for the servers to go up
            sleep(wait)

        # Now update the inventory for ansible
        update_ansible_inventory(cfg)

    # If the logic that was provided is 'ansible', or none, apply it
    if ansible_tags or not logic or logic == 'ansible':
        apply_ansible_infrastructure(cfg, arguments)

    logging.info(f'SinCity applied successfully!')


def apply_terraform_infrastructure(cfg: dict):
    apply_terraform(get_terraform_provider_dir(cfg['provider']))


def apply_ansible_infrastructure(cfg: dict, arguments: dict):
    # The environments we will provision the servers for
    ansible_envs = ('linux', 'windows')
    selected_envs = arguments['--ansible-env']
    ansible_tags = arguments['--ansible-tags']

    # If not all of the environments were selected, apply only the selected ones
    if selected_envs != 'all':
        ansible_envs = (selected_envs,)

    for env in ansible_envs:
        ansible_env_dir = get_ansible_env_dir(env)

        logging.info(
            f'Applying ansible configurations for environment: {env}...')

        # Get the playbook we want to play
        playbook = arguments.get('--ansible-playbook', 'main.yml')

        # Generate the command
        cmd = f'ansible-playbook {playbook}'

        # If tags were provided, apply them to the command
        if ansible_tags:
            cmd += f' --tags={ansible_tags}'

        # Now apply the ansible infrastructure
        returncode = run_command(
            cmd, cwd=ansible_env_dir)

        if returncode:
            logging.error(
                f'Ansible exited with code {returncode}, apply failed')
            exit(1)

        logging.info(f'Ansible for environment: {env} applied successfully!')

    logging.info('Ansible was applied successfully!')
