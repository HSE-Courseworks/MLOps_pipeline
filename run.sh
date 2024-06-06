python3 telegram_feature/telegram_bot.py &

docker compose \
    -f docker-compose.html_page.yaml \
    -f docker-compose.FastAPI.yaml \
    -f docker-compose.airflow.yaml \
    -f docker-compose.mlflow_minio.yaml \
    -f docker-compose.grafana_prometheus.yaml \
    --env-file ./env/.env.airflow \
    --env-file ./env/.env.mlflow \
    --env-file ./env/.env.minio up --build
