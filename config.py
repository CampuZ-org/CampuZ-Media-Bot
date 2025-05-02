from pydantic import BaseModel
from typing import Optional
import yaml
from pathlib import Path
from loguru import logger


class Config(BaseModel):
    timezone: str
    llm_provider: str
    llm_api_key: str
    telegram_token: str
    vector_lag_hours: int = 24
    occasion_window: tuple[int, int] = (-10, 20)


class KuratorConfig(BaseModel):
    media_task: str
    profile: Optional[str] = None


class JournalistConfig(BaseModel):
    media_task: str
    profiles: dict[str, dict]


class EditorConfig(BaseModel):
    media_task: str
    min_interval_minutes: int = 5


def load_config(project_dir: str) -> tuple[Config, KuratorConfig, JournalistConfig, EditorConfig]:
    """Загружает и валидирует конфигурации."""
    base_path = Path(f"/app/projects/{project_dir}")
    try:
        with open(base_path / "config.yaml", "r") as f:
            config_data = yaml.safe_load(f)
        with open(base_path / "ai_kurator.yaml", "r") as f:
            kurator_data = yaml.safe_load(f)
        with open(base_path / "ai_journalist.yaml", "r") as f:
            journalist_data = yaml.safe_load(f)
        with open(base_path / "ai_editor.yaml", "r") as f:
            editor_data = yaml.safe_load(f)

        return (
            Config(**config_data),
            KuratorConfig(**kurator_data),
            JournalistConfig(**journalist_data),
            EditorConfig(**editor_data)
        )
    except Exception as e:
        logger.error(f"Config load error in {project_dir}: {e}")
        raise