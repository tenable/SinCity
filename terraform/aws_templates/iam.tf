{% if 'policies' in network %}
# Autogenerated policies
  {% for key,value in network.policies.items() %}
resource "aws_iam_policy" "{{ key }}" {
  name        = "{{ key }}"
  description = "{{ value.description | default("") }}"
  policy      = {{ value | to_aws_policy | to_terraform_json | safe }}
}
  {% endfor %}
# End of auto generated policies
{% endif %}


{% if 'groups' in network %}
  # Autogenerated groups
  {% for key,value in network.groups.items() %}
resource "aws_iam_group" "{{ key }}" {
  name = "{{ key }}"
  path = "{{ value.path | default('/') }}"
}

    {% if 'policies' in value %}
        {% for policy in value.policies %}
  resource "aws_iam_group_policy_attachment" "{{ key }}_{{ policy }}" {
    group      = aws_iam_group.{{ key }}.name
    policy_arn = aws_iam_policy.{{ policy }}.arn
  }
        {% endfor %}
    {% endif %}
  {% endfor %}
  # End of auto generated groups
{% endif %}


{% if 'users' in network %}
  # Autogenerated users
  {% for key,value in network.users.items() %}
    resource "aws_iam_user" "{{ key }}" {
      name = "{{ key }}"
      path = "{{ value.path | default('/') }}"
    }

    {% if 'policies' in value %}
        {% for policy in value.policies %}
  resource "aws_iam_user_policy_attachment" "{{ key }}_{{ policy }}" {
    user      = aws_iam_user.{{ key }}.name
    policy_arn = aws_iam_policy.{{ policy }}.arn
  }
        {% endfor %}
    {% endif %}

    {% if 'groups' in value %}
resource "aws_iam_user_group_membership" "{{ key }}_groups" {
  user      = aws_iam_user.{{ key }}.name
  groups = {{ value.groups | to_terraform_array('aws_iam_group','name') | safe }}
}
    {% endif %}
  {% endfor %}
  # End of auto generated users
{% endif %}

{% if 'roles' in network %}
  # Autogenerated roles
  {% for key,value in network.roles.items() %}
resource "aws_iam_role" "{{ key }}" {
  name = "{{ key }}"
  path = "{{ value.path | default('/') }}"

  {% if 'assume_role_policy' in value %}
  assume_role_policy = {{ value.assume_role_policy | to_aws_policy | to_terraform_json | safe }}
  {% endif %}
}

  {% if 'policies' in value %}
    {% for policy in value.policies %}
resource "aws_iam_role_policy_attachment" "{{ key }}_{{ policy }}" {
  role       = aws_iam_role.{{ key }}.name
  policy_arn = aws_iam_policy.{{ policy }}.arn
}
    {% endfor %}
  {% endif %}

  {% endfor %}
  # End of autogenerated roles
{% endif %}