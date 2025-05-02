from loguru import logger

def setup_logger(project_dir: str):
    """Настраивает логирование для проекта."""
    logger.add(
        f"/app/projects/{project_dir}/data/logs/{{time}}.log",
        rotation="100 MB",
        compression="gz",
        level="INFO"
    )
