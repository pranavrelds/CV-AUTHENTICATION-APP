resource "random_id" "random_string" {
  byte_length = 8
}

resource "azurerm_service_plan" "cv_authentication_service_plan" {
  name                = "${random_id.random_string.dec}-${var.webapp_service_plan_name}"
  resource_group_name = module.container_registry.cv_authentication_resource_group_name
  location            = module.container_registry.cv_authentication_resource_group_location
  os_type             = var.webapp_os_type
  sku_name            = var.webapp_sku_name
}

resource "azurerm_linux_web_app" "mydockerapp" {
  name                = "${random_id.random_string.dec}${var.web_app_name}"
  resource_group_name = module.container_registry.cv_authentication_resource_group_name
  location            = module.container_registry.cv_authentication_resource_group_location
  service_plan_id     = azurerm_service_plan.cv_authentication_service_plan.id

  app_settings = {
    WEBSITES_ENABLE_APP_SERVICE_STORAGE = var.web_app_settings_storage
    WEBSITES_PORT                       = var.web_app_settings_port
    WEBSITES_CONTAINER_START_TIME_LIMIT = var.web_app_start_time_limit
    DOCKER_REGISTRY_SERVER_URL          = module.container_registry.cv_authentication_login_server
    DOCKER_REGISTRY_SERVER_USERNAME     = module.container_registry.cv_authentication_admin_username
    DOCKER_REGISTRY_SERVER_PASSWORD     = module.container_registry.cv_authentication_admin_password
  }

  site_config {
    application_stack {
      docker_image     = "${module.container_registry.cv_authentication_login_server}/${var.docker_image_name}"
      docker_image_tag = var.docker_image_tag
    }
  }
}
