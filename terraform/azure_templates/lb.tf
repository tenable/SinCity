# Auto generated alb
{% if 'load_balancers' in network %}
  {% for key, value in network.load_balancers.items() %}

# Generate a public ip address for the load balancer
resource "azurerm_public_ip" "{{ key }}" {
  name                = "my-public-ip"
  location            = azurerm_resource_group.resource_group_sincity.location
  resource_group_name = azurerm_resource_group.resource_group_sincity.name
  allocation_method = "Dynamic"

  {% if value.tags %}
  tags = {
    {{ value.tags | to_terraform_json(2, True) | safe }}
  }
  {% endif %}
}

# Generate the Load Balancer
resource "azurerm_lb" "{{ key }}" {
  name                = "{{ key }}"
  location            = azurerm_resource_group.resource_group_sincity.location
  resource_group_name = azurerm_resource_group.resource_group_sincity.name

  frontend_ip_configuration {
    name                 = "{{ key }}_frontend_ip_config"
    public_ip_address_id = azurerm_public_ip.{{ key }}.id
  }


  {% if value.tags %}
  tags = {
    {{ value.tags | to_terraform_json(2, True) | safe }}
  }
  {% endif %}
}

  {% if 'hosts' in value %}
# Generate the Backend Address Pool
resource "azurerm_lb_backend_address_pool" "{{ key }}" {
  loadbalancer_id = azurerm_lb.{{ key }}.id
  name            = "{{ key }}"
}

# Attach the backend instances/computers
  {% for hostname, value in network.hosts.items() %}
resource "azurerm_network_interface_backend_address_pool_association" "{{ key }}-{{ hostname }}" {
  network_interface_id    = azurerm_network_interface.ni_{{ hostname }}.id
  ip_configuration_name   = "ip_configuration_{{ hostname }}"
  backend_address_pool_id = azurerm_lb_backend_address_pool.{{ key }}.id
}
  {% endfor %}

# Generate the Load Balancer Rule
resource "azurerm_lb_rule" "{{ key }}" {
  loadbalancer_id                = azurerm_lb.{{ key }}.id
  name                           = "{{ key }}"
  protocol                       = "{{ 'Tcp' if value.protocol == 'http' or value.protocol == 'https' else value.protocol | default('Tcp') | capitalize }}"
  frontend_port                  = {{ value.forward_port | default(80) }}
  backend_port                   = {{ value.host_port | default(80) }}
  frontend_ip_configuration_name = "{{ key }}_frontend_ip_config"
  backend_address_pool_ids        = [azurerm_lb_backend_address_pool.{{ key }}.id]
}
  {% endif %}

  {% endfor %}
{% endif %}
# End of auto generated alb
