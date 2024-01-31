#!/bin/bash
docker-compose -f page_documentation/docker-compose.yaml up -d
docker-compose -f FastAPI-app/docker-compose.yaml up -d
echo -e "AIRFLOW_UID=$(id -u)" > .env
docker-compose up -d airflow-init
docker-compose up -d
sudo bash ./minio/minio.sh
