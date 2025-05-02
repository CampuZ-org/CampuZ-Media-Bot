import yaml
from pathlib import Path
from loguru import logger
from datetime import datetime
from langchain_openai import ChatOpenAI


async def generate_post(task: dict, config: dict, project_dir: str) -> dict:
    """Генерирует пост с использованием LLM."""
    try:
        occasion = task["occasion"]
        profile = config.profiles.get(task.get("profile", "default"), {})

        # Загрузка шаблона
        template_path = Path(f"/app/projects/{project_dir}/templates/post.yaml")
        if not template_path.exists():
            template_path = Path("/app/templates/post.yaml")
        with open(template_path, "r") as f:
            template = yaml.safe_load(f)["template"]

        # Генерация поста через LLM
        llm = ChatOpenAI(model="gpt-4o-mini", api_key=config.llm_api_key)
        prompt = (
            f"Создай пост для события: {occasion.get('Название', '')}. "
            f"Шаблон: {template}. "
            f"Стиль: {profile.get('tone', 'formal')}. "
            f"Язык: {config.get('language', 'ru')}. "
            f"Максимум 200 слов. "
            f"Добавь эмодзи: {profile.get('emojis', False)}."
        )
        logger.debug(f"LLM request (journalist): {prompt}")
        text = await llm.apredict(prompt)
        logger.debug(f"LLM response (journalist): {text}")

        tags = " ".join(f"#{t}" for t in occasion.get("Теги", "").split(",") if t)

        post = {
            "title": occasion.get("Название", ""),
            "text": text,
            "tags": tags,
            "image": occasion.get("Картинка", ""),
            "poll": occasion.get("Имя опроса", ""),
            "timestamp": datetime.now().isoformat(),
            "project_dir": project_dir
        }
        return post
    except Exception as e:
        logger.error(f"Post generation error in {project_dir}: {e}")
        return None