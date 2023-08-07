import logging

# This script allows us to merge multiple 'network.json' files into one JSON file,
# this allows us to create multiple attack techniques.


# def validate_network_dict(dict: dict) -> str:
#     """
#     Validates the provided 'network.json' dictionary.
#     If 'final_dict' is set to true, provides full validations, if not,
#     only verifies minimal requirements for 'network.json' dict.
#     """

#     rules = {'keypair': ['name', 'public_key'], 'hosts': {
#         'type': 'key-value', 'structure': ['name', 'ip', 'type', 'role', '+domain', '+users', '+files', {'+win_services': ['binpath']}]}}

#     return validate_props(dict, rules)


# def validate_props(obj: dict, rules) -> str:
#     # If it's an array, validate that all required props exist
#     if type(rules) is list:
#         for key in rules:
#             # If it's not an optional key
#             if not key.startswith('+'):
#                 # Verify that this object exists
#                 if not key in obj:
#                     return f'The key {key} is missing!'

#     # If it's a dictionary
#     elif type(rules) is dict:
#         for key in rules:
#             is_optional = key.startswith('+')
#             real_key = key[1:] if is_optional else key

#             if not real_key in obj and not is_optional:
#                 return f'The key {key} is missing!'

#             # Get the value for this object
#             value = obj[real_key]

#             # Get the rule associated with it
#             rule = rules[key]

#             error: str = None

#             if type(rule) is dict:
#                 if 'type' in rule and 'structure' in rule:
#                     if not type(value) is dict:
#                         error = f'Object {value} is not a dictionary!'
#                     else:
#                         for inner_key in value:
#                             error = validate_props(
#                                 value[inner_key], rule['structure'])

#                             # If we found an error, return it
#                             if error:
#                                 return error
#                 else:
#                     error = validate_props(value, rule)

#                 # If it's a complicated rule, validate that the value following it
#                 if type(rule) is list:
#                     # Get the error if any
#                     error = validate_props(value, rule)

#                 if error:
#                     return error

#     else:
#         return 'This type of object is invalid'


# def validate_rules(rules, obj, key: str) -> str:
#     is_optional = key.startswith('+')
#     real_key = key[1:] if is_optional else key
#     rule = rules[key] if rules is list else rules

#     if type(rule) == str and real_key in obj:
#         return
#     elif type(rule) == dict:
#         for rule_key in rule:
#             sub_rule = rule[rule_key]
#             error = validate_rules(sub_rule, obj[real_key], rule_key)

#             if error:
#                 return error
#     elif type(rule) == list:
#         for item in rule:
#             error = validate_rules(item, obj, item)

#             if error:
#                 return error
