output "command" {
  description = "Please add a secret version for the secret you just created using this command."
  value       = <<EOT
# Please add a secret version for the secret you just created using this command:

echo -n "${var.secret}" | \
gcloud --project=${var.project} secrets versions add ${google_secret_manager_secret.secret.secret_id} --data-file=-
EOT
}
