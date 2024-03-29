docker compose \
    -f docker-compose.html_page.yaml \
    -f docker-compose.FastAPI.yaml \
    -f docker-compose.airflow.yaml \
    -f docker-compose.mlflow_minio.yaml \
    --env-file ./env/.env.airflow \
    --env-file ./env/.env.mlflow \
    --env-file ./env/.env.minio down
sudo chown -R "$(id -u)" airflow/{logs,dags,plugins,config}
sudo rm -rf FastAPI-app/app/__pycache__  airflow/plugins  airflow/config airflow/dags/__pycache__ \
            airflow/logs airflow/dags/telegram_feature telegram_feature/__pycache__ mlflow_experiments/__pycache__ \
            airflow/dags/mlflow_experiments
