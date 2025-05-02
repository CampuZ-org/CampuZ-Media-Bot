from datetime import datetime
from typing import List, Dict
from loguru import logger
import sqlite3
from sentence_transformers import SentenceTransformer, util
from langchain_openai import ChatOpenAI
from utils import compute_vector, compare_vectors

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')


async def create_task(events: List[Dict], messages: List[Dict], now: datetime, window_start: datetime,
                      window_end: datetime, config: dict, project_dir: str) -> List[Dict]:
    """Формирует задания для журналиста с использованием LLM."""
    tasks = []
    db_path = f"/app/projects/{project_dir}/data/posts.db"
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=config.llm_api_key)

    # Инициализация базы
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS posts (vector BLOB, timestamp TEXT, post_id TEXT)")

    for event in events + messages:
        event_time = datetime.fromisoformat(event.get("Время") or event.get("Время начала"))
        if window_start <= event_time <= window_end:
            # Векторизация повода
            text = f"{event.get('Название', '')} {event.get('Анонс', event.get('Описание', ''))}"
            vector = compute_vector(text)

            # Проверка дубликатов
            cursor.execute("SELECT vector FROM posts WHERE timestamp > ?",
                           [(now - timedelta(hours=config.vector_lag_hours)).isoformat()])
            existing_vectors = [row[0] for row in cursor.fetchall()]
            is_duplicate = any(compare_vectors(vector, ev) > 0.9 for ev in existing_vectors)

            if not is_duplicate:
                # Генерация текстовой постановки через LLM
                prompt = f"Сформулируй задание для поста: {text}. Язык: {config.get('language', 'ru')}."
                logger.debug(f"LLM request (kurator): {prompt}")
                response = await llm.apredict(prompt)
                logger.debug(f"LLM response (kurator): {response}")

                task = {
                    "occasion": event,
                    "text": response,
                    "profile": config.profile
                }
                tasks.append(task)
                cursor.execute("INSERT INTO posts (vector, timestamp, post_id) VALUES (?, ?, ?)",
                               (vector.tobytes(), now.isoformat(), "pending"))

    conn.commit()
    conn.close()
    return tasks