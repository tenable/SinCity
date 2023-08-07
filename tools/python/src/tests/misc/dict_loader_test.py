import os
from misc.dict_loader import get_dict_from_file, get_dicts_from_folder, get_merged_dict_from_folder


def test_get_merged_dicts_from_folder():
    dir = os.path.join(os.path.dirname(__file__),
                       "../static/dicts_from_folder")
    dict = get_merged_dict_from_folder(dir)

    assert dict == {'some_vars': {'name': 'Jack'},
                    'full_name': 'Jack Rosenfeld', 'some_property': {'a': 'hello world'}}


def test_get_dicts_from_folder():
    dir = os.path.join(os.path.dirname(__file__),
                       "../static/dicts_from_folder")
    dicts = get_dicts_from_folder(dir)

    assert dicts == {"json_vars.json": {"full_name": "{{ some_vars.name }} Rosenfeld", "some_property": {
        "a": "hello world"}}, "__pre_vars.yml": {"some_vars": {"name": "Jack"}}}


def test_get_dict_from_file_json_format():
    json_path = os.path.join(os.path.dirname(__file__), "../static/dummy.json")
    dict = get_dict_from_file(json_path)

    assert dict == {"hosts": {"{{ main_workstation.key }}": {"groups": {
        "Remote Management Users": {"members": ["{{ main_user.key }}"]}}}}, "tags": ["T1021.006"]}


def test_get_dict_from_file_yaml_format():
    yaml_path = os.path.join(os.path.dirname(__file__), "../static/dummy.yaml")
    dict = get_dict_from_file(yaml_path)

    assert dict == {"hosts": {"{{ main_workstation.key }}": {"groups": {
        "Remote Management Users": {"members": ["{{ main_user.key }}"]}}}}, "tags": ["T1021.006"]}
