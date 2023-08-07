import os
import re
import json
import pathlib
from jinja2 import Environment, FileSystemLoader, select_autoescape
from builder.provider_templating import to_aws_policy
from misc.text_utils import remove_extra_spaces


def get_jinja_env(templates_dir: str) -> None:
    """
    Returns the env object required for Jinja2 to generate templates.
    """
    env = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=select_autoescape()
    )

    env.filters['to_terraform_json'] = to_terraform_json
    env.filters['to_ldap_path'] = to_ldap_path
    env.filters['get_object_by_path'] = get_nested_object
    env.filters['to_aws_policy'] = to_aws_policy
    env.filters['to_terraform_array'] = to_terraform_array

    return env


def apply_templates(templates_dir: str, target_dir: str,
                    variables: dict, target_files_suffix: str = '') -> None:
    """
    Applies the templates from the provided templates dir, and writes them out
    in the same hierarchy to the target path.
    """

    env = get_jinja_env(templates_dir)

    # The starting path is empty because this is the root directory
    apply_templates_for_dir('', templates_dir, target_dir,
                            env, variables, target_files_suffix)


def apply_templates_for_dir(starting_path: str, dir: str,
                            target_dir: str, env: Environment,
                            variables: dict,
                            target_files_suffix: str = '') -> None:
    """
    Applies the templates for the provided directory. The starting_path
    indicates the path relative to where the templating sourced from,
    this allows us to write it back to the exact same location.
    """

    for file_name in os.listdir(dir):
        file_path = os.path.join(dir, file_name)

        # If the target is a directory
        if os.path.isdir(file_path):
            apply_templates_for_dir(
                os.path.join(starting_path, file_name), file_path,
                target_dir, env, variables,
                target_files_suffix)
        else:
            # Generate the target directory
            target_dir = os.path.join(target_dir, starting_path)

            # Now build the target file path
            file_info = pathlib.Path(file_name)
            file_name_no_ext = file_info.stem
            file_ext = file_info.suffix

            # Build the target file name
            target_file = os.path.join(
                target_dir, f'{file_name_no_ext}{target_files_suffix}{file_ext}')

            # Now apply the template
            apply_template(env, file_path,
                           target_file, variables)


def apply_template(env: Environment, file_path: str, target_file_path: str,
                   variables: dict):
    """
    Applies rendering to the provided file template and writes it back to
    the target file path.
    """

    text = None

    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Generate the rendered template
    rendered_template = get_rendered_template(
        text, variables, env, file_path=file_path)

    # Create the directories if not exists
    os.makedirs(os.path.dirname(target_file_path), exist_ok=True)

    # Now write the template back to the target path
    with open(target_file_path, 'w', encoding='utf-8') as f:
        f.write(rendered_template)


def get_rendered_template(text: str, variables: dict,
                          env: Environment = None, **kwargs) -> str:
    """
    Renders the provided template text using Jinja2.
    """

    try:
        template = env.from_string(text)
        rendered_template = template.render(**variables)

        return remove_extra_spaces(rendered_template)
    except Exception as ex:
        # Get the file path if exists
        file_path = kwargs.get('file_path')

        if file_path:
            raise Exception(
                f'Failed to render template for file "{file_path}"! error: {ex}')

        raise ex


def to_terraform_json(value: dict, indent=2, remove_brackets: bool = False):
    """
    Converts the provided value into a terraform style JSON format. Used within
    the Jinja templates.
    """

    output = json.dumps(value, indent=indent)

    # Remove columns generated with JSON
    def repl(match: re.Match):
        value = match.group(1)
        return f'{value}'

    output = re.sub(r'(\}|\]|(\: ".+")|\d+),', repl, output)

    # Replace key with quotes to terraform style
    def repl(match: re.Match):
        value = match.group(1)
        return f'{value} = '

    output = re.sub(r'"((\w|\-)+)":', repl, output)

    if remove_brackets:
        output = output[2:]
        output = output[:-2]
        output = output.strip()

    return output


def to_ldap_path(value: str) -> str:
    return ''.join([f'DC={x},' for x in value.split('.')])[:-1]


def to_terraform_array(value: list[str],
                       prefix: str, suffix: str,
                       add_quotes=False) \
        -> list[str]:
    """
    This filter receives a terraform array (e.g an array of policy names),
    and appends a prefix and a suffix.

    For example, we have policies: ['access_s3', 'deny_public']
    we can receive: ['aws_resource_policy.access_s3.name',
                    'aws_resource_policy.deny_public.name']
    """

    output = json.dumps(
        [f'{prefix}{"." if prefix else ""}{x}{"." if suffix else ""}{suffix}'
            for x in value])

    if not add_quotes:
        return output.replace('"', '')

    return output


def get_nested_object(obj: dict, path: str) -> any:
    try:
        parts = path.split('.')
        for part in parts:
            if '[' in part:
                key, index = part.split('[')
                index = int(index.strip(']'))
                obj = obj[key][index]
            else:
                obj = obj[part]
        return obj
    except (KeyError, TypeError, IndexError):
        return None


# if __name__ == '__main__':
#     apply_templates(get_templates_dir(), get_root_dir(),
#                     {"region": 'test'})
