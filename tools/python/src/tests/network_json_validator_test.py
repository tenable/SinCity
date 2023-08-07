# from cli.network_json_utils import validate_props, validate_rules, validate_network_dict
# from common import get_json_dict
# import os


# def test_validate_rules_simple_array():
#     obj = {'a': {'b': {}, 'c': {}}}
#     rules = {'a': ['b', 'c']}

#     assert validate_rules(rules, obj, 'a') == None


# def test_validate_rules_simple_array_fail():
#     obj = {'a': {'b': {}, }}
#     rules = {'a': ['b', 'c']}

#     assert validate_rules(rules, obj, 'a') == None


# def test_validate_rules_complex():
#     obj = {'a': {'b': {}, 'c': {}, 'd': {}}}
#     rules = {'a': ['b', 'c', {'d': ['x']}]}

#     validate_rules(rules, obj, 'a')


# def test_validate_props_array_success():
#     rules = ['a', 'b', '+c']
#     obj = {'a': 'something', 'b': 'nothing', 'c': 'great'}

#     assert validate_props(obj, rules) == None


# def test_validate_props_array_fail():
#     rules = ['a', 'b', '+c']
#     obj = {'a': 'something'}

#     assert validate_props(obj, rules) == 'The key b is missing!'


# def test_validate_props_struct_fail():
#     rules = {'a': {'type': 'key-value',
#                    'structure': ['ab', 'cd']}, 'b': ['z', 'x']}

#     obj = {
#         'a': {
#             'dc01': {'ab': 'hello', 'ch': 'world'},
#             'dc02': {'ab': 'hello', 'cd': 'world'}
#         },
#         'b': {'z': 'hello', 'x': 'world'}
#     }

#     assert validate_props(obj, rules) == 'The key cd is missing!'


# def test_validate_props_struct_success():
#     rules = {'a': {'type': 'key-value',
#                    'structure': ['ab', 'cd']}, 'b': ['z', 'x']}

#     obj = {
#         'a': {
#             'dc01': {'ab': 'hello', 'cd': 'world'}
#         },
#         'b': {'z': 'hello', 'x': 'world'}
#     }

#     assert validate_props(obj, rules) == None


# def test_validate_props_success():
#     obj = {
#         'hosts': {
#             "dc01": {
#                 "name": "dc01",
#                 "ip": "10.0.100.11",
#                 "type": "windows",
#                 "role": "dc",
#                 "domain": "basin.local"
#             },
#             "web01": {
#                 "name": "web01",
#                 "ip": "10.0.100.31",
#                 "type": "linux",
#                 "role": "linux_web_server",
#                 "subnet": "basin"
#             }
#         },
#     }

#     rules = {'hosts':
#              {
#                  'type': 'key-value',
#                  'structure': ['name', 'ip', 'type', 'role', '+domain', '+subnet']
#              }}

#     assert validate_props(obj, rules) == None


# def test_validate_props_fail():
#     obj = {
#         'hosts': {
#             "dc01": {
#                 "name": "dc01",
#                 "ip": "10.0.100.11",
#                 "type": "windows",
#                 "role": "dc",
#                 "domain": "basin.local"
#             },
#             "web01": {
#                 "name": "web01",
#                 "ip": "10.0.100.31",
#                 "role": "linux_web_server",
#                 "subnet": "basin"
#             }
#         },
#     }

#     rules = {'hosts':
#              {
#                  'type': 'key-value',
#                  'structure': ['name', 'ip', 'type', 'role', '+domain', '+subnet']
#              }}

#     assert validate_props(obj, rules) == 'The key type is missing!'


# def test_validate_props_fail_case_2():
#     obj = {
#         'children': {
#             "itzik": {
#                 "age": 15,
#             },

#             "david": {
#                 "age": 12,
#                 "hobbies": {'play': 'Play at the garden'}
#             }
#         },
#     }

#     rules = {'children':
#              {
#                  'type': 'key-value',
#                  'structure': ['age', {'+hobbies': {'type': 'array'}}]
#              }}

#     assert validate_props(obj, rules) == 'The key type is missing!'


# def test_validate_network_dict_success():
#     valid_file_path = os.path.join(os.path.dirname(
#         os.path.realpath(__file__)), 'static/correct_network.json')

#     obj = get_json_dict(valid_file_path)
#     assert validate_network_dict(obj['network']) == None


# def test_validate_network_dict_fail():
#     valid_file_path = os.path.join(os.path.dirname(
#         os.path.realpath(__file__)), 'static/incorrect_network.json')

#     obj = get_json_dict(valid_file_path)
#     assert validate_network_dict(obj['network']) == 'The key role is missing!'


# def test_merge_network_dicts():
#     pass
