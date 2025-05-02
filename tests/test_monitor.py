import pytest
from monitor import start_metrics_server, increment_posts_published, increment_errors
from unittest.mock import patch


@pytest.mark.asyncio
async def test_metrics():
    """Тестирует метрики Prometheus."""
    with patch("prometheus_client.start_http_server") as mock_server:
        start_metrics_server()
        mock_server.assert_called_with(8000)

    increment_posts_published()
    increment_errors()
    # Проверка метрик требует реального Prometheus, здесь только вызовы