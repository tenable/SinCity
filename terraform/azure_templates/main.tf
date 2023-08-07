terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.65.0"
    }
    azuread = {
      source  = "hashicorp/azuread"
    }
  }
}
provider "azurerm" {
  features {}
}