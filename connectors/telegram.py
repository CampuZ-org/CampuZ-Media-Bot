import requests
from loguru import logger
from schedule import load_schedule
from pathlib import Path

async def publish_to_telegram(post: dict, token: str) -> str:
    """Публикует пост, опрос или изображение в Telegram."""
    project_dir = post.get("project_dir", "")
    try:
        url = f"https://api.telegram.org/bot{token}/"
        chat_id = "@YourChannel"  # Заменить на реальный chat_id

        if post.get("poll"):
            # Загрузка опроса
            _, _, polls = load_schedule(project_dir)
            poll_data = polls.get(post["poll"], {})
            if not poll_data:
                raise ValueError(f"Poll {post['poll']} not found")

            data = {
                "chat_id": chat_id,
                "question": poll_data.get("Вопрос", "Опрос"),
                "options": poll_data.get("Варианты", "").split(","),
                "is_anonymous": True
            }
            endpoint = "sendPoll"
        elif post.get("image"):
            # Отправка изображения
            data = {
                "chat_id": chat_id,
                "photo": post["image"],
                "caption": f"**{post['title']}**\n{post['text']}\n{post['tags']}",
                "parse_mode": "Markdown"
            }
            endpoint = "sendPhoto"
        else:
            # Отправка текста
            data = {
                "chat_id": chat_id,
                "text": f"**{post['title']}**\n{post['text']}\n{post['tags']}",
                "parse_mode": "Markdown"
            }
            endpoint = "sendMessage"

        response = requests.post(url + endpoint, json=data)
        response.raise_for_status()
        return str(response.json().get("result", {}).get("message_id", "mock_id"))
    except Exception as e:
        logger.error(f"Telegram publish error: {e}")
        raise