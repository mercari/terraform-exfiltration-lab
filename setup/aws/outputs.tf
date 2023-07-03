output "command" {
  description = "Please add a secret version for the secret you just created using this command."
  value       = <<EOT
# Please add a secret version for the secret you just created using this command:

aws secretsmanager put-secret-value \
    --region ${var.region} \
    --secret-id ${aws_secretsmanager_secret.secret.id} \
    --secret-string "${var.secret}"
EOT
}
