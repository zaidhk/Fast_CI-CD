output "staging_url" {
  description = "URL de l'application de staging"
  value       = "http://localhost:${var.staging_port}"
}

output "staging_health_endpoint" {
  description = "Endpoint health check du staging"
  value       = "http://localhost:${var.staging_port}/health"
}

output "container_name" {
  description = "Nom du conteneur Docker de staging"
  value       = docker_container.staging.name
}
