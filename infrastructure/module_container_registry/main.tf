module "resource_group" {
  source = "../module_resource_group"
}

resource "random_id" "random_string_for_acr" {
  byte_length = 8
}

resource "azurerm_container_registry" "cv_auth_app" {
  name                = "${random_id.random_string_for_acr.dec}${var.cv_authentication_acr_name}"
  resource_group_name = module.resource_group.cv_authentication_resource_group_name
  location            = module.resource_group.cv_authentication_resource_group_location
  admin_enabled       = var.cv_authentication_acr_admin_enabled
  sku                 = var.cv_authentication_acr_sku
}
