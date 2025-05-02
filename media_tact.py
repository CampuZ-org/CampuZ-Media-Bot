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
        # Уведомление администратору (заглушка)
        logger.warning("Sending Telegram notification to admin")