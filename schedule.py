import pandas as pd
from pathlib import Path
from typing import List, Dict
from loguru import logger
import requests
from requests.exceptions import RequestException

def check_image_url(url: str) -> bool:
    """Проверяет доступность URL изображения."""
    if not url:
        return False
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200 and 'image' in response.headers.get('content-type', '').lower()
    except RequestException as e:
        logger.warning(f"Image URL check failed for {url}: {e}")
        return False

def load_schedule(project_dir: str) -> tuple[List[Dict], List[Dict], Dict]:
    """Читает schedule.xlsx и проверяет URL изображений."""
    file_path = Path(f"/app/projects/{project_dir}/schedule.xlsx")
    try:
        events = pd.read_excel(file_path, sheet_name="События").to_dict("records")
        messages = pd.read_excel(file_path, sheet_name="Сервисные сообщения").to_dict("records")
        polls = pd.read_excel(file_path, sheet_name="Опросы").set_index("Машинное имя").to_dict("index")

        # Проверка URL изображений в событиях
        for event in events:
            image_url = event.get("Картинка", "")
            if image_url and not check_image_url(image_url):
                logger.info(f"Resetting invalid image URL for event {event.get('Название', '')}")
                event["Картинка"] = ""

        # Проверка URL изображений в сервисных сообщениях
        for message in messages:
            image_url = message.get("Картинка", "")
            if image_url and not check_image_url(image_url):
                logger.info(f"Resetting invalid image URL for message {message.get('Название', '')}")
                message["Картинка"] = ""

        return events, messages, polls
    except Exception as e:
        logger.error(f"Schedule load error in {project_dir}: {e}")
        raise