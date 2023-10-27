# MLOps_pipeline
## Running Airflow in Docker
To start Airflow, follow these steps:
1. Set the environment variable AIRFLOW_ID and save it to the .env file

```bash
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

2. Initialize the database

```bash
docker-compose up airflow-init
```

3. Launch docker-compose

```bash
docker-compose up
```