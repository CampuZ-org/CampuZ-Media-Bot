from langchain_openai import ChatOpenAI
from loguru import logger


def get_llm(config: dict) -> ChatOpenAI:
    """Инициализирует LLM на основе конфигурации."""
    try:
        llm_provider = config.get('llm_provider', 'openai')
        llm_kwargs = {"api_key": config.llm_api_key}

        if llm_provider == 'deepseek':
            llm_kwargs["base_url"] = config.get('llm_base_url', 'https://api.deepseek.com/v1')
            llm_kwargs["model"] = "deepseek-chat"
        else:
            llm_kwargs["model"] = "gpt-4o-mini"

        logger.info(f"Initializing LLM: {llm_provider}")
        return ChatOpenAI(**llm_kwargs)
    except Exception as e:
        logger.error(f"LLM initialization error: {e}")
        raise