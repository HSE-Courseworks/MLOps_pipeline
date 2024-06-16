from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from datetime import datetime, timedelta
from mlflow_experiments.main import train_and_predict_models, load_and_check_model
from mlflow_experiments.data_loader import load_iris_dataset
from mlflow_experiments.models import NaiveCustomModel
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
import json
import numpy as np
import mlflow
import os

MLFLOW_TRACKING_URI = "http://mlflow:5000"
MINIO_ENDPOINT_URL = "http://minio:9000"
AWS_ACCESS_KEY_ID = "minioadmin"
AWS_SECRET_ACCESS_KEY = "minioadmin"

experiment_name = "tests_ml"

RANDOM_FOREST = "RandomForest"
NAIVE_CUSTOM_MODEL = "NaiveCustomModel"
SIMPLE_AI_MODEL = "SimpleAIModel"


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


def train_and_predict_models_wrapper(
    model_func, name, X_train, y_train, X_test, y_test, **kwargs
):
    ti = kwargs["ti"]
    name, run_id, M1, P1 = train_and_predict_models(
        model_func, name, X_train, y_train, X_test, y_test
    )
    ti.xcom_push(key="name", value=name)
    ti.xcom_push(key="run_id", value=run_id)
    ti.xcom_push(key="M1", value=M1)
    ti.xcom_push(key="P1", value=P1.tolist())


def load_and_check_model_wrapper(name, **kwargs):
    ti = kwargs["ti"]
    name = ti.xcom_pull(key="name", task_ids=f"{name}_train_and_predict")
    run_id = ti.xcom_pull(key="run_id", task_ids=f"{name}_train_and_predict")
    M1 = ti.xcom_pull(key="M1", task_ids=f"{name}_train_and_predict")
    P1_list = ti.xcom_pull(key="P1", task_ids=f"{name}_train_and_predict")
    P1 = np.array(P1_list)
    load_and_check_model(run_id, name, X_test, y_test, P1, M1, experiment_name)


def test_manager(**kwargs):
    ti = kwargs["ti"]
    test_settings = {
        RANDOM_FOREST: True,
        NAIVE_CUSTOM_MODEL: True,
        SIMPLE_AI_MODEL: True,
    }

    models_to_test = {}
    for model_func, name in model_functions:
        if test_settings[name]:
            models_to_test[f"{name}_train_and_predict"] = True

    Variable.set("models_to_test", json.dumps(models_to_test), serialize_json=True)

    return models_to_test


with DAG(
    "mlflow_tests",
    description="Run models tests",
    schedule_interval="@daily",
    catchup=False,
    max_active_runs=1,
    concurrency=3,
    default_args={
        "owner": "airflow",
        "start_date": datetime(2024, 2, 27),
        "retries": 6,
        "retry_delay": timedelta(minutes=0.5),
        "provide_context": True,
    },
) as dag:

    setup_mlflow()

    X_train, X_test, y_train, y_test = load_iris_dataset()
    model_functions = [
        (
            lambda: RandomForestRegressor(n_estimators=100, random_state=42),
            RANDOM_FOREST,
        ),
        (lambda: NaiveCustomModel(), NAIVE_CUSTOM_MODEL),
        (lambda: LinearRegression(), SIMPLE_AI_MODEL),
    ]

    test_manager_task = BranchPythonOperator(
        task_id="test_manager",
        python_callable=test_manager,
        provide_context=True,
    )

    for model_func, name in model_functions:
        train_and_predict_task = PythonOperator(
            task_id=f"{name}_train_and_predict",
            python_callable=train_and_predict_models_wrapper,
            op_args=[model_func, name, X_train, y_train, X_test, y_test],
            provide_context=True,
        )

        load_and_check_task = PythonOperator(
            task_id=f"{name}_load_and_check",
            python_callable=load_and_check_model_wrapper,
            op_args=[name],
            provide_context=True,
        )

        test_manager_task >> train_and_predict_task >> load_and_check_task
