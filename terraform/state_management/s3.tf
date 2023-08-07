terraform {
  backend "s3" {
    bucket         = "{{ state_backend_name }}"
    key            = "global/s3/terraform.tfstate"
    region           = "{{ region }}"

    dynamodb_table = "{{ state_backend_name }}"
    encrypt        = true
  }
}