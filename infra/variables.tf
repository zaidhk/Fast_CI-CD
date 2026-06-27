variable "docker_image" {
  description = "Docker image to deploy for staging"
  type        = string
  default     = "ghcr.io/opencode/cicd-api:latest"
}

variable "staging_port" {
  description = "External port for the staging container"
  type        = number
  default     = 8081
}
