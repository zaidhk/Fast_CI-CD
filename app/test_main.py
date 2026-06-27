from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] is not None
    assert data["status"] == "running"


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "database" in data["checks"]
    assert "cache" in data["checks"]


def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    assert "http_requests_total" in response.text


def test_unknown_route_returns_404():
    response = client.get("/nonexistent")
    assert response.status_code == 404


def test_metrics_counters_increment():
    client.get("/")
    client.get("/health")
    response = client.get("/metrics")
    content = response.text
    assert 'http_requests_total{method="GET",endpoint="/"}' in content
    assert 'http_requests_total{method="GET",endpoint="/health"}' in content
