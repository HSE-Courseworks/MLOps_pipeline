mkdir -p ./data/pgadmin_db
chown -R 5050:5050 data/pgadmin_db
docker compose \
    -f docker-compose.html_page.yaml \
    -f docker-compose.FastAPI.yaml \
    -f docker-compose.airflow.yaml \
    -f docker-compose.mlflow_minio.yaml \
    --env-file ./env/.env.airflow \
    --env-file ./env/.env.mlflow \
    --env-file ./env/.env.minio up --build
