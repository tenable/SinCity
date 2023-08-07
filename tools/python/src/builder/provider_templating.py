"""
This file contains Jinja2 filter functions used to apply on specific providers.
For example, it allows rendering policies on AWS correctly.
"""

import json


def to_aws_policy(value: dict) -> dict:
    policy = {
        "Version": "2012-10-17",
        "Statement": []
    }

    # Go through al of the action types
    for action_type in ['allowed_actions', 'disallowed_actions']:
        action_data: dict = value.get(action_type)

        # If this action type does not exist, go on
        if not action_data:
            continue

        for action in action_data:
            statement = {
                "Effect": "Allow"
                if action_type == "allowed_actions"
                else "Deny",

                "Action": action["name"],
                "Resource": action.get("resources"),
                "Principal": action.get("principal")
            }

            # Clear empty keys
            statement = {key: value for key,
                         value in statement.items() if value}

            policy["Statement"].append(statement)

    return json.dumps(policy, indent=2)
