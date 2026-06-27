# Projet DevOps CI/CD Pipeline

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│   GitHub     │────▶│  GitHub       │────▶│  Docker Hub  │
│   Repository │     │  Actions /   │     │  / ghcr.io   │
│              │     │  Jenkins     │     │              │
└─────────────┘     └──────┬───────┘     └──────────────┘
                           │
                    ┌──────▼───────┐
                    │  SonarQube   │
                    │  (Quality)   │
                    └──────────────┘
                           │
                    ┌──────▼───────┐
                    │   Trivy      │
                    │  (Security)  │
                    └──────────────┘
                           │
                    ┌──────▼───────┐
                    │  Terraform   │
                    │  (Docker)    │
                    └──────────────┘
                           │
                    ┌──────▼───────┐
                    │   Staging    │
                    │  localhost:  │
                    │    8081      │
                    └──────────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
       ┌──────▼────┐ ┌────▼─────┐ ┌───▼─────┐
       │Prometheus │ │ Grafana  │ │  Smoke  │
       │:9090      │ │ :3000    │ │  Tests  │
       └───────────┘ └──────────┘ └─────────┘
```

### Stack technique

| Composant      | Technologie                        |
|----------------|------------------------------------|
| Application    | Python 3.11 + FastAPI              |
| Base de test   | pytest + pytest-cov                |
| Linter         | flake8                             |
| CI/CD          | GitHub Actions + Jenkins (au choix)|
| Qualité        | SonarQube                          |
| Sécurité       | Trivy                              |
| Conteneurisation | Docker + Docker Compose          |
| Infrastructure | Terraform + Provider Docker        |
| Monitoring     | Prometheus + Grafana               |

## Pipeline CI/CD (9 étapes)

| Stage | Nom             | Description                          |
|-------|-----------------|--------------------------------------|
| 1     | Checkout        | Récupération du code source          |
| 2     | Lint            | Analyse statique avec flake8         |
| 3     | Build & Test    | Tests unitaires + couverture         |
| 4     | SonarQube Scan  | Analyse qualité du code              |
| 5     | Quality Gate    | Validation du Quality Gate           |
| 6     | Security Scan   | Scan Trivy de l'image Docker         |
| 7     | Push            | Publication vers le registre         |
| 8     | IaC Apply       | Déploiement staging avec Terraform   |
| 9     | Smoke Test      | Vérification de l'endpoint /health   |

## Prérequis locaux

- Docker Desktop (avec support WSL2 ou Hyper-V)
- Python 3.11+
- Terraform >= 1.5
- Trivy (optionnel, pour le scan local)

## Lancement local

### 1. Application seule

```bash
pip install -r requirements.txt
cd app
uvicorn main:app --host 0.0.0.0 --port 8000
```

Accès : http://localhost:8000

### 2. Avec Docker Compose

```bash
docker compose up --build -d
```

Accès : http://localhost:8000

### 3. Tests unitaires

```bash
pip install -r requirements.txt
cd app
pytest test_main.py --cov=. --cov-report=term -v
```

### 4. Lint

```bash
flake8 app/ --max-line-length=120 --count
```

### 5. Infrastructure (Terraform)

```bash
docker network create cicd-network
cd infra
terraform init
terraform apply -auto-approve -var="staging_port=8081"
```

Staging disponible sur : http://localhost:8081

### 6. Monitoring

```bash
docker network create cicd-network
cd monitoring
docker compose up -d
```

- Prometheus : http://localhost:9090
- Grafana : http://localhost:3000 (admin/admin)

## Exécution du pipeline

### GitHub Actions

1. Pushez le code sur GitHub
2. Configurez les secrets dans **Settings > Secrets and variables > Actions** :
   - `SONAR_TOKEN` : token SonarQube Cloud
   - `GITHUB_TOKEN` : automatiquement fourni par GitHub
3. Le pipeline s'exécute automatiquement sur chaque push vers `main`/`master`

### Jenkins (local)

1. Lancez Jenkins : `docker run -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts`
2. Installez les plugins : Docker Pipeline, SonarQube Scanner, Terraform
3. Créez un **Pipeline** job pointant vers ce repository (branche main)
4. Configurez les credentials Jenkins :
   - `sonar-host-url` : URL du serveur SonarQube
   - `sonar-token` : token d'authentification
   - `ghcr-credentials` : credentials Docker pour ghcr.io
5. Lancez le build

## Structure du projet

```
ProjetDevops/
├── app/
│   ├── main.py              # API FastAPI
│   └── test_main.py          # Tests unitaires
├── .github/
│   └── workflows/
│       └── ci-cd.yml         # Pipeline GitHub Actions
├── infra/
│   ├── main.tf               # Terraform (Docker provider)
│   ├── variables.tf
│   └── outputs.tf
├── monitoring/
│   ├── docker-compose.yml    # Prometheus + Grafana
│   ├── prometheus.yml        # Configuration Prometheus
│   └── grafana-dashboard-guide.md
├── Dockerfile                # Image Docker optimisée
├── docker-compose.yml        # Application Compose
├── Jenkinsfile               # Pipeline Jenkins
├── requirements.txt
└── README.md
```
