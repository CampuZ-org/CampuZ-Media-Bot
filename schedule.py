import pandas as pd
from pathlib import Path
from typing import List, Dict
from loguru import logger

def load_schedule(project_dir: str) -> tuple[List[Dict], List[Dict], Dict]:
    """Читает schedule.xlsx."""
    file_path = Path(f"/app/projects/{project_dir}/schedule.xlsx")
    try:
        events = pd.read_excel(file_path, sheet_name="События").to_dict("records")
        messages = pd.read_excel(file_path, sheet_name="Сервисные сообщения").to_dict("records")
        polls = pd.read_excel(file_path, sheet_name="Опросы").set_index("Машинное имя").to_dict("index")
        return events, messages, polls
    except Exception as e:
        logger.error(f"Schedule load error in {project_dir}: {e}")
        raise