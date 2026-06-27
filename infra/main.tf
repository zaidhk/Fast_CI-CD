terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {
}

resource "docker_network" "cicd_network" {
  name   = "cicd-network"
  driver = "bridge"
}

resource "docker_image" "app_image" {
  name         = var.docker_image
  keep_locally = true
}

resource "docker_container" "staging" {
  name    = "cicd-api-staging"
  image   = docker_image.app_image.image_id
  restart = "unless-stopped"

  ports {
    internal = 8000
    external = var.staging_port
  }

  networks_advanced {
    name = docker_network.cicd_network.name
  }

  healthcheck {
    test         = ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
    interval     = "15s"
    timeout      = "5s"
    retries      = 3
    start_period = "10s"
  }
}
