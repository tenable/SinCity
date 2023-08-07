variable "additional_tags" {
  default = {
    Project = "sincity_lab"
  }
  description = "Additional resource tags"
  type        = map(string)
}