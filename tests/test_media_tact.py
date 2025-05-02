import pytest
from pathlib import Path
from media_tact import run_media_tact


@pytest.mark.asyncio
async def test_media_tact(tmp_path: Path):
    """Тестирует медиа-такт."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    (project_dir / "config.yaml").write_text("""
timezone: "Europe/Moscow"
llm_provider: "openai"
llm_api_key: "mock-key"
telegram_token: "mock-token"
""")
    (project_dir / "ai_kurator.yaml").write_text("media_task: 'Test task'")
    (project_dir / "ai_journalist.yaml").write_text(
        "media_task: 'Test task'\nprofiles: {'default': {'tone': 'formal'}}")
    (project_dir / "ai_editor.yaml").write_text("media_task: 'Test task'")
    (project_dir / "templates").mkdir()
    (project_dir / "templates/post.yaml").write_text("template: '{title}'")
    (project_dir / "data").mkdir()

    # Mock schedule.xlsx
    writer = pd.ExcelWriter(project_dir / "schedule.xlsx")
    pd.DataFrame([{"Название": "Доклад", "Время начала": "2025-05-02T10:00"}]).to_excel(writer, sheet_name="События")
    pd.DataFrame([]).to_excel(writer, sheet_name="Сервисные сообщения")
    pd.DataFrame([]).to_excel(writer, sheet_name="Опросы")
    writer.close()

    await run_media_tact(project_dir.name)  # Проверяет, что медиа-такт не падает