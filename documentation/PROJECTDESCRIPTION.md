## Description of the project's parts

```
run.sh
│
├───> docker-compose.airflow.yaml
│     ├───> airflow
│     └───> postgres
│
├───> docker-compose.FastAPI.yaml
│     └───> fastapi
│
├───> docker-compose.html_page.yaml
│     └───> html_page
│
├───> docker-compose.mlflow_minio.yaml
│     ├───> mlflow
│     └───> minio
│
└───> telegram_bot
```

## Table of Contents

- [Airflow](#airflow)
- [Postgres](#postgres)
- [Fastapi](#fastapi)
- [Html page](#html-page)
- [Mlflow](#mlflow)
- [Minio](#minio)
- [Telegram bot](#telegram-bot)

### Airflow
*localhost:8080*

(Content about Airflow)

### Postgres
*localhost:15432*

(Content about Postgres)

### Fastapi
*localhost:8000*

(Content about Fastapi)

### Html page
*localhost:8888*

(Content about Html page)

### Mlflow
*localhost:5000*

(Content about Mlflow)

### Minio
*localhost:9001*

(Content about Minio)

### Telegram bot

Telegram bot is designed to provide users with information about different sections of the project.

Main functions:
• User greeting
• Section selection
• Extracting the contents of a section

Supported sections:
🏠 Main: Main page of the project.
📚 Documentation: Documentation of the project.
🛠️ Airflow: Information about Airflow.
🤖 MLflow: Information about MLflow.