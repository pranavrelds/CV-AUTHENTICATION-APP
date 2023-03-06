variable "cv_authentication_acr_name" {
  default = "cv_authentication_ACR"
  type    = string
}

variable "cv_authentication_acr_sku" {
  default = "Standard"
  type    = string
}

variable "cv_authentication_acr_admin_enabled" {
  default = true
  type    = bool
}
