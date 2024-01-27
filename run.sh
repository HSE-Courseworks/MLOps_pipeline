#!/bin/bash
docker-compose -f page_documentation/docker-compose.yaml up -d
docker-compose -f FastAPI-app/docker-compose.yaml up -d
cd page_documentation/documentation/
python3 main.py
cd ..
cd ..
echo -e "AIRFLOW_UID=$(id -u)" > .env
docker-compose up airflow-init 
docker-compose up
