import logging
from mergedeep import Strategy
from common import write_network_json, find_root_dir, \
    get_network_file_path
import os
from config import SinCityConfig
from misc.io_utils import find_file_with_pattern, JSON_YAML_FIND_PATTERN
from builder.variables import get_assets_variables_or_empty
from builder.scenarios import append_scenarios
from builder.utils import get_network_template_dict_and_update_variables, \
    merge_network_dicts


def build_network_json(scenarios: list[str], topologies: list[str],
                       cfg: SinCityConfig,
                       strategy: Strategy = Strategy.ADDITIVE,
                       root_dir: str = None) -> None:
    """
    Builds a new 'network.json' file that is a merge of all of the techniques provided.
    If 'fresh' is set to true, the correct 'network.json' wil be overwritten.
    """

    if not root_dir:
        root_dir = os.getcwd()

    root_dir = find_root_dir()
    scenarios_dir = os.path.join(root_dir, 'scenarios')
    topologies_dir = os.path.join(root_dir, 'topologies')

    # A list of all dictionaries (scenarios and topologies) to be merged later on
    network_dicts: list[dict] = []

    # FIXME: Should be a generic function instead for the general templates and the network.json
    # Set all of the variables to be used later on with the template
    variables = {'assets': get_assets_variables_or_empty(
        root_dir), 'config': cfg}

    # If we are not laying under existing topologies, append to the existing 'network.json'
    if not topologies:
        network_file = get_network_file_path(root_dir)
        network_dict = get_network_template_dict_and_update_variables(
            network_file, variables)
        network_dicts.append(network_dict)
    else:
        append_topologies(topologies, topologies_dir, network_dicts, variables)

    # If scenarios were provided, apply all of the scenarios
    if scenarios:
        append_scenarios(scenarios, scenarios_dir, network_dicts, variables)

    # Now create the new network dict
    new_network_json = merge_network_dicts(network_dicts, strategy)

    # Append required network.json data
    append_network_required_data(new_network_json)

    # Add the 'network' key
    if 'network' not in new_network_json:
        new_network_json = {'network': new_network_json}

    # Now write the new 'network.json' file
    write_network_json(new_network_json, root_dir)


def append_topologies(topologies: list[str], topologies_dir: str,
                      network_dicts: list[dict], variables: dict,
                      append_index: int = -1):
    based_on_topologies: list[str] = []

    # Go through each topology under the topologies and add
    for topology in topologies:
        # The topology file path
        topology_file = find_file_with_pattern(
            topologies_dir, topology + JSON_YAML_FIND_PATTERN)

        if not topology_file:
            logging.error(f'The topology {topology} was not found!')
            exit(1)

        # Get the scenario dictionary and update the variables from the extracted scenario
        template_dict = get_network_template_dict_and_update_variables(
            topology_file, variables)

        # If this topology is based on another topology
        if 'based_on' in template_dict:
            # Go through each topology this topology is based on
            for based_on_topology in template_dict['based_on']:
                # If it does not already exists in the existing topologies
                if based_on_topology not in topologies:
                    # Add the based on topologies
                    based_on_topologies.append(based_on_topology)

            # Now remove the based_on key
            del template_dict['based_on']

        # Now append the technique to the list of dictionaries
        network_dicts.append(template_dict) if append_index == - 1 \
            else network_dicts.insert(append_index, template_dict)

    # Now after we finished appending all dictionaries, let's append the based on topologies as well
    # Append the topologies to the beginning of the network_dicts as they act as the base
    if len(based_on_topologies) > 0:
        append_topologies(based_on_topologies, topologies_dir,
                          network_dicts, variables, 0)


def append_network_required_data(network: dict) -> dict:
    """
    Appends additional data missing in the 'network.json'.
    """

    if 'hosts' in network:
        for key, value in network['hosts'].items():
            # If name is not provided
            if 'name' not in value:
                # Generate the name from the key
                value['name'] = key

            if 'subnet' not in value and 'domain' not in value:
                logging.error(
                    'The host %s does not have a subnet or domain', key)

    if 'dcs_map' in network:
        dcs_map = network['dcs_map']

        # Add DC under each domain
        for dc_name in dcs_map:
            domain_name = dcs_map[dc_name]

            # If this DC does not exist under the hosts
            if dc_name not in network['hosts']:
                logging.error(f'DC {dc_name} does not exist under the host!')
                exit(3)

            # Get the IP address of the DC server
            dc_ip = network['hosts'][dc_name]['ip']

            # Get the domain object
            domain_object = network['domains'][domain_name]

            # Append the DC data to this domain
            domain_object['dc'] = {
                "name": dc_name,
                "ip": dc_ip
            }

    return network
