resource "azurerm_resource_group" "resource_group_sincity" {
  name     = "{{ network.cloud.azure.resource_group }}"
  location = "{{ config.region }}"
}