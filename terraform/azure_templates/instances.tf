{% if 'hosts' in network %}

  {% if 'load_balancers' in network %}
    {% for lb_name,lb_value in network.load_balancers.items() %}
resource "azurerm_availability_set" "{{ lb_name }}" {
  name                = "{{ lb_name }}"
  location            = azurerm_resource_group.resource_group_sincity.location
  resource_group_name = azurerm_resource_group.resource_group_sincity.name

  platform_fault_domain_count = 2
  platform_update_domain_count = 5
}
    {% endfor %}
  {% endif %}


  {% for key,value in network.hosts.items() %}
resource "azurerm_public_ip" "pi_{{ key }}" {
  name                = "pi_{{ key }}"
  resource_group_name = azurerm_resource_group.resource_group_sincity.name
  location            = azurerm_resource_group.resource_group_sincity.location
  allocation_method   = "Static"
}

resource "azurerm_network_interface" "ni_{{ key }}" {
  name                = "{{ key }}"
  location            = azurerm_resource_group.resource_group_sincity.location
  resource_group_name = azurerm_resource_group.resource_group_sincity.name
  ip_configuration {
    name                          = "ip_configuration_{{ key }}"
    subnet_id                     = azurerm_subnet.{{value.subnet}}.id
    private_ip_address_allocation = "Static"
    private_ip_address            = "{{value.ip}}"
    public_ip_address_id          = azurerm_public_ip.pi_{{ key }}.id
  }
}

resource "azurerm_virtual_machine" "{{ key }}" {
  name                             = "{{ key }}"
  location                         = azurerm_resource_group.resource_group_sincity.location
  resource_group_name              = azurerm_resource_group.resource_group_sincity.name
  network_interface_ids            = {{['ni_' + key] | to_terraform_array("azurerm_network_interface", "id") | safe }}
  vm_size                          = "Standard_DS1_v2"
  delete_os_disk_on_termination    = true
  delete_data_disks_on_termination = true
  os_profile {
    computer_name  = "{{ key }}"
    admin_username = "centos"
    # admin_password = "Cyber123!"
    custom_data = file("{{ '../../resources/configure_for_ansible.ps1' if value.type == 'windows' else '../../resources/configure_for_ansible.sh' }}")
  }

  {% if 'identities' in value %}
  identity {
    type = "UserAssigned"
    identity_ids = {{ value.identities | to_terraform_array('azurerm_user_assigned_identity', 'id') | safe }}
  }
  {% endif %}

  {% if 'load_balancers' in network %}
    {% for lb_name,lb_value in network.load_balancers.items() %}
      {% if 'hosts' in lb_value and key in lb_value.hosts %}
  availability_set_id = azurerm_availability_set.{{ lb_name }}.id
      {% endif %}
    {% endfor %}
  {% endif %}


    {% if value.type == "linux" %}
  os_profile_linux_config {
    disable_password_authentication  = true
    ssh_keys {
      path     = "/home/centos/.ssh/authorized_keys"
      key_data =   "{{ network.keypair.public_key }}"
    }
  }
    {% endif %}
  storage_os_disk{
        name                             = "{{key}}sincitystorage_os_disk"
        caching                          = "ReadWrite"
        create_option                    = "FromImage"
}
  storage_image_reference {
    publisher = "{{ network.server_roles[value.role].providers.azure.publisher }}"
    offer     = "{{ network.server_roles[value.role].providers.azure.offer }}"
    sku       = "{{ network.server_roles[value.role].providers.azure.sku }}"
    version   = "{{ network.server_roles[value.role].providers.azure.version }}"
  }
  tags = {
    Project = "sincity_lab", Role = "{{value.role}}"
  }
}
  {% endfor %}
{% endif %}
