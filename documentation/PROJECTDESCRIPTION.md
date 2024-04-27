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

Airflow in our project automates different parts of the project with the following key components:

DAGs:  
• **tg_data_dag**: Retrieves the last n posts from specified Telegram channels daily.  
• **mlflow_tests_dag**: Manages machine learning model testing. Includes tasks for setting up MLflow, loading datasets, training models, and checking model performance. 

### Postgres
*localhost:15432*

In this project, PostgreSQL is the core database system, used for efficient data storage and retrieval. The application connects to PostgreSQL using psycopg2, enabling operations with posts like data insertion, retrieval, update, and deletion. The database schema, defined within the application, supports the project's data model, ensuring the database structure aligns with the project's needs.  

### Fastapi
*localhost:8000*

FastAPI application provides a REST API for the project, handling GET and POST requests.

Features:  
• **GET Request**: Retrieves data from the root URL.  
• **POST Request**: Accepts user input to submit data to the /user endpoint.  

### Html page
*localhost:8888*

The HTML page of the project is an interactive interface that provides basic information about the project and the technologies used in it. 

Supported sections:  
🏠 **Main**: Main page of the project.  
📚 **Documentation**: Documentation of the project.  
🛠️ **Airflow**: Information about Airflow.  
🤖 **MLflow**: Information about MLflow.  

### Mlflow
*localhost:5000*

MLflow in our project is used for managing the machine learning lifecycle, including model training, prediction, and performance evaluation. 

Stages:
1. **Setup**: Configuring MLflow with a tracking URI and MinIO storage details.  
2. **Model training and prediction**: Training models with provided functions and datasets, logging results to MLflow.  
3. **Model loading and checking**: Retrieving logged model information and assessing performance on test data.  
4. **Model testing**: Deciding which models to test based on predefined settings, using Airflow to orchestrate the process.  

### Minio
*localhost:9001*

In our project, MinIO is utilized as a storage solution for machine learning artifacts and models, working in conjunction with MLflow. It's configured with specific access and secret keys for secure data management.  

### Telegram bot
*@tg_post_analysis_bot*

Telegram bot is designed to provide users with information about different sections of the project.  

Main functions:  
• **User greeting**  
• **Section selection** (look [html page](#html-page))  
• **Extracting the contents of a section**  