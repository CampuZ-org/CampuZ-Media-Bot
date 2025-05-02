from prometheus_client import Counter, Histogram, start_http_server
from loguru import logger

# Метрики
cycle_duration = Histogram("bot_cycle_duration_seconds", "Cycle duration")
tact_duration = Histogram("bot_media_tact_duration_seconds", "Media tact duration")
posts_published = Counter("bot_posts_published_total", "Total posts published")
posts_rejected = Counter("bot_posts_rejected_total", "Total posts rejected")
errors = Counter("bot_errors_total", "Total errors")

def start_metrics_server():
    """Запускает сервер метрик Prometheus."""
    try:
        start_http_server(8000)
        logger.info("Prometheus metrics server started at :8000/metrics")
    except Exception as e:
        logger.error(f"Metrics server error: {e}")

def observe_cycle_duration(seconds: float):
    """Регистрирует длительность цикла."""
    cycle_duration.observe(seconds)

def observe_tact_duration(seconds: float):
    """Регистрирует длительность медиа-такта."""
    tact_duration.observe(seconds)

def increment_posts_published():
    """Увеличивает счётчик опубликованных постов."""
    posts_published.inc()

def increment_posts_rejected():
    """Увеличивает счётчик отклонённых постов."""
    posts_rejected.inc()

def increment_errors():
    """Увеличивает счётчик ошибок."""
    errors.inc()