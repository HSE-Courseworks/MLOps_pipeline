cat ./env/.env.airflow ./env/.env.mlflow ./env/.env.minio > ./env/.env.project
docker-compose \
    -f docker-compose.page_doc.yaml \
    -f docker-compose.FastAPI.yaml \
    -f docker-compose.airflow.yaml \
    -f docker-compose.minio.yaml \
    -f docker-compose.mlflow.yaml \
    --env-file ./env/.env.project up
