from datetime import datetime, timedelta
from loguru import logger


async def review_post(post: dict, config: dict, project_dir: str) -> tuple[bool, str]:
    """Проверяет пост и решает, что с ним делать."""
    try:
        # Заглушка: проверка на наличие текста
        if not post["text"]:
            logger.warning(f"Empty post in {project_dir}")
            return False, "reject"

        # Проверка интервала
        last_publish_file = Path(f"/app/projects/{project_dir}/data/last_publish.txt")
        if last_publish_file.exists():
            with open(last_publish_file, "r") as f:
                last_time = datetime.fromisoformat(f.read())
            if datetime.now() - last_time < timedelta(minutes=config.min_interval_minutes):
                return True, "queue"

        # Сохранение времени публикации
        with open(last_publish_file, "w") as f:
            f.write(datetime.now().isoformat())

        return True, "publish"
    except Exception as e:
        logger.error(f"Post review error in {project_dir}: {e}")
        return False, "reject"
    