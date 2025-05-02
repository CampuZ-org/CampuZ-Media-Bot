from connectors.telegram import publish_to_telegram
from loguru import logger
from monitor import increment_posts_published


async def publish_post(post: dict, telegram_token: str, project_dir: str):
    """Публикует пост в Telegram и сохраняет статистику."""
    try:
        post_id = await publish_to_telegram(post, telegram_token)
        logger.info(f"Published post {post_id} for {project_dir}")
        increment_posts_published()

        # Сохранение статистики (заглушка для просмотров и действий)
        views = 0  # Заменить на реальный вызов Telegram API
        actions = 0  # Например, голоса в опросах
        stats_file = f"/app/projects/{project_dir}/data/stats.csv"
        with open(stats_file, "a") as f:
            f.write(f"{post_id},{post['timestamp']},{views},{actions},{post['title']}\n")
    except Exception as e:
        logger.error(f"Publish error in {project_dir}: {e}")