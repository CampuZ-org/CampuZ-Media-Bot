import yaml
from pathlib import Path
from loguru import logger
from datetime import datetime


async def generate_post(task: dict, config: dict, project_dir: str) -> dict:
    """Генерирует пост."""
    try:
        occasion = task["occasion"]
        profile = config.profiles.get(task.get("profile", "default"), {})

        # Загрузка шаблона
        template_path = Path(f"/app/projects/{project_dir}/templates/post.yaml")
        if not template_path.exists():
            template_path = Path("/app/templates/post.yaml")
        with open(template_path, "r") as f:
            template = yaml.safe_load(f)["template"]

        # Заглушка для LLM
        text = template.format(
            title=occasion.get("Название", ""),
            room=occasion.get("Зал", ""),
            start_time=occasion.get("Время начала", occasion.get("Время", ""))
        )
        tags = " ".join(f"#{t}" for t in occasion.get("Теги", "").split(",") if t)

        post = {
            "title": occasion.get("Название", ""),
            "text": text,
            "tags": tags,
            "image": occasion.get("Картинка", ""),
            "poll": occasion.get("Имя опроса", ""),
            "timestamp": datetime.now().isoformat()
        }
        return post
    except Exception as e:
        logger.error(f"Post generation error in {project_dir}: {e}")
        return None