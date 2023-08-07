import logging
from builder.templating import get_rendered_template, get_jinja_env
import os

from misc.io_utils import get_files_with_pattern, find_file_with_pattern, JSON_YAML_FIND_PATTERN
from misc.dict_loader import get_dict_from_file
from pathlib import Path
from common import find_root_dir
from builder.utils import merge_network_dicts

ACTIONS_DIR = os.path.join(find_root_dir(), 'actions')


def get_scenarios_file_map(scenarios_dir: str) -> dict[str, str]:
    """
    Returns all of the scenarios by using the key as either the scenario name or it's tag,
    and value represents the scenario file path without suffix (for example: cloud/full_iam_user).
    """

    scenarios_file_map = {}

    # Get the absolute path of scenarios directory
    scenarios_abs_dir = os.path.abspath(scenarios_dir)

    # Get all JSON scenarios
    for file_path in get_files_with_pattern(os.path.join(scenarios_abs_dir, '**/*.{json,yaml,yml}')):
        # Get only the scenario path part
        scenario_path = file_path.replace(scenarios_abs_dir, '')[1:]
        path_info = Path(scenario_path)
        scenario_path_no_suffix = scenario_path[:-len(path_info.suffix)]
        scenario_file_name = path_info.stem

        # Add this scenario as a tag
        tags = [scenario_path_no_suffix]

        if scenario_file_name != scenario_path_no_suffix:
            tags += [scenario_file_name]

        # Now read the files and add the tags as well
        scenario_dict = get_dict_from_file(file_path)

        if 'network' in scenario_dict:
            scenario_dict = scenario_dict['network']

        # If tags are presented in this scenario, add them
        if 'tags' in scenario_dict:
            tags += scenario_dict['tags']

        # Now create keys for all of the tags and their values
        for tag in tags:
            # Now add this tag as a key and the value add the file name
            scenarios_file_map[tag] = scenario_path

    return scenarios_file_map


def append_scenarios(scenarios: list[str], scenarios_dir: str,
                     network_dicts: list[dict], variables: dict):
    # If 'all' techniques were provided
    if len(scenarios) == 1 and scenarios[0] == 'all':
        # Empty the scenarios array and add all of the techniques found
        scenarios = []

        # Get the absolute path of scenarios directory
        scenarios_abs_dir = os.path.abspath(scenarios_dir)

        # Get all of the scenarios dictionaries
        for file_path in get_files_with_pattern(os.path.join(scenarios_abs_dir, '**/*.{json,yaml,yml}')):
            # Get only the scenario path part
            scenario_path = file_path.replace(scenarios_abs_dir, '')[1:]

            # Now append this scenario
            scenarios.append(scenario_path)
    else:
        # Get a dictionary with all of the scenarios names and tags as key and their appropriate value as value
        scenarios_file_map = get_scenarios_file_map(scenarios_dir)
        scenarios_file_names = []

        # Go through each map
        for technique in scenarios:
            # If this technique exists in our map
            if technique in scenarios_file_map:
                # Use the actual file name of the scenario
                scenarios_file_names.append(scenarios_file_map[technique])
            else:
                logging.error(
                    f'The {technique} scenario was not found under the scenarios directory!')
                exit(1)

        # Now change the scenarios to the updated file names
        scenarios = scenarios_file_names

    # Go through each technique in the provided scenarios
    for technique in scenarios:
        # The technique file path
        technique_file = os.path.join(scenarios_dir, f'{technique}')

        if not os.path.exists(technique_file):
            logging.error(f'The scenario {technique_file} was not found!')
            exit(11)

        technique_dict = {}

        def apply_templating_to_text(text: str, file_path: str):
            # Apply rendering on the technique
            text = get_rendered_template(
                text, variables, get_jinja_env(technique_file),
                file_path=file_path)

            return text

        technique_dict = get_dict_from_file(
            technique_file, apply_templating_to_text)

        if 'tags' in technique_dict:
            del technique_dict['tags']

        # Apply actions for this scenario
        technique_dict = apply_actions_for_scenario(
            technique_file, technique_dict, variables)

        # Now append the technique to the list of dictionaries
        network_dicts.append(technique_dict)


def apply_actions_for_scenario(scenario_file: str, scenario_dict: dict[str, any], variables: dict) -> dict[str, any]:
    """
    Applies any actions if provided by the scenarios, if not,
    return the scenario as is.
    """

    action_dicts = []

    # If actions are used in this scenario
    if 'use_actions' in scenario_dict:
        actions = scenario_dict['use_actions']

        for action in actions:
            action_file = find_file_with_pattern(
                ACTIONS_DIR, f'{action}{JSON_YAML_FIND_PATTERN}')

            # If the action file was not found
            if not action_file:
                logging.error(
                    f'Failed to find action {action}, used by the scenario {scenario_file}!')
                exit(1)

            def apply_templating_to_text(text: str, file_path: str):
                # Apply rendering on the technique
                text = get_rendered_template(
                    text, variables, get_jinja_env(action_file),
                    file_path=file_path)

                return text

            action_dict = get_dict_from_file(
                action_file, apply_templating_to_text)

            # Add this action dictionary to the list of dictionaries
            action_dicts += [action_dict]

        # Remove the 'use_actions' for this scenario
        del scenario_dict['use_actions']

        # Add this scenario as the last one to allow it to override other fields
        action_dicts += [scenario_dict]

        return merge_network_dicts(action_dicts)

    return scenario_dict
