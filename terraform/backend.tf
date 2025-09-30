terraform {
  backend "s3" {
    bucket  = "devops-course-terraform-tfstate-bucket-2025"
    key     = "infra/terraform.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}
