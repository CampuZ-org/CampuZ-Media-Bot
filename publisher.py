from connectors.telegram import publish_to_telegram
from loguru import logger

async def publish_post(post: dict, telegram_token: str, project_dir: str):
    """Публикует пост в Telegram."""
    try:
        post_id = await publish_to_telegram(post, telegram_token)
        logger.info(f"Published post {post_id} for {project_dir}")
        # Сохранение статистики (заглушка)
        with open(f"/app/projects/{project_dir}/data/stats.csv", "a") as f:
            f.write(f"{post_id},{post['timestamp']},0,0,none\n")
    except Exception as e:
        logger.error(f"Publish error in {project_dir}: {e}")