from builder.network_json import merge_network_dicts
from builder.utils import remove_duplicated_list_items


def test_merge_network_dicts():
    dict_a = {'hosts': {
        "dc01": {
            "name": "dc01"
        },
        "ws01": {
            "ip": "10.0.100.30",
            'win_services': {
                'teleport': {
                    'name': 'teleport'
                }
            }
        },
        'web01': {
            "name": "web01",
        }
    }}

    dict_b = {'hosts': {
        "dc01": {
            "name": "dc01",
            "ip": "10.0.100.11"
        },
        "ws01": {
            "name": "ws01",
            "ip": "10.0.100.35",
            'win_services': {
                'teleport': {'name': 'teleport', 'description': 'itzik is nice'}
            }
        },
        'web01': {
            "name": "web01",
        }
    }}

    merged_dicts = merge_network_dicts([dict_a, dict_b])

    assert (merged_dicts == {'hosts': {
        "dc01": {
            "name": "dc01",
            "ip": "10.0.100.11"
        },
        "ws01": {
            "name": "ws01",
            "ip": "10.0.100.35",
            'win_services': {
                'teleport': {'name': 'teleport', 'description': 'itzik is nice'}
            }
        },
        'web01': {
            "name": "web01",
        }
    }})


def test_remove_duplicated_list_items():
    obj = {'objA': {'a': ['a', 'b', 'a', 'd']},
           'objB': ['h', 'h', 'z', 'h', '0']}

    remove_duplicated_list_items(obj)

    assert obj == {'objA': {'a': ['a', 'b', 'd']},
                   'objB': ['h', 'z',  '0']}


def test_remove_duplicated_list_items_case_b():
    obj = ['Griffindor',
           'Remote Desktop Users', 'Remote Desktop Users']

    remove_duplicated_list_items(obj)

    assert obj == ['Griffindor', 'Remote Desktop Users']
