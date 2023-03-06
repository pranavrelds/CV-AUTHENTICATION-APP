output "cv_authentication_acr_login_server" {
  value = azurerm_container_registry.cv_auth_app.login_server
}

output "cv_authentication_acr_admin_username" {
  value = azurerm_container_registry.cv_auth_app.admin_username
}

output "cv_authentication_acr_admin_password" {
  value = azurerm_container_registry.cv_auth_app.admin_password
}

output "cv_authentication_resource_group_name" {
  value = module.resource_group.cv_authentication_resource_group_name
}

output "cv_authentication_resource_group_location" {
  value = module.resource_group.cv_authentication_resource_group_location
}