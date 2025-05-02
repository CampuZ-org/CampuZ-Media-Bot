import pytest
import pandas as pd
from pathlib import Path
from schedule import load_schedule


@pytest.mark.asyncio
async def test_load_schedule(tmp_path: Path):
    """Тестирует загрузку расписания."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()

    # Создание mock-Excel
    writer = pd.ExcelWriter(project_dir / "schedule.xlsx")
    pd.DataFrame([{"Название": "Доклад", "Время начала": "2025-05-02T10:00"}]).to_excel(writer, sheet_name="События")
    pd.DataFrame([{"Название": "Объявление", "Время": "2025-05-02T11:00"}]).to_excel(writer,
                                                                                     sheet_name="Сервисные сообщения")
    pd.DataFrame([{"Машинное имя": "poll1", "Вопрос": "Придёте?"}]).to_excel(writer, sheet_name="Опросы")
    writer.close()

    events, messages, polls = load_schedule(project_dir.name)
    assert len(events) == 1
    assert events[0]["Название"] == "Доклад"
    assert polls["poll1"]["Вопрос"] == "Придёте?"