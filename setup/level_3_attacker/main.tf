resource "google_storage_bucket" "exfil_bucket" {
  name          = var.exfil_bucket
  location      = var.exfil_bucket_location
  force_destroy = true

  public_access_prevention = "enforced"
}


resource "google_project_iam_audit_config" "audit_log" {
  project = var.project
  service = "storage.googleapis.com"

  audit_log_config {
    log_type = "DATA_READ"
  }
}
