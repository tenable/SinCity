from common import find_root_dir
from misc.io_utils import get_files_with_pattern
from misc.dict_loader import get_dict_from_file
import os
from pathlib import Path
import yaml
import csv
import json
import io


def prettify_file_name(file_name):
    # Split the file name at each underscore and capitalize each word
    prettified_name = " ".join(word.capitalize()
                               for word in file_name.split("_"))
    return prettified_name


def get_supported_techniques_dict() -> dict[str, list[str]]:
    root_dir = find_root_dir()
    scenarios_dir = os.path.join(root_dir, 'scenarios')

    # Get the absolute path of scenarios directory
    scenarios_abs_dir = os.path.abspath(scenarios_dir)

    # Create the dictionary
    dict = {}

    # Get all JSON scenarios
    for file_path in get_files_with_pattern(os.path.join(scenarios_abs_dir, '**/*.{json,yaml,yml}')):
        # Get only the scenario path part
        scenario_path = file_path.replace(scenarios_abs_dir, '')[1:]
        path_info = Path(scenario_path)
        key = prettify_file_name(path_info.stem)

        # Create an empty tags array
        tags = []

        # Now read the files and add the tags as well
        scenario_dict = get_dict_from_file(file_path)

        if 'network' in scenario_dict:
            scenario_dict = scenario_dict['network']

        # If tags are presented in this scenario, add them
        if 'tags' in scenario_dict:
            tags += scenario_dict['tags']

        dict[key] = tags

    return dict


def print_supported_techniques(format: str = 'csv'):
    # Get the techniques dictionary
    techniques = get_supported_techniques_dict()

    if format == 'yaml':
        print(yaml.dump(techniques))
    elif format == 'json':
        print(json.dumps(techniques, indent=4))
    elif format == 'csv':
        # Convert the data to a list of dictionaries
        rows = []
        for technique, tags in techniques.items():
            tags = ", ".join(tags) if tags else ""
            rows.append([technique, tags])

        csv_output = io.StringIO()
        writer = csv.writer(csv_output)
        writer.writerows(rows)
        print(csv_output.getvalue())
