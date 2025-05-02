import pytest
from pathlib import Path
from config import load_config
from pydantic import ValidationError


@pytest.mark.asyncio
async def test_load_config(tmp_path: Path):
    """Тестирует загрузку конфигурации."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()

    # Создание mock-конфигураций
    (project_dir / "config.yaml").write_text("""
timezone: "Europe/Moscow"
llm_provider: "openai"
llm_api_key: "mock-key"
telegram_token: "mock-token"
""")
    (project_dir / "ai_kurator.yaml").write_text("media_task: 'Test task'")
    (project_dir / "ai_journalist.yaml").write_text("media_task: 'Test task'\nprofiles: {}")
    (project_dir / "ai_editor.yaml").write_text("media_task: 'Test task'")

    config, kurator, journalist, editor = load_config(project_dir.name)
    assert config.timezone == "Europe/Moscow"
    assert kurator.media_task == "Test task"


@pytest.mark.asyncio
async def test_invalid_config(tmp_path: Path):
    """Тестирует ошибку валидации."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()

    (project_dir / "config.yaml").write_text("timezone: 123")  # Неверный тип
    (project_dir / "ai_kurator.yaml").write_text("media_task: 'Test task'")
    (project_dir / "ai_journalist.yaml").write_text("media_task: 'Test task'\nprofiles: {}")
    (project_dir / "ai_editor.yaml").write_text("media_task: 'Test task'")

    with pytest.raises(ValidationError):
        load_config(project_dir.name)