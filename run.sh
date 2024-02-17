docker compose \
    -f docker-compose.page_doc.yaml \
    -f docker-compose.FastAPI.yaml \
    -f docker-compose.airflow.yaml \
    -f docker-compose.mlflow_minio.yaml \
    --env-file ./env/.env.airflow \
    --env-file ./env/.env.mlflow \
    --env-file ./env/.env.minio up
