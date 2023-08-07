import os
import logging
from builder.templating import get_rendered_template, get_jinja_env
from misc.jinja_utils import extract_variables_from_obj
from misc.dict_loader import get_dict_from_file
from mergedeep import Strategy, merge


def get_network_template_dict_and_update_variables(file_path: str,
                                                   variables: dict) -> dict:
    """
    Parses a network template dictionary and update it's variables from the ones
    obtained from the template.
    """

    if not os.path.exists(file_path):
        logging.error(f'The scenario {file_path} was not found!')
        exit(11)

    template_dict = {}

    def apply_templating(text: str, file_path: str) -> str:
        # Apply rendering on the technique
        text = get_rendered_template(
            text, variables, get_jinja_env(file_path),
            file_path=file_path)

        return text

    template_dict = get_dict_from_file(file_path, apply_templating)
    extract_variables_from_obj(template_dict, variables)

    # If the network is presented in the scenario provided, simply extract the contents from it
    if 'network' in template_dict:
        template_dict = template_dict['network']

    return template_dict


def merge_network_dicts(dicts: list[dict], strategy: Strategy = Strategy.ADDITIVE) -> dict:
    """
    Merges multiple 'network.json' dictionaries into one dictionary file and returns it.
    """

    output = merge({}, *dicts, strategy=strategy)

    # Remove any duplicated array items
    remove_duplicated_list_items(output)

    return output


def remove_duplicated_list_items(obj) -> None:
    if type(obj) == list:
        found_strs = {}
        found_objects = []

        for entry in obj:
            if type(entry) == str:
                # If this entry does not exist in the strings that we found
                if not entry in found_strs:
                    # Add it to the dictionary
                    found_strs[entry] = True
                    found_objects.append(entry)
            else:
                found_objects.append(entry)
                remove_duplicated_list_items(entry)

        # Now clear all of the existing array
        obj.clear()

        # Add only objects we found once
        for entry in found_objects:
            obj.append(entry)

    elif type(obj) == dict:
        # Remove all duplicated list items in this object
        for key in obj:
            remove_duplicated_list_items(obj[key])
