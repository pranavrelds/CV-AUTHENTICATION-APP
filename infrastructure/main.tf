terraform {}

provider "azurerm" {
  features {}
}

module "web_app" {
  source = "./module_web_app"
}
