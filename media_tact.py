import asyncio
from datetime import datetime, timedelta
import pytz
from config import load_config
from schedule import load_schedule
from agents.ai_kurator import create_task
from agents.ai_journalist import generate_post
from agents.ai_editor import review_post
from publisher import publish_post
from loguru import logger
import requests


async def send_admin_notification(token: str, message: str):
    """Отправляет уведомление администратору через Telegram."""
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {
            "chat_id": "@AdminChat",  # Заменить на реальный chat_id
            "text": message
        }
        response = requests.post(url, json=data)
        response.raise_for_status()
        logger.info("Admin notification sent")
    except Exception as e:
        logger.error(f"Admin notification error: {e}")


async def run_media_tact(project_dir: str):
    """Выполняет медиа-такт для проекта."""
    logger.info(f"Starting media tact for {project_dir}")
    try:
        # Загрузка конфигурации и расписания
        config, kurator_config, journalist_config, editor_config = load_config(project_dir)
        events, messages, polls = load_schedule(project_dir)

        # Определение временного окна
        tz = pytz.timezone(config.timezone)
        now = datetime.now(tz)
        window_start = now + timedelta(minutes=config.occasion_window[0])
        window_end = now + timedelta(minutes=config.occasion_window[1])

        # Формирование заданий
        tasks = await create_task(events, messages, now, window_start, window_end, kurator_config, project_dir)

        # Генерация и публикация постов
        for task in tasks:
            post = await generate_post(task, journalist_config, project_dir)
            if post:
                approved, action = await review_post(post, editor_config, project_dir)
                if approved and action == "publish":
                    await publish_post(post, config.telegram_token, project_dir)
    except Exception as e:
        logger.error(f"Media tact error in {project_dir}: {e}")
        await send_admin_notification(config.telegram_token, f"Error in {project_dir}: {e}")