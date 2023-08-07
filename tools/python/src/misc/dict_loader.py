import pathlib
import json
import yaml
from misc.io_utils import get_files_with_pattern
from os import path
from builder.templating import get_jinja_env, get_rendered_template
import json
from mergedeep import Strategy, merge


def get_merged_dict_from_folder(dir: str, variables: dict = {}, interceptor=None) -> dict[str]:
    """
    Returns a single merged dictionary with all of the dictionaries merged.
    Jinja2 is acceptable and variables will be populated according to the
    variables obtained or read dynamically while parsing the files.

    Files will be parsed sorted by their file names.
    """

    dicts = get_dicts_from_folder(dir, interceptor)
    env = get_jinja_env(dir)
    output = {**variables}

    # Get the keys sorted by their name
    file_paths = sorted(dicts)

    for file_path in file_paths:
        # Get the dictionary
        dict = dicts[file_path]

        # Convert the dictionary into JSON string
        text = json.dumps(dict)

        # Parse Jinja templates
        text = get_rendered_template(text, output, env,
                                     file_path=file_path)

        # Convert it back into json dict
        dict = json.loads(text)
        output = merge({}, output, dict, strategy=Strategy.ADDITIVE)

    return output


def get_dicts_from_folder(dir: str, interceptor=None) -> dict[dict[str]]:
    """
    Returns a dictionary of dictionaries, which the key contains the file name and the value
    contains the dictionary of variables.
    """

    full_path = path.join(dir, '**/*.{json,yaml,yml}')

    files = get_files_with_pattern(full_path)

    dicts = {}

    for file in files:
        dict = get_dict_from_file(file, interceptor)

        file_path = file.replace(dir, '')

        if file_path.startswith('/'):
            file_path = file_path[1:]

        dicts[file_path] = dict

    return dicts


def get_dict_from_file(file_path: str, interceptor=None) -> dict[str]:
    """
    Returns a dictionary from the provided file path. The file path
    must be either YAML or JSON file.
    """

    path_info = pathlib.Path(file_path)
    suffix = path_info.suffix
    output: dict[str] = {}

    with open(file_path, 'r', encoding='utf-8') as f:
        # Read file string
        text = f.read()

        # If an interceptor was provided, call the interceptor with the text
        text = interceptor(text, file_path) if interceptor else text

        if suffix == '.json':
            output = json.loads(text)
        elif suffix == '.yaml' or suffix == '.yml':
            output = yaml.safe_load(text)

    return output
