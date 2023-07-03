variable "project" {
  type = string
}

variable "region" {
  type = string
}

variable "exfil_bucket" {
  type = string
}

variable "exfil_id" {
  type    = number
  default = 101010
}

variable "secret_id" {
  type = string
}
