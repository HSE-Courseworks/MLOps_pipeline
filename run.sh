#!/bin/bash
docker-compose -f project_page/docker-compose.yaml up -d
docker-compose -f FastAPI-app/docker-compose.yaml up -d
echo -e "AIRFLOW_UID=$(id -u)" > .env
docker-compose up airflow-init
docker-compose up -d

