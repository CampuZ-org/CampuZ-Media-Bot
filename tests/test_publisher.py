import pytest
from publisher import publish_post
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_publish_post(tmp_path: Path):
    """Тестирует публикацию поста."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    (project_dir / "data").mkdir()

    post = {"title": "Test", "text": "Test post", "timestamp": "2025-05-02T10:00"}
    with patch("connectors.telegram.publish_to_telegram", AsyncMock(return_value="123")):
        await publish_post(post, "mock-token", project_dir.name)

    # Проверка статистики
    with open(project_dir / "data/stats.csv", "r") as f:
        assert "123" in f.read()

        