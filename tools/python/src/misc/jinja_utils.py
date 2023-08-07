def extract_variables_from_obj(obj: dict,
                               variables: dict = {},
                               key: str = None) -> dict:
    """
    Extracts all of the variables from an object containing the key 'variable', this will be done recursive.
    """

    if type(obj) is dict:
        output = {**obj}

        # If a key is provided, use it
        if key is not None:
            output['key'] = key

        if 'variable' in obj:
            variables[obj['variable']] = output

        # Add variable groups
        if 'variable_group' in obj:
            group_name = obj['variable_group']
            variable_groups = variables.get('groups', {})
            variable_group = variable_groups.get(group_name, [])
            variable_group += [output]
            variable_groups[group_name] = variable_group
            variables['groups'] = variable_groups

        for key in obj:
            extract_variables_from_obj(obj[key], variables, key)

    return variables
