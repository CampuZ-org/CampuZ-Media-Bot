import pytest
from agents.ai_kurator import create_task
from agents.ai_journalist import generate_post
from agents.ai_editor import review_post
from datetime import datetime, timedelta
from pathlib import Path


@pytest.mark.asyncio
async def test_kurator(tmp_path: Path):
    """Тестирует создание задания."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    (project_dir / "data").mkdir()

    events = [{"Название": "Доклад", "Время начала": "2025-05-02T10:00"}]
    now = datetime.fromisoformat("2025-05-02T09:55")
    tasks = await create_task(events, [], now, now - timedelta(minutes=10), now + timedelta(minutes=20),
                              {"media_task": "Test"}, project_dir.name)
    assert len(tasks) == 1
    assert tasks[0]["occasion"]["Название"] == "Доклад"


@pytest.mark.asyncio
async def test_journalist(tmp_path: Path):
    """Тестирует генерацию поста."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    (project_dir / "templates").mkdir()
    (project_dir / "templates/post.yaml").write_text("template: '{title}'")

    task = {"occasion": {"Название": "Доклад"}, "profile": "casual_host"}
    config = {"profiles": {"casual_host": {"tone": "informal", "emojis": True}}}
    post = await generate_post(task, config, project_dir.name)
    assert "🎉" in post["text"]


@pytest.mark.asyncio
async def test_editor(tmp_path: Path):
    """Тестирует проверку поста."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()

    post = {"title": "Test", "text": "Test post"}
    config = {"min_interval_minutes": 5}
    approved, action = await review_post(post, config, project_dir.name)
    assert approved
    assert action == "publish"