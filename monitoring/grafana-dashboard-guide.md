# Guide rapide : Importer un dashboard Grafana

## Prérequis
- Prometheus et Grafana sont lancés (cf. `monitoring/docker-compose.yml`)
- L'application API expose ses métriques sur `/metrics`

## Accès
- Grafana : http://localhost:3000
- Identifiants par défaut : `admin / admin`

## 1. Ajouter Prometheus comme Data Source

1. Connectez-vous à Grafana (http://localhost:3000)
2. Allez dans **Configuration (gear icon)** > **Data Sources** > **Add data source**
3. Choisissez **Prometheus**
4. Dans le champ **URL**, mettez : `http://prometheus:9090`
5. Cliquez sur **Save & Test**

## 2. Importer un dashboard JSON

Créez un nouveau dashboard et ajoutez les deux panels suivants :

### Panel 1 : Requêtes HTTP par minute (Graphique en série temporelle)

- **Type** : Time series
- **Requête PromQL** :
  ```
  rate(http_requests_total[1m])
  ```
- **Legend** : `{{method}} - {{endpoint}}`
- **Unit** : cpm (counts per minute)
- **Title** : Requêtes HTTP par minute

### Panel 2 : Latence des requêtes HTTP (p99 en secondes)

- **Type** : Time series
- **Requête PromQL** :
  ```
  histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, method, endpoint))
  ```
- **Legend** : `{{method}} - {{endpoint}}`
- **Unit** : seconds
- **Title** : Latence p99 des requêtes HTTP

### Sauvegarde

1. Cliquez sur l'icône **Save** (disquette) en haut à droite
2. Donnez un nom au dashboard (ex: "CI/CD API Monitoring")
3. Cliquez sur **Save**

## 3. Alternative : Dashboard JSON import

Vous pouvez aussi télécharger un dashboard pré-fait depuis https://grafana.com/grafana/dashboards/
et chercher "FastAPI" ou "Python monitoring" pour trouver des dashboards compatibles.
