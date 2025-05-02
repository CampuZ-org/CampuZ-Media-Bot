import asyncio
import os
from pathlib import Path
from loguru import logger
from media_tact import run_media_tact

async def cycle():
    """Запускает цикл обхода каждые 5 минут."""
    projects_dir = Path("/app/projects")
    while True:
        logger.info("Starting cycle")
        try:
            for project_dir in projects_dir.iterdir():
                if project_dir.is_dir():
                    await run_media_tact(project_dir.name)
        except Exception as e:
            logger.error(f"Cycle error: {e}")
        await asyncio.sleep(300)  # 5 минут

if __name__ == "__main__":
    logger.add("/data/logs/bot.log", rotation="100 MB", compression="gz")
    asyncio.run(cycle())