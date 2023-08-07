import os
import logging
import time

from mergedeep import Strategy
from common import find_root_dir, run_command, \
    get_generic_templates_dir, get_terraform_provider_templates_dir, \
    get_terraform_provider_dir, get_network_dict

from builder.templating import apply_templates
from ansible.build_local_inventory import generate_local_inventory
from config import get_sincity_config
from shutil import which
from builder.network_json import build_network_json
from builder.variables import get_assets_variables_or_empty
from config import SinCityConfig
from misc.io_utils import remove_files_with_pattern


def build_infrastructure(arguments: dict):
    logging.info('Building templates and local files...')

    cfg = get_sincity_config(True)
    network = get_network_dict()

    # If the command 'build' was actually typed in, and not called by
    # the apply function
    if 'build' in arguments:
        scenarios_str: str = arguments.get('--scenarios', None)
        topologies_str: str = arguments.get('--topologies', None)
        strategy: Strategy = Strategy.REPLACE if arguments.get(
            '--strategy', 'add') == 'replace' else Strategy.ADDITIVE

        # If techniques were provided, build the network json file
        # with those techniques
        if scenarios_str or topologies_str:
            logging.info(
                'Updating network.json with provided topologies and \
                techniques...')
            scenarios = scenarios_str.split(
                ',') if scenarios_str is not None else None
            topologies = topologies_str.split(
                ',') if topologies_str is not None else None
            build_network_json(scenarios, topologies, cfg,  strategy)

    # Wait up, this fixes the bugs that the templating does not render the last network.json
    time.sleep(0.2)

    # If bash is supported, use the 'build_locals' script as it was
    # meant to be, otherwise just use it as is
    binary = 'sh -c' if which('bash') else 'sh'
    returncode = run_command(f'{binary} ./tools/build_locals.sh',
                             cwd=os.path.join(find_root_dir()))

    if returncode != 0:
        logging.info(
            f'Failed to build terraform locals! exit code: {returncode}')
        exit(1)

    assets_variables = get_assets_variables_or_empty()

    # FIXME: Should be a generic function instead for the general templates
    # and the network.json
    template_variables = {'config': cfg, 'network': {**network},
                          'assets': assets_variables}

    apply_generic_templates(cfg, template_variables)
    apply_provider_templates(cfg, template_variables)

    logging.info('Successfully applied templates!')


def apply_provider_templates(cfg: SinCityConfig, variables: dict):
    provider = cfg['provider']
    terraform_provider_templates_dir = get_terraform_provider_templates_dir(
        provider)
    target_terraform_dir = get_terraform_provider_dir(provider)

    # Delete all templates files before
    delete_templated_files()

    if os.path.exists(terraform_provider_templates_dir):
        logging.info('Applying provider templates...')

        apply_templates(terraform_provider_templates_dir,
                        target_terraform_dir,
                        variables,
                        '_templated')


def apply_generic_templates(cfg: SinCityConfig, variables: dict):
    logging.info('Applying generic templates...')
    generic_templates_dir = get_generic_templates_dir()

    # If the generic templates directory exists, apply the templates
    if os.path.exists(generic_templates_dir):
        apply_templates(generic_templates_dir, find_root_dir(),
                        variables)


def update_ansible_inventory(cfg: dict, is_local: bool = False):
    if is_local:
        generate_local_inventory(find_root_dir())
        return

    # If the provided is AWS, generate the inventory accordingly
    if cfg['provider'] == 'aws':
        logging.info(
            'Fetching servers from AWS api and updating inventory accordingly...')
        from aws.generate_ansible_inventory import update_inventory_files
        regions = [cfg['region']]
        update_inventory_files(find_root_dir(), regions)
    elif cfg['provider'] == 'azure':
        logging.info('Fetching servers from Azure api and updating inventory accordingly...')
        from azure.generate_ansible_inventory import update_inventory_files
        subscription_id = cfg["subscription_id"]
        update_inventory_files(find_root_dir(), subscription_id)


def delete_templated_files():
    """
    Removes all of the files ending with the '_templated.tf' suffix.
    """

    root_dir = find_root_dir()
    files_deleted = remove_files_with_pattern(
        os.path.join(root_dir, './**/*_templated.tf'))
    logging.info(f'Successfully deleted {len(files_deleted)} templates')
