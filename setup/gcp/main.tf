resource "google_secret_manager_secret" "secret" {
  project   = var.project
  secret_id = var.secret_id

  replication { automatic = true }

  labels = {
    label = "very-secret"
  }
}

resource "google_secret_manager_secret_version" "secret" {
  secret = google_secret_manager_secret.secret.id

  secret_data = var.secret
}
