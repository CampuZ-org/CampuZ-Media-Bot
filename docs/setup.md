# Setup Instructions

# Prerequisites

Docker and Docker Compose installed.
Python 3.11 (optional for local development).
Telegram Bot token and LLM API key.


# Installation

Clone the repository:
```commandline
git clone <repository-url>
cd <repository>
```


Create .env file:
```commandline
echo "TELEGRAM_TOKEN=your-telegram-token" > .env
echo "LLM_API_KEY=your-llm-api-key" >> .env
```


Build and run with Docker:
```commandline
docker-compose up --build
```


# Configuration

Create a project folder in `/app/projects/<project_name>`.
Add `config.yaml`, `ai_kurator.yaml`, `ai_journalist.yaml`, `ai_editor.yaml`, and `schedule.xlsx` (see `examples/event_template`).
Ensure `/templates/post.yaml` exists or use the default in `/app/templates`.

Running Locally
```commandline
pip install -r requirements.txt
python main.py
```

# Monitoring

Metrics available at `http://localhost:8000/metrics`.
Logs stored in `/app/projects/<project_name>/data/logs/`.

