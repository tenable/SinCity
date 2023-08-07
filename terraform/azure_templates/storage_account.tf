{% if 'storage' in network %}
   {% for name,storage in network.storage.items() %}
resource "azurerm_storage_account" "{{ name }}" {
  name                     = "{{ name }}"
  resource_group_name      = azurerm_resource_group.resource_group_sincity.name
  location                 = azurerm_resource_group.resource_group_sincity.location
  account_tier             = "Standard"
  account_replication_type = "GRS"
}
resource "azurerm_storage_container" "sincitycontainer" {
  # FIXME: This is hard-coded, need to move this into the network file
  name                  = "sincitycontainer"
  storage_account_name  = azurerm_storage_account.{{ name }}.name
  container_access_type = "{{storage.access_type}}"
}
  {% if 'files' in storage %}
  {% for file_key,file_value in storage.files.items() %}
  resource "azurerm_storage_blob" "{{ file_key }}" {
    storage_account_name   = azurerm_storage_account.{{ name }}.name
    storage_container_name = azurerm_storage_container.sincitycontainer.name
    type                   = "Block"
    {% if 'blob' in file_value %}
      source_content         = "{{ file_value.blob }}"
    {% endif %}
    {% if 'source' in file_value %}
      source       =            "{{ file_value.source }}"
    {% endif %}
    {% if 'path' in file_value %}
      name         = "{{ file_value.path }}"
    {% endif %}
      }
  {% endfor %}
{% endif %}
  {% endfor %}
{% endif %}
