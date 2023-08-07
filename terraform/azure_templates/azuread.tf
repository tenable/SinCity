{% if 'users' in network %}
{% for username, user in network.users.items() %}
resource "azuread_user" "{{ username }}" {
  display_name                = "{{ username }}@{{ config.azure_domain }}"
  password                    = "Cyber123!"
  user_principal_name         = "{{ username }}@{{ config.azure_domain }}"
}
{% if 'groups' in user %}
{% for name in user.groups %}
  resource "azuread_group_member" "{{ username }}" {
    group_object_id  = azuread_group.{{name}}.id
    member_object_id = azuread_user.{{username}}.id
}
      {% endfor %}
    {% endif %}
  {% endfor %}
{% endif %}

{% if 'groups' in network %}
{% for groupname, group in network.groups.items() %}
resource "azuread_group" "{{ groupname }}" {
  display_name             = "{{ groupname }}"
  security_enabled         = true
}
{% endfor %}
{% endif %}
