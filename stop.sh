kill $(pgrep -f telegram_bot.py)

docker compose \
    -f docker-compose.html_page.yaml \
    -f docker-compose.FastAPI.yaml \
    -f docker-compose.airflow.yaml \
    -f docker-compose.mlflow_minio.yaml \
    -f docker-compose.grafana_prometheus.yaml \
    --env-file ./env/.env.airflow \
    --env-file ./env/.env.mlflow \
    --env-file ./env/.env.minio down
    
sudo chown -R "$(id -u)" airflow/{logs,dags,plugins,config}
sudo rm -rf FastAPI-app/.pytest_cache FastAPI-app/__pycache__ FastAPI-app/app/__pycache__  airflow/plugins  airflow/config airflow/dags/__pycache__ \
            airflow/logs airflow/dags/telegram_feature telegram_feature/__pycache__ mlflow_experiments/__pycache__ \
            airflow/dags/mlflow_experiments
