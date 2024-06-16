from telegram_feature.telegram_utils import TelegramClient, read_tg_info
from telegram_feature.telegram_channels import tg_channels
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from datetime import datetime, timedelta
from telegram_feature.config import SESSION_STRING
import json
from reactions_predicting.predicter import reactions_predicter
import sqlite3
import pandas as pd
import mlflow
import os
import psycopg2
import joblib
import requests

api_id, api_hash = read_tg_info()
session_string = SESSION_STRING
client = TelegramClient(api_id, api_hash, session_string)
client.create_tables()
channels = tg_channels


MLFLOW_TRACKING_URI = "http://mlflow:5000"
MINIO_ENDPOINT_URL = "http://minio:9000"
AWS_ACCESS_KEY_ID = "minioadmin"
AWS_SECRET_ACCESS_KEY = "minioadmin"
experiment_name = "predict_posts"

def setup_mlflow():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    os.environ.update(
        {
            "MLFLOW_TRACKING_URI": MLFLOW_TRACKING_URI,
            "MLFLOW_S3_ENDPOINT_URL": MINIO_ENDPOINT_URL,
            "AWS_ACCESS_KEY_ID": AWS_ACCESS_KEY_ID,
            "AWS_SECRET_ACCESS_KEY": AWS_SECRET_ACCESS_KEY,
        }
    )
    mlflow.set_experiment(experiment_name)


def get_reactions(text: str):
    predicter = reactions_predicter()


def read_posts_from_db(database_path, table_name):
    db_con = psycopg2.connect(
        dbname="airflow",
        user="airflow",
        password="airflow",
        host="postgres_airflow",
    )
    cur = db_con.cursor()
    cur.execute(
        f"""
        SELECT p.post_id, p.post_text, STRING_AGG(emoji || count, ',' ORDER BY emoji) AS reactions_dictionary
        FROM {table_name} p
        INNER JOIN reactions r ON p.post_id = r.post_id
        GROUP BY p.post_id, p.post_text;
        """
    )
    data = pd.DataFrame(cur.fetchall(), columns=["post_id", "post_text", "reactions"])
    data = data.iloc[1:, :]
    data = data.set_index("post_id")
    return data


def main():
    setup_mlflow()
    run_name = f"Prediction Run - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    posts_with_reactions = read_posts_from_db("db/database.db", "posts")


    rp = reactions_predicter(posts_with_reactions, "reactions")
    prediction1 = rp.predict(text="кормен - лучшая книга по алгоритмам")
    prediction2 = rp.predict(text="террористы взяли в заложники автобус")
    run_name = f"Prediction Run - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    current_dir = os.path.dirname(__file__)
    model_dir = os.path.join(current_dir, "reactions_model")
    os.makedirs(model_dir, exist_ok=True)
    model_filename = "reactions_model.joblib"
    model_path = os.path.join(model_dir, model_filename)
    joblib.dump(rp, model_path)

    with open('prediction1.json', 'w', encoding='utf-8') as f:
        json.dump(prediction1, f, ensure_ascii=False)

    with open('prediction2.json', 'w', encoding='utf-8') as f:
        json.dump(prediction2, f, ensure_ascii=False)

    with mlflow.start_run(run_name=run_name):
        mlflow.log_param("Experiment", experiment_name)
        mlflow.log_artifact("prediction1.json")
        mlflow.log_artifact("prediction2.json")
        mlflow.sklearn.log_model(rp, "reactions_model")
        mlflow.log_artifact(model_path, artifact_path="reactions_model")

        model_uri = mlflow.get_artifact_uri("reactions_model")
        model_path = os.path.join(model_uri[:], "reactions_model.joblib")  
        print(model_path)
        url = "http://app:8000/load_model/" 

        payload = {
            "model_path": model_path
        }

        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, data=json.dumps(payload), headers=headers)
            response.raise_for_status()
            print("POST request successful!")
            print("Response:", response.json())
        except requests.exceptions.RequestException as e:
            print("Error sending POST request:", e)




def retrieve_posts(client, channel_id, n, **kwargs):
    try:
        client.get_n_last_posts(channel_id, n)
    except Exception as e:
        if 'FLOOD_WAIT' in str(e):
            wait_time = int(str(e).split()[-2])
            time.sleep(wait_time)
            client.get_n_last_posts(channel_id, n)
        else:
            raise e


def tg_channels_manager(**kwargs):
    ti = kwargs["ti"]
    channels_to_retrieve = {}
    for channel_id, should_retrieve in channels.items():
        if should_retrieve:
            channels_to_retrieve[f"retrieve_posts_channel_{channel_id}"] = True
    Variable.set(
        "channels_to_retrieve", json.dumps(channels_to_retrieve), serialize_json=True
    )
    return channels_to_retrieve


with DAG(
    "Mlops_pipline",
    description="Mlops_pipline",
    schedule_interval="@daily",
    catchup=False,
    max_active_runs=1, 
    concurrency=3,
    default_args={
        "owner": "bro",
        "start_date": datetime(2024, 2, 22),
        "retries": 6,
        "retry_delay": timedelta(minutes=0.5),
        "provide_context": True,
    },
) as dag:

    tg_channels_manager_task = BranchPythonOperator(
        task_id="tg_channels_manager",
        python_callable=tg_channels_manager,
        provide_context=True,
    )

    retrieve_posts_tasks = []
    for channel_id, should_retrieve in channels.items():
        retrieve_posts_task = PythonOperator(
            task_id=f"retrieve_posts_channel_{channel_id}",
            python_callable=retrieve_posts,
            op_args=[client, channel_id, 150],
            provide_context=True,
        )
        retrieve_posts_tasks.append(retrieve_posts_task)



    # Task to perform the main prediction and log results to MLflow
    main_task = PythonOperator(
        task_id="main_task",
        python_callable=main
    )

    # Setting up task dependencies
    tg_channels_manager_task >> retrieve_posts_tasks
    for task in retrieve_posts_tasks:
        task >> main_task


    
