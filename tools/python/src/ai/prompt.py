import yaml
from jinja2 import Template
from typing import TypedDict
import os
import json


class OpenAIMessage(TypedDict):
    role: str
    content: str


class OpenAIPromptFile(TypedDict):
    messages: list[OpenAIMessage]
    config: dict


def parse_prompt_file(file_path: str, context: dict) -> OpenAIPromptFile:
    with open(file_path, 'r', encoding='utf-8') as file:
        yaml_str = file.read()

        template = Template(yaml_str)
        rendered_yaml = template.render(context)

        parsed_data = yaml.safe_load(rendered_yaml)
        return parsed_data


def write_prompt_topology_file(topology: dict, file_path: str):
    """
    Writes a topology file, receives the topology dictionary and a file path
    and write the file. If the file is with '.json' extension, the file will be saved in JSON format,
    otherwise the file will be saved as YAML.
    """

    # Get the file extension
    ext = '.yaml'
    file_path_split = os.path.splitext(file_path)

    # If the we got an extension
    if len(file_path_split) > 1 and file_path_split[1] != '':
        ext = file_path_split[1]
        file_path = file_path_split[0]

    # Determine the format output according to the file extension
    file_contents = yaml.dump(
        topology) if ext == '.yaml' else json.dumps(topology, indent=4)

    with open(file_path + ext, 'w', encoding='utf-8') as f:
        f.write(file_contents)
