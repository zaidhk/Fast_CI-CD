from fastapi import FastAPI, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Histogram, Gauge
import time

app = FastAPI(title="DevOps CI/CD Demo API", version="1.0.0")

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "HTTP request latency", ["method", "endpoint"])
IN_PROGRESS = Gauge("http_requests_in_progress", "Requests in progress")


@app.middleware("http")
async def metrics_middleware(request, call_next):
    method = request.method
    path = request.url.path
    IN_PROGRESS.inc()
    REQUEST_COUNT.labels(method=method, endpoint=path).inc()
    start = time.time()
    response = await call_next(request)
    REQUEST_LATENCY.labels(method=method, endpoint=path).observe(time.time() - start)
    IN_PROGRESS.dec()
    return response


@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API DevOps CI/CD - v1.0.1", "status": "running"}


@app.get("/health")
def health():
    return {"status": "healthy", "checks": {"database": "skipped", "cache": "skipped"}}


@app.get("/metrics")
def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
