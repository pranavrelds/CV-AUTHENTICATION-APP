resource "random_id" "random_string_for_rg" {
  byte_length = 8
}

resource "azurerm_resource_group" "cv_authentication_resource_group" {
  name     = "${random_id.random_string_for_rg.dec}-${var.cv_authentication_resource_group_name}"
  location = var.cv_authentication_resource_group_location
}