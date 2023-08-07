resource "azurerm_virtual_network" sincity_virtual_network {
name = "sincity_virtual_network"
resource_group_name = azurerm_resource_group.resource_group_sincity.name
address_space = ["{{network.cloud.azure.virtual_network_address_space if cloud in network else '10.0.0.0/16' | safe }}"] //fixme
location = azurerm_resource_group.resource_group_sincity.location
}
{% if 'subnets' in network %}
{% for name ,subnet in network.subnets.items() %}
resource "azurerm_subnet" "{{ name }}" {
  name                 = "{{ name }}"
  resource_group_name  = azurerm_resource_group.resource_group_sincity.name
  virtual_network_name = azurerm_virtual_network.sincity_virtual_network.name
  address_prefixes     = {{[subnet.address] | tojson | safe}}
}
  {% endfor %}
{% endif %}


{% if 'security_groups' in network %}
{% for name ,securitygroup in network.security_groups.items() %}
resource "azurerm_network_security_group" "{{ name }}" {
  name                = "{{ name }}"
  location            = azurerm_resource_group.resource_group_sincity.location
  resource_group_name = azurerm_resource_group.resource_group_sincity.name
  {% for k ,v in securitygroup.inbound.items() %}
  security_rule {
    name                       = "{{k}}"
    direction                  = "Inbound"
    access                     = "{{ v.access | capitalize }}"
    protocol                   = "{{(v.protocol if v.protocol != -1 else '*') | capitalize}}"
    source_port_range          = "*"
    destination_port_range     = "{{v.start_port-v.end_port}}"

    {% if '0.0.0.0/0' in v.cidr_blocks %}
    source_address_prefix = "*"
    {% else %}
    source_address_prefixes = {{ v.cidr_blocks | to_terraform_array("", "", True) | safe }}
    {% endif %}
    destination_address_prefix = "*"
    priority                   = {{ loop.index + 99 }}
  }
          {% endfor %}

  {% for k ,v in securitygroup.outbound.items() %}
  security_rule {
    name                       = "{{k}}"
    direction                  = "Outbound"
    access                     = "{{v.access | capitalize }}"
    protocol                   = "{{(v.protocol if v.protocol != -1 else '*') | capitalize}}"
    source_port_range          = "{{v.start_port-v.end_port}}"
    destination_port_range     = "*"
    source_address_prefix      = "*"
    destination_address_prefix = "{{( '*' if '0.0.0.0/0' in v.cidr_blocks else v.cidr_blocks)}}" #fixme
    priority                   = {{ loop.index + 99 }}
  }
          {% endfor %}
}
  {% endfor %}
{% endif %}

{% if 'network_interfaces' in network %}
{% for name ,network_interface in network.network_interfaces.items() %}
resource "azurerm_network_interface" "{{ name }}" {
  name                = "{{ name }}"
  location            = azurerm_resource_group.resource_group_sincity.location
  resource_group_name = azurerm_resource_group.resource_group_sincity.name
  {% if 'ip_configurations' in network_interface %}
  {% for ipname ,ip_configuration in network_interface.ip_configurations.items() %}
  ip_configuration {
    name                          = "{{ ipname }}"
    subnet_id                     = azurerm_subnet.{{ ip_configuration.subnet_id }}.id
    private_ip_address_allocation = "{{ ip_configuration.private_ip_address_allocation }}"
  }
      {% endfor %}
    {% endif %}
}
  {% endfor %}
{% endif %}

{% if 'networksecurityconnection' in network %}
{% for name ,con in network.networksecurityconnection.items() %}
resource "azurerm_network_interface_security_group_association" "{{ name }}" {
  network_interface_id      = azurerm_network_interface.{{con.network_interface}}.id
  network_security_group_id = azurerm_network_security_group.{{con.network_security_group}}.id
}
  {% endfor %}
{% endif %}

