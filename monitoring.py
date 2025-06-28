import time
import logging
from functools import wraps
from prometheus_client import Counter, Histogram, generate_latest
from fastapi import Request, Response
from fastapi.responses import PlainTextResponse

# Metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')
CACHE_HITS = Counter('cache_hits_total', 'Total cache hits')
CACHE_MISSES = Counter('cache_misses_total', 'Total cache misses')

def track_performance(func):
    """Decorator to track function performance"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            duration = time.time() - start_time
            REQUEST_DURATION.observe(duration)
    return wrapper

# Add to main.py for metrics endpoint
@app.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint"""
    return PlainTextResponse(generate_latest())