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

In this project, PostgreSQL is the core database system, used for efficient data storage and retrieval. The application connects to PostgreSQL using psycopg2, enabling operations with posts like data insertion, retrieval, update, and deletion. The database schema, defined within the application, supports the project's data model, ensuring the database structure aligns with the project's needs. 

### Fastapi
*localhost:8000*

FastAPI application provides a REST API for the project, handling GET and POST requests.

Features: \
• GET Request: Retrieves data from the root URL. \
• POST Request: Accepts user input to submit data to the /user endpoint.

### Html page
*localhost:8888*

The HTML page of the project is an interactive interface that provides basic information about the project and the technologies used in it. 

Supported sections: \
🏠 Main: Main page of the project. \
📚 Documentation: Documentation of the project. \
🛠️ Airflow: Information about Airflow. \
🤖 MLflow: Information about MLflow.

### Mlflow
*localhost:5000*

(Content about Mlflow)

### Minio
*localhost:9001*

(Content about Minio)

### Telegram bot
*@tg_post_analysis_bot*

Telegram bot is designed to provide users with information about different sections of the project.

Main functions: \
• User greeting \
• Section selection (look [html page](#html-page))\
• Extracting the contents of a section