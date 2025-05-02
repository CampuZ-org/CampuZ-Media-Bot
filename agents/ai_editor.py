from datetime import datetime, timedelta
from loguru import logger
from langchain_openai import ChatOpenAI


async def review_post(post: dict, config: dict, project_dir: str) -> tuple[bool, str]:
    """Проверяет пост с использованием LLM."""
    try:
        if not post["text"]:
            logger.warning(f"Empty post in {project_dir}")
            return False, "reject"

        # Проверка через LLM
        llm = ChatOpenAI(model="gpt-4o-mini", api_key=config.llm_api_key)
        prompt = (
            f"Проверь пост: {post['text']}. "
            f"Соответствует ли он профессиональному тону? "
            f"Есть ли ошибки или неуместный контент? "
            f"Верни 'approve' или 'reject'."
        )
        logger.debug(f"LLM request (editor): {prompt}")
        decision = await llm.apredict(prompt)
        logger.debug(f"LLM response (editor): {decision}")

        if decision.lower() != "approve":
            logger.warning(f"Post rejected in {project_dir}: {post['title']}")
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