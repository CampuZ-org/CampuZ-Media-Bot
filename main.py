import asyncio
import os
import signal
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

async def shutdown(loop):
    """Обрабатывает graceful shutdown."""
    logger.info("Received shutdown signal, stopping...")
    tasks = [task for task in asyncio.all_tasks(loop) if task is not asyncio.current_task()]
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()
    logger.info("Shutdown complete")

def handle_shutdown(loop):
    """Регистрирует обработчики сигналов."""
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown(loop)))

if __name__ == "__main__":
    logger.add("/data/logs/bot.log", rotation="100 MB", compression="gz")
    loop = asyncio.get_event_loop()
    handle_shutdown(loop)
    try:
        loop.run_until_complete(cycle())
    except asyncio.CancelledError:
        pass
    finally:
        loop.run_until_complete(shutdown(loop))