docker-compose \
    -f docker-compose.page_doc.yaml \
    -f docker-compose.FastAPI.yaml \
    -f docker-compose.airflow.yaml \
    -f docker-compose.minio.yaml \
    -f docker-compose.mlflow.yaml \
    --env-file ./env/.env.project down
sudo chown -R "$(id -u)" airflow/{logs,dags,plugins,config}
rm -rf FastAPI-app/app/__pycache__  airflow/plugins  airflow/config airflow/dags/__pycache__  airflow/logs
