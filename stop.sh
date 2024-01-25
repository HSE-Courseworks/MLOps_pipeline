#!/bin/bash
docker-compose -f project_page/docker-compose.yaml down
docker-compose -f FastAPI-app/docker-compose.yaml up -d
docker-compose down
sudo chown -R "$(id -u)" airflow/{logs,dags,plugins,config}
rm -rf FastAPI-app/app/__pycache__ 
rm .env
rm -rf airflow/plugins airflow/config airflow/dags/__pycache__ airflow/logs