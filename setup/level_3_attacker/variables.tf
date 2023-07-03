variable "project" {
  type = string
}

variable "region" {
  type = string
}

variable "exfil_bucket" {
  type = string
}

variable "exfil_bucket_location" {
  type    = string
  default = "US"
}
