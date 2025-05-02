# CampuZ-Media-Bot
Digital Media Team of AI-agent for your Events


```commandline
project_root/
├── main.py
├── config.py
├── schedule.py
├── media_tact.py
├── publisher.py
├── connectors/
│   ├── __init__.py
│   ├── telegram.py
├── agents/
│   ├── __init__.py
│   ├── ai_kurator.py
│   ├── ai_journalist.py
│   ├── ai_editor.py
├── utils.py
├── logger.py
├── monitor.py
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_schedule.py
│   ├── test_media_tact.py
│   ├── test_publisher.py
│   ├── test_agents.py
│   ├── mocks/
├── docs/
│   ├── api.md
│   ├── setup.md
├── examples/
│   ├── event_template/
│   │   ├── config.yaml
│   │   ├── schedule.xlsx
│   │   ├── ai_kurator.yaml
│   │   ├── ai_editor.yaml
│   │   ├── ai_journalist.yaml
│   │   ├── templates/
│   │   │   ├── post.yaml
│   │   ├── data/
│   │   │   ├── posts.db
│   │   │   ├── stats.csv
├── templates/
│   ├── post.yaml
├── requirements.txt
├── Dockerfile
└── docker-compose.yml

```

main.py
Запускает бота, реализует Цикл обхода каждые 5 минут, проверяет папки в /app/projects.

config.py
Обрабатывает конфигурационные файлы (config.yaml, ai_*.yaml) с валидацией через pydantic.

schedule.py
Читает и обрабатывает schedule.xlsx (вкладки: События, Сервисные сообщения, Опросы).

media_tact.py
Реализует Медиа-такт: проверяет конфигурацию, читает расписание, координирует ИИ-агентов и публикацию.

publisher.py
Управляет очередью постов и передаёт их в telegram.py.

connectors/telegram.py
Публикует посты в Telegram через Bot API.

agents/ai_kurator.py
Формирует задания для ИИ-журналиста.

agents/ai_journalist.py
Генерирует посты с учётом профиля и шаблона.

agents/ai_editor.py
Проверяет посты и принимает решения о публикации.

logger.py
Настраивает логирование с ротацией и сжатием.

examples/event_template/config.yaml
Пример конфигурации проекта.

examples/event_template/ai_kurator.yaml
Пример конфигурации куратора.

examples/event_template/ai_journalist.yaml
Пример конфигурации журналиста.

examples/event_template/ai_editor.yaml
Пример конфигурации редактора.

examples/event_template/templates/post.yaml
Пример шаблона поста.

templates/post.yaml
Дефолтный шаблон поста.

requirements.txt
Список зависимостей.

Dockerfile
Контейнеризация бота.

docker-compose.yml
Настройка Docker Compose.

Пояснения
LLM-заглушка: Реальная интеграция с LLM (OpenAI/Grok) требует настройки langchain и API-ключей в .env. Текущий код использует заглушки для генерации текста.
Telegram API: Реальная публикация требует настройки chat_id и токена в config.yaml. Текущий код отправляет тестовый запрос.
Тесты и документация: Пропущены, чтобы сократить объём. Могу добавить tests/*.py, docs/api.md, docs/setup.md по вашему запросу.
SQLite: База posts.db создаётся автоматически при первом запуске.
Логирование: Логи пишутся в /data/logs/ с ротацией.




